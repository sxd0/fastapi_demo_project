DC = docker-compose
POSTGRES_USER = postgres
DB_NAME = booking
SERVICE_NAME = db

.PHONY: up down uvi db bash logs migrate upgrade downgrade

up:
	colima start
	$(DC) up -d


down:
	$(DC) down
	colima stop


uvi:
	poetry run uvicorn src.main:app --reload


db:
	$(DC) exec -it $(SERVICE_NAME) psql -U $(POSTGRES_USER) -d $(DB_NAME)


bash:
	$(DC) exec -it $(SERVICE_NAME) bash


logs:
	$(DC) logs -f


migrate: ### EXAMPLE: make migrate m="..."
	PYTHONPATH=. poetry run alembic revision --autogenerate -m "$(m)"


upgrade:
	PYTHONPATH=. poetry run alembic upgrade head


downgrade:
	PYTHONPATH=. poetry run alembic downgrade -1

pretty:
	ruff check --fix
	ruff format
