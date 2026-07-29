<p align="center">
  <h1 align="center">AMBench</h1>
  <p align="center"><strong>Unified Benchmark for Agent Memory Systems</strong></p>
  <p align="center">
    <a href="https://github.com/tobias-weiss-ai-xr/agent-memory-bench"><img src="https://img.shields.io/badge/GitHub-181717.svg?logo=github" alt="GitHub"></a>
    <a href="https://gitlab.com/tbsweiss/agent-memory-bench"><img src="https://img.shields.io/badge/GitLab-2185D0.svg?logo=gitlab" alt="GitLab"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/agent-memory-bench/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/tobias-weiss-ai-xr/agent-memory-bench/validate.yml?label=CI&logo=github" alt="CI"></a>
    <a href="docs/leaderboard.md"><img src="https://img.shields.io/badge/Leaderboard-Open-004D40.svg" alt="Leaderboard"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/agentic-vr-research"><img src="https://img.shields.io/badge/Agentic_VR_Survey-004D40.svg" alt="Agentic VR Survey"></a>
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
| [Vectorize AMB](https://github.com/vectorize-io/agent-memory-benchmark) | ~5 scenarios | No taxonomy — covers practical scenarios but not the 27-cell design space |
| **AMBench** | **27 + 4 ext.** | **Full coverage** |

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

## Why AMBench Over Alternatives

Vectorize's [AMB](https://github.com/vectorize-io/agent-memory-benchmark) is the closest existing benchmark — both focus on agent memory evaluation with cost tracking and open results. However, AMBench differs in key ways:

| Dimension | Vectorize AMB | AMBench |
|-----------|--------------|---------|
| **Coverage** | ~5 practical scenarios (beam, lifebench, locomo, longmemeval, personamem) | 27 taxonomy cells + 4 extended dimensions (177 tasks) |
| **Scoring** | Single LLM-as-judge (Gemini) | 4 strategies (exact, keyword, LLM-judge, auto) |
| **Vendor lock-in** | Gemini-only for generation + judging | Any OpenAI-compatible API via LiteLLM |
| **Task validation** | None | 44+ tests, YAML schema check, ID collision detection, coverage reporting |
| **Memory isolation** | Not supported | Dual-run protocol isolates memory from reasoning |
| **Taxonomic coverage** | No taxonomy — datasets target specific use cases | Full 3×3×3 form×function×dynamics design space |
| **Extended dimensions** | No | Temporal (decay, consolidation, bi-temporal), multimodal, security, multi-agent |
| **LLM dependency** | Answer generation and judging both use Gemini | Model-agnostic — swap providers without changing tasks |

We benchmark memory architectures, not just memory providers. A complete memory system combines storage, retrieval, reasoning, and tool use — AMBench evaluates all of it across the full design space.

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

## Related Projects

- [Agent Memory Research Survey](https://github.com/tobias-weiss-ai-xr/agent-memory-research) — Living survey of 1,047 agent memory papers
- [Agentic VR Survey](https://github.com/tobias-weiss-ai-xr/agentic-vr-research) — Living survey of 4,942 agentic AI in VR papers
- [Extended Survey](https://doi.org/10.5281/zenodo.20780690) — Taxonomy this benchmark is based on
