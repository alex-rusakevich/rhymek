#!/usr/bin/env python3
import argparse

from rhymek.processors import get_lang_processor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A word which need to be rhymed")
    parser.add_argument("word_in", type=str)
    parser.add_argument(
        "-l",
        "--langcode",
        type=str,
        help="The language code of the searched word (ru, en etc.)",
        default="ru",
    )
    args = parser.parse_args()

    processor = get_lang_processor(args.langcode)
    if not processor:
        raise Exception(f"Processor for language code '{args.langcode}' does not exist")

    word_to_search = args.word_in

    results = processor.process(word_to_search)

    for i, r in enumerate(results):
        print(f"{r: <20}", end=" ")

        if (i + 1) % 3 == 0:
            print()

    print()
