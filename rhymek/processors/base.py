import re


class BaseWorker:
    name = ""
    web_address = ""

    def get_rhymes(self, word: str) -> list:
        pass


class BaseRhymeProcessor:
    WORKERS = ()
    HIGHLIGHT_START = "["
    HIGHLIGHT_END = "]"

    def __init__(self):
        pass

    def process(self, word: str):
        results = []
        for worker in self.WORKERS:
            results += worker.get_rhymes(word)

        results = [i for i in set(results) if i.strip() != ""]

        for i, v in enumerate(results):
            common_end = self.__class__.get_common_end(word, v)
            if common_end != "":
                results[i] = re.sub(
                    common_end + "$",
                    f"{self.HIGHLIGHT_START}{common_end}{self.HIGHLIGHT_END}",
                    results[i],
                )

        return results

    @staticmethod
    def get_common_end(ref_word: str, word_from: str) -> str:
        found_str = ""
        i = -1

        while (i * -1) <= len(ref_word) and (i * -1) <= len(word_from):
            if ref_word[i] == word_from[i]:
                found_str += word_from[i]
            else:
                return found_str[::-1]
            i -= 1

        return found_str[::-1]
