# Beyond Benchmarks: The Hunt for a New Cost-Performance Champion

**Why AMBench must keep extending until the architecture that changes everything emerges.**

---

## 1. Acknowledge the Limitations

Let's be honest about where AMBench stands today:

| Limitation | Impact | Why It Matters |
|------------|--------|----------------|
| **93 of 540 tasks** (17%) | Incomplete coverage | Systems can cherry-pick cells |
| **No evaluator** | Manual testing only | No automated leaderboard |
| **Text-described multimodal** | Not real multimodal data | Can't test true cross-modal systems |
| **No baselines** | No reference points | Can't compare systems objectively |
| **No memory isolation** | Can't separate memory from reasoning | MemoryAgentBench showed this is critical |
| **Human-generated tasks** | Scalability ceiling | Procedural generation needed for 10^4 turns |
| **No cost tracking** | Accuracy-only evaluation | Real-world deployment cares about $/task |

This is not a weakness of the approach — it's an honest reflection of where the field is. Every existing benchmark has the same limitations, just at a smaller scale. The difference is AMBench is designed to *overcome* them, not hide from them.

---

## 2. The Fragmentation Problem Is Worse Than Reported

The paper says "over 80 benchmarks, none spanning more than 3 of 27 cells." Reality is worse:

```
LoCoMo:       █░░░░░░░░░░░░░░░░░░░░░░░░░░  (1 cell, factual/token-level)
LongMemEval:  █░░░░░░░░░░░░░░░░░░░░░░░░░░  (1 cell)
MemBench:     ███░░░░░░░░░░░░░░░░░░░░░░░░  (11 cells, best in class)
MemoryAgent:  ██░░░░░░░░░░░░░░░░░░░░░░░░░  (5 cells)
WorldMemArena:█░░░░░░░░░░░░░░░░░░░░░░░░░░  (3 cells, first in exp/param)
─────────────────────────────────────────────────
AMBench goal: █████████████████████████████  (27 cells)
```

This means **no system today can claim to be the best at agent memory**. Every leaderboard is a local maximum on a narrow capability. The system that wins LoCoMo might fail completely on temporal reasoning or cross-modal retrieval.

---

## 3. The Cost-Performance Frontier Is Where the Real War Is

Accuracy matters. But in production, cost kills:

```
System A: 95% accuracy, $0.50/task → deployable
System B: 97% accuracy, $5.00/task → academic curiosity
System C: 85% accuracy, $0.02/task → mass adoption
```

AMBench must measure:

| Metric | Why |
|--------|-----|
| **Accuracy per cell** | What can the system actually do? |
| **Tokens per query** | How expensive is retrieval? |
| **Storage per fact** | How scalable is it? |
| **Latency p95** | Can it run in real-time? |
| **Training cost** | How much to adapt to new domains? |
| **Memory isolation score** | Is it actually helping or just the LLM being smart? |

The champion we're looking for isn't the one with the highest accuracy — it's the one with the **best accuracy at a cost the market can bear**.

---

## 4. Why Extending Is the Only Path to a Champion

### 4.1 The Field Is Moving Too Fast for Static Benchmarks

| Period | Papers | Key Emergence |
|--------|:------:|---------------|
| Pre-2025 | 58 | Foundational RAG |
| 2025 | 246 | Reflection, experience replay |
| Jan-Jun 2026 | 494 | Token-level working memory explosion |
| **Jul 2026** | **171** | **Security, multimodal, bi-temporal** |

A benchmark frozen today would be obsolete in 3 months. AMBench must be *living* — new cells, new modalities, new adversarial scenarios added continuously.

### 4.2 The Sparse Cells Are Where Breakthroughs Will Come From

| Sparse Cell | Papers | What's Missing |
|-------------|:------:|----------------|
| Working/Parametric | 10 | Runtime weight adaptation—could be the key to truly adaptive agents |
| Experiential/Latent | 15 | Latent representations of subjective experience—closest to human memory |
| Experiential/Parametric | 11 | Learning from experience via weight updates—the RL-meets-memory frontier |

These cells are sparse because they're *hard*. The system that cracks them will have a fundamental advantage. AMBench needs enough tasks in these cells to *measure* that advantage when it arrives.

### 4.3 The Cost Curve Is Steep

Current cost per query for a typical agent memory system:

```
RAG-based:          ~$0.001/query  (token-level, cheap but limited)
Fine-tuned:         ~$0.01/query   (parametric, better but expensive)
Hybrid:             ~$0.005/query  (best of both, still emerging)
Latent-state:       ~$0.0001/query (theoretical, almost no deployed systems)
```

The champion will likely be a hybrid that achieves 95%+ of the best accuracy at <10% of the cost. We can't find it without measuring both dimensions.

---

## 5. The Argument for Relentless Extension

### Why Stop at 27 Cells?

The taxonomy is already showing signs of needing expansion:
- **Multi-agent memory** (120+ papers, 0 dedicated cells)
- **Security-hardened memory** (120+ papers, 0 dedicated cells)
- **Hardware-aware memory** (emerging cluster)
- **Neuromorphic memory** (embryonic cluster)

Every new cell we add now means fewer papers we have to reclassify later.

### Why Target 540 Tasks?

Statistical significance. A system answering 5 questions in a cell might get lucky. 20 questions per cell gives p < 0.05 confidence. 540 total tasks across 27 cells gives a comprehensive picture of a system's capabilities and weaknesses.

### Why Procedural Generation?

Human-generated tasks don't scale to 10^4 turns. We need:
- Template-based task generation (parameterized scenarios)
- Automated difficulty calibration
- Anti-gaming measures (systems will overfit to static benchmarks)
- Continuous freshness (new tasks pushed regularly)

### Why Cost-Performance as the Primary Metric?

Because that's what determines real-world adoption. The system with 92% accuracy at $0.001/task will be deployed over the system with 94% accuracy at $0.05/task. Every time. AMBench must make this visible.

---

## 6. The Target Profile of a Champion System

When a system achieves all of the following, we'll know we've found our champion:

| Criterion | Target | Why |
|-----------|--------|-----|
| 27-cell coverage | ≥90% accuracy in all cells | No blind spots |
| Cell balance | ≤10% variance across cells | Consistent, not cherry-picked |
| Temporal reasoning | ≥85% on decay, consolidation, bi-temporal | Memory that understands time |
| Cross-modal transfer | ≥80% cross-modal retrieval accuracy | Memory that generalizes across senses |
| Forgetting resistance | ≤10% accuracy loss over 90-day simulated window | Memory that lasts |
| Memory isolation | ≥20 point improvement over no-memory baseline | Actually contributing, not just LLM cleverness |
| Cost efficiency | ≤5,000 tokens per query average | Economically viable |
| Storage efficiency | ≤1KB per fact average | Scales to millions of facts |
| Latency | ≤500ms p95 retrieval | Real-time capable |
| Adversarial robustness | ≥80% accuracy under poisoning attack | Trustworthy |

No system today achieves any 3 of these simultaneously. The one that does will define the next era of agent memory.

---

## 7. The Call

AMBench is not a project. It's a *process*.

A process of:
- Adding tasks until no cell has fewer than 20
- Evaluating until a system achieves ≥90% across all 27 cells
- Extending until the taxonomy covers what the field actually needs
- Measuring until cost-performance is as visible as accuracy
- Iterating until the benchmark itself becomes the standard the community rallies around

The benchmark that defines agent memory hasn't been built yet. But the foundation is laid. Every task added, every cell filled, every line of evaluator code written brings us closer to the cost-performance champion that the field desperately needs.

**Extend until a new champion emerges. Then extend some more.**
