#!/usr/bin/env python3
"""Scan source and generated output for backup material and likely secrets."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


FORBIDDEN_NAMES = {"wp-config.php", ".env", ".env.local", "attachment-records.private.csv"}
FORBIDDEN_SUFFIXES = {".sql", ".sql.gz", ".tar", ".tar.gz", ".tgz", ".pem", ".key"}
FORBIDDEN_DIRS = {"private", "source-data", "raw-inventory", "backups"}
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".md", ".toml", ".xml", ".txt", ".yaml", ".yml", ".py", ".sh", ".csv", ".conf"}
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    "stripe-secret": re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{20,}\b"),
    "credential-assignment": re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{24,}"),
}
SKIP_DIRS = {".git", "themes", "__pycache__", "node_modules", ".hugo_cache", "resources"}


def files_under(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path


def forbidden_path(relative: str) -> list[str]:
    path = Path(relative)
    name = path.name.lower()
    problems = []
    if any(part.lower() in FORBIDDEN_DIRS for part in path.parts[:-1]):
        problems.append("private source directory")
    if name in FORBIDDEN_NAMES or name.startswith(".env") or any(name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
        problems.append("forbidden backup/credential file")
    return problems


def content_findings(label: str, relative: str, data: bytes) -> list[str]:
    findings = [f"{problem}: {label}/{relative}" for problem in forbidden_path(relative)]
    findings.extend(secret_findings(label, relative, data))
    return findings


def secret_findings(label: str, relative: str, data: bytes) -> list[str]:
    findings: list[str] = []
    suffix = Path(relative).suffix.lower()
    if suffix not in TEXT_SUFFIXES or len(data) > 25_000_000 or b"\0" in data:
        return findings
    text = data.decode("utf-8", errors="ignore")
    for secret_name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(f"possible {secret_name} in {label}/{relative}; value not printed")
    return findings


def scan_index(repo: Path) -> tuple[int, list[str]]:
    try:
        result = subprocess.run(["git", "ls-files", "--stage", "-z"], cwd=repo,
                                capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return 0, ["could not enumerate staged Git index"]
    findings: list[str] = []
    scanned = 0
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, path_bytes = entry.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        relative = path_bytes.decode("utf-8", errors="replace")
        if stage != "0":
            continue
        if mode == "120000":
            findings.append(f"symbolic link found in staged index: {relative}")
            continue
        if mode not in ("100644", "100755"):
            continue
        findings.extend(f"{problem}: staged index/{relative}" for problem in forbidden_path(relative))
        if Path(relative).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            size = int(subprocess.run(["git", "cat-file", "-s", oid], cwd=repo,
                                      capture_output=True, check=True, text=True).stdout.strip())
            if size > 25_000_000:
                continue
            data = subprocess.run(["git", "cat-file", "blob", oid], cwd=repo,
                                  capture_output=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            findings.append(f"could not read staged Git blob: {relative}")
            continue
        scanned += 1
        findings.extend(content_findings("staged index", relative, data))
    return scanned, findings


def scan_history(repo: Path) -> tuple[int, list[str]]:
    try:
        result = subprocess.run(["git", "rev-list", "--objects", "--all"], cwd=repo,
                                capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return 0, ["could not enumerate Git history objects"]
    findings: list[str] = []
    seen: set[str] = set()
    scanned = 0
    for line in result.stdout.splitlines():
        parts = line.decode("utf-8", errors="replace").split(" ", 1)
        oid = parts[0]
        relative = parts[1] if len(parts) > 1 else oid
        findings.extend(f"{problem}: Git history/{relative}" for problem in forbidden_path(relative))
        if oid in seen:
            continue
        seen.add(oid)
        try:
            kind = subprocess.run(["git", "cat-file", "-t", oid], cwd=repo,
                                  capture_output=True, check=True, text=True).stdout.strip()
            if kind != "blob":
                continue
            if Path(relative).suffix.lower() not in TEXT_SUFFIXES:
                continue
            size = int(subprocess.run(["git", "cat-file", "-s", oid], cwd=repo,
                                      capture_output=True, check=True, text=True).stdout.strip())
            if size > 25_000_000:
                continue
            data = subprocess.run(["git", "cat-file", "blob", oid], cwd=repo,
                                  capture_output=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            findings.append(f"could not inspect Git history object {oid}")
            continue
        scanned += 1
        findings.extend(content_findings("Git history", relative, data))
    return scanned, findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--site", type=Path, help="optional generated site directory; omitted before a Hugo build exists")
    ap.add_argument("--include-index", action="store_true", help="also inspect every staged Git blob")
    ap.add_argument("--include-history", action="store_true", help="also inspect reachable committed blobs")
    args = ap.parse_args()
    repo = args.repo.resolve()
    site = args.site.resolve() if args.site else None
    failures: list[str] = []
    scanned = 0
    roots = [("repository", repo)]
    if site:
        roots.append(("generated output", site))
    for label, root in roots:
        if not root.is_dir():
            failures.append(f"scan root is missing: {root}")
            continue
        for path in files_under(root):
            scanned += 1
            rel = path.relative_to(root).as_posix()
            name = path.name.lower()
            if path.is_symlink():
                failures.append(f"symbolic link found in source/output: {root.name}/{rel}")
                continue
            if root == repo and rel == "reports/asset-candidates.csv":
                ignore_rules = (repo / ".gitignore").read_text(encoding="utf-8", errors="replace").splitlines()
                if "/reports/asset-candidates.csv" not in ignore_rules:
                    failures.append("private upload path inventory is not explicitly gitignored")
                continue
            failures.extend(f"{problem}: {root.name}/{rel}" for problem in forbidden_path(rel))
            if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 25_000_000:
                continue
            try:
                data = path.read_bytes()
            except OSError as exc:
                failures.append(f"could not read {root.name}/{rel}: {exc}")
                continue
            failures.extend(secret_findings(root.name, rel, data))
    index_count = history_count = 0
    if args.include_index:
        index_count, index_findings = scan_index(repo)
        failures.extend(index_findings)
    if args.include_history:
        history_count, history_findings = scan_history(repo)
        failures.extend(history_findings)
    scope = "repository and generated output" if site else "repository only; generated output not supplied"
    print(f"Scanned {scanned} files across {scope}; staged_blobs={index_count}; history_blobs={history_count}; findings={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
