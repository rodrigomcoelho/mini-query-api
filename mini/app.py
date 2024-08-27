from http import HTTPStatus

from fastapi import Body, FastAPI, Path

from mini.bigquery import BigQueryExporter
from mini.db import DuckDB
from mini.models import RegisterEntityModel, UpdateEntityModel
from mini.utils.request import parser_page_query, parser_record_key, validate_entity
from mini.utils.storage import get_export_path, get_import_path

app = FastAPI()


@app.get(path="/entities/{entity_id}/definition", status_code=HTTPStatus.OK)
async def entity_definition(entity_id: str = Path(default=...)):
    validate_entity(entity_id)
    with DuckDB() as db:
        return {"definition": db.get_entity_definition(entity_id)}


@app.get(path="/entities/{entity_id}/summarize", status_code=HTTPStatus.OK)
async def summarize_entity(entity_id: str = Path(default=...)):
    validate_entity(entity_id)
    with DuckDB() as db:
        return {"summary": db.summarize_entity(entity_id)}


@app.get(
    path="/entities/{entity_id}/records/field/{record_key}/value/{record_id}", status_code=HTTPStatus.OK
)
async def fetch_one_entity_record_by_key(
    entity_id: str = Path(default=...),
    record_key: str = Path(default=...),
    record_id: str = Path(default=...),
):
    validate_entity(entity_id)
    with DuckDB() as db:
        return {
            "entity": entity_id,
            "data": [db.fetch_one(entity_id, key=record_key, value=record_id)],
        }


@app.get(path="/entities/{entity_id}/records", status_code=HTTPStatus.OK)
async def fetch_all_entity_records(
    entity_id: str = Path(default=...),
    page: int | None = None,
):
    validate_entity(entity_id)
    parsed_page = parser_page_query(page)

    with DuckDB() as db:
        return {
            "entity": entity_id,
            "data": list(db.fetch_many(entity_id, offset=parsed_page)),
        }


@app.get(path="/entities", status_code=HTTPStatus.OK)
async def fetch_all_entities():
    with DuckDB() as db:
        return {"entities": db.get_entities()}


@app.post(path="/entities", status_code=HTTPStatus.CREATED)
async def register_new_entity(
    entity: RegisterEntityModel = Body(default_factory=RegisterEntityModel),
):
    validate_entity(entity.entityName)

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
async def update_exisiting_entity(
    entity_id: str = Path(default=...),
    entity: UpdateEntityModel = Body(default_factory=UpdateEntityModel),
):
    validate_entity(entity_id)
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
async def health_status():
    return {"status": "healthy"}
