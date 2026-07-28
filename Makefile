.PHONY: validate test clean

validate:
	@echo "Validating task YAML files..."
	@python3 -c "
	import yaml
	from pathlib import Path
	errors = 0
	for f in sorted(Path('tasks').rglob('*.yaml')):
	    if '.gitkeep' in f.name: continue
	    try:
	        with open(f) as fh:
	            data = yaml.safe_load(fh)
	        ep = data.get('episode', {})
	        assert 'id' in ep, f'{f}: missing id'
	        assert 'cell' in ep, f'{f}: missing cell'
	        assert 'query' in ep, f'{f}: missing query'
	        assert 'expected' in ep, f'{f}: missing expected'
	    except Exception as e:
	        print(f'  ERROR: {e}')
	        errors += 1
	if errors:
	    print(f'Found {errors} error(s)')
	    exit(1)
	print('All tasks valid')
	"

test:
	python3 -m pytest tests/

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete

count:
	@echo "Task count by cell:"
	@find tasks -name '*.yaml' ! -name '.gitkeep' | sort | while read f; do \
		cell=$$(grep -A1 'cell:' "$$f" | tail -1 | sed 's/.*cell: *//'); \
		echo "$$cell"; \
	done | sort | uniq -c | sort -rn
