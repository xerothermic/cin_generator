from collections import defaultdict
import logging

import pandas as pd

logger = logging.getLogger()

class ChhoeTaigiDBParser:
    """ Convert ChhoeTaigiDatabase csv to .cin format """
    def __init__(self, dict_path):
        self._dict_path = dict_path
        self._taigi_df = pd.read_csv(self._dict_path)
        self._cin_map = defaultdict(set)

    def parse(self):
        """ parse KipInput and fill _cin_map """
        self._parse_single_word_v2()
        self._parse_single_word_from_phrase()
        self._parse_simple_phrase()
        return self

    def __str__(self):
        """ convert _cin_map to string """
        buf = ['']
        sorted_cin_map = dict(sorted(self._cin_map.items()))
        for k, l in sorted_cin_map.items():
            for v in l:
                # In OpenVanilla: type k will output v
                buf.append(f"{k} {v}")
        return '\n'.join(buf)

    def _parse_single_word_v2(self):
        """ convert single word to unicode and hanlo """
        # Ignore KipInput with () / space and japanese
        single_word_df = self._taigi_df[~self._taigi_df.KipInput.str.contains("\\(|/|-| |な")]
        for _idx, row in single_word_df.iterrows():
            k = row["KipInput"].lower()
            self._cin_map[k].add(row["KipUnicode"].lower())
            self._cin_map[k].add(row["HanLoTaibunKip"])

    def _parse_single_word_from_phrase(self):
        """ parse phrase with pattern <word>-<word> ... to single word unicode and hanlo """
        # ignore /
        single_phrase_df = self._taigi_df[
            (~self._taigi_df.KipInput.str.contains("/")) &
            self._taigi_df.KipInput.str.contains("^[a-zA-Z2345789]+(-[a-zA-Z2345789]+)+$")]
        for _idx, row in single_phrase_df.iterrows():
            kip_input_list = row["KipInput"].split("-")
            kip_utf8_list = row["KipUnicode"].split("-")
            kip_hanlo_list = row["HanLoTaibunKip"]
            if len(kip_input_list) != len(kip_utf8_list):
                logger.warning(f"{len(kip_input_list)=} != {len(kip_utf8_list)=}")
                continue
            for k, v in zip(kip_input_list, kip_utf8_list):
                self._cin_map[k.lower()].add(v.lower())
            if len(kip_input_list) != len(kip_hanlo_list):
                logger.warning(f"{kip_input_list} != {kip_hanlo_list}")
                continue
            for k, v in zip(kip_input_list, kip_hanlo_list):
                self._cin_map[k.lower()].add(v)

    def _parse_simple_phrase(self):
        """
        parse phrase with pattern <word>-<word> ..., so we can type longer phrase at a time
        """
        # ignore / 
        single_phrase_df = self._taigi_df[
            (~self._taigi_df.KipInput.str.contains("/")) &
            self._taigi_df.KipInput.str.contains("^[a-zA-Z2345789]+(-[a-zA-Z2345789]+)+$")]
        logger.info(single_phrase_df.shape)
        for _idx, row in single_phrase_df.iterrows():
            kip_input = row["KipInput"].replace("-", "").lower()
            self._cin_map[kip_input].add(row["KipUnicode"])
            self._cin_map[kip_input].add(row["HanLoTaibunKip"])