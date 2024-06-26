from __future__ import annotations

import pathlib

import pytest

import event_scrapper_srt
from event_scrapper_srt import Event


def test_get_events_from_sitemap():
    xml_content = pathlib.Path('testing/example-events-sitemap.xml').read_bytes()
    actual = event_scrapper_srt.get_events(xml_content=xml_content)
    expected = [
        Event(
            url='https://swingrevolution.pl/wydarzenia/swingowa-potancowka-nad-motlawa/',
            lastmod='2023-01-07T14:28:50+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/w-rytmie-swinga-potancowka/',
            lastmod='2023-01-30T16:59:29+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/practice-chill/',
            lastmod='2024-06-25T10:06:15+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/sunday-summer-night-coniedzielna-potancowka/',
            lastmod='2024-06-25T10:08:35+00:00',
        ),
    ]
    assert actual == expected


@pytest.mark.parametrize(
    'file',
    (
        'example-event.html',
        'example-event-recurring.html',
    ),
)
def test_extract_event_details(file):
    html_content = pathlib.Path(f'testing/{file}').read_text()
    event_scrapper_srt.extract_event_details(html_content=html_content)
