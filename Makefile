tests:
	tox

coverage:
	tox run -e coverage

integration-tests:
	tox run -e integration-tests

start-dev-instance:
	docker compose --file ./gancio/docker-compose.yml up --detach

stop-dev-instance:
	docker compose --file ./gancio/docker-compose.yml stop

remove-dev-instance:
	docker compose --file ./gancio/docker-compose.yml down
	sudo rm -rf ./gancio/data

.PHONY: tests coverage integration-tests start-dev-instance stop-dev-instance remove-dev-instance
