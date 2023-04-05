from database import base

def get_api_key():
    token = input("Введите API-ключ | enter your API-key: ")
    return token


def get_language():
    lang = None
    while lang is None:
        try:
            lang_choice = int(input('[1] RU \n[2] EN \nВыберите язык | select language (enter "1" or "2"): '))
        except ValueError:
            print('Введите только "1" (русский) или только "2" (английский) | input only "1" (russian) or "2" (english)')
            continue
        if lang_choice in [1, 2]:
            lang = ["ru", "en"][lang_choice-1]
        else:
            print('Введите только "1" (русский) или только "2" (английский) | input only "1" (russian) or "2" (english)')
            continue
    return lang


def set_settings(base, token: str, lang: str):
    sql = 'INSERT INTO SETTINGS (token, lang) values(?, ?)'
    data = [(token, lang)]
    print(data)
    with base:
        base.execute("DELETE FROM SETTINGS")
        base.executemany(sql, data)
        base.commit()


def get_settings():
    with base:
        settings = [row for row in base.execute("SELECT token, lang FROM SETTINGS")]


    if settings:
        for row in settings:
            print(f"\nНайдены сохраненные настройки | Saved settings found:\nAPI-ключ | API-key: {row[0]}\nЯзык | language: {row[1]}")
        while True:
            try:
                change = bool(int(input("\nПродолжить с ними [0] или изменить [1]? | Continue with them [0] or change [1]? ")))
                break
            except ValueError:
                continue
        if change:
            configure_settings(0)
    else:
        configure_settings(0)


    with base:
        data = base.execute("SELECT token, lang FROM SETTINGS")
    for row in data:
        token, lang = row


    return (token, lang)

        
def configure_settings(key):
    api_key = get_api_key()
    language = get_language()
    print(api_key, language)
    set_settings(base, api_key, language)