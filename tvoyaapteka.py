import json
import os
import requests
from bs4 import BeautifulSoup

"""
План
1. Через клиент-серверный запрос ("https://www.tvoyaapteka.ru/bitrix/ajax/modal_geoip.php?action=get_towns&region_id=")
и подставление айдишников с 918 по 923 получаем json с id городов
2. Текущий 'current' город открывает JS
...
"""

def get_data():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }

    """Получение html страницы для более удобной работы"""

    #     req = requests.get(url="https://www.tvoyaapteka.ru/adresa-aptek/", headers=headers)
    #     print(req.text)
    #
    #     if not os.path.exists("data"):
    #         os.mkdir("data")
    #
    #     with open("data/tvoyaapteka.html", "w") as file:
    #         file.write(req.text)

    """Получение данных"""

    data = []
    with open("data/tvoyaapteka.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    list_pharmacies = soup.find_all("div", class_="address_aptek_cont")

    for card in list_pharmacies:
        address = card.find_all("div", class_="apteka_item normal_store")

        for st in address:
            street = st.find("div", class_="apteka_address").text.replace('Ул. ', "")
            name = st.find("div", class_="apteka_title").find("span").text
            work_time = " ".join((st.find("div", class_="apteka_time")).text.split()) \
                .replace(' до ', "-").replace('Ежедневно с', "пн-вс").replace('.', ":") \
                .replace(' до ', "-").replace('Ежедневно ', "").replace(': с', "") \
                .replace('круглосуточно', "пн-вс 0:00-24:00").lower()  # можно ещё регулярками
            latitude = float(st.get("data-lat"))
            longitude = float(st.get("data-lon"))
            phones = None

            data.append(
                {
                    "address": street,
                    "latlon": ([latitude, longitude]),
                    "name": name,
                    "phones": ([phones]),
                    "working_hours": ([work_time])
                }
            )


    """Запись json файла"""

    with open(f"data/tvoyaapteka.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


""" Требования """


# {
# "address": "203-й микрорайон, корп. 1",
# "latlon": [62.031799, 129.754762],
# "name": "ТвояАптека.рф",
# "phones": [ "+78001000003"], номера телефонов аптек на сайте не указаны
# "working_hours": ["пн-вс 08:00-21:00"]
# },

def main():
    get_data()


if __name__ == '__main__':
    main()
