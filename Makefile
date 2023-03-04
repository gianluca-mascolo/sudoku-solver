format:
	poetry run flake8 .
	poetry run black .
	poetry run isort .
test:
	poetry run pytest
sudoku:
	poetry run sudoku
