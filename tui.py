import json
import os
import requests
from bs4 import BeautifulSoup


"""
План
1. Через клиент-серверный запрос ("https://apigate.tui.ru/api/office/cities") получаем json с id городов
2. Подставляем id городов в конец запроса (https://apigate.tui.ru/api/office/list?cityId=) получаем инфу о офисах
3. Извлекаем требуемые данные, форматируем, упорядочиваем
4. Записываем json
"""

def get_data(url):

    response = requests.get(url)
    data = response.json()
    city = [x for x in data['cities']][0]
    return print(city['cityId'])

get_data("https://apigate.tui.ru/api/office/cities")


# def main():
#     get_data()
#
#
# if __name__ == '__main__':
#     main()
