from pydantic import BaseModel


class ResultSchema(BaseModel):
    """
    Описание структуры сообщений.
    """

    messages: dict[str, str] | None
    message: str


class BadRequestResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой Bad request.
    """

    result: ResultSchema
    status: str


class NotFoundResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой Not Found.
    """

    result: ResultSchema
    status: str


# Описал как отдельную модель, чтобы не нарушать принцип единства ответственности
class ServerErrorResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой Server error.
    """

    result: ResultSchema
    status: str
