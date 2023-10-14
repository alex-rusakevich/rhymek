import requests
from bs4 import BeautifulSoup

from rhymek.processors.base import BaseRhymeProcessor
from rhymek.utils import BASIC_HEADERS


class RhymeProcessor(BaseRhymeProcessor):
    @staticmethod
    def get_common_end(ref_word: str, word_from: str) -> str:
        ref_word = ref_word.lower().strip()
        word_from = word_from.lower().strip()

        VOICELESS_VOICED = {"б": "п", "в": "ф", "г": "к", "д": "т", "ж": "ш", "з": "с"}

        found_str = ""

        if ref_word[-1] == word_from[-1] or (
            word_from[-1] in VOICELESS_VOICED
            and ref_word[-1] == VOICELESS_VOICED[word_from[-1]]
        ):
            found_str += word_from[-1]

        i = -2

        while (i * -1) <= len(ref_word) and (i * -1) <= len(word_from):
            if ref_word[i] == word_from[i]:
                found_str += word_from[i]
            else:
                break
            i -= 1

        return found_str[::-1]

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

    def rifmovka_ru(word: str) -> list:
        resp = requests.get(f"https://rifmovka.ru/rifma/{word}", headers=BASIC_HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        words = []

        uls = soup.find_all("ul", {"class": "vowelBlock"})
        for ul in uls:
            lis = ul.find_all("li")
            for li in lis:
                words.append(li.text.strip())

        return words

    WORKERS = (rifme_net_worker, rifmovka_ru)
