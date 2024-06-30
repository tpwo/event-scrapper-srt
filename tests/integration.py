"""Tests which require Gancio to be running on localhost.

The filename doesn't have `test` in the name, so pytest won't pick it up by default.

These tests should be run like that:

    pytest tests/integration.py
"""
from __future__ import annotations

from event_scrapper_srt import add_event_requests
from event_scrapper_srt import prepare_gancio_event
from testing.resources import example_event


def test_add_event():
    gancio_event = prepare_gancio_event(example_event)
    for event in gancio_event:
        add_event_requests(event)
