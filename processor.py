import logging
import sys

import pandas as pd

from chhoe_taigi_db_parser import ChhoeTaigiDBParser

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger()


def print_header():
    print("%gen_inp")
    print("%ename kip-tailo")
    print("%cname 教羅")
    print("%encoding UTF-8")
    print("%selkey qwdfzxyzv")
    print_keyname()
    print("%chardef begin", end="")


def print_keyname():
    skip_list = "qwdfzxyzv"
    print("%keyname begin")
    for i in range(1,10):
        print(f"{i} {i}")

    for c in range(26):
        ch = chr(ord('a') + c)
        if ch in skip_list:
            continue
        print(f"{ch} {ch}")
    print("%keyname end")


def print_footer():
    print("%chardef end")


def main():
    parser = ChhoeTaigiDBParser("ChhoeTaigiDatabase/ChhoeTaigiDatabase/ChhoeTaigi_KauiokpooTaigiSutian.csv")
    print_header()
    print(parser.parse())
    print_footer()


if __name__ == "__main__":
    logger.info("Processing ChhoeTaigi DataBase to cin file...")
    main()
