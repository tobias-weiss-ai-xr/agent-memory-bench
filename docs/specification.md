# AMBench Specification v0.1

**Agent Memory Benchmark — Unified Evaluation Framework**

---

## 1. Design Principles

1. **Full taxonomy coverage** — Generate evaluation questions for each of the 27 taxonomy cells, with question counts proportional to the relative importance of each cell.
2. **Temporal reasoning** — Include questions requiring decay-aware queries, bi-temporal point-in-time queries, and trend detection.
3. **Multimodal evaluation** — Include vision, audio, and text modalities, with both within-modality and cross-modality retrieval tasks.
4. **Biological inspiration assessment** — Metrics that distinguish between cognitive-metaphor, neuro-inspired, and brain-architecture systems.
5. **Long-horizon evaluation** — Support for at least 10⁴ interaction turns with controlled information injection, novelty decay, and information overlap.
6. **Memory-specific isolation** — Control for the agent's reasoning ability by comparing performance with and without the memory system under test.

## 2. Taxonomy Coverage

### 2.1 The 27 Cells

The benchmark covers all combinations of:

| Axis | Levels |
|------|--------|
| **Function** | Factual, Experiential, Working |
| **Form** | Token-level, Parametric, Latent |
| **Dynamics** | Formation, Evolution, Retrieval |

### 2.2 The 3 Extended Dimensions

| Dimension | Levels |
|-----------|--------|
| **Temporal Dynamics** | None, Decay-based, Consolidation-based, Bi-temporal |
| **Modality** | Text-only, Multimodal-in, Multimodal-out, Full-multimodal |
| **Biological Inspiration** | None, Cognitive-metaphor, Neuro-inspired, Brain-architecture |

### 2.3 Coverage Requirements

Each of the 27 cells must have at least **20 evaluation questions** spanning:
- 5 formation scenarios
- 5 evolution scenarios
- 5 retrieval scenarios
- 5 cross-cell scenarios

For the extended dimensions:
- Temporal Dynamics: minimum 50 questions per level
- Modality: minimum 30 questions per modality path
- Biological Inspiration: minimum 20 questions per level

## 3. Task Categories

### 3.1 Core Tasks

| Task ID | Name | Cells | Description |
|---------|------|-------|-------------|
| F-T-F | Factual Token Formation | factual/token-level/formation | Store factual information from text |
| F-T-E | Factual Token Evolution | factual/token-level/evolution | Update/consolidate stored facts |
| F-T-R | Factual Token Retrieval | factual/token-level/retrieval | Retrieve stored facts by query |
| E-T-F | Experiential Token Formation | experiential/token-level/formation | Store episodic experiences |
| ... | *(27 total)* | ... | ... |

### 3.2 Temporal Tasks

| Task ID | Name | Description |
|---------|------|-------------|
| T-DECAY | Decay-based forgetting | Memory importance decays over time; query after delays |
| T-CONSOL | Sleep consolidation | Offline memory reorganization between sessions |
| T-BITEMP | Bi-temporal reasoning | Query valid-time vs transaction-time conflicts |
| T-TREND | Trend detection | "How has X changed over the last N sessions?" |

### 3.3 Multimodal Tasks

| Task ID | Name | Modality Path |
|---------|------|---------------|
| M-TEXT | Text-only memory | Text in → text out |
| M-VISUAL | Visual memory | Image in → text/description out |
| M-AUDIO | Audio memory | Audio in → text/description out |
| M-CROSS | Cross-modal retrieval | Image in → retrieve related text (and vice versa) |
| M-EMBODIED | Embodied memory | Vision + proprioception → action retrieval |

### 3.4 Biological Inspiration Metrics

| Metric | What It Measures |
|--------|-----------------|
| B-NONE | No biological inspiration (engineering baseline) |
| B-METAPHOR | Uses cognitive concepts loosely (e.g., "episodic memory") |
| B-NEURO | Models specific neural mechanisms (e.g., forgetting curves, gating) |
| B-BRAIN | Implements computational model of brain subsystem |

## 4. Evaluation Protocol

### 4.1 Session Structure

```
Session 0: Information injection (seed facts/experiences)
Session 1: Query round (N questions) + new information
Session 2: Query round + new information + consolidation trigger
...
Session K: Final query round (all 27 cells)

Interleaved:
- Decay windows (query after 1h, 24h, 7d of simulated time)
- Consolidation triggers (sleep, batch reprocessing)
- Modality switches (text → image → audio → cross-modal)
```

### 4.2 Metrics

| Metric | Formula |
|--------|---------|
| **Memory Accuracy** | Correct retrievals / total queries |
| **Temporal Precision** | Correct time-attributed retrievals / temporal queries |
| **Cross-Modal Transfer** | Cross-modal correct / within-modal correct |
| **Consolidation Gain** | Post-consolidation accuracy / pre-consolidation accuracy |
| **Forgetting Rate** | Decay in accuracy over time windows |
| **Memory-Specific Score** | Accuracy(with memory) − Accuracy(without memory) |
| **Budget Efficiency** | Accuracy per token / storage unit |

### 4.3 Isolation Design

Following MemoryAgentBench:
```
Score_memory = Score_agent_with_memory − Score_agent_without_memory
```

Each task is run twice: once with the memory system active, once with a no-memory baseline. The difference isolates the memory system's contribution.

## 5. Data Format

### 5.1 Episode Format

```yaml
episode:
  id: "F-T-F-001"
  cell: "factual/token-level/formation"
  turn: 0
  modality: "text"
  input: "The user's name is Alice and they prefer vegetarian food."
  expected: ["Alice", "vegetarian"]
  query: "What is the user's name and dietary preference?"
  distractors: ["Bob", "vegan", "pescatarian"]
```

### 5.2 Temporal Episode

```yaml
episode:
  id: "T-BITEMP-001"
  cell: "working/latent/bi-temporal"
  turn: 5
  modality: "text"
  timeline:
    - time: "2026-01-15"
      fact: "User lives in Berlin"
      transaction_time: "2026-01-15"
    - time: "2026-06-01"
      fact: "User moved to Munich"
      transaction_time: "2026-06-01"
  query: "Where did the user live in March 2026?"
  expected: "Berlin"
  reasoning: "Valid time query — the move to Munich occurred in June, so in March the user was still in Berlin"
```

### 5.3 Multimodal Episode

```yaml
episode:
  id: "M-CROSS-001"
  cell: "factual/latent/cross-modal"
  turn: 3
  modality: "visual_to_text"
  input: "<image of a golden retriever playing fetch>"
  storage_prompt: "Describe what you see in detail and store it."
  query: "What breed of dog was playing fetch?"
  expected: "golden retriever"
  distraction: "<image of a border collie>"
```

## 6. Reference Implementation Roadmap

| Phase | Milestone | Timeline |
|-------|-----------|----------|
| 0 | Specification draft | ✅ Complete |
| 1 | Cell-level task definitions (all 27) | Q3 2026 |
| 2 | Temporal task suite | Q3 2026 |
| 3 | Multimodal task suite | Q4 2026 |
| 4 | Reference evaluator (Python) | Q4 2026 |
| 5 | Leaderboard infrastructure | Q1 2027 |
| 6 | Community review and iteration | Ongoing |

## 7. References

- Liu et al. (2026). Memory in the Age of AI Agents: A Survey. arXiv:2512.13564.
- Weiß, T. (2026). Agent Memory Research in 2026: A Data-Driven Survey and Extended Taxonomy. Zenodo. https://doi.org/10.5281/zenodo.20780690
- Tan et al. (2025). MemBench: A Comprehensive Benchmark for Agent Memory.
- Wu et al. (2024). LongMemEval: Benchmarking Long-Term Interactive Memory.
- Unknown (2025). MemoryAgentBench: Separating Memory from Reasoning.
