#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QTextEdit, QComboBox, QPushButton)
from calibre.utils.config import JSONConfig

from .i18n import TRANSLATIONS, get_default_template, get_translation

# 创建配置对象
prefs = JSONConfig('plugins/ask_gpt')

# 支持的语言列表
SUPPORTED_LANGUAGES = [
    # 英语（默认语言）
    ('en', 'English (default)'),
    
    # 丹麦语
    ('da', 'Dansk'),
    
    # 德语
    ('de', 'Deutsch'),
    
    # 西班牙语
    ('es', 'Español'),
    
    # 芬兰语
    ('fi', 'Suomi'),
    
    # 法语
    ('fr', 'Français'),
    
    # 日语
    ('ja', '日本語'),
    
    # 荷兰语
    ('nl', 'Nederlands'),
    
    # 挪威语
    ('no', 'Norsk'),
    
    # 葡萄牙语
    ('pt', 'Português'),
    
    # 俄语
    ('ru', 'Русский'),
    
    # 瑞典语
    ('sv', 'Svenska'),
    
    # 简体中文
    ('zh', '简体中文'),
    
    # 繁体中文
    ('zht', '繁體中文'),
    
    # 粤语
    ('yue', '粵語'),
]

# 默认配置
prefs.defaults['auth_token'] = os.environ.get('XAI_AUTH_TOKEN', '')
prefs.defaults['template'] = get_default_template('zh')  # 使用中文模板作为默认值
prefs.defaults['api_base_url'] = 'https://api.x.ai/v1'
prefs.defaults['model'] = 'grok-2-latest'
prefs.defaults['language'] = 'zh'  # 默认使用简体中文

def get_prefs():
    """获取配置"""
    # 如果配置中没有 auth token，尝试从环境变量获取
    if not prefs['auth_token'] and os.environ.get('XAI_AUTH_TOKEN'):
        prefs['auth_token'] = os.environ.get('XAI_AUTH_TOKEN')
    
    # 确保模板不为空，如果为空则使用当前语言的默认模板
    if not prefs['template']:
        prefs['template'] = get_default_template(prefs['language'])
    
    return prefs

class ConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 获取当前语言的翻译
        self.i18n = TRANSLATIONS.get(prefs['language'], TRANSLATIONS['en'])
        
        # 语言选择
        lang_label = QLabel(self.i18n['language_label'])
        self.layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(prefs['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
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
    
    def on_language_changed(self, index):
        """语言改变时更新模板"""
        lang_code = self.lang_combo.currentData()
        self.template_edit.setText(get_default_template(lang_code))

    def save_settings(self):
        """保存配置到 calibre 配置文件"""
        prefs['auth_token'] = self.auth_token_edit.text()
        prefs['api_base_url'] = self.base_url_edit.text()
        prefs['model'] = self.model_edit.text()
        prefs['template'] = self.template_edit.toPlainText()
        prefs['language'] = self.lang_combo.currentData()
