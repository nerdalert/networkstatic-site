"""Shared migration publication exclusions."""
from __future__ import annotations

import csv
from pathlib import Path


def read_exclusions(root: Path) -> tuple[set[str], set[str]]:
    path = root / "config/publication-exclusions.csv"
    if not path.is_file():
        return set(), set()
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    return ({row.get("wp_id", "").strip() for row in rows if row.get("wp_id", "").strip()},
            {row.get("route", "").strip().rstrip("/") + "/" for row in rows
             if row.get("route", "").strip()})


def is_excluded(wp_id: str, route: str, excluded_ids: set[str], excluded_routes: set[str]) -> bool:
    normalized_route = route.rstrip("/") + "/" if route.strip("/") else "/"
    return str(wp_id) in excluded_ids or normalized_route in excluded_routes
