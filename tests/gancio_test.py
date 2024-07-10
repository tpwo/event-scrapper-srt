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
@freezegun.freeze_time('2024-07-01')
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
@freezegun.freeze_time('2025-01-01')
def test_prepare_gancio_event_skip_all(details, caplog):
    caplog.set_level(logging.INFO)
    actual = gancio.prepare_event(event=details, img_getter=get_image_mock)
    assert actual == []
    assert 'Past event occurence found' in caplog.text
    assert 'No Gancio events created: no future `date_times` found' in caplog.text


@freezegun.freeze_time('2024-07-10')
def test_prepare_gancio_event_one_skip_one_create(caplog):
    caplog.set_level(logging.INFO)
    actual = gancio.prepare_event(
        event=resources.example_event_recurring, img_getter=get_image_mock
    )
    assert actual == [resources.example_event_recurring_gancio[-1]]
    assert 'Prepared 1 events for Gancio' in caplog.text
    assert 'Skipped 1 of 2 scrapped occurrences' in caplog.text


def test_prepare_gancio_event_no_date_times_found(caplog):
    caplog.set_level(logging.INFO)
    actual = gancio.prepare_event(event=resources.example_event_past, img_getter=get_image_mock)
    assert actual == []
    assert (
        '[Swingowa potańcówka nad Motławą] No Gancio events created: '
        'no future `date_times` found' in caplog.text
    )


def get_image_mock(image_url: str) -> bytes:
    return b''
