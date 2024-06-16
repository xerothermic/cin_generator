from collections import defaultdict
from typing import List

from chhoe_taigi_db_parser import ChhoeTaigiDBParser


class ChhoeTaigiDbMerger:
    def __init__(self):
        self._parsers: List[ChhoeTaigiDBParser] = []

    def add_parser(self, parser: ChhoeTaigiDBParser) -> None:
        self._parsers.append(parser)

    def merge(self):
        keys = set()
        [keys.update(p.cin_map.keys()) for p in self._parsers]
        merged_cin_map = defaultdict(set)
        for k in keys:
            for p in self._parsers:
                if k in p.cin_map:
                    v = p.cin_map[k]
                    if k in merged_cin_map:
                        merged_cin_map[k].update(v)
                    else:
                        merged_cin_map[k] = v
        return merged_cin_map