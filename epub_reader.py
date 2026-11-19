#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scroll an EPUB inside the plugin and ask about the selected text.

The official calibre viewer is a separate process, so this dialog renders the
spine itself with the embedded browser and reuses the saved Ask prompt.
"""

import hashlib
import html
import logging
import os
import posixpath
import re
import shutil
import sys
import zipfile
from xml.etree import ElementTree

try:
    from .utils import (
        as_unicode_text,
        clean_prompt_metadata_text,
        is_placeholder_metadata,
        omit_placeholder_template_fields,
    )
except ImportError:
    from utils import (
        as_unicode_text,
        clean_prompt_metadata_text,
        is_placeholder_metadata,
        omit_placeholder_template_fields,
    )

logger = logging.getLogger(__name__)

_DOC_TYPES = {
    'application/xhtml+xml',
    'text/html',
    'application/html',
    'text/xml',
}
READER_CONTEXT_CHARS = 500
READER_CONTEXT_CHARS_MIN = 50
READER_CONTEXT_CHARS_MAX = 2000
READER_PROMPT_FLAGS = (
    'reader_include_book',
    'reader_include_chapter',
    'reader_include_context',
    'reader_include_selection',
    'reader_include_note',
)
READER_PREVIEW_BOOK = {
    'title': 'Frankenstein',
    'author': 'Mary Shelley',
    'publisher': 'Lackington, Hughes, Harding, Mavor & Jones',
    'pubyear': '1818',
    'language': 'English',
    'series': '',
}
READER_PROMPT_INTRO_FALLBACK = (
    'You are helping someone read a book. The book, chapter, and passage below are only '
    'context: they show what the reader is looking at. Answer from your own knowledge as well '
    'as that context. Do not limit the answer to what the excerpt already says, and do not '
    'refuse because the answer is not written there. If the reader does not add a separate '
    'question, explain the selected passage.'
)
_RETIRED_READER_INTROS = {
    'You are helping someone read a book. Use only the information below. '
    'Answer the reader\'s question. If there is no separate question, explain the selected passage.',
    '你在帮助读者理解一本书。只根据下面给出的信息回答。如果读者没有另写问题，就解释选中的段落。',
    '你在幫助讀者理解一本書。只根據下面給出的資訊回答。如果讀者沒有另寫問題，就解釋選取的段落。',
    '你喺度幫讀者理解一本書。只根據下面俾嘅資料回答。如果讀者冇另寫問題，就解釋選取嗰段。',
}
READER_PREVIEW_CHAPTER = 'Chapter 5'
READER_PREVIEW_SELECTION = (
    'It was on a dreary night of November that I beheld the accomplishment of my toils.'
)
READER_PREVIEW_BEFORE = (
    'Ingolstadt still held me in its laboratories. I paused, examining and analysing all the '
    'minutiae of causation, as exemplified in the change from life to death, and death to life, '
    'until from the midst of this darkness a sudden light broke in upon me, a light so brilliant '
    'and wondrous, yet so simple, that while I became dizzy with the immensity of the prospect '
    'which it illustrated, I was surprised that among so many men of genius who had directed '
    'their inquiries towards the same science, I alone should be reserved to discover so '
    'astonishing a secret. Remember, I am not recording the vision of a madman. The sun does not '
    'more certainly shine in the heavens than that which I now affirm is true. Some miracle might '
    'have produced it, yet the stages of the discovery were distinct and probable. After days and '
    'nights of incredible labour and fatigue, I succeeded in discovering the cause of generation '
    'and life; nay, more, I became myself capable of bestowing animation upon lifeless matter. '
    'The astonishment which I had at first experienced on this discovery soon gave place to '
    'delight and rapture. After so much time spent in painful labour, to arrive at once at the '
    'summit of my desires was the most gratifying consummation of my toils. What had been the '
    'study and desire of the wisest men since the creation of the world was now within my grasp. '
    'I prepared the instruments and watched the candlewick.'
)
READER_PREVIEW_AFTER = (
    'With an anxiety that almost amounted to agony, I collected the instruments of life around '
    'me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It '
    'was already one in the morning; the rain pattered dismally against the panes, and my candle '
    'was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull '
    'yellow eye of the creature open; it breathed hard, and a convulsive motion agitated its '
    'limbs. How can I describe my emotions at this catastrophe, or how delineate the wretch whom '
    'with such infinite pains and care I had endeavoured to form? His limbs were in proportion, '
    'and I had selected his features as beautiful. Beautiful! Great God! His yellow skin scarcely '
    'covered the work of muscles and arteries beneath; his hair was of a lustrous black, and '
    'flowing; his teeth of a pearly whiteness; but these luxuriances only formed a more horrid '
    'contrast with his watery eyes, that seemed almost of the same colour as the dun-white '
    'sockets in which they were set, his shrivelled complexion and straight black lips.'
)
_DEFAULT_TEMPLATE = (
    'User query: {query}\n'
    'Book title: {title}\n'
    'Author: {author}\n'
    'Publisher: {publisher}\n'
    'Publication year: {pubyear}\n'
    'Language: {language}\n'
    'Series: {series}'
)
_SELECTION_JS = r"""
(function () {
  if (window.__askAiSelectionBound) return;
  function report() {
    var text = '';
    try { text = String(window.getSelection() || ''); } catch (e) { return; }
    if (!text.replace(/^\s+|\s+$/g, '')) return;
    if (!window.__askAiBridge) return;
    window.__askAiBridge.setSelection(text);
  }
  function bind() {
    if (window.__askAiSelectionBound) return;
    if (typeof QWebChannel === 'undefined' || typeof qt === 'undefined') return;
    window.__askAiSelectionBound = true;
    new QWebChannel(qt.webChannelTransport, function (channel) {
      window.__askAiBridge = channel.objects.bridge;
      document.addEventListener('mouseup', report);
      document.addEventListener('keyup', report);
      var progressTimer = null;
      function reportProgress() {
        var el = document.scrollingElement || document.documentElement || document.body;
        if (!el || !window.__askAiBridge || !window.__askAiBridge.setProgress) return;
        var max = (el.scrollHeight || 0) - (el.clientHeight || 0);
        if (max < 1) return;
        window.__askAiBridge.setProgress(el.scrollTop / max);
      }
      window.addEventListener('scroll', function () {
        if (progressTimer) return;
        progressTimer = setTimeout(function () {
          progressTimer = null;
          reportProgress();
        }, 200);
      }, true);
    });
  }
  function start() {
    if (typeof QWebChannel !== 'undefined') {
      bind();
      return;
    }
    var script = document.createElement('script');
    script.src = 'qrc:///qtwebchannel/qwebchannel.js';
    script.onload = bind;
    (document.head || document.documentElement).appendChild(script);
  }
  start();
})();
"""


class EpubError(Exception):
    """EPUB export or parse failed."""


class WebEngineMissing(EpubError):
    """This calibre build has no Qt WebEngine."""


class Chapter(object):
    def __init__(self, title, rel_path, abs_path):
        self.title = title
        self.rel_path = rel_path
        self.abs_path = abs_path


class ParsedEpub(object):
    def __init__(self, title, chapters, root):
        self.title = title
        self.chapters = chapters
        self.root = root


def _local(tag):
    if not tag:
        return ''
    return tag.rsplit('}', 1)[-1]


def _norm_zip_path(path):
    path = (path or '').replace('\\', '/').strip()
    path = path.split('#', 1)[0]
    path = path.split('?', 1)[0]
    try:
        from urllib.parse import unquote
        path = unquote(path)
    except Exception:
        pass
    parts = []
    for part in path.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return '/'.join(parts)


def _join_href(base_dir, href):
    href = _norm_zip_path(href)
    if not base_dir or href.startswith('/'):
        return href.lstrip('/')
    return _norm_zip_path(posixpath.join(base_dir, href))


def _media_type(value):
    return (value or '').split(';', 1)[0].strip().lower()


def _text(node):
    if node is None:
        return ''
    return ''.join(node.itertext()).strip()


def _safe_extract(archive, dest):
    dest = os.path.abspath(dest)
    os.makedirs(dest, exist_ok=True)
    prefix = dest + os.sep
    for info in archive.infolist():
        name = _norm_zip_path(info.filename)
        if not name:
            continue
        target = os.path.abspath(os.path.join(dest, *name.split('/')))
        if target != dest and not target.startswith(prefix):
            continue
        if info.is_dir() or info.filename.endswith('/'):
            os.makedirs(target, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with archive.open(info) as src, open(target, 'wb') as out:
            shutil.copyfileobj(src, out)


def _read_xml(path):
    with open(path, 'rb') as handle:
        data = handle.read()
    data = re.sub(br'^\xef\xbb\xbf', b'', data)
    return ElementTree.fromstring(data)


def _opf_path(root):
    container = os.path.join(root, 'META-INF', 'container.xml')
    if not os.path.isfile(container):
        raise EpubError('META-INF/container.xml is missing')
    tree = _read_xml(container)
    for node in tree.iter():
        if _local(node.tag) == 'rootfile':
            full_path = node.attrib.get('full-path') or node.attrib.get('full-path'.upper())
            if full_path:
                return _norm_zip_path(full_path)
    raise EpubError('EPUB rootfile is missing')


def _manifest_and_spine(opf_path):
    tree = _read_xml(opf_path)
    manifest = {}
    spine = []
    title = ''
    for node in tree.iter():
        name = _local(node.tag)
        if name == 'title' and not title:
            title = _text(node)
        elif name == 'item':
            item_id = node.attrib.get('id') or ''
            href = node.attrib.get('href') or ''
            if not item_id or not href:
                continue
            manifest[item_id] = {
                'href': href,
                'media_type': _media_type(node.attrib.get('media-type')),
                'properties': node.attrib.get('properties') or '',
            }
        elif name == 'itemref':
            idref = node.attrib.get('idref') or ''
            if not idref:
                continue
            linear = (node.attrib.get('linear') or 'yes').lower() != 'no'
            spine.append((idref, linear))
    return title, manifest, spine


def _toc_map(root, opf_dir, manifest):
    titles = {}

    def remember(href, title):
        title = re.sub(r'\s+', ' ', (title or '')).strip()
        if not href or not title:
            return
        path = _join_href(opf_dir, href)
        titles.setdefault(path, title)

    nav_items = []
    ncx_items = []
    for item in manifest.values():
        props = set((item.get('properties') or '').split())
        if 'nav' in props:
            nav_items.append(item['href'])
        if item.get('media_type') == 'application/x-dtbncx+xml':
            ncx_items.append(item['href'])

    for href in nav_items:
        path = os.path.join(root, *_join_href(opf_dir, href).split('/'))
        if not os.path.isfile(path):
            continue
        try:
            tree = _read_xml(path)
        except ElementTree.ParseError:
            tree = None
        if tree is not None:
            for node in tree.iter():
                if _local(node.tag) != 'a':
                    continue
                remember(node.attrib.get('href'), _text(node))
            continue
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            raw = handle.read()
        for match in re.finditer(
            r'<a\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            raw,
            flags=re.I | re.S,
        ):
            remember(match.group(1), re.sub(r'<[^>]+>', ' ', match.group(2)))

    for href in ncx_items:
        path = os.path.join(root, *_join_href(opf_dir, href).split('/'))
        if not os.path.isfile(path):
            continue
        try:
            tree = _read_xml(path)
        except ElementTree.ParseError:
            continue
        for node in tree.iter():
            if _local(node.tag) != 'navPoint':
                continue
            label = ''
            src = ''
            for child in node.iter():
                cname = _local(child.tag)
                if cname == 'text' and not label:
                    label = _text(child)
                elif cname == 'content' and not src:
                    src = child.attrib.get('src') or ''
            remember(src, label)
    return titles


_BLOCK_RE = re.compile(r'<(script|style|head)\b[^>]*>.*?</\1>', re.I | re.S)
_BODY_RE = re.compile(r'<body\b[^>]*>(.*)</body>', re.I | re.S)
_SVG_RE = re.compile(r'<svg\b[^>]*>.*?</svg>', re.I | re.S)
_IMG_RE = re.compile(r'<img\b[^>]*/?>', re.I | re.S)
_OBJECT_RE = re.compile(r'<object\b[^>]*>.*?</object>|<object\b[^>]*/?>|<embed\b[^>]*/?>', re.I | re.S)
_ATTR_RE_CACHE = {}


def _attr(tag, name):
    pattern = _ATTR_RE_CACHE.get(name)
    if pattern is None:
        pattern = re.compile(
            r'\b' + re.escape(name) + r'\s*=\s*(["\'])(.*?)\1',
            re.I | re.S,
        )
        _ATTR_RE_CACHE[name] = pattern
    match = pattern.search(tag or '')
    if not match:
        return ''
    return html.unescape(match.group(2)).strip()


def _readable_text(raw):
    """Visible body text, ignoring head, scripts, and tags."""
    text = _BLOCK_RE.sub(' ', raw or '')
    body = _BODY_RE.search(text)
    if body:
        text = body.group(1)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def _image_name(tag, fallback):
    from urllib.parse import unquote
    alt = _attr(tag, 'alt')
    if alt:
        return alt
    src = _attr(tag, 'src') or _attr(tag, 'href') or _attr(tag, 'xlink:href') or _attr(tag, 'data')
    if src:
        name = os.path.basename(unquote(src.split('#', 1)[0].split('?', 1)[0]))
        if name:
            return name
    return fallback


def _placeholder_html(template, name):
    try:
        label = template.format(name=name)
    except Exception:
        label = template
    return '<p class="ask-ai-image-placeholder">{0}</p>'.format(html.escape(label))


def _rewrite_unsupported_images(raw, placeholder):
    """Replace img/svg/object with a text line. Images are not rendered here."""
    def svg_sub(match):
        return _placeholder_html(placeholder, _image_name(match.group(0), 'SVG'))

    def img_sub(match):
        return _placeholder_html(placeholder, _image_name(match.group(0), 'image'))

    def object_sub(match):
        return _placeholder_html(placeholder, _image_name(match.group(0), 'image'))

    updated = _SVG_RE.sub(svg_sub, raw)
    updated = _IMG_RE.sub(img_sub, updated)
    updated = _OBJECT_RE.sub(object_sub, updated)
    return updated


def _prepare_chapter_html(path, placeholder, keep_image_only=False):
    """Skip image-only documents unless the book has nothing else to show.

    Chapters that do have text get their pictures replaced with a short line.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            raw = handle.read()
    except OSError:
        return False
    if not _readable_text(raw) and not keep_image_only:
        return False
    updated = _rewrite_unsupported_images(raw, placeholder)
    if updated != raw:
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(updated)
    return True


def _heading_title(path):
    try:
        with open(path, 'rb') as handle:
            raw = handle.read(65536)
    except OSError:
        return ''
    text = raw.decode('utf-8', errors='replace')
    match = re.search(r'<h[1-3]\b[^>]*>(.*?)</h[1-3]>', text, flags=re.I | re.S)
    if not match:
        return ''
    title = re.sub(r'<[^>]+>', ' ', match.group(1))
    title = html.unescape(re.sub(r'\s+', ' ', title)).strip()
    return title[:180]


def parse_epub(epub_path, extract_dir, image_placeholder='Image preview is unavailable: {name}'):
    """Unzip an EPUB and return spine chapters in reading order."""
    if not zipfile.is_zipfile(epub_path):
        raise EpubError('File is not an EPUB zip')
    if os.path.isdir(extract_dir):
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(epub_path, 'r') as archive:
        _safe_extract(archive, extract_dir)

    opf_rel = _opf_path(extract_dir)
    opf_abs = os.path.join(extract_dir, *opf_rel.split('/'))
    if not os.path.isfile(opf_abs):
        raise EpubError('OPF file is missing')
    opf_dir = posixpath.dirname(opf_rel)
    title, manifest, spine = _manifest_and_spine(opf_abs)
    toc = _toc_map(extract_dir, opf_dir, manifest)

    def chapter_from(item_id, index, keep_image_only):
        item = manifest.get(item_id)
        if not item or item['media_type'] not in _DOC_TYPES:
            return None
        rel = _join_href(opf_dir, item['href'])
        abs_path = os.path.join(extract_dir, *rel.split('/'))
        if not os.path.isfile(abs_path):
            return None
        if not _prepare_chapter_html(abs_path, image_placeholder, keep_image_only):
            return None
        label = toc.get(rel) or _heading_title(abs_path) or 'Chapter {n}'.format(n=index)
        return Chapter(label, rel, abs_path)

    def collect(item_ids, keep_image_only):
        found = []
        for item_id in item_ids:
            chapter = chapter_from(item_id, len(found) + 1, keep_image_only)
            if chapter is not None:
                found.append(chapter)
        return found

    chosen = [item_id for item_id, linear in spine if linear]
    if not chosen:
        chosen = [item_id for item_id, _linear in spine]
    chapters = collect(chosen, keep_image_only=False)
    if not chapters:
        # Every spine document was a picture. Keep them and show a text stand-in.
        chapters = collect(chosen, keep_image_only=True)
    if not chapters:
        manifest_ids = list(manifest.keys())
        chapters = collect(manifest_ids, keep_image_only=False) or collect(manifest_ids, keep_image_only=True)
    return ParsedEpub(title or '', chapters, extract_dir)


READER_FONT_SIZES = (14, 16, 18, 20, 22, 24)
READER_LINE_HEIGHTS = (1.4, 1.6, 1.8, 2.0)
READER_THEMES = ('default', 'sepia', 'night')
_READER_THEME_COLORS = {
    'sepia': ('#f4ecd8', '#3b2f1e'),
    'night': ('#1c1c1c', '#e8e8e8'),
}


def list_configured_models(prefs, i18n=None):
    """Configured providers as (id, label), using the same checks as the Ask dialog."""
    try:
        from .models.base import LOCAL_OPENAI_COMPAT_PROVIDER_IDS, extract_provider_id
    except ImportError:
        import importlib.util
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'base.py')
        spec = importlib.util.spec_from_file_location('ask_ai_plugin_models_base', base_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        LOCAL_OPENAI_COMPAT_PROVIDER_IDS = module.LOCAL_OPENAI_COMPAT_PROVIDER_IDS
        extract_provider_id = module.extract_provider_id
    i18n = i18n or {}
    models_config = prefs.get('models', {}) or {}
    found = []
    for ai_id, config in models_config.items():
        if not isinstance(config, dict):
            continue
        if not as_unicode_text(config.get('model')).strip():
            continue
        provider_id = extract_provider_id(ai_id, config)
        if provider_id in LOCAL_OPENAI_COMPAT_PROVIDER_IDS:
            if not as_unicode_text(config.get('api_base_url')).strip():
                continue
        elif provider_id != 'nvidia_free' and ai_id != 'nvidia_free':
            token_field = 'auth_token' if provider_id == 'grok' else 'api_key'
            if not as_unicode_text(config.get(token_field)).strip():
                continue
        if provider_id == 'nvidia_free' or ai_id == 'nvidia_free':
            display_name = 'Nvidia AI ({0})'.format(i18n.get('free', 'Free'))
        else:
            display_name = config.get('display_name') or ai_id
        model_name = config.get('model') or 'unknown'
        found.append((ai_id, '{0} - {1}'.format(display_name, model_name)))
    return found


def reader_style_script(font_size, line_height, theme):
    """JavaScript that applies font size, line height, and an optional paper color."""
    try:
        size = int(font_size)
    except (TypeError, ValueError):
        size = 18
    size = max(12, min(size, 32))
    try:
        height = float(line_height)
    except (TypeError, ValueError):
        height = 1.6
    height = max(1.2, min(height, 2.4))
    height_text = '%.1f' % height
    colors = _READER_THEME_COLORS.get(theme or 'default')
    css = (
        'body,p,li,div,span,td,blockquote,a{{font-size:{size}px !important;'
        'line-height:{height} !important;}}'
        'h1{{font-size:{h1}px !important;line-height:{height} !important;}}'
        'h2{{font-size:{h2}px !important;line-height:{height} !important;}}'
        'h3{{font-size:{h3}px !important;line-height:{height} !important;}}'
    ).format(
        size=size,
        height=height_text,
        h1=int(size * 1.6),
        h2=int(size * 1.35),
        h3=int(size * 1.15),
    )
    css = css.replace('\\', '\\\\').replace("'", "\\'")
    if colors:
        bg, fg = colors
        color_js = (
            "var bg='%s',fg='%s';"
            "var root=document.documentElement;var body=document.body;"
            "if(root){root.style.setProperty('background-color',bg,'important');}"
            "if(body){body.style.setProperty('background-color',bg,'important');"
            "body.style.setProperty('color',fg,'important');}"
            "var nodes=document.querySelectorAll('body *');"
            "for(var i=0;i<nodes.length;i++){"
            "var el=nodes[i];"
            "el.style.setProperty('color',fg,'important');"
            "el.style.setProperty('-webkit-text-fill-color',fg,'important');"
            "var ns=el.namespaceURI||'';"
            "if(ns.indexOf('svg')!==-1){el.style.setProperty('fill',fg,'important');}"
            "}"
        ) % (bg, fg)
    else:
        color_js = (
            "var root=document.documentElement;var body=document.body;"
            "if(root){root.style.removeProperty('background-color');}"
            "if(body){body.style.removeProperty('background-color');"
            "body.style.removeProperty('color');}"
            "var nodes=document.querySelectorAll('body *');"
            "for(var i=0;i<nodes.length;i++){"
            "var el=nodes[i];"
            "el.style.removeProperty('color');"
            "el.style.removeProperty('-webkit-text-fill-color');"
            "el.style.removeProperty('fill');"
            "}"
        )
    return (
        "(function(){"
        "var style=document.getElementById('ask-ai-reader-style');"
        "if(!style){style=document.createElement('style');style.id='ask-ai-reader-style';"
        "(document.head||document.documentElement).appendChild(style);}"
        "style.textContent='%s';"
        "%s"
        "})();"
    ) % (css, color_js)


def reader_answer_stylesheet(font_size, line_height):
    """Markdown stylesheet for the reader reply, using the reading font settings."""
    try:
        size = int(font_size)
    except (TypeError, ValueError):
        size = 18
    size = max(12, min(size, 32))
    try:
        height = float(line_height)
    except (TypeError, ValueError):
        height = 1.6
    height = max(1.2, min(height, 2.4))
    try:
        from .ui_constants import get_response_content_stylesheet
    except ImportError:
        from ui_constants import get_response_content_stylesheet
    override = (
        '.response-body, p, li, blockquote, td, th, '
        'h1, h2, h3, h4, h5, h6 {{ font-size: {size}px; }}'
    ).format(size=size)
    return get_response_content_stylesheet() + override


READER_ANSWER_SCROLLBAR_GUTTER = 16


def reader_answer_reserves_scrollbar_lane(platform=None):
    """macOS draws the reader scrollbar over the reply, so that lane is reserved."""
    if platform is None:
        platform = sys.platform
    return platform == 'darwin'


def reader_answer_margins(base_margin, gutter=0):
    """Left, top, right, bottom. A positive gutter keeps the scrollbar off the text."""
    try:
        base = float(base_margin)
    except (TypeError, ValueError):
        base = 4
    if base < 0:
        base = 0
    try:
        extra = float(gutter)
    except (TypeError, ValueError):
        extra = 0
    if extra < 0:
        extra = 0
    return (base, base, base + extra, base)


def reader_answer_line_px(font_size, line_height):
    """Pixel line box matching the web view: font size times the chosen line height."""
    try:
        size = int(font_size)
    except (TypeError, ValueError):
        size = 18
    size = max(1, size)
    try:
        height = float(line_height)
    except (TypeError, ValueError):
        height = 1.6
    height = max(1.0, height)
    return max(size, int(round(size * height)))


READER_PROGRESS_LIMIT = 40
READER_WINDOW_DEFAULT = (1180, 760)


def reader_window_size(width, height, default=READER_WINDOW_DEFAULT):
    """Keep a restored reader window inside a usable range."""
    try:
        width = int(width)
        height = int(height)
    except (TypeError, ValueError):
        return default
    width = max(640, min(width, 8000))
    height = max(480, min(height, 8000))
    return width, height


def reader_window_mode(fullscreen, maximized):
    """Which window layout to restore. Filling the desktop wins over maximized."""
    if fullscreen:
        return 'fullscreen'
    if maximized:
        return 'maximized'
    return 'normal'


def reader_client_geometry_for_frame(avail, frame, inner):
    """Client rectangle that places the window frame on the usable desktop.

    ``avail``, ``frame`` and ``inner`` are ``(x, y, width, height)``.
    The frame includes the title bar; the usable desktop does not include
    the menu bar or dock.
    """
    ax, ay, aw, ah = avail
    fx, fy, fw, fh = frame
    ix, iy, iw, ih = inner
    dx = fx - ix
    dy = fy - iy
    return (
        int(ax - dx),
        int(ay - dy),
        max(1, int(aw - (fw - iw))),
        max(1, int(ah - (fh - ih))),
    )


READER_SPLIT_DEFAULT = 720 / 1140.0


def reader_split_ratio(left, right, default=None):
    """Left pane share of the reader splitter, kept inside a usable range."""
    if default is None:
        default = READER_SPLIT_DEFAULT
    try:
        left = float(left)
        right = float(right)
    except (TypeError, ValueError):
        return default
    total = left + right
    if total <= 0:
        return default
    ratio = left / total
    if ratio != ratio:
        return default
    return max(0.15, min(0.85, ratio))


def reader_split_ratio_value(value, default=None):
    """Stored left-pane share. Invalid values fall back to the default split."""
    if default is None:
        default = READER_SPLIT_DEFAULT
    try:
        ratio = float(value)
    except (TypeError, ValueError):
        return default
    if ratio != ratio:
        return default
    return max(0.15, min(0.85, ratio))


def reader_split_sizes(total, ratio, minimum=160):
    """Pixel widths that reproduce a saved left/right share."""
    try:
        total = int(total)
    except (TypeError, ValueError):
        total = 1140
    total = max(total, minimum * 2)
    ratio = reader_split_ratio_value(ratio)
    left = int(round(total * ratio))
    left = max(minimum, min(left, total - minimum))
    return [left, total - left]


def reader_book_key(library_path, book_id):
    """Stable progress key for one book in one calibre library."""
    text = '{0}\n{1}'.format(library_path or '', book_id)
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:20]


def find_chapter_index(chapters, href):
    """Return the spine index for a saved chapter path, or None."""
    target = _norm_zip_path(href)
    if not target:
        return None
    for index, chapter in enumerate(chapters or []):
        if _norm_zip_path(getattr(chapter, 'rel_path', '')) == target:
            return index
    base = target.split('/')[-1]
    if not base:
        return None
    matches = []
    for index, chapter in enumerate(chapters or []):
        if _norm_zip_path(getattr(chapter, 'rel_path', '')).split('/')[-1] == base:
            matches.append(index)
    if len(matches) == 1:
        return matches[0]
    return None


def reader_progress_entry(prefs, book_key):
    if not book_key or prefs is None or not hasattr(prefs, 'get'):
        return None
    store = prefs.get('reader_progress')
    if not isinstance(store, dict):
        return None
    entry = store.get(book_key)
    if not isinstance(entry, dict):
        return None
    href = as_unicode_text(entry.get('href')).strip()
    if not href:
        return None
    try:
        ratio = float(entry.get('ratio', 0))
    except (TypeError, ValueError):
        ratio = 0.0
    if ratio < 0:
        ratio = 0.0
    if ratio > 1:
        ratio = 1.0
    return {'href': href, 'ratio': ratio}


def store_reader_progress(prefs, book_key, href, ratio, limit=READER_PROGRESS_LIMIT):
    """Remember the chapter path and scroll ratio. Returns the stored entry."""
    if not book_key or prefs is None:
        return None
    href = _norm_zip_path(as_unicode_text(href))
    if not href:
        return None
    try:
        ratio = float(ratio)
    except (TypeError, ValueError):
        ratio = 0.0
    ratio = 0.0 if ratio < 0 else 1.0 if ratio > 1 else ratio
    store = prefs.get('reader_progress') if hasattr(prefs, 'get') else {}
    if not isinstance(store, dict):
        store = {}
    else:
        store = dict(store)
    store.pop(book_key, None)
    store[book_key] = {'href': href, 'ratio': round(ratio, 4)}
    while len(store) > limit:
        store.pop(next(iter(store)))
    prefs['reader_progress'] = store
    return store[book_key]


def reader_history_question(selection, note, limit=80):
    """Short text stored as the history question: the note, or the selection."""
    text = as_unicode_text(note).strip() or as_unicode_text(selection).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + '...'


def reader_history_books(book_id, book):
    """Book metadata in the same shape the ask window stores."""
    book = book or {}
    author = as_unicode_text(book.get('author')).strip()
    language = as_unicode_text(book.get('language')).strip()
    return [{
        'id': book_id,
        'title': as_unicode_text(book.get('title')),
        'authors': [author] if author else [],
        'publisher': as_unicode_text(book.get('publisher')),
        'pubdate': as_unicode_text(book.get('pubyear')),
        'languages': [language] if language else [],
        'series': as_unicode_text(book.get('series')),
        'deleted': False,
    }]


def history_answer_text(history):
    """Plain answer from one history record."""
    if not isinstance(history, dict):
        return ''
    answers = history.get('answers')
    chosen = None
    if isinstance(answers, dict) and answers:
        for key, value in answers.items():
            if key != 'default':
                chosen = value
                break
        if chosen is None:
            chosen = answers.get('default')
    elif history.get('answer'):
        chosen = history.get('answer')
    if isinstance(chosen, dict):
        return as_unicode_text(chosen.get('answer'))
    return as_unicode_text(chosen)


def list_book_formats(db, book_id):
    api = getattr(db, 'new_api', None) or db
    formats = None
    try:
        formats = api.formats(book_id)
    except TypeError:
        formats = db.formats(book_id, index_is_id=True)
    if not formats:
        return []
    if isinstance(formats, str):
        return [part.strip().upper() for part in formats.split(',') if part.strip()]
    return [str(part).strip().upper() for part in formats if str(part).strip()]


def export_epub(db, book_id, dest_path):
    """Copy the library EPUB to dest_path."""
    api = getattr(db, 'new_api', None) or db
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    with open(dest_path, 'wb') as handle:
        try:
            api.copy_format_to(book_id, 'EPUB', handle)
        except TypeError:
            handle.seek(0)
            handle.truncate()
            db.copy_format_to(book_id, 'EPUB', handle, index_is_id=True)
    if os.path.getsize(dest_path) > 0:
        return dest_path
    raw = None
    if hasattr(api, 'format'):
        try:
            raw = api.format(book_id, 'EPUB', as_path=False)
        except TypeError:
            raw = api.format(book_id, 'EPUB')
    if not raw and hasattr(db, 'format'):
        raw = db.format(book_id, 'EPUB', index_is_id=True)
    if not raw:
        raise EpubError('EPUB format is empty')
    with open(dest_path, 'wb') as handle:
        handle.write(raw)
    return dest_path


def chapter_plain_text(path):
    """Visible chapter text, with block tags turned into line breaks."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            raw = handle.read()
    except OSError:
        return ''
    text = _BLOCK_RE.sub(' ', raw or '')
    body = _BODY_RE.search(text)
    if body:
        text = body.group(1)
    text = re.sub(r'<(?:br|p|div|h[1-6]|li|tr|blockquote)\b[^>]*>', '\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text).replace('\xa0', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' *\n *', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def surrounding_context(chapter_text, selection, radius=READER_CONTEXT_CHARS):
    """Return text before and after the selection inside one chapter."""
    chapter = re.sub(r'\s+', ' ', chapter_text or '').strip()
    passage = re.sub(r'\s+', ' ', selection or '').strip()
    if not chapter or not passage:
        return '', ''
    index = chapter.find(passage)
    if index < 0:
        return '', ''
    start = max(0, index - radius)
    end = min(len(chapter), index + len(passage) + radius)
    before = chapter[start:index].strip()
    after = chapter[index + len(passage):end].strip()
    return before, after


def reader_context_chars(prefs, default=READER_CONTEXT_CHARS):
    """How many characters of chapter text to keep on each side of a selection."""
    raw = default
    if prefs is not None and hasattr(prefs, 'get'):
        raw = prefs.get('reader_context_chars', default)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = default
    if value < READER_CONTEXT_CHARS_MIN:
        return READER_CONTEXT_CHARS_MIN
    if value > READER_CONTEXT_CHARS_MAX:
        return READER_CONTEXT_CHARS_MAX
    return value


def reader_preview_chapter_text():
    return ' '.join((
        READER_PREVIEW_BEFORE,
        READER_PREVIEW_SELECTION,
        READER_PREVIEW_AFTER,
    ))


def _reader_flag(prefs, key):
    if prefs is None or not hasattr(prefs, 'get'):
        return True
    value = prefs.get(key, True)
    if isinstance(value, str):
        return value.strip().lower() not in ('0', 'false', 'no', 'off')
    return bool(value)


def _reader_label(i18n, key, fallback):
    if i18n is None:
        return fallback
    return i18n.get(key, fallback)


def stored_reader_intro(saved):
    """Drop the old instruction that told the model to use only the excerpt."""
    text = as_unicode_text(saved).strip()
    if text in _RETIRED_READER_INTROS:
        return ''
    return text


def _saved_reader_text(prefs, pref_key, i18n, i18n_key, fallback):
    saved = ''
    if prefs is not None and hasattr(prefs, 'get'):
        saved = as_unicode_text(prefs.get(pref_key, '')).strip()
    if pref_key == 'reader_prompt_intro':
        saved = stored_reader_intro(saved)
    if saved:
        return saved
    return _reader_label(i18n, i18n_key, fallback)


def build_reader_prompt(book, chapter_title, selection, note='', before='', after='',
                        prefs=None, i18n=None, use_saved_enhancements=False):
    """Assemble the reading-mode prompt from the checked sections."""
    if prefs is None:
        try:
            from .config import get_prefs
        except ImportError:
            from config import get_prefs
        prefs = get_prefs()
    i18n = i18n or {}
    book = book or {}
    intro = _saved_reader_text(
        prefs,
        'reader_prompt_intro',
        i18n,
        'reader_prompt_intro',
        READER_PROMPT_INTRO_FALLBACK,
    )
    lines = [intro] if intro else []

    if _reader_flag(prefs, 'reader_include_book'):
        fields = (
            ('reader_prompt_title', 'Title', 'title'),
            ('reader_prompt_author', 'Author', 'author'),
            ('reader_prompt_publisher', 'Publisher', 'publisher'),
            ('reader_prompt_pubyear', 'Publication year', 'pubyear'),
            ('reader_prompt_language', 'Language', 'language'),
            ('reader_prompt_series', 'Series', 'series'),
        )
        book_lines = []
        for label_key, fallback, field in fields:
            value = clean_prompt_metadata_text(as_unicode_text(book.get(field)))
            if field == 'title' and not value:
                value = 'Unknown'
            if field != 'title' and is_placeholder_metadata(value, field=field):
                continue
            book_lines.append('{0}: {1}'.format(
                _reader_label(i18n, label_key, fallback),
                value,
            ))
        if book_lines:
            lines.append('')
            lines.append(_reader_label(i18n, 'reader_prompt_book', 'Book'))
            lines.extend(book_lines)

    chapter = as_unicode_text(chapter_title).strip()
    if _reader_flag(prefs, 'reader_include_chapter') and chapter:
        lines.append('')
        lines.append(_reader_label(i18n, 'reader_prompt_chapter', 'Chapter'))
        lines.append(chapter)

    if _reader_flag(prefs, 'reader_include_context'):
        if as_unicode_text(before).strip():
            lines.append('')
            lines.append(_reader_label(i18n, 'reader_prompt_before', 'Before the selection'))
            lines.append(as_unicode_text(before).strip())
        if as_unicode_text(after).strip():
            lines.append('')
            lines.append(_reader_label(i18n, 'reader_prompt_after', 'After the selection'))
            lines.append(as_unicode_text(after).strip())

    selected = as_unicode_text(selection).strip()
    if _reader_flag(prefs, 'reader_include_selection') and selected:
        lines.append('')
        lines.append(_reader_label(i18n, 'reader_prompt_selection', 'Selected passage'))
        lines.append(selected)

    extra = as_unicode_text(note).strip()
    question = ''
    if _reader_flag(prefs, 'reader_include_note'):
        question = extra or _saved_reader_text(
            prefs,
            'reader_prompt_default_question',
            i18n,
            'reader_prompt_default_question',
            'Explain this passage using the chapter context.',
        )
    if question:
        lines.append('')
        lines.append(_reader_label(i18n, 'reader_prompt_question', 'Reader\'s question'))
        lines.append(question)

    prompt = '\n'.join(lines).strip()
    if use_saved_enhancements:
        try:
            try:
                from .prompts_widget import apply_prompt_enhancements
            except ImportError:
                from prompts_widget import apply_prompt_enhancements
            return apply_prompt_enhancements(prompt)
        except Exception:
            logger.info('Falling back to reader-local prompt enhancements')
    return _apply_local_enhancements(prompt, prefs, i18n)


def build_reader_preview(prefs=None, i18n=None):
    """Frankenstein sample used by the prompt settings page."""
    preview_prefs = dict(prefs or {})
    preview_prefs['use_persona'] = False
    preview_prefs['use_interface_language'] = False
    before, after = surrounding_context(
        reader_preview_chapter_text(),
        READER_PREVIEW_SELECTION,
        reader_context_chars(preview_prefs),
    )
    return build_reader_prompt(
        READER_PREVIEW_BOOK,
        READER_PREVIEW_CHAPTER,
        READER_PREVIEW_SELECTION,
        '',
        before,
        after,
        prefs=preview_prefs,
        i18n=i18n,
        use_saved_enhancements=False,
    )


def build_selection_prompt(book, selection, note='', prefs=None, i18n=None,
                           use_saved_enhancements=False):
    """Fill the saved single-book template. {query} is the selection plus note."""
    if prefs is None:
        try:
            from .config import get_prefs
        except ImportError:
            from config import get_prefs
        prefs = get_prefs()

    selected = as_unicode_text(selection).strip()
    extra = as_unicode_text(note).strip()
    if selected and extra:
        query = selected + '\n\n' + extra
    else:
        query = selected or extra

    template = as_unicode_text(prefs.get('template', '') if hasattr(prefs, 'get') else '')
    if not template.strip():
        template = _DEFAULT_TEMPLATE
    if '{query}' not in template and '{question}' in template:
        template = template.replace('{question}', '{query}')

    template_vars = {
        'query': query,
        'title': clean_prompt_metadata_text(as_unicode_text(book.get('title'))) or 'Unknown',
        'author': clean_prompt_metadata_text(as_unicode_text(book.get('author'))),
        'publisher': as_unicode_text(book.get('publisher')),
        'pubyear': as_unicode_text(book.get('pubyear')),
        'language': as_unicode_text(book.get('language')),
        'series': as_unicode_text(book.get('series')),
    }
    template = omit_placeholder_template_fields(template, template_vars)
    try:
        prompt = template.format(**template_vars)
    except KeyError as exc:
        raise EpubError('template:' + str(exc)) from exc

    if use_saved_enhancements:
        try:
            try:
                from .prompts_widget import apply_prompt_enhancements
            except ImportError:
                from prompts_widget import apply_prompt_enhancements
            return apply_prompt_enhancements(prompt)
        except Exception:
            logger.info('Falling back to reader-local prompt enhancements')
    return _apply_local_enhancements(prompt, prefs, i18n)


def _apply_local_enhancements(prompt, prefs, i18n):
    result = prompt
    use_persona = prefs.get('use_persona', True)
    if use_persona:
        persona = as_unicode_text(prefs.get('persona', '')).strip()
        if persona:
            result = persona + '\n\n' + result
    use_language = prefs.get('use_interface_language', False)
    if use_language and i18n is not None:
        lang_code = as_unicode_text(prefs.get('language', 'en')) or 'en'
        language_name = lang_code
        try:
            try:
                from .i18n import get_all_languages
            except ImportError:
                from i18n import get_all_languages
            language_name = get_all_languages().get(lang_code, lang_code)
        except Exception:
            language_name = lang_code
        instruction = i18n.get(
            'language_instruction_text',
            'Please respond in {language_name}.',
        )
        result = result + '\n\n' + instruction.format(language_name=language_name)
    return result


def book_prompt_fields(mi, language_name=''):
    """Map a calibre Metadata object onto the template fields."""
    authors = getattr(mi, 'authors', None) or []
    if isinstance(authors, str):
        author = authors
    else:
        author = ', '.join([as_unicode_text(item) for item in authors if item])
    pubyear = ''
    pubdate = getattr(mi, 'pubdate', None)
    if pubdate is not None and hasattr(pubdate, 'year') and pubdate.year and pubdate.year > 101:
        pubyear = str(pubdate.year)
    return {
        'id': getattr(mi, 'id', None),
        'title': as_unicode_text(getattr(mi, 'title', '')),
        'author': author,
        'publisher': as_unicode_text(getattr(mi, 'publisher', '')),
        'pubyear': pubyear,
        'language': as_unicode_text(language_name),
        'series': as_unicode_text(getattr(mi, 'series', '') or ''),
    }


def language_display_name(lang_code, unknown_label='Unknown'):
    if not lang_code:
        return ''
    code = as_unicode_text(lang_code).lower().strip()
    if code in ('und', 'un', 'zxx', 'unknown'):
        return unknown_label
    try:
        from calibre.utils.localization import calibre_langcode_to_name
        name = calibre_langcode_to_name(code)
        if name:
            return name
    except Exception:
        pass
    return code


def metadata_language_code(mi):
    languages = getattr(mi, 'languages', None)
    if languages:
        if isinstance(languages, (list, tuple)):
            return languages[0] if languages else ''
        return str(languages)
    return getattr(mi, 'language', '') or ''


def webengine_available():
    try:
        _import_webengine()
        return True
    except Exception:
        return False


def _import_webengine():
    try:
        from qt.webengine import (
            QWebChannel,
            QWebEnginePage,
            QWebEngineScript,
            QWebEngineSettings,
            QWebEngineView,
        )
    except ImportError:
        from PyQt5.QtWebChannel import QWebChannel
        from PyQt5.QtWebEngineWidgets import (
            QWebEnginePage,
            QWebEngineScript,
            QWebEngineSettings,
            QWebEngineView,
        )
    return {
        'QWebChannel': QWebChannel,
        'QWebEnginePage': QWebEnginePage,
        'QWebEngineScript': QWebEngineScript,
        'QWebEngineSettings': QWebEngineSettings,
        'QWebEngineView': QWebEngineView,
    }


def _enum_member(owner, group_name, name):
    group = getattr(owner, group_name, None)
    if group is not None and hasattr(group, name):
        return getattr(group, name)
    return getattr(owner, name)


def markdown_to_html(text):
    text = as_unicode_text(text)
    try:
        from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import markdown2
    except ImportError:
        from lib.ask_ai_plugin_vendor import markdown2
    return markdown2.markdown(text, extras={
        'fenced-code-blocks': None,
        'tables': None,
        'break-on-newline': None,
        'strike': None,
    })


def create_epub_ask_dialog(parent, api, book, chapters, temp_dir, i18n, book_key='', book_id=None):
    """Build the reader dialog. Imports Qt only when the window is opened."""
    if not chapters:
        raise EpubError('no chapters')
    try:
        web = _import_webengine()
    except Exception as exc:
        raise WebEngineMissing(str(exc)) from exc

    from PyQt5.QtCore import (
        QEasingCurve, QEvent, QObject, QPropertyAnimation, QRect, QThread, QTimer, Qt, QUrl,
        pyqtSignal, pyqtSlot,
    )
    from PyQt5.QtWidgets import (
        QApplication,
        QActionGroup,
        QComboBox,
        QDialog,
        QHBoxLayout,
        QLabel,
        QMenu,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSplitter,
        QTextBrowser,
        QTextEdit,
        QToolButton,
        QVBoxLayout,
        QWidget,
    )

    QWebChannel = web['QWebChannel']
    QWebEnginePage = web['QWebEnginePage']
    QWebEngineScript = web['QWebEngineScript']
    QWebEngineSettings = web['QWebEngineSettings']
    QWebEngineView = web['QWebEngineView']

    class SelectionBridge(QObject):
        selection_changed = pyqtSignal(str)
        progress_changed = pyqtSignal(float)

        @pyqtSlot(str)
        def setSelection(self, text):
            self.selection_changed.emit(text or '')

        @pyqtSlot(float)
        def setProgress(self, ratio):
            try:
                self.progress_changed.emit(float(ratio))
            except (TypeError, ValueError):
                return

    class AskWorker(QThread):
        chunk = pyqtSignal(str)
        succeeded = pyqtSignal(str)
        failed = pyqtSignal(str)

        def __init__(self, client, prompt, lang_code, model_id=None):
            super(AskWorker, self).__init__()
            self.client = client
            self.prompt = prompt
            self.lang_code = lang_code
            self.model_id = model_id

        def run(self):
            try:
                def on_chunk(text):
                    if text:
                        self.chunk.emit(text)

                answer = self.client.ask(
                    self.prompt,
                    lang_code=self.lang_code or 'en',
                    model_id=self.model_id,
                    stream=True,
                    stream_callback=on_chunk,
                )
                if not isinstance(answer, str):
                    answer = '' if answer is None else str(answer)
                self.succeeded.emit(answer)
            except Exception as exc:
                self.failed.emit(str(exc))

    class ReaderPage(QWebEnginePage):
        link_activated = pyqtSignal(object)

        def acceptNavigationRequest(self, url, nav_type, is_main_frame):
            link_type = _enum_member(
                QWebEnginePage, 'NavigationType', 'NavigationTypeLinkClicked',
            )
            if is_main_frame and nav_type == link_type:
                self.link_activated.emit(url)
                return False
            return super(ReaderPage, self).acceptNavigationRequest(url, nav_type, is_main_frame)

    class EpubAskDialog(QDialog):
        def __init__(self):
            super(EpubAskDialog, self).__init__(parent)
            self.api = api
            self.book = book
            self.chapters = list(chapters)
            self.temp_dir = temp_dir
            self.i18n = i18n
            self._index = 0
            self._request_token = 0
            self._worker = None
            self._workers = []
            self._closing = False
            self._busy = False
            self._selection = ''
            self._stream_text = ''
            self._follow_tail = True
            self._answer_pin_start = False
            self._pinning_answer = False
            self._pending_note = ''
            self._note_expanded = False
            self._loading = False
            self._loading_step = 0
            self._book_key = book_key or ''
            self._book_id = book_id
            self._history_uid = None
            self._asked_note = ''
            self._asked_selection = ''
            self._scroll_ratio = 0.0
            self._pending_ratio = None
            self._progress_hold = False
            self._model_id = None
            self._font_size = 18
            self._line_height = 1.6
            self._theme = 'default'
            self._window_width, self._window_height = READER_WINDOW_DEFAULT
            self._window_mode = 'normal'
            self._window_restored = False
            self._window_ready = False
            self._observed_special = False
            self._pending_normal_from = None
            self._applying_window_layout = False
            self._split_ratio = READER_SPLIT_DEFAULT
            self._split_restore_pending = True
            self._answer_home_anim = None
            self._answer_home_token = 0
            self._answer_scroll_animating = False
            self._answer_home_from_tail = False
            self._load_reader_prefs()
            self._observed_special = self._window_mode in ('fullscreen', 'maximized')

            title = book.get('title') or i18n.get('read_and_ask', 'Read and ask')
            self.setWindowTitle(i18n.get('read_window_title', 'Read and ask — {title}').format(title=title))
            self.resize(self._window_width, self._window_height)
            self._window_save_timer = QTimer(self)
            self._window_save_timer.setSingleShot(True)
            self._window_save_timer.timeout.connect(self._save_reader_window)
            self._window_mode_timer = QTimer(self)
            self._window_mode_timer.setSingleShot(True)
            self._window_mode_timer.timeout.connect(self._confirm_normal_window)
            self._answer_home_timer = QTimer(self)
            self._answer_home_timer.setSingleShot(True)
            self._answer_home_timer.timeout.connect(self._animate_answer_home)

            self.bridge = SelectionBridge(self)
            self.bridge.selection_changed.connect(self._on_selection)
            self.bridge.progress_changed.connect(self._on_reader_progress)

            root = QVBoxLayout(self)
            orientation = getattr(Qt, 'Horizontal', None)
            if orientation is None:
                orientation = Qt.Orientation.Horizontal
            splitter = QSplitter(orientation, self)
            splitter.setChildrenCollapsible(False)
            self.splitter = splitter
            root.addWidget(splitter)

            left = QWidget()
            left_layout = QVBoxLayout(left)
            left_layout.setContentsMargins(0, 0, 0, 0)
            nav = QHBoxLayout()
            self.prev_btn = QPushButton(i18n.get('read_prev_chapter', 'Previous'))
            self.next_btn = QPushButton(i18n.get('read_next_chapter', 'Next'))
            self.chapter_combo = QComboBox()
            for chapter in self.chapters:
                self.chapter_combo.addItem(chapter.title)
            self.prev_btn.clicked.connect(self._prev)
            self.next_btn.clicked.connect(self._next)
            nav.addWidget(self.prev_btn)
            nav.addWidget(self.chapter_combo, 1)
            nav.addWidget(self.next_btn)
            left_layout.addLayout(nav)

            style_row = QHBoxLayout()
            self.font_size_label = QLabel(i18n.get('read_font_size', 'Font size'))
            style_row.addWidget(self.font_size_label)
            self.font_size_combo = QComboBox()
            for size in READER_FONT_SIZES:
                self.font_size_combo.addItem(str(size), size)
            style_row.addWidget(self.font_size_combo)
            self.line_height_label = QLabel(i18n.get('read_line_height', 'Line height'))
            style_row.addWidget(self.line_height_label)
            self.line_height_combo = QComboBox()
            for height in READER_LINE_HEIGHTS:
                self.line_height_combo.addItem('%.1f' % height, height)
            style_row.addWidget(self.line_height_combo)
            self.theme_label = QLabel(i18n.get('read_theme', 'Style'))
            style_row.addWidget(self.theme_label)
            self.theme_combo = QComboBox()
            for theme_id, label_key, fallback in (
                ('default', 'read_theme_default', 'Default'),
                ('sepia', 'read_theme_sepia', 'Sepia'),
                ('night', 'read_theme_night', 'Night'),
            ):
                self.theme_combo.addItem(i18n.get(label_key, fallback), theme_id)
            style_row.addWidget(self.theme_combo)
            self.fullscreen_btn = QPushButton(i18n.get('read_fullscreen', 'Full screen'))
            self.fullscreen_btn.setCheckable(True)
            self.fullscreen_btn.clicked.connect(self._toggle_fullscreen)
            self._sync_fullscreen_button()
            style_row.addWidget(self.fullscreen_btn)
            style_row.addStretch(1)
            left_layout.addLayout(style_row)
            self._select_combo_data(self.font_size_combo, self._font_size)
            self._select_combo_data(self.line_height_combo, self._line_height)
            self._select_combo_data(self.theme_combo, self._theme)
            self.font_size_combo.currentIndexChanged.connect(self._on_style_changed)
            self.line_height_combo.currentIndexChanged.connect(self._on_style_changed)
            self.theme_combo.currentIndexChanged.connect(self._on_style_changed)

            self.view = QWebEngineView(left)
            page = ReaderPage(self.view)
            self.view.setPage(page)
            page.link_activated.connect(self._on_link)
            page.loadFinished.connect(self._apply_reader_style)
            self._install_selection_script(page)
            channel = QWebChannel(page)
            channel.registerObject('bridge', self.bridge)
            page.setWebChannel(channel)
            self._channel = channel
            settings = self.view.settings()
            for name, enabled in (
                ('JavascriptEnabled', True),
                ('LocalContentCanAccessFileUrls', True),
                ('LocalContentCanAccessRemoteUrls', False),
            ):
                try:
                    settings.setAttribute(
                        _enum_member(QWebEngineSettings, 'WebAttribute', name),
                        enabled,
                    )
                except Exception:
                    logger.info('WebEngine setting %s is unavailable', name)
            left_layout.addWidget(self.view, 1)

            right = QWidget()
            right_layout = QVBoxLayout(right)
            right_layout.setContentsMargins(8, 0, 0, 0)
            model_row = QHBoxLayout()
            self.model_label = QLabel(i18n.get('read_model', 'Model'))
            model_row.addWidget(self.model_label)
            self.model_combo = QComboBox()
            self._fill_model_combo()
            self.model_combo.currentIndexChanged.connect(self._on_model_changed)
            model_row.addWidget(self.model_combo, 1)
            right_layout.addLayout(model_row)
            self.history_button = QToolButton()
            self.history_button.setText(i18n.get('history', 'History'))
            text_only = getattr(Qt, 'ToolButtonTextOnly', None)
            if text_only is None:
                text_only = Qt.ToolButtonStyle.ToolButtonTextOnly
            self.history_button.setToolButtonStyle(text_only)
            popup = getattr(QToolButton, 'InstantPopup', None)
            if popup is None:
                popup = QToolButton.ToolButtonPopupMode.InstantPopup
            self.history_button.setPopupMode(popup)
            self.history_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.history_menu = QMenu(self.history_button)
            self.history_button.setMenu(self.history_menu)
            self.history_menu.aboutToShow.connect(self._reload_reader_history_menu)
            right_layout.addWidget(self.history_button)
            self.status_label = QLabel('')
            self.status_label.setWordWrap(True)
            self.status_label.setVisible(False)
            right_layout.addWidget(self.status_label)
            self.answer = QTextBrowser()
            self.answer.setOpenExternalLinks(True)
            self.answer.setPlaceholderText(i18n.get(
                'read_answer_placeholder',
                'Select text in the book, then ask. The reply shows here.',
            ))
            try:
                from .ui_constants import get_response_area_qss
            except ImportError:
                from ui_constants import get_response_area_qss
            self.answer.setStyleSheet(get_response_area_qss())
            self._apply_answer_style()
            scroll_policy = getattr(Qt, 'ScrollBarAsNeeded', None)
            if scroll_policy is None:
                scroll_policy = Qt.ScrollBarPolicy.ScrollBarAsNeeded
            self.answer.setVerticalScrollBarPolicy(scroll_policy)
            self._reserve_answer_scrollbar_lane()
            self.answer.verticalScrollBar().valueChanged.connect(self._on_answer_scroll)
            self.answer.verticalScrollBar().sliderPressed.connect(self._stop_answer_scroll_animation)
            self.answer.viewport().installEventFilter(self)
            right_layout.addWidget(self.answer, 1)

            self._stream_timer = QTimer(self)
            self._stream_timer.setSingleShot(True)
            self._stream_timer.timeout.connect(self._flush_stream_render)
            self._loading_timer = QTimer(self)
            self._loading_timer.timeout.connect(self._advance_loading)
            self._progress_timer = QTimer(self)
            self._progress_timer.setSingleShot(True)
            self._progress_timer.timeout.connect(self._flush_reader_progress)

            composer = QHBoxLayout()
            self.note_edit = QTextEdit()
            self.note_edit.setPlaceholderText(i18n.get(
                'read_note_placeholder',
                'Optional note. Enter sends it with the selected text.',
            ))
            self.note_edit.installEventFilter(self)
            app = QApplication.instance()
            if app is not None:
                app.installEventFilter(self)
            self._set_note_expanded(False)
            composer.addWidget(self.note_edit, 1)
            self.send_btn = QPushButton(i18n.get('read_send', 'Ask'))
            self.stop_btn = QPushButton(i18n.get('read_stop', 'Stop'))
            self.stop_btn.setVisible(False)
            self.send_btn.clicked.connect(self._ask)
            self.stop_btn.clicked.connect(self._stop)
            composer.addWidget(self.send_btn)
            composer.addWidget(self.stop_btn)
            right_layout.addLayout(composer)

            splitter.addWidget(left)
            splitter.addWidget(right)
            splitter.setStretchFactor(0, 1)
            splitter.setStretchFactor(1, 1)
            splitter.setSizes(reader_split_sizes(1140, self._split_ratio))
            splitter.splitterMoved.connect(self._on_splitter_moved)
            self.chapter_combo.currentIndexChanged.connect(self._show_chapter)
            start_index = 0
            start_ratio = None
            saved = self._saved_progress()
            if saved:
                found = find_chapter_index(self.chapters, saved['href'])
                if found is not None:
                    start_index = found
                    start_ratio = saved['ratio']
            self._show_chapter(start_index, restore_ratio=start_ratio)

        def _install_selection_script(self, page):
            script = QWebEngineScript()
            script.setName('ask-ai-selection')
            script.setInjectionPoint(_enum_member(
                QWebEngineScript, 'InjectionPoint', 'DocumentReady',
            ))
            script.setWorldId(_enum_member(
                QWebEngineScript, 'ScriptWorldId', 'MainWorld',
            ))
            script.setRunsOnSubFrames(False)
            script.setSourceCode(_SELECTION_JS)
            page.scripts().insert(script)

        def _load_reader_prefs(self):
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                prefs = get_prefs()
            except Exception:
                prefs = {}
            self._font_size = self._pref_choice(prefs, 'reader_font_size', READER_FONT_SIZES, 18)
            self._line_height = self._pref_choice(prefs, 'reader_line_height', READER_LINE_HEIGHTS, 1.6)
            theme = prefs.get('reader_theme', 'default') if hasattr(prefs, 'get') else 'default'
            self._theme = theme if theme in READER_THEMES else 'default'
            selected = prefs.get('selected_model') if hasattr(prefs, 'get') else None
            self._model_id = selected
            if hasattr(prefs, 'get'):
                self._window_width, self._window_height = reader_window_size(
                    prefs.get('reader_window_width'),
                    prefs.get('reader_window_height'),
                )
                self._window_mode = reader_window_mode(
                    bool(prefs.get('reader_window_fullscreen', False)),
                    bool(prefs.get('reader_window_maximized', False)),
                )
                self._split_ratio = reader_split_ratio_value(
                    prefs.get('reader_split_ratio', READER_SPLIT_DEFAULT),
                )

        def _pref_choice(self, prefs, key, choices, default):
            value = prefs.get(key, default) if hasattr(prefs, 'get') else default
            for choice in choices:
                if value == choice or str(value) == str(choice):
                    return choice
            return default

        def _select_combo_data(self, combo, value):
            index = combo.findData(value)
            if index < 0:
                index = 0
            combo.blockSignals(True)
            combo.setCurrentIndex(index)
            combo.blockSignals(False)

        def _fill_model_combo(self):
            models = []
            selected = self._model_id
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                prefs = get_prefs()
                models = list_configured_models(prefs, self.i18n)
                selected = prefs.get('selected_model') or selected
            except Exception:
                logger.info('Reader could not list configured models')
            self.model_combo.blockSignals(True)
            self.model_combo.clear()
            for ai_id, label in models:
                self.model_combo.addItem(label, ai_id)
            if not models:
                fallback = selected or self.i18n.get('read_model', 'Model')
                try:
                    fallback = self.api.model_display_name or fallback
                except Exception:
                    pass
                self.model_combo.addItem(as_unicode_text(fallback), selected)
            index = self.model_combo.findData(selected)
            if index < 0:
                index = 0
            self.model_combo.setCurrentIndex(index)
            self._model_id = self.model_combo.currentData()
            self.model_combo.blockSignals(False)

        def _on_model_changed(self):
            ai_id = self.model_combo.currentData()
            if not ai_id:
                return
            self._model_id = ai_id
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                get_prefs()['selected_model'] = ai_id
            except Exception:
                logger.info('Reader model switch was not saved')

        def _on_style_changed(self):
            self._font_size = self.font_size_combo.currentData() or self._font_size
            self._line_height = self.line_height_combo.currentData() or self._line_height
            self._theme = self.theme_combo.currentData() or 'default'
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                prefs = get_prefs()
                prefs['reader_font_size'] = self._font_size
                prefs['reader_line_height'] = self._line_height
                prefs['reader_theme'] = self._theme
            except Exception:
                logger.info('Reader style was not saved')
            self._apply_reader_style()
            self._apply_answer_style()

        def _apply_reader_style(self, _ok=True):
            if self._closing:
                return
            script = reader_style_script(self._font_size, self._line_height, self._theme)
            ratio = self._pending_ratio
            def after_style(_value=None):
                if self._closing:
                    return
                if ratio is not None:
                    self._scroll_reader_to(ratio)
                else:
                    self._progress_hold = False
            try:
                self.view.page().runJavaScript(script, after_style)
            except TypeError:
                try:
                    self.view.page().runJavaScript(script)
                except Exception:
                    logger.info('Reader style could not be applied')
                if ratio is not None:
                    QTimer.singleShot(120, lambda: self._scroll_reader_to(ratio))
            except Exception:
                logger.info('Reader style could not be applied')

        def _apply_answer_style(self):
            css = reader_answer_stylesheet(self._font_size, self._line_height)
            document = self.answer.document()
            document.setDefaultStyleSheet(css)
            font = self.answer.font()
            font.setPixelSize(int(self._font_size))
            self.answer.setFont(font)
            document.setDefaultFont(font)
            if self._stream_text:
                self._render_answer(self._stream_text)
            elif self._loading:
                self._show_loading_frame()
            else:
                self._apply_answer_line_height()

        def _show_chapter(self, index, url=None, restore_ratio=None):
            if index < 0 or index >= len(self.chapters):
                return
            self._index = index
            self.chapter_combo.blockSignals(True)
            self.chapter_combo.setCurrentIndex(index)
            self.chapter_combo.blockSignals(False)
            self.prev_btn.setEnabled(index > 0)
            self.next_btn.setEnabled(index < len(self.chapters) - 1)
            if restore_ratio is not None:
                try:
                    self._pending_ratio = max(0.0, min(1.0, float(restore_ratio)))
                except (TypeError, ValueError):
                    self._pending_ratio = 0.0
            elif url is None:
                self._pending_ratio = 0.0
            else:
                self._pending_ratio = None
                self._scroll_ratio = 0.0
            self._progress_hold = True
            if self._pending_ratio is not None:
                self._scroll_ratio = self._pending_ratio
                self._schedule_progress_save()
            target = url or QUrl.fromLocalFile(self.chapters[index].abs_path)
            self.view.load(target)

        def _saved_progress(self):
            if not self._book_key:
                return None
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                return reader_progress_entry(get_prefs(), self._book_key)
            except Exception:
                logger.info('Saved reading position could not be read')
                return None

        def _on_reader_progress(self, ratio):
            if self._closing or self._progress_hold or self._pending_ratio is not None:
                return
            try:
                ratio = max(0.0, min(1.0, float(ratio)))
            except (TypeError, ValueError):
                return
            if abs(ratio - self._scroll_ratio) < 0.004:
                return
            self._scroll_ratio = ratio
            self._schedule_progress_save()

        def _schedule_progress_save(self):
            timer = getattr(self, '_progress_timer', None)
            if timer is not None:
                timer.start(600)

        def _flush_reader_progress(self):
            if not self._book_key or not self.chapters:
                return
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                prefs = get_prefs()
                store_reader_progress(
                    prefs,
                    self._book_key,
                    self.chapters[self._index].rel_path,
                    self._scroll_ratio,
                )
                if hasattr(prefs, 'commit'):
                    prefs.commit()
            except Exception:
                logger.info('Reading position was not saved')

        def _scroll_reader_to(self, ratio):
            if self._closing:
                return
            try:
                ratio = max(0.0, min(1.0, float(ratio)))
            except (TypeError, ValueError):
                ratio = 0.0
            self._pending_ratio = ratio
            script = (
                '(function(){var el=document.scrollingElement||document.documentElement'
                '||document.body;if(!el)return;var max=Math.max((el.scrollHeight||0)'
                '-(el.clientHeight||0),0);el.scrollTop=max*%s;})();'
            ) % ('%.4f' % ratio)
            try:
                self.view.page().runJavaScript(script)
            except Exception:
                logger.info('Reading position could not be restored')
            QTimer.singleShot(400, self._finish_scroll_restore)

        def _finish_scroll_restore(self):
            if self._pending_ratio is None:
                return
            self._scroll_ratio = self._pending_ratio
            self._pending_ratio = None
            self._progress_hold = False

        def _prev(self):
            self._show_chapter(self._index - 1)

        def _next(self):
            self._show_chapter(self._index + 1)

        def _on_link(self, url):
            path = ''
            try:
                path = url.toLocalFile()
            except Exception:
                path = ''
            if not path:
                return
            target = os.path.abspath(path)
            for index, chapter in enumerate(self.chapters):
                if os.path.abspath(chapter.abs_path) == target:
                    self._show_chapter(index, url)
                    return
            extract_root = os.path.abspath(self.temp_dir)
            if target.startswith(extract_root + os.sep):
                self.view.load(url)

        def _qt_flag(self, group, name):
            if hasattr(Qt, name):
                return getattr(Qt, name)
            return getattr(getattr(Qt, group), name)

        def _set_note_expanded(self, expanded):
            self._note_expanded = bool(expanded)
            height = 96 if self._note_expanded else 36
            self.note_edit.setMinimumHeight(height)
            self.note_edit.setMaximumHeight(height)

        def _global_event_pos(self, event):
            if hasattr(event, 'globalPosition'):
                return event.globalPosition().toPoint()
            return event.globalPos()

        def _press_inside_widget(self, widget, event):
            if widget is None or not widget.isVisible():
                return False
            try:
                pos = self._global_event_pos(event)
            except Exception:
                return False
            return QRect(widget.mapToGlobal(widget.rect().topLeft()), widget.rect().size()).contains(pos)

        def _collapse_note_if_unfocused(self):
            if self._closing or not self._note_expanded:
                return
            focus = QApplication.focusWidget()
            if focus is self.note_edit or (focus is not None and self.note_edit.isAncestorOf(focus)):
                return
            if focus in (getattr(self, 'send_btn', None), getattr(self, 'stop_btn', None)):
                return
            self._set_note_expanded(False)

        def _event_type(self, name):
            if hasattr(QEvent, name):
                return getattr(QEvent, name)
            return getattr(QEvent.Type, name)

        def eventFilter(self, obj, event):
            answer = getattr(self, 'answer', None)
            if (
                answer is not None
                and obj is answer.viewport()
                and event.type() == self._event_type('Wheel')
                and getattr(self, '_answer_scroll_animating', False)
            ):
                self._stop_answer_scroll_animation()
            if obj is getattr(self, 'note_edit', None):
                if event.type() == self._event_type('FocusIn'):
                    self._set_note_expanded(True)
                elif event.type() == self._event_type('FocusOut'):
                    QTimer.singleShot(0, self._collapse_note_if_unfocused)
                elif event.type() == self._event_type('KeyPress'):
                    enter = event.key() in (
                        self._qt_flag('Key', 'Key_Return'),
                        self._qt_flag('Key', 'Key_Enter'),
                    )
                    shift = self._qt_flag('KeyboardModifier', 'ShiftModifier')
                    if enter and not (event.modifiers() & shift):
                        self._ask()
                        return True
            elif (
                event.type() == self._event_type('MouseButtonPress')
                and getattr(self, '_note_expanded', False)
                and not self._closing
            ):
                inside_note = self._press_inside_widget(getattr(self, 'note_edit', None), event)
                inside_action = self._press_inside_widget(getattr(self, 'send_btn', None), event)
                inside_action = inside_action or self._press_inside_widget(getattr(self, 'stop_btn', None), event)
                if not inside_note and not inside_action:
                    self._set_note_expanded(False)
            return super(EpubAskDialog, self).eventFilter(obj, event)

        def _set_status(self, text):
            text = as_unicode_text(text).strip()
            self.status_label.setText(text)
            self.status_label.setVisible(bool(text))

        def _on_selection(self, text):
            text = as_unicode_text(text).strip()
            if not text or text == self._selection:
                return
            self._selection = text
            if not self._busy and not self._stream_text:
                self._set_status(self.i18n.get(
                    'read_selection_count', '{n} characters selected',
                ).format(n=len(text)))

        def _set_busy(self, busy):
            self._busy = busy
            self.send_btn.setVisible(not busy)
            self.stop_btn.setVisible(busy)
            self.note_edit.setReadOnly(busy)
            if busy:
                self._set_status('')

        def _on_answer_scroll(self, value):
            if getattr(self, '_answer_scroll_animating', False):
                return
            bar = self.answer.verticalScrollBar()
            if not bar:
                return
            if value > bar.minimum() + 8:
                self._answer_pin_start = False
                self._answer_home_from_tail = False
            self._follow_tail = value >= bar.maximum() - 8

        def _reserve_answer_scrollbar_lane(self):
            document = self.answer.document()
            gutter = READER_ANSWER_SCROLLBAR_GUTTER if reader_answer_reserves_scrollbar_lane() else 0
            left, top, right, bottom = reader_answer_margins(document.documentMargin(), gutter)
            root = document.rootFrame()
            fmt = root.frameFormat()
            fmt.setLeftMargin(left)
            fmt.setTopMargin(top)
            fmt.setRightMargin(right)
            fmt.setBottomMargin(bottom)
            root.setFrameFormat(fmt)

        def _watch_answer_document_size(self):
            layout = self.answer.document().documentLayout()
            if layout is None:
                return
            try:
                layout.documentSizeChanged.disconnect(self._on_answer_document_resized)
            except Exception:
                pass
            layout.documentSizeChanged.connect(self._on_answer_document_resized)

        def _on_answer_document_resized(self, *_args):
            if not getattr(self, '_answer_pin_start', False):
                return
            self._schedule_answer_home()

        def _move_answer_cursor_home(self):
            from PyQt5.QtGui import QTextCursor
            cursor = self.answer.textCursor()
            start = getattr(QTextCursor, 'Start', None)
            if start is None:
                start = QTextCursor.MoveOperation.Start
            cursor.movePosition(start)
            self.answer.setTextCursor(cursor)

        def _render_answer(self, text, scroll_to_start=False):
            bar = self.answer.verticalScrollBar()
            was_following = self._follow_tail
            self._cancel_answer_home_animation()
            if scroll_to_start:
                self._answer_pin_start = True
                self._follow_tail = False
                self._answer_home_from_tail = was_following
            else:
                self._answer_pin_start = False
                self._answer_home_from_tail = False
            follow = self._follow_tail and not scroll_to_start
            old_value = bar.value() if bar else 0
            try:
                bar.valueChanged.disconnect(self._on_answer_scroll)
            except Exception:
                pass
            try:
                body = markdown_to_html(text or '')
                self.answer.setHtml('<div class="response-body">{0}</div>'.format(body))
            except Exception:
                logger.exception('Failed to render reader answer as markdown')
                self.answer.setPlainText(text or '')
            self._apply_answer_line_height()
            self._reserve_answer_scrollbar_lane()
            if scroll_to_start:
                self._watch_answer_document_size()
            if bar:
                if scroll_to_start:
                    if self._answer_home_from_tail and bar.maximum() > bar.minimum():
                        bar.setValue(bar.maximum())
                elif follow:
                    bar.setValue(bar.maximum())
                else:
                    bar.setValue(min(old_value, bar.maximum()))
                bar.valueChanged.connect(self._on_answer_scroll)
            if scroll_to_start:
                self._schedule_answer_home()

        def _animation_is_running(self, anim):
            if anim is None:
                return False
            running = getattr(QPropertyAnimation, 'Running', None)
            if running is None:
                running = getattr(getattr(QPropertyAnimation, 'State', None), 'Running', None)
            try:
                return anim.state() == running
            except Exception:
                return False

        def _cancel_answer_home_animation(self):
            self._answer_home_token = getattr(self, '_answer_home_token', 0) + 1
            timer = getattr(self, '_answer_home_timer', None)
            if timer is not None:
                timer.stop()
            anim = getattr(self, '_answer_home_anim', None)
            if self._animation_is_running(anim):
                anim.stop()
            self._answer_scroll_animating = False

        def _stop_answer_scroll_animation(self):
            self._cancel_answer_home_animation()
            self._answer_pin_start = False
            self._answer_home_from_tail = False

        def _schedule_answer_home(self):
            if self._closing or not getattr(self, '_answer_pin_start', False):
                return
            if self._animation_is_running(getattr(self, '_answer_home_anim', None)):
                return
            timer = getattr(self, '_answer_home_timer', None)
            if timer is not None:
                timer.start(60)

        def _set_answer_scroll(self, value):
            bar = self.answer.verticalScrollBar()
            if bar is None:
                return
            self._answer_scroll_animating = True
            try:
                bar.setValue(value)
            finally:
                self._answer_scroll_animating = False

        def _animate_answer_home(self):
            if self._closing or not getattr(self, '_answer_pin_start', False):
                return
            bar = self.answer.verticalScrollBar()
            if bar is None:
                return
            end = bar.minimum()
            start = bar.value()
            if self._answer_home_from_tail and start <= end + 8 and bar.maximum() > end + 24:
                start = bar.maximum()
            self._answer_scroll_animating = True
            try:
                self._move_answer_cursor_home()
                bar.setValue(start)
            finally:
                self._answer_scroll_animating = False
            if start <= end + 2:
                self._finish_answer_home()
                return
            easing = getattr(QEasingCurve, 'OutCubic', None)
            if easing is None:
                easing = QEasingCurve.Type.OutCubic
            self._answer_home_token = getattr(self, '_answer_home_token', 0) + 1
            token = self._answer_home_token
            anim = QPropertyAnimation(bar, b'value', self)
            anim.setDuration(480)
            anim.setStartValue(start)
            anim.setEndValue(end)
            anim.setEasingCurve(QEasingCurve(easing))
            anim.finished.connect(lambda token=token: self._finish_answer_home(token))
            self._answer_home_anim = anim
            self._answer_scroll_animating = True
            anim.start()

        def _finish_answer_home(self, token=None):
            if token is not None and token != getattr(self, '_answer_home_token', None):
                return
            if self._closing or not getattr(self, '_answer_pin_start', False):
                self._answer_scroll_animating = False
                return
            self._answer_scroll_animating = True
            try:
                self._move_answer_cursor_home()
                bar = self.answer.verticalScrollBar()
                if bar is not None:
                    bar.setValue(bar.minimum())
            finally:
                self._answer_scroll_animating = False
            self._answer_pin_start = False
            self._answer_home_from_tail = False

        def _pin_answer_start(self):
            self._schedule_answer_home()

        def _flush_stream_render(self):
            if self._closing:
                return
            self._render_answer(self._stream_text)

        def _on_chunk(self, token, text):
            if token != self._request_token or self._closing:
                return
            self._stop_loading()
            self._stream_text += text
            if not self._stream_timer.isActive():
                self._stream_timer.start(80)

        def _ask(self):
            selection = self._selection.strip()
            note = self.note_edit.toPlainText().strip()
            if not selection and not note:
                self._set_status(self.i18n.get(
                    'read_selection_empty', 'Select some text in the book first.',
                ))
                return
            try:
                from .config import get_prefs
                from .prompt_limits import validate_prompt_length
            except ImportError:
                from config import get_prefs
                from prompt_limits import validate_prompt_length
            prefs = get_prefs()
            try:
                chapter = self.chapters[self._index]
                before = ''
                after_text = ''
                if _reader_flag(prefs, 'reader_include_context'):
                    before, after_text = surrounding_context(
                        chapter_plain_text(chapter.abs_path),
                        selection,
                        reader_context_chars(prefs),
                    )
                prompt = build_reader_prompt(
                    self.book,
                    chapter.title,
                    selection,
                    note,
                    before,
                    after_text,
                    prefs=prefs,
                    i18n=self.i18n,
                    use_saved_enhancements=True,
                )
            except EpubError as exc:
                self._set_status(str(exc))
                return
            length_error = validate_prompt_length(prompt, False, prefs, self.i18n, 1)
            if length_error:
                self._set_status(length_error)
                return
            self._set_note_expanded(False)
            self.note_edit.clearFocus()
            self._pending_note = note
            self._asked_note = note
            self._asked_selection = selection
            self._history_uid = None
            self.note_edit.clear()
            self._request_token += 1
            token = self._request_token
            lang = 'en'
            try:
                lang = prefs.get('language', 'en') or 'en'
            except Exception:
                lang = 'en'
            self._stream_text = ''
            self._follow_tail = True
            self._set_busy(True)
            self._start_loading()
            worker = AskWorker(self.api, prompt, lang, self._model_id)
            worker.chunk.connect(lambda text, token=token: self._on_chunk(token, text))
            worker.succeeded.connect(lambda text, token=token: self._on_answer(token, text))
            worker.failed.connect(lambda message, token=token: self._on_fail(token, message))
            self._workers.append(worker)
            worker.finished.connect(lambda worker=worker: self._workers.remove(worker) if worker in self._workers else None)
            self._worker = worker
            worker.start()

        def _answer_line_height_type(self):
            from PyQt5.QtGui import QTextBlockFormat
            member = getattr(QTextBlockFormat, 'FixedHeight', None)
            group = getattr(QTextBlockFormat, 'LineHeightTypes', None)
            if member is None and group is not None:
                member = getattr(group, 'FixedHeight', None)
            if isinstance(member, int):
                return member
            value = getattr(member, 'value', None)
            if isinstance(value, int):
                return value
            return 2

        def _apply_answer_line_height(self):
            from PyQt5.QtGui import QTextCursor, QTextFormat
            ratio = 1.6
            try:
                ratio = float(self._line_height)
            except (TypeError, ValueError):
                ratio = 1.6
            try:
                size = int(self._font_size)
            except (TypeError, ValueError):
                size = 18
            size = max(1, size)
            fixed = self._answer_line_height_type()
            pixels = reader_answer_line_px(size, ratio)
            document = self.answer.document()
            keep = getattr(QTextCursor, 'KeepAnchor', None)
            if keep is None:
                keep = QTextCursor.MoveMode.KeepAnchor
            adjustment = getattr(QTextFormat, 'FontSizeAdjustment', None)
            pending = []
            block = document.begin()
            while block.isValid():
                fragment = block.begin()
                while not fragment.atEnd():
                    frag = fragment.fragment()
                    if frag.length() <= 0:
                        fragment += 1
                        continue
                    fmt = frag.charFormat()
                    font = fmt.font()
                    adjusted = False
                    if adjustment is not None and fmt.hasProperty(adjustment):
                        adjusted = fmt.intProperty(adjustment) != 0
                    if font.pixelSize() != size or adjusted:
                        pending.append((frag.position(), frag.length(), fmt))
                    fragment += 1
                block = block.next()
            for pos, length, fmt in pending:
                font = fmt.font()
                font.setPixelSize(size)
                fmt.setFont(font)
                if adjustment is not None:
                    fmt.setProperty(adjustment, 0)
                cursor = QTextCursor(document)
                cursor.setPosition(pos)
                cursor.setPosition(min(pos + length, document.characterCount()), keep)
                cursor.setCharFormat(fmt)
            block = document.begin()
            while block.isValid():
                fmt = block.blockFormat()
                if fmt.lineHeight() != pixels or fmt.lineHeightType() != fixed:
                    fmt.setLineHeight(pixels, fixed)
                    cursor = QTextCursor(block)
                    cursor.setBlockFormat(fmt)
                block = block.next()

        def _start_loading(self):
            self._loading = True
            self._loading_step = 0
            self._show_loading_frame()
            self._loading_timer.start(400)

        def _show_loading_frame(self):
            base = self.i18n.get('read_requesting', 'Requesting')
            dots = '.' * ((self._loading_step % 3) + 1)
            self.answer.setPlainText(base + dots)
            self._apply_answer_line_height()
            self._reserve_answer_scrollbar_lane()

        def _advance_loading(self):
            if self._closing or not self._loading or self._stream_text:
                self._loading_timer.stop()
                return
            self._loading_step += 1
            self._show_loading_frame()

        def _stop_loading(self):
            self._loading = False
            self._loading_timer.stop()

        def _restore_note(self):
            note = self._pending_note
            self._pending_note = ''
            if note:
                self.note_edit.setPlainText(note)

        def _stop(self):
            self._stream_timer.stop()
            self._request_token += 1
            had_answer = bool(self._stream_text.strip())
            self._stop_loading()
            if not had_answer:
                self.answer.clear()
            self._restore_note()
            self._set_note_expanded(False)
            self._set_busy(False)

        def _on_answer(self, token, text):
            if token != self._request_token or self._closing:
                return
            self._stream_timer.stop()
            self._stop_loading()
            self._pending_note = ''
            self._set_busy(False)
            if not (text or '').strip():
                if not self._stream_text.strip():
                    self.answer.setPlainText(self.i18n.get('empty_answer', 'Empty answer'))
                    self._apply_answer_line_height()
                    self._reserve_answer_scrollbar_lane()
                else:
                    self._render_answer(self._stream_text, scroll_to_start=True)
                return
            self._stream_text = text
            self._render_answer(text, scroll_to_start=True)
            self._save_reader_history(text)

        def _on_fail(self, token, message):
            if token != self._request_token or self._closing:
                return
            self._stream_timer.stop()
            had_answer = bool(self._stream_text.strip())
            self._stop_loading()
            if not had_answer:
                self.answer.clear()
            self._restore_note()
            self._set_busy(False)
            self._set_status(message)

        def _history_manager(self):
            try:
                from .history_manager import HistoryManager
            except ImportError:
                from history_manager import HistoryManager
            return HistoryManager()

        def _history_answer(self, history):
            return history_answer_text(history)

        def _reload_reader_history_menu(self):
            menu = self.history_menu
            menu.clear()
            if self._book_id is None:
                empty = menu.addAction(self.i18n.get('no_history', 'No history records'))
                empty.setEnabled(False)
                return
            try:
                histories = self._history_manager().get_related_histories([self._book_id])
            except Exception:
                logger.info('Reading history could not be loaded')
                histories = []
            if not histories:
                empty = menu.addAction(self.i18n.get('no_history', 'No history records'))
                empty.setEnabled(False)
                return
            group = QActionGroup(menu)
            group.setExclusive(True)
            self._history_action_group = group
            new_action = menu.addAction(self.i18n.get('new_conversation', 'New Conversation'))
            new_action.setCheckable(True)
            new_action.setChecked(not self._history_uid)
            new_action.triggered.connect(self._start_new_reader_question)
            group.addAction(new_action)
            menu.addSeparator()
            found = False
            for history in histories:
                question = as_unicode_text(history.get('question')).strip()
                if not question:
                    question = self.i18n.get('empty_question_placeholder', '(No question)')
                elif len(question) > 42:
                    question = question[:42].rstrip() + '...'
                label = '{0} - {1}'.format(question, history.get('timestamp') or '')
                action = menu.addAction(label)
                action.setCheckable(True)
                if history.get('uid') == self._history_uid:
                    action.setChecked(True)
                    found = True
                action.triggered.connect(
                    lambda checked=False, uid=history.get('uid'): self._show_reader_history(uid)
                )
                group.addAction(action)
            if not found:
                new_action.setChecked(True)
            menu.addSeparator()
            clear_action = menu.addAction(self.i18n.get(
                'clear_current_book_history', 'Clear Current Book History',
            ))
            clear_action.triggered.connect(self._clear_reader_history)

        def _start_new_reader_question(self):
            self._history_uid = None
            self._stream_text = ''
            self.answer.clear()
            self.note_edit.clear()
            self._set_note_expanded(False)

        def _show_reader_history(self, uid):
            try:
                history = self._history_manager().get_history_by_uid(uid)
            except Exception:
                logger.info('Reading history item could not be opened')
                return
            if not history:
                return
            self._history_uid = uid
            question = as_unicode_text(history.get('question'))
            answer = self._history_answer(history)
            self.note_edit.setPlainText(question)
            self._set_note_expanded(bool(question.strip()))
            self._stream_text = answer
            self._follow_tail = False
            if answer.strip():
                self._render_answer(answer, scroll_to_start=True)
            else:
                self.answer.clear()

        def _clear_reader_history(self):
            title = as_unicode_text(self.book.get('title')) or self.i18n.get('read_and_ask', 'Read and ask')
            confirm = self.i18n.get(
                'confirm_clear_book_history',
                'Are you sure you want to clear all history for:\n{book_titles}?',
            ).format(book_titles=title)
            yes = getattr(QMessageBox, 'Yes', None)
            no = getattr(QMessageBox, 'No', None)
            if yes is None:
                yes = QMessageBox.StandardButton.Yes
                no = QMessageBox.StandardButton.No
            reply = QMessageBox.question(
                self,
                self.i18n.get('confirm', 'Confirm'),
                confirm,
                yes | no,
                no,
            )
            if reply != yes:
                return
            try:
                manager = self._history_manager()
                histories = manager.get_related_histories([self._book_id])
                for history in histories:
                    manager.delete_history(history.get('uid'))
            except Exception:
                logger.info('Reading history could not be cleared')
                return
            self._start_new_reader_question()

        def _save_reader_history(self, answer):
            answer = as_unicode_text(answer).strip()
            if not answer or self._book_id is None:
                return
            question = reader_history_question(self._asked_selection, self._asked_note)
            if not question:
                question = self.i18n.get('reader_prompt_default_question', 'Explain this passage using the chapter context.')
            try:
                manager = self._history_manager()
                uid = manager.generate_uid([self._book_id])
                model_info = {
                    'provider_name': '',
                    'model': as_unicode_text(getattr(self.api, 'model', '') or self._model_id),
                    'api_base': as_unicode_text(getattr(self.api, 'api_base', '')),
                }
                manager.save_history(
                    uid,
                    'single',
                    reader_history_books(self._book_id, self.book),
                    question,
                    answer,
                    ai_id=self._model_id or None,
                    model_info=model_info,
                )
                self._history_uid = uid
            except Exception:
                logger.info('Reading question was not saved')
                return
            try:
                from .statistics_widget import increment_ai_reply_count
                from .config import get_prefs
                increment_ai_reply_count(get_prefs())
            except Exception:
                try:
                    from statistics_widget import increment_ai_reply_count
                    from config import get_prefs
                    increment_ai_reply_count(get_prefs())
                except Exception:
                    logger.info('Reply count was not updated')

        def _window_state_flag(self, name):
            flag = getattr(Qt, name, None)
            if flag is None:
                flag = getattr(Qt.WindowState, name)
            return flag

        def _window_states(self):
            states = self.windowState()
            handle = self.windowHandle() if hasattr(self, 'windowHandle') else None
            if handle is not None:
                try:
                    states = states | handle.windowState()
                except Exception:
                    pass
            return states

        def _is_fullscreen(self):
            try:
                return bool(self._window_states() & self._window_state_flag('WindowFullScreen'))
            except Exception:
                return False

        def _is_maximized(self):
            try:
                return bool(self._window_states() & self._window_state_flag('WindowMaximized'))
            except Exception:
                return False

        def _save_reader_window(self):
            try:
                try:
                    from .config import get_prefs
                except ImportError:
                    from config import get_prefs
                prefs = get_prefs()
            except Exception:
                logger.info('Reader window state was not saved')
                return
            prefs['reader_window_fullscreen'] = self._window_mode == 'fullscreen'
            prefs['reader_window_maximized'] = self._window_mode == 'maximized'
            prefs['reader_split_ratio'] = self._current_split_ratio()
            if self._window_ready and self._window_mode == 'normal' and not self._applying_window_layout:
                self._window_width, self._window_height = reader_window_size(
                    self.width(), self.height(),
                )
            prefs['reader_window_width'] = self._window_width
            prefs['reader_window_height'] = self._window_height
            try:
                prefs.commit()
            except Exception:
                logger.info('Reader window state was not saved')

        def resizeEvent(self, event):
            super(EpubAskDialog, self).resizeEvent(event)
            if self._applying_window_layout:
                return
            if self._split_restore_pending:
                self._apply_split_ratio()
            if not self._window_ready or self._is_fullscreen() or self._is_maximized():
                return
            self._leave_desktop_fill_if_moved()
            if self._window_mode == 'normal':
                self._window_save_timer.start(400)

        def moveEvent(self, event):
            super(EpubAskDialog, self).moveEvent(event)
            if self._applying_window_layout or not self._window_ready:
                return
            if self._is_fullscreen() or self._is_maximized():
                return
            if self._window_mode != 'fullscreen':
                return
            self._leave_desktop_fill_if_moved()
            if self._window_mode == 'normal':
                self._window_save_timer.start(400)

        def _current_split_ratio(self):
            splitter = getattr(self, 'splitter', None)
            if splitter is None:
                return self._split_ratio
            sizes = splitter.sizes()
            if len(sizes) < 2 or sum(sizes) <= 0:
                return self._split_ratio
            return reader_split_ratio(sizes[0], sizes[1], self._split_ratio)

        def _on_splitter_moved(self, *_args):
            self._split_ratio = self._current_split_ratio()
            self._split_restore_pending = False
            if self._window_ready:
                self._window_save_timer.start(400)

        def _apply_split_ratio(self):
            splitter = getattr(self, 'splitter', None)
            if splitter is None or not self._split_restore_pending:
                return
            if self._window_mode == 'fullscreen' and not self._geometry_fills_desktop():
                return
            if self._window_mode == 'maximized' and not self._is_maximized():
                return
            total = sum(splitter.sizes()) or splitter.width()
            if total <= 0:
                return
            splitter.blockSignals(True)
            splitter.setSizes(reader_split_sizes(total, self._split_ratio))
            splitter.blockSignals(False)
            self._split_restore_pending = False

        def apply_language(self, i18n):
            """Refresh reader chrome after the plugin language changes."""
            self.i18n = i18n or {}
            title = as_unicode_text(self.book.get('title')) or self.i18n.get('read_and_ask', 'Read and ask')
            self.setWindowTitle(self.i18n.get(
                'read_window_title', 'Read and ask — {title}',
            ).format(title=title))
            self.prev_btn.setText(self.i18n.get('read_prev_chapter', 'Previous'))
            self.next_btn.setText(self.i18n.get('read_next_chapter', 'Next'))
            self.font_size_label.setText(self.i18n.get('read_font_size', 'Font size'))
            self.line_height_label.setText(self.i18n.get('read_line_height', 'Line height'))
            self.theme_label.setText(self.i18n.get('read_theme', 'Style'))
            theme_labels = (
                ('default', 'read_theme_default', 'Default'),
                ('sepia', 'read_theme_sepia', 'Sepia'),
                ('night', 'read_theme_night', 'Night'),
            )
            self.theme_combo.blockSignals(True)
            for theme_id, label_key, fallback in theme_labels:
                index = self.theme_combo.findData(theme_id)
                if index >= 0:
                    self.theme_combo.setItemText(index, self.i18n.get(label_key, fallback))
            self.theme_combo.blockSignals(False)
            self.model_label.setText(self.i18n.get('read_model', 'Model'))
            self.history_button.setText(self.i18n.get('history', 'History'))
            self.answer.setPlaceholderText(self.i18n.get(
                'read_answer_placeholder',
                'Select text in the book, then ask. The reply shows here.',
            ))
            self.note_edit.setPlaceholderText(self.i18n.get(
                'read_note_placeholder',
                'Optional note. Enter sends it with the selected text.',
            ))
            self.send_btn.setText(self.i18n.get('read_send', 'Ask'))
            self.stop_btn.setText(self.i18n.get('read_stop', 'Stop'))
            self._sync_fullscreen_button()
            if self._selection and not self._busy and not self._stream_text:
                self._set_status(self.i18n.get(
                    'read_selection_count', '{n} characters selected',
                ).format(n=len(self._selection)))

        def _sync_fullscreen_button(self):
            button = getattr(self, 'fullscreen_btn', None)
            if button is None:
                return
            full = self._window_mode == 'fullscreen'
            button.blockSignals(True)
            button.setChecked(full)
            if full:
                button.setText(self.i18n.get('read_exit_fullscreen', 'Exit full screen'))
            else:
                button.setText(self.i18n.get('read_fullscreen', 'Full screen'))
            button.blockSignals(False)

        def _reader_screen(self):
            screen = None
            if hasattr(self, 'screen'):
                try:
                    screen = self.screen()
                except Exception:
                    screen = None
            if screen is None and hasattr(self, 'windowHandle'):
                handle = self.windowHandle()
                if handle is not None:
                    try:
                        screen = handle.screen()
                    except Exception:
                        screen = None
            if screen is None:
                app = QApplication.instance()
                if app is not None and hasattr(app, 'primaryScreen'):
                    try:
                        screen = app.primaryScreen()
                    except Exception:
                        screen = None
            return screen

        def _screen_available_geometry(self):
            screen = self._reader_screen()
            if screen is None:
                return None
            try:
                return screen.availableGeometry()
            except Exception:
                return None

        def _geometry_fills_desktop(self):
            avail = self._screen_available_geometry()
            if avail is None:
                return False
            frame = self.frameGeometry()
            return (
                abs(frame.x() - avail.x()) <= 16
                and abs(frame.y() - avail.y()) <= 16
                and abs(frame.width() - avail.width()) <= 24
                and abs(frame.height() - avail.height()) <= 24
            )

        def _place_frame(self, avail):
            frame = self.frameGeometry()
            inner = self.geometry()
            x, y, width, height = reader_client_geometry_for_frame(
                (avail.x(), avail.y(), avail.width(), avail.height()),
                (frame.x(), frame.y(), frame.width(), frame.height()),
                (inner.x(), inner.y(), inner.width(), inner.height()),
            )
            self.setGeometry(x, y, width, height)

        def _leave_desktop_fill_if_moved(self):
            if self._window_mode != 'fullscreen' or self._geometry_fills_desktop():
                return
            self._window_mode = 'normal'
            self._window_width, self._window_height = reader_window_size(
                self.width(), self.height(),
            )
            self._sync_fullscreen_button()

        def _fill_available_desktop(self):
            """Grow the window to the usable desktop. The menu bar and dock stay visible."""
            avail = self._screen_available_geometry()
            if avail is None:
                return
            self._applying_window_layout = True
            try:
                if self._is_fullscreen() or self._is_maximized():
                    self.showNormal()
                self._window_mode = 'fullscreen'
                self._observed_special = False
                self._place_frame(avail)
            finally:
                self._applying_window_layout = False
            self._apply_split_ratio()

        def _restore_windowed_size(self):
            self._applying_window_layout = True
            try:
                if self._is_fullscreen() or self._is_maximized():
                    self.showNormal()
                self._window_mode = 'normal'
                self._observed_special = False
                width, height = reader_window_size(self._window_width, self._window_height)
                avail = self._screen_available_geometry()
                if avail is None:
                    self.resize(width, height)
                    return
                width = min(width, max(1, avail.width()))
                height = min(height, max(1, avail.height()))
                x = avail.x() + max(0, (avail.width() - width) // 2)
                y = avail.y() + max(0, (avail.height() - height) // 2)
                self.setGeometry(int(x), int(y), int(width), int(height))
            finally:
                self._applying_window_layout = False

        def _toggle_fullscreen(self, checked):
            self._window_mode_timer.stop()
            self._pending_normal_from = None
            self._observed_special = False
            if checked:
                if self._window_mode != 'fullscreen':
                    self._window_width, self._window_height = reader_window_size(
                        self.width(), self.height(),
                    )
                self._fill_available_desktop()
            else:
                self._restore_windowed_size()
            self._sync_fullscreen_button()
            self._save_reader_window()

        def _current_window_mode(self):
            if self._is_fullscreen():
                return 'fullscreen'
            if self._is_maximized():
                return 'maximized'
            return 'normal'

        def _confirm_normal_window(self):
            """Ignore the brief un-fullscreen that happens while the window is closing."""
            if self._closing or not self.isVisible():
                return
            mode = self._current_window_mode()
            if mode == 'fullscreen':
                return
            if mode == 'maximized':
                self._window_mode = 'maximized'
                self._pending_normal_from = None
                self._sync_fullscreen_button()
                self._save_reader_window()
                return
            if self._window_mode == 'fullscreen' and not self._observed_special:
                return
            if self._window_mode == 'normal':
                return
            self._pending_normal_from = None
            self._window_mode = 'normal'
            self._sync_fullscreen_button()
            self._save_reader_window()

        def _capture_window_mode(self):
            if self._closing or not self._window_ready:
                return
            mode = self._current_window_mode()
            if mode in ('fullscreen', 'maximized'):
                self._window_mode_timer.stop()
                self._pending_normal_from = None
                self._observed_special = True
                if mode != self._window_mode:
                    self._window_mode = mode
                    self._sync_fullscreen_button()
                    self._save_reader_window()
                else:
                    self._sync_fullscreen_button()
                return
            if self._window_mode == 'fullscreen' and not self._observed_special:
                return
            if self._window_mode != 'normal':
                self._pending_normal_from = self._window_mode
                self._window_mode_timer.start(1200)

        def changeEvent(self, event):
            super(EpubAskDialog, self).changeEvent(event)
            if not self._window_ready or self._closing:
                return
            if event.type() != self._event_type('WindowStateChange'):
                return
            QTimer.singleShot(0, self._capture_window_mode)
            QTimer.singleShot(400, self._capture_window_mode)

        def showEvent(self, event):
            super(EpubAskDialog, self).showEvent(event)
            self._window_ready = True
            if self._window_restored:
                return
            self._window_restored = True
            if self._window_mode == 'fullscreen':
                QTimer.singleShot(0, self._fill_available_desktop)
            elif self._window_mode == 'maximized':
                QTimer.singleShot(0, self.showMaximized)
            self._sync_fullscreen_button()
            QTimer.singleShot(0, self._apply_split_ratio)

        def closeEvent(self, event):
            self._closing = True
            self._request_token += 1
            self._stop_loading()
            if getattr(self, '_progress_timer', None) is not None:
                self._progress_timer.stop()
            self._flush_reader_progress()
            if getattr(self, '_window_save_timer', None) is not None:
                self._window_save_timer.stop()
            if getattr(self, '_window_mode_timer', None) is not None:
                if self._window_mode_timer.isActive() and self._pending_normal_from:
                    self._window_mode = self._pending_normal_from
                self._window_mode_timer.stop()
            self._save_reader_window()
            app = QApplication.instance()
            if app is not None:
                app.removeEventFilter(self)
            for worker in list(self._workers):
                if worker.isRunning():
                    worker.wait(200)
            try:
                self.view.stop()
            except Exception:
                pass
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            super(EpubAskDialog, self).closeEvent(event)

    return EpubAskDialog()
