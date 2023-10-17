#!/usr/bin/env python3
import argparse
from argparse import Namespace, RawDescriptionHelpFormatter

import colorama

from rhymek.cache import clear_cache, get_cache, set_cache
from rhymek.processors import (
    get_available_langcodes,
    get_lang_processor,
    get_services_names_addresses,
)


def main(args: Namespace):
    if args.clear_cache:
        clear_cache()

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

    if not args.no_rhymes_number:
        print("Rhymes found:", len(results), "\n")

    for i, r in enumerate(results):
        # r = r.replace("[", colorama.Fore.GREEN).replace("]", colorama.Fore.RESET)

        print(f"{r: <20}", end=" ")

        if (i + 1) % 3 == 0 and i + 1 != len(results):
            print()

    print()

    if not args.no_cache and not has_cache:
        set_cache(word_to_search, args.langcode, results)


if __name__ == "__main__":
    colorama.init()

    web_services_dict = get_services_names_addresses()
    web_services_str = ""

    for locale, web_services in web_services_dict.items():
        web_services_str += f"{locale.upper()} locale:\n"

        for i, (name, address) in enumerate(web_services):
            web_services_str += f"{i+1}. {name} ({address})\n"

        web_services_str += "\n"

    parser = argparse.ArgumentParser(
        prog="rhymek",
        description="A program for finding rhymes to various words",
        formatter_class=RawDescriptionHelpFormatter,
        epilog=f"""
The project would not be possible without these web services:

{web_services_str}
""",
    )
    parser.add_argument("word_in", type=str)
    parser.add_argument(
        "-l",
        "--langcode",
        type=str,
        help=f"The language code of the searched word ({', '.join(get_available_langcodes())})",
        default=tuple(get_available_langcodes())[0],
    )
    parser.add_argument(
        "-c",
        "--no-cache",
        action="store_true",
        help="Don't load and save cache for searched word and language",
    )
    parser.add_argument(
        "-C",
        "--clear-cache",
        action="store_true",
        help="Clear cache before start",
    )
    parser.add_argument(
        "-n",
        "--no-rhymes-number",
        action="store_true",
        help="Don't print rhymes number",
    )

    args = parser.parse_args()
    main(args)
