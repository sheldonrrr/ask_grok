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

    def test_compact_strips_crlf_from_metadata(self):
        books = [{'id': 1, 'title': 'Title\r\nSub', 'authors': 'Author\r'}]
        tsv = utils.format_books_compact_tsv(books)
        self.assertNotIn('\r', tsv)
        self.assertIn('1|Title Sub|Author', tsv)

    def test_split_compact_tsv_lines_handles_crlf(self):
        tsv = '1|A|B\r\n2|C|D\r\n'
        lines = utils.split_compact_tsv_lines(tsv)
        self.assertEqual(lines, ['1|A|B', '2|C|D'])

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

    def test_custom_limit_with_separators_in_prefs(self):
        prefs = {'enable_custom_prompt_limit': True, 'max_prompt_length': '128,000'}
        self.assertEqual(prompt_limits.get_max_prompt_length(True, prefs), 128_000)

    def test_parse_prompt_limit_value(self):
        self.assertEqual(prompt_limits.parse_prompt_limit_value('128,000'), 128_000)
        self.assertEqual(prompt_limits.parse_prompt_limit_value('524 288'), 524_288)
        self.assertEqual(prompt_limits.parse_prompt_limit_value('524_288'), 524_288)

    def test_parse_prompt_limit_text_normalized_flag(self):
        value, normalized = prompt_limits.parse_prompt_limit_text('128,000')
        self.assertEqual(value, 128_000)
        self.assertTrue(normalized)

        value, normalized = prompt_limits.parse_prompt_limit_text('524288')
        self.assertEqual(value, 524_288)
        self.assertFalse(normalized)

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

    def test_build_library_prompt_respects_limit_with_crlf_titles(self):
        books = [
            {'id': i, 'title': f'Book {i}\r\nEdition', 'authors': f'Author {i}\r'}
            for i in range(1, 101)
        ]
        prefs = {
            'library_cached_metadata': json.dumps(books, ensure_ascii=False),
            'enable_custom_prompt_limit': True,
            'max_prompt_length': 8000,
        }
        prompt = utils.build_library_prompt('Find books', prefs)
        self.assertNotIn('\r', prompt)
        self.assertLessEqual(len(prompt), 8000)

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

    _MODELS = ('deepseek-flash', 'deepseek-chat')

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


class TestOmitPlaceholderMetadata(unittest.TestCase):
    def test_unknown_and_empty_fields_are_placeholders(self):
        self.assertTrue(utils.is_placeholder_metadata('Unknown', 'author'))
        self.assertTrue(utils.is_placeholder_metadata('未知', 'language'))
        self.assertTrue(utils.is_placeholder_metadata('und', 'language'))
        self.assertTrue(utils.is_placeholder_metadata('', 'series'))
        self.assertTrue(utils.is_placeholder_metadata('101', 'publisher'))
        self.assertFalse(utils.is_placeholder_metadata('Springer', 'publisher'))
        self.assertFalse(utils.is_placeholder_metadata('Mary Shelley', 'author'))
        self.assertFalse(utils.is_placeholder_metadata('101', 'author'))

    def test_omits_unknown_clauses_from_default_english_template(self):
        template = (
            'Context: You are assisting a user of calibre. '
            'Book Information: Title: "{title}", Author: {author}, Publisher: {publisher}, '
            'Publication Year: {pubyear}, Language: {language}, Series: {series}. '
            'User Question: {query}.'
        )
        values = {
            'title': utils.clean_prompt_metadata_text(
                '[] Advances in Psychiatry Second(BookFi.org)'
            ),
            'author': 'Unknown',
            'publisher': '',
            'pubyear': '2005',
            'language': 'Unknown',
            'series': 'Unknown',
            'query': 'who wrote this',
        }
        filled = utils.omit_placeholder_template_fields(template, values).format(**values)
        self.assertEqual(values['title'], 'Advances in Psychiatry Second')
        self.assertIn('Advances in Psychiatry Second', filled)
        self.assertNotIn('BookFi', filled)
        self.assertNotIn('[]', filled)
        self.assertIn('2005', filled)
        self.assertIn('who wrote this', filled)
        self.assertNotIn('Unknown', filled)
        self.assertNotIn('Author:', filled)
        self.assertNotIn('Publisher:', filled)
        self.assertNotIn('Language:', filled)
        self.assertNotIn('Series:', filled)
        self.assertIn('Publication Year:', filled)

    def test_omits_numeric_publisher_101(self):
        template = 'Title: "{title}", Publisher: {publisher}, Author: {author}.'
        values = {'title': 'A Book', 'publisher': '101', 'author': 'Ada Lovelace'}
        filled = utils.omit_placeholder_template_fields(template, values).format(**values)
        self.assertIn('Ada Lovelace', filled)
        self.assertNotIn('101', filled)
        self.assertNotIn('Publisher:', filled)

    def test_omits_unknown_clauses_from_chinese_template(self):
        template = (
            '书籍信息：书名："{title}"，作者：{author}，出版社：{publisher}，'
            '出版年份：{pubyear}，语言：{language}，系列：{series}。用户问题：{query}。'
        )
        values = {
            'title': '测试书',
            'author': '未知',
            'publisher': '101',
            'pubyear': '2005',
            'language': '未知',
            'series': '',
            'query': '谁写的',
        }
        filled = utils.omit_placeholder_template_fields(template, values).format(**values)
        self.assertIn('测试书', filled)
        self.assertIn('2005', filled)
        self.assertIn('谁写的', filled)
        self.assertNotIn('未知', filled)
        self.assertNotIn('101', filled)
        self.assertNotIn('作者：', filled)
        self.assertNotIn('出版社：', filled)
        self.assertIn('出版年份：', filled)

    def test_line_template_drops_placeholder_rows(self):
        template = (
            'User query: {query}\n'
            'Book title: {title}\n'
            'Author: {author}\n'
            'Publisher: {publisher}\n'
            'Publication year: {pubyear}\n'
        )
        values = {
            'query': 'hello',
            'title': 'Frankenstein',
            'author': 'Unknown',
            'publisher': '101',
            'pubyear': '1818',
        }
        filled = utils.omit_placeholder_template_fields(template, values).format(**values)
        self.assertIn('Frankenstein', filled)
        self.assertIn('1818', filled)
        self.assertNotIn('Author:', filled)
        self.assertNotIn('Publisher:', filled)


class TestPromptTemplateLanguage(unittest.TestCase):
    def test_old_english_default_follows_interface_language(self):
        old_english = (
            'About the book "{title}": Author: {author}, Publisher: {publisher}, '
            'Publication Year: {pubyear}, book in language: {language}, '
            'Series: {series}, My question is: {query}'
        )
        traditional = '背景說明：書名：「{title}」，作者：{author}。用戶問題：{query}。'
        resolved = utils.resolve_prompt_template(
            old_english,
            traditional,
            [traditional],
            ('{title}', '{author}', '{query}'),
        )
        self.assertEqual(resolved, traditional)

    def test_custom_prompt_is_kept(self):
        custom = (
            'Please answer as a historian. Title {title}. Author {author}. '
            'Question {query}. ' + ('context ' * 80)
        )
        traditional = '背景說明：書名：「{title}」作者：{author} 問題：{query}'
        self.assertEqual(
            utils.resolve_prompt_template(
                custom, traditional, [traditional], ('{title}', '{author}', '{query}')
            ),
            custom.strip(),
        )

    def test_unknown_calibre_year_101_is_placeholder(self):
        self.assertTrue(utils.is_placeholder_metadata('101', 'pubyear'))
        self.assertFalse(utils.is_placeholder_metadata('2003', 'pubyear'))


class TestPersonaLanguage(unittest.TestCase):
    def test_builtin_english_persona_follows_prompt_language(self):
        english = 'As a researcher, I want to research through book data.'
        chinese = '作为研究人员，我希望通过书籍数据进行研究。'
        german = 'Als Forscher möchte ich durch Buchdaten recherchieren。'
        known = [english, chinese, german]
        self.assertEqual(utils.resolve_persona_text(english, chinese, known), chinese)
        self.assertEqual(utils.resolve_persona_text('', german, known), german)
        self.assertEqual(utils.resolve_persona_text(None, german, known), german)

    def test_custom_persona_is_kept(self):
        custom = 'I am a historian of the 19th century.'
        chinese = '作为研究人员，我希望通过书籍数据进行研究。'
        self.assertEqual(
            utils.resolve_persona_text(custom, chinese, [chinese]),
            custom,
        )


class TestPromptSpliceI18n(unittest.TestCase):
    def test_non_english_library_prompt_appends_localized_output_rule(self):
        french_rule = (
            'IMPORTANT : renvoyez UNIQUEMENT les livres correspondants '
            'sous forme de liste à puces HTML ci-dessus.'
        )
        i18n = {
            'library_prompt_template': (
                'Voici les livres : {metadata} Requête de l\'utilisateur : {query}'
            ),
            'library_output_only_rule': french_rule,
        }
        prefs = {
            'library_cached_metadata': json.dumps(
                [{'id': 1, 'title': 'Le Rouge et le Noir', 'authors': 'Stendhal'}],
                ensure_ascii=False,
            ),
        }
        prompt = utils.build_library_prompt('Qui a écrit ce livre ?', prefs, i18n)
        self.assertIn('Requête de l\'utilisateur', prompt)
        self.assertIn(french_rule, prompt)
        self.assertNotIn('Output ONLY', prompt)
        self.assertNotIn('Do not write analysis', prompt)

    def test_english_and_chinese_templates_are_not_given_a_second_rule(self):
        prefs = {
            'library_cached_metadata': json.dumps(
                [{'id': 1, 'title': 'Frankenstein', 'authors': 'Mary Shelley'}],
                ensure_ascii=False,
            ),
        }
        english = {
            'library_prompt_template': (
                'Books: {metadata} User query: {query} Output ONLY the bullet list.'
            ),
            'library_output_only_rule': (
                'IMPORTANT: Output ONLY the matching books as the HTML bullet list above.'
            ),
        }
        prompt = utils.build_library_prompt('who wrote it', prefs, english)
        self.assertEqual(prompt.count('Output ONLY'), 1)

        chinese = {
            'library_prompt_template': '书籍：{metadata} 用户查询：{query} 只输出上述列表。',
            'library_output_only_rule': '重要：只输出上面 HTML 列表中的匹配书籍。',
        }
        prompt = utils.build_library_prompt('谁写的', prefs, chinese)
        self.assertEqual(prompt.count('只输出'), 1)
        self.assertNotIn('Output ONLY', prompt)

    def test_french_metadata_labels_survive_placeholder_omission(self):
        template = (
            'Informations sur le livre : Titre : "{title}", Auteur : {author}, '
            'Éditeur : {publisher}, Année de publication : {pubyear}, '
            'Langue : {language}, Série : {series}. '
            'Question de l\'utilisateur : {query}.'
        )
        values = {
            'title': 'Le Rouge et le Noir',
            'author': 'Stendhal',
            'publisher': '101',
            'pubyear': '1830',
            'language': 'inconnu',
            'series': '',
            'query': 'De quoi parle ce livre ?',
        }
        filled = utils.omit_placeholder_template_fields(template, values).format(**values)
        self.assertIn('Titre : "Le Rouge et le Noir"', filled)
        self.assertIn('Auteur : Stendhal', filled)
        self.assertIn('Année de publication : 1830', filled)
        self.assertIn('Question de l\'utilisateur', filled)
        self.assertNotIn('Author:', filled)
        self.assertNotIn('Éditeur', filled)
        self.assertNotIn('Langue', filled)
        self.assertNotIn('Série', filled)
        self.assertNotIn('inconnu', filled)


class TestCleanPromptMetadata(unittest.TestCase):
    def test_strips_empty_brackets_and_bookfi_watermark(self):
        cleaned = utils.clean_prompt_metadata_text(
            '[] Advances in Psychiatry Second(BookFi.org)'
        )
        self.assertEqual(cleaned, 'Advances in Psychiatry Second')

    def test_strips_other_site_watermarks_and_keeps_edition(self):
        cleaned = utils.clean_prompt_metadata_text(
            '[ ] Real Title (2nd edition) (z-lib.org)'
        )
        self.assertEqual(cleaned, 'Real Title (2nd edition)')

    def test_keeps_nonempty_brackets(self):
        self.assertEqual(
            utils.clean_prompt_metadata_text('[Vol. 1] The History of Rome'),
            '[Vol. 1] The History of Rome',
        )

    def test_compact_tsv_cleans_title_watermark(self):
        tsv = utils.format_books_compact_tsv([{
            'id': 12,
            'title': '[] Advances in Psychiatry Second(BookFi.org)',
            'authors': 'Unknown',
        }])
        self.assertEqual(tsv, '12|Advances in Psychiatry Second|Unknown')


if __name__ == '__main__':
    unittest.main(verbosity=2)
