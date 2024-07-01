from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from collections.abc import Callable
from collections.abc import Sequence
from collections.abc import Sized
from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from pprint import pformat
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from lxml import etree

SITEMAP_URL = 'https://swingrevolution.pl/events-sitemap.xml'
HEADER_DESCRIPTION = 'Trochę szczegółów'
HEADER_DATE_TIMES = 'Kiedy?'
HEADER_PLACE = 'Gdzie?'


@dataclass(frozen=True)
class SitemapElem:
    url: str
    lastmod: str


@dataclass(frozen=True)
class Event:
    url: str
    title: str
    description: str
    place_name: str
    place_address: str
    image_url: str | None
    date_times: list[Occurrence]


@dataclass(frozen=True)
class Occurrence:
    start: datetime
    end: datetime | None


@dataclass(frozen=True)
class GancioEvent:
    """Represents an API request to create a new event in Gancio.

    Documentation:
    https://gancio.org/dev/api#add-a-new-event
    """

    title: str
    description: str
    place_name: str
    place_address: str
    online_locations: list[str]
    start_datetime: int
    end_datetime: int | None
    multidate: int
    tags: list[str]
    image: bytes | None


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    xml_content = get_xml_content(SITEMAP_URL)
    sitemap_elems = get_events_from_sitemap(xml_content)
    events = get_events(sitemap_elems)
    dump_events_to_json(events, folder='output')
    gancio_events = get_gancio_events(events)
    future_events = get_future_events(gancio_events)
    # There is a default rate limiting 5 requests per 5 minutes, so we
    # iterate only on a few events
    for event in future_events[:5]:
        response = add_event_requests(event)
        logging.info(f'Event added:\n{pformat(response)}')
        print(''.center(80, '-'))


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
    ns = {'ns': str(schema_parts[0])}

    elements = root.xpath('//ns:url', namespaces=ns)
    if isinstance(elements, Sized):
        logging.info(f'Found {len(elements)} events in the sitemap')
    else:
        raise SystemExit(f'No events found in the sitemap. `elements`: `{elements}')

    events = []
    for elem in reversed(elements):
        assert isinstance(elem, etree._Element)
        url = get_xpath_value(elem, 'ns:loc/text()', ns)
        lastmod = get_xpath_value(elem, 'ns:lastmod/text()', ns)
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


def get_xpath_value(elem: etree._Element, path: str, namespace: dict[str, str]) -> str:
    all = elem.xpath(path, namespaces=namespace)
    assert isinstance(all, Sequence)
    return str(all[0])


def get_events(sitemap_elems: list[SitemapElem]) -> list[Event]:
    events = []
    for event in sitemap_elems:
        with urllib.request.urlopen(event.url) as response:
            html_content = response.read().decode('utf-8')
            events.append(extract_event_details(html_content, event.url))
    logging.info(f'Extracted details for {len(events)} events')
    return events


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


def event_older_than_max_age_days(dt: datetime, max_age_days: int) -> bool:
    days = (dt - datetime.now(timezone.utc)).days * -1
    logging.debug(f'Event is {days} days old')
    return days > max_age_days


def extract_event_details(html_content: str, url: str) -> Event:
    soup = BeautifulSoup(html_content, 'html.parser')

    title = get_title(soup)
    image_url = get_image_url(soup)
    place_name, place_address = get_place_name_address(soup)

    try:
        date_times = get_date_times(soup)
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


def get_title(soup: BeautifulSoup) -> str:
    for elem in soup.find_all('h1'):
        return elem.text.strip()
    raise ValueError(f'Title not found in the provided HTML content: `{soup}`')


def get_image_url(soup: BeautifulSoup) -> str | None:
    for elem in soup.find_all('header'):
        for div in elem.find_all('div'):
            return div['data-bg'].partition('(')[-1].partition(')')[0]
    logging.warning(f'Failed to extract image url from HTML content: `{soup}`')
    return None


def get_date_times(soup: BeautifulSoup) -> list[Occurrence]:
    for elem in soup.find_all('h5'):
        if HEADER_DATE_TIMES in elem.text:
            return extract_date_times(elem.parent.find_all('p'))
    raise ValueError(f'Time details not found in the provided HTML content: `{soup}`')


def extract_date_times(p_elems: list[BeautifulSoup]) -> list[Occurrence]:
    date_times = []
    for dt in p_elems:
        if date_str_raw := dt.find('strong'):
            date_str = date_str_raw.text.strip()
            start_time_str = dt.text.partition('-')[0].split()[-1]
            start_datetime = parse_polish_date(f'{date_str} {start_time_str}')
            end_timestamp = get_end_timestamp(dt.text, date_str)
            date_times.append(Occurrence(start=start_datetime, end=end_timestamp))
    return date_times


def get_end_timestamp(dt_text: str, date_str: str) -> datetime | None:
    try:
        end_time_str = dt_text.partition('-')[-1].split()[-1]
    except IndexError:
        logging.warning(f'No end time found for the date `{dt_text}`, setting to None')
        return None
    else:
        return parse_polish_date(f'{date_str} {end_time_str}')


def get_place_name_address(soup: BeautifulSoup) -> tuple[str, str]:
    for elem in soup.find_all('h5'):
        if HEADER_PLACE in elem.text:
            if place_section_raw := elem.parent.find('p'):
                # For some reason each time the place value starts with
                # backtick, so we strip it
                place_section = place_section_raw.text.lstrip('`').strip()
                place_name_raw, _, place_address_raw = place_section.partition(',')
                return place_name_raw.strip(), place_address_raw.strip()
    raise ValueError(f'Place details not found in the provided HTML content: `{soup}`')


def get_description(soup: BeautifulSoup) -> str:
    for elem in soup.find_all('h4'):
        if HEADER_DESCRIPTION in elem.text:
            if raw := elem.parent.find('p'):
                return ' '.join(raw.decode_contents().strip().replace('\n', '').split())
    logging.warning(f'Description not found in the provided HTML content: `{soup}`')
    return ''


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
            return datetime.strptime(date_str, '%d %m %Y %H:%M').replace(
                tzinfo=ZoneInfo('Europe/Warsaw')
            )
    raise ValueError(f'Polish month name not found in the provided date string: {date_str}')


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


def add_event_requests(event: GancioEvent) -> dict[str, object]:
    """Add an event to Gancio using the requests library.

    TODO:
    - issue with tags, 500 server error, it worked with urllib
    - issue with online_locations, it creates a location per character (!)
    """
    url = 'http://127.0.0.1:13120/api/event'
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
