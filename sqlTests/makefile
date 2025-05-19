# Makefile for managing Docker Compose services and DB import

COMPOSE_FILE=docker-compose.yml
DB_SERVICE=db
DB_USER=vscode
DB_PASSWORD=Keins123!
DB_NAME=BarbotDB
SQL_DUMP=backup.sql
SQL_TESTDATA=testdata.sql

# List all tables you expect after import (space-separated)
CHECK_TABLES=Cocktail Zapfstelle Zutat Rezept

# The Docker Compose network name (usually <foldername>_default)
DOCKER_NETWORK=sqltests_default

.PHONY: help up up-all up-db up-flask down import-db import-testdata logs --no-cache

help:
	@echo "Usage:"
	@echo "  make up              # Start all containers and import DB if needed"
	@echo "  make up --no-cache   # Build images from scratch, then start and import"
	@echo "  make up-all          # Start all containers (no import)"
	@echo "  make up-db           # Start only the db container"
	@echo "  make up-flask        # Start only the flask container (db must be up)"
	@echo "  make down            # Stop all containers"
	@echo "  make import-db       # Import SQL dump into MariaDB if not already imported"
	@echo "  make import-testdata # Import testdata into MariaDB if tables exist"
	@echo "  make logs            # Show logs for all containers"

up:
ifeq ($(findstring --no-cache,$(MAKECMDGOALS)),--no-cache)
	@echo "Building images with --no-cache..."
	docker compose -f $(COMPOSE_FILE) build --no-cache
	@$(MAKE) _up_main
else
	@$(MAKE) _up_main
endif

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

import-db:
	@echo "Checking if database import is needed..."
	@missing=0; \
	for table in $(CHECK_TABLES); do \
		if ! docker compose -f $(COMPOSE_FILE) exec -T $(DB_SERVICE) \
			mariadb -u$(DB_USER) -p$(DB_PASSWORD) -D$(DB_NAME) -e "SHOW TABLES LIKE '$$table';" | grep -q "$$table"; then \
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
			sh -c "mysql -h$(DB_SERVICE) -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < /sql/$(SQL_DUMP)"; \
		echo "Import complete."; \
	fi

import-testdata:
	@echo "Checking if testdata import is needed..."
	@missing=0; \
	for table in $(CHECK_TABLES); do \
		if ! docker compose -f $(COMPOSE_FILE) exec -T $(DB_SERVICE) \
			mariadb -u$(DB_USER) -p$(DB_PASSWORD) -D$(DB_NAME) -e "SHOW TABLES LIKE '$$table';" | grep -q "$$table"; then \
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
			sh -c "mysql -h$(DB_SERVICE) -u$(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < /sql/$(SQL_TESTDATA)"; \
		echo "Testdata import complete."; \
	else \
		echo "One or more tables are missing. Please create the schema first."; \
	fi

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

# This dummy target prevents make from treating --no-cache as a file/command
--no-cache:
	@:
