#!/usr/bin/env python3
"""Validate a newly created Obsidian knowledge domain."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
SECRET_PATTERNS = {
    "OpenAI-style API key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--domain", required=True, type=Path)
    return parser.parse_args()


def resolve_target(vault: Path, target: str, note_stems: set[str]) -> bool:
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return True

    path_target = Path(target)
    if path_target.suffix.lower() in {
        ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif",
        ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".canvas",
    }:
        direct = vault / path_target
        return direct.exists() or any(p.name == path_target.name for p in vault.rglob("*"))

    return path_target.stem in note_stems


def main() -> int:
    args = parse_args()
    vault = args.vault.expanduser().resolve()
    domain = args.domain.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not (vault / ".obsidian").is_dir():
        errors.append(f"Vault has no .obsidian directory: {vault}")
    if not domain.is_dir():
        errors.append(f"Domain directory does not exist: {domain}")
    try:
        domain.relative_to(vault)
    except ValueError:
        errors.append(f"Domain is outside vault: {domain}")

    markdown_files = list(vault.rglob("*.md")) if vault.exists() else []
    domain_notes = list(domain.rglob("*.md")) if domain.exists() else []
    note_stems = {p.stem for p in markdown_files}
    wikilink_count = 0

    for note in domain_notes:
        text = note.read_text(encoding="utf-8")
        for match in WIKILINK_RE.finditer(text):
            wikilink_count += 1
            target = match.group(1)
            if not resolve_target(vault, target, note_stems):
                errors.append(f"Unresolved Wikilink in {note.name}: [[{target}]]")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Likely {label} in {note.name}")

    canvas_nodes = 0
    canvas_edges = 0
    for canvas_path in domain.rglob("*.canvas"):
        try:
            canvas = json.loads(canvas_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid Canvas JSON {canvas_path.name}: {exc}")
            continue
        nodes = canvas.get("nodes", [])
        edges = canvas.get("edges", [])
        canvas_nodes += len(nodes)
        canvas_edges += len(edges)
        ids = {node.get("id") for node in nodes}
        for node in nodes:
            if node.get("type") == "file":
                file_value = node.get("file", "")
                if not file_value or not (vault / file_value).exists():
                    errors.append(f"Missing Canvas file in {canvas_path.name}: {file_value}")
        for edge in edges:
            if edge.get("fromNode") not in ids or edge.get("toNode") not in ids:
                errors.append(f"Canvas edge references missing node in {canvas_path.name}: {edge}")

    graph_path = vault / ".obsidian" / "graph.json"
    if graph_path.exists():
        try:
            json.loads(graph_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid graph.json: {exc}")
    else:
        warnings.append("No .obsidian/graph.json found")

    attachment_count = sum(1 for p in (domain / "attachments").glob("*") if p.is_file()) \
        if (domain / "attachments").is_dir() else 0
    if attachment_count == 0:
        warnings.append("No files found in attachments/")
    if not list(domain.rglob("*.canvas")):
        warnings.append("No Canvas file found")

    lectures_dir = domain / "Lectures"
    if lectures_dir.is_dir():
        lecture_notes = list(lectures_dir.rglob("*.md"))
        if not lecture_notes:
            warnings.append("Lectures/ exists but contains no Markdown chapters")
        for note in lecture_notes:
            text = note.read_text(encoding="utf-8")
            non_frontmatter = re.sub(r"^---.*?---", "", text, flags=re.DOTALL)
            if len(non_frontmatter.strip()) < 2500:
                warnings.append(f"Detailed lecture may be too short: {note.relative_to(domain)}")

    print(
        f"notes={len(domain_notes)} wikilinks={wikilink_count} "
        f"attachments={attachment_count} canvas_nodes={canvas_nodes} "
        f"canvas_edges={canvas_edges} errors={len(errors)} warnings={len(warnings)}"
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
