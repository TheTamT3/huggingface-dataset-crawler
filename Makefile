.PHONY: install
install:
	@echo "🚀 Installing environment"
	poetry install --with dev

.PHONY: lint
lint:
	@echo "🚀 Checking poetry.lock file"
	poetry check --lock
	@echo "🚀 Linting with ruff"
	poetry run ruff check --exclude src/serivces/crawler/
	@echo "🚀 Linting with pylint"
	poetry run pylint src
	@echo "🚀 Checking with mypy"
	poetry run mypy src --exclude src/serivces/crawler/
	@echo "🟢 All checks have passed"


.PHONY: format
format:
	@echo "🚀 Formatting with ruff"
	poetry run ruff format
	@echo "🟢 Formated"

.PHONY: fix
fix:
	@echo "🚀 Fixing with ruff"
	poetry run ruff check --fix ${path} --exclude src/serivces/crawler/
	@echo "🟢 Fixed"



