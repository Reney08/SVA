# Makefile for managing Docker Compose services and DB import

COMPOSE_FILE=docker-compose.yml
DB_SERVICE=db
DB_USER=vscode
DB_PASSWORD=Keins123!
DB_NAME=BarbotDB
SQL_DUMP=backup.sql

# List all tables you expect after import (space-separated)
CHECK_TABLES=Cocktail Zapfstelle Zutat Rezept

# The Docker Compose network name (usually <foldername>_default)
DOCKER_NETWORK=sqltests_default

.PHONY: help up up-db up-flask down import-db logs

help:
	@echo "Usage:"
	@echo "  make up         # Start all containers and import DB if needed"
	@echo "  make up-db      # Start only the db container"
	@echo "  make up-flask   # Start only the flask container (db must be up)"
	@echo "  make down       # Stop all containers"
	@echo "  make import-db  # Import SQL dump into MariaDB if not already imported"
	@echo "  make logs       # Show logs for all containers"

up: up-all import-db
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

logs:
	docker compose -f $(COMPOSE_FILE) logs -f
