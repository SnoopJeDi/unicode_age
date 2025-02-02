from __future__ import annotations

from typing import Tuple

from .unicode_age_db import iter_spans


UCDVersion = Tuple[int, int]


def version(codept: int) -> UCDVersion | None:
    for (start, stop, major, minor) in iter_spans():
        if start <= codept <= stop:
            return (major, minor)

    # linear scan failed
    raise ValueError("Codepoint U+{codept:x} was not allocated as of UCD {UCD_VERSION}")
