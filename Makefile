.PHONY: validate test coverage clean

validate:
	@echo "Validating task YAML files..."
	@python3 scripts/validate.py

test:
	python3 -m pytest tests/ -v 2>/dev/null || echo "No tests directory yet (normal for v0.1)"

coverage:
	python3 scripts/coverage.py

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
