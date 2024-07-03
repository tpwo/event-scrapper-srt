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
