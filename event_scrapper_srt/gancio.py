from __future__ import annotations

import json
import logging
import urllib.request
from dataclasses import asdict
from datetime import datetime

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
        end_datetime = int(dt.end.timestamp()) if dt.end else None
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


def add_event(event: GancioEvent, instance_url: str) -> dict[str, object]:
    url = f'{instance_url}/api/event'
    data = json.dumps(asdict(event)).encode()
    headers = {'Content-Type': 'application/json'}
    resp = urllib.request.urlopen(
        urllib.request.Request(url, data=data, headers=headers, method='POST')
    )
    return json.load(resp)
