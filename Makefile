PROJECT_ROOT := .
MANAGE_PY    := python manage.py
REQS_DIR     := $(PROJECT_ROOT)/requirements
REQS_BASE    := $(REQS_DIR)/base.txt
REQS_ADMIN   := $(REQS_DIR)/administration.txt
REQS_TEST    := $(REQS_DIR)/test.txt
REQS_QUALITY := $(REQS_DIR)/quality.txt
REQS_PROD    := $(REQS_DIR)/production.txt

REQS_ALL     := $(REQS_BASE) $(REQS_ADMIN) $(REQS_TEST) $(REQS_QUALITY) $(REQS_PROD)
reqs: $(REQS_ALL)
.PHONY: reqs

upgrade:
	$(RM) $(REQS_ALL)
	$(MAKE) reqs PIP_COMPILE_ARGS=--rebuild
.PHONY: upgrade

$(REQS_DIR)/%.txt: PIP_COMPILE_ARGS?=
$(REQS_DIR)/%.txt: $(REQS_DIR)/%.in
	pip-compile --no-header $(PIP_COMPILE_ARGS) --output-file "$@.tmp" "$<" >/tmp/pip-compile.out.tmp || { \
	  ret=$$?; echo "pip-compile failed:" >&2; cat /tmp/pip-compile.out.tmp >&2; \
	  $(RM) "$@.tmp" /tmp/pip-compile.out.tmp; \
	  exit $$ret; }
	@sed -n '1,10 s/# Depends on/-r/; s/\.in/.txt/p' "$<" > "$@"
	@cat "$@.tmp" >> "$@"
	@$(RM) "$@.tmp" /tmp/pip-compile.out.tmp

lint:
	pylama $(PROJECT_ROOT)/carbondoomsday
.PHONY: lint

isort:
	find $(PROJECT_ROOT) -name "*.py" | xargs isort -c --diff -sp=setup.cfg
.PHONY: isort

PYTEST_ARGS?=
PYTEST=py.test -c setup.cfg $(PYTEST_ARGS)
test:
	$(PYTEST) $(PROJECT_ROOT)/carbondoomsday
.PHONY: test

install:
	pip install -e .
	pip install -r $(REQS_ADMIN) -r $(REQS_QUALITY) -r $(REQS_TEST)
.PHONY: install

DOCKER_IMAGE := carbondoomsday/carbondoomsday
docker_build:
	docker build -t $(DOCKER_IMAGE) .
.PHONY: docker_build

migrations:
	python manage.py makemigrations
.PHONY: makemigrations

migrate:
	python manage.py migrate
.PHONY: migrate
