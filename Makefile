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

test:
	@$(PIPENVRUN) pytest --cov=carbondoomsday
.PHONY: test

proof: lint sort test dbcheckmigrations
.PHONY: proof

celery:
	@$(PIPENVRUN) celery -A carbondoomsday -l info worker -B -E
.PHONY: celery

shell:
	@$(PIPENVRUN) $(MANAGEPY) shell_plus --ipython --quiet-load
.PHONY: shell

server:
	@$(PIPENVRUN) $(MANAGEPY) runserver
.PHONY: server

scrape_mlo_co2_since_2015:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_2015
.PHONY: scrape_mlo_co2_since_2015

scrape_mlo_co2_since_1974:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_1974
.PHONY: scrape_mlo_co2_since_1974

scrape_mlo_co2_since_1958:
	@$(PIPENVRUN) $(MANAGEPY) scrape_mlo_co2_since_1958
.PHONY: scrape_mlo_co2_since_1958
