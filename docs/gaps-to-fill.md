# AMBench: Gaps to Fill

**What exists, what's missing, and what's most urgent.**

---

## Current Coverage Status (2026-07-28)

| Area | Tasks | Status |
|------|:-----:|:------:|
| Factual/Token-level | 5 | 🚧 Needs 15 more per cell |
| Working/Token-level | 6 | 🚧 Needs 14 more per cell |
| Experiential/Token-level | 4 | 🚧 Needs 16 more |
| Temporal tasks | 5 | 🚧 Needs 45 more |
| Multimodal tasks | 4 | 🚧 Needs 26 more |
| Sparse cells | 4 | 🚧 Critical — most important |
| **Total** | **28** | ❌ Need ~540 total |

---

## Priority Gap Analysis

### Tier 1: Critical Gaps (blockers for unified evaluation)

| Gap | Why It Matters | What's Needed |
|-----|----------------|---------------|
| **No cross-modal benchmark** | No way to measure if vision memory can be retrieved via text | 30 cross-modal episodes |
| **No biological inspiration metric** | No way to distinguish cognitive-metaphor from brain-architecture systems | 4-level classification rubric + 20 test cases |
| **No memory isolation protocol implementation** | Without it, you can't separate memory from reasoning | Reference implementation of dual-run evaluation |
| **No multi-agent memory tasks** | 120+ papers on multi-agent systems but zero shared-memory benchmarks | 20 multi-agent episodes |
| **No poisoning/adversarial tasks** | 120+ security papers but no standard adversarial eval | 20 adversarial episodes |

### Tier 2: High Priority (essential for release)

| Gap | Why It Matters | What's Needed |
|-----|----------------|---------------|
| **Working/Parametric empty** | Only 3 papers in this cell, no benchmark coverage to drive progress | 20 episodes |
| **Experiential/Parametric sparse** | 11 papers, second-sparsest cell | 20 episodes |
| **Experiential/Latent sparse** | 15 papers, but includes most neuro-inspired work (SCM, All-Mem) | 20 episodes |
| **Temporal reasoning tasks** | No dedicated temporal benchmark exists at all | 50 episodes across decay, consolidation, bi-temporal |
| **Long-horizon (>10^4 turns)** | No benchmark tests multi-year deployment stability | 10 long-horizon scenarios |

### Tier 3: Foundation (needed for basic functionality)

| Gap | Why It Matters |
|-----|----------------|
| Factual/Latent tasks | 30 papers, no dedicated evaluation |
| Factual/Parametric tasks | 20 papers, growing cell |
| Working/Latent tasks | 55 papers, 3.0x growth |
| Automated scoring pipeline | Need to standardize answer comparison |
| Leaderboard infrastructure | Need somewhere to publish results |

---

## What's Uniquely Hard

### 1. Latent Memory Evaluation
Latent memories are hidden states — you can't query them directly like token stores. Evaluation must use behavioral probes: give the agent a task that *requires* the latent memory and measure if behavior changes.

**Solution:** Behavioral probe tasks where the correct action is impossible without the latent memory.

### 2. Parametric Memory Evaluation
Parametric memories require weight updates. Evaluation must include a training/adaptation phase before the query phase, and must account for compute cost.

**Solution:** Two-phase episodes (adaptation + query) with compute cost tracking.

### 3. Temporal Ground Truth
Temporal evaluation requires controlled simulation of time. Real-world temporal benchmarks are impractical (you can't wait 90 days for a decay test).

**Solution:** Simulated time with explicit timestamps. The memory system gets timestamped events and must respond to time-relative queries.

### 4. Multimodal Ground Truth
Multimodal evaluation requires paired data: the same fact expressed in text, image, and audio formats.

**Solution:** Build a paired multimodal dataset where each fact exists in 2-3 modalities.

---

## How to Fill These Gaps

### Quick Wins (can be done in hours)
- Working/Token-level tasks (15 more) — easiest cell, lots of scenarios
- Factual/Token-level tasks (15 more) — most well-understood cell
- Decay tasks (10 more) — just vary the time window and fact type

### Medium Effort (days)
- Temporal consolidation tasks (10 more) — need multi-session narratives
- Multimodal visual tasks (10 more) — need scene descriptions
- Bi-temporal tasks (10 more) — need timeline construction

### Long-term (weeks)
- Parametric cell tasks — need understanding of fine-tuning/adaptation APIs
- Multi-agent tasks — need multi-agent interaction protocols
- Adversarial tasks — need realistic attack scenarios
- Reference evaluator — need full implementation

---

## Timeline to First Release

| Milestone | Tasks Needed | Target |
|-----------|:------------:|:------:|
| Working/Token-level baseline | 20 | Week 1 |
| Factual/Token-level baseline | 20 | Week 1 |
| All token-level cells | 60 | Week 2 |
| Temporal suite | 50 | Week 3 |
| Multimodal suite | 30 | Week 4 |
| Sparse cell suite | 60 | Week 5 |
| Full 27-cell coverage | 540 | Month 3 |
| Evaluator v1 | — | Month 3 |
| Leaderboard launch | — | Month 4 |
