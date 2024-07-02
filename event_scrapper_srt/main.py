from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime
from pprint import pformat

import requests

from event_scrapper_srt.event import Event
from event_scrapper_srt.event import GancioEvent
from event_scrapper_srt.scrapper import get_events
from event_scrapper_srt.scrapper import get_events_from_sitemap
from event_scrapper_srt.util import get_url_content

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'


def main() -> int:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    xml_content = get_url_content(SITEMAP_URL)
    sitemap_elems = get_events_from_sitemap(xml_content)
    events = get_events(sitemap_elems)
    dump_events_to_json(events, folder='output')
    gancio_events = get_gancio_events(events)
    future_events = get_future_events(gancio_events)
    # There is a default rate limiting 5 requests per 5 minutes, so we
    # iterate only on a few events
    for event in future_events[:5]:
        response = add_event_requests(event, instance_url='http://127.0.0.1:13120')
        logging.info(f'Event added:\n{pformat(response)}')
        print(''.center(80, '-'))
    return 0


def get_gancio_events(events: list[Event]) -> list[GancioEvent]:
    gancio_events = []
    for event in events:
        gancio_events.extend(prepare_gancio_event(event))
    logging.info(f'Prepared {len(gancio_events)} events for Gancio')
    return gancio_events


def get_future_events(events: list[GancioEvent]) -> list[GancioEvent]:
    """Filters out past events."""
    future_events = []
    for event in events:
        if datetime.fromtimestamp(event.start_datetime) > datetime.now():
            future_events.append(event)
    logging.info(f'{len(future_events)} of {len(events)} are future events')
    return future_events


def dump_events_to_json(events: list[Event], folder: str) -> None:
    os.makedirs(folder, exist_ok=True)
    filename = f'{folder}/events_{datetime.now().isoformat()}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(
            [asdict(event) for event in events], file, indent=4, ensure_ascii=False, default=str
        )
    logging.info(f'Saved event details to `{filename}`')


def get_image(image_url: str) -> bytes:
    image_response = urllib.request.urlopen(image_url)
    return image_response.read()


def prepare_gancio_event(
    event: Event, img_getter: Callable[[str], bytes] = get_image
) -> list[GancioEvent]:
    if event.image_url:
        image = img_getter(event.image_url)
    else:
        image = None
    events = []
    for dt in event.date_times:
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
                image=image,
            )
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
    files = {'image': ('image', event.image, 'application/octet-stream')}
    response = requests.post(url, data=data, files=files)  # type: ignore[arg-type]

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


if __name__ == '__main__':
    main()
