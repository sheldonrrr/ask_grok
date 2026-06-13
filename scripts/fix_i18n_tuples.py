#!/usr/bin/env python3
"""Convert mistaken tuple i18n values (str, str) into implicit string concatenation."""

from __future__ import annotations

import ast
import re
from pathlib import Path


def _indent(line: str) -> str:
    match = re.match(r'^(\s*)', line)
    return match.group(1) if match else '            '


def _render_entry(key_name: str, value: str, base_indent: str) -> list[str]:
    val_indent = base_indent + '    '
    if '\n' not in value and len(value) <= 88:
        return [f"{base_indent}'{key_name}': {repr(value)},\n"]

    chunks: list[str] = []
    remaining = value
    while remaining:
        limit = 88
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        split_at = remaining.rfind(' ', 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip()

    lines = [f"{base_indent}'{key_name}': (\n"]
    lines.extend(f'{val_indent}{repr(chunk)}\n' for chunk in chunks)
    lines.append(f'{base_indent}),\n')
    return lines


def fix_file(path: Path) -> int:
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    fixes: list[tuple[int, int, list[str]]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not isinstance(value, ast.Tuple) or not value.elts:
                continue
            if not all(isinstance(elt, ast.Constant) and isinstance(elt.value, str) for elt in value.elts):
                continue
            joined = ''.join(elt.value for elt in value.elts)
            key_name = key.value if isinstance(key, ast.Constant) else '?'
            start = value.lineno - 1
            end = value.end_lineno
            while start >= 0 and f"'{key_name}'" not in lines[start] and f'"{key_name}"' not in lines[start]:
                start -= 1
            base_indent = _indent(lines[start])
            fixes.append((start, end, _render_entry(key_name, joined, base_indent)))

    for start, end, new_lines in sorted(fixes, key=lambda item: item[0], reverse=True):
        lines[start:end] = new_lines

    if fixes:
        path.write_text(''.join(lines), encoding='utf-8')
    return len(fixes)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    total = 0
    for path in sorted((root / 'i18n').glob('*.py')):
        if path.name in {'__init__.py', 'base.py'}:
            continue
        count = fix_file(path)
        if count:
            print(f'Fixed {count} tuples in {path.name}')
            total += count
    print(f'Total fixes: {total}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
