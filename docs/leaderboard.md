# AMBench Leaderboard

**Central registry of agent memory system evaluation results.**

Inspired by the [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
and [HELM](https://crfm.stanford.edu/helm/latest/).

---

## How to Submit

1. Run the evaluation harness:
   ```bash
   python src/harness.py --model your-model --markdown results.md --output results.json
   ```

2. Open a PR with your `results.json` to the `leaderboard/` directory.

3. The leaderboard maintainers will verify and merge.

## Current Rankings

*No submissions yet — be the first!*

| Rank | Model | Params | Context | Core Score | Temporal | Multimodal | Cost/Task | Submitted |
|------|-------|--------|---------|:----------:|:---------:|:----------:|:---------:|:----------|
| — | — | — | — | — | — | — | — | — |

## Metrics

| Metric | Description | Weight |
|--------|-------------|:------:|
| **Core Score** | Average accuracy across all 27 taxonomy cells | 40% |
| **Temporal** | Accuracy on decay, consolidation, bi-temporal tasks | 20% |
| **Multimodal** | Accuracy on visual, audio, cross-modal tasks | 15% |
| **Cost/Task** | Average tokens consumed per task (lower is better) | 15% |
| **Latency** | Average response time per task (lower is better) | 10% |

## Scoring Formula

```
Final Score = 0.40 × Core + 0.20 × Temporal + 0.15 × Multimodal 
            + 0.15 × (1 - cost/max_cost) + 0.10 × (1 - latency/max_latency)
```

Where `max_cost` and `max_latency` are the worst values among all submissions.

## Hall of Champions

When a system achieves all of the following simultaneously, it enters the Hall:

| Criterion | Threshold |
|-----------|:---------:|
| Core Score | ≥90% across all 27 cells |
| Cell Balance | ≤10% variance between best/worst cell |
| Temporal Decay | ≤10% accuracy loss over 90-day simulated window |
| Memory Isolation | ≥20 point improvement over no-memory baseline |
| Cost Efficiency | ≤5,000 tokens per query average |
| Latency | ≤500ms p95 retrieval |
| Adversarial Robustness | ≥80% accuracy under poisoning attack |
