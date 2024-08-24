from mini.exceptions import InvalidRecordKeyError, PageQueryError


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
