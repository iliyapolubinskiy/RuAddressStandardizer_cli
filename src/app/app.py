from src.standardizer.standardizer import Standardizer
from src.database.database import Database


class App:

    def __init__(self):
        """
        Инициализация объекта приложения, создание экземпляров Database и Standardizer
        Проверка наличия сохраненных настроек, запрос и запись настроек в случае их отсутствия.
        """
        self.db = Database()
        self.settings = self.db.get_settings()
        if not self.settings:
            self.settings = self.update_settings()
        else:
            self.display_settings()
        self.standardizer = Standardizer(*self.settings)

    def display_settings(self) -> None:
        """
        Вывод используемых настроек на экран
        :return:
        """
        print(f"Загружены настройки:\n"
              f"dadata token: {self.settings[0]};\n"
              f"язык ответов: {'en' if self.settings[1] else 'ru'}.")

    def update_settings(self) -> tuple[str, int]:
        """
        Метод для обновления настроек
        :return:
        """
        lang: str = input("Выберите язык ответов:\n[0] ru\n[1] en\n")
        while lang not in ["1", "0"]:
            lang = input("Выберите язык ответов:\n[0] ru\n [1] en\n")
        token: str = input("Введите dadata API-ключ: ")
        self.db.update_settings(token, int(lang))
        return token, int(lang)

    def run_loop(self) -> None:
        """
        Основной цикл приложения.
        В нем происходит чтение ввода и управление программой.
        :return:
        """
        while True:
            query: str = self.get_user_input()
            if not query:
                continue
            elif query == "S":
                self.settings = self.update_settings()
            elif query == "V":
                self.display_settings()
            elif query == "Q":
                raise SystemExit
            else:
                self.process_query_loop(query)

    def process_query_loop(self, query: str) -> None:
        """
        Если пользователь ввел запрос, то управление передается в этот метод.
        :param query: Пользовательский запрос - строка с адресом
        :return:
        """
        while True:
            addresses: list[dict] = self.standardizer.get_addresses(query)
            [print(f'[{i}] {addr["value"]}') for i, addr in enumerate(addresses)]
            query: str = self.get_user_input()
            if not query:
                continue
            elif query == "S":
                self.settings = self.update_settings()
                break
            elif query == "Q":
                raise SystemExit
            elif query == "V":
                self.display_settings()
            elif query.isdigit() and 0 <= int(query) < len(addresses):
                query: int = int(query)
                self.display_address(addresses[query])
                return
            else:
                print("Непонятный ввод.\n")

    @staticmethod
    def display_address(address: dict) -> None:
        """
        Отобразить адрес в определенном формате (адрес, координаты)
        :param address: Словарь, содержащий ответ от сервиса DaData, в котором присутствуют ключи "value", "data"
        :return:
        """
        data: dict = address.get("data")
        print(
            f"{address['value']}\n"
            f"Широта: {data.get('geo_lat')}\n"
            f"Долгота: {data.get('geo_lon')}"
        )

    @staticmethod
    def get_user_input() -> str:
        """
        Метод для отображения информации и считывания пользовательского ввода.
        :return:
        """
        print(
            "\nВведите адрес или команду.\n"
            "Возможные команды:\n"
            "[V] показать настройки\n"
            "[S] изменить настройки\n"
            "[Q] выйти\n"
        )
        return input("Ввод: ")
