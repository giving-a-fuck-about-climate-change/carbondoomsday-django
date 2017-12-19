PROJECT_ROOT := .
SOURCE_DIR   := $(PROJECT_ROOT)/carbondoomsday/
MANAGEPY     := python manage.py
PIPENVRUN    := pipenv run
DOCKER_IMAGE := carbondoomsday/measurements/

dockerbuild:
	@docker build -t $(DOCKER_IMAGE) .
.PHONY: dockerbuild

lint:
	@$(PIPENVRUN) pylama $(SOURCE_DIR)
.PHONY: lint

sort:
	@find $(SOURCE_DIR) -name "*.py" | xargs $(PIPENVRUN) isort -c --diff -sp=setup.cfg
.PHONY: sort

pyclean:
	@find $(SOURCE_DIR) -name "*.pyc" | xargs rm

test:
	@$(PIPENVRUN) pytest --cov=carbondoomsday
.PHONY: test

proof: lint sort test dbcheckmigrations
.PHONY: proof

showurls:
	@$(PIPENVRUN) $(MANAGEPY) show_urls -f aligned | less
.PHONY: showurls

dbmigrations:
	@$(PIPENVRUN) $(MANAGEPY) makemigrations measurements
.PHONY: dbmigrations

dbcheckmigrations:
	@$(PIPENVRUN) $(MANAGEPY) makemigrations --check
.PHONY: dbcheckmigrations

dbmigrate:
	@$(PIPENVRUN) $(MANAGEPY) migrate
.PHONY: dbmigrate

dbreset:
	@$(PIPENVRUN) $(MANAGEPY) reset_db
.PHONY: dbreset

celery:
	@$(PIPENVRUN) celery -A carbondoomsday -l info worker -B -E
.PHONY: celery

shell:
	@$(PIPENVRUN) $(MANAGEPY) shell_plus --bpython --quiet-load
.PHONY: shell

server:
	@$(PIPENVRUN) $(MANAGEPY) runserver
.PHONY: server

dbadmin:
	@$(PIPENVRUN) $(MANAGEPY) createsuperuser
.PHONY: dbadmin

scrape_mlo_co2_since_2015:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_2015
.PHONY: scrape_mlo_co2_since_2015

scrape_mlo_co2_since_1974:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_1974
.PHONY: scrape_mlo_co2_since_1974

scrape_mlo_co2_since_1958:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_1958
.PHONY: scrape_mlo_co2_since_1958

prodbash:
	@heroku run bash -a carbondoomsday
.PHONY: prodbash

prodrelease:
	@git push heroku-prod master
.PHONY: prodrelease

prodlogs:
	@heroku logs -t -a carbondoomsday
.PHONY: prodlogs

testbash:
	@heroku run bash -a carbondoomsday-test
.PHONY: testbash

testlogs:
	@heroku logs -t -a carbondoomsday-test
.PHONY: testlogs
