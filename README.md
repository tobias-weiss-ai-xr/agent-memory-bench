<p align="center">
  <h1 align="center">AMBench</h1>
  <p align="center"><strong>Unified Benchmark for Agent Memory Systems</strong></p>
  <p align="center">
    <a href="https://github.com/tobias-weiss-ai-xr/agent-memory-bench"><img src="https://img.shields.io/badge/GitHub-181717.svg?logo=github" alt="GitHub"></a>
    <a href="https://gitlab.com/tbsweiss/agent-memory-bench"><img src="https://img.shields.io/badge/GitLab-2185D0.svg?logo=gitlab" alt="GitLab"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/agent-memory-bench/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/tobias-weiss-ai-xr/agent-memory-bench/validate.yml?label=CI&logo=github" alt="CI"></a>
    <a href="docs/leaderboard.md"><img src="https://img.shields.io/badge/Leaderboard-Open-004D40.svg" alt="Leaderboard"></a>
  </p>
</p>

---

## The Problem

The [agent memory research landscape](https://github.com/tobias-weiss-ai-xr/agent-memory-research) has grown to **1,049 papers** with **80+ distinct benchmarks** — yet **no single benchmark spans more than 11 of 27 taxonomy cells**.

| Benchmark | Cells | What's Missing |
|-----------|:-----:|----------------|
| LoCoMo | 1 | Temporal, multimodal, experiential, working |
| LongMemEval | 1 | Everything except factual/token-level |
| MemBench | ~11 | Experiential, temporal, multimodal |
| **AMBench** | **27** | **Full coverage** |

## What AMBench Covers

### 27-Cell Taxonomy (Forms × Functions × Dynamics)

| | Token-level | Parametric | Latent |
|---|:---:|:---:|:---:|
| **Factual** | 7 tasks | 5 tasks | 5 tasks |
| **Experiential** | 5 tasks | 5 tasks | 5 tasks |
| **Working** | 7 tasks | 5 tasks | 5 tasks |

### Extended Dimensions

| Dimension | Description | Tasks |
|-----------|-------------|:-----:|
| ⏱ Temporal | Decay, consolidation, bi-temporal | 11 |
| 🖼 Multimodal | Visual, audio, cross-modal | 9 |
| 🔒 Security | Memory poisoning, injection | 5 |
| 👥 Multi-agent | Shared memory, experience transfer | 5 |

**Total: 147 core + 30 extended = 177 tasks**

## Quick Start

```bash
git clone https://github.com/tobias-weiss-ai-xr/agent-memory-bench.git
cd agent-memory-bench
pip install -r requirements.txt
pip install openai  # for API access

# Dry run (no API key needed)
python src/harness.py --mock --max-tasks 5

# LiteLLM proxy (recommended)
export LITELLM_API_KEY=sk-...
python src/harness.py --litellm --model gpt-4

# Direct API
export DEEPSEEK_API_KEY=sk-...
python src/harness.py --model deepseek/deepseek-v4-flash

# Full report
python src/harness.py --litellm --markdown results.md
```

## Key Features

| Feature | Inspired By | Status |
|---------|-------------|:------:|
| **27-cell taxonomy** | Original survey | ✅ |
| **LLM-as-judge scoring** | MT-Bench, AlpacaEval | ✅ |
| **Canary GUID** | BIG-bench | ✅ |
| **Multi-metric evaluation** | HELM | ✅ |
| **Community task format** | BIG-bench | ✅ |
| **Leaderboard** | Open LLM Leaderboard | 🚧 |
| **Memory isolation protocol** | MemoryAgentBench | 🚧 |

## Scoring

AMBench supports four scoring strategies, selectable via `--scoring`:

| Method | Best For | Description |
|--------|----------|-------------|
| `exact` | Easy recall tasks | Checks if expected text appears in response |
| `keyword` | Medium tasks | F1 overlap of keywords between response and expected |
| `llm_judge` | Complex reasoning | LLM-as-judge (like MT-Bench) |
| `auto` (default) | Mixed difficulty | Exact for easy, keyword for medium, judge for hard |

## Cost-Performance Tracking

Unlike most benchmarks, AMBench tracks cost alongside accuracy:

```
Model: gpt-4
Core Score: 87% | Temporal: 72% | Multimodal: 68%
Avg Latency: 340ms | Avg Tokens: 1,247
Cost/Task: $0.0025 | Cost/Full Run: $0.44
```

This makes it possible to find the **best accuracy at a cost the market can bear**.

## Repository Structure

```
ambench/
├── tasks/            # 177 task episodes (27 cells + extended)
├── src/harness.py    # Main evaluation harness
├── scripts/          # validate.py, coverage.py
├── tests/            # 40+ tests
├── docs/             # Specification, gaps, leaderboard
└── task-templates/   # Episode format reference
```

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). We especially welcome:
- Task definitions for underpopulated cells
- Reference implementations of memory systems
- Bug reports and feature requests

## License

MIT — see [LICENSE](LICENSE).

## Citation

```bibtex
@misc{weiss2026ambench,
  author = {Weiß, Tobias},
  title = {AMBench: A Unified Benchmark for Agent Memory Systems},
  year = {2026},
  howpublished = {\url{https://github.com/tobias-weiss-ai-xr/agent-memory-bench}},
}
```

## Related

- [Agent Memory Research Dataset](https://github.com/tobias-weiss-ai-xr/agent-memory-research) — 1,049 papers
- [Extended Survey](https://doi.org/10.5281/zenodo.20780690) — Taxonomy this benchmark is based on
