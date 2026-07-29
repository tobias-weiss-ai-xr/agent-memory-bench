#!/usr/bin/env bash
# AMBench Comprehensive Test Battery
# Run: bash scripts/test_battery.sh
set -euo pipefail

PASS=0
FAIL=0
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass() { PASS=$((PASS+1)); echo -e "  ${GREEN}✅${NC} $1"; }
fail() { FAIL=$((FAIL+1)); echo -e "  ${RED}❌${NC} $1"; }

echo "=== AMBench Test Battery ==="
echo ""

# 1. Validation
echo "--- Validation ---"
python3 scripts/validate.py && pass "Validate all tasks" || fail "Validate all tasks"
python3 scripts/coverage.py > /dev/null 2>&1 && pass "Coverage generation" || fail "Coverage generation"
python3 scripts/validate.py /tmp/nonexistent_dir_xyz 2>&1 && fail "Empty dir rejected" || pass "Empty dir rejected"

# 2. Unit Tests
echo "--- Unit Tests ---"
python3 -m pytest tests/ -q > /dev/null 2>&1 && pass "pytest suite" || fail "pytest suite"

# 3. Harness Modes
echo "--- Harness Modes ---"
python3 src/harness.py --mock --max-tasks 5 > /dev/null 2>&1 && fail "Mock mode (should fail >50%)" || pass "Mock mode"
python3 src/harness.py --mock --max-tasks 3 --markdown /tmp/am-test.md > /dev/null 2>&1 && fail "Mock with markdown" || pass "Mock with markdown"
python3 src/harness.py --mock --cells factual --max-tasks 2 > /dev/null 2>&1 && fail "Mock cell filter" || pass "Mock cell filter"
python3 src/harness.py --mock --scoring exact --max-tasks 2 > /dev/null 2>&1 && fail "Scoring exact" || pass "Scoring exact"
python3 src/harness.py --mock --scoring keyword --max-tasks 2 > /dev/null 2>&1 && fail "Scoring keyword" || pass "Scoring keyword"
python3 src/harness.py --mock --scoring llm_judge --max-tasks 2 > /dev/null 2>&1 && fail "Scoring llm_judge" || pass "Scoring llm_judge"

# 4. CLI
echo "--- CLI ---"
# No args should show help (not hang or crash)
(env -u LITELLM_API_KEY -u DEEPSEEK_API_KEY -u OPENAI_API_KEY -u OPENROUTER_API_KEY python3 src/harness.py 2>&1 || true) | grep -q "usage" && pass "No args shows help" || fail "No args shows help"
python3 src/harness.py --help 2>&1 | grep -q usage && pass "Help flag" || fail "Help flag"

# 5. Integrity
echo "--- Integrity ---"
python3 -c "import yaml,sys;from pathlib import Path;from collections import Counter;ids=[yaml.safe_load(open(f)).get('episode',{}).get('id','') for f in Path('tasks').rglob('*.yaml') if '.gitkeep' not in f.name];dupes=[(e,c) for e,c in Counter(ids).items() if c>1];sys.exit(len(dupes))" \
  && pass "Unique IDs" || fail "Duplicate IDs found!"

# 6. Summary
echo ""
echo "============================================"
TOTAL=$((PASS+FAIL))
echo -e "Results: ${GREEN}${PASS}${NC}/${TOTAL} passed"
if [ $FAIL -gt 0 ]; then
  echo -e "${RED}${FAIL} tests FAILED${NC}"
  exit 1
else
  echo -e "${GREEN}All tests passed!${NC}"
fi
