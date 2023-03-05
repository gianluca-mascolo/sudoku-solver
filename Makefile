format:
	poetry run black .
	poetry run isort .
	poetry run flake8 .
test:
	poetry run pytest
sudoku:
	poetry run sudoku
setup:
	poetry install
	pre-commit install
