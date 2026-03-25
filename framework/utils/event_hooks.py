import allure
from httpx import Request, Response

from framework.utils.curl import make_curl_from_request
from framework.utils.logger import get_logger

logger = get_logger("HTTP_LOGGER")


def curl_event_hook(request: Request):
    """
    Event hook для автоматического прикрепления cURL команды к Allure отчету.

    :param request: HTTP-запрос, переданный в `httpx` клиент.
    """
    curl_command = make_curl_from_request(request)

    allure.attach(curl_command, "cURL команда", allure.attachment_type.TEXT)


def log_request_event_hook(request: Request):
    """
    Логирует информацию об отправленном HTTP-запросе.

    :param request: Объект запроса HTTPX.
    """
    logger.info(f"Отправить {request.method} запрос на {request.url}")


def log_response_event_hook(response: Response):
    """
    Логирует информацию о полученном HTTP-ответе.

    :param response: Объект ответа HTTPX.
    """
    logger.info(f"Получен {response.status_code} {response.reason_phrase} с {response.url}")
