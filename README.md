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
    <a href="https://github.com/tobias-weiss-ai-xr/agent-skill-research"><img src="https://img.shields.io/badge/Skill_Survey-004D40.svg" alt="Skill Survey"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/agent-skill-bench"><img src="https://img.shields.io/badge/Skill_Bench-004D40.svg" alt="Skill Bench"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/agent-learning-research"><img src="https://img.shields.io/badge/Learning_Survey-004D40.svg?logo=github" alt="Learning Survey"></a>
    <a href="https://github.com/tobias-weiss-ai-xr/learning-research"><img src="https://img.shields.io/badge/Learning_Research-004D40.svg?logo=github" alt="Learning Research"></a>
    <a href="docker/"><img src="https://img.shields.io/badge/Reproducible-Docker-2496ED.svg?logo=docker" alt="Reproducible"></a>
  </p>
</p>

---

## The Problem

The [agent memory research landscape](https://github.com/tobias-weiss-ai-xr/agent-memory-research) has grown to **1,049 papers** with **80+ distinct benchmarks** — yet **no single benchmark spans more than 11 of 27 taxonomy cells**.

| Benchmark | Coverage | What's Missing |
|-----------|:--------:|----------------|
| LoCoMo | 1 cell | Temporal, multimodal, experiential, working |
| LongMemEval | 1 cell | Everything except factual/token-level |
| MemBench | ~11 cells | Experiential, temporal, multimodal |
| [Vectorize AMB](https://github.com/vectorize-io/agent-memory-benchmark) | 7 datasets (no taxonomy) | No systematic coverage — tests specific scenarios, not the design space |
| **AMBench** | **27 cells + 4 ext.** | **Full taxonomic coverage** |

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

## Related Work

The agent memory evaluation landscape has grown rapidly alongside the agent AI field. Our [Agent Memory Survey](https://github.com/tobias-weiss-ai-xr/agent-memory-research) identifies **80+ benchmark-focused papers**, yet no existing benchmark covers more than 11 of the 27 taxonomy cells. Below we survey the major approaches, grouped by evaluation philosophy.

### Memory-Provider Benchmarks

**[Vectorize AMB](https://github.com/vectorize-io/agent-memory-benchmark)** (64 ★, 26 forks) is the closest existing benchmark to AMBench in spirit — both are open, track cost alongside accuracy, and aim to standardize evaluation. However, they evaluate fundamentally different things:

| Dimension | Vectorize AMB | AMBench |
|-----------|--------------|---------|
| **What it tests** | Memory providers (RAG backends: BM25, Mem0, Hindsight, Qdrant, Cognee, Mastra) | Agent memory architectures (reasoning + retrieval combined) |
| **Coverage** | 7 datasets (BEAM, LifeBench, LoCoMo, LongMemEval, MemBench, MemSim, PersonaMem) | 177 hand-crafted tasks across 27 taxonomy cells + 4 extended dimensions |
| **Taxonomy** | None — datasets target specific use cases | Full 3×3×3 form×function×dynamics design space |
| **Scoring** | Single LLM-as-judge (Gemini) + MCQ | 4 strategies — exact, keyword F1, LLM-as-judge, auto-select (difficulty-adaptive) |
| **LLM dependency** | Gemini-only (generation + judging) | Any OpenAI-compatible API via LiteLLM |
| **Task validation** | None | 44+ tests, YAML schema checker, ID collision detection |
| **Memory isolation** | Not supported | Dual-run protocol (± memory) |
| **Extended scenarios** | No | Temporal, multimodal, security, multi-agent |
| **Dependencies** | 16 packages | 3 packages (pyyaml, openai, pytest) |
| **Live leaderboard** | ✅ agentmemorybenchmark.ai | 🚧 In development |

Vectorize AMB is a **memory-provider benchmark**: it answers *"Which RAG backend has the best recall for long-context Q&A?"* by wrapping existing datasets into a unified harness with a Gemini judge. AMBench is a **memory-capability benchmark**: it answers *"How well does my agent system remember across all types of memory — factual recall, experiential episodes, working memory — under different dynamics and extended conditions?"* These are complementary — run both for a complete picture.

### Dataset-Based Benchmarks

**LoCoMo (Long Context Memory).** The most widely-reported benchmark in the literature (adopted by Mem0, Memento, and others). It evaluates long-context conversational memory across 10 multi-session dialogues (~1,500–2,000 questions) with controlled information density. **Coverage:** 1 cell (Factual/Token-level). No temporal, multimodal, experiential, or working memory evaluation.

**LongMemEval** (ICLR 2025, [arXiv:2410.10813](https://arxiv.org/abs/2410.10813)). The first dedicated benchmark for long-term interactive memory in chat assistants — 500 QA pairs across 5 categories (personal info, interests, events, interactions, conversation history). Its V2 extension adds web agent scenarios touching Experiential memory. **Coverage:** 1 cell (Factual/Token-level), V2 adds partial Experiential/Token-level.

**BEAM (Benchmark for Agent Memory).** A technical-memory stress benchmark with 700 questions at 1M-token scale. Tests whether memory systems retain facts across very large interaction histories (100K–10M tokens). **Coverage:** Factual/Token-level — stress testing at scale, not taxonomic coverage.

### Governance & Security Benchmarks

**[InMind](https://arxiv.org/abs/2607.24368)** (July 2026). A 125-task benchmark exposing the **implicit-association blind spot**: memory systems collapse from 84% accuracy (memory in context) to 14.4% (memory must be retrieved) when needed facts don't lexically resemble the query. Uses paired controls to isolate three confounds (fact never stored, model lacks bridging knowledge, fact stored but never surfaced). **Coverage:** Targets Factual memory, but the blind-spot phenomenon cuts across all cells.

**[GateMem](https://github.com/rzhub/GateMem)** (192 ★, [arXiv:2606.18829](https://arxiv.org/abs/2606.18829)). Evaluates **memory governance** in multi-principal shared-memory agents: can a single memory system serve multiple users while (a) answering correctly for authorized requests, (b) avoiding privacy leakage, and (c) reliably forgetting on request? 91 multi-party episodes across 4 domains with 2,218 hidden checkpoints. Introduces the **Memory Governance Score (MGS)** = Utility × (1 − Access-Control Violation Rate) × (1 − Active-Forgetting Failure Rate). **Coverage:** Cross-cutting — governance is orthogonal to the memory taxonomy.

### Agent-Capability Benchmarks

**[MemBench](https://arxiv.org/abs/2502.13701)**. Proposes evaluation across factual accuracy, temporal consistency, personalization, and instruction following using multi-turn interaction sessions with controlled information injection. **Coverage:** 11 cells (Factual + Working, partial Latent). Does not cover Experiential, temporal, or multimodal dimensions.

**[MemoryAgentBench](https://arxiv.org/abs/2502.13701)**. Introduces **memory isolation** through incremental multi-turn interactions — compares agent performance with and without the memory system to separate memory-specific capability from general LLM reasoning. This design philosophy directly inspired AMBench's dual-run protocol. **Coverage:** 3 cells (Factual/Token-level primary, partial Experiential and Parametric).

**[Veracium](https://github.com/veracium-ai/Veracium)** ([arXiv:2607.21962](https://arxiv.org/abs/2607.21962), July 2026). Inverts the standard evaluation pipeline: generates ground-truth facts with validity intervals **before** rendering any dialogue text, then instantiates questions mechanically from the script. Discovered the **Tenure Crossover** — memory architecture rankings invert with history length (3-week leader vs 9-week leader). ~380 questions, 15 types. **Coverage:** Longitudinal — tests a single architecture's performance trajectory rather than breadth.

### Landscape Summary

| Category | Benchmark | Coverage | Taxonomy? | Scoring | Vendor Lock | Memory Isolation | Key Innovation |
|----------|-----------|:--------:|:---------:|:-------:|:-----------:|:----------------:|----------------|
| **Dataset** | LoCoMo | 1 cell | ❌ | LLM-judge | None | ❌ | Multi-session conversations |
| **Dataset** | LongMemEval | 1 cell | ❌ | LLM-judge | None | ❌ | 5 memory abilities |
| **Dataset** | BEAM | 1 cell | ❌ | Nugget score | None | ❌ | 1M-token stress test |
| **Provider** | Vectorize AMB | 7 datasets | ❌ | Gemini judge | **Gemini** | ❌ | 10+ RAG backends, live leaderboard |
| **Governance** | InMind | 1 cell* | ❌ | LLM-judge | None | ❌ | Implicit-association blind spot |
| **Governance** | GateMem | Cross-cutting | ❌ | MGS | None | ❌ | Multi-principal access control |
| **Capability** | MemBench | ~11 cells | Partial | LLM-judge | None | ❌ | Injection-controlled sessions |
| **Capability** | MemoryAgentBench | 3 cells | ❌ | Accuracy | None | ✅ | Memory isolation protocol |
| **Capability** | Veracium | 1 trajectory | ❌ | LLM-judge | None | ❌ | Ground-truth-first, tenure crossover |
| **Capability** | **AMBench** | **27+4 ext.** | **✅ Full** | **4 strategies** | **None** | **✅** | **Full taxonomic coverage** |

\*InMind targets Factual memory but the phenomenon applies across all cells.

**The gap is clear:** no existing benchmark covers more than 11 of 27 taxonomy cells. None evaluates temporal dynamics, multimodal integration, or security as first-class dimensions. None combines taxonomic breadth with memory isolation, difficulty-adaptive scoring, and cost-performance tracking. AMBench is designed to fill all of these gaps simultaneously.

> **Reproducible evaluation** — All benchmarks run in a containerized environment
> with pinned dependencies and model snapshots. See [CONTRIBUTING.md](CONTRIBUTING.md)
> for one-command eval instructions.

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
| **Memory isolation protocol** | MemoryAgentBench | ✅ |

## 🏗️ Infrastructure

### Memory Isolation Protocol

The memory isolation protocol measures the **marginal contribution** of a memory system by comparing performance with and without memory context. This separates the memory system's contribution from the LLM's raw reasoning ability.

**Dual-Run Evaluation (`--dual-run`):**
- For each task, the harness runs two evaluations:
  - **Baseline run**: Evaluates the task with **empty context** — measures what the LLM can answer from parametric knowledge alone
  - **Memory run**: Evaluates the same task with **full context** — measures the memory-assisted capability
- **Memory contribution** = `memory_score - baseline_score` per task
- The summary reports baseline average, memory average, and average contribution across all tasks

```bash
# Dry-run dual evaluation with mock responses
python src/harness.py --mock --dual-run

# Real evaluation (requires API key)
python src/harness.py --model gpt-4 --dual-run

# With markdown report
python src/harness.py --mock --dual-run --markdown results/dual-run.md

# Resume support: per-run state is tracked independently
python src/harness.py --mock --dual-run --resume
```

**Baseline Reference (`--baseline`):**
- Pre-computed no-memory baseline scores can be loaded for comparison with memory-assisted runs
- Baseline files are stored in `results/baseline/` and contain the `avg_score` from a memory-free evaluation
- The report displays **Memory Isolation Gain** when a baseline is provided

```bash
# Generate a no-memory baseline
python src/harness.py --mock --dual-run --output results/baseline/llm-baseline.json

# Compare a memory-system run against the baseline
python src/harness.py --mock --memory-isolation --baseline results/baseline/llm-baseline.json
```

**Output Structure:** Dual-run JSON reports contain both `baseline` and `memory` sub-reports, a `per_task` breakdown with per-task scores and contributions, and summary metrics (`avg_contribution`, `positive_contributions`, `negative_contributions`).

### Resume Capability

### Docker Sandboxing

Run the harness in a containerized environment:

```
docker compose -f docker/docker-compose.yml up
```

The `--docker` flag prints setup instructions. Results are written to `results/` on the host.

### Hidden Annotation Fields

Task YAML files may include an optional `hidden` section with `expected_action`, `judge_spec`, and `leak_targets`. These fields are validated by `scripts/validate.py` but are **excluded from agent input** — they never appear in the prompt sent to the evaluated model. The validator warns when hidden fields are detected.

### Leaderboard PR Submission

Submit evaluation results via pull request. Add a JSON file to `leaderboard/` following `leaderboard/template.json`:

```json
{"system": "...", "model": "...", "scores": {"overall": 0.0, "factual": 0.0, "experiential": 0.0, "working": 0.0}, "date": "YYYY-MM-DD"}
```

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
├── task-templates/   # Episode format reference
├── docker/           # Docker sandboxing (Dockerfile, compose)
├── leaderboard/      # PR-based leaderboard submissions
└── results/          # Resume state and evaluation outputs
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

### Similar Benchmarks

- **[GoodAI LTM Benchmark](https://github.com/GoodAI/goodai-ltm-benchmark)** (88 ⭐) — Long-term memory and continual learning benchmark for LLM agents. Ships with agent harness and evaluator. Closest in scope to AMBench.
- **[GateMem](https://github.com/rzhub/GateMem)** (192 ⭐) — Memory governance benchmark for multi-principal shared-memory agents. Unique focus on access control, privacy leakage, and active forgetting.
- **[HaluMem](https://github.com/MemTensor/HaluMem)** (148 ⭐) — Operation-level hallucination evaluation for agent memory systems. Probes retrieval errors, stale context, and memory-induced hallucinations.
- **[AgentBench](https://github.com/THUDM/AgentBench)** (3,614 ⭐, ICLR 2024) — 8-environment interactive benchmark evaluating LLMs as agents. Gold standard for general agent evaluation.
- **[OSWorld](https://github.com/xlang-ai/OSWorld)** (3,046 ⭐, NeurIPS 2024) — 369 open-ended real-computer tasks in live VMs. Reference for real-environment task trace design.
- **[tau2-bench](https://github.com/sierra-research/tau2-bench)** (1,689 ⭐) — Tool-agent-user interaction benchmark with dual-control tasks. Strong multi-turn, stateful evaluation design.
- **[SWE-bench](https://github.com/SWE-bench/SWE-bench)** (5,515 ⭐) — 2,294 real GitHub issue resolution tasks with Docker-based harness. Reference architecture for sandboxed eval and leaderboard design.

### Sibling Repositories

- [Agent Memory Research Survey](https://github.com/tobias-weiss-ai-xr/agent-memory-research) — Living survey of 1,047 agent memory papers
- [Agentic VR Survey](https://github.com/tobias-weiss-ai-xr/agentic-vr-research) — Living survey of 4,942 agentic AI in VR papers
- [Skill Survey](https://github.com/tobias-weiss-ai-xr/agent-skill-research) — Living survey of AI agent skills (tool use, planning, reasoning, code generation, etc.)
- [Skill Bench](https://github.com/tobias-weiss-ai-xr/agent-skill-bench) — Unified benchmark for evaluating AI agent skills
- [Agent Learning Research](https://github.com/tobias-weiss-ai-xr/agent-learning-research) — Survey of learning in AI agents
- [Learning Research](https://github.com/tobias-weiss-ai-xr/learning-research) — Interdisciplinary survey of learning across all disciplines
- [Extended Survey](https://doi.org/10.5281/zenodo.20780690) — Taxonomy this benchmark is based on
