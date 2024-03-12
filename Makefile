all: venv_create dry_run

check:
	pyenv virtualenv 3.10 rss_tmp -f
	pyenv local rss_tmp
	python3 app/rss_feed_reader.py

venv_create:
	pyenv install 3.10 --skip-existing
	pyenv virtualenv 3.10 rss_tmp -f
	pyenv local rss_tmp
	pip install -r app/requirements.txt

dry_run: venv_create
	pyenv local rss_tmp
	HOW_DEEP_ITEMS_LOOK_BACK=12 \
	LOOKING_DAYS=365 \
	SENSITIVE_PLUGINS='HTMLResource' \
	python3 app/rss_feed_reader.py

test:
	pyenv local rss_tmp
	pip install pytest pytest-cov
	pytest tests/
	coverage run -m pytest
	coverage report -m

lint:
	pyenv local rss_tmp
	pip install flake8 pylint
	flake8 app/rss_feed_reader.py
	pylint app/rss_feed_reader.py