# CARBIS_TQ

Тестовое задание для кандидата на должность разработчика программного обеспечения CARBIS

Программа, функционал которой предоставляет пользователю доступ к API сервиса dadata.ru, в частности - к функционалу подсказок адресов.

При запуске программы пользователю необходимо ввести API-ключ и выбрать язык, который будет использоваться программой при работе.
Настройки сохраняются в базу данных на движке SQLite. 

После настройки необходимо ввести адрес в произвольной форме, как на английском, так и на русском. На экран будет выведено до 20 адресов, удовлетворяющих запросу. 
Для получения точных координат адреса необходимо выбрать нужный адрес из тех, что вывелись на экран. Для этого нужно ввести число, соответствующее нужному адресу. 
При отсутствии нужного адреса рекомендуется выбрать любой из показанных, получить его координаты и повторно ввести уже более точный адрес (уточнить регион, город). 

Завершить работу с программой можно в любой момент путем закрытия приложения, либо введя "Q" вместо адреса на этапе уточнения адреса у пользователя. 

При повторном запуске программы у пользователя будет выбор: продолжить работу с уже введенными настройками (API-ключ и язык) или ввести другие. Для выбора необходимо ввести 1 или 2. 

# Начало работы

Для начала работы необходимо:

1. установить Python версии 3.8
2. Установить библиотеку Dadata следующей командой:
``` python
pip install dadata
```
3. Зарегистрироваться на сайте https://dadata.ru/ и получить API-ключ.