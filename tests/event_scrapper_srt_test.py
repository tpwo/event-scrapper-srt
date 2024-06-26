from __future__ import annotations

import datetime
import pathlib

import pytest

import event_scrapper_srt
from event_scrapper_srt import Event


def test_get_events_from_sitemap():
    xml_content = pathlib.Path('testing/example-events-sitemap.xml').read_bytes()
    actual = event_scrapper_srt.get_events(xml_content=xml_content)
    expected = [
        Event(
            url='https://swingrevolution.pl/wydarzenia/swingowa-potancowka-nad-motlawa/',
            lastmod='2023-01-07T14:28:50+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/w-rytmie-swinga-potancowka/',
            lastmod='2023-01-30T16:59:29+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/practice-chill/',
            lastmod='2024-06-25T10:06:15+00:00',
        ),
        Event(
            url='https://swingrevolution.pl/wydarzenia/sunday-summer-night-coniedzielna-potancowka/',
            lastmod='2024-06-25T10:08:35+00:00',
        ),
    ]
    assert actual == expected


@pytest.mark.parametrize(
    ('file', 'expected'),
    (
        (
            'example-event.html',
            {
                'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
                'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, Łąkowa 35/38, Gdańsk',
                'image_url': 'https://swingrevolution.pl/wp-content/uploads/2022/04/351150267_646835474155254_2037209978322475013_n.jpg',
                'date_times': [datetime.datetime(2024, 7, 27, 15, 0)],
            },
        ),
        (
            'example-event-recurring.html',
            {
                'title': 'Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
                'description': '<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, ul. Łąkowa 35/38',
                'image_url': 'https://swingrevolution.pl/wp-content/uploads/2024/06/448471294_881076660731133_508893191348552274_n.jpg',
                'date_times': [
                    datetime.datetime(2024, 7, 7, 23, 0),
                    datetime.datetime(2024, 7, 14, 23, 0),
                    datetime.datetime(2024, 7, 21, 23, 0),
                    datetime.datetime(2024, 7, 28, 23, 0),
                    datetime.datetime(2024, 8, 4, 23, 0),
                    datetime.datetime(2024, 8, 11, 23, 0),
                    datetime.datetime(2024, 8, 18, 23, 0),
                    datetime.datetime(2024, 8, 25, 23, 0),
                ],
            },
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
            {
                'title': 'Swingowa potańcówka nad Motławą',
                'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
                'place_name': 'Za ile?',
                'place_address': '10zł',
                'image_url': 'https://swingrevolution.pl/wp-content/uploads/2022/11/321906541_1231864150738514_2749587281127323943_n.jpg',
                'date_times': [],
            },
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
            {
                'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
                'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, Łąkowa 35/38, Gdańsk',
                'image_url': 'https://swingrevolution.pl/wp-content/uploads/2022/04/351150267_646835474155254_2037209978322475013_n.jpg',
                'date_times': [datetime.datetime(2024, 7, 27, 15, 0)],
            },
            {
                'title': 'Lindy Hop dla początkujacych | intensywne warsztaty',
                'description': 'Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, Łąkowa 35/38, Gdańsk',
                'place_latitude': 0.0,
                'place_longitude': 0.0,
                'online_locations': '[]',
                'start_datetime': 1722085200,
                'multidate': 1,
                'tags': '[]',
                'image': b'',
            },
        ),
        (
            {
                'title': 'Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
                'description': '<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, ul. Łąkowa 35/38',
                'image_url': 'https://swingrevolution.pl/wp-content/uploads/2024/06/448471294_881076660731133_508893191348552274_n.jpg',
                'date_times': [
                    datetime.datetime(2024, 7, 7, 23, 0),
                    datetime.datetime(2024, 7, 14, 23, 0),
                    datetime.datetime(2024, 7, 21, 23, 0),
                    datetime.datetime(2024, 7, 28, 23, 0),
                    datetime.datetime(2024, 8, 4, 23, 0),
                    datetime.datetime(2024, 8, 11, 23, 0),
                    datetime.datetime(2024, 8, 18, 23, 0),
                    datetime.datetime(2024, 8, 25, 23, 0),
                ],
            },
            {
                'title': 'Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
                'description': '<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
                'place_name': 'Gdzie?',
                'place_address': '`\n                                        Studio Swing Revolution Trójmiasto, ul. Łąkowa 35/38',
                'place_latitude': 0.0,
                'place_longitude': 0.0,
                'online_locations': '[]',
                'start_datetime': 1724619600,
                'multidate': 1,
                'tags': '[]',
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
