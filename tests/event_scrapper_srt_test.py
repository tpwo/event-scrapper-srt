from __future__ import annotations

import pathlib

import freezegun
import pytest

import event_scrapper_srt
from event_scrapper_srt import SitemapElem
from testing import resources


@freezegun.freeze_time('2023-02-28')
def test_get_events_from_sitemap():
    xml_content = pathlib.Path('testing/example-events-sitemap.xml').read_bytes()
    actual = event_scrapper_srt.get_events_from_sitemap(xml_content=xml_content, max_age_days=30)
    expected = [
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/sunday-summer-night-coniedzielna-potancowka/',
            lastmod='2024-06-25T10:08:35+00:00',
        ),
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/practice-chill/',
            lastmod='2024-06-25T10:06:15+00:00',
        ),
        SitemapElem(
            url='https://swingrevolution.pl/wydarzenia/w-rytmie-swinga-potancowka/',
            lastmod='2023-01-30T16:59:29+00:00',
        ),
    ]
    assert actual == expected


@pytest.mark.parametrize(
    ('file', 'expected'),
    (
        (
            'example-event.html',
            resources.example_event,
        ),
        (
            'example-event-recurring.html',
            resources.example_event_recurring,
        ),
    ),
)
def test_extract_event_details(file, expected):
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = event_scrapper_srt.extract_event_details(html_content=html_content)
    assert actual == expected


@pytest.mark.parametrize(
    ('file', 'expected'),
    (
        (
            'example-event-past.html',
            resources.example_event_past,
        ),
    ),
)
def test_extract_past_event_details(file, expected, caplog):
    html_content = pathlib.Path(f'testing/{file}').read_text()
    actual = event_scrapper_srt.extract_event_details(html_content=html_content)
    assert actual == expected
    assert 'Failed to extract date and time from: ' in caplog.text
    assert "Error: `'NoneType' object has no attribute 'text'`" in caplog.text


@pytest.mark.parametrize(
    ('details', 'expected'),
    (
        (
            resources.example_event,
            {
                'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
                'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
                'place_name': 'Studio Swing Revolution Trójmiasto',
                'place_address': 'Łąkowa 35/38, Gdańsk',
                'start_datetime': 1722074400,
                'multidate': 0,
                'tags': '["swing"]',
                'recurrent': {'days': ['2024-07-27T12:00:00']},
                'image': b'',
            },
        ),
        (
            resources.example_event_recurring,
            {
                'title': 'Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
                'description': '<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
                'place_name': 'Studio Swing Revolution Trójmiasto',
                'place_address': 'ul. Łąkowa 35/38',
                'start_datetime': 1720375200,
                'multidate': 0,
                'tags': '["swing"]',
                'recurrent': {
                    'days': [
                        '2024-07-07T20:00:00',
                        '2024-07-14T20:00:00',
                        '2024-07-21T20:00:00',
                        '2024-07-28T20:00:00',
                        '2024-08-04T20:00:00',
                        '2024-08-11T20:00:00',
                        '2024-08-18T20:00:00',
                        '2024-08-25T20:00:00',
                    ]
                },
                'image': b'',
            },
        ),
    ),
)
def test_prepare_gancio_event(details, expected):
    actual = event_scrapper_srt.prepare_gancio_event(
        event_details=details, img_getter=get_image_mock
    )
    assert actual == expected


def get_image_mock(image_url: str) -> bytes:
    return b''
