all: venv_create dry_run

check_env:
	@test $${HOW_DEEP_ITEMS_LOOK_BACK?Please set environment variable HOW_DEEP_ITEMS_LOOK_BACK}
	@test $${LOOKING_DAYS?Please set environment variable LOOKING_DAYS}
	@test $${SENSITIVE_PLUGINS?Please set environment variable SENSITIVE_PLUGINS}

check:
	pyenv local rss_tmp
	python3 app/rss_feed_reader.py

venv_create:
	pyenv install 3.10 --skip-existing
	pyenv virtualenv 3.10 rss_tmp -f
	pyenv local rss_tmp
	pip install -r app/requirements.txt

dry_run:
	pyenv local rss_tmp
	HOW_DEEP_ITEMS_LOOK_BACK=12 \
	LOOKING_DAYS=365 \
	SENSITIVE_PLUGINS='kubernetes;HTMLResource' \
	python3 app/rss_feed_reader.py

test:
	pyenv local rss_tmp
	pip install pytest
	pytest tests/
