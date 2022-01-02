# Show help by default.
.DEFAULT_GOAL := help

## help: show available commands
.PHONY: help
help:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## serve: run server
.PHONY: serve
serve:
	@python -m harper.server

## test: run unit tests
.PHONY: test
test:
	@pytest tests

## coverage: run available tests and report coverage
.PHONY: coverage
coverage:
	@coverage run --branch -m pytest
	@coverage html

## docs: build documentation
.PHONY: docs
docs:
	@mkdocs build

## lint: run software quality checks
.PHONY: lint
lint:
	@flake8
	@isort --check .
	@black --check .
	@pydocstyle --convention=google --count harper

## reformat: reformat code in place
.PHONY: reformat
reformat:
	@isort .
	@black .

## clean: remove junk files
.PHONY: clean
clean:
	@find . -type d -name __pycache__ -exec rm -rf {} \;
	@find . -name '*~' -exec rm {} \;
	@find . -name .DS_Store -exec rm {} \;
	@rm -rf htmlcov
