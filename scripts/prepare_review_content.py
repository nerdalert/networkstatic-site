#!/usr/bin/env python3
"""Assemble project utility pages and public WordPress review content."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, default=Path("migration-review/build-content"))
    args = parser.parse_args()
    destination = (ROOT / args.destination).resolve()
    if not destination.is_relative_to((ROOT / "migration-review").resolve()):
        parser.error("destination must stay inside migration-review")

    project_content = ROOT / "content"
    review_content = ROOT / "migration-review/generated/content"
    for source in (project_content, review_content):
        if not source.is_dir():
            parser.error(f"content source directory is missing: {source}")

    shutil.rmtree(destination, ignore_errors=True)
    shutil.copytree(project_content, destination)
    shutil.copytree(review_content, destination, dirs_exist_ok=True)
    print(f"Prepared review content from project pages and {review_content}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
