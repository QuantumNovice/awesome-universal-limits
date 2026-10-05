PY ?= uv run python

.PHONY: figures test lint schemas sources site dev

figures:            ## regenerate schemas, JSON exports, figures, site data, references and the README gallery
	$(PY) -m allowed_universe.build

schemas:            ## rewrite data/schema/*.json from src/allowed_universe/datasets.py
	$(PY) -m allowed_universe.build --schemas

test:
	$(PY) -m pytest -q

lint:
	uv run ruff check src tests tools
	uv run ruff format --check src tests tools

sources:            ## check every DOI against Crossref and every URL over HTTP (needs network)
	$(PY) tools/check_sources.py

site:               ## production build of the Vue site into site/dist (run `make figures` first)
	cd site && npm ci && npm run build

dev:                ## local dev server for the site
	cd site && npm run dev
