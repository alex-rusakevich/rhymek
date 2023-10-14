import requests
from bs4 import BeautifulSoup

from rhymek.processors.base import BaseRhymeProcessor
from rhymek.utils import BASIC_HEADERS


class RhymeProcessor(BaseRhymeProcessor):
    def rifme_net_worker(word: str) -> list:
        resp = requests.get(f"https://rifme.net/r/{word}/0", headers=BASIC_HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        words = []

        soup.find("ul#tochnye")
        if tochnye := soup.select_one("ul#tochnye"):
            for li in tochnye.findAll("li"):
                if not li.text.startswith("http"):
                    words.append(li.text.strip())

        return words

    WORKERS = (rifme_net_worker,)
