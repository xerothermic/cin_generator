import logging
import sys

import click

from chhoe_taigi_db_parser import ChhoeTaigiDBParser

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger()


def print_header():
    print("%gen_inp")
    print("%ename kip-tailo")
    print("%cname 教羅")
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
    parser1 = ChhoeTaigiDBParser("ChhoeTaigiDatabase/ChhoeTaigiDatabase/ChhoeTaigi_KauiokpooTaigiSutian.csv")
    parser2 = ChhoeTaigiDBParser("ChhoeTaigiDatabase/ChhoeTaigiDatabase/ChhoeTaigi_iTaigiHoataiTuichiautian.csv")
    parser3 = ChhoeTaigiDBParser("ChhoeTaigiDatabase/ChhoeTaigiDatabase/ChhoeTaigi_TaihoaSoanntengTuichiautian.csv")
    parser4 = ChhoeTaigiDBParser("ChhoeTaigiDatabase/ChhoeTaigiDatabase/ChhoeTaigi_TaijitToaSutian.csv")
    parser1.parse()
    parser2.parse()
    parser3.parse()
    parser4.parse()

    cin_map1 = parser1._cin_map
    cin_map2 = parser2._cin_map
    cin_map3 = parser3._cin_map
    cin_map4 = parser4._cin_map
    cin_map1.update(cin_map2)
    cin_map1.update(cin_map3)
    cin_map1.update(cin_map4)
    print_header()
    # print(parser.parse())
    print(parser1.stringify(cin_map1))
    print_footer()


if __name__ == "__main__":
    logger.info("Processing ChhoeTaigi DataBase to cin file...")
    main()
