setup:
	poetry install
	pre-commit install

lint:
	flake8 ./*.py
	isort --check --diff ./*.py
	black --check ./*.py

fix:
	isort ./*.py
	black ./*.py