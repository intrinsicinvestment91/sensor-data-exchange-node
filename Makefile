.PHONY: test lint typecheck benchmark install

install:
	pip install -r requirements-dev.txt

lint:
	ruff check sden/ tests/ sden-client/sden_client/ sden-client/tests/

typecheck:
	mypy sden/ --ignore-missing-imports

test: lint typecheck
	pytest -v

benchmark:
	pytest tests/test_benchmark.py -v --tb=short
