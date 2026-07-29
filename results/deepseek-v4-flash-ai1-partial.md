# Partial Benchmark: DeepSeek V4 Flash (ai1) on Agent Memory Bench

**Date:** 2026-07-29
**Model:** `deepseek-v4-flash/ai1` via LiteLLM proxy (`192.168.42.20:4000`)
**Scoring:** `auto` (keyword F1 / exact match)
**Tasks:** 68/734 completed (partial — aborted, saved via `--resume`)

## Results

| Metric | Value |
|--------|-------|
| Tasks completed | 68 |
| Passed (score >= 0.5) | 9 (13.2%) |
| Weighted score | 24.2% |
| Total tokens | 17,327 |
| Avg latency | 48,111 ms |
| Fast responses (<100ms) | 34 (likely cached/retrieved) |
| Slow responses (>30s) | 32 |

## Analysis

- **Bimodal latency**: ~50% of responses arrived in <100ms (suggesting server-side caching or pre-computed results), ~50% took 30-170s (actual generation).
- **Score distribution**: Most scores clustered between 0.0-0.3, with only 9 tasks scoring >= 0.5. The model struggles with experiential/latent and experiential/parametric memory tasks that require implicit knowledge retrieval.
- **Cached responses scored lower on average** (0.11 vs 0.37 for full-generation responses), suggesting cached outputs are shorter/less specific.

## Cells Covered

Primarily experiential/latent (evolution, formation, retrieval) and experiential/parametric (evolution, formation). No factual or working memory cells were evaluated in this partial run.

## Resume

The `results/resume_state.jsonl` file contains completion data for all 68+5=73 tasks. Run with `--resume` to continue from task 74.
