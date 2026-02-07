DC = docker-compose
POSTGRES_USER = postgres
DB_NAME = booking
SERVICE_NAME = db

.PHONY: up down db bash logs migrate upgrade downgrade

up:
	colima start
	$(DC) up -d


down:
	$(DC) down
	colima stop


db:
	$(DC) exec -it $(SERVICE_NAME) psql -U $(POSTGRES_USER) -d $(DB_NAME)


bash:
	$(DC) exec -it $(SERVICE_NAME) bash


logs:
	$(DC) logs -f


migrate: ### EXAMPLE: make migrate m="..."
	PYTHONPATH=. alembic revision --autogenerate -m "$(m)"


upgrade:
	PYTHONPATH=. alembic upgrade head


downgrade:
	PYTHONPATH=. alembic downgrade -1
