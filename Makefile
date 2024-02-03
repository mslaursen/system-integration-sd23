01-a:
	poetry run go run assignments/01/main.go
01-b:
	poetry run python assignments/01/main.py

lint-py:
	poetry run ruff check . --fix
	poetry run mypy assignments
	poetry run black assignments
