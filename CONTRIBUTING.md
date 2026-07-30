# Contributing to AMBench

We welcome contributions to the unified agent memory benchmark!

## How to Contribute

### 1. Define Tasks for a Cell

Pick a cell from the [coverage matrix](docs/coverage-matrix.md) and define 20+ evaluation episodes.

Each episode should be a YAML file following the format in [docs/specification.md](docs/specification.md).

Place them in:
```
tasks/<function>/<form>/<dynamics>/episode-NNN.yaml
```

### 2. Propose a New Task Category

Open an issue with your proposal. We're especially interested in:
- Temporal reasoning tasks
- Multimodal tasks
- Cross-modal transfer tasks
- Multi-agent memory tasks

### 3. Implement the Evaluator

We need a reference implementation in Python that:
- Reads the episode YAML files
- Runs the memory system under test
- Computes all metrics
- Outputs a standardized results JSON

### 4. Report a Bug or Gap

Open an issue if you find:
- A taxonomy cell with insufficient coverage
- An ambiguous evaluation episode
- A metric that doesn't capture what it should

## PR Process

1. Fork the repo
2. Create a branch: `git checkout -b feat/my-contribution`
3. Commit your changes
4. Push and open a PR
5. We'll review within 7 days

## Reproducible Evaluation

All evaluations can be run in a containerized environment with pinned dependencies
and model versions for full reproducibility:

```bash
# Build the container
docker compose -f docker/docker-compose.yml build

# Run mock evaluation (no API key needed)
docker compose -f docker/docker-compose.yml run --rm ambench --mock

# Run real evaluation
export OPENAI_API_KEY=sk-...
docker compose -f docker/docker-compose.yml run --rm ambench

# Run with custom model and scoring
export OPENAI_API_KEY=sk-...
export AMBENCH_MODEL=claude-3-5-sonnet-20241022
export AMBENCH_SCORING=llm_judge
docker compose -f docker/docker-compose.yml run --rm ambench
```

## Code of Conduct

Be excellent to each other. This is a scientific infrastructure project — all contributions are valued regardless of seniority.
