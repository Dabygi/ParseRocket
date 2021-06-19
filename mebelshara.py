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

    """Получение данных"""

    data = []
    with open("data/mebelshara.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    list_shops = soup.find_all("div", class_="city-item")

    for destination in list_shops:
        city = destination.find("h4", class_="js-city-name").text
        info = destination.find_all("div", class_="shop-list-item")
        for st in info:
            street = st.get("data-shop-address")
            addr = city + ", " + street
            latitude = float(st.get("data-shop-latitude"))
            longitude = float(st.get("data-shop-longitude"))
            name = st.get("data-shop-name")
            phones = st.get("data-shop-phone").replace('(', '').replace(')', '')
            work_time = st.get("data-shop-mode1")

            excep = ('Без выходных:', 'Без выходных')
            if work_time in excep:
                work_time = "пн - вс"
            else:
                work_time = work_time

            work_week = st.get("data-shop-mode2")
            work = work_time + " " + work_week

            data.append(
                {
                    "address": addr,
                    "latlon": ([latitude, longitude]),
                    "name": name,
                    "phones": ([phones]),
                    "working_hours": ([work])
                }
            )


        """Запись json файла"""

    with open(f"data/mebelshara.json", "w") as file:
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
