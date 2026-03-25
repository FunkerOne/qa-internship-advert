from typing import Any, Sized

import allure

from framework.utils.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")


@allure.step("Ожидает HTTP статус код: {expected}")
def assert_status_code[T](actual: T, expected: T) -> None:
    """
    Проверяет, что фактический статус-код ответа соответствует ожидаемому.

    :param actual: Фактический статус-код ответа.
    :param expected: Ожидаемый статус-код.
    :raises AssertionError: Если статус-коды не совпадают.
    """
    logger.info(f"Ожидает HTTP статус код: {expected}")

    assert actual == expected, (
        f"Некорректный статус-код ответа. Ожидаемый статус-код: {expected}. Фактический статус-код: {actual}."
    )


@allure.step("Ожидает, что {name} равно {expected}")
def assert_equal(actual: Any, expected: Any, name: str) -> None:
    """
    Проверяет, что фактическое значение равно ожидаемому.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :raises AssertionError: Если фактическое значение не равно ожидаемому.
    """
    logger.info(f"Ожидает что {name} равно {expected}")

    assert actual == expected, (
        f'Некорректное значение поля: "{name}". Ожидаемое значение: {expected}. Фактическое значение: {actual}'
    )


@allure.step("Ожидает, что {name} НЕ равно {expected}")
def assert_not_equal(actual: Any, expected: Any, name: str) -> None:
    """
    Проверяет, что фактическое значение НЕ равно ожидаемому.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :raises AssertionError: Если фактическое значение равно ожидаемому.
    """
    logger.info(f"Ожидает что {name} НЕ равно {expected}")

    assert actual == expected, (
        f'Некорректное значение поля: "{name}". Ожидаемое значение: {expected}. Фактическое значение: {actual}'
    )


@allure.step("Ожидает, что {name} не пустое, фактическое значение {actual}")
def assert_not_empty(actual: Any, name: str) -> None:
    """
    Проверяет, что фактическое значение не пустое.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :raises AssertionError: Если фактическое значение ложно.
    """
    logger.info(f"Ожидает что {name} не пустое")

    assert actual, f'Некорректное значение поля: "{name}". Ожидаем заполненное поле, но получили: {actual}'


def assert_length(actual: Sized, expected: Sized, name: str) -> None:
    """
    Проверяет, что длины двух объектов совпадают.

    :param name: Название проверяемого объекта.
    :param actual: Фактический объект.
    :param expected: Ожидаемый объект.
    :raises AssertionError: Если длины не совпадают.
    """
    with allure.step(f"Ожидает, что длина {name} равняется {len(expected)}"):
        logger.info(f"Ожидает, что длина {name} равняется {len(expected)}")

        assert len(actual) == len(expected), (
            f'Некорректная длина объекта: "{name}". Ожидаемая длина: {len(expected)}. Фактическая длина: {len(actual)}'
        )
