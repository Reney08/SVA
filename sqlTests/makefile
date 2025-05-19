# Makefile for managing Docker Compose services and DB import

COMPOSE_FILE = docker-compose.yml
DB_SERVICE   = db
DB_USER      = vscode
DB_PASSWORD ?= Keins123!
DB_NAME      = BarbotDB
SQL_DUMP    ?= backup.sql
SQL_TESTDATA?= testdata.sql

# List all tables you expect after import (space-separated)
CHECK_TABLES = Cocktail Zapfstelle Zutat Rezept

# The Docker Compose network name (adjust if needed)
DOCKER_NETWORK ?= sqltests_default

.PHONY: help up up-nocache up-all up-db up-flask down import-db import-testdata logs status _up_main

help:
	@echo "Usage:"
	@echo "  make up              # Start all containers and import DB if needed"
	@echo "  make up-nocache      # Build images from scratch, then start and import"
	@echo "  make up-all          # Start all containers (no import)"
	@echo "  make up-db           # Start only the db container"
	@echo "  make up-flask        # Start only the flask container (db must be up)"
	@echo "  make down            # Stop all containers"
	@echo "  make import-db       # Import SQL dump into MariaDB if not already imported"
	@echo "  make import-testdata # Import testdata into MariaDB if tables exist"
	@echo "  make logs            # Show logs for all containers"
	@echo "  make status          # Show container status"

up: up-all import-db import-testdata
	@echo "All services are up and database is initialized (if needed)."

up-nocache:
	@echo "Building images with --no-cache..."
	docker compose -f $(COMPOSE_FILE) build --no-cache
	@$(MAKE) _up_main

_up_main: up-all import-db import-testdata
	@echo "All services are up and database is initialized (if needed)."

up-all:
	docker compose -f $(COMPOSE_FILE) up -d

up-db:
	docker compose -f $(COMPOSE_FILE) up -d $(DB_SERVICE)

up-flask:
	docker compose -f $(COMPOSE_FILE) up -d flask

down:
	docker compose -f $(COMPOSE_FILE) down

# Wait for DB to be ready
wait-db:
	@echo "Waiting for database to be ready..."
	@retries=10; until docker compose -f $(COMPOSE_FILE) exec -T $(DB_SERVICE) \
		mariadb -u$(DB_USER) -p$(DB_PASSWORD) -e "SELECT 1;" >/dev/null 2>&1 || [ $$retries -eq 0 ]; do \
		echo "Waiting..."; \
		sleep 3; \
		retries=`expr $$retries - 1`; \
	done

import-db: wait-db
	@echo "Checking if database import is needed..."
	@missing=0; \
	for table in $(CHECK_TABLES); do \
		if ! docker compose -f $(COMPOSE_FILE) exec -T $(DB_SERVICE) \
			mariadb -u$(DB_USER) -p$(DB_PASSWORD) -D$(DB_NAME) -e "SHOW TABLES LIKE '$$table';" | grep -q "^$$table$$"; then \
			echo "Table '$$table' is missing."; \
			missing=1; \
		fi; \
	done; \
	if [ $$missing -eq 0 ]; then \
		echo "All tables exist. Skipping import."; \
	else \
		echo "One or more tables are missing. Importing SQL dump..."; \
		docker run --rm \
			--network $(DOCKER_NETWORK) \
			-v $(PWD):/sql \
			mariadb:latest \
			sh -c "set -e; mariadb -h$(DB_SERVICE) -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < /sql/$(SQL_DUMP)"; \
		echo "Import complete."; \
	fi

import-testdata: wait-db
	@echo "Checking if testdata import is needed..."
	@missing=0; \
	for table in $(CHECK_TABLES); do \
		if ! docker compose -f $(COMPOSE_FILE) exec -T $(DB_SERVICE) \
			mariadb -u$(DB_USER) -p$(DB_PASSWORD) -D$(DB_NAME) -e "SHOW TABLES LIKE '$$table';" | grep -q "^$$table$$"; then \
			echo "Table '$$table' is missing."; \
			missing=1; \
		fi; \
	done; \
	if [ $$missing -eq 0 ]; then \
		echo "All tables exist. Importing testdata..."; \
		docker run --rm \
			--network $(DOCKER_NETWORK) \
			-v $(PWD):/sql \
			mariadb:latest \
			sh -c "set -e; mariadb -h$(DB_SERVICE) -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < /sql/$(SQL_TESTDATA)"; \
		echo "Testdata import complete."; \
	else \
		echo "One or more tables are missing. Please create the schema first."; \
	fi

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

status:
	docker compose -f $(COMPOSE_FILE) ps
