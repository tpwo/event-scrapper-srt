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
$ python -m event_scrapper_srt
2024-07-03 16:51:04,263 - INFO - Found 69 events in the sitemap
2024-07-03 16:51:04,270 - INFO - Extracted 7 events from the sitemap
2024-07-03 16:51:04,512 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No date and time information found
2024-07-03 16:51:05,473 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No date and time information found
2024-07-03 16:51:05,973 - WARNING - No end time found for the date `<p><strong>19 lipca 2024</strong> 20:00<hr/></p>`, setting to None
2024-07-03 16:51:05,974 - WARNING - No end time found for the date `<p><strong>16 sierpnia 2024</strong> 20:00</p>`, setting to None
2024-07-03 16:51:05,976 - INFO - Extracted details for 7 events
2024-07-03 16:51:05,980 - INFO - Saved event details to `output/events_2024-07-03T16:51:05.977033.json`
2024-07-03 16:51:06,303 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No Gancio events created: no future `date_times` found
2024-07-03 16:51:06,585 - INFO - [Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA] Prepared 8 events for Gancio
2024-07-03 16:51:06,861 - INFO - [Practice & CHILL] Prepared 4 events for Gancio
2024-07-03 16:51:07,139 - INFO - [Practice & CHILL | Wersja FAST FEET] Prepared 4 events for Gancio
2024-07-03 16:51:07,423 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No Gancio events created: no future `date_times` found
2024-07-03 16:51:07,738 - INFO - [Lindy Hop dla początkujacych | intensywne warsztaty] Prepared 1 events for Gancio
2024-07-03 16:51:08,087 - INFO - [SWING NA PERONIE | potańcówka & live music] Prepared 2 events for Gancio
2024-07-03 16:51:08,088 - INFO - Prepared 19 Gancio events for publishing
Continue with publishing events to `http://127.0.0.1:13120` (y/N)?
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
