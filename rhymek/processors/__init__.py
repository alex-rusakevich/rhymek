from typing import Union

from rhymek.processors import ru
from rhymek.processors.base import BaseRhymeProcessor

LANG_PROCESSORS = {
    "ru": ru.RhymeProcessor(),
}


def get_lang_processor(langcode: str) -> Union[BaseRhymeProcessor, None]:
    return LANG_PROCESSORS.get(langcode)


def get_available_langcodes():
    return LANG_PROCESSORS.keys()
