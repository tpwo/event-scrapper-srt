"""Tests which require Gancio to be running on localhost.

The filename doesn't have `test` in the name, so pytest won't pick it up by default.

These tests should be run like that:

    pytest tests/integration.py
"""

from __future__ import annotations

import shutil
import subprocess
import time

import pytest

from event_scrapper_srt import gancio
from testing.resources import example_event


@pytest.fixture
def gancio_instance(tmp_path):
    shutil.copytree('testing/gancio', tmp_path / 'gancio')
    out = subprocess.run(
        ('docker', 'compose', '--file', tmp_path / 'gancio/docker-compose.yml', 'up', '--detach'),
        check=True,
    )
    time.sleep(10)
    yield out
    subprocess.run(
        ('docker', 'compose', '--file', tmp_path / 'gancio/docker-compose.yml', 'down'), check=True
    )


def test_add_event(gancio_instance):
    gancio_event = gancio.prepare_event(example_event)
    for event in gancio_event:
        expected = {
            'likes': [],
            'boost': [],
            'online_locations': [],
            'id': 5,
            'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
            'description': '<p>Daj się zarazić swingowym bakcylem podczas intensywnych warsztatów od podstaw! Nie musisz nic umieć (większość z nas tak właśnie zaczynała), a jeśli plączą Ci się nogi – wspólnie je rozplączemy. 🙂 Udowodnimy Ci, że taniec może być prosty i przyjemny, a to wszystko w doborowym towarzystwie pozytywnie zakręconych ludzi i przy dźwiękach porywającego do tańca swinga.</p><p>🔸 ZAPISY 🔸<br> · Zajęcia odbędą się w sobotę 27 lipca (3h, od 12:00-15:00).<br> · Na zajęciach zmieniamy się w parach.<br> · Nie potrzebujesz pary do wzięcia udziału w zajęciach. Przy zapisach dbamy o odpowiednie proporcje w grupie.<br> · Każda osoba musi wypełnić osobny formularz (nawet gdy zapisujesz się w parze).<br> ❗ Ilość miejsc na zajęciach jest ograniczona.</p>',
            'multidate': '1',
            'start_datetime': '1722074400',
            'end_datetime': '1722085200',
            'recurrent': None,
            'is_visible': False,
            'media': [],
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
        actual = gancio.add_event_requests(event, instance_url='http://127.0.0.1:13121')
        # Output is dynamic so we only compare selected attributes
        for key in ('title', 'description', 'start_datetime', 'end_datetime'):
            assert actual[key] == expected[key]
