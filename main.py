import json
import os
import requests
from bs4 import BeautifulSoup


def get_all_pages():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }

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
            latitude = destination.get("data-shop-latitude")
            longitude = destination.get("data-shop-longitude")
            name = destination.find("div", class_="shop-name").text
            phones = destination.find("div", class_="shop-phone").text
            work_time = destination.get("data-shop-mode1")
            if work_time == 'Без выходных:':
                work_time = "пн - вс"
            work_week = destination.get("data-shop-mode2")

            data.append(
                {
                    "address": city,
                    "latlon": [latitude, longitude],
                    "name": name,
                    "phones": [phones],
                    "working_hours": [work_time, work_week]
                }
            )

    with open(f"mebelshara.json", "a") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


        # print(f'address: "{city}, {street}",')
        # print(f'latlon: [{latitude}, {longitude}],')
        # print(f'name: "{name}",')
        # print(f'phones: [{phones}],')
        # print(f'working_hours: ["{work_time} {work_week}"]')

# {
#     "address": "Белгород, Пугачева, 5",
#     "latlon": [44.983268, 41.096873],
#     "name": "Мебель Шара",
#     "phones": ["8 800 551 06 10"]
#     "working_hours": ["пн - вс 10:00 - 20:00"]
# },


def main():
    get_all_pages()


if __name__ == '__main__':
    main()
