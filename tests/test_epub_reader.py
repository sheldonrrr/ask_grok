#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""EPUB spine parsing and selection-prompt assembly for the reader MVP."""

import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import epub_reader


CONTAINER = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

OPF = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Sample Book</dc:title>
  </metadata>
  <manifest>
    <item id="c1" href="text/c1.xhtml" media-type="application/xhtml+xml"/>
    <item id="c2" href="text/c2.xhtml" media-type="application/xhtml+xml"/>
    <item id="notes" href="text/notes.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles/book.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="c1"/>
    <itemref idref="c2"/>
    <itemref idref="notes" linear="no"/>
  </spine>
</package>
"""

NAV = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <body>
    <nav epub:type="toc">
      <ol>
        <li><a href="text/c1.xhtml">Chapter One</a></li>
        <li><a href="text/c2.xhtml">Chapter Two</a></li>
      </ol>
    </nav>
  </body>
</html>
"""

CHAPTER = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head><link rel="stylesheet" href="../styles/book.css"/></head>
  <body><h1>Ignored heading</h1><p>{body}</p></body>
</html>
"""


def _write_epub(dest, opf=OPF):
    files = {
        'META-INF/container.xml': CONTAINER,
        'OEBPS/content.opf': opf,
        'OEBPS/nav.xhtml': NAV,
        'OEBPS/styles/book.css': 'p { color: #222; }',
        'OEBPS/text/c1.xhtml': CHAPTER.format(body='Hello selection.'),
        'OEBPS/text/c2.xhtml': CHAPTER.format(body='Second chapter.'),
        'OEBPS/text/notes.xhtml': CHAPTER.format(body='Notes.'),
    }
    with zipfile.ZipFile(dest, 'w') as archive:
        for name, text in files.items():
            archive.writestr(name, text.encode('utf-8'))


class ParseEpubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='ask_ai_epub_test_')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_spine_order_titles_and_css_path(self):
        epub_path = os.path.join(self.tmp, 'book.epub')
        _write_epub(epub_path)
        parsed = epub_reader.parse_epub(epub_path, os.path.join(self.tmp, 'extracted'))
        self.assertEqual(parsed.title, 'Sample Book')
        self.assertEqual([chapter.title for chapter in parsed.chapters], ['Chapter One', 'Chapter Two'])
        self.assertEqual(parsed.chapters[0].rel_path, 'OEBPS/text/c1.xhtml')
        css_path = os.path.normpath(os.path.join(os.path.dirname(parsed.chapters[0].abs_path), '..', 'styles', 'book.css'))
        self.assertTrue(os.path.isfile(css_path))
        with open(parsed.chapters[0].abs_path, 'r', encoding='utf-8') as handle:
            self.assertIn('Hello selection.', handle.read())

    def test_nonlinear_chapters_used_when_spine_has_no_linear_docs(self):
        opf = OPF.replace('<itemref idref="c1"/>', '<itemref idref="c1" linear="no"/>')
        opf = opf.replace('<itemref idref="c2"/>', '<itemref idref="c2" linear="no"/>')
        epub_path = os.path.join(self.tmp, 'notes.epub')
        _write_epub(epub_path, opf=opf)
        parsed = epub_reader.parse_epub(epub_path, os.path.join(self.tmp, 'extracted'))
        self.assertEqual(len(parsed.chapters), 3)

    def test_skips_image_only_pages_and_labels_inline_images(self):
        epub_path = os.path.join(self.tmp, 'cover.epub')
        opf = OPF.replace(
            '<item id="c1" href="text/c1.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>\n'
            '    <item id="c1" href="text/c1.xhtml" media-type="application/xhtml+xml"/>',
        ).replace(
            '<itemref idref="c1"/>',
            '<itemref idref="cover"/>\n    <itemref idref="c1"/>',
        )
        illustrated = CHAPTER.format(body='Hello selection.').replace(
            '</body>',
            '<img src="../images/ship.jpg" alt="A ship"/></body>',
        )
        with zipfile.ZipFile(epub_path, 'w') as archive:
            archive.writestr('META-INF/container.xml', CONTAINER.encode('utf-8'))
            archive.writestr('OEBPS/content.opf', opf.encode('utf-8'))
            archive.writestr('OEBPS/nav.xhtml', NAV.encode('utf-8'))
            archive.writestr('OEBPS/styles/book.css', b'p { color: #222; }')
            archive.writestr(
                'OEBPS/text/cover.xhtml',
                b'<html xmlns="http://www.w3.org/1999/xhtml"><body><img src="cover.jpg" alt="Cover"/></body></html>',
            )
            archive.writestr('OEBPS/text/c1.xhtml', illustrated.encode('utf-8'))
            archive.writestr('OEBPS/text/c2.xhtml', CHAPTER.format(body='Second chapter.').encode('utf-8'))
            archive.writestr('OEBPS/text/notes.xhtml', CHAPTER.format(body='Notes.').encode('utf-8'))
        parsed = epub_reader.parse_epub(
            epub_path,
            os.path.join(self.tmp, 'extracted'),
            image_placeholder='Image preview is unavailable: {name}',
        )
        self.assertEqual([chapter.title for chapter in parsed.chapters], ['Chapter One', 'Chapter Two'])
        with open(parsed.chapters[0].abs_path, 'r', encoding='utf-8') as handle:
            html_text = handle.read()
        self.assertIn('Hello selection.', html_text)
        self.assertIn('Image preview is unavailable: A ship', html_text)
        self.assertNotIn('<img', html_text.lower())

    def test_image_only_book_keeps_a_text_stand_in(self):
        epub_path = os.path.join(self.tmp, 'pictures.epub')
        opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Pictures</dc:title></metadata>
  <manifest>
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine><itemref idref="cover"/></spine>
</package>
"""
        with zipfile.ZipFile(epub_path, 'w') as archive:
            archive.writestr('META-INF/container.xml', CONTAINER.replace('OEBPS/content.opf', 'content.opf').encode('utf-8'))
            archive.writestr('content.opf', opf.encode('utf-8'))
            archive.writestr(
                'cover.xhtml',
                b'<html xmlns="http://www.w3.org/1999/xhtml"><body><img src="cover.jpg"/></body></html>',
            )
        parsed = epub_reader.parse_epub(epub_path, os.path.join(self.tmp, 'pictures'))
        self.assertEqual(len(parsed.chapters), 1)
        with open(parsed.chapters[0].abs_path, 'r', encoding='utf-8') as handle:
            html_text = handle.read()
        self.assertIn('Image preview is unavailable: cover.jpg', html_text)

    def test_rejects_non_zip(self):
        path = os.path.join(self.tmp, 'nope.epub')
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write('not an epub')
        with self.assertRaises(epub_reader.EpubError):
            epub_reader.parse_epub(path, os.path.join(self.tmp, 'extracted'))


class PromptTests(unittest.TestCase):
    def test_reader_prompt_includes_book_chapter_and_context(self):
        prefs = {
            'use_persona': True,
            'persona': 'Be brief.',
            'use_interface_language': False,
        }
        prompt = epub_reader.build_reader_prompt(
            {'title': 'Dune', 'author': 'Frank Herbert', 'publisher': ''},
            'Arrakis',
            'the spice',
            'Explain this.',
            before='before the line',
            after='after the line',
            prefs=prefs,
            i18n={'language_instruction_text': 'Please respond in {language_name}.'},
        )
        self.assertIn('Be brief.', prompt)
        self.assertIn('Title: Dune', prompt)
        self.assertIn('Author: Frank Herbert', prompt)
        self.assertNotIn('Publisher', prompt)
        self.assertIn('Arrakis', prompt)
        self.assertIn('before the line', prompt)
        self.assertIn('the spice', prompt)
        self.assertIn('after the line', prompt)
        self.assertIn('Explain this.', prompt)

    def test_reader_prompt_omits_unchecked_sections(self):
        prefs = {
            'reader_include_book': False,
            'reader_include_chapter': False,
            'reader_include_context': False,
            'reader_include_selection': True,
            'reader_include_note': False,
            'use_persona': False,
            'use_interface_language': False,
        }
        prompt = epub_reader.build_reader_prompt(
            {'title': 'Dune'},
            'Arrakis',
            'the spice',
            'Explain this.',
            before='before the line',
            after='after the line',
            prefs=prefs,
        )
        self.assertNotIn('Dune', prompt)
        self.assertNotIn('Arrakis', prompt)
        self.assertNotIn('before the line', prompt)
        self.assertNotIn('Explain this.', prompt)
        self.assertIn('the spice', prompt)
        self.assertNotIn('Explain this passage', prompt)
        self.assertNotIn("Reader's question", prompt)

    def test_reader_prompt_uses_saved_wording(self):
        prefs = {
            'reader_include_book': False,
            'reader_include_chapter': False,
            'reader_include_context': False,
            'reader_include_selection': False,
            'reader_include_note': True,
            'reader_prompt_intro': 'Stay with this chapter.',
            'reader_prompt_default_question': 'What is the narrator afraid of?',
            'use_persona': False,
            'use_interface_language': False,
        }
        prompt = epub_reader.build_reader_prompt(
            {'title': 'Dune'},
            'Arrakis',
            'the spice',
            '',
            prefs=prefs,
            i18n={'reader_prompt_intro': 'Default intro', 'reader_prompt_default_question': 'Default note'},
        )
        self.assertIn('Stay with this chapter.', prompt)
        self.assertIn('What is the narrator afraid of?', prompt)
        self.assertNotIn('Default intro', prompt)
        self.assertNotIn('Default note', prompt)

    def test_reader_preview_follows_checks_and_radius(self):
        full = epub_reader.build_reader_preview({'reader_context_chars': 2000})
        self.assertIn('Frankenstein', full)
        self.assertIn('Mary Shelley', full)
        self.assertIn('1818', full)
        self.assertIn('Chapter 5', full)
        self.assertIn('Ingolstadt', full)
        self.assertIn(epub_reader.READER_PREVIEW_SELECTION, full)
        self.assertIn('black lips', full)
        self.assertIn('Explain this passage', full)

        without_book = epub_reader.build_reader_preview({
            'reader_include_book': False,
            'reader_context_chars': 2000,
        })
        self.assertNotIn('Frankenstein', without_book)
        self.assertNotIn('Mary Shelley', without_book)

        without_note = epub_reader.build_reader_preview({
            'reader_include_note': False,
            'reader_context_chars': 2000,
        })
        self.assertNotIn('Explain this passage', without_note)
        self.assertNotIn("Reader's question", without_note)

        short = epub_reader.build_reader_preview({'reader_context_chars': 50})
        self.assertNotIn('Ingolstadt', short)
        self.assertNotIn('black lips', short)
        self.assertIn('candlewick', short)
        self.assertLess(len(short), len(full))

    def test_reader_context_chars_clamps_invalid_values(self):
        self.assertEqual(epub_reader.reader_context_chars({}), 500)
        self.assertEqual(epub_reader.reader_context_chars({'reader_context_chars': '120'}), 120)
        self.assertEqual(epub_reader.reader_context_chars({'reader_context_chars': 'nope'}), 500)
        self.assertEqual(epub_reader.reader_context_chars({'reader_context_chars': 9}), 50)
        self.assertEqual(epub_reader.reader_context_chars({'reader_context_chars': 99999}), 2000)

    def test_surrounding_context_uses_nearby_text(self):
        chapter = 'Alpha ' + ('word ' * 80) + 'the spice must flow ' + ('later ' * 80)
        before, after = epub_reader.surrounding_context(chapter, 'the spice must flow', radius=30)
        self.assertTrue(before.endswith('word'))
        self.assertTrue(after.startswith('later'))
        self.assertLessEqual(len(before), 30)
        self.assertLessEqual(len(after), 30)


class ReaderChromeTests(unittest.TestCase):
    def test_configured_models_skip_incomplete_entries(self):
        prefs = {
            'models': {
                'grok': {'model': 'grok-3', 'auth_token': 'token', 'display_name': 'Grok'},
                'blank': {'model': '   ', 'api_key': 'token'},
                'ollama': {'model': 'llama', 'provider_id': 'ollama', 'api_base_url': ''},
                'local': {
                    'model': 'llama',
                    'provider_id': 'ollama',
                    'api_base_url': 'http://127.0.0.1:11434',
                    'display_name': 'Ollama',
                },
            }
        }
        listed = epub_reader.list_configured_models(prefs, {'free': 'Free'})
        self.assertEqual(
            listed,
            [('grok', 'Grok - grok-3'), ('local', 'Ollama - llama')],
        )

    def test_reader_style_script_sets_size_line_height_and_theme(self):
        script = epub_reader.reader_style_script(18, 1.6, 'default')
        self.assertIn('font-size:18px', script)
        self.assertIn('line-height:1.6', script)
        self.assertNotIn('background:', script)
        sepia = epub_reader.reader_style_script(20, 1.8, 'sepia')
        self.assertIn('font-size:20px', sepia)
        self.assertIn('#f4ecd8', sepia)
        self.assertIn('#3b2f1e', sepia)
        self.assertIn("setProperty('color',fg,'important')", sepia)
        self.assertIn('line-height:1.8', sepia)
        night = epub_reader.reader_style_script(18, 1.6, 'night')
        self.assertIn('#e8e8e8', night)
        self.assertIn("querySelectorAll('body *')", night)

    def test_answer_stylesheet_uses_reader_font_settings(self):
        css = epub_reader.reader_answer_stylesheet(20, 1.8)
        self.assertIn('font-size: 20px', css)
        self.assertNotIn('line-height: 1.8', css)
        self.assertIn('.response-body', css)
        self.assertIn('h1, h2, h3, h4, h5, h6 { font-size: 20px; }', css)
        self.assertNotIn('font-size: 32px', css)
        self.assertEqual(epub_reader.reader_answer_line_px(18, 1.4), 25)
        self.assertEqual(epub_reader.reader_answer_line_px(20, 1.8), 36)

    def test_reader_answer_keeps_a_scrollbar_lane_on_macos(self):
        self.assertTrue(epub_reader.reader_answer_reserves_scrollbar_lane('darwin'))
        self.assertFalse(epub_reader.reader_answer_reserves_scrollbar_lane('win32'))
        self.assertEqual(epub_reader.reader_answer_margins(4, 0), (4, 4, 4, 4))
        self.assertEqual(
            epub_reader.reader_answer_margins(4, epub_reader.READER_ANSWER_SCROLLBAR_GUTTER),
            (4, 4, 20, 4),
        )


class ReadingProgressTests(unittest.TestCase):
    def test_progress_restores_the_saved_chapter_and_ratio(self):
        chapters = [
            epub_reader.Chapter('One', 'ops/c1.xhtml', '/tmp/c1.xhtml'),
            epub_reader.Chapter('Two', 'ops/c2.xhtml', '/tmp/c2.xhtml'),
        ]
        prefs = {}
        key = epub_reader.reader_book_key('/libraries/main', 42)
        self.assertEqual(epub_reader.reader_book_key('/libraries/main', 42), key)
        self.assertNotEqual(epub_reader.reader_book_key('/libraries/other', 42), key)
        stored = epub_reader.store_reader_progress(prefs, key, 'ops/c2.xhtml', 1.4)
        self.assertEqual(stored['ratio'], 1.0)
        entry = epub_reader.reader_progress_entry(prefs, key)
        self.assertEqual(entry['href'], 'ops/c2.xhtml')
        self.assertEqual(epub_reader.find_chapter_index(chapters, entry['href']), 1)
        self.assertIsNone(epub_reader.find_chapter_index(chapters, 'missing.xhtml'))
        renamed = [
            epub_reader.Chapter('Two', 'text/c2.xhtml', '/tmp/c2.xhtml'),
        ]
        self.assertEqual(epub_reader.find_chapter_index(renamed, 'ops/c2.xhtml'), 0)

    def test_progress_keeps_only_the_newest_books(self):
        prefs = {}
        for number in range(3):
            epub_reader.store_reader_progress(
                prefs, 'book-{0}'.format(number), 'c.xhtml', 0.2, limit=2,
            )
        self.assertEqual(list(prefs['reader_progress']), ['book-1', 'book-2'])

    def test_reader_window_size_stays_in_range(self):
        self.assertEqual(epub_reader.reader_window_size(900, 700), (900, 700))
        self.assertEqual(epub_reader.reader_window_size(10, 10), (640, 480))
        self.assertEqual(epub_reader.reader_window_size('nope', None), (1180, 760))
        self.assertEqual(epub_reader.reader_window_mode(True, True), 'fullscreen')
        self.assertEqual(epub_reader.reader_window_mode(False, True), 'maximized')
        self.assertEqual(epub_reader.reader_window_mode(False, False), 'normal')
        fitted = epub_reader.reader_client_geometry_for_frame(
            (0, 25, 1440, 850),
            (0, 0, 800, 600),
            (0, 22, 800, 578),
        )
        self.assertEqual(fitted, (0, 47, 1440, 828))
        self.assertAlmostEqual(epub_reader.reader_split_ratio(720, 420), 720 / 1140.0)
        self.assertEqual(epub_reader.reader_split_ratio(-1, 0), epub_reader.READER_SPLIT_DEFAULT)
        self.assertAlmostEqual(epub_reader.reader_split_ratio_value(0.4), 0.4)
        self.assertEqual(epub_reader.reader_split_ratio_value('nope'), epub_reader.READER_SPLIT_DEFAULT)
        self.assertEqual(epub_reader.reader_split_sizes(1000, 0.25), [250, 750])
        self.assertEqual(epub_reader.reader_split_sizes(1000, 0.01), [160, 840])

    def test_reader_history_uses_the_note_or_selection(self):
        self.assertEqual(
            epub_reader.reader_history_question('selected passage', 'Why this line?'),
            'Why this line?',
        )
        long_selection = 'word ' * 30
        preview = epub_reader.reader_history_question(long_selection, '')
        self.assertTrue(preview.endswith('...'))
        self.assertLessEqual(len(preview), 83)
        books = epub_reader.reader_history_books(7, {'title': 'Frankenstein', 'author': 'Mary Shelley'})
        self.assertEqual(books[0]['id'], 7)
        self.assertEqual(books[0]['authors'], ['Mary Shelley'])
        self.assertFalse(books[0]['deleted'])
        answer = epub_reader.history_answer_text({
            'answers': {'grok': {'answer': 'Because of the creature.'}},
        })
        self.assertEqual(answer, 'Because of the creature.')

    def test_retired_narrow_intro_falls_back_to_open_task(self):
        old = (
            'You are helping someone read a book. Use only the information below. '
            'Answer the reader\'s question. If there is no separate question, explain the selected passage.'
        )
        prompt = epub_reader.build_reader_prompt(
            {'title': 'Dune'},
            'Arrakis',
            'the spice',
            '',
            prefs={
                'reader_prompt_intro': old,
                'reader_include_book': False,
                'reader_include_chapter': False,
                'reader_include_context': False,
                'reader_include_selection': True,
                'reader_include_note': False,
                'use_persona': False,
                'use_interface_language': False,
            },
        )
        self.assertNotIn('Use only the information below', prompt)
        self.assertIn('your own knowledge', prompt)

class FormatListTests(unittest.TestCase):
    def test_string_and_new_api(self):
        class Legacy(object):
            def formats(self, book_id, index_is_id=False):
                return 'epub, PDF'

        class Api(object):
            def formats(self, book_id):
                return ['EPUB', 'mobi']

        class Modern(object):
            new_api = Api()

        self.assertEqual(epub_reader.list_book_formats(Legacy(), 1), ['EPUB', 'PDF'])
        self.assertEqual(epub_reader.list_book_formats(Modern(), 1), ['EPUB', 'MOBI'])


if __name__ == '__main__':
    unittest.main()
