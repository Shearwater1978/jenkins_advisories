SENSITIVE_PLUGINS ?= 'HTMLResource'
HOW_DEEP_ITEMS_LOOK_BACK ?= 12
LOOKING_DAYS ?= 365

all: help

.PHONY: help
help: ## Display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "\033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: check
check: venv_create ## Run script in the prod mode
	pyenv local rss_tmp
	pip install -r app/requirements.txt >/dev/null 2>&1
	python3 app/rss_feed_reader.py

.PHONY: venv_create
venv_create: ## Create and prepare env, if it nor exists
	pyenv install 3.10 --skip-existing >/dev/null 2>&1
	pyenv virtualenv 3.10 rss_tmp -f
	pyenv local rss_tmp
	pip install -r app/requirements.txt >/dev/null 2>&1

.PHONY: dry_run
dry_run: venv_create ## Dry run script
	pyenv local rss_tmp
	HOW_DEEP_ITEMS_LOOK_BACK=$(HOW_DEEP_ITEMS_LOOK_BACK) \
	LOOKING_DAYS=$(LOOKING_DAYS) \
	SENSITIVE_PLUGINS=$(SENSITIVE_PLUGINS) \
	python3 app/rss_feed_reader.py

.PHONY: test
test: venv_create ## Executing pytest
	pyenv local rss_tmp
	pip install pytest pytest-cov >/dev/null 2>&1
	pytest tests/
	coverage run -m pytest
	coverage report -m
	pytest --cov --cov-report=html

.PHONY: lint
lint: venv_create ## Executing linters
	pyenv local rss_tmp
	pip install flake8 pylint >/dev/null 2>&1
	flake8 app/rss_feed_reader.py
	pylint app/rss_feed_reader.py