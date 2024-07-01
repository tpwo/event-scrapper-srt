venv:
	tox devenv

test:
	tox

coverage:
	tox run -e coverage

integration-tests:
	tox run -e integration-tests

GANCIO_DIR=./gancio
DOCKER_COMPOSE_FILE=$(GANCIO_DIR)/docker-compose.yml

start-dev-instance:
	docker compose --file $(DOCKER_COMPOSE_FILE) up --detach

stop-dev-instance:
	docker compose --file $(DOCKER_COMPOSE_FILE) stop

remove-dev-instance:
	docker compose --file $(DOCKER_COMPOSE_FILE) down
	sudo rm -rf $(GANCIO_DIR)/data

.PHONY: venv test coverage integration-tests start-dev-instance stop-dev-instance remove-dev-instance
