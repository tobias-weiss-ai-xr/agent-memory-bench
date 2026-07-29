# AMBench Documentation

**Agent Memory Benchmark — Unified Evaluation Framework**

---

## Getting Started

| Document | Description |
|----------|-------------|
| [README](../README.md) | Project overview, badges, quick start |
| [Getting Started Guide](getting-started.md) | Install, configure, run your first evaluation |

## Specification

| Document | Description |
|----------|-------------|
| [Specification](specification.md) | Full benchmark specification (27 cells, evaluation protocol, metrics) |
| [Taxonomy Coverage Matrix](coverage-matrix.md) | Live coverage tracker with current task counts |
| [Biological Inspiration Metrics](biological-inspiration-metrics.md) | 4-level classification for bio-inspired memory systems |

## Gap Analysis

| Document | Description |
|----------|-------------|
| [Gaps to Fill](gaps-to-fill.md) | Priority-ranked gaps requiring community contributions |
| [Extended Vision](vision-extended.md) | Why AMBench must keep extending until a cost-performance champion emerges |

## Development

| Document | Description |
|----------|-------------|
| [Contributing](../CONTRIBUTING.md) | How to add tasks, report bugs, implement features |
| [Test Harness](../src/harness.py) | Python CLI for running evaluations against LLM APIs |

## Repository Structure

```
ambench/
├── tasks/                    # Task episodes organized by taxonomy cell
│   ├── factual/
│   │   ├── token-level/
│   │   ├── parametric/
│   │   └── latent/
│   ├── experiential/
│   │   └── ...
│   ├── working/
│   │   └── ...
│   ├── temporal/             # Extended: temporal dynamics
│   ├── multimodal/           # Extended: multi-modality
│   ├── security/             # Extended: adversarial robustness
│   └── multi-agent/          # Extended: shared memory
├── src/
│   ├── harness.py            # Main evaluation harness
│   └── evaluator.py          # Deprecated (delegates to harness)
├── scripts/
│   ├── validate.py           # YAML task validator
│   └── coverage.py           # Coverage report generator
├── tests/                    # 40+ tests
├── docs/                     # Documentation
└── task-templates/           # Episode format reference
```
