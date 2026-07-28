# Biological Inspiration Metrics

**How to classify and evaluate the biological fidelity of agent memory systems.**

---

## The 4-Level Scale

| Level | Label | Definition | Example Systems |
|-------|-------|------------|-----------------|
| B0 | None | No biological inspiration. Purely engineering-driven design. | Mem0, MemGPT, most RAG systems |
| B1 | Cognitive-metaphor | Uses high-level cognitive concepts as loose metaphors without detailed biological fidelity. | Most experiential memory systems, reflection-based agents |
| B2 | Neuro-inspired | Explicitly models specific neuroscientific mechanisms (forgetting curves, hippocampal indexing, synaptic gating) but does not attempt full biological fidelity. | HippoRAG, FadeMem, CraniMem |
| B3 | Brain-architecture | Implements a detailed computational model of a brain subsystem with multiple interacting regions or cell types. | SCM (sleep consolidation), Human-Inspired Memory Architecture, XMem (Atkinson-Shiffrin) |

## Evaluation Protocol

### Step 1: System Classification

Evaluate the system documentation / paper against these criteria:

| Criterion | B0 | B1 | B2 | B3 |
|-----------|:--:|:--:|:--:|:--:|
| Uses memory terminology (episodic, semantic) | Maybe | Yes | Yes | Yes |
| References specific brain regions | No | Metaphor only | Yes (1-2 regions) | Yes (multiple regions) |
| Models neural mechanisms explicitly | No | No | Yes | Yes |
| Implements computational model of neural process | No | No | Partial | Full |
| Cites cognitive neuroscience literature | No | Minimal | Yes | Extensively |
| Biological plausibility discussed | No | No | Sometimes | Yes |

### Step 2: Functional Fidelity Assessment

For systems classified as B2 or B3, evaluate functional fidelity:

| Mechanism | Human Memory | B2 Approximation | B3 Approximation |
|-----------|-------------|------------------|------------------|
| Forgetting | Ebbinghaus curve, interference-based | Exponential decay function | Multi-factor decay with interference |
| Consolidation | Hippocampal replay during sleep | Periodic reprocessing | NREM/REM sleep cycle simulation |
| Retrieval | Pattern completion, cue-based | Semantic similarity search | Dual-process (familiarity + recollection) |
| Encoding | Experience-dependent plasticity | Importance-weighted storage | Multi-factor salience (recency, frequency, emotional valence) |

### Step 3: Performance Correlation

Measure whether higher biological fidelity correlates with:
- Better long-term retention (decay resistance)
- Better cross-modal transfer
- Better handling of contradictory information
- Lower storage requirements
- Higher computational cost

This is the empirical question the benchmark is designed to answer.

## Test Suite

| Test ID | Description | Measures |
|---------|-------------|----------|
| B-FORGET | Retention after increasing time intervals | Decay curve shape match to human data |
| B-CONSOL | Offline consolidation benefit | Pre vs post-sleep accuracy gain |
| B-INTERF | Proactive and retroactive interference | Accuracy drop when similar memories compete |
| B-CUEREC | Cue-dependent recall | Recall accuracy with partial vs full cues |
| B-SOURCE | Source memory accuracy | Recall of when/where a fact was learned |
