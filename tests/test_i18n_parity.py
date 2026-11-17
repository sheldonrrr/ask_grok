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


def _literal_string(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal_string(node.left)
        right = _literal_string(node.right)
        if left is None or right is None:
            return None
        return left + right
    return None


def _extract_translation_map(filepath: Path) -> dict[str, str]:
    with open(filepath, 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    values: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key_node, value_node in zip(node.keys, node.values):
            if not isinstance(key_node, ast.Constant) or not isinstance(key_node.value, str):
                continue
            text = _literal_string(value_node)
            if text is not None:
                values[key_node.value] = text
    return values


def _extract_translation_keys(filepath: Path) -> set[str]:
    return set(_extract_translation_map(filepath))


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

    def test_prompt_splice_keywords_are_not_leftover_english(self):
        """Headers and suffixes concatenated into the outgoing prompt must be translated."""
        splice_keys = ('multi_book_entry_header', 'library_output_only_rule')
        en_values = _extract_translation_map(I18N_DIR / 'en.py')
        for key in splice_keys:
            self.assertIn(key, en_values)
        for lang_path in LANGUAGE_FILES:
            lang_code = lang_path.stem
            values = _extract_translation_map(lang_path)
            with self.subTest(language=lang_code):
                for key in splice_keys:
                    self.assertNotEqual(
                        values.get(key),
                        en_values[key],
                        f'{lang_code} {key} is still the English prompt fragment',
                    )
                self.assertNotIn('Output ONLY', values['library_output_only_rule'])
                self.assertNotIn('Book {idx}', values['multi_book_entry_header'])
        french = _extract_translation_map(I18N_DIR / 'fr.py')
        self.assertEqual(french['multi_book_entry_header'], 'Livre {idx} :')
        self.assertIn('UNIQUEMENT', french['library_output_only_rule'])


if __name__ == '__main__':
    unittest.main()
