PACKAGE = mdthtml
VENV = .venv

.PHONY: build
build: clean src tests pyproject.toml
	python -m build

.PHONY: venv
venv: build
	rm -rf $(VENV)
	python -m venv $(VENV)
	.venv/bin/python -m pip install . pytest

.PHONY: pipx
pipx: build
	pipx install .

.PHONY: test
test: venv
	.venv/bin/pytest -s tests

.PHONY: clean
clean:
	rm -fr dist build src/*egg-info .pytest_cache .venv
	find . -type d -name __pycache__ -exec rm -r {} \+
