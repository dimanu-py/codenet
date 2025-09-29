.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(firstword $(MAKEFILE_LIST)) | \
			awk 'BEGIN {FS = ":.*## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: local-setup
local-setup:  ## Setup git hooks and install dependencies.
	@echo "\n⌛ Setting up the project...\n"
	@make install
	@uv run -m pre_commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

.PHONY: test
test:  ## Run all test.
	@echo "\n⌛ Running tests...\n"
	@make up
	@uv run pytest tests -ra
	@make down

.PHONY: unit
unit:  ## Run all unit test.
	@echo "\n⌛ Running unit tests...\n"
	@uv run pytest -m "unit" -ra

.PHONY: integration
integration:  ## Run all integration test.
	@echo "\n⌛ Running integration tests...\n"
	@uv run pytest -m "integration" -ra

.PHONY: acceptance
acceptance:  ## Run all acceptance test.
	@echo "\n⌛ Running acceptance tests...\n"
	@make up
	@uv run pytest -m "acceptance" -ra
	@make down

.PHONY: coverage
coverage:  ## Run all test with coverage.
	@echo "\n⌛ Running tests with coverage...\n"
	@make up
	@uv run coverage run --branch -m pytest tests
	@uv run coverage html
	@make down
	@$(BROWSER) htmlcov/index.html

.PHONY: install
install:  ## Install dependencies.
	@echo "\n⌛ Installing dependencies...\n"
	@uv sync --all-groups

.PHONY: update
update:  ## Update dependencies.
	@echo "\n⌛ Updating dependencies...\n"
	@uv sync --upgrade

.PHONY: add-dep
add-dep:  ## Add a new dependency <make add-dep dep="mypy --group lint">
	@uv add $(dep)

.PHONY: remove-dep
remove-dep:  ## Remove a dependency <make remove-dep="mypy --group lint">
	@uv remove $(dep)

.PHONY: check-typing
check-typing:  ## Run mypy type checking.
	@echo "\n⌛ Running type checking with mypy...\n"
	@uv run mypy

.PHONY: check-lint
check-lint:  ## Run ruff linting check.
	@echo "\n⌛ Running linting check...\n"
	@uvx ruff check src tests

.PHONY: lint
lint:  ## Apply ruff linting fix.
	@echo "\n⌛ Applying linting fixes...\n"
	@uvx ruff check --fix src tests

.PHONY: check-format
check-format:  ## Run ruff format check.
	@echo "\n⌛ Checking code formatting...\n"
	@uvx ruff format --check src tests

.PHONY: format
format:  ## Apply ruff format fix.
	@echo "\n⌛ Formatting project code...\n"
	@uvx ruff format src tests

.PHONY: watch
watch:  ## Run all test with every change.
	@echo "\n⌛ Running tests in watch mode...\n"
	@uv run ptw --runner "pytest -n auto test -ra"

.PHONY: show
show:  ## Show installed dependencies.
	@uv tree

.PHONY: search
search:  ## Show package details.
	@read -p "Enter package name to search: " package;\
	@uv pip show $$package

.PHONY: audit
audit: # It audits dependencies and source code
	@echo "\n⌛ Running security audit...\n"
	@uv run -m pip_audit --progress-spinner off

.PHONY: secrets
secrets: # It checks for secrets in the source code
	@echo "\n⌛ Checking secrets...\n"
	@uv run -m pre_commit run gitleaks --all-files

.PHONY: up
up: ## Create and start containers.
	@docker-compose up -d

.PHONY: down
down: ## Stop and remove containers.
	@docker-compose down -v --remove-orphans