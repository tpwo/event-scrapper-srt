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
        expected = {
            'likes': [],
            'boost': [],
            'online_locations': [],
            'id': 5,
            'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
            'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
            'multidate': '1',
            'start_datetime': '1722074400',
            'end_datetime': '1722085200',
            'recurrent': None,
            'is_visible': False,
            'media': [
                {
                    'url': '9f9e80aabd602969655156d6ebe94670.jpg',
                    'height': 628,
                    'width': 1200,
                    'name': 'Lindy Hop dla początkujacych | intensywne warsztaty',
                    'size': 227552,
                    'focalpoint': [0, 0],
                }
            ],
            'updatedAt': '2024-06-30T20:23:57.641Z',
            'createdAt': '2024-06-30T20:23:57.627Z',
            'slug': 'lindy-hop-dla-poczatkujacych-or-intensywne-warsztaty-4',
            'placeId': 1,
            'tags': [],
            'place': {
                'id': 1,
                'name': 'Studio Swing Revolution Trójmiasto',
                'address': 'ul. Łąkowa 35/38',
                'latitude': None,
                'longitude': None,
                'createdAt': '2024-06-30T16:53:41.996Z',
                'updatedAt': '2024-06-30T16:53:41.996Z',
            },
        }
        actual = add_event_requests(event)
        # Output is dynamic so we only compare selected attributes
        for key in ('title', 'description', 'start_datetime', 'end_datetime'):
            assert actual[key] == expected[key]
