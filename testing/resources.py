from __future__ import annotations

import datetime
import zoneinfo

from event_scrapper_srt import Event
from event_scrapper_srt import GancioEvent
from event_scrapper_srt import Occurrence

example_event = Event(
    url='https://example.com/',
    title='Lindy Hop dla początkujacych | intensywne warsztaty',
    description='<p>Daj się zarazić swingowym bakcylem podczas intensywnych warsztatów od podstaw! Nie musisz nic umieć (większość z nas tak właśnie zaczynała), a jeśli plączą Ci się nogi – wspólnie je rozplączemy. 🙂 Udowodnimy Ci, że taniec może być prosty i przyjemny, a to wszystko w doborowym towarzystwie pozytywnie zakręconych ludzi i przy dźwiękach porywającego do tańca swinga.</p><p>🔸 ZAPISY 🔸<br/> · Zajęcia odbędą się w sobotę 27 lipca (3h, od 12:00-15:00).<br/> · Na zajęciach zmieniamy się w parach.<br/> · Nie potrzebujesz pary do wzięcia udziału w zajęciach. Przy zapisach dbamy o odpowiednie proporcje w grupie.<br/> · Każda osoba musi wypełnić osobny formularz (nawet gdy zapisujesz się w parze).<br/> ❗ Ilość miejsc na zajęciach jest ograniczona.</p>',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='Łąkowa 35/38, Gdańsk',
    image_url='https://swingrevolution.pl/wp-content/uploads/2022/04/351150267_646835474155254_2037209978322475013_n.jpg',
    date_times=[
        Occurrence(
            start=datetime.datetime(
                2024, 7, 27, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')
            ),
            end=datetime.datetime(
                2024, 7, 27, 15, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')
            ),
        )
    ],
)

example_event_gancio = [
    GancioEvent(
        title='Lindy Hop dla początkujacych | intensywne warsztaty',
        description='<p>Daj się zarazić swingowym bakcylem podczas intensywnych warsztatów od podstaw! Nie musisz nic umieć (większość z nas tak właśnie zaczynała), a jeśli plączą Ci się nogi – wspólnie je rozplączemy. 🙂 Udowodnimy Ci, że taniec może być prosty i przyjemny, a to wszystko w doborowym towarzystwie pozytywnie zakręconych ludzi i przy dźwiękach porywającego do tańca swinga.</p><p>🔸 ZAPISY 🔸<br/> · Zajęcia odbędą się w sobotę 27 lipca (3h, od 12:00-15:00).<br/> · Na zajęciach zmieniamy się w parach.<br/> · Nie potrzebujesz pary do wzięcia udziału w zajęciach. Przy zapisach dbamy o odpowiednie proporcje w grupie.<br/> · Każda osoba musi wypełnić osobny formularz (nawet gdy zapisujesz się w parze).<br/> ❗ Ilość miejsc na zajęciach jest ograniczona.</p>',
        place_name='Studio Swing Revolution Trójmiasto',
        place_address='Łąkowa 35/38, Gdańsk',
        online_locations=['https://example.com/'],
        start_datetime=1722074400,
        end_datetime=1722085200,
        multidate=1,
        tags=['swing'],
        image=b'',
    )
]

example_event_recurring = Event(
    url='https://example.com/',
    title='Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
    description='<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
    place_name='Studio Swing Revolution Trójmiasto',
    place_address='ul. Łąkowa 35/38',
    image_url='https://swingrevolution.pl/wp-content/uploads/2024/06/448471294_881076660731133_508893191348552274_n.jpg',
    date_times=[
        Occurrence(
            start=datetime.datetime(
                2024, 7, 7, 20, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')
            ),
            end=datetime.datetime(2024, 7, 7, 23, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')),
        ),
        Occurrence(
            start=datetime.datetime(
                2024, 7, 14, 20, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')
            ),
            end=datetime.datetime(
                2024, 7, 14, 23, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')
            ),
        ),
    ],
)


example_event_recurring_gancio = [
    GancioEvent(
        title='Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
        description='<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
        place_name='Studio Swing Revolution Trójmiasto',
        place_address='ul. Łąkowa 35/38',
        online_locations=['https://example.com/'],
        start_datetime=1720375200,
        end_datetime=1720386000,
        multidate=1,
        tags=['swing'],
        image=b'',
    ),
    GancioEvent(
        title='Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA',
        description='<p>Wyobraźcie sobie letni, niedzielny wieczór… 🌅 Dzień powoli się kończy, ale jednak czegoś brakuje do pełnego spełnienia. Zaczynasz szukać potańcówki tu i tam, i nic nie ma! Kto w niedzielę robi potańcówki? Kto robi imprezy regularnie, tak by nie musieć się zastanawiać i ich szukać? 🤔</p><p>Otóż… MY! 😃 Kochani, zapraszamy Was na Sunday Summer Night! Co niedzielę przez lipiec i sierpień otwieramy nasze studio o 20:00, organizujemy DJ’kę i bawimy się do 23:00. 🎶 </p><p>Bez socialu nie ma tańca, więc zapraszamy wszystkich Lindy Hopersów, tancerzy Solo Jazz, Boogie i Balboa Maniaków na parkiet! 💃🕺 Chcemy stworzyć kolejną okazję do tańczenia i integracji naszej trójmiejskiej społeczności.</p><p>Jeśli jesteś nowy/nowa, przyjdź i poproś kogoś o pokazanie podstawowych kroków. 👟 Tylko ci, którzy spróbowali dołączyć do nas, wiedzą, jak łatwa i przyjemna to sprawa, a nasza społeczność słynie ze swojej otwartości i przyjazności. 🌟</p><p>Do zobaczenia na parkiecie!</p><p>– Coniedziele 7 lipca – 25 sierpnia, Studio SRT, 20:00-23:00</p>',
        place_name='Studio Swing Revolution Trójmiasto',
        place_address='ul. Łąkowa 35/38',
        online_locations=['https://example.com/'],
        start_datetime=1720980000,
        end_datetime=1720990800,
        multidate=1,
        tags=['swing'],
        image=b'',
    ),
]


example_event_past = Event(
    url='https://example.com/',
    title='Swingowa potańcówka nad Motławą',
    description='<p>Zapraszamy serdecznie na kolejną z serii potańcówek swingowych nad Motławą.</p><p>Jest to wspólna inicjatywa 3 szkół tańców swingowych z Trójmiasta (Harlem Beats, Swing Revolution Trójmiasto, Shag College) we współpracy z ORIA MAGIC HOUSE w sercu Gdańska nad samą Motławą, której celem jest zintegrowanie środowiska tancerzy swingowych w Trójmieście. Chcemy również podczas krótkich lekcji pokazowych prezentować tańce swingowe szerszej publiczności, dlatego wpadnij na imprezkę w klimacie swingowym i zabierz ze sobą znajomych</p><p>ORIA MAGIC HOUSE nad Motławą to piękne miejsce, które jest zarówno restauracją, jak i teatrem i galerią sztuki, organizatorem wielu koncertów i imprez kulturalnych. Można tu coś dobrego zjeść i napić się zimowej herbaty</p>',
    place_name='Oria Magic House',
    place_address='Stara Stocznia 4/1, Gdańsk',
    image_url='https://swingrevolution.pl/wp-content/uploads/2022/11/321906541_1231864150738514_2749587281127323943_n.jpg',
    date_times=[],
)
