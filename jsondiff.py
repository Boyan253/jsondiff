#!/usr/bin/env python3
"""Deep diff two JSON documents, reported as dotted paths."""

import argparse
import json
import sys

__version__ = "0.1.0"

ADDED, REMOVED, CHANGED = "+", "-", "~"


def walk(a, b, path=""):
    """Yield (kind, path, old, new) for every difference between a and b."""
    if isinstance(a, dict) and isinstance(b, dict):
        for key in sorted(set(a) | set(b)):
            sub = "%s.%s" % (path, key) if path else str(key)
            if key not in a:
                yield (ADDED, sub, None, b[key])
            elif key not in b:
                yield (REMOVED, sub, a[key], None)
            else:
                yield from walk(a[key], b[key], sub)
        return
    if isinstance(a, list) and isinstance(b, list):
        for i in range(max(len(a), len(b))):
            sub = "%s[%d]" % (path, i)
            if i >= len(a):
                yield (ADDED, sub, None, b[i])
            elif i >= len(b):
                yield (REMOVED, sub, a[i], None)
            else:
                yield from walk(a[i], b[i], sub)
        return
    if a != b:
        yield (CHANGED, path or ".", a, b)


def brief(value, limit=60):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def format_diff(diffs):
    lines = []
    for kind, path, old, new in diffs:
        if kind == ADDED:
            lines.append("+ %s = %s" % (path, brief(new)))
        elif kind == REMOVED:
            lines.append("- %s = %s" % (path, brief(old)))
        else:
            lines.append("~ %s: %s -> %s" % (path, brief(old), brief(new)))
    return lines


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 when the documents differ (for CI)")
    args = ap.parse_args(argv)

    diffs = list(walk(load(args.before), load(args.after)))
    for line in format_diff(diffs):
        print(line)
    if not diffs:
        print("no differences", file=sys.stderr)
    return 1 if (diffs and args.exit_code) else 0


if __name__ == "__main__":
    raise SystemExit(main())
