# Event Scrapper SRT

Event Scrapper for <https://swingrevolution.pl/>.

**Update: SRT was closed at the beginning of 2025, so this repo is now archived.**

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

## How to use?

### CLI

Use `--help` to see available options.

```bash
python -m event_scrapper_srt --help
```

### Saving output into the file

All logged messages are directed to `stderr`, and scrapped events to `stdout`. With `>` you can direct `stdout` to a file.

```bash
python -m event_scrapper_srt > output.json
```

Alternatively, you can direct logs to another file by using `1>` and `2>`:

```bash
python -m event_scrapper_srt 1> output.json 2> log.txt
```

You might consider `2>>` to append to log file instead of overwriting it:

```bash
python -m event_scrapper_srt 1> output.json 2>> logs.txt
```

### Sample output

```con
$ python -m event_scrapper_srt > output.json
2024-07-10 22:26:44,296 - INFO - Found 69 events in the sitemap
2024-07-10 22:26:44,298 - INFO - Extracted 7 events from the sitemap
2024-07-10 22:26:44,509 - WARNING - No end time found for the date `<p><strong>12 lipca 2024</strong> 20:00<hr/></p>`, setting to None
2024-07-10 22:26:44,509 - WARNING - No end time found for the date `<p><strong>16 sierpnia 2024</strong> 20:00</p>`, setting to None
2024-07-10 22:26:44,730 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No date and time information found
2024-07-10 22:26:45,580 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No date and time information found
2024-07-10 22:26:45,817 - INFO - Extracted details for 7 events
2024-07-10 22:26:45,817 - INFO - [SWING NA PERONIE | potańcówka & live music] Prepared 2 events for Gancio
2024-07-10 22:26:45,817 - INFO - [Summertime Jump Party | Impreza na zakończenie sezonu] No Gancio events created: no future `date_times` found
2024-07-10 22:26:45,817 - INFO - [Sunday Summer Night | CONIEDZIELNA POTAŃCÓWKA] Prepared 7 events for Gancio
2024-07-10 22:26:45,817 - INFO - [Practice & CHILL] Prepared 3 events for Gancio
2024-07-10 22:26:45,817 - INFO - [Practice & CHILL | Wersja FAST FEET] Prepared 3 events for Gancio
2024-07-10 22:26:45,817 - INFO - [Trening Performance & Show | SPOTKANIE INFORMACYJNE] No Gancio events created: no future `date_times` found
2024-07-10 22:26:45,817 - INFO - [Lindy Hop dla początkujacych | intensywne warsztaty] Prepared 1 events for Gancio
2024-07-10 22:26:45,817 - INFO - In total prepared 16 events for Gancio
2024-07-10 22:26:45,817 - INFO - Dumping output to stdout...
```

### Generated structure

Scrapped events directed to `stdout` are in [Newline Delimited JSON](https://github.com/ndjson/ndjson-spec) format. Each line has the following structure:

```json
{"title": "Lindy Hop dla początkujacych | intensywne warsztaty", "description": "<p>Daj się zarazić swingowym bakcylem...<snipped>", "place_name": "Studio Swing Revolution Trójmiasto", "place_address": "Łąkowa 35/38, Gdańsk", "online_locations": ["https://swingrevolution.pl/warsztaty-lindy-hop-od-podstaw/"], "start_datetime": 1722074400, "end_datetime": 1722085200, "multidate": 1, "tags": ["swing"], "image_url": "https://swingrevolution.pl/wp-content/uploads/2022/04/351150267_646835474155254_2037209978322475013_n.jpg"}
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
