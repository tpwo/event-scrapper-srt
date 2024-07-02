from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    """Event details extracted from the website.

    Args:

        url: The URL of the event.
        title: Event name.
        description: HTML-compatible description of the event.
        place_name: The name of the place where the event takes place.
        place_address: The address of the place where the event takes place.
        image_url: The URL of the image associated with the event.
        date_times: A list of event occurrence times. A single element
                    list if event is not recurring.
    """

    url: str
    title: str
    description: str
    place_name: str
    place_address: str
    image_url: str | None
    date_times: list[Occurrence]


@dataclass(frozen=True)
class Occurrence:
    """Event occurence time details.

    Args:
        start: The start date and time of the event.
        end: The end date and time of the event. `None` if not available.
    """

    start: datetime
    end: datetime | None


@dataclass(frozen=True)
class GancioEvent:
    """API request used to create a new event in Gancio.

    Documentation:
    https://gancio.org/dev/api#add-a-new-event

    Args:

        title: Event name.
        description: HTML-compatible description of the event.
        place_name: The name of the place where the event takes place.
        place_address: The address of the place where the event takes place.
        online_locations: List of URL associated with the event.
        start_datetime: The start of the event as Unix timestamp.
        end_datetime: The end of the event as Unix timestamp. `None` if
                      not available.
        multidate: 0 or 1 represeting whether the event spans over multiple
                   days. *Currently* always set to 1.
        tags: List of tags associated with the event.
        image: The image associated with the event as bytes. `None` if not available.
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
