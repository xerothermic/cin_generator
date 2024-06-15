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
        self._parse_alternative_phrase()
        self._add_no_tones()
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

    def _parse_alternative_phrase(self):
        """ parse 文|白|替|俗 """
        alternative_phrase = self._taigi_df[self._taigi_df.KipInput.str.contains("(文|白|替|俗)")]
        # Drop -- /
        alternative_phrase = alternative_phrase[~alternative_phrase.KipInput.str.contains("--|/")]
        for _idx, row in alternative_phrase.iterrows():
            kip_input = row["KipInput"].split("(")[0].lower()
            kip_utf8 = row["KipUnicode"].split("(")[0]
            self._cin_map[kip_input].add(kip_utf8)
            self._cin_map[kip_input].add(row["HanLoTaibunKip"])
            # Add other input if available
            if isinstance(row["KipInputOthers"], str):
                if row["KipInputOthers"].count('-') or row["KipInputOthers"].count('/'):
                    continue
                kip_input_others = row["KipInputOthers"].split("(")[0].lower()
                kip_utf8_others = row["KipUnicodeOthers"].split("(")[0].lower()
                self._cin_map[kip_input_others].add(kip_utf8_others)

    def _add_no_tones(self):
        no_tones_map = defaultdict(set)
        no_digit_map = {ord(str(d)): None for d in (2,3,4,5,7,8)}
        for k,v in self._cin_map.items():
            k = k.translate(no_digit_map)
            if k in no_tones_map:
                no_tones_map[k].update(v)
            else:
                no_tones_map[k] = v
        self._cin_map.update(no_tones_map)