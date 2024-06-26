from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from datetime import datetime
from typing import NamedTuple

from bs4 import BeautifulSoup
from lxml import etree


class Event(NamedTuple):
    url: str
    lastmod: str


def main() -> None:
    sitemap_url = 'https://swingrevolution.pl/events-sitemap.xml'
    xml_content = get_xml_content(sitemap_url)
    events = get_events(xml_content)
    details = []
    gancio_events = []

    for event in reversed(events):
        try:
            with urllib.request.urlopen(event.url) as response:
                html_content = response.read().decode('utf-8')
                event_details = extract_event_details(html_content)
                details.append(event_details)
                gancio_events.append(prepare_gancio_event(event_details))
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} - {e.read().decode('utf-8')}")
        except urllib.error.URLError as e:
            print(f'URLError: {e.reason}')


def get_xml_content(sitemap_url: str) -> bytes:
    with urllib.request.urlopen(sitemap_url) as response:
        return response.read()


def get_events(xml_content: bytes) -> list[Event]:
    # Parse the XML content using lxml
    root = etree.fromstring(xml_content)

    # Extract the namespace from xsi:schemaLocation
    schema_location = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
    schema_parts = schema_location.split()
    namespace = schema_parts[0]  # Extract the namespace URL

    # Define the namespace dictionary for use in xpath
    ns = {'ns': namespace}

    # Find all <url> elements
    urls = root.xpath('//ns:url', namespaces=ns)

    # Extract event details from each <url>
    events = []
    for url in urls:
        loc = url.xpath('ns:loc/text()', namespaces=ns)[0]
        lastmod = url.xpath('ns:lastmod/text()', namespaces=ns)
        lastmod = lastmod[0] if lastmod else 'N/A'

        event = Event(url=loc, lastmod=lastmod)
        events.append(event)

    return events


def extract_event_details(html_content: str) -> dict[str, object]:
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract image URL
    image_div = soup.find('div', class_='page-header min-vh-80 lazy')
    image_url = image_div['data-bg'].replace('url(', '').replace(')', '') if image_div else None

    # Extract event title
    title = soup.find('h1').text.strip()

    # Extract place details
    place_section = soup.find_all('div', class_='col-md-6 mx-auto')[1]
    place_name = place_section.find('h5').text.strip()
    place_address = place_section.find('p').text.strip()

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
            date_times.append(start_datetime)

    return {
        'title': title,
        'description': get_description(soup),
        'place_name': place_name,
        'place_address': place_address,
        'image_url': image_url,
        'date_times': date_times,
    }


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


def prepare_gancio_event(event_details: dict[str, object]) -> dict[str, object]:
    date_times = event_details['date_times']
    assert isinstance(date_times, list)
    for event_date in date_times:
        data = {
            'title': event_details['title'],
            'description': event_details['description'],
            'place_name': event_details['place_name'],
            'place_address': event_details['place_address'],
            'place_latitude': 0.0,  # Replace with actual latitude
            'place_longitude': 0.0,  # Replace with actual longitude
            'online_locations': json.dumps([]),  # Empty list for online locations
            'start_datetime': int(event_date.timestamp()),
            'multidate': 1,  # Assuming these are multidate events
            'tags': json.dumps([]),  # Add relevant tags
        }

        if event_details['image_url']:
            image_url = event_details['image_url']
            assert isinstance(image_url, str)
            image_response = urllib.request.urlopen(image_url)
            image_data = image_response.read()
            data['image'] = image_data

    return data


if __name__ == '__main__':
    main()
