#!/usr/bin/env python3
"""Check prompt size and warn about possible exposed credentials, locally."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = (
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("AWS access key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)

def inspect_prompt(text: str) -> dict:
    """Return statistics and heuristic credential warnings without retaining text."""
    findings = [
        {"type": label, "count": len(pattern.findall(text))}
        for label, pattern in SECRET_PATTERNS if pattern.search(text)
    ]
    return {
        "characters": len(text),
        "words": len(text.split()),
        "estimated_tokens": (len(text) + 3) // 4,
        "empty": not text.strip(),
        "possible_credentials": findings,
    }

def read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.path:
        try:
            return Path(args.path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ValueError(f"Cannot read input file: {exc}") from exc
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("Provide a file path, --text, or pipe text through stdin.")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="UTF-8 text file to inspect")
    parser.add_argument("--text", help="Prompt text (avoid secrets in shell history)")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()
    try:
        prompt = read_input(args)
    except ValueError as exc:
        parser.error(str(exc))
    report = inspect_prompt(prompt)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("PromptCheck report")
        print(f"Characters: {report['characters']}")
        print(f"Words: {report['words']}")
        print(f"Estimated tokens: ~{report['estimated_tokens']} (rough heuristic)")
        if report["empty"]:
            print("Warning: input is empty or whitespace-only.")
        if report["possible_credentials"]:
            print("Warning: possible credential patterns detected:")
            for item in report["possible_credentials"]:
                print(f"  - {item['type']}: {item['count']} match(es)")
            print("Review locally; matches may be false positives.")
        else:
            print("No known credential patterns detected (not a guarantee).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
