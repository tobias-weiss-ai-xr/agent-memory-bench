# AMBench Taxonomy Coverage Matrix

**Goal:** Every cell must have ≥20 evaluation questions.

## Legend
- ✅ = ≥20 questions defined
- 🚧 = 5–19 questions defined
- ❌ = <5 questions defined

---

## 1. Core Taxonomy (Forms × Functions × Dynamics)

| Function | Form | Formation | Evolution | Retrieval | Total |
|----------|------|:---------:|:---------:|:---------:|:-----:|
| **Factual** | Token-level | 🚧 | 🚧 | 🚧 | 0/60 |
| **Factual** | Parametric | ❌ | ❌ | ❌ | 0/60 |
| **Factual** | Latent | ❌ | ❌ | ❌ | 0/60 |
| **Experiential** | Token-level | ❌ | ❌ | ❌ | 0/60 |
| **Experiential** | Parametric | ❌ | ❌ | ❌ | 0/60 |
| **Experiential** | Latent | ❌ | ❌ | ❌ | 0/60 |
| **Working** | Token-level | 🚧 | 🚧 | 🚧 | 0/60 |
| **Working** | Parametric | ❌ | ❌ | ❌ | 0/60 |
| **Working** | Latent | ❌ | ❌ | ❌ | 0/60 |
| | | **0/180** | **0/180** | **0/180** | **0/540** |

## 2. Extended Dimensions

### Temporal Dynamics

| Level | Questions | Status |
|-------|:---------:|:------:|
| None | 0/50 | ❌ |
| Decay-based | 0/50 | ❌ |
| Consolidation-based | 0/50 | ❌ |
| Bi-temporal | 0/50 | ❌ |

### Modality

| Path | Questions | Status |
|------|:---------:|:------:|
| Text-only | 0/30 | ❌ |
| Multimodal-in (visual) | 0/30 | ❌ |
| Multimodal-in (audio) | 0/30 | ❌ |
| Multimodal-out | 0/30 | ❌ |
| Full-multimodal | 0/30 | ❌ |
| Cross-modal transfer | 0/30 | ❌ |

### Biological Inspiration

| Level | Metrics | Status |
|-------|:-------:|:------:|
| None | 0/20 | ❌ |
| Cognitive-metaphor | 0/20 | ❌ |
| Neuro-inspired | 0/20 | ❌ |
| Brain-architecture | 0/20 | ❌ |

---

## Priority Order

Based on the gap analysis of the 1,049-paper dataset, cells should be filled in this order:

1. **Working/Token-level** (hottest cell, 283 papers, 4.4× growth) — easiest to define tasks for
2. **Factual/Token-level** (largest cell, 456 papers) — baseline every system must pass
3. **Experiential/Token-level** (169 papers, growing fast) — reflection-based systems need this
4. **Working/Latent** (55 papers, 3.0× growth) — latent working memory systems
5. **Temporal tasks** (decay, consolidation, bi-temporal) — highest-impact gap
6. **Multimodal tasks** — second-highest gap
7. **Sparse cells** (Working/Parametric, Experiential/Latent, Experiential/Parametric) — most rewarding for discoverers
8. **Biological inspiration metrics** — long-tail but valuable

## How to Contribute

Pick a cell from the matrix above and define 20 evaluation episodes following the format in [specification.md](specification.md). Submit via pull request.

See the [task-templates/](task-templates/) directory for episode format examples.
