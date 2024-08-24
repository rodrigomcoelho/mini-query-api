from http import HTTPStatus

from fastapi.exceptions import HTTPException


class EnvinronmentVariableMissingError(Exception): ...


class InvalidRecordKeyError(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(message),
            headers=headers,
        )


class NotEvenOneEntityHasBeenRegisteredExeption(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(message),
            headers=headers,
        )


class EntityAlreadyRegisteredException(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail=str(message),
            headers=headers,
        )


class EntityNotFoundException(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(message),
            headers=headers,
        )


class RecordNotFoundException(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(message),
            headers=headers,
        )


class PageQueryError(HTTPException):
    def __init__(
        self, message: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(message),
            headers=headers,
        )
