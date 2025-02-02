# `unicode_age`

[![Build](https://github.com/SnoopJ/unicode_age/actions/workflows/build_wheels.yml/badge.svg?branch=main)](https://github.com/SnoopJ/unicode_age/actions/workflows/build_wheels.yml)

A package for determining what version a Unicode codepoint was added to the standard

This package's version `X.Y.Z.U` tracks Unicode version `X.Y.Z`, with `U` reserved as
a release counter for updates unrelated to the Unicode version.

## Example usage

```python
>>> import unicode_age
>>> codept = ord("\N{SNAKE}")  # added in Unicode 6.0
>>> print(unicode_age.version(codept))
(6, 0)
```

## Rationale

Before writing this module, I was parsing `DerivedAge.txt` into a `list[int | None]`,
but this approach consumes an atrocious amount of memory (10 MB) for
what it is. Using the representation here consumes three orders of magnitude
less memory (~30 KB), and it was kinda fun to write besides :)

## Updating

The script `makeunicode_age.py` consumes
[`DerivedAge.txt`](https://www.unicode.org/reports/tr44/#DerivedAge.txt) and
produces the `unicode_age_db.py` file that holds the backing data for this
library. To make a build for another version of the Unicode Character Database,
you should be able to replace `DerivedAge.txt` and re-run this script.
