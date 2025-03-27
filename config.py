#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QTextEdit, QComboBox)
import os
from calibre.utils.config import JSONConfig
from .i18n import get_translation

# 全局配置对象
prefs = JSONConfig('plugins/ask_gpt')

# 支持的语言选项
LANGUAGE_OPTIONS = [
    # 中文变体
    ('zh', '简体中文'),
    ('zht', '繁體中文'),
    ('yue', '粵語'),
    
    # 日语
    ('ja', '日本語'),
    
    # 欧洲语系
    ('fr', 'Français'),   # 法语
    ('de', 'Deutsch'),    # 德语
    ('es', 'Español'),    # 西班牙语
    ('ru', 'Русский'),    # 俄语
    ('pt', 'Português'),  # 葡萄牙语
    ('sv', 'Svenska'),    # 瑞典语
    ('da', 'Dansk'),      # 丹麦语
    ('nl', 'Nederlands'), # 荷兰语
    ('no', 'Norsk'),      # 挪威语
    ('fi', 'Suomi'),      # 芬兰语
    
    # 英语
    ('en', 'English'),    # 保留英语作为选项
]

# 默认配置
prefs.defaults['auth_token'] = os.environ.get('XAI_AUTH_TOKEN', '')
prefs.defaults['template'] = '关于《{title}》这本书的信息：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，语言：{language}，系列：{series}，我的问题是：{query}'
prefs.defaults['api_base_url'] = 'https://api.x.ai/v1'
prefs.defaults['model'] = 'grok-2-latest'
prefs.defaults['language'] = 'zh'  # 默认使用简体中文

def get_prefs():
    # 如果配置中没有 auth token，尝试从环境变量获取
    if not prefs['auth_token'] and os.environ.get('XAI_AUTH_TOKEN'):
        prefs['auth_token'] = os.environ.get('XAI_AUTH_TOKEN')
    return prefs

class ConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 获取当前语言的翻译
        self.i18n = get_translation(prefs['language'])
        
        # 语言选择
        lang_label = QLabel(self.i18n['language_label'])
        self.layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox(self)
        for code, name in LANGUAGE_OPTIONS:
            self.lang_combo.addItem(name, code)
        # 设置当前语言
        index = self.lang_combo.findData(prefs['language'])
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
        self.layout.addWidget(self.lang_combo)
        
        # X.AI Authorization Token 配置
        key_label = QLabel(self.i18n['token_label'])
        key_help = QLabel(self.i18n['token_help'])
        key_help.setStyleSheet('color: gray; font-size: 11px;')
        self.layout.addWidget(key_label)
        self.layout.addWidget(key_help)
        
        self.auth_token_edit = QLineEdit(self)
        self.auth_token_edit.setText(prefs['auth_token'])
        self.layout.addWidget(self.auth_token_edit)
        
        # API Base URL 配置
        base_url_label = QLabel(self.i18n['base_url_label'])
        self.layout.addWidget(base_url_label)
        
        self.base_url_edit = QLineEdit(self)
        self.base_url_edit.setText(prefs['api_base_url'])
        self.base_url_edit.setPlaceholderText(self.i18n['base_url_placeholder'])
        self.layout.addWidget(self.base_url_edit)
        
        # Model 配置
        model_label = QLabel(self.i18n['model_label'])
        self.layout.addWidget(model_label)
        
        self.model_edit = QLineEdit(self)
        self.model_edit.setText(prefs['model'])
        self.model_edit.setPlaceholderText(self.i18n['model_placeholder'])
        self.layout.addWidget(self.model_edit)
        
        # 提示词模板配置
        template_label = QLabel(self.i18n['template_label'])
        self.layout.addWidget(template_label)
        
        self.template_edit = QTextEdit(self)
        self.template_edit.setText(prefs['template'])
        self.template_edit.setPlaceholderText(self.i18n['template_placeholder'])
        self.template_edit.setFixedHeight(180)
        self.layout.addWidget(self.template_edit)
        
        self.layout.addStretch()
    
    def save_settings(self):
        """保存配置到 calibre 配置文件"""
        prefs['auth_token'] = self.auth_token_edit.text()
        prefs['api_base_url'] = self.base_url_edit.text()
        prefs['model'] = self.model_edit.text()
        prefs['template'] = self.template_edit.toPlainText()
        prefs['language'] = self.lang_combo.currentData()
