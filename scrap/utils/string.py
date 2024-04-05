import html
from types import NoneType
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
    # char special
    str = re.sub(r"[œ]", "oe", str)
    # remove multiple space
    str = re.sub(r"\s\s+", " ", str)
    # remove white spaces
    str = str.strip()

    return ud.normalize("NFKD", str).encode("ascii", "ignore").decode("utf8")


def convert_int(s: AnyStr, default=-1):
    if s is None:
        return default

    if isinstance(s, int):
        return s

    s = normalize(s)
    try:
        s = s.replace(" ", "")
        i = int(s)
    except Exception:
        i = default
    return i


def convert_float(s: AnyStr, default=-1):
    if s is None:
        return default

    if isinstance(s, float):
        return s

    try:
        s = s.replace(" ", "")
        s = s.replace(",", ".")
        i = float(s)
    except Exception:
        i = default
    return i
