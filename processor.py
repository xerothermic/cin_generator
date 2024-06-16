import logging
import sys

import click

from chhoe_taigi_db_merger import ChhoeTaigiDbMerger
from chhoe_taigi_db_parser import ChhoeTaigiDBParser

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger()


def print_header():
    print("%gen_inp")
    print("%ename combo-tailo")
    print("%cname 多漢羅")
    print("%encoding UTF-8")
    print("%selkey qwdfzxyv")
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
    csv_path = "ChhoeTaigiDatabase/ChhoeTaigiDatabase/"
    csv_files = [
        "ChhoeTaigi_KauiokpooTaigiSutian.csv",
        "ChhoeTaigi_iTaigiHoataiTuichiautian.csv",
        "ChhoeTaigi_TaihoaSoanntengTuichiautian.csv",
        "ChhoeTaigi_TaijitToaSutian.csv",
    ]
    parsers = []
    merger = ChhoeTaigiDbMerger()
    for csv_file in csv_files:
        parser = ChhoeTaigiDBParser(csv_path+csv_file)
        parser.parse()
        parsers.append(parser)
        merger.add_parser(parser)

    merged_cin_map = merger.merge()

    print_header()
    # print(parser.parse())
    print(ChhoeTaigiDBParser.stringify(merged_cin_map))
    print_footer()


if __name__ == "__main__":
    logger.info("Processing ChhoeTaigi DataBase to cin file...")
    main()
