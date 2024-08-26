from re import compile

from mini.exceptions import (
    InvalidEntityFormatError,
    InvalidRecordKeyError,
    PageQueryError,
)


def parser_record_key(record_key: str) -> dict:
    splitted = record_key.split(":")

    if len(splitted) != 2:
        raise InvalidRecordKeyError(
            "Record key must be in the format 'key:value'"
        )

    return splitted


def parser_page_query(page: str | None) -> int:
    try:
        if page is None:
            return 0

        parsed_int = int(page)
        if parsed_int < 1:
            raise PageQueryError("Page must be greater than 0")

        parsed_int = (parsed_int - 1) * 100

        return parsed_int

    except Exception:
        raise PageQueryError("Page must be an integer")


def validate_entity(entity: str) -> None:
    if not isinstance(entity, str):
        raise InvalidEntityFormatError("Entity must be a string")

    if len(entity) > 50:
        raise InvalidEntityFormatError(
            "Entity must be less than 50 characters"
        )

    if not entity[0].isalpha():
        raise InvalidEntityFormatError("Entity must start with an alphabet")

    pattern = compile(r"^[a-zA-Z0-9_]+$")

    if not pattern.match(entity):
        raise InvalidEntityFormatError(
            "Entity must be alphanumeric and underscore only"
        )
