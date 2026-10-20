#!/usr/bin/env python3
"""
repo-context-packer: Pack any codebase into a single LLM-ready Markdown file.
"""

import os
import sys
import argparse
from pathlib import Path

DEFAULT_IGNORES = {
    ".git", "__pycache__", "node_modules", "venv", ".venv",
    "dist", "build", ".idea", ".vscode", ".DS_Store", "package-lock.json"
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
    ".tar", ".gz", ".exe", ".dll", ".so", ".pyc", ".mp4", ".mp3"
}

def estimate_tokens(text: str) -> int:
    """Rough token estimation (~4 characters per token for English/code)."""
    return max(1, len(text) // 4)

def should_ignore(path: Path, ignore_set: set) -> bool:
    for part in path.parts:
        if part in ignore_set:
            return True
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    return False

def generate_tree(root_dir: Path, ignore_set: set) -> str:
    tree_lines = [f"📁 {root_dir.resolve().name}/"]
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in sorted(dirs) if d not in ignore_set]
        rel_root = Path(root).relative_to(root_dir)
        level = len(rel_root.parts)
        indent = "  " * level
        if rel_root != Path("."):
            tree_lines.append(f"{indent}├── 📂 {rel_root.name}/")
        sub_indent = "  " * (level + 1)
        for f in sorted(files):
            file_path = Path(root) / f
            if not should_ignore(file_path.relative_to(root_dir), ignore_set):
                tree_lines.append(f"{sub_indent}└── 📄 {f}")
    return "\n".join(tree_lines)

def pack_repository(root_dir: Path, output_file: Path, max_size_kb: int = 500):
    ignore_set = set(DEFAULT_IGNORES)
    ignore_set.add(output_file.name)

    sections = []
    total_files = 0

    # 1. Directory Tree
    tree_str = generate_tree(root_dir, ignore_set)
    sections.append("# Project Directory Structure\n\n```text\n" + tree_str + "\n```\n")

    # 2. File Contents
    sections.append("# File Contents\n")
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in sorted(dirs) if d not in ignore_set]
        for file in sorted(files):
            file_path = Path(root) / file
            rel_path = file_path.relative_to(root_dir)

            if should_ignore(rel_path, ignore_set):
                continue

            if file_path.stat().st_size > max_size_kb * 1024:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                ext = file_path.suffix.lstrip(".") or "text"
                sections.append(f"## `{rel_path.as_posix()}`\n\n```{ext}\n{content}\n```\n")
                total_files += 1
            except (UnicodeDecodeError, PermissionError):
                continue

    final_output = "\n".join(sections)
    output_file.write_text(final_output, encoding="utf-8")
    total_tokens = estimate_tokens(final_output)

    print(f"✅ Packed {total_files} files into '{output_file}'")
    print(f"📊 Estimated LLM Context Size: ~{total_tokens:,} tokens")

def main():
    parser = argparse.ArgumentParser(description="Pack a repo into an LLM-ready Markdown file.")
    parser.add_argument("path", nargs="?", default=".", help="Path to repository (default: current directory)")
    parser.add_argument("-o", "--output", default="context.md", help="Output Markdown filename")
    parser.add_argument("--max-kb", type=int, default=500, help="Skip files larger than this size in KB")
    args = parser.parse_args()

    pack_repository(Path(args.path), Path(args.output), args.max_kb)

if __name__ == "__main__":
    main()
