#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit and integration tests for prompt length / library compact metadata logic."""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.load_env import load_dotenv

load_dotenv()

import prompt_limits
import utils


def _sample_i18n() -> dict:
    return {
        'question_too_long_detail': (
            'Prompt is too long ({current} characters, limit {limit}, over by {over}). '
            'You selected {book_count} book(s).'
        ),
        'question_too_long_hint_ai_search': 'Use AI Search for library-wide queries.',
        'question_too_long_reduce_books': 'Try deselecting about {count} book(s).',
        'question_too_long_hint_default': 'Default limit: {limit} ({mode}).',
        'question_too_long_hint_custom': 'Custom limit enabled.',
        'question_too_long_hint_library_search': 'Enable custom limit (suggested: 524288).',
        'multi_book': 'Multi-Book',
        'single_book': 'Single Book',
    }


def _make_books(count: int) -> list:
    return [
        {'id': i, 'title': f'Test Book {i}', 'authors': f'Author {i % 7}'}
        for i in range(1, count + 1)
    ]


class TestCompactMetadata(unittest.TestCase):
    def test_compact_tsv_format(self):
        books = _make_books(3)
        tsv = utils.format_books_compact_tsv(books)
        lines = tsv.split('\n')
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith('1|Test Book 1|'))

    def test_compact_escapes_pipe_in_title(self):
        books = [{'id': 9, 'title': 'A|B', 'authors': 'C'}]
        tsv = utils.format_books_compact_tsv(books)
        self.assertIn('9|A/B|C', tsv)

    def test_library_metadata_for_prompt_uses_compact_tsv(self):
        prefs = {'library_cached_metadata': json.dumps(_make_books(5), ensure_ascii=False)}
        compact = utils.format_library_metadata_for_prompt(prefs)
        self.assertNotIn('[{', compact)
        self.assertEqual(compact.count('\n'), 4)

    def test_update_library_metadata_indexes_all_books(self):
        book_ids = list(range(1, 251))
        db = MagicMock()
        db.new_api.all_book_ids.return_value = book_ids

        def fake_metadata(book_id, index_is_id=True):
            mi = MagicMock()
            mi.title = f'Book {book_id}'
            mi.authors = ['Author']
            return mi

        db.get_metadata.side_effect = fake_metadata
        prefs = {}

        ok, count, err = utils.update_library_metadata(db, prefs)
        self.assertTrue(ok, err)
        self.assertEqual(count, 250)
        stored = json.loads(prefs['library_cached_metadata'])
        self.assertEqual(len(stored), 250)


class TestPromptLimits(unittest.TestCase):
    def test_default_limits(self):
        prefs = {'enable_custom_prompt_limit': False}
        self.assertEqual(prompt_limits.get_max_prompt_length(False, prefs), 128_000)
        self.assertEqual(prompt_limits.get_max_prompt_length(True, prefs), 256_000)

    def test_custom_limit(self):
        prefs = {'enable_custom_prompt_limit': True, 'max_prompt_length': 524288}
        self.assertEqual(prompt_limits.get_max_prompt_length(True, prefs), 524288)

    def test_validate_rejects_over_limit_with_details(self):
        prefs = {'enable_custom_prompt_limit': False}
        err = prompt_limits.validate_prompt_length(
            'x' * 300_000, True, prefs, _sample_i18n(), book_count=120,
        )
        self.assertIsNotNone(err)
        self.assertIn('300000', err)
        self.assertIn('256000', err)
        self.assertIn('Use AI Search', err)

    def test_validate_passes_under_limit(self):
        prefs = {'enable_custom_prompt_limit': False}
        err = prompt_limits.validate_prompt_length(
            'short question', False, prefs, _sample_i18n(), book_count=1,
        )
        self.assertIsNone(err)

    def test_build_library_prompt_scales_with_many_books(self):
        prefs = {
            'library_cached_metadata': json.dumps(_make_books(1000), ensure_ascii=False),
        }
        prompt = utils.build_library_prompt('Find Python books', prefs)
        self.assertIn('Find Python books', prompt)
        self.assertGreater(len(prompt), 20000)
        # Compact: ~1000 books should stay well under default multi limit
        self.assertLess(len(prompt), 256_000)

    def test_build_library_prompt_truncates_when_over_limit(self):
        prefs = {
            'library_cached_metadata': json.dumps(_make_books(500), ensure_ascii=False),
            'enable_custom_prompt_limit': True,
            'max_prompt_length': 5000,
        }
        prompt = utils.build_library_prompt('Find Python books', prefs, _sample_i18n())
        self.assertLess(len(prompt), 6000)
        self.assertIn('500', prompt)

    def test_library_search_error_message(self):
        prefs = {'enable_custom_prompt_limit': False}
        err = prompt_limits.validate_prompt_length(
            'x' * 300_000, True, prefs, _sample_i18n(), book_count=8000,
            is_library_search=True,
        )
        self.assertIsNotNone(err)
        self.assertIn('524288', err)


class TestDeepSeekIntegration(unittest.TestCase):
    """Live API checks using DEEPSEEK_API_KEY from .env (skipped if missing)."""

    _MODELS = ('deepseek-chat', 'deepseek-v4-flash')

    @classmethod
    def setUpClass(cls):
        cls.api_key = os.environ.get('DEEPSEEK_API_KEY', '').strip()
        if not cls.api_key:
            raise unittest.SkipTest('DEEPSEEK_API_KEY not set in .env')

    def _post_chat(self, prompt: str, max_tokens: int = 32):
        import requests

        last_error = None
        for model in self._MODELS:
            response = requests.post(
                'https://api.deepseek.com/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': max_tokens,
                    'temperature': 0,
                },
                timeout=120,
            )
            if response.status_code == 200:
                return model, response.json()
            last_error = f'{model}: HTTP {response.status_code} {response.text[:300]}'

        self.fail(f'DeepSeek request failed for all models: {last_error}')

    def test_api_key_valid(self):
        model, data = self._post_chat('Reply with exactly: OK')
        content = data['choices'][0]['message']['content']
        self.assertTrue(content.strip())

    def test_large_library_prompt_accepted_by_api(self):
        prefs = {
            'library_cached_metadata': json.dumps(_make_books(800), ensure_ascii=False),
            'enable_custom_prompt_limit': True,
            'max_prompt_length': 524288,
        }
        prompt = utils.build_library_prompt(
            'Which book titles mention Python? Reply with one title only.',
            prefs,
        )
        self.assertLess(len(prompt), 524288)

        length_err = prompt_limits.validate_prompt_length(
            prompt, True, prefs, _sample_i18n(),
            book_count=prompt_limits.count_books_in_library_metadata(prefs),
        )
        self.assertIsNone(length_err, length_err)

        model, data = self._post_chat(prompt, max_tokens=64)
        content = data['choices'][0]['message']['content']
        self.assertTrue(content.strip(), f'Empty response from {model}')

    def test_default_limit_blocks_oversized_multi_book_prompt(self):
        prefs = {'enable_custom_prompt_limit': False}
        oversized = 'x' * 300_000
        err = prompt_limits.validate_prompt_length(
            oversized, True, prefs, _sample_i18n(), book_count=200,
        )
        self.assertIsNotNone(err)
        self.assertIn('300000', err)


if __name__ == '__main__':
    unittest.main(verbosity=2)
