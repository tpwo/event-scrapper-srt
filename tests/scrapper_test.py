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


@pytest.mark.parametrize(
    ('url', 'expected'),
    (('example-event-past.html', [resources.example_event_past]),),
)
def test_get_events_past(url, expected, caplog):
    caplog.set_level(logging.INFO)
    actual = scrapper.get_events([f'testing/{url}'], html_getter=get_html_fake)
    assert actual[0] == expected[0]
    assert len(actual) == len(expected) == 1
    assert (
        'Past event found: no date and time information in `Swingowa potańcówka nad Motławą`'
        in caplog.text
    )


def get_html_fake(path: str) -> bytes:
    """Fake HTML getter. Instead of HTML it returns content of a file."""
    return pathlib.Path(path).read_bytes()
