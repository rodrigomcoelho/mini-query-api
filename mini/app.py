from http import HTTPStatus

from fastapi import Body, FastAPI, Path
from loguru import logger

from mini.bigquery import BigQueryExporter
from mini.db import DuckDB
from mini.models import RegisterEntityModel, UpdateEntityModel
from mini.utils.request import parser_page_query, parser_record_key
from mini.utils.storage import get_export_path, get_import_path

app = FastAPI()


@app.get(path="/entities/{entity}/definition", status_code=HTTPStatus.OK)
async def get_entity_definition(entity: str = Path(default=...)):
    with DuckDB() as db:
        return {"definition": db.get_entity_definition(entity)}


@app.get(
    path="/entities/{entity_id}/records/{record_id}", status_code=HTTPStatus.OK
)
async def get_table(
    entity_id: str = Path(default=...),
    record_id: str = Path(default=...),
):

    parsed_key = parser_record_key(record_id)
    with DuckDB() as db:
        return {
            "entity": entity_id,
            "data": [db.fetch_one(entity_id, where=parsed_key)],
        }


@app.get(path="/entities/{entity_id}/records", status_code=HTTPStatus.OK)
async def get_table(
    entity_id: str = Path(default=...),
    page: int | None = None,
):
    logger.debug("Getting table: {} - page {}", entity_id, page)
    parsed_page = parser_page_query(page)

    with DuckDB() as db:
        return {
            "entity": entity_id,
            "data": list(db.fetch_many(entity_id, offset=parsed_page)),
        }


@app.get(path="/entities", status_code=HTTPStatus.OK)
async def get_all_entities():
    with DuckDB() as db:
        return {"entities": db.get_entities()}


@app.post(path="/entities", status_code=HTTPStatus.CREATED)
async def register_new_entity(
    entity: RegisterEntityModel = Body(default_factory=RegisterEntityModel),
):
    with BigQueryExporter() as bq:
        bq.query(entity.query).export(get_export_path(entity.entityName))

    with DuckDB(read_only=False) as db:
        db.load_table(
            path=get_import_path(entity.entityName),
            format="parquet",
            table=entity.entityName,
            index=entity.indexField,
        )


@app.put(path="/entities/{entity_id}", status_code=HTTPStatus.OK)
async def register_new_entity(
    entity_id: str = Path(default=...),
    entity: UpdateEntityModel = Body(default_factory=UpdateEntityModel),
):
    with BigQueryExporter() as bq:
        bq.query(entity.query).export(get_export_path(entity_id))

    with DuckDB(read_only=False) as db:
        db.load_table(
            path=get_import_path(entity_id),
            format="parquet",
            table=entity_id,
            overwrite=True,
            index=entity.indexField,
        )


@app.get(path="/", status_code=HTTPStatus.OK)
async def home():
    return {"status": "healthy"}
