"""Enums used by pictoken"""

import sys
from enum import unique

# This project supports Python versions lower than 3.11, thus
# we use a backport for StrEnum when needed.
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


@unique
class Model(StrEnum):
    CHATGPT_4O_LATEST = "chatgpt-4o-latest"
    GPT_4O = "gpt-4o"
    GPT_4O_2024_05_13 = "gpt-4o-2024-05-13"
    GPT_4O_2024_08_06 = "gpt-4o-2024-08-06"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_TURBO_2024_04_09 = "gpt-4-turbo-2024-04-09"


@unique
class ImageDetail(StrEnum):
    LOW = "low"
    HIGH = "high"
    AUTO = "auto"
