from __future__ import annotations

import logging
import pathlib

import pytest

from event_scrapper_srt import scrapper
from testing import resources


@pytest.mark.parametrize(
    ('url', 'expected'),
    (
        ('example-event.html', [resources.example_event]),
        ('example-event-recurring.html', [resources.example_event_recurring]),
    ),
)
def test_get_events(url, expected):
    actual = scrapper.get_events([f'testing/{url}'], html_getter=get_html_fake)
    assert actual[0] == expected[0]
    assert len(actual) == len(expected) == 1


def get_html_fake(path: str) -> bytes:
    """Fake HTML getter. Instead of HTML it returns content of a file."""
    return pathlib.Path(path).read_bytes()


@pytest.mark.parametrize(
    ('file', 'expected'),
    (
        ('example-event.html', resources.example_event),
        ('example-event-recurring.html', resources.example_event_recurring),
    ),
)
def test_extract_event_details(file, expected):
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = scrapper.extract_event_details(html_content=html_content, url=f'testing/{file}')
    assert actual == expected


@pytest.mark.parametrize(
    ('file', 'expected'),
    (('example-event-past.html', resources.example_event_past),),
)
def test_extract_past_event_details(file, expected, caplog):
    caplog.set_level(logging.INFO)
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = scrapper.extract_event_details(html_content=html_content, url=f'testing/{file}')
    assert actual == expected
    assert 'Past event found: no date and time information' in caplog.text
