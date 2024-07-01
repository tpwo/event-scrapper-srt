start-dev-instance:
	docker compose --file ./gancio/docker-compose.yml up --detach

stop-dev-instance:
	docker compose --file ./gancio/docker-compose.yml stop

remove-dev-instance:
	docker compose --file ./gancio/docker-compose.yml down
	sudo rm -rf ./gancio/data

.PHONY: start-dev-instance stop-dev-instace remove-dev-instance
