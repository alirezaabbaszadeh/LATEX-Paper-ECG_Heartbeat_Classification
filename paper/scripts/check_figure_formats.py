#!/usr/bin/env python3
"""Validate figure file formats and basic metadata for QA.

This script scans the ``paper/figures`` directory and ensures each
figure has an allowed file extension that matches journal submission
requirements. It also flags empty files so the QA workflow can fail
fast before manuscript submission.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".eps",
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
}


@dataclass
class FigureIssue:
    """Represents a problem found during validation."""

    path: Path
    message: str

    def __str__(self) -> str:  # pragma: no cover - human readable helper
        return f"{self.path}: {self.message}"


def find_figures(root: Path) -> Iterable[Path]:
    """Yield figure files rooted at ``root`` ignoring hidden paths."""

    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part.startswith(".") for part in path.parts):
            yield path


def validate_figure(path: Path) -> List[FigureIssue]:
    """Run validations for a single figure file."""

    issues: List[FigureIssue] = []
    suffix = path.suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        issues.append(
            FigureIssue(
                path=path,
                message=(
                    f"Unsupported extension '{path.suffix}'. "
                    f"Allowed extensions: {allowed}."
                ),
            )
        )

    try:
        size = path.stat().st_size
    except OSError as exc:  # pragma: no cover - filesystem errors are rare
        issues.append(FigureIssue(path=path, message=f"Unable to read file size: {exc}"))
    else:
        if size == 0:
            issues.append(FigureIssue(path=path, message="File is empty."))

    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate figure formats for QA workflows.")
    parser.add_argument(
        "root",
        nargs="?",
        default="paper/figures",
        help="Directory containing figure assets (default: paper/figures).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"::error ::Figure directory '{root}' does not exist.", file=sys.stderr)
        return 1

    issues: List[FigureIssue] = []
    figures = list(find_figures(root))

    if not figures:
        print(f"::warning ::No figures found under '{root}'.", file=sys.stderr)

    for figure in figures:
        issues.extend(validate_figure(figure))

    if issues:
        print("::error ::Figure format validation failed with the following issues:", file=sys.stderr)
        for issue in issues:
            print(f"::error file={issue.path}::{issue.message}", file=sys.stderr)
        return 1

    print(f"Validated {len(figures)} figure(s); all formats are acceptable.")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
