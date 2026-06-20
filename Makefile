SHELL := /bin/bash

COMPOSE ?= docker compose
PROJECT ?= fastapi-docker-traefik
VERIFY_PROJECT ?= fastapi-deps-verify
APP_HOST ?= fastapi.localhost
APP_URL ?= http://127.0.0.1:8008
TRAEFIK_URL ?= http://127.0.0.1:8081
WAIT_SECONDS ?= 60
TAIL ?= 120
SERVICE ?=
DB_USER ?= fastapi
DB_NAME ?= fastapi

.DEFAULT_GOAL := help

.PHONY: help check-docker config pull build rebuild up dev wait urls smoke verify verify-clean ps logs logs-web logs-db logs-traefik shell python db-shell db-tables pip-check restart stop down down-v clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-docker: ## Fail fast when Docker daemon is unavailable
	@docker info >/dev/null 2>&1 || { echo "Docker daemon is not available. Start Docker and retry."; exit 1; }

config: check-docker ## Validate and render the Docker Compose config
	$(COMPOSE) -p $(PROJECT) config

pull: check-docker ## Pull external service images
	$(COMPOSE) -p $(PROJECT) pull db traefik

build: check-docker ## Build the FastAPI image
	$(COMPOSE) -p $(PROJECT) build web

rebuild: check-docker ## Rebuild the FastAPI image without cache
	$(COMPOSE) -p $(PROJECT) build --no-cache web

up: check-docker ## Start the stack without rebuilding
	$(COMPOSE) -p $(PROJECT) up -d

dev: check-docker ## Build, start, wait for the app, and print URLs
	$(COMPOSE) -p $(PROJECT) up --build -d
	$(MAKE) --no-print-directory PROJECT=$(PROJECT) wait
	$(MAKE) --no-print-directory urls

wait: check-docker ## Wait until Traefik routes to the FastAPI app
	@echo "Waiting for $(APP_HOST) via $(APP_URL) ..."
	@for i in $$(seq 1 $(WAIT_SECONDS)); do \
		if curl -fsS -H 'Host: $(APP_HOST)' '$(APP_URL)/' >/dev/null 2>&1; then \
			echo "App is ready."; \
			exit 0; \
		fi; \
		sleep 1; \
	done; \
	echo "Timed out waiting for app after $(WAIT_SECONDS)s."; \
	$(COMPOSE) -p $(PROJECT) ps; \
	$(COMPOSE) -p $(PROJECT) logs --tail=$(TAIL) web db traefik; \
	exit 1

urls: ## Print local development URLs
	@echo "App:     http://$(APP_HOST):8008/"
	@echo "OpenAPI: http://$(APP_HOST):8008/openapi.json"
	@echo "Traefik: $(TRAEFIK_URL)/dashboard/"

smoke: wait ## Run HTTP smoke checks through Traefik
	@curl -fsS -H 'Host: $(APP_HOST)' '$(APP_URL)/'; echo
	@curl -fsS -H 'Host: $(APP_HOST)' '$(APP_URL)/openapi.json' >/dev/null
	@echo "HTTP smoke checks passed."

verify: dev smoke pip-check db-tables ## Verify the current dev stack

verify-clean: check-docker ## Verify using a temporary project and remove it afterward
	@set -e; \
	trap '$(MAKE) --no-print-directory PROJECT=$(VERIFY_PROJECT) down-v' EXIT; \
	$(MAKE) --no-print-directory PROJECT=$(VERIFY_PROJECT) dev; \
	$(MAKE) --no-print-directory PROJECT=$(VERIFY_PROJECT) smoke; \
	$(MAKE) --no-print-directory PROJECT=$(VERIFY_PROJECT) pip-check; \
	$(MAKE) --no-print-directory PROJECT=$(VERIFY_PROJECT) db-tables

ps: check-docker ## Show stack containers
	$(COMPOSE) -p $(PROJECT) ps

logs: check-docker ## Follow logs, optionally SERVICE=web|db|traefik
	$(COMPOSE) -p $(PROJECT) logs -f --tail=$(TAIL) $(SERVICE)

logs-web: check-docker ## Follow FastAPI logs
	$(COMPOSE) -p $(PROJECT) logs -f --tail=$(TAIL) web

logs-db: check-docker ## Follow Postgres logs
	$(COMPOSE) -p $(PROJECT) logs -f --tail=$(TAIL) db

logs-traefik: check-docker ## Follow Traefik logs
	$(COMPOSE) -p $(PROJECT) logs -f --tail=$(TAIL) traefik

shell: check-docker ## Open a shell in the FastAPI container
	$(COMPOSE) -p $(PROJECT) exec web bash

python: check-docker ## Open Python in the FastAPI container
	$(COMPOSE) -p $(PROJECT) exec web python

db-shell: check-docker ## Open psql in the Postgres container
	$(COMPOSE) -p $(PROJECT) exec db psql -U $(DB_USER) -d $(DB_NAME)

db-tables: check-docker ## List tables in the application database
	$(COMPOSE) -p $(PROJECT) exec -T db psql -U $(DB_USER) -d $(DB_NAME) -c '\dt'

pip-check: check-docker ## Check installed Python dependencies inside the app container
	$(COMPOSE) -p $(PROJECT) exec -T web python -m pip check

restart: check-docker ## Restart the stack
	$(COMPOSE) -p $(PROJECT) restart

stop: check-docker ## Stop containers without removing them
	$(COMPOSE) -p $(PROJECT) stop

down: check-docker ## Stop and remove containers, keeping volumes
	$(COMPOSE) -p $(PROJECT) down --remove-orphans

down-v: check-docker ## Stop and remove containers plus volumes
	$(COMPOSE) -p $(PROJECT) down -v --remove-orphans

clean: down-v ## Alias for a full local reset
