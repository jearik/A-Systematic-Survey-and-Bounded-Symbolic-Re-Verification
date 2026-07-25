#!/usr/bin/env python3
"""Shared payload-selection rules for release generation and validation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".idea", ".vscode", "__pycache__", "build", "dist", "tmp"}
IGNORED_NAMES = {"MANIFEST_SHA256.csv", ".DS_Store", "Thumbs.db"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def is_payload(path: Path, root: Path = ROOT) -> bool:
    """Return True only for files intended to be part of the public payload."""
    if not path.is_file():
        return False
    relative = path.relative_to(root)
    return (
        path.name not in IGNORED_NAMES
        and path.suffix.lower() not in IGNORED_SUFFIXES
        and not any(part in IGNORED_DIRS for part in relative.parts)
    )


def payload_files(root: Path = ROOT) -> list[Path]:
    """Return payload files in deterministic POSIX-path order."""
    return sorted(
        (path for path in root.rglob("*") if is_payload(path, root)),
        key=lambda path: path.relative_to(root).as_posix(),
    )
