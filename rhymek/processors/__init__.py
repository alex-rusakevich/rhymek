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


def get_services_names_addresses() -> dict:
    result = {}

    for langcode, processor in LANG_PROCESSORS.items():
        result[langcode] = []
        for worker in processor.WORKERS:
            result[langcode].append((worker.name, worker.web_address))

    return result
