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


class SitemapElem(NamedTuple):
    url: str
    lastmod: str


class Event(NamedTuple):
    title: str
    description: str
    place_name: str
    place_address: str
    image_url: str | None
    date_times: list[str]


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    sitemap_url = 'https://swingrevolution.pl/events-sitemap.xml'
    xml_content = get_xml_content(sitemap_url)
    future_events: list[Event] = []

    for event in get_events(xml_content):
        for date_time in event.date_times:
            if datetime.fromisoformat(date_time) > datetime.now():
                future_events.append(event)
                break
    logging.info(f'{len(future_events)} of them are future events')

    os.makedirs('output', exist_ok=True)
    with open(f'output/details_{datetime.now().isoformat()}.json', 'w', encoding='utf-8') as file:
        json.dump(future_events, file, indent=4, ensure_ascii=False)
    logging.info('Saved event details to `output/details.json`')


def get_xml_content(sitemap_url: str) -> bytes:
    with urllib.request.urlopen(sitemap_url) as response:
        return response.read()


def get_events(xml_content: bytes) -> list[Event]:
    events = []
    for event in get_events_from_sitemap(xml_content):
        with urllib.request.urlopen(event.url) as response:
            html_content = response.read().decode('utf-8')
            events.append(extract_event_details(html_content))
    logging.info(f'Extracted details for {len(events)} events')
    return events


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


def event_older_than_max_age_days(dt: datetime, max_age_days: int) -> bool:
    days = (dt - datetime.now(timezone.utc)).days * -1
    logging.debug(f'Event is {days} days old')
    return days > max_age_days


def extract_event_details(html_content: str) -> Event:
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract image URL
    image_div = soup.find('div', class_='page-header min-vh-80 lazy')
    image_url = image_div['data-bg'].replace('url(', '').replace(')', '') if image_div else None

    # Extract event title
    title = soup.find('h1').text.strip()

    # Extract place details
    details_class = 'col-md-6 mx-auto'
    details = soup.find_all('div', class_=details_class)
    for detail in details:
        if 'Gdzie?' in detail.text:
            place_section_raw = detail.find('p').text
            # For some reason each time the place value starts with
            # backtick, so we strip it
            place_section = place_section_raw.lstrip('`').strip()
            place_name_raw, _, place_address_raw = place_section.partition(',')
            place_name = place_name_raw.strip()
            place_address = place_address_raw.strip()
            break

    # Extract event dates and times
    date_times = []
    date_time_section = (
        soup.find('div', class_='col-md-6 mx-auto')
        .find('div', class_='p-3 text-center')
        .find_all('p')
    )
    for dt in date_time_section:
        try:
            date_str, time_str = dt.find('strong').text.strip(), dt.text.split()[-1]
        except AttributeError as err:
            logging.warning(f'Failed to extract date and time from: `{dt}`. Error: `{err}`')
        else:
            dt_str = f'{date_str} {time_str}'
            start_datetime = parse_polish_date(dt_str)
            date_times.append(start_datetime.isoformat())

    return Event(
        title=title,
        description=get_description(soup),
        place_name=place_name,
        place_address=place_address,
        image_url=image_url,
        date_times=date_times,
    )


def get_place_name_address(soup: BeautifulSoup) -> tuple[str, str]:
    details_class = 'col-md-6 mx-auto'
    details = soup.find_all('div', class_=details_class)
    place_header = 'Gdzie?'
    for detail in details:
        if place_header in detail.text:
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


def prepare_gancio_event(
    event_details: Event, img_getter: Callable[[str], bytes]
) -> dict[str, object]:
    date_times = event_details.date_times
    # Structure based on Gancio API
    # https://gancio.org/dev/api#add-a-new-event
    data = {
        'title': event_details.title,
        'description': event_details.description,
        'place_name': event_details.place_name,
        'place_address': event_details.place_address,
        'start_datetime': int(datetime.fromisoformat(date_times[0]).timestamp()),
        # Assuming these are not multidate events
        'multidate': 0,
        'tags': json.dumps(['swing']),
        'recurrent': {'days': date_times},
    }
    if event_details.image_url:
        assert isinstance(event_details.image_url, str)
        data['image'] = img_getter(event_details.image_url)

    return data


def get_image(image_url: str) -> bytes:
    image_response = urllib.request.urlopen(image_url)
    return image_response.read()


if __name__ == '__main__':
    main()
