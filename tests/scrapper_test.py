from __future__ import annotations

import logging

import pytest

from event_scrapper_srt import scrapper
from testing import fakes
from testing import resources


@pytest.mark.parametrize(
    ('url', 'expected'),
    [
        ('example-event.html', [resources.example_event]),
        ('example-event-recurring.html', [resources.example_event_recurring]),
    ],
)
def test_get_events(url, expected, caplog):
    caplog.set_level(logging.INFO)
    actual = scrapper.get_events([f'testing/{url}'], content_getter=fakes.content_getter)
    assert actual[0] == expected[0]
    assert len(actual) == len(expected) == 1
    assert 'Extracted details for 1 events' in caplog.text


@pytest.mark.parametrize(
    ('url', 'expected'),
    [
        ('example-event-past.html', [resources.example_event_past]),
    ],
)
def test_get_events_past(url, expected, caplog):
    caplog.set_level(logging.INFO)
    actual = scrapper.get_events([f'testing/{url}'], content_getter=fakes.content_getter)
    assert actual[0] == expected[0]
    assert len(actual) == len(expected) == 1
    assert '[Swingowa potańcówka nad Motławą] No date and time information found' in caplog.text
