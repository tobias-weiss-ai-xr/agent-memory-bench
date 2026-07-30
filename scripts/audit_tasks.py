#!/usr/bin/env python3
"""Task quality audit for AMBench.

Detects potential issues in task definitions:
- Duplicate queries (from procedural generation)
- Substring query overlaps
- Difficulty-5 with trivial expected answers
- Context length outliers (>3σ from mean)
- Modality-skill mismatches

Outputs JSON report to docs/audit-report.json
"""

import json
import math
import statistics
from pathlib import Path
from collections import Counter, defaultdict


VALID_27_CELLS = {
    f"{func}/{form}/{dyn}"
    for func in ["factual", "experiential", "working"]
    for form in ["token-level", "parametric", "latent"]
    for dyn in ["formation", "evolution", "retrieval"]
}

VALID_EXTENDED_DOMAINS = {"temporal", "multimodal", "security", "multi-agent"}
EXPECTED_MODALITIES = {
    "text",
    "visual",
    "audio",
    "visual_to_text",
    "audio_to_text",
    "text_to_visual",
    "text_to_audio",
    "visual_to_audio",
    "audio_to_visual",
}

SKILL_TO_EXPECTED_MODALITIES = {
    "factual": {"text"},
    "experiential": {"text"},
    "working": {"text"},
    "temporal": {"text"},
    "security": {"text"},
    "multi-agent": {"text"},
    "multimodal": {
        "text",
        "visual",
        "audio",
        "visual_to_text",
        "audio_to_text",
        "text_to_visual",
        "text_to_audio",
        "visual_to_audio",
        "audio_to_visual",
    },
}


def is_expected_modal_match(domain: str, modality: str) -> bool:
    """Check if modality is expected for the given skill domain."""
    expected = SKILL_TO_EXPECTED_MODALITIES.get(domain, set())
    if not expected:
        return True
    if modality not in EXPECTED_MODALITIES:
        return False
    return modality in expected


def is_trivial_expected(expected: list) -> bool:
    """Heuristic: difficulty-5 task with very simple expected answer."""
    if not expected:
        return False
    total_words = sum(len(e.split()) for e in expected)
    # Trivial if few short answers or single numeric/name answer
    if len(expected) == 1 and len(expected[0].split()) <= 3:
        return True
    if len(expected) <= 2 and total_words <= 5:
        return True
    return False


def main():
    task_dir = Path("tasks")
    all_files = sorted(task_dir.rglob("*.yaml"))

    import yaml

    tasks = []
    ctx_lengths = []
    queries = []
    query_to_files = defaultdict(list)

    for fpath in all_files:
        if ".gitkeep" in fpath.name:
            continue
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
            ep = data.get("episode", {})
        except Exception:
            continue

        ep["_file"] = str(fpath)
        tasks.append(ep)
        ctx = ep.get("context", "")
        ctx_lengths.append(len(ctx))
        q = ep.get("query", "").strip()
        queries.append(q)
        query_to_files[q].append(str(fpath))

    # Statistics
    mean_ctx = statistics.mean(ctx_lengths)
    stdev_ctx = statistics.stdev(ctx_lengths)
    upper_bound = mean_ctx + 3 * stdev_ctx
    lower_bound = max(0, mean_ctx - 3 * stdev_ctx)

    # Findings
    findings = {
        "total_tasks": len(tasks),
        "duplicate_queries": [],
        "substring_queries": [],
        "difficulty5_trivial": [],
        "context_outliers": [],
        "modality_mismatches": [],
    }

    # 1. Duplicate queries
    qcounts = Counter(queries)
    for q, cnt in sorted(qcounts.items(), key=lambda x: -x[1]):
        if cnt > 1:
            findings["duplicate_queries"].append(
                {
                    "query": q[:120],
                    "count": cnt,
                    "files": query_to_files[q][:5],
                }
            )

    # 2. Substring queries (min length 20 to avoid noise)
    seen_queries = set(queries)
    substring_pairs = set()
    for q in sorted(seen_queries):
        if len(q) < 20:
            continue
        for other in seen_queries:
            if q != other and other and q in other:
                pair = (q, other)
                if pair not in substring_pairs:
                    substring_pairs.add(pair)
                    findings["substring_queries"].append(
                        {
                            "substring": q[:100],
                            "container": other[:100],
                            "sub_len": len(q),
                            "container_len": len(other),
                        }
                    )

    # 3. Difficulty-5 with trivial expected
    for ep in tasks:
        if ep.get("difficulty") == 5:
            expected = ep.get("expected", [])
            ctx_len = len(ep.get("context", ""))
            if is_trivial_expected(expected):
                findings["difficulty5_trivial"].append(
                    {
                        "file": ep["_file"],
                        "query": ep.get("query", "")[:80],
                        "expected": expected,
                        "context_length": ctx_len,
                    }
                )

    # 4. Context length outliers
    for ep in tasks:
        ctx = ep.get("context", "")
        clen = len(ctx)
        if clen > upper_bound or clen < lower_bound:
            findings["context_outliers"].append(
                {
                    "file": ep["_file"],
                    "context_length": clen,
                    "mean": round(mean_ctx, 1),
                    "stdev": round(stdev_ctx, 1),
                    "direction": "long" if clen > upper_bound else "short",
                }
            )

    # 5. Modality-skill mismatches
    for ep in tasks:
        cell = ep.get("cell", "")
        modality = ep.get("modality", "")
        if not cell or not modality:
            continue
        parts = cell.split("/")
        domain = parts[0]
        if not is_expected_modal_match(domain, modality):
            findings["modality_mismatches"].append(
                {
                    "file": ep["_file"],
                    "cell": cell,
                    "modality": modality,
                    "expected_modalities": sorted(
                        SKILL_TO_EXPECTED_MODALITIES.get(domain, set())
                    ),
                }
            )

    # Summary
    summary = {
        "total_findings": sum(
            len(v) for k, v in findings.items() if isinstance(v, list)
        ),
        "duplicate_query_groups": len(findings["duplicate_queries"]),
        "substring_query_pairs": len(findings["substring_queries"]),
        "difficulty5_trivial_count": len(findings["difficulty5_trivial"]),
        "context_outliers_count": len(findings["context_outliers"]),
        "modality_mismatch_count": len(findings["modality_mismatches"]),
        "upper_context_bound": round(upper_bound, 1),
        "lower_context_bound": round(lower_bound, 1),
        "mean_context_length": round(mean_ctx, 1),
        "context_stdev": round(stdev_ctx, 1),
    }

    report = {
        "summary": summary,
        "findings": findings,
    }

    output_path = Path("docs/audit-report.json")
    output_path.write_text(json.dumps(report, indent=2))
    print(f"Audit report written to {output_path}")
    print(f"Summary: {json.dumps(summary, indent=2)}")
    print()
    print(f"Duplicate query groups: {summary['duplicate_query_groups']}")
    print(f"Substring query pairs: {summary['substring_query_pairs']}")
    print(f"Difficulty-5 with trivial expected: {summary['difficulty5_trivial_count']}")
    print(f"Context length outliers: {summary['context_outliers_count']}")
    print(f"Modality mismatches: {summary['modality_mismatch_count']}")

    # Print remaining notes
    remaining_d5 = findings["difficulty5_trivial"]
    if remaining_d5:
        print("\nRemaining difficulty-5 tasks flagged as trivial (review needed):")
        for d in remaining_d5:
            print(f"  {d['file']}: expected={d['expected']}")
        print(
            "  (Manual review: vcl-005 is needle-in-haystack, T-BITEMP-001 is bi-temporal reasoning)"
        )
    print("\nAudit complete. Report written to docs/audit-report.json")


if __name__ == "__main__":
    import sys

    main()
