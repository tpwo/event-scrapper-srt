# Event Scrapper SRT

Event Scrapper for <https://swingrevolution.pl/> which then can publish them to a [Gancio](https://gancio.org/) instance.

## Development

### Prerequsites

- Python 3.11
- `make`
- `docker` with `compose` to run dev instance of Gancio and integration tests

### Install tox

```
pip install tox
```

### Create venv

```
make venv
```

This command:

- creates virtual environment in the project directory: `./venv`
- installs all dependencies required to run the app and tests

### Run unit tests and static checks

```
make test
```

### Run integration tests

```
make integration-test
```

### Measure code coverage

```
make coverage
```

## Working with DEV instance of Gancio

### To start it

```
make start-dev-instance
```

### To stop it

```
make stop-dev-instance
```

### To remove it

Sudo is required to remove docker artifacts.

```
make remove-dev-instance
```
