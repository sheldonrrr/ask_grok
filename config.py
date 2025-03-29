#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QTextEdit, QComboBox, QPushButton,
                           QDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
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
        self.lang_label = QLabel(self.i18n['language_label'])
        layout.addWidget(self.lang_label)
        
        self.lang_combo = QComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(prefs['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)
        
        # X.AI Authorization Token 配置
        self.key_label = QLabel(self.i18n['token_label'])
        self.key_help = QLabel(self.i18n['token_help'])
        self.key_help.setStyleSheet('color: gray; font-size: 11px;')
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_help)
        
        self.auth_token_edit = QLineEdit(self)
        self.auth_token_edit.setText(prefs['auth_token'])
        layout.addWidget(self.auth_token_edit)
        
        # API Base URL 配置
        self.base_url_label = QLabel(self.i18n['base_url_label'])
        layout.addWidget(self.base_url_label)
        
        self.base_url_edit = QLineEdit(self)
        self.base_url_edit.setText(prefs['api_base_url'])
        self.base_url_edit.setPlaceholderText(self.i18n['base_url_placeholder'])
        layout.addWidget(self.base_url_edit)
        
        # Model 配置
        self.model_label = QLabel(self.i18n['model_label'])
        layout.addWidget(self.model_label)
        
        self.model_edit = QLineEdit(self)
        self.model_edit.setText(prefs['model'])
        self.model_edit.setPlaceholderText(self.i18n['model_placeholder'])
        layout.addWidget(self.model_edit)
        
        # 提示词模板配置
        self.template_label = QLabel(self.i18n['template_label'])
        layout.addWidget(self.template_label)
        
        self.template_edit = QTextEdit(self)
        self.template_edit.setText(prefs['template'])
        self.template_edit.setPlaceholderText(self.i18n['template_placeholder'])
        self.template_edit.setFixedHeight(180)
        layout.addWidget(self.template_edit)
        
        # 添加一个弹性空间
        layout.addStretch()
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 创建保存成功提示标签
        self.save_success_label = QLabel('')
        self.save_success_label.setStyleSheet('color: #2ecc71; font-size: 12px;')  # 使用绿色
        self.save_success_label.hide()  # 初始时隐藏
        button_layout.addWidget(self.save_success_label)
        
        button_layout.addStretch()
        
        # 创建保存按钮
        self.save_button = QPushButton(self.i18n.get('save_button', 'Save'))
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setFixedWidth(80)  # 调整为标准按钮宽度
        self.save_button.setFixedHeight(24)  # 调整为标准按钮高度
        self.save_button.setEnabled(False)  # 初始状态设为不可点击
        
        # 设置按钮样式
        self.save_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
            }
            QPushButton:hover:enabled {
                background-color: #f5f5f5;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # 连接所有输入控件的信号
        self.lang_combo.currentIndexChanged.connect(self.on_config_changed)
        self.auth_token_edit.textChanged.connect(self.on_config_changed)
        self.base_url_edit.textChanged.connect(self.on_config_changed)
        self.model_edit.textChanged.connect(self.on_config_changed)
        self.template_edit.textChanged.connect(self.on_config_changed)
        
        # 保存初始配置值
        self.initial_values = {
            'language': self.lang_combo.currentData(),
            'auth_token': self.auth_token_edit.text(),
            'api_base_url': self.base_url_edit.text(),
            'model': self.model_edit.text(),
            'template': self.template_edit.toPlainText()
        }
    
    def on_config_changed(self):
        """当任何配置发生改变时检查是否需要启用保存按钮"""
        current_values = {
            'language': self.lang_combo.currentData(),
            'auth_token': self.auth_token_edit.text(),
            'api_base_url': self.base_url_edit.text(),
            'model': self.model_edit.text(),
            'template': self.template_edit.toPlainText()
        }
        
        # 比较当前值和初始值
        has_changes = any(
            current_values[key] != self.initial_values[key]
            for key in self.initial_values
        )
        
        # 根据是否有改变来设置保存按钮状态
        self.save_button.setEnabled(has_changes)
    
    def save_settings(self):
        """保存设置但不关闭窗口"""
        # 保存所有设置
        prefs['auth_token'] = self.auth_token_edit.text()
        prefs['api_base_url'] = self.base_url_edit.text()
        prefs['model'] = self.model_edit.text()
        prefs['template'] = self.template_edit.toPlainText()
        prefs['language'] = self.lang_combo.currentData()
        
        # 更新初始值为当前值
        self.initial_values = {
            'language': self.lang_combo.currentData(),
            'auth_token': self.auth_token_edit.text(),
            'api_base_url': self.base_url_edit.text(),
            'model': self.model_edit.text(),
            'template': self.template_edit.toPlainText()
        }
        
        # 禁用保存按钮
        self.save_button.setEnabled(False)
        
        # 显示保存成功提示
        self.save_success_label.setText(self.i18n.get('save_success', 'Settings saved'))
        self.save_success_label.show()
        
        # 2秒后隐藏提示
        QTimer.singleShot(2000, self.save_success_label.hide)
        
        # 发送 settings_saved 信号
        self.settings_saved.emit()
    
    def on_language_changed(self, index):
        """语言改变时更新模板和界面语言"""
        lang_code = self.lang_combo.currentData()
        
        # 更新界面语言
        self.i18n = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
        self.setWindowTitle(self.i18n['config_title'])
        
        # 更新所有标签文本
        self.lang_label.setText(self.i18n['language_label'])
        self.key_label.setText(self.i18n['token_label'])
        self.key_help.setText(self.i18n['token_help'])
        self.base_url_label.setText(self.i18n['base_url_label'])
        self.model_label.setText(self.i18n['model_label'])
        self.template_label.setText(self.i18n['template_label'])
        
        # 更新输入框占位符
        self.base_url_edit.setPlaceholderText(self.i18n['base_url_placeholder'])
        self.model_edit.setPlaceholderText(self.i18n['model_placeholder'])
        self.template_edit.setPlaceholderText(self.i18n['template_placeholder'])
        
        # 更新按钮文本
        self.save_button.setText(self.i18n.get('save_button', 'Save'))
        
        # 如果保存成功提示正在显示，也更新它的文本
        if not self.save_success_label.isHidden():
            self.save_success_label.setText(self.i18n.get('save_success', 'Settings saved'))
        
        # 更新模板内容
        self.template_edit.setText(get_default_template(lang_code))
    
    def accept(self):
        """保存配置并关闭对话框"""
        self.save_settings()
        super().accept()

    # 添加自定义信号
    settings_saved = pyqtSignal()
