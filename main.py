from standardizer.standardizer import Standardizer
from database.database import Database


def get_user_input():
    print(
        "\nВведите адрес или команду.\n"
        "Возможные команды:\n"
        "[S] изменить настройки\n"
        "[Q] выйти\n"
    )
    return input("Ввод: ")


def update_settings(db) -> tuple[str, int]:
    lang = input("Выберите язык ответов:\n[0] ru\n[1] en\n")
    while lang not in ["1", "0"]:
        lang = input("Выберите язык ответов:\n[0] ru\n [1] en\n")
    token = input("Введите dadata API-ключ: ")
    db.update_settings(token, lang)
    return token, int(lang)


def main():
    db = Database()
    settings = db.get_settings()
    if not settings:
        settings = update_settings(db)
    else:
        print(f"Загружены настройки:\n"
              f"dadata token: {settings[0]};\n"
              f"язык ответов: {'en' if settings[1] else 'ru'}.")
    st = Standardizer(*settings)

    while True:
        query = get_user_input()
        if not query:
            continue
        elif query == "S":
            settings = update_settings(db)
            st.update_settings(*settings)
        elif query == "Q":
            raise SystemExit
        else:
            while True:
                addresses = st.get_addresses(query)
                [print(f'[{i}] {addr["value"]}') for i, addr in enumerate(addresses)]
                query = get_user_input()
                if not query:
                    break
                elif query == "S":
                    settings = update_settings(db)
                    st.update_settings(*settings)
                    break
                elif query == "Q":
                    raise SystemExit
                elif query.isdigit() and 0 <= int(query) < len(addresses):
                    query = int(query)
                    address = addresses[query]
                    data = address.get("data")
                    print(
                        f"{address['value']}\n"
                        f"Широта: {data.get('geo_lat')}\n"
                        f"Долгота: {data.get('geo_lon')}"
                    )
                    break
                print("Неизвестный ввод.\n")


if __name__ == "__main__":
    main()
