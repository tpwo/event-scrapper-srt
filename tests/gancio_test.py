from __future__ import annotations

import logging

import freezegun
import pytest

from event_scrapper_srt import gancio
from testing import resources


@pytest.mark.parametrize(
    ('details', 'expected'),
    (
        (resources.example_event, resources.example_event_gancio),
        (resources.example_event_recurring, resources.example_event_recurring_gancio),
    ),
)
def test_prepare_gancio_event(details, expected):
    actual = gancio.prepare_event(event=details, img_getter=get_image_mock)
    assert actual == expected


@pytest.mark.parametrize(
    ('details'),
    (
        resources.example_event,
        resources.example_event_recurring,
    ),
)
# Events are older than the frozen time
@freezegun.freeze_time('2025-01-01')
def test_prepare_gancio_event_past(details, caplog):
    caplog.set_level(logging.INFO)
    actual = gancio.prepare_event(event=details, img_getter=get_image_mock)
    assert actual == []
    assert 'Past event occurence found in scrapped' in caplog.text
    assert 'Prepared 0 events for Gancio' in caplog.text


def test_prepare_gancio_event_no_date_times_found(caplog):
    caplog.set_level(logging.INFO)
    actual = gancio.prepare_event(event=resources.example_event_past, img_getter=get_image_mock)
    assert actual == []
    assert (
        'No Gancio events created: no `date_times` in scrapped '
        '`Swingowa potańcówka nad Motławą`' in caplog.text
    )


def get_image_mock(image_url: str) -> bytes:
    return b''
