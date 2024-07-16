from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime
from datetime import time
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

from event_scrapper_srt import util
from event_scrapper_srt.event import Event
from event_scrapper_srt.event import Occurrence


class _Header:
    """HTML headers names in the scrapped webpage."""

    DATE_TIMES = 'Kiedy?'
    PLACE = 'Gdzie?'
    DESCRIPTION = 'Trochę szczegółów'


def get_events(
    urls: list[str], content_getter: Callable[[str], bytes] = util.get_url_content
) -> list[Event]:
    events = []
    for url in urls:
        html_content = content_getter(url).decode()
        events.append(_extract_event_details(html_content, url))
    logging.info(f'Extracted details for {len(events)} events')
    return events


def _extract_event_details(html_content: str, url: str) -> Event:
    soup = BeautifulSoup(html_content, 'html.parser')

    title = _get_title(soup)
    image_url = _get_image_url(soup)
    place_name, place_address = _get_place_name_address(soup)

    try:
        date_times = _get_date_times(soup)
    except ValueError:
        date_times = []
        logging.info(f'[{title}] No date and time information found')

    return Event(
        url=url,
        title=title,
        description=_get_description(soup),
        place_name=place_name,
        place_address=place_address,
        image_url=image_url,
        date_times=date_times,
    )


def _get_title(soup: BeautifulSoup) -> str:
    for elem in soup.find_all('h1'):
        return elem.text.strip()
    raise ValueError(f'Title not found in the provided HTML content: `{soup}`')


def _get_description(soup: BeautifulSoup) -> str:
    for elem in soup.find_all('h4'):
        if _Header.DESCRIPTION in elem.text and (raw := elem.parent.find('p')):
            return ' '.join(raw.decode_contents().strip().replace('\n', '').split())
    logging.warning(f'Description not found in the provided HTML content: `{soup}`')
    return ''


def _get_place_name_address(soup: BeautifulSoup) -> tuple[str, str]:
    for elem in soup.find_all('h5'):
        if _Header.PLACE in elem.text and (place_section_raw := elem.parent.find('p')):
            # For some reason each time the place value starts with
            # backtick, so we strip it
            place_section = place_section_raw.text.lstrip('`').strip()
            place_name_raw, _, place_address_raw = place_section.partition(',')
            return place_name_raw.strip(), place_address_raw.strip()
    raise ValueError(f'Place details not found in the provided HTML content: `{soup}`')


def _get_image_url(soup: BeautifulSoup) -> str | None:
    for elem in soup.find_all('header'):
        for div in elem.find_all('div'):
            return div['data-bg'].partition('(')[-1].partition(')')[0]
    logging.warning(f'Failed to extract image url from HTML content: `{soup}`')
    return None


def _get_date_times(soup: BeautifulSoup) -> list[Occurrence]:
    for elem in soup.find_all('h5'):
        if _Header.DATE_TIMES in elem.text:
            return _extract_date_times(elem.parent.find_all('p'))
    raise ValueError(f'Time details not found in the provided HTML content: `{soup}`')


def _extract_date_times(p_elems: list[BeautifulSoup]) -> list[Occurrence]:
    date_times = []
    for dt in p_elems:
        if dt.find('strong'):
            date_times.append(_extract_date_time(dt, tzinfo=ZoneInfo('Europe/Warsaw')))
    return date_times


def _extract_date_time(soup: BeautifulSoup, tzinfo: ZoneInfo) -> Occurrence:
    """Extracts date and start and end time from the provided string.

    The HTML looks like this:

        <p><strong>DD MONTH YYYY</strong> HH:MM</p>
        i.e.
        DD MONTH YYYY HH:MM

        <p><strong>DD MONTH YYYY</strong> HH:MM - HH:MM</p>
        i.e.
        DD MONTH YYYY HH:MM - HH:MM

    Note that end time is optional.

    E.g.

        <p><strong>8 listopada 2024</strong> 21:00</p>
        i.e.
        8 listopada 2024 21:00

        <p><strong>27 lipca 2024</strong> 12:00 - 15:00</p>
        i.e.
        27 lipca 2024 12:00 - 15:00
    """
    date_str = soup.find('strong').text.strip()
    date = _parse_polish_date(date_str)

    start_time = soup.text.partition('-')[0].split()[-1]
    start_dt = datetime.combine(date, _get_time(start_time), tzinfo=tzinfo)

    try:
        end_time = soup.text.partition('-')[-1].split()[-1]
    except IndexError:
        logging.warning(f'No end time found for the date `{soup}`, setting to None')
        end_dt = None
    else:
        end_dt = datetime.combine(date, _get_time(end_time), tzinfo=tzinfo)

    return Occurrence(start=start_dt, end=end_dt)


_MONTHS_PL = {
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


def _parse_polish_date(date_str: str) -> datetime:
    for pl_month, month_num in _MONTHS_PL.items():
        if pl_month in date_str:
            return datetime.strptime(date_str.replace(pl_month, f'{month_num:02}'), '%d %m %Y')
    raise ValueError(f'Polish month name not found in the provided date string: {date_str}')


def _get_time(time_str: str) -> time:
    hour, _, minute = time_str.partition(':')
    return time(int(hour), int(minute))
