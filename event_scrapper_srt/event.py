from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class Event:
    """Event details extracted from the website.

    Args:
    ----
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
    ----
        start: The start date and time of the event.
        end: The end date and time of the event. `None` if not available.

    """

    start: datetime
    end: datetime | None


@dataclass(frozen=True)
class GancioEvent:
    """Represents a single Gancio event.

    Structure is based on the API request used to create a new event in Gancio.

    Documentation:
    https://gancio.org/dev/api#add-a-new-event

    **PLEASE NOTE** that documentation provided above seems to be
    outdated, as it doesn't mention `image_url` field. However, when
    provided to Gancio, it automatically downloads the image and
    attaches it to the created event.

    Args:
    ----
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
        image_url: The URL of the image associated with the event.

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
    image_url: str | None
