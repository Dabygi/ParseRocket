import json
import os
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }

    req = requests.get(url, headers)
    print(req.text)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/tui.html", "w") as file:
        file.write(req.text)

get_data("https://www.tui.ru/offices/")

#
# def main():
#     get_data()
#
#
# if __name__ == '__main__':
#     main()
