.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(firstword $(MAKEFILE_LIST)) | \
			awk 'BEGIN {FS = ":.*## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: test
test:  ## Run all test.
	@make up
	@uv run pytest -n 0 tests -ra
	@make down

.PHONY: unit
unit:  ## Run all unit test.
	@uv run pytest -n auto -m "unit" -ra

.PHONY: integration
integration:  ## Run all integration test.
	@uv run pytest -m "integration" -ra

.PHONY: acceptance
acceptance:  ## Run all acceptance test.
	@make up
	@uv run pytest -m "acceptance" -ra
	@make down

.PHONY: coverage
coverage:  ## Run all test with coverage.
	@make up
	@uv run coverage run --branch -m pytest tests
	@uv run coverage html
	@make down
	@$(BROWSER) htmlcov/index.html

.PHONY: local-setup
local-setup:  ## Setup git hooks and install dependencies.
	@scripts/local-setup.sh
	@make install

.PHONY: install
install:  ## Install dependencies.
	@uv sync --all-groups

.PHONY: update
update:  ## Update dependencies.
	@uv sync --upgrade

.PHONY: add-dep
add-dep:  ## Add a new dependency.
	@scripts/add-dependency.sh

.PHONY: remove-dep
remove-dep:  ## Remove a dependency.
	@scripts/remove-dependency.sh

.PHONY: check-typing
check-typing:  ## Run mypy type checking.
	@uv run mypy

.PHONY: check-lint
check-lint:  ## Run ruff linting check.
	@uvx ruff check src tests

.PHONY: lint
lint:  ## Apply ruff linting fix.
	@uvx ruff check --fix src tests

.PHONY: check-format
check-format:  ## Run ruff format check.
	@uvx ruff format --check src tests

.PHONY: format
format:  ## Apply ruff format fix.
	@uvx ruff format src tests

.PHONY: pre-commit
pre-commit: check-typing check-lint check-format all-unit ## Run pre-commit checks.

.PHONY: pre-push
pre-push:  all-integration all-acceptance ## Run pre-push checks.

.PHONY: watch
watch:  ## Run all test with every change.
	@uv run ptw --runner "pytest -n auto tests -ra"

.PHONY: insert-template
insert-template:  ## Insert a template class among the existing ones.
	@uv run python -m scripts.insert_template

.PHONY: create-aggregate
create-aggregate:  ## Create a new aggregate inside contexts folder.
	@uv run python -m scripts.create_aggregate

.PHONY: show
show:  ## Show installed dependencies.
	@uv tree

.PHONY: search
search:  ## Show package details.
	@read -p "Enter package name to search: " package;\
	uv pip show $$package

.PHONY: commit
commit: ## Commit changes with commitizen.
	@cz commit

.PHONY: up
up: ## Create and start containers.
	@docker-compose up -d

.PHONY: down
down: ## Stop and remove containers.
	@docker-compose down -v --remove-orphans