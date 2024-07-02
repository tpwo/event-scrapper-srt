from __future__ import annotations

import urllib.request


def get_url_content(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:
        return response.read()
