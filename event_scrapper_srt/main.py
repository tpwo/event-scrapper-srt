from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict
from datetime import datetime
from pprint import pformat

from event_scrapper_srt import gancio
from event_scrapper_srt import scrapper
from event_scrapper_srt import sitemap
from event_scrapper_srt.event import Event

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'


def main() -> int:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    events = scrapper.get_events(sitemap.get_urls(SITEMAP_URL))
    dump_events_to_json(events, folder='output')
    gancio_events = gancio.create_events(events)
    # There is a default rate limiting 5 requests per 5 minutes, so we
    # iterate only on a few events
    for event in gancio_events[:5]:
        response = gancio.add_event_requests(event, instance_url='http://127.0.0.1:13120')
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
