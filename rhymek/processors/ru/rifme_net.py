import requests
from bs4 import BeautifulSoup

from rhymek.utils import BASIC_HEADERS


def processor(word: str) -> list:
    resp = requests.get(f"https://rifme.net/r/{word}/0", headers=BASIC_HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    words = []

    soup.find("ul#tochnye")
    for li in soup.select_one("ul#tochnye").findAll("li"):
        if not li.text.startswith("http"):
            words.append(li.text.strip())

    return words
