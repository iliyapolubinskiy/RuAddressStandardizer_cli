from dadata import Dadata
import sqlite3 as sl


lang, token, base = None, None, None
en = {"Address": "Please, enter address ", "Adr_number": "Please, select address by entering a number: ", 
      "Lat": "Latitude:", "Lon": "longitude:", "exit": 'or "Q" for quit: ', 
      "NotFound": "Oops, nothing found. Chech your address and try again.", 
      "IncorrectValue": "You must enter the number corresponding to the selected address.",
      "quting": "Goodbye, tnx for work."}

ru = {"Address": "Пожалуйста, введите адрес ", "Adr_number": "Пожалуйста, выберите нужный адрес, введя нужное число: ", 
      "Lat": "Ширина:", "Lon": "долгота:", "exit": 'или "Q" для выхода: ', 
      "NotFound": "Упс, ничего не найдено. Проверьте корректность ввода и попробуйте снова.", 
      "IncorrectValue": "Необходимо ввести число, соответствующее выбранному адресу.",
      "quting": "До свидания, спасибо за работу."}


def setStg():
    global base, token, lang
    with base:
        base.execute("DELETE FROM SETTINGS")
    token = input("Введите API-ключ | enter your API-key: ")
    while lang == None:
        try:
            lang_choice= int(input('[1] RU \n[2] EN \nВыберите язык | select language (enter "1" or "2"): '))
        except ValueError:
            print('Введите только "1" (русский) или только "2" (английский) | input only "1" (russian) or "2" (english)')
            continue
        if lang_choice == 1:
            lang = "ru"
        elif lang_choice == 2:
            lang = "en"
        else:
            continue
    sql = 'INSERT INTO SETTINGS (token, lang) values(?, ?)'
    data = [(token, lang)]
    with base:
        base.executemany(sql, data)


def getCoords(token, lang):
    global lang_dict, en, ru
    token = token
    language = lang
    if lang == "ru":
        lang_dict = ru
    if lang == "en":
        lang_dict = en
    dadata = Dadata(token)
    user_query = input(f'{lang_dict["Address"]}{lang_dict["exit"]}')
    if user_query == "Q":
        print(lang_dict["quting"])
        raise SystemExit
    result = dadata.suggest("address", user_query, 20, language=language)
    print("")
    for i in range(len(result)):
        print(f'[{i+1}] {result[i]["unrestricted_value"]}')
    print("")
    if result:
        while True:
            try:
                adr_n = int(input(lang_dict["Adr_number"]))
                print(f'\n{result[adr_n-1]["value"]} \n {lang_dict["Lat"]} {result[adr_n-1]["data"]["geo_lat"]}, {lang_dict["Lon"]} {result[adr_n-1]["data"]["geo_lon"]} \n')
                break
            except IndexError:
                print(lang_dict['IncorrectValue'])
                continue
            except ValueError:
                print(lang_dict['IncorrectValue'])
                continue
    elif not result:
        print(lang_dict["NotFound"])


base = sl.connect('users_stg.db')
try:
    with base:
        base.execute("""
            CREATE TABLE SETTINGS (
                token TEXT,
                lang TEXT
            );
        """)
except sl.OperationalError:
    pass


settings = []
with base:
    data = base.execute("SELECT token, lang FROM SETTINGS")
for row in data:
    settings.append(row)


if settings:
    for row in settings:
        print(f"\nНайдены сохраненные настройки | Saved settings found:\nAPI-ключ | API-key: {row[0]}\nЯзык | language: {row[1]}")
    cnt_or_chn = 0
    while cnt_or_chn not in [1, 2]:
        try:
            cnt_or_chn = int(input("\nПродолжить с ними [1] или изменить [2]? | Continue with them [1] or change [2]? "))
        except ValueError:
            continue
elif not settings:
    setStg()
    cnt_or_chn = 1


if cnt_or_chn == 2:
    setStg()
elif cnt_or_chn == 1:
    with base:
        data = base.execute("SELECT token, lang FROM SETTINGS")
    for row in data:
        token = row[0]
        lang = row[1]


while True: 
    getCoords(token, lang)
