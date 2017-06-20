PROJECT_ROOT := .
SOURCE_DIR   := $(PROJECT_ROOT)/carbondoomsday
MANAGE_PY    := python manage.py
DOCKER_IMAGE := carbondoomsday/carbondoomsday

lint:
	pipenv run pylama $(SOURCE_DIR)
.PHONY: lint

isort:
	find $(SOURCE_DIR) -name "*.py" | xargs pipenv run isort -c --diff -sp=setup.cfg
.PHONY: isort

test:
	pipenv run pytest
.PHONY: test

docker_build:
	docker build -t $(DOCKER_IMAGE) .
.PHONY: docker_build

migrations:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py makemigrations carbondioxide
.PHONY: makemigrations

check_migrations:
	pipenv run python manage.py makemigrations --check
.PHONY: check_migrations

migrate:
	pipenv run python manage.py migrate
.PHONY: migrate

reset:
	pipenv run python manage.py reset_db
.PHONY: migrate

clean_migrations:
	rm -rf $(SOURCE_DIR)/carbondioxide/migrations/
.PHONY: clean_migrations

celery:
	pipenv run celery -A carbondoomsday worker -l info
.PHONY: celery

static:
	pipenv python manage.py collectstatic --noinput -v 3
.PHONY: static

server:
	pipenv run uwsgi --emperor uwsgi.ini
.PHONY: server

admin:
	pipenv run python manage.py createsuperuser
.PHONY: admin
