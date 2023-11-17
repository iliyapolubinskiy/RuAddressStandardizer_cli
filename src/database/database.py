import sqlite3 as sl
from src.logger.logger import log


class Database:

    def __init__(self, db_name: str = "settings"):
        self.base: sl.Connection = sl.connect(f'{db_name}.db')
        self.get_or_create_table()

    def get_or_create_table(self) -> None:
        """
        Проверка таблицы на существование и создание таблицы при её отсутствии.
        :return:
        """
        with self.base as base:
            try:
                base.execute("SELECT * FROM settings")
                log.log_info("table already exists")
            except sl.OperationalError as e:
                if "no such table" in str(e):
                    print("Настройки не найдены")
                    base.execute("""
                        CREATE TABLE settings (
                            token VARCHAR(40),
                            lang INTEGER
                        );
                    """)
                    base.commit()
                    log.log_info("table created")
                else:
                    log.log_info(e)
                    raise e

    def get_settings(self) -> tuple[str]:
        """
        Достать настройки из базы данных
        :return: (token, lang(0 or 1)) сохраненные настройки
        """
        with self.base as base:
            cursor = base.execute("SELECT * FROM settings")
            result = cursor.fetchone()
        return result

    def update_settings(self, token: str = None, lang: int = None) -> None:
        """
        Обновить настройки в базе данных
        :param token: API-Ключ сервиса DaData
        :param lang: Язык. 0 - русский, 1 - английский
        :return:
        """
        if token or lang:
            sql: str = (
                f"INSERT INTO settings (token, lang) "
                f"VALUES ('{token}', {lang});"
            )
        else:
            return
        with self.base as base:
            base.execute(f"DELETE FROM settings;")
            base.execute(sql)
            base.commit()
            log.log_info("settings updated")
