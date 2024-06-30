from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import datetime
from datetime import timezone
from typing import NamedTuple

from bs4 import BeautifulSoup
from lxml import etree

HEADER_DATE_TIMES = 'Kiedy?'
HEADER_PLACE = 'Gdzie?'


class SitemapElem(NamedTuple):
    url: str
    lastmod: str


class Event(NamedTuple):
    url: str
    title: str
    description: str
    place_name: str
    place_address: str
    image_url: str | None
    date_times: list[Occurrence]


class Occurrence(NamedTuple):
    start: datetime
    end: datetime | None


class GancioEvent(NamedTuple):
    title: str
    description: str
    place_name: str
    place_address: str
    online_locations: list[str]
    start_datetime: int
    multidate: int
    tags: str
    image: bytes | None


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    sitemap_url = 'https://swingrevolution.pl/events-sitemap.xml'
    xml_content = get_xml_content(sitemap_url)
    sitemap_elems = get_events_from_sitemap(xml_content)
    events = get_events(sitemap_elems)
    future_events = get_future_events(events)
    dump_events_to_json(future_events, folder='output')


def get_xml_content(sitemap_url: str) -> bytes:
    with urllib.request.urlopen(sitemap_url) as response:
        return response.read()


def get_events_from_sitemap(xml_content: bytes, max_age_days: int = 30) -> list[SitemapElem]:
    """Extracts event URLs and lastmod dates from the sitemap XML content.

    Sitemap displays the events from the oldest to the newest, so we
    reverse the list at the end.

    Args:
        xml_content: The XML content of the sitemap.
        max_age_days: The maximum age of the event in days. Events older
        than this will be skipped.

    """
    root = etree.fromstring(xml_content)

    schema_location = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
    schema_parts = schema_location.split()
    # Define the namespace dictionary for use in xpath
    ns = {'ns': schema_parts[0]}

    elements = root.xpath('//ns:url', namespaces=ns)
    logging.info(f'Found {len(elements)} events in the sitemap')

    events = []
    for elem in reversed(elements):
        url = elem.xpath('ns:loc/text()', namespaces=ns)[0]
        lastmod = elem.xpath('ns:lastmod/text()', namespaces=ns)[0]
        try:
            lastmod_dt = datetime.fromisoformat(lastmod)
        except ValueError as err:
            logging.warning(f'Failed to parse lastmod date `{lastmod}`. Error: `{err}`')
        else:
            if event_older_than_max_age_days(lastmod_dt, max_age_days):
                logging.debug(f'Event `{url}` is older than {max_age_days} days, skipping')
            else:
                event = SitemapElem(url=url, lastmod=lastmod)
                events.append(event)

    logging.info(f'Extracted {len(events)} events from the sitemap')
    return events


def get_events(sitemap_elems: list[SitemapElem]) -> list[Event]:
    events = []
    for event in sitemap_elems:
        with urllib.request.urlopen(event.url) as response:
            html_content = response.read().decode('utf-8')
            events.append(extract_event_details(html_content, event.url))
    logging.info(f'Extracted details for {len(events)} events')
    return events


def get_future_events(events: list[Event]) -> list[Event]:
    """Filters out events that are in the past.

    Currently the event is qualified as future if any of its `date_times`
    is in the future which might be not ideal.

    TODO: decide if we should remove past dates from event `date_times` field.
    """
    future_events = []
    for event in events:
        for date_time in event.date_times:
            if date_time.start > datetime.now():
                future_events.append(event)
                break
    logging.info(f'{len(future_events)} of {len(events)} are future events')
    return future_events


def dump_events_to_json(events: list[Event], folder: str) -> None:
    os.makedirs(folder, exist_ok=True)
    filename = f'{folder}/events_{datetime.now().isoformat()}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([event._asdict() for event in events], file, indent=4, ensure_ascii=False)
    logging.info(f'Saved event details to `{filename}`')


def event_older_than_max_age_days(dt: datetime, max_age_days: int) -> bool:
    days = (dt - datetime.now(timezone.utc)).days * -1
    logging.debug(f'Event is {days} days old')
    return days > max_age_days


def extract_event_details(html_content: str, url: str) -> Event:
    soup = BeautifulSoup(html_content, 'html.parser')

    image_div = soup.find('div', class_='page-header min-vh-80 lazy')
    image_url = image_div['data-bg'].replace('url(', '').replace(')', '') if image_div else None

    title = soup.find('h1').text.strip()

    details_class = 'col-md-6 mx-auto'
    details = soup.find_all('div', class_=details_class)

    place_name, place_address = get_place_name_address(details)

    try:
        date_times = get_date_times(details)
    except ValueError:
        date_times = []
        logging.info(f'Past event found: no date and time information in `{title}`')

    return Event(
        url=url,
        title=title,
        description=get_description(soup),
        place_name=place_name,
        place_address=place_address,
        image_url=image_url,
        date_times=date_times,
    )


def get_date_times(details: list[BeautifulSoup]) -> list[Occurrence]:
    for detail in details:
        if HEADER_DATE_TIMES in detail.text:
            return extract_date_times(detail.find_all('p'))
    raise ValueError(f'Time details not found in the provided HTML content: `{details}`')


def extract_date_times(p_elems: list[BeautifulSoup]) -> list[Occurrence]:
    date_times = []
    for dt in p_elems:
        date_str = dt.find('strong').text.strip()
        start_time_str = dt.text.partition('-')[0].split()[-1]
        end_time_str = dt.text.partition('-')[-1].split()[-1]
        start_datetime = parse_polish_date(f'{date_str} {start_time_str}')
        end_timestamp = parse_polish_date(f'{date_str} {end_time_str}')
        date_times.append(Occurrence(start=start_datetime, end=end_timestamp))
    return date_times


def get_place_name_address(details: list[BeautifulSoup]) -> tuple[str, str]:
    for detail in details:
        if HEADER_PLACE in detail.text:
            place_section_raw = detail.find('p').text
            # For some reason each time the place value starts with
            # backtick, so we strip it
            place_section = place_section_raw.lstrip('`').strip()
            place_name_raw, _, place_address_raw = place_section.partition(',')
            return place_name_raw.strip(), place_address_raw.strip()
    raise ValueError(f'Place details not found in the provided HTML content: `{details}`')


def get_description(soup: BeautifulSoup) -> str:
    html_class = 'col-lg-6 justify-content-center d-flex flex-column ps-lg-5 pt-lg-0 pt-3'
    desc_section = soup.find('div', class_=html_class)
    desc = desc_section.find('p').decode_contents().strip() if desc_section else ''
    desc_formatted = ' '.join(desc.replace('\n', '').split())
    return desc_formatted


# Polish month names mapping
MONTHS_PL = {
    'stycznia': 1,
    'lutego': 2,
    'marca': 3,
    'kwietnia': 4,
    'maja': 5,
    'czerwca': 6,
    'lipca': 7,
    'sierpnia': 8,
    'września': 9,
    'października': 10,
    'listopada': 11,
    'grudnia': 12,
}


def parse_polish_date(date_str: str) -> datetime:
    for pl_month, month_num in MONTHS_PL.items():
        if pl_month in date_str:
            date_str = date_str.replace(pl_month, f'{month_num:02}')
            return datetime.strptime(date_str, '%d %m %Y %H:%M')
    raise ValueError(f'Polish month name not found in the provided date string: {date_str}')


def get_image(image_url: str) -> bytes:
    image_response = urllib.request.urlopen(image_url)
    return image_response.read()


def prepare_gancio_event(
    event: Event, img_getter: Callable[[str], bytes] = get_image
) -> GancioEvent:
    # Structure based on Gancio API
    # https://gancio.org/dev/api#add-a-new-event
    if event.image_url:
        image = img_getter(event.image_url)
    else:
        image = None
    return GancioEvent(
        title=event.title,
        description=event.description,
        place_name=event.place_name,
        place_address=event.place_address,
        online_locations=[event.url],
        start_datetime=int(event.date_times[0].start.timestamp()),
        # Assuming these are not multidate events
        multidate=0,
        tags=json.dumps(['swing']),
        image=image,
    )


def add_event(event: GancioEvent) -> dict[str, object]:
    url = 'http://127.0.0.1:13120/api/event'
    data = json.dumps(event._asdict()).encode()
    headers = {'Content-Type': 'application/json'}
    resp = urllib.request.urlopen(
        urllib.request.Request(url, data=data, headers=headers, method='POST')
    )
    return json.load(resp)


if __name__ == '__main__':
    main()
