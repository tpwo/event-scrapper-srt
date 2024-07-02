from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict
from datetime import datetime
from pprint import pformat

from event_scrapper_srt.event import Event
from event_scrapper_srt.gancio import add_event_requests
from event_scrapper_srt.gancio import get_future_events
from event_scrapper_srt.gancio import get_gancio_events
from event_scrapper_srt.scrapper import get_events
from event_scrapper_srt.sitemap import get_elements
from event_scrapper_srt.util import get_url_content

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'


def main() -> int:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    xml_content = get_url_content(SITEMAP_URL)
    sitemap_elems = get_elements(xml_content)
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


def dump_events_to_json(events: list[Event], folder: str) -> None:
    os.makedirs(folder, exist_ok=True)
    filename = f'{folder}/events_{datetime.now().isoformat()}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(
            [asdict(event) for event in events], file, indent=4, ensure_ascii=False, default=str
        )
    logging.info(f'Saved event details to `{filename}`')


if __name__ == '__main__':
    main()
