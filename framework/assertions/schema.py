import allure

from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from framework.utils.logger import get_logger

logger = get_logger("SCHEMA_ASSERTIONS")


@allure.step("Валидация JSON схемы")
def validate_json_schema[T](actual_instance: T, expected_schema: dict) -> None:
    """
    Проверяет, соответствует ли JSON-объект (actual_instance) заданной JSON-схеме (expected_schema).

    :param actual_instance: JSON-данные, которые нужно проверить.
    :param expected_schema: Ожидаемая JSON-schema.
    :raises jsonschema.exceptions.ValidationError:
    Если actual_instance не соответствует expected_schema.
    """
    logger.info("Валидация JSON схемы")

    validate(
        instance=actual_instance,
        schema=expected_schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
