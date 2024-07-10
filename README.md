# Event Scrapper SRT

Event Scrapper for <https://swingrevolution.pl/> which then can publish them to a [Gancio](https://gancio.org/) instance.

## How to run?

### Prerequsites

- Python 3.11
- `make`
- `docker` with `compose` to run dev instance of Gancio and integration tests

### Install tox

```bash
pip install tox
```

### Create venv

```bash
make venv
# or
tox devenv
```

This command:

- creates virtual environment in the project directory: `./venv`
- installs all dependencies required to run the app and tests

## CLI

Use `--help` to see available options.

```bash
python -m event_scrapper_srt --help
```

### Sample output with default arguments

```con
$ python -m event_scrapper_srt --output-path output.json
2024-07-10 21:44:20,521 - INFO - Found 69 events in the sitemap
2024-07-10 21:44:20,522 - INFO - Extracted 7 events from the sitemap
2024-07-10 21:44:20,739 - WARNING - No end time found for the date `<p><strong>12 lipca 2024</strong> 20:00<hr/></p>`, setting to None
2024-07-10 21:44:20,739 - WARNING - No end time found for the date `<p><strong>16 sierpnia 2024</strong> 20:00</p>`, setting to None
2024-07-10 21:44:20,945 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No date and time information found
2024-07-10 21:44:21,824 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No date and time information found
2024-07-10 21:44:22,055 - INFO - Extracted details for 7 events
2024-07-10 21:44:22,055 - INFO - [SWING NA PERONIE | potańcówka & live music] Prepared 2 events for Gancio
2024-07-10 21:44:22,055 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No Gancio events created: no future `date_times` found
2024-07-10 21:44:22,055 - INFO - [Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA] Prepared 7 events for Gancio
2024-07-10 21:44:22,055 - INFO - [Practice & CHILL] Prepared 3 events for Gancio
2024-07-10 21:44:22,055 - INFO - [Practice & CHILL | Wersja FAST FEET] Prepared 3 events for Gancio
2024-07-10 21:44:22,055 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No Gancio events created: no future `date_times` found
2024-07-10 21:44:22,055 - INFO - [Lindy Hop dla początkujacych | intensywne warsztaty] Prepared 1 events for Gancio
2024-07-10 21:44:22,058 - INFO - Saved 16 events to `/home/tpwo/ws/event-scrapper-srt/output.json`
```

## Development

### Run unit tests and static checks

```bash
make test
# or
tox run -e py311
```

### Run integration tests

`docker` with `compose` needs to be available.

```bash
make integration-tests
# or
tox run -e integration-tests
```

### Measure code coverage

```bash
make coverage
# or
tox run -e coverage
```

## Working with DEV instance of Gancio

`docker` with `compose` needs to be available.

### To start it

```bash
make start-dev-instance
```

### To stop it

```bash
make stop-dev-instance
```

### To remove it

Sudo is required to remove docker artifacts.

```bash
make remove-dev-instance
```
