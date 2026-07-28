#!/usr/bin/env python3
"""Generate coverage report for AMBench tasks."""

import json
import yaml
from pathlib import Path
from collections import defaultdict

all_cells = [(f, fo, d) for f in ['factual', 'experiential', 'working']
             for fo in ['token-level', 'parametric', 'latent']
             for d in ['formation', 'evolution', 'retrieval']]

cells = defaultdict(int)
for f in Path('tasks').rglob('*.yaml'):
    if '.gitkeep' in f.name:
        continue
    with open(f) as fh:
        ep = yaml.safe_load(fh).get('episode', {})
    cells[ep.get('cell', 'unknown')] += 1

print("=" * 60)
print("  AMBENCH COVERAGE REPORT")
print("=" * 60)
print()
print(f"{'Function':12s} {'Form':14s} {'Dynamics':12s}  {'Tasks':>5s}  {'Status':>8s}")
print("-" * 52)

covered_cells = 0
total_tasks = 0
for func, form, dyn in all_cells:
    key = f"{func}/{form}/{dyn}"
    count = cells.get(key, 0)
    total_tasks += count
    if count >= 5:
        status = "🟢 5+"
    elif count >= 1:
        status = "🟡 1-4"
    else:
        status = "🔴 0"
    bar = "#" * min(count, 20) + "-" * (20 - min(count, 20))
    print(f"{func:12s} {form:14s} {dyn:12s}  [{bar}] {count:2d}  {status}")
    if count > 0:
        covered_cells += 1

print("-" * 52)
print(f"{'TOTAL':39s}  {total_tasks:2d}  {covered_cells}/27 cells")
print()

# Summary by function
func_counts = defaultdict(int)
for k, v in cells.items():
    func_counts[k.split('/')[0]] += v
print("By Function:")
for func in ['factual', 'experiential', 'working']:
    print(f"  {func:15s}: {func_counts.get(func, 0):3d} tasks")

# Summary by form
form_counts = defaultdict(int)
for k, v in cells.items():
    form_counts[k.split('/')[1]] += v
print("By Form:")
for form in ['token-level', 'parametric', 'latent']:
    print(f"  {form:15s}: {form_counts.get(form, 0):3d} tasks")

# Extended dimensions
print()
print("=" * 60)
print("  EXTENDED DIMENSIONS")
print("=" * 60)
extended_tags = defaultdict(int)
for f in Path('tasks').rglob('*.yaml'):
    if '.gitkeep' in f.name:
        continue
    with open(f) as fh:
        ep = yaml.safe_load(fh).get('episode', {})
    for tag in ep.get('tags', []):
        if tag in ['temporal', 'decay', 'consolidation', 'bitemporal',
                   'multimodal', 'visual', 'audio', 'cross-modal',
                   'security', 'poisoning', 'injection',
                   'multi-agent']:
            extended_tags[tag] += 1

if extended_tags:
    for tag, count in sorted(extended_tags.items()):
        print(f"  {tag:20s}: {count:3d} tasks")

# Save JSON
report = {
    "total_tasks": total_tasks,
    "cells_covered": covered_cells,
    "cells_total": 27,
    "cells": {k: v for k, v in sorted(cells.items())},
}
Path("docs/coverage-report.json").write_text(json.dumps(report, indent=2))
print(f"\nReport saved to docs/coverage-report.json")
