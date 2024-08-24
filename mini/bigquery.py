from os import getenv

from google.cloud.bigquery import Client as BigQueryClient
from loguru import logger


class BigQueryExporter:
    def __init__(self, project_id: str | None = None):
        self.__project_id: str = project_id or getenv("GOOGLE_CLOUD_PROJECT")
        self.__statement: str | None = None
        self.__bq_client: BigQueryClient | None = None

    def __enter__(self) -> "BigQueryExporter":
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def open(self, read_only: bool = True) -> None:
        self.__bq_client = BigQueryClient(project=self.__project_id)

    def close(self) -> None:
        self.__bq_client.close()

    def query(self, statement: str) -> "BigQueryExporter":
        if not isinstance(statement, str):
            raise ValueError("Statement must be a string")

        self.__statement = statement
        return self

    def __build_export_statement(self, storage_path: str) -> str:
        if not self.__statement:
            raise ValueError("Statement must be set")

        options = (
            "format='PARQUET'",
            "compression='SNAPPY'",
            "overwrite=true",
        )

        options_str = ", ".join(options)

        export_statement = (
            "EXPORT DATA OPTIONS(uri='{storage_path}', {options})\n"
        )
        export_statement += "AS {query}"

        return export_statement.format(
            storage_path=storage_path,
            options=options_str,
            query=self.__statement,
        )

    def export(self, destination: str) -> None:

        statement = self.__build_export_statement(destination)

        logger.debug("Exporting data to {}", destination)
        logger.debug("Statement: {}", statement)

        self.__bq_client.query_and_wait(query=statement)
        logger.debug("Exported data to {}", destination)
