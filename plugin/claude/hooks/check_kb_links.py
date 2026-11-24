#!/usr/bin/env python3
"""PostToolUse hook: report broken relative links in an edited kb/ page.

Reads the hook payload (JSON) on stdin. Acts only when the edited file is a
Markdown file under a `kb/` directory. Exits 2 with the broken links on stderr
so Claude can fix them; exits 0 in every other case, including any error, so
the hook never blocks writing. Standard library only; no network access.
"""
import json
import os
import re
import sys
from urllib.parse import unquote

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
SKIP = ("http://", "https://", "mailto:", "tel:", "#", "data:")
FENCE = re.compile(r"^\s*(```|~~~)")


def broken_links(path):
    base = os.path.dirname(path)
    out = []
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = re.sub(r"`[^`]*`", "", line)
            for target in LINK.findall(line):
                if target.lower().startswith(SKIP):
                    continue
                rel = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not rel:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(base, rel))):
                    out.append((lineno, target))
    return out


def main():
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    if not os.path.isabs(path):
        path = os.path.join(payload.get("cwd") or os.getcwd(), path)
    parts = os.path.normpath(path).split(os.sep)
    if "kb" not in parts[:-1] or not os.path.isfile(path):
        return 0
    bad = broken_links(path)
    if not bad:
        return 0
    lines = [f"{path} has {len(bad)} relative link(s) to files that don't exist:"]
    lines += [f"  line {n}: {t}" for n, t in bad]
    lines.append("Fix the path, create the page, or remove the link.")
    print("\n".join(lines), file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
