#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QTextEdit, QComboBox, QPushButton,
                           QDialog, QDialogButtonBox, QHBoxLayout)
from PyQt5.QtCore import Qt
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

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 获取当前语言的翻译
        self.i18n = TRANSLATIONS.get(prefs['language'], TRANSLATIONS['en'])
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['config_title'])
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 语言选择
        lang_label = QLabel(self.i18n['language_label'])
        layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(prefs['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)
        
        # X.AI Authorization Token 配置
        key_label = QLabel(self.i18n['token_label'])
        key_help = QLabel(self.i18n['token_help'])
        key_help.setStyleSheet('color: gray; font-size: 11px;')
        layout.addWidget(key_label)
        layout.addWidget(key_help)
        
        self.auth_token_edit = QLineEdit(self)
        self.auth_token_edit.setText(prefs['auth_token'])
        layout.addWidget(self.auth_token_edit)
        
        # API Base URL 配置
        base_url_label = QLabel(self.i18n['base_url_label'])
        layout.addWidget(base_url_label)
        
        self.base_url_edit = QLineEdit(self)
        self.base_url_edit.setText(prefs['api_base_url'])
        self.base_url_edit.setPlaceholderText(self.i18n['base_url_placeholder'])
        layout.addWidget(self.base_url_edit)
        
        # Model 配置
        model_label = QLabel(self.i18n['model_label'])
        layout.addWidget(model_label)
        
        self.model_edit = QLineEdit(self)
        self.model_edit.setText(prefs['model'])
        self.model_edit.setPlaceholderText(self.i18n['model_placeholder'])
        layout.addWidget(self.model_edit)
        
        # 提示词模板配置
        template_label = QLabel(self.i18n['template_label'])
        layout.addWidget(template_label)
        
        self.template_edit = QTextEdit(self)
        self.template_edit.setText(prefs['template'])
        self.template_edit.setPlaceholderText(self.i18n['template_placeholder'])
        self.template_edit.setFixedHeight(180)
        layout.addWidget(self.template_edit)
        
        # 添加一个弹性空间
        layout.addStretch()
        
        # 按钮布局
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # 自定义按钮样式
        for button in button_box.buttons():
            if button.text() == 'OK':
                button.setText(self.i18n.get('ok_button', 'OK'))
            elif button.text() == 'Cancel':
                button.setText(self.i18n.get('cancel_button', 'Cancel'))
            button.setFixedWidth(100)
            button.setFixedHeight(32)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button_box)
        layout.addLayout(button_layout)
    
    def on_language_changed(self, index):
        """语言改变时更新模板和界面语言"""
        lang_code = self.lang_combo.currentData()
        self.template_edit.setText(get_default_template(lang_code))
        
        # 更新界面语言
        self.i18n = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
        self.setWindowTitle(self.i18n['config_title'])
        
        # 更新所有标签文本
        for widget in self.findChildren(QLabel):
            if widget.text() == self.i18n['language_label']:
                widget.setText(self.i18n['language_label'])
            elif widget.text() == self.i18n['token_label']:
                widget.setText(self.i18n['token_label'])
            elif widget.text() == self.i18n['token_help']:
                widget.setText(self.i18n['token_help'])
            elif widget.text() == self.i18n['base_url_label']:
                widget.setText(self.i18n['base_url_label'])
            elif widget.text() == self.i18n['model_label']:
                widget.setText(self.i18n['model_label'])
            elif widget.text() == self.i18n['template_label']:
                widget.setText(self.i18n['template_label'])
        
        # 更新按钮文本
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            for button in button_box.buttons():
                if button.text() == 'OK':
                    button.setText(self.i18n.get('ok_button', 'OK'))
                elif button.text() == 'Cancel':
                    button.setText(self.i18n.get('cancel_button', 'Cancel'))
    
    def accept(self):
        """保存配置并关闭对话框"""
        self.save_settings()
        super().accept()
    
    def save_settings(self):
        """保存配置到 calibre 配置文件"""
        prefs['auth_token'] = self.auth_token_edit.text()
        prefs['api_base_url'] = self.base_url_edit.text()
        prefs['model'] = self.model_edit.text()
        prefs['template'] = self.template_edit.toPlainText()
        prefs['language'] = self.lang_combo.currentData()
