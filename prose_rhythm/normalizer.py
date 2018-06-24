# -*- coding: utf-8 -*-
"""
Normalize Latin text for preprocessing.

The module assume that the text is already macronized and is utf 8 encoded.
"""
import regex as re

DEFAULT_PUNC = [".", "?", "!", ";", ":"]
DEFAULT_ABBREV = ["Agr.", "Ap.", "A.", "K.", "D.", "F.", "C.",
                  "Cn.", "L.", "Mam.", "M\'", "M.", "N.", "Oct.",
                  "Opet.", "Post.", "Pro.", "P.", "Q.", "Sert.",
                  "Ser.", "Sex.", "S.", "St.", "Ti.", "T.", "V.",
                  "Vol.", "Vop.", "Pl."]


class Normalizer(object):
    """
    Normalizes Latin text for preprocessing module.
    """

    def __init__(self, punctuation=None, replace_abbrev=True, abbrev=None):
        self.punctuation = DEFAULT_PUNC if punctuation is None else punctuation
        self.replace_abbrev = replace_abbrev
        self.abbrev = DEFAULT_ABBREV if abbrev is None else abbrev

    def _replace_abbreviations(self, text):
        """
        Replace abbreviations
        :return:
        """
        for abbrev in self.abbrev:
            text = text.replace(abbrev, "00000")
        return text

    @staticmethod
    def _replace_roman_numerals(text):
        text = re.sub(r"^[IīVXLCDMiīvxlcdm]+[\s\.]", "roman_numeral ", text)
        text = re.sub(r"\s[IīVXLCDMiīvxlcdm]+[\s\.]", " roman_numeral ", text)
        return text

    @staticmethod
    def _remove_extra_white_space(text):
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"^\s", "", text)
        return text

    def normalize(self, text):
        """
        Normalize text.
        Punctuation is standardized with the supplied punctuation list.
        :return: normalized text
        """
        default_seperator = "."

        for punc in self.punctuation:
            text = text.replace(punc, default_seperator)

        if self.replace_abbrev:
            text = self._replace_abbreviations(text)

        text = self._replace_roman_numerals(text)
        text = text.lower()
        text = self._remove_extra_white_space(text)
        return text


if __name__ == "__main__":
    test = 'Puer bona est Agr. malus?'
    normalizer = Normalizer()
    print(normalizer.normalize(test))
