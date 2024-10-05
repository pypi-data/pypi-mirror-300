from enum import Enum
from random import choice, random

from grapheme import graphemes

from .fixtures import character_mappings


class JankLevel(Enum):
    NONE = 0
    MINIMAL = 1
    JANK = 2
    # ZALGO = 3


def _charmap(ch):
    return choice(character_mappings[ch])


def _convert(ch, level):
    match level:
        case JankLevel.MINIMAL:
            if ch in character_mappings.keys():
                if random() > 0.5:
                    return _charmap(ch)
        case JankLevel.JANK:
            if ch in character_mappings.keys():
                return _charmap(ch)
    return ch


def jank(string, level=JankLevel.MINIMAL):
    return "".join(_convert(ch, level) for ch in graphemes(string))
