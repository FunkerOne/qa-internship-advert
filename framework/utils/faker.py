from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker, который будет использоваться для генерации данных.
        """
        self.faker = faker

    def integer(self, start: int = 1, end: int = 1000) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное целое число.
        """
        return self.faker.random_int(start, end)

    def seller_id(self) -> int:
        """
        Генерирует случайный идентификатор продавца в диапазоне от 111_111 до 999_999.

        :return: Случайная цена объявления.
        """
        return self.integer(start=111_111, end=999_999)

    def price(self) -> int:
        """
        Генерирует случайную цену объявления в диапазоне от 50 до 10_000.

        :return: Случайная цена объявления.
        """
        return self.integer(50, 10_000)

    def likes(self) -> int:
        """
        Генерирует случайное количество лайков в диапазоне от 1 до 50.

        :return: Случайное количество лайков.
        """
        return self.integer(1, 50)

    def view_count(self) -> int:
        """
        Генерирует случайный количество просмотров в диапазоне от 1 до 100.

        :return: Случайный количество просмотров.
        """
        return self.integer(1, 100)

    def contacts(self) -> int:
        """
        Генерирует случайное количество контактов в диапазоне от 1 до 15.

        :return: количество контактов.
        """
        return self.integer(1, 15)


fake = Fake(faker=Faker("ru_RU"))
