from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import asdict
from datetime import datetime
from pprint import pformat

from event_scrapper_srt import gancio
from event_scrapper_srt import scrapper
from event_scrapper_srt import sitemap
from event_scrapper_srt.event import GancioEvent

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'
GANCIO_URL = 'http://127.0.0.1:13120'


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(prog='event_scrapper_srt')
    parser.add_argument(
        '--sitemap-url',
        default=SITEMAP_URL,
        help='events are scrapped from here (default: %(default)s)',
    )
    parser.add_argument(
        '--gancio-url', default=GANCIO_URL, help='events are published there (default: %(default)s)'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='JSON with scrapped events is saved there (default: %(default)s)',
    )
    parser.add_argument(
        '--max-events-publish',
        type=int,
        default=5,
        help='publish maximum that many events to gancio (default: %(default)s)',
    )
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='do not ask for confirmation before publishing events',
    )
    args = parser.parse_args(argv)

    events = scrapper.get_events(sitemap.get_urls(args.sitemap_url))
    gancio_events = gancio.create_events(events)
    dump_events_to_json(gancio_events, folder=args.output_dir)
    logging.info(f'Prepared {len(gancio_events)} Gancio events for publishing')

    confirm = not args.no_confirm
    if confirm:
        if input(f'Continue with publishing events to `{args.gancio_url}` (y/N)? ') != 'y':
            raise SystemExit('Aborting')

    # There is a default rate limiting 5 requests per 5 minutes, so we
    # iterate only on a few events
    for event in gancio_events[: args.max_events_publish]:
        response = gancio.add_event(event, instance_url=args.gancio_url)
        logging.info(f'Event added:\n{pformat(response)}')
        print(''.center(80, '-'))
    return 0


def dump_events_to_json(events: list[GancioEvent], folder: str) -> None:
    """Saves scrapped events to JSON for better traceability."""
    os.makedirs(folder, exist_ok=True)
    filename = f'{folder}/events_{datetime.now().isoformat()}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(
            [asdict(event) for event in events], file, indent=4, ensure_ascii=False, default=str
        )
    logging.info(f'Saved event details to `{filename}`')


if __name__ == '__main__':
    main()
