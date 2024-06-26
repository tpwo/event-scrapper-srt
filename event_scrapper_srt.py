from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET


def fetch_event_details(sitemap_url):
    # Fetch the XML content from the URL
    with urllib.request.urlopen(sitemap_url) as response:
        xml_content = response.read()

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Namespace required for parsing specific XML tags
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Find all <url> elements
    urls = root.findall("ns:url", namespace)

    # Extract event details from each <url>
    events = []
    for url in urls:
        loc = url.find("ns:loc", namespace).text
        lastmod = (
            url.find("ns:lastmod", namespace).text
            if url.find("ns:lastmod", namespace) is not None
            else "N/A"
        )

        event = {"loc": loc, "lastmod": lastmod}
        events.append(event)

    return events


def main():
    sitemap_url = "https://swingrevolution.pl/events-sitemap.xml"
    events = fetch_event_details(sitemap_url)

    # Print out event details
    for event in events:
        print(f"Event URL: {event['loc']}")
        print(f"Last Modified: {event['lastmod']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
