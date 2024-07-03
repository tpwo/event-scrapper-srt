from __future__ import annotations

import freezegun

from event_scrapper_srt import sitemap
from testing import fakes


@freezegun.freeze_time('2023-02-28')
def test_get_urls():
    actual = sitemap.get_urls(
        'testing/example-events-sitemap.xml', content_getter=fakes.content_getter
    )
    expected = [
        'https://swingrevolution.pl/wydarzenia/sunday-summer-night-coniedzielna-potancowka/',
        'https://swingrevolution.pl/wydarzenia/practice-chill/',
        'https://swingrevolution.pl/wydarzenia/w-rytmie-swinga-potancowka/',
    ]
    assert actual == expected
