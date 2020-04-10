
COMPOSE ?= docker-compose -f docker-compose.yml

run: build
run:
	$(COMPOSE) up -d

rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

build:
	$(COMPOSE) build