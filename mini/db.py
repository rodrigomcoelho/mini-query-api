from os import getenv
from os.path import exists

from duckdb import (
    CatalogException,
    ColumnExpression,
    ConstantExpression,
    DuckDBPyConnection,
    IOException,
    connect,
)
from humanize import naturalsize
from loguru import logger

from mini.exceptions import (
    EntityAlreadyRegisteredException,
    EntityNotFoundException,
    NotEvenOneEntityHasBeenRegisteredExeption,
    RecordNotFoundException,
)
from mini.utils.decorators import howlong


def to_camel_case(text: str) -> str:
    parts = text.split("_")
    camel_case_string = parts[0] + "".join(
        word.capitalize() for word in parts[1:]
    )

    return camel_case_string


class DuckDB:
    _EXTENSIONS = ("httpfs",)

    def __init__(self, read_only: bool = True) -> None:
        self.__conn: DuckDBPyConnection = None
        self.__read_only = read_only

    def __enter__(self) -> "DuckDB":
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def open(self) -> None:
        try:
            self.__conn = connect(
                database="./data/db.duckdb",
                read_only=self.__read_only,
            )

            if not self.__read_only and exists("./data/db.duckdb"):
                self.__prepare_enviroment()

        except IOException as error:
            logger.error("Error opening connection: {}", error)
            raise NotEvenOneEntityHasBeenRegisteredExeption(
                "No entity has been registered."
            )

    def close(self) -> None:
        self.__conn.close()

    def __get_hmac_key_configuration(self) -> tuple[str]:
        access_id = getenv("GOOGLE_CLOUD_STORAGE_HMAC_ACCESS_KEY")
        secret_key = getenv("GOOGLE_CLOUD_STORAGE_HMAC_SECRET")

        content = ", ".join(
            (
                "TYPE GCS",
                f"KEY_ID '{access_id}'",
                f"SECRET '{secret_key}'",
            )
        )

        return (f"CREATE SECRET ({content});",)

    def __prepare_enviroment(self) -> None:

        for extension in self._EXTENSIONS:
            self.__conn.install_extension(extension)
            self.__conn.load_extension(extension)

        for config in self.__get_hmac_key_configuration():
            self.__conn.execute(config)

    @howlong
    def load_table(
        self,
        path: str,
        format: str,
        table: str,
        *,
        index: str | None = None,
        overwrite: bool = False,
    ) -> None:

        if overwrite:
            self.__conn.sql(f"DROP TABLE IF EXISTS {table};")
            self.__conn.sql(f"DROP INDEX IF EXISTS {table}__{index}__idx;")

        try:
            self.__conn.read_parquet(
                file_glob=f"{path}/*.{format}",
                hive_partitioning=False,
                compression="snappy",
            ).create(table)

        except CatalogException as error:
            if "Table with name" in str(error) and "already exists" in str(
                error
            ):
                raise EntityAlreadyRegisteredException(
                    f"Entity {table} already registered"
                )
            raise error
        except Exception as error:
            raise error

        if index:
            index_statement = f"CREATE UNIQUE INDEX {table}__{index}__idx ON {table} ({index});"
            logger.debug(index_statement)
            self.__conn.sql(index_statement)

    def __table_columns(self, table_name: str) -> list[str]:
        return self.__conn.table(table_name).columns

    def get_entities(self) -> list[dict]:
        result = (
            self.__conn.table("duckdb_tables")
            .select("table_name", "estimated_size")
            .fetchall()
        )
        entities = []
        for table, size in result:
            entities.append(
                {"entitiyName": table, "estimatedSize": naturalsize(size)}
            )

        return entities

    def get_entity_definition(self, table_name: str) -> dict:
        key = ColumnExpression("table_name")
        value = ConstantExpression(table_name)
        selected_columns = (
            "column_name",
            "data_type",
            "column_index",
            "is_nullable",
            "column_default",
            "character_maximum_length",
            "numeric_precision",
            "numeric_scale",
        )
        response = (
            self.__conn.table("duckdb_columns")
            .filter(key == value)
            .select(*selected_columns)
        )

        result: list[dict] = []

        for rows in response.fetchall():
            row = {}
            for index, key in enumerate(selected_columns):
                value = rows[index]
                if value is None:
                    continue
                row[to_camel_case(key)] = value

            result.append(row)

        if not result:
            raise EntityNotFoundException(f"Entity {table_name} not found")

        return result

    @howlong
    def fetch_one(self, table_name: str, where: list[str]) -> dict:
        key, value = where

        key = ColumnExpression(key)
        value = ConstantExpression(value)

        try:
            result = (
                self.__conn.table(table_name)
                .filter(key == value)
                .limit(1)
                .fetchone()
            )
        except CatalogException as error:
            logger.error("Error fetching data: {}", error)
            raise EntityNotFoundException(f"Entity {table_name} not found")

        if not result:
            raise RecordNotFoundException(f"Record '{key}={value}' not found")

        columns = self.__table_columns(table_name)

        return dict(zip(columns, result))

    @howlong
    def fetch_many(
        self, table_name: str, limit: int = 100, offset: int = 0
    ) -> list[dict]:
        try:
            result = (
                self.__conn.table(table_name).limit(limit, offset).fetchall()
            )
        except CatalogException as error:
            logger.error("Error fetching data: {}", error)
            raise EntityNotFoundException(f"Entity {table_name} not found")

        if not result:
            []

        columns = self.__table_columns(table_name)

        return map(lambda x: dict(zip(columns, x)), result)
