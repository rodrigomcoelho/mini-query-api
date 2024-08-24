from pydantic import BaseModel


class EntityModel(BaseModel):
    entity: str
    data: list[dict]
    totalRows: int


class RegisterEntityModel(BaseModel):
    query: str
    entityName: str
    indexField: str | None


class UpdateEntityModel(BaseModel):
    query: str
    indexField: str | None
