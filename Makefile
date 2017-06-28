PROJECT_ROOT := .
SOURCE_DIR   := $(PROJECT_ROOT)/carbondoomsday
MANAGEPY     := python manage.py
PIPENVRUN    := pipenv run
DOCKER_IMAGE := carbondoomsday/measurements/

.DEFAULT_GOAL := help

GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

HELPME = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (20 - length $$_->[0]); \
	print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }

help:
	@perl -e '$(HELPME)' $(MAKEFILE_LIST)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DOCKER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
dockerbuild:  ##@docker Build the application docker image.
	@docker build -t $(DOCKER_IMAGE) .
.PHONY: dockerbuild

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PYTHON
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
lint: ##@python Check the Python source code for code quality issues.
	@$(PIPENVRUN) pylama $(SOURCE_DIR)
.PHONY: lint

sort:  ##@python Check that the Python source code imports are sorted correctly.
	@find $(SOURCE_DIR) -name "*.py" | xargs $(PIPENVRUN) isort -c --diff -sp=setup.cfg
.PHONY: sort

test:  ##@python Run the Python tests.
	@$(PIPENVRUN) pytest --cov=carbondoomsday
.PHONY: test

proof: lint sort test dbcheckmigrations  ##@python Pretend to be Travis CI and check the changes.
.PHONY: proof

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DJANGO
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
showurls:  ##@django List all available URLS served by Django.
	@$(PIPENVRUN) $(MANAGEPY) show_urls -f aligned | less
.PHONY: showurls

dbmigrations:  ##@django Create database migrations.
	@$(PIPENVRUN) $(MANAGEPY) makemigrations measurements
.PHONY: dbmigrations

dbcheckmigrations:  ##@django Check if you need to create a new migration.
	@$(PIPENVRUN) $(MANAGEPY) makemigrations --check
.PHONY: dbcheckmigrations

dbmigrate:  ##@django Run the database migrations.
	@$(PIPENVRUN) $(MANAGEPY) migrate
.PHONY: dbmigrate

dbreset:  ##@django Reset the database.
	@$(PIPENVRUN) $(MANAGEPY) reset_db
.PHONY: dbreset

celery:  ##@django Run the celery worker.
	@$(PIPENVRUN) celery -A carbondoomsday -l info worker -B -E
.PHONY: celery

shell:  ##@django Run a completion powered Django shell.
	@$(PIPENVRUN) $(MANAGEPY) shell_plus
.PHONY: shell

server:  ##@django Run the development mode server.
	@$(PIPENVRUN) $(MANAGEPY) runserver
.PHONY: server

dbadmin:  ##@django Create an admin user for the Django admin.
	@$(PIPENVRUN) $(MANAGEPY) createsuperuser
.PHONY: dbadmin

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DATA
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
scrapelatest:  ##@data Get the latest CO2 data.
	@$(PIPENVRUN) $(MANAGEPY) scrape_latest_co2
.PHONY: scrapelatest

scrapehistoric:  ##@data Get historical CO2 data.
	@$(PIPENVRUN) $(MANAGEPY) scrape_historic_co2
.PHONY: scrapehistoric

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HEROKU
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
prodbash:  ##@heroku Run a bash console on the production server.
	@heroku run bash -a carbondoomsday
.PHONY: prodbash

prodlogs:  ##@heroku Tail the logs for the production environment.
	@heroku logs -t -a carbondoomsday
.PHONY: prodlogs

testbash:  ##@heroku Run a bash console on the staging server.
	@heroku run bash -a carbondoomsday-test
.PHONY: testbash

testlogs:  ##@heroku Tail the logs for the staging environment.
	@heroku logs -t -a carbondoomsday-test
.PHONY: testlogs
