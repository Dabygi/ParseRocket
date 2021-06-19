import json
import os
import requests
from bs4 import BeautifulSoup


def get_page():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }

    """Получение html страницы для более удобной работы"""

    # r = requests.get(url="https://www.mebelshara.ru/contacts/", headers=headers)
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/mebelshara.html", "w") as file:
    #     file.write(r.text)

    data = []
    with open("data/mebelshara.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    city_name = soup.find_all("div", class_="city-item")

    for name in city_name:
        city = name.find("h4", class_="js-city-name").text

        list_shops = soup.find_all("div", class_="shop-list-item")

        for destination in list_shops:
            street = destination.find("div", class_="shop-address").text
            latitude = float(destination.get("data-shop-latitude"))
            longitude = float(destination.get("data-shop-longitude"))
            name = destination.find("div", class_="shop-name").text
            phones = destination.find("div", class_="shop-phone").text
            work_time = destination.get("data-shop-mode1")
            excep = ('Без выходных:', 'Без выходных')
            if work_time in excep:
                work_time = "пн - вс"
            else:
                work_time = work_time

            work_week = destination.get("data-shop-mode2")
            work = work_time + " " + work_week

            data.append(
                {
                    "address": street,
                    "latlon": [float(latitude), float(longitude)],
                    "name": name,
                    "phones": [phones],
                    "working_hours": [work]
                }
            )


        """Запись json файла"""

    with open(f"mebelshara.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


        """ Требования """
# {
#     "address": "Белгород, Пугачева, 5",
#     "latlon": [44.983268, 41.096873],
#     "name": "Мебель Шара",
#     "phones": ["8 800 551 06 10"]
#     "working_hours": ["пн - вс 10:00 - 20:00"]
# },

def main():
    get_page()


if __name__ == '__main__':
    main()
