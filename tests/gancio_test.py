from __future__ import annotations

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


def get_image_mock(image_url: str) -> bytes:
    return b''
