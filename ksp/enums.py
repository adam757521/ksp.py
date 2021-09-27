from enum import Enum


class Languages(Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    HEBREW = "he"


class Sorts(Enum):
    LOW_TO_HIGH = 1
    HIGH_TO_LOW = 2
    NEW_TO_OLD = 3
    OLD_TO_NEW = 4
    POPULARITY = 5
