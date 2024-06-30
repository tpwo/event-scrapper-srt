from __future__ import annotations

import datetime

from event_scrapper_srt import Event
from event_scrapper_srt import GancioEvent
from event_scrapper_srt import Occurrence

example_event = Event(
    url='https://example.com/',
    title='Lindy Hop dla początkujacych | intensywne warsztaty',
    description='Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='Łąkowa 35/38, Gdańsk',
    image_url='https://swingrevolution.pl/wp-content/uploads/2022/04/351150267_646835474155254_2037209978322475013_n.jpg',
    date_times=[
        Occurrence(
            start=datetime.datetime(2024, 7, 27, 12, 0), end=datetime.datetime(2024, 7, 27, 15, 0)
        )
    ],
)

example_event_gancio = GancioEvent(
    title='Lindy Hop dla początkujacych | intensywne warsztaty',
    description='Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='Łąkowa 35/38, Gdańsk',
    online_locations=['https://example.com/'],
    start_datetime=1722074400,
    multidate=0,
    tags='["swing"]',
    recurrent={'days': ['2024-07-27T12:00:00']},
    image=b'',
)

example_event_recurring = Event(
    url='https://example.com/',
    title='Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
    description='<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='ul. Łąkowa 35/38',
    image_url='https://swingrevolution.pl/wp-content/uploads/2024/06/448471294_881076660731133_508893191348552274_n.jpg',
    date_times=[
        Occurrence(
            start=datetime.datetime(2024, 7, 7, 20, 0), end=datetime.datetime(2024, 7, 7, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 7, 14, 20, 0), end=datetime.datetime(2024, 7, 14, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 7, 21, 20, 0), end=datetime.datetime(2024, 7, 21, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 7, 28, 20, 0), end=datetime.datetime(2024, 7, 28, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 8, 4, 20, 0), end=datetime.datetime(2024, 8, 4, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 8, 11, 20, 0), end=datetime.datetime(2024, 8, 11, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 8, 18, 20, 0), end=datetime.datetime(2024, 8, 18, 23, 0)
        ),
        Occurrence(
            start=datetime.datetime(2024, 8, 25, 20, 0), end=datetime.datetime(2024, 8, 25, 23, 0)
        ),
    ],
)


example_event_recurring_gancio = GancioEvent(
    title='Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
    description='<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='ul. Łąkowa 35/38',
    online_locations=['https://example.com/'],
    start_datetime=1720375200,
    multidate=0,
    tags='["swing"]',
    recurrent={
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
    image=b'',
)

example_event_past = Event(
    url='https://example.com/',
    title='Swingowa potańcówka nad Motławą',
    description='Genialny w swej prostocie, bez określonych reguł i sztywnej ramy, pełen szaleństwa i ekspresji, najradośniejszy ze wszystkich tańców na świecie – taki jest właśnie Lindy Hop! 😉 Jest on najpopularniejszym tańcem swingowym i przygode ze swingiem polecamy zacząć własnie od niego.',
    place_name='Oria Magic House',
    place_address='Stara Stocznia 4/1, Gdańsk',
    image_url='https://swingrevolution.pl/wp-content/uploads/2022/11/321906541_1231864150738514_2749587281127323943_n.jpg',
    date_times=[],
)
