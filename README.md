# Agent Memory Benchmark (AMBench)

**A unified evaluation framework for agent memory systems.**

[![GitHub](https://img.shields.io/badge/GitHub-tobias--weiss--ai--xr/agent--memory--bench-181717.svg?logo=github)](https://github.com/tobias-weiss-ai-xr/agent-memory-bench)
[![GitLab](https://img.shields.io/badge/GitLab-graphwiz--ai/agent--memory--bench-2185D0.svg?logo=gitlab)](https://gitlab.com/tbsweiss/agent-memory-bench)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/Specification-coming_soon-b31b1b.svg?logo=arXiv)]()

---

## The Problem

The [agent memory research landscape](https://github.com/tobias-weiss-ai-xr/agent-memory-research) has grown to **1,049 papers** (July 2026) with **over 80 distinct benchmarks** — yet **no single benchmark spans more than 11 of 27 taxonomy cells**. Every benchmark evaluates a narrow slice:

| Benchmark | Cells Covered | Missing |
|-----------|:------------:|---------|
| LoCoMo | 1 | Temporal, multimodal, experiential, working |
| LongMemEval | 1 | Everything except factual/token-level |
| MemBench | ~11 | Experiential, temporal, multimodal |
| MemoryAgentBench | ~5 | Most of working, all of latent |
| Ledger-QA | ~3 | Only experiential/token-level |
| **AMBench (this project)** | **27** | **Nothing — full coverage** |

This fragmentation means:
- **No fair comparison** across memory architectures
- **No temporal reasoning** evaluation (decay, consolidation, bi-temporal)
- **No multimodal memory** standard
- **No biological inspiration** metric
- **No long-horizon** standard (>10⁴ turns)

## The Vision

**AMBench** is a living benchmark specification that:

1. **Covers all 27 taxonomy cells** — Factual / Experiential / Working × Token-level / Parametric / Latent
2. **Evaluates 3 new dimensions** — Temporal Dynamics, Modality, Biological Inspiration
3. **Supports long-horizon evaluation** — up to 10⁴+ interaction turns
4. **Isolates memory from reasoning** — following MemoryAgentBench's design
5. **Is community-driven** — open specification, open data, open leaderboard

## Quick Start

```bash
# Clone the repo
git clone https://github.com/tobias-weiss-ai-xr/agent-memory-bench.git
cd agent-memory-bench

# See the specification
cat docs/specification.md

# View the taxonomy coverage matrix
cat docs/coverage-matrix.md
```

## Status

| Component | Status |
|-----------|:------:|
| Specification | ✅ Draft |
| Taxonomy coverage matrix | ✅ Complete |
| Cell-level task definitions | 🚧 In progress |
| Reference implementation | ❌ Not started |
| Leaderboard | ❌ Not started |
| Community review | ❌ Welcome |

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome:
- Feedback on the specification
- New task proposals for uncovered cells
- Reference implementations
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

- [Agent Memory Research Dataset](https://github.com/tobias-weiss-ai-xr/agent-memory-research) — 1,049 papers on agent memory
- [Extended Survey on Zenodo](https://doi.org/10.5281/zenodo.20780690) — the taxonomy this benchmark is based on
