from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

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
    parser.add_argument(
        '--output-path',
        default=f'output/{datetime.now().isoformat()}.json',
        help='JSON with scrapped events is saved there (default: %(default)s)',
    )
    args = parser.parse_args(argv)

    events = scrapper.get_events(sitemap.get_urls(args.sitemap_url))
    gancio_events = gancio.create_events(events)

    dump_events_to_json(gancio_events, output_path=args.output_path)

    return 0


def dump_events_to_json(events: list[GancioEvent], output_path: str) -> None:
    """Saves scrapped events to Newline Delimited JSON."""
    path = Path(output_path)

    if path.exists():
        raise SystemExit(f'Error: `{path.absolute()}` already exists')

    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        logging.info(f'Created folder `{path.parent.absolute()}`')

    with open(path, 'w', encoding='utf-8') as file:
        for event in events:
            json.dump(asdict(event), file, indent=None, ensure_ascii=False, default=str)
            file.write('\n')
    logging.info(f'Saved {len(events)} events to `{path.absolute()}`')


if __name__ == '__main__':
    main()
