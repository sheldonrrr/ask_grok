#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ensure every registered i18n language file has the same translation keys as en.py."""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

I18N_DIR = ROOT / 'i18n'
LANGUAGE_FILES = sorted(
    path for path in I18N_DIR.glob('*.py')
    if path.name not in ('__init__.py', 'base.py', 'en.py')
)


def _extract_translation_keys(filepath: Path) -> set[str]:
    with open(filepath, 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    keys: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key_node in node.keys:
                if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                    keys.add(key_node.value)
    return keys


class TestI18nParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.en_keys = _extract_translation_keys(I18N_DIR / 'en.py')

    def test_en_has_translation_keys(self):
        self.assertGreater(len(self.en_keys), 0)

    def test_all_languages_match_en_keys(self):
        for lang_path in LANGUAGE_FILES:
            lang_code = lang_path.stem
            with self.subTest(language=lang_code):
                lang_keys = _extract_translation_keys(lang_path)
                missing = sorted(self.en_keys - lang_keys)
                extra = sorted(lang_keys - self.en_keys)
                self.assertEqual(
                    missing,
                    [],
                    f'{lang_code}.py missing keys: {missing[:10]}{"..." if len(missing) > 10 else ""}',
                )
                self.assertEqual(
                    extra,
                    [],
                    f'{lang_code}.py extra keys: {extra[:10]}{"..." if len(extra) > 10 else ""}',
                )


if __name__ == '__main__':
    unittest.main()
