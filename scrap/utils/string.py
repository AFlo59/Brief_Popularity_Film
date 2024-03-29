import html
import unicodedata as ud
import re
from typing import AnyStr


def normalize(str: AnyStr) -> AnyStr:
    # escape HTML
    str = html.unescape(str)
    # lowercase
    str = str.lower()
    # remove punctuation
    str = re.sub(r"[^\w\s]", "", str)
    # remove multiple space
    str = re.sub(r"\s\s+", " ", str)
    # remove white spaces
    str = str.strip()

    return ud.normalize("NFKD", str).encode("ascii", "ignore").decode("utf8")


def convert_int(s, default=-1):
    try:
        i = int(s)
    except ValueError:
        i = default
    return i
