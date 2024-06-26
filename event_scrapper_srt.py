from __future__ import annotations

import urllib.request

from lxml import etree


def fetch_event_details(sitemap_url):
    # Fetch the XML content from the URL
    with urllib.request.urlopen(sitemap_url) as response:
        xml_content = response.read()

    # Parse the XML content using lxml
    root = etree.fromstring(xml_content)

    # Extract the namespace from xsi:schemaLocation
    schema_location = root.attrib[
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
    ]
    schema_parts = schema_location.split()
    namespace = schema_parts[0]  # Extract the namespace URL

    # Define the namespace dictionary for use in xpath
    ns = {"ns": namespace}

    # Find all <url> elements
    urls = root.xpath("//ns:url", namespaces=ns)

    # Extract event details from each <url>
    events = []
    for url in urls:
        loc = url.xpath("ns:loc/text()", namespaces=ns)[0]
        lastmod = url.xpath("ns:lastmod/text()", namespaces=ns)
        lastmod = lastmod[0] if lastmod else "N/A"

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
