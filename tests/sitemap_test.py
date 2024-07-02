from __future__ import annotations

import pathlib

import freezegun

from event_scrapper_srt import sitemap
from event_scrapper_srt.sitemap import SitemapElem


@freezegun.freeze_time('2023-02-28')
def test_get_events_from_sitemap():
    xml_content = pathlib.Path('testing/example-events-sitemap.xml').read_bytes()
    actual = sitemap.get_elements(xml_content=xml_content, max_age_days=30)
    expected = [
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/sunday-summer-night-coniedzielna-potancowka/',
            lastmod='2024-06-25T10:08:35+00:00',
        ),
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/practice-chill/',
            lastmod='2024-06-25T10:06:15+00:00',
        ),
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/w-rytmie-swinga-potancowka/',
            lastmod='2023-01-30T16:59:29+00:00',
        ),
    ]
    assert actual == expected
