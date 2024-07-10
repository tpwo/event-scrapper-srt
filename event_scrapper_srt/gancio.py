from __future__ import annotations

import json
import logging
import urllib
from dataclasses import asdict
from datetime import datetime

import requests

from event_scrapper_srt.event import Event
from event_scrapper_srt.event import GancioEvent


def create_events(scrapped_events: list[Event]) -> list[GancioEvent]:
    """Returns objects representing future events for Gancio based on scrapped events."""
    events = []
    for scrapped in scrapped_events:
        events.extend(prepare_event(scrapped))
    return events


def prepare_event(
    event: Event,
) -> list[GancioEvent]:
    """Prepares one or more Gancio event from a single scrapped event.

    Skips past events.
    """
    events = []
    skipped = 0
    for dt in event.date_times:
        if dt.start < datetime.now(tz=dt.start.tzinfo):
            logging.info(f'[{event.title}] Past event occurence found, skipping: {dt.start}')
            skipped += 1
            continue
        if dt.end:
            end_datetime = int(dt.end.timestamp())
        else:
            end_datetime = None
        events.append(
            GancioEvent(
                title=event.title,
                description=event.description,
                place_name=event.place_name,
                place_address=event.place_address,
                online_locations=[event.url],
                start_datetime=int(dt.start.timestamp()),
                end_datetime=end_datetime,
                # Always set event as multidate, as it doesn't break
                # anything, and without it mutlidate events are
                # incorrectly added.
                multidate=1,
                tags=['swing'],
                image_url=event.image_url,
            )
        )
    if not events:
        logging.info(f'[{event.title}] No Gancio events created: no future `date_times` found')
        return []
    else:
        logging.info(f'[{event.title}] Prepared {len(events)} events for Gancio')
        if skipped > 0:
            logging.info(
                f'[{event.title}] Skipped {skipped} of {len(event.date_times)} scrapped occurrences'
            )
        return events


def add_event_requests(event: GancioEvent, instance_url: str) -> dict[str, object]:
    """Add an event to Gancio using the requests library.

    Args:
        event: The event to be added.
        instance_url: The URL and port of the Gancio instance, e.g.
                      `http://127.0.0.1:13120` for local running.

    TODO:
    - issue with tags, 500 server error, it worked with urllib
    - issue with online_locations, it creates a location per character (!)
    """
    url = f'{instance_url}/api/event'
    data = {
        'title': event.title,
        'description': event.description,
        'place_name': event.place_name,
        'place_address': event.place_address,
        # 'online_locations': event.online_locations[0],
        'start_datetime': event.start_datetime,
        'end_datetime': event.end_datetime,
        'multidate': 1,
        # 'tags': event.tags,
    }
    response = requests.post(url, data=data)

    response.raise_for_status()

    return response.json()


def add_event(event: GancioEvent) -> dict[str, object]:
    url = 'http://127.0.0.1:13120/api/event'
    data = json.dumps(asdict(event)).encode()
    headers = {'Content-Type': 'application/json'}
    resp = urllib.request.urlopen(
        urllib.request.Request(url, data=data, headers=headers, method='POST')
    )
    return json.load(resp)
