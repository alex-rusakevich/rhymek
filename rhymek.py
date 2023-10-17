#!/usr/bin/env python3
import argparse
from argparse import Namespace

import colorama

from rhymek.cache import get_cache, set_cache
from rhymek.processors import get_available_langcodes, get_lang_processor


def main(args: Namespace):
    processor = get_lang_processor(args.langcode)
    if not processor:
        raise Exception(f"Processor for language code '{args.langcode}' does not exist")

    word_to_search = args.word_in
    has_cache = False
    results = []

    if not args.no_cache and (
        cached_results := get_cache(word_to_search, args.langcode)
    ):
        results = cached_results
        has_cache = True
    else:
        results = processor.process(word_to_search)

    for i, r in enumerate(results):
        # r = r.replace("[", colorama.Fore.GREEN).replace("]", colorama.Fore.RESET)

        print(f"{r: <20}", end=" ")

        if (i + 1) % 3 == 0:
            print()

    print()

    if not args.no_cache and not has_cache:
        set_cache(word_to_search, args.langcode, results)


if __name__ == "__main__":
    colorama.init()

    parser = argparse.ArgumentParser(description="A word which need to be rhymed")
    parser.add_argument("word_in", type=str)
    parser.add_argument(
        "-l",
        "--langcode",
        type=str,
        help=f"The language code of the searched word ({', '.join(get_available_langcodes())})",
        default="ru",
    )
    parser.add_argument(
        "-C",
        "--no-cache",
        action="store_true",
        help=f"Don't load and save cache for searched word and language",
    )

    args = parser.parse_args()
    main(args)
