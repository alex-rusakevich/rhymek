class BaseRhymeProcessor:
    WORKERS = ()

    def __init__(self):
        pass

    def process(self, word: str):
        results = []
        for proc in self.WORKERS:
            results += proc(word)

        results = list(set(results))

        for i, v in enumerate(results):
            common_end = BaseRhymeProcessor.get_common_end(word, v)
            if common_end != "":
                results[i] = results[i].replace(
                    common_end, f'<span class="ending">{common_end}</span>'
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
