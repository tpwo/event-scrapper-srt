from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone

from lxml import etree


@dataclass(frozen=True)
class SitemapElem:
    """An entry in the events sitemap.

    Args:

        url: The URL of the event.
        lastmod: The last modification date of the event in the format
                 `YYYY-MM-DDTHH:MM:SS+00:00`.

    https://swingrevolution.pl/events-sitemap.xml
    """

    url: str
    lastmod: str


def get_elements(xml_content: bytes, max_age_days: int = 30) -> list[SitemapElem]:
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

    logging.info(f'Found {len(elements)} events in the sitemap')
    events = []

    for elem in reversed(elements):
        assert isinstance(elem, etree._Element)
        url = _get_xpath_value(elem, 'ns:loc/text()', ns)
        lastmod = _get_xpath_value(elem, 'ns:lastmod/text()', ns)
        try:
            lastmod_dt = datetime.fromisoformat(lastmod)
        except ValueError as err:
            logging.warning(f'Failed to parse lastmod date `{lastmod}`. Error: `{err}`')
        else:
            if _event_older_than(lastmod_dt, max_age_days):
                logging.debug(f'Event `{url}` is older than {max_age_days} days, skipping')
            else:
                event = SitemapElem(url=url, lastmod=lastmod)
                events.append(event)

    logging.info(f'Extracted {len(events)} events from the sitemap')
    return events


def _get_xpath_value(elem: etree._Element, path: str, namespace: dict[str, str]) -> str:
    all = elem.xpath(path, namespaces=namespace)
    assert isinstance(all, Sequence)
    return str(all[0])


def _event_older_than(dt: datetime, max_age_days: int) -> bool:
    days = (dt - datetime.now(timezone.utc)).days * -1
    logging.debug(f'Event is {days} days old')
    return days > max_age_days
