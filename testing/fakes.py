from __future__ import annotations

import pathlib


def content_getter(path: str) -> bytes:
    """Fake webpage content getter. Instead of HTML it returns a content of a file."""
    return pathlib.Path(path).read_bytes()
