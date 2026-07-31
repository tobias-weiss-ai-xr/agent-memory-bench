# CaRE Protocol — Compute-aware Remasking Evaluation

This document defines the **CaRE evaluation protocol** implemented in the AMBench harness. It adapts the *CaRE (Compute-aware Remasking Evaluation)* methodology from arXiv:2607.24763 to LLM-based agent memory evaluation.

## Motivation

[CaRE](https://arxiv.org/abs/2607.24763) showed that masked diffusion language model (MDLM) evaluations systematically conflate algorithmic improvements with hidden choices of compute and stochasticity. Compute-matched comparisons **reversed several published rankings**, and temperature alone explained the majority of score variance.

AMBench faces the identical failure modes when comparing agent memory systems:

| Failure Mode | Effect on Rankings |
|--------------|-------------------|
| Different `max_tokens` budgets per submission | Systems with more compute appear "better" |
| Temperature not reported / not fixed | Rankings flip across sampling temperatures |
| Single-run evaluations | Variance treated as signal; rank instability |
| Single-metric reporting | Cost/latency trade-offs invisible |

## The Three Pillars

### 1. Standardise NFE (Number of Function Evaluations)

For LLM evaluation, the compute budget per task is the generation budget. CaRE mode requires all submissions to run with an explicit, reported NFE budget:

```
--max-tokens 512
```

The harness emits `max_tokens` in the report config and the CaRE report header. Submissions with different NFE budgets are **not directly comparable** — report the budget alongside every score.

### 2. Control Stochasticity Explicitly

Sampling temperature and seed are first-class, controlled variables:

```
--temperature 0.0 --seed 42 --runs 3
```

- `--seed` sets the sampling seed (where the provider supports it) and the seed base for multi-run sweeps
- `--runs N` executes the full task suite N times with seeds `base + 0..N-1`
- Reports show **mean ± std** across runs, making variance visible rather than hidden

### 3. Enforce Multi-Metric Reporting

Every CaRE evaluation reports three metrics simultaneously:

| Metric | What It Captures |
|--------|------------------|
| **Score** | Memory-system correctness (0.0–1.0) |
| **Latency (ms)** | Per-task response time |
| **Tokens (NFE)** | Actual compute consumed |

A system that scores higher only because it consumes 4× the tokens is *visible* in CaRE output — it cannot hide behind a single headline number.

## Running a CaRE Evaluation

```bash
# Deterministic single run (baseline)
python src/harness.py --model gpt-4o-mini --temperature 0.0 \
  --seed 42 --max-tokens 512 --markdown results/care-gpt4o-mini.md

# Variance-aware evaluation: 5 seeded runs
python src/harness.py --model gpt-4o-mini --temperature 0.0 \
  --seed 42 --runs 5 --max-tokens 512 --markdown results/care-gpt4o-mini-5runs.md

# Temperature sensitivity sweep (3 temperatures × 3 runs)
for t in 0.0 0.5 1.0; do
  python src/harness.py --model gpt-4o-mini --temperature $t \
    --seed 42 --runs 3 --max-tokens 512 \
    --markdown results/care-gpt4o-mini-t$t.md
done
```

CaRE runs are compatible with the memory-isolation baseline: run the same seeds against a no-memory baseline to compute isolation gains per run.

## Leaderboard Submission Requirements

CaRE-compliant leaderboard submissions MUST include:

1. **NFE budget** (`max_tokens`) — standardised at 512 unless explicitly overridden
2. **Stochasticity settings** — temperature AND seed base
3. **Number of runs** — minimum 3 for variance reporting
4. **Multi-metric table** — score, latency, tokens
5. **Full report** produced by `src/harness.py --runs N` (no hand-picked runs)

## Interpreting Results

- **Mean ± std**: report the mean, but treat std as the error bar. A 0.05 score gap with 0.06 std is noise.
- **Score per NFE**: normalise by `max_tokens` when comparing across budgets — score/token efficiency matters.
- **Rank stability**: check whether the per-run ranking of systems is stable; unstable rankings indicate the benchmark is not resolving the systems.

## References

- CaRE: Compute-aware Remasking Evaluation Protocol for Masked Diffusion Language Models — [arXiv:2607.24763](https://arxiv.org/abs/2607.24763)
- AMBench harness: `src/harness.py` (flags: `--max-tokens`, `--seed`, `--runs`, `--temperature`)
