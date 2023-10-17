import requests
from bs4 import BeautifulSoup

from rhymek.processors.base import BaseRhymeProcessor, BaseWorker
from rhymek.utils import BASIC_HEADERS


class RifmeNetWorker(BaseWorker):
    name = "rifme.net"
    web_address = "https://rifme.net"

    def get_rhymes(self, word: str) -> list:
        resp = requests.get(f"https://rifme.net/r/{word}/0", headers=BASIC_HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        words = []

        soup.find("ul#tochnye")
        if tochnye := soup.select_one("ul#tochnye"):
            for li in tochnye.findAll("li"):
                if not li.text.startswith("http"):
                    words.append(li.text.strip())

        return words


class RifmovkaRuWorker(BaseWorker):
    name = "rifmovka.ru"
    web_address = "https://rifmovka.ru"

    def get_rhymes(self, word: str) -> list:
        resp = requests.get(f"https://rifmovka.ru/rifma/{word}", headers=BASIC_HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        words = []

        uls = soup.find_all("ul", {"class": "vowelBlock"})
        for ul in uls:
            lis = ul.find_all("li")
            for li in lis:
                words.append(li.text.strip())

        return words


class RhymeProcessor(BaseRhymeProcessor):
    LANG_NAME = "Русский"

    WORKERS = (RifmeNetWorker(), RifmovkaRuWorker())

    @staticmethod
    def get_common_end(ref_word: str, word_from: str) -> str:
        def devoice_char(char_in: str):
            VOICELESS_VOICED = {
                "б": "п",
                "в": "ф",
                "г": "к",
                "д": "т",
                "ж": "ш",
                "з": "с",
            }

            if char_in in VOICELESS_VOICED:
                return VOICELESS_VOICED[char_in]
            else:
                return char_in

        ref_word = ref_word.lower().strip()
        word_from = word_from.lower().strip()

        found_str = ""

        if ref_word[-1] == word_from[-1] or (
            devoice_char(word_from[-1]) == devoice_char(ref_word[-1])
        ):
            found_str += word_from[-1]
        else:
            return found_str

        i = -2

        while (i * -1) <= len(ref_word) and (i * -1) <= len(word_from):
            if ref_word[i] == word_from[i]:
                found_str += word_from[i]
            else:
                break
            i -= 1

        return found_str[::-1]
