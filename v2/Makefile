.PHONY: install test run docker

install:
	python -m pip install -e '.[dev]'

test:
	pytest -q

run:
	python app.py

docker:
	docker build -t mylife-v2:local .
