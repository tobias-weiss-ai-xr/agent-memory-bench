#!/usr/bin/env python3
"""Procedural task generator for AMBench.

Reads parameter grids from task_grids.py, fills YAML templates,
validates each generated task, and writes to tasks/<cell>/ dirs.

Usage:
    python3 scripts/generate_tasks.py                     # generate for all cells
    python3 scripts/generate_tasks.py --dry-run            # preview only
    python3 scripts/generate_tasks.py --cells security/injection  # specific cell
    python3 scripts/generate_tasks.py --count 10           # generate 10 per cell
"""

import argparse
import sys
from pathlib import Path

import yaml

# Add scripts dir to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))
from task_grids import PARAM_GRIDS

# Import validator
from validate import validate_task


TASKS_DIR = Path(__file__).parent.parent / "tasks"


def _yaml_block(text, indent=4):
    """Format multi-line text as a YAML literal block."""
    lines = text.strip().split("\n")
    if len(lines) == 1:
        return text.strip()
    result = "|\n"
    for line in lines:
        result += " " * indent + line.rstrip() + "\n"
    return result.rstrip("\n")


def _yaml_list(items, indent=2):
    """Format a list as YAML block-style list items."""
    if not items:
        return ""
    lines = []
    for item in items:
        if item is None:
            continue
        lines.append(" " * indent + "- " + str(item))
    return "\n".join(lines)


def _yaml_nested_list(groups, indent=2):
    """Format nested lists for alternatives field."""
    if not groups:
        return ""
    lines = []
    for group in groups:
        items = ", ".join(f'"{g}"' for g in group)
        lines.append(" " * indent + "- [" + items + "]")
    return "\n".join(lines)


def render_task_yaml(params):
    """Render a param dict into a valid AMBench task YAML string.

    Uses block-style YAML matching the project conventions.
    """
    lines = ["episode:"]

    # id (string)
    eid = params.get("id", "")
    if any(c in eid for c in ":{}[],&*?|>!%@`"):
        lines.append(f'  id: "{eid}"')
    else:
        lines.append(f"  id: {eid}")

    # cell
    cell = params.get("cell", "")
    lines.append(f"  cell: {cell}")

    # turn
    lines.append(f"  turn: {params.get('turn', 0)}")

    # modality
    mod = params.get("modality", "text")
    lines.append(f"  modality: {mod}")

    # context
    ctx = params.get("context", "")
    if "\n" in ctx or len(ctx) > 80:
        lines.append(f"  context: |")
        for line in ctx.strip().split("\n"):
            lines.append(f"    {line}")
    else:
        lines.append(f"  context: {ctx}")

    # query
    qry = params.get("query", "")
    lines.append(f"  query: {qry}")

    # expected (required)
    expected = params.get("expected", [])
    lines.append("  expected:")
    for exp in expected:
        lines.append(f'  - "{exp}"')

    # alternatives (optional)
    alt = params.get("alternatives")
    if alt:
        lines.append("  alternatives:")
        lines.append(_yaml_nested_list(alt, indent=4))

    # distractors (optional)
    dist = params.get("distractors")
    if dist:
        lines.append(f"  distractors: {dist}")

    # difficulty
    lines.append(f"  difficulty: {params.get('difficulty', 1)}")

    # tags
    tags = params.get("tags", [])
    if tags:
        lines.append("  tags:")
        for tag in tags:
            lines.append(f"  - {tag}")

    return "\n".join(lines)


def get_existing_ids():
    """Return set of all episode IDs already in task files."""
    existing = set()
    for fpath in sorted(TASKS_DIR.rglob("*.yaml")):
        if ".gitkeep" in fpath.name:
            continue
        try:
            with open(fpath) as f:
                data = yaml.safe_load(f)
            if data and "episode" in data:
                eid = data["episode"].get("id")
                if eid:
                    existing.add(eid)
        except Exception:
            pass
    return existing


def get_existing_filenames(cell_dir):
    """Return set of filenames already in a cell directory."""
    existing = set()
    if cell_dir.exists():
        for fpath in cell_dir.iterdir():
            if fpath.suffix == ".yaml" and ".gitkeep" not in fpath.name:
                existing.add(fpath.name)
    return existing


def resolve_seq(params, existing_files):
    """Find the next available sequence number.

    Tries the seq from params first, then increments until a free slot is found.
    Returns the params with an updated id and filename using the resolved seq.
    """
    # Extract current seq from id (last group of digits)
    eid = params["id"]
    fname = params.get("filename", f"{eid.lower()}.yaml")

    # Check if this id/fname is taken
    if fname not in existing_files:
        return params  # already unique

    # Find next available seq
    # Parse the numeric suffix from id
    import re

    m = re.search(r"(\d+)$", eid)
    if not m:
        return params  # can't parse, skip

    stem = fname.rsplit(".", 1)[0]  # remove .yaml
    base_id = eid[: -len(m.group(1))]
    base_stem = stem[: -len(m.group(1))]
    digits = len(m.group(1))

    seq = int(m.group(1))
    while True:
        seq += 1
        new_id = f"{base_id}{seq:0{digits}d}"
        new_fname = f"{base_stem}{seq:0{digits}d}.yaml"
        if new_fname not in existing_files:
            params = dict(params)
            params["id"] = new_id
            params["filename"] = new_fname
            return params


def main():
    parser = argparse.ArgumentParser(
        description="Generate AMBench tasks from parameter grids"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without writing files"
    )
    parser.add_argument(
        "--cells",
        type=str,
        default=None,
        help="Comma-separated list of cells to generate (e.g., 'security/injection,security/poisoning')",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Max tasks per cell (default: all from grid)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing tasks (default: skip)",
    )
    args = parser.parse_args()

    # Determine which cells to process
    if args.cells:
        target_cells = [c.strip() for c in args.cells.split(",")]
    else:
        target_cells = sorted(PARAM_GRIDS.keys())

    # Filter to cells that have grids defined
    target_cells = [c for c in target_cells if c in PARAM_GRIDS]

    if not target_cells:
        print("No valid cells specified or found in PARAM_GRIDS.", file=sys.stderr)
        sys.exit(1)

    print(f"AMBench Task Generator")
    print(f"  Target cells: {len(target_cells)}")
    print(f"  Dry run: {args.dry_run}")
    print(f"  Overwrite: {args.overwrite}")
    if args.count:
        print(f"  Max per cell: {args.count}")
    print()

    # Load existing IDs to avoid duplicates
    existing_ids = get_existing_ids()

    total_generated = 0
    total_skipped = 0
    total_errors = 0
    cell_results = []

    for cell in target_cells:
        cell_fname = cell.replace("/", "_").replace("-", "_")
        params_list = PARAM_GRIDS[cell]

        if args.count and len(params_list) > args.count:
            params_list = params_list[: args.count]

        # Determine output dir from cell path
        cell_parts = cell.split("/")
        out_dir = TASKS_DIR / cell_parts[0] / cell_parts[1]
        if len(cell_parts) == 3:
            out_dir = out_dir / cell_parts[2]
        out_dir.mkdir(parents=True, exist_ok=True)

        # Find existing files to skip duplicates
        existing_files = get_existing_filenames(out_dir)

        cell_generated = 0
        cell_skipped = 0
        cell_errors = 0

        for i, params in enumerate(params_list):
            # Resolve sequence number to avoid conflicts
            params = resolve_seq(params, existing_files)
            fname = params.get("filename", f"{params['id'].lower()}.yaml")

            # Check for existing file
            out_path = out_dir / fname
            if out_path.exists() and not args.overwrite:
                cell_skipped += 1
                continue

            # Check for duplicate ID
            if params["id"] in existing_ids and not args.overwrite:
                cell_skipped += 1
                continue

            # Render YAML
            try:
                yaml_str = render_task_yaml(params)
            except Exception as e:
                print(f"  ERROR rendering {cell}/{fname}: {e}", file=sys.stderr)
                cell_errors += 1
                continue

            # Validate by parsing back
            try:
                data = yaml.safe_load(yaml_str)
            except yaml.YAMLError as e:
                print(f"  ERROR YAML parse {cell}/{fname}: {e}", file=sys.stderr)
                cell_errors += 1
                continue

            if data is None:
                print(f"  ERROR empty YAML {cell}/{fname}", file=sys.stderr)
                cell_errors += 1
                continue

            # Use relative path for validation (validator compares against tasks/ dir)
            rel_path = Path("tasks") / "/".join(cell_parts) / fname
            errors = validate_task(rel_path, data)
            if errors:
                print(f"  VALIDATION FAILED {cell}/{fname}:", file=sys.stderr)
                for err in errors:
                    print(f"    - {err}", file=sys.stderr)
                cell_errors += 1
                continue

            # Write
            if not args.dry_run:
                try:
                    out_path.write_text(yaml_str + "\n")
                except Exception as e:
                    print(f"  ERROR writing {out_path}: {e}", file=sys.stderr)
                    cell_errors += 1
                    continue

            existing_files.add(fname)
            existing_ids.add(params["id"])
            cell_generated += 1

        total_generated += cell_generated
        total_skipped += cell_skipped
        total_errors += cell_errors
        cell_results.append((cell, cell_generated, cell_skipped, cell_errors))

        status = f"  {cell:45s} +{cell_generated:2d} generated, {cell_skipped:2d} skipped, {cell_errors:2d} errors"
        print(status)

    print()
    print(f"{'=' * 60}")
    print(
        f"  Total: {total_generated:2d} generated, {total_skipped:2d} skipped, {total_errors:2d} errors"
    )
    print(f"  Tasks written to: tasks/<function>/<form>/<dynamics>/")
    print(f"{'=' * 60}")

    if args.dry_run:
        print("\n  DRY RUN — no files written.")

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
