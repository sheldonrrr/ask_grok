#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ask 弹窗统一工具栏。"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QSizePolicy,
)
from PyQt5.QtCore import Qt

from calibre_plugins.ask_ai_plugin.ui_constants import (
    SPACING_SMALL, ASK_TOOLBAR_HEIGHT, ASK_TOOLBAR_INSET_V,
    ASK_TOOLBAR_BUTTON_MIN_WIDTH, style_ask_toolbar_widget,
)


class AskToolbar(QWidget):
    """一行工具栏：左侧 AI/历史，右侧随机/停止/发送。"""

    def __init__(self, i18n, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self._left_layout = QHBoxLayout()
        self._left_layout.setSpacing(SPACING_SMALL)
        self._left_layout.setContentsMargins(0, 0, 0, 0)
        self._left_layout.setAlignment(Qt.AlignVCenter)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, ASK_TOOLBAR_INSET_V, 0, ASK_TOOLBAR_INSET_V)
        root.setSpacing(SPACING_SMALL)
        root.setAlignment(Qt.AlignVCenter)
        root.addLayout(self._left_layout)
        root.addStretch()

        self.suggest_button = QPushButton(self.i18n.get('suggest_button', 'Random'))
        style_ask_toolbar_widget(self.suggest_button, min_width=ASK_TOOLBAR_BUTTON_MIN_WIDTH)
        self.suggest_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        root.addWidget(self.suggest_button, alignment=Qt.AlignVCenter)

        self.stop_button = QPushButton(self.i18n.get('stop_button', 'Stop'))
        style_ask_toolbar_widget(self.stop_button, min_width=ASK_TOOLBAR_BUTTON_MIN_WIDTH)
        self.stop_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stop_button.setVisible(False)
        root.addWidget(self.stop_button, alignment=Qt.AlignVCenter)

        self.send_button = QPushButton(self.i18n.get('send_button', 'Send'))
        style_ask_toolbar_widget(self.send_button, min_width=ASK_TOOLBAR_BUTTON_MIN_WIDTH)
        self.send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        root.addWidget(self.send_button, alignment=Qt.AlignVCenter)

        self.setFixedHeight(ASK_TOOLBAR_HEIGHT)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def add_left_widget(self, widget):
        if widget is None:
            return
        style_ask_toolbar_widget(widget)
        self._left_layout.addWidget(widget, alignment=Qt.AlignVCenter)

    def set_ai_search_mode(self, is_ai_search):
        """AI Search 模式隐藏随机问题按钮。"""
        self.suggest_button.setVisible(not is_ai_search)
