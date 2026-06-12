#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ask 弹窗可折叠元数据栏。"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QSizePolicy,
)
from PyQt5.QtCore import Qt

from calibre_plugins.ask_ai_plugin.ui_constants import (
    SPACING_TINY,
    get_ask_metadata_collapsed_style,
    get_ask_metadata_toggle_style,
)


class AskMetadataBar(QWidget):
    """默认折叠为一行摘要，点击展开详情。"""

    def __init__(self, i18n, language_name_fn=None, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self._language_name_fn = language_name_fn or (lambda x: x)
        self._expanded = False
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACING_TINY)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(SPACING_TINY)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(get_ask_metadata_collapsed_style())
        self.summary_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        header_row.addWidget(self.summary_label, stretch=1)

        self.toggle_btn = QPushButton('▸')
        self.toggle_btn.setFixedSize(24, 24)
        self.toggle_btn.setStyleSheet(get_ask_metadata_toggle_style())
        self.toggle_btn.clicked.connect(self._toggle_expanded)
        header_row.addWidget(self.toggle_btn)

        root.addLayout(header_row)

        self.detail_list = QListWidget()
        self.detail_list.setFrameShape(QListWidget.NoFrame)
        self.detail_list.setVisible(False)
        self.detail_list.setMaximumHeight(120)
        root.addWidget(self.detail_list)

    def _toggle_expanded(self):
        if self.detail_list.count() == 0:
            return
        self._expanded = not self._expanded
        self.detail_list.setVisible(self._expanded)
        self.toggle_btn.setText('▾' if self._expanded else '▸')

    def _single_book_summary(self, meta):
        """单书折叠摘要：书名优先，无书名时再显示作者、出版社等。"""
        parts = []
        title = (meta.get('title') or '').strip()
        if title:
            parts.append(title)
        authors = meta.get('authors') or []
        author_str = ', '.join(a for a in authors if a).strip()
        if author_str:
            parts.append(author_str)
        publisher = (meta.get('publisher') or '').strip()
        if publisher:
            parts.append(publisher)
        if parts:
            return ' · '.join(parts)
        # 无书名/作者/出版社时，回退到其他元数据
        if meta.get('series'):
            parts.append(str(meta['series']).strip())
        if meta.get('pubdate'):
            parts.append(str(meta['pubdate']).strip())
        if meta.get('languages'):
            langs = [self._language_name_fn(code) for code in meta['languages']]
            lang_str = ', '.join(l for l in langs if l).strip()
            if lang_str:
                parts.append(lang_str)
        return ' · '.join(parts)

    def _ai_search_summary(self):
        try:
            from calibre_plugins.ask_ai_plugin.config import get_prefs
            import json
            prefs = get_prefs()
            library_metadata = prefs.get('library_cached_metadata', '')
            if not library_metadata:
                return self.i18n.get('ai_search_mode_info', 'Searching across your entire library')
            books = json.loads(library_metadata)
            count = len(books)
            return self.i18n.get(
                'ai_search_books_info', '{count} books indexed'
            ).format(count=count)
        except Exception:
            return self.i18n.get('ai_search_mode_info', 'Searching across your entire library')

    def refresh(self, books_metadata=None, is_multi_book=False, is_ai_search=False):
        """根据当前书籍元数据刷新显示。"""
        books_metadata = books_metadata or []
        self.detail_list.clear()
        self._expanded = False
        self.detail_list.setVisible(False)
        self.toggle_btn.setText('▸')

        if is_ai_search:
            summary = self._ai_search_summary()
            self.summary_label.setText(summary)
            self.toggle_btn.setVisible(False)
            return

        if not books_metadata:
            self.summary_label.setText('')
            self.toggle_btn.setVisible(False)
            self.setVisible(False)
            return

        self.setVisible(True)
        self.toggle_btn.setVisible(True)

        if is_multi_book:
            count = len(books_metadata)
            unit = self.i18n.get('books_unit', 'books')
            self.summary_label.setText(f"{count} {unit}")
            for idx, meta in enumerate(books_metadata, 1):
                title = meta.get('title', '')
                authors = ', '.join(meta.get('authors', []) or [])
                line = f"{idx}. {title}"
                if authors:
                    line += f" — {authors}"
                self.detail_list.addItem(QListWidgetItem(line))
        else:
            meta = books_metadata[0]
            self.summary_label.setText(self._single_book_summary(meta))

            detail_lines = []
            if meta.get('title'):
                detail_lines.append(
                    f"{self.i18n.get('metadata_title', 'Title')}: {meta['title']}"
                )
            if meta.get('authors'):
                detail_lines.append(
                    f"{self.i18n.get('metadata_authors', 'Authors')}: {', '.join(meta['authors'])}"
                )
            if meta.get('publisher'):
                detail_lines.append(
                    f"{self.i18n.get('metadata_publisher', 'Publisher')}: {meta['publisher']}"
                )
            if meta.get('pubdate'):
                detail_lines.append(
                    f"{self.i18n.get('metadata_pubyear', 'Publication Date')}: {meta['pubdate']}"
                )
            if meta.get('languages'):
                langs = [
                    self._language_name_fn(code) for code in meta['languages']
                ]
                detail_lines.append(
                    f"{self.i18n.get('metadata_language', 'Languages')}: {', '.join(langs)}"
                )
            if meta.get('series'):
                detail_lines.append(
                    f"{self.i18n.get('metadata_series', 'Series')}: {meta['series']}"
                )
            for line in detail_lines:
                self.detail_list.addItem(QListWidgetItem(line))

        if self.detail_list.count() == 0:
            self.toggle_btn.setVisible(False)
