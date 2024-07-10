from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict

from event_scrapper_srt import gancio
from event_scrapper_srt import scrapper
from event_scrapper_srt import sitemap
from event_scrapper_srt.event import GancioEvent

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(prog='event_scrapper_srt')
    parser.add_argument(
        '--sitemap-url',
        default=SITEMAP_URL,
        help='events are scrapped from here (default: %(default)s)',
    )
    args = parser.parse_args(argv)

    events = scrapper.get_events(sitemap.get_urls(args.sitemap_url))
    gancio_events = gancio.create_events(events)
    logging.info(f'In total prepared {len(gancio_events)} events for Gancio')
    logging.info('Dumping output to stdout...')

    dump_events_to_json(gancio_events)

    return 0


def dump_events_to_json(events: list[GancioEvent]) -> None:
    """Dump scrapped events to stdout as Newline Delimited JSON."""
    for event in events:
        json.dump(asdict(event), sys.stdout, indent=None, ensure_ascii=False, default=str)
        print()


if __name__ == '__main__':
    main()
