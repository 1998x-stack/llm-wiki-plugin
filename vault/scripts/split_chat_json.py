#!/usr/bin/env python3
"""Split ChatGPT-exported JSON into per-round markdown files.

Usage:
    python split_chat_json.py <json_file> [--outdir <dir>]

Each JSON contains metadata + messages array. Messages alternate
Prompt/Response. This script pairs them and writes one markdown
per pair into a subfolder (default: same name as JSON without .json).
"""

import json
import os
import re
import sys
import argparse
from typing import Optional, List


def _strip_timestamp(text: str) -> str:
    """Remove leading timestamp line like '2026-04-12 10:30:34\\n\\n\\n'."""
    return re.sub(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*\n*", "", text).strip()


def _strip_thinking(text: str) -> str:
    """Remove '> 已思考若干秒' lines from response."""
    return re.sub(r"^>\s*已思考.*秒\s*\n*", "", text, flags=re.MULTILINE).strip()


def _make_filename(prompt_text: str, index: int) -> str:
    """Generate a safe filename from the prompt question text."""
    clean = _strip_timestamp(prompt_text)
    # Take first line or up to 50 chars
    first_line = clean.split("\n")[0][:50].strip()
    # Remove characters unsafe for filenames
    safe = re.sub(r'[\\/:*?"<>|]', "", first_line)
    safe = safe.strip(". ")
    if not safe:
        safe = f"round-{index:02d}"
    return f"{index:02d}-{safe}.md"


def split_chat(json_path: str, outdir: Optional[str] = None) -> List[str]:
    """Split a ChatGPT JSON export into per-round markdown files.

    Returns list of created file paths.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = data.get("metadata", {})
    title = metadata.get("title", os.path.splitext(os.path.basename(json_path))[0])
    messages = data.get("messages", [])

    if not messages:
        print(f"No messages found in {json_path}")
        return []

    # Default output dir: same as json file path without .json
    if outdir is None:
        outdir = os.path.splitext(json_path)[0]

    os.makedirs(outdir, exist_ok=True)

    # Pair messages: every two (Prompt + Response)
    created = []
    pair_index = 0
    i = 0
    while i < len(messages):
        prompt_msg = messages[i]
        response_msg = messages[i + 1] if i + 1 < len(messages) else None

        pair_index += 1

        prompt_text = prompt_msg.get("say", "")
        prompt_time = prompt_msg.get("time", "")
        prompt_clean = _strip_timestamp(prompt_text)

        filename = _make_filename(prompt_text, pair_index)
        filepath = os.path.join(outdir, filename)

        lines = []
        lines.append(f"# {_strip_timestamp(prompt_text).split(chr(10))[0][:80]}")
        lines.append("")
        lines.append(f"> Source: {title}")
        lines.append(f"> Time: {prompt_time}")
        lines.append("")
        lines.append("## Question")
        lines.append("")
        lines.append(prompt_clean)
        lines.append("")

        if response_msg:
            response_text = response_msg.get("say", "")
            response_clean = _strip_thinking(_strip_timestamp(response_text))
            lines.append("## Answer")
            lines.append("")
            lines.append(response_clean)
            lines.append("")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        created.append(filepath)
        i += 2  # Move to next pair

    # Verify all writes succeeded before removing source
    all_ok = all(os.path.isfile(p) and os.path.getsize(p) > 0 for p in created)
    if all_ok and created:
        os.remove(json_path)
        print(f"Split {json_path} → {len(created)} files in {outdir}/ (JSON removed)")
    else:
        print(f"Split {json_path} → {len(created)} files in {outdir}/ (JSON kept — verify writes)")
    for p in created:
        print(f"  {os.path.basename(p)}")

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Split ChatGPT JSON into per-round markdowns"
    )
    parser.add_argument("json_file", help="Path to ChatGPT JSON export")
    parser.add_argument(
        "--outdir", help="Output directory (default: <json_file> without .json)"
    )
    args = parser.parse_args()

    if not os.path.isfile(args.json_file):
        print(f"Error: {args.json_file} not found")
        sys.exit(1)

    split_chat(args.json_file, args.outdir)


if __name__ == "__main__":
    main()
