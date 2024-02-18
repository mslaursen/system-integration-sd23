01-a:
	poetry run go run assignments/assignment1/go_solution/parse_module.go
01-b:
	python assignments/assignment1/python_solution/parse_module.py

lint-py:
	poetry run ruff check . --fix
	poetry run mypy assignments
	poetry run black assignments

02-a:
	uvicorn assignments.assignment2.server:app --reload
