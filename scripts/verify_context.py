#!/usr/bin/env python3
"""Check the active context graph and target.md's pure portfolio import boundary.

This is a static maintenance check, not semantic approval or a security sandbox.
Historical documents are intentionally outside the active-document link check.
"""

import argparse
import ast
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REQUIRED = (
    "AGENTS.md",
    "README.md",
    "docs/INDEX.md",
    "docs/ROADMAP.md",
    "docs/DEVELOPMENT.md",
    "docs/TESTING.md",
    "docs/SECURITY.md",
    "docs/product/strategy.md",
    "docs/domain/investment-operations.md",
    "docs/architecture/target.md",
    "docs/architecture/adr-008-investment-operations.md",
    "docs/ai/governance.md",
    "docs/engineering/operations.md",
    "docs/engineering/refactor-verification.md",
    "docs/zh-TW/overview.md",
    "docs/zh-TW/architecture.md",
    "src/alphapulse/portfolio/valuation.py",
    "tests/portfolio/test_valuation.py",
)
ACTIVE_DOCS = tuple(path for path in REQUIRED if path.endswith(".md")) + (
    "docs/QUICKSTART.md",
    "docs/architecture/README.md",
)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def collect_errors(root: Path) -> list[str]:
    root = root.resolve()
    errors = [
        f"Missing authority or evidence: {path}"
        for path in REQUIRED
        if not (root / path).is_file()
    ]
    for name in ACTIVE_DOCS:
        path = root / name
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        # Ignore example Markdown inside fenced code blocks.
        prose = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        for target in LINK.findall(prose):
            target = target.strip().split(' "', 1)[0].strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f"Broken local link: {name} -> {target}")
        if "alphapulse-mlops-platform" in content:
            errors.append(f"Stale active project identity: {name}")
    for path in sorted((root / "src/alphapulse/portfolio").rglob("*.py")):
        relative = path.relative_to(root)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            errors.append(f"Invalid Python: {relative}:{exc.lineno}")
            continue
        for node in ast.walk(tree):
            imports = []
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level == 1:
                    continue  # Inside this same portfolio package.
                if node.level > 1:
                    errors.append(
                        f"Portfolio boundary violation: {relative}:{node.lineno}"
                    )
                    continue
                imports = [node.module or ""]
            for module in imports:
                if (
                    module.split(".")[0] not in sys.stdlib_module_names
                    and module != "alphapulse.portfolio"
                    and not module.startswith("alphapulse.portfolio.")
                ):
                    errors.append(
                        f"Portfolio boundary violation: {relative}:{node.lineno} -> {module}"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    errors = collect_errors(parser.parse_args().root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        "Active context links, required authorities, identity and portfolio imports: PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
