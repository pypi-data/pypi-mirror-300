from __future__ import annotations

import os
import typing
from io import BytesIO

import pytest
from pgpq import ArrowToPostgresBinaryEncoder
from pyarrow import parquet
from tests.helpers import count_rows_in_test_table

from psqlpy import ConnectionPool, Cursor, QueryResult, Transaction
from psqlpy.exceptions import (
    ConnectionClosedError,
    ConnectionExecuteError,
    TransactionExecuteError,
)

pytestmark = pytest.mark.anyio


async def test_connection_execute(
    psql_pool: ConnectionPool,
    table_name: str,
    number_database_records: int,
) -> None:
    """Test that single connection can execute queries."""
    connection = await psql_pool.connection()

    conn_result = await connection.execute(
        querystring=f"SELECT * FROM {table_name}",
    )
    assert isinstance(conn_result, QueryResult)
    assert len(conn_result.result()) == number_database_records


async def test_connection_fetch(
    psql_pool: ConnectionPool,
    table_name: str,
    number_database_records: int,
) -> None:
    """Test that single connection can fetch queries."""
    connection = await psql_pool.connection()

    conn_result = await connection.fetch(
        querystring=f"SELECT * FROM {table_name}",
    )
    assert isinstance(conn_result, QueryResult)
    assert len(conn_result.result()) == number_database_records


async def test_connection_connection(
    psql_pool: ConnectionPool,
) -> None:
    """Test that connection can create transactions."""
    connection = await psql_pool.connection()
    transaction = connection.transaction()

    assert isinstance(transaction, Transaction)


@pytest.mark.parametrize(
    ("insert_values"),
    [
        [[1, "name1"], [2, "name2"]],
        [[10, "name1"], [20, "name2"], [30, "name3"]],
        [[1, "name1"]],
        [],
    ],
)
async def test_connection_execute_many(
    psql_pool: ConnectionPool,
    table_name: str,
    number_database_records: int,
    insert_values: list[list[typing.Any]],
) -> None:
    connection = await psql_pool.connection()
    try:
        await connection.execute_many(
            f"INSERT INTO {table_name} VALUES ($1, $2)",
            insert_values,
        )
    except TransactionExecuteError:
        assert not insert_values
    else:
        assert await count_rows_in_test_table(
            table_name,
            connection,
        ) - number_database_records == len(insert_values)


async def test_connection_fetch_row(
    psql_pool: ConnectionPool,
    table_name: str,
) -> None:
    connection = await psql_pool.connection()
    database_single_query_result: typing.Final = await connection.fetch_row(
        f"SELECT * FROM  {table_name} LIMIT 1",
        [],
    )
    result = database_single_query_result.result()
    assert isinstance(result, dict)


async def test_connection_fetch_row_more_than_one_row(
    psql_pool: ConnectionPool,
    table_name: str,
) -> None:
    connection = await psql_pool.connection()
    with pytest.raises(ConnectionExecuteError):
        await connection.fetch_row(
            f"SELECT * FROM  {table_name}",
            [],
        )


async def test_connection_fetch_val(
    psql_pool: ConnectionPool,
    table_name: str,
) -> None:
    connection = await psql_pool.connection()
    value: typing.Final = await connection.fetch_val(
        f"SELECT COUNT(*) FROM {table_name}",
        [],
    )
    assert isinstance(value, int)


async def test_connection_fetch_val_more_than_one_row(
    psql_pool: ConnectionPool,
    table_name: str,
) -> None:
    connection = await psql_pool.connection()
    with pytest.raises(ConnectionExecuteError):
        await connection.fetch_row(
            f"SELECT * FROM  {table_name}",
            [],
        )


async def test_connection_cursor(
    psql_pool: ConnectionPool,
    table_name: str,
    number_database_records: int,
) -> None:
    """Test cursor from Connection."""
    connection = await psql_pool.connection()
    cursor: Cursor
    all_results: list[dict[typing.Any, typing.Any]] = []

    async with connection.transaction(), connection.cursor(
        querystring=f"SELECT * FROM {table_name}",
    ) as cursor:
        async for cur_res in cursor:
            all_results.extend(cur_res.result())

    assert len(all_results) == number_database_records


async def test_connection_async_context_manager(
    psql_pool: ConnectionPool,
    table_name: str,
    number_database_records: int,
) -> None:
    """Test connection as a async context manager."""
    async with psql_pool.acquire() as connection:
        conn_result = await connection.execute(
            querystring=f"SELECT * FROM {table_name}",
        )
        assert not psql_pool.status().available

    assert psql_pool.status().available == 1

    assert isinstance(conn_result, QueryResult)
    assert len(conn_result.result()) == number_database_records


async def test_closed_connection_error(
    psql_pool: ConnectionPool,
) -> None:
    """Test exception when connection is closed."""
    connection = await psql_pool.connection()
    connection.back_to_pool()

    with pytest.raises(expected_exception=ConnectionClosedError):
        await connection.execute("SELECT 1")


async def test_binary_copy_to_table(
    psql_pool: ConnectionPool,
) -> None:
    """Test binary copy in connection."""
    table_name: typing.Final = "cars"
    await psql_pool.execute(f"DROP TABLE IF EXISTS {table_name}")
    await psql_pool.execute(
        """
CREATE TABLE IF NOT EXISTS cars (
    model VARCHAR,
    mpg FLOAT8,
    cyl INTEGER,
    disp FLOAT8,
    hp INTEGER,
    drat FLOAT8,
    wt FLOAT8,
    qsec FLOAT8,
    vs INTEGER,
    am INTEGER,
    gear INTEGER,
    carb INTEGER
);
""",
    )

    arrow_table = parquet.read_table(
        f"{os.path.dirname(os.path.abspath(__file__))}/test_data/MTcars.parquet",  # noqa: PTH120, PTH100
    )
    encoder = ArrowToPostgresBinaryEncoder(arrow_table.schema)
    buf = BytesIO()
    buf.write(encoder.write_header())
    for batch in arrow_table.to_batches():
        buf.write(encoder.write_batch(batch))
    buf.write(encoder.finish())
    buf.seek(0)

    async with psql_pool.acquire() as connection:
        inserted_rows = await connection.binary_copy_to_table(
            source=buf,
            table_name=table_name,
        )

    expected_inserted_row: typing.Final = 32

    assert inserted_rows == expected_inserted_row

    real_table_rows: typing.Final = await psql_pool.execute(
        f"SELECT COUNT(*) AS rows_count FROM {table_name}",
    )
    assert real_table_rows.result()[0]["rows_count"] == expected_inserted_row


async def test_execute_batch_method(psql_pool: ConnectionPool) -> None:
    """Test `execute_batch` method."""
    await psql_pool.execute(querystring="DROP TABLE IF EXISTS execute_batch")
    await psql_pool.execute(querystring="DROP TABLE IF EXISTS execute_batch2")
    query = "CREATE TABLE execute_batch (name VARCHAR);CREATE TABLE execute_batch2 (name VARCHAR);"
    async with psql_pool.acquire() as conn:
        await conn.execute_batch(querystring=query)
        await conn.execute(querystring="SELECT * FROM execute_batch")
        await conn.execute(querystring="SELECT * FROM execute_batch2")
