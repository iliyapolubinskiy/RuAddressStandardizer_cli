from dadata import Dadata
from SettingManager import get_settings

en = {"string": "en", "Address": "Please, enter address ", "Adr_number": "Please, select address by entering a number: ", 
      "Lat": "Latitude:", "Lon": "longitude:", "exit": 'or "Q" for quit: ', 
      "NotFound": "Oops, nothing found. Chech your address and try again.", 
      "IncorrectValue": "You must enter the number corresponding to the selected address.",
      "ChangeQuery": "Change my query.",
      "quting": "Goodbye, tnx for work.",
      "main_menu_message": """Please, enter an address or:
\"S\" for reset the settings; 
\"Q\" for quit.

Ввод: """}

ru = {"string": "ru", "Address": "Пожалуйста, введите адрес ", "Adr_number": "Пожалуйста, выберите нужный адрес, введя нужное число: ", 
      "Lat": "Ширина:", "Lon": "долгота:", "exit": 'или "Q" для выхода: ', 
      "NotFound": "Упс, ничего не найдено. Проверьте корректность ввода и попробуйте снова.", 
      "IncorrectValue": "Необходимо ввести число, соответствующее выбранному адресу.",
      "ChangeQuery": "Изменить запрос.",
      "quting": "До свидания, спасибо за работу.",
      "main_menu_message": """Пожалуйста, введите адрес, либо одну из букв:
\"S\" для переопределения настроек; 
\"Q\" для выхода.

Ввод: """}



def validate_address(token, lang):
    dadata = Dadata(token)
    user_input = input(f'{lang["main_menu_message"]}')
    if user_input == "Q":
        print(lang["quting"])
        raise SystemExit
    if user_input == "S":
        return True
    result = dadata.suggest("address", user_input, 20, language=lang["string"])
    print()
    for i in range(len(result)):
        print(f'[{i+1}] {result[i]["unrestricted_value"]}')
    print(f'\n[0] {lang["ChangeQuery"]}\n')
    if result:
        while True:
            try:
                user_input = int(input(lang["Adr_number"]))
                if user_input != 0:
                    print(f'\n{result[user_input-1]["value"]} \n {lang["Lat"]} {result[user_input-1]["data"]["geo_lat"]}, {lang["Lon"]} {result[user_input-1]["data"]["geo_lon"]} \n')
                break
            except IndexError:
                print(lang['IncorrectValue'])
                continue
            except ValueError:
                print(lang['IncorrectValue'])
                continue
    else:
        print(lang["NotFound"])


if __name__ == "__main__":
    token, lang = get_settings()
    
    while True: 
        if validate_address(token, en if lang == "en" else ru):
            token, lang = get_settings()
