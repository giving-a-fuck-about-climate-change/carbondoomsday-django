PROJECT_ROOT := .
SOURCE_DIR   := $(PROJECT_ROOT)/carbondoomsday
MANAGEPY     := python manage.py
PIPENVRUN    := pipenv run
DOCKER_IMAGE := carbondoomsday/carbondoomsday

lint:
	$(PIPENVRUN) pylama $(SOURCE_DIR)
.PHONY: lint

isort:
	find $(SOURCE_DIR) -name "*.py" | xargs $(PIPENVRUN) isort -c --diff -sp=setup.cfg
.PHONY: isort

test:
	$(PIPENVRUN) pytest --cov=carbondoomsday
.PHONY: test

docker_build:
	docker build -t $(DOCKER_IMAGE) .
.PHONY: docker_build

migrations:
	$(PIPENVRUN) $(MANAGEPY) makemigrations
	$(PIPENVRUN) $(MANAGEPY) makemigrations carbondioxide
.PHONY: makemigrations

check_migrations:
	$(PIPENVRUN) $(MANAGEPY) makemigrations --check
.PHONY: check_migrations

migrate:
	$(PIPENVRUN) $(MANAGEPY) migrate
.PHONY: migrate

reset:
	$(PIPENVRUN) $(MANAGEPY) reset_db
.PHONY: migrate

clean_migrations:
	rm -rf $(SOURCE_DIR)/carbondioxide/migrations/
.PHONY: clean_migrations

celery:
	$(PIPENVRUN) celery worker -A carbondoomsday -l info
.PHONY: celery

static:
	$(PIPENVRUN) $(MANAGEPY) collectstatic --noinput -v 3
.PHONY: static

server:
	$(PIPENVRUN) uwsgi --emperor uwsgi.ini
.PHONY: server

devserver:
	$(PIPENVRUN) $(MANAGEPY) runserver
.PHONY: devserver

admin:
	$(PIPENVRUN) $(MANAGEPY) createsuperuser
.PHONY: admin

scrape_latest:
	$(PIPENVRUN) $(MANAGEPY) scrape_latest
.PHONY: scrape_latest

scrape_historic:
	$(PIPENVRUN) $(MANAGEPY) scrape_historic
.PHONY: scrape_historic

compose:
	cd dockercompose && $(PIPENVRUN) docker-compose up
.PHONY: compose

proof: lint isort test check_migrations
.PHONY: proof
