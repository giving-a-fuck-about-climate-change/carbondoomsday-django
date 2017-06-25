PROJECT_ROOT := .
SOURCE_DIR   := $(PROJECT_ROOT)/carbondoomsday
MANAGEPY     := python manage.py
PIPENVRUN    := pipenv run
DOCKER_IMAGE := carbondoomsday/carbondoomsday

.DEFAULT_GOAL := help

GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (20 - length $$_->[0]); \
	print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }

help:  ##@helpful Show the list of all commands available.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PYTHON
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
pylint: ##@python Check the Python source code for code quality issues.
	@$(PIPENVRUN) pylama $(SOURCE_DIR)
.PHONY: pylint

pysort:  ##@python Check that the Python source code imports are sorted correctly.
	@find $(SOURCE_DIR) -name "*.py" | xargs $(PIPENVRUN) isort -c --diff -sp=setup.cfg
.PHONY: pysort

pytest:  ##@python Run the Python tests.
	@$(PIPENVRUN) pytest --cov=carbondoomsday
.PHONY: pytest

pyproof: lint isort test check_migrations  ##@python Pretend to be Travis CI and check the changes.
.PHONY: pyproof

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DJANGO
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
dockerbuild:  ##@docker Build the application docker image.
	@docker build -t $(DOCKER_IMAGE) .
.PHONY: dockerbuild

compose:  ##@docker Run the docker-compose powered setup.
	@cd dockercompose && $(PIPENVRUN) docker-compose up
.PHONY: compose

dbmigrations:  ##@django Create database migrations
	@$(PIPENVRUN) $(MANAGEPY) makemigrations
	@$(PIPENVRUN) $(MANAGEPY) makemigrations carbondioxide
.PHONY: dbmakemigrations

dbcheckmigrations:  ##@django Check if you need to create a new migration.
	@$(PIPENVRUN) $(MANAGEPY) makemigrations --check
.PHONY: dbcheckmigrations

dbmigrate:  ##@django Run the database migrations.
	@$(PIPENVRUN) $(MANAGEPY) migrate
.PHONY: dbmigrate

dbreset:  ##@django Reset the database. Watch your environment!
	@$(PIPENVRUN) $(MANAGEPY) reset_db
.PHONY: dbreset

celery:  ##@django Run the celery worker.
	@$(PIPENVRUN) celery -A carbondoomsday -l info worker -B -E
.PHONY: celery

static:  ##@django Collect all static files needed for Django.
	@$(PIPENVRUN) $(MANAGEPY) collectstatic --noinput -v 3
.PHONY: static

devserver:  ##@django Run the development mode server
	@$(PIPENVRUN) $(MANAGEPY) runserver
.PHONY: devserver

createadmin:  ##@django Create an admin user for the Django admin.
	@$(PIPENVRUN) $(MANAGEPY) createsuperuser
.PHONY: createadmin

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DATA
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
scrapelatest:  ##@data Get the latest CO2 measurement data.
	@$(PIPENVRUN) $(MANAGEPY) scrape_latest
.PHONY: scrapelatest

scrapehistoric:  ##@data Get historical CO2 measurement data.
	@$(PIPENVRUN) $(MANAGEPY) scrape_historic
.PHONY: scrapehistoric

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HEROKU
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
prodbash:  ##@heroku Run a bash console on the production server.
	@heroku run bash -a carbondoomsday
.PHONY: prodbash

testbash:  ##@heroku Run a bash console on the test server.
	@heroku run bash -a carbondoomsday-test
.PHONY: testbash

runlocal:  ##@heroku Run a local web server like Heroku would.
	@heroku local web
.PHONY: testbash

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# JAVASCRIPT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
jsbuild:  ##@javascript Build the React components
	@npm run build
.PHONY: jsbuild

jswatch:  ##@javascript Build and watch the React components
	@npm run watch
.PHONY: jswatch
