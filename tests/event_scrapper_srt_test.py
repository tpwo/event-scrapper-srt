from __future__ import annotations

import logging
import pathlib

import freezegun
import pytest

import event_scrapper_srt
from event_scrapper_srt import SitemapElem
from testing import resources


@freezegun.freeze_time('2023-02-28')
def test_get_events_from_sitemap():
    xml_content = pathlib.Path('testing/example-events-sitemap.xml').read_bytes()
    actual = event_scrapper_srt.get_events_from_sitemap(xml_content=xml_content, max_age_days=30)
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


@pytest.mark.parametrize(
    ('file', 'expected'),
    (
        ('example-event.html', resources.example_event),
        ('example-event-recurring.html', resources.example_event_recurring),
    ),
)
def test_extract_event_details(file, expected):
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = event_scrapper_srt.extract_event_details(html_content=html_content)
    assert actual == expected


@pytest.mark.parametrize(
    ('file', 'expected'),
    (('example-event-past.html', resources.example_event_past),),
)
def test_extract_past_event_details(file, expected, caplog):
    caplog.set_level(logging.INFO)
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = event_scrapper_srt.extract_event_details(html_content=html_content)
    assert actual == expected
    assert 'Past event found: no date and time information' in caplog.text


@pytest.mark.parametrize(
    ('details', 'expected'),
    (
        (resources.example_event, resources.example_event_gancio),
        (resources.example_event_recurring, resources.example_event_recurring_gancio),
    ),
)
def test_prepare_gancio_event(details, expected):
    actual = event_scrapper_srt.prepare_gancio_event(
        event_details=details, img_getter=get_image_mock
    )
    assert actual == expected


def get_image_mock(image_url: str) -> bytes:
    return b''
