# Leaderboard

AMBench public leaderboard. Submit your memory system results via PR.

## Submission Instructions

1. **Run the harness** on your system:
   ```bash
   python3 src/harness.py --model <your-model> [--litellm] [other flags]
   ```

2. **Create a submission JSON** following `template.json` schema:
   ```json
   {
     "system": "MyMemorySystem",
     "model": "gpt-4",
     "scores": {
       "overall": 0.85,
       "factual": 0.9,
       "experiential": 0.82,
       "working": 0.88,
       "temporal": 0.8,
       "multimodal": 0.75,
       "security": 0.95,
       "multi-agent": 0.78
     },
     "date": "2026-07-29"
   }
   ```

3. **Place the file** at `leaderboard/submissions/<your-system-name>.json`

4. **Open a PR** using the leaderboard submission template

## Verification

Submissions are automatically validated on PR:
- JSON schema must match `template.json`
- All 8 score categories required
- Scores must be numbers between 0.0 and 1.0
- Date must be ISO8601 (YYYY-MM-DD)

## Ranking

Leaderboard is sorted by **overall** score descending (highest first). Ties broken arbitrarily.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `system` | string | Name of your memory system |
| `model` | string | LLM model identifier |
| `scores.overall` | float 0-1 | Aggregate score across all categories |
| `scores.factual` | float 0-1 | Factual memory score |
| `scores.experiential` | float 0-1 | Experiential memory score |
| `scores.working` | float 0-1 | Working memory score |
| `scores.temporal` | float 0-1 | Temporal reasoning score |
| `scores.multimodal` | float 0-1 | Multimodal integration score |
| `scores.security` | float 0-1 | Security/alignment score |
| `scores.multi-agent` | float 0-1 | Multi-agent coordination score |
| `date` | string | ISO8601 date of evaluation |
