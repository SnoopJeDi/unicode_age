from __future__ import annotations
import re
import struct
import sys
from pathlib import Path
from textwrap import dedent


HERE = Path(__file__).parent.resolve()
DERIVEDAGES = HERE.joinpath("DerivedAge.txt")


def _write_spans(spans: list, ucd_version: tuple, outfile: Path):
    span_fmt = "iibb"
    VersionSpan = struct.Struct(span_fmt)

    Nbytes = len(spans) * VersionSpan.size
    buf = bytearray(Nbytes)

    for n, s in enumerate(spans):
        VersionSpan.pack_into(buf, n*VersionSpan.size, *s)

    py_src = dedent(f"""
    from __future__ import annotations
    import struct

    UCD_VERSION = {ucd_version}

    VersionSpan = struct.Struct({span_fmt!r})

    def iter_spans():
        yield from VersionSpan.iter_unpack(VERSION_SPANS)

    VERSION_SPANS = {repr(buf)}
    """)


    outfile.write_text(py_src)
    print(f"Wrote to {outfile}")


def _derivedage_spans(fn):
    CODEPT = r"[0-9A-Fa-f]+"
    PATT = rf"^({CODEPT})(?:\.\.({CODEPT}))?\s*;\s*([\d.]+)\s*#.*"

    with open(fn, "r") as f:
        for line in f:
            if line.strip() and line.startswith("#"):
                continue
            if m := re.match(PATT, line):
                start, stop, ver = m.groups()
                start = int(start, base=16)
                if stop:
                    stop = int(stop, base=16)
                    stop = min(stop, sys.maxunicode)
                else:
                    stop = start

                major, minor = [int(part) for part in ver.split('.')]

                yield start, stop, major, minor


def parse_ucdversion(fn: Path) -> tuple[int, int, int]:
    with open(fn, "r") as f:
        patt = r"DerivedAge-(?P<version>\d+\.\d+\.\d+)\.txt"
        m = re.search(patt, f.readline())
        if not m:
            raise ValueError("Cannot determine UCD version of {str(fn)!r}")

    ver = tuple(int(val) for val in m.group("version").split('.'))
    return ver


def main():
    ucd_version = parse_ucdversion(DERIVEDAGES)
    print(f"Scanning for version spans for UCD {ucd_version}: {str(DERIVEDAGES)}")
    spans = list(_derivedage_spans(DERIVEDAGES))
    print(f"Found {len(spans)} versioned spans")

    UNICODE_AGE = HERE.joinpath("src", "unicode_age")
    PYTHON_OUTFILE = UNICODE_AGE.joinpath("unicode_age_db.py")

    _write_spans(
        spans,
        ucd_version=ucd_version,
        outfile=PYTHON_OUTFILE,
    )


if __name__ == "__main__":
    main()
