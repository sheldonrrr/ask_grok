#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, 
                           QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from calibre.utils.config import JSONConfig

from calibre_plugins.ask_grok.i18n import get_default_template, get_translation

# 创建配置对象
prefs = JSONConfig('plugins/ask_grok')

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
prefs.defaults['auth_token'] = ''
prefs.defaults['template'] = get_default_template('en')
prefs.defaults['api_base_url'] = 'https://api.x.ai/v1'
prefs.defaults['model'] = 'grok-3-latest'
prefs.defaults['language'] = 'en'
prefs.defaults['ask_dialog_width'] = 600
prefs.defaults['ask_dialog_height'] = 400


def get_prefs():
    """获取配置"""
    # 确保模板不为空，如果为空则使用当前语言的默认模板
    if not prefs['template']:
        prefs['template'] = get_default_template(prefs.get('language', 'en'))
    
    # 确保语言键存在，如果不存在则使用默认值 'en'
    if 'language' not in prefs:
        prefs['language'] = 'en'
    
    return prefs

class ConfigDialog(QWidget):
    # 添加信号
    settings_saved = pyqtSignal()  # 设置保存信号
    language_changed = pyqtSignal(str)  # 语言改变信号
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        # 获取当前语言的翻译
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 保存初始值
        self.initial_values = {}
        self.setup_ui()
        self.load_initial_values()
        
    def get_auth_token_without_bearer(self, token):
        """从 token 中移除 'Bearer ' 前缀"""
        if not token:
            return ''
        if token.startswith('Bearer '):
            return token[7:].strip()
        return token.strip()
        
    def get_auth_token_with_bearer(self, token):
        """确保 token 有 'Bearer ' 前缀"""
        if not token:
            return ''
        token = token.strip()
        if not token.startswith('Bearer '):
            return f'Bearer {token}'
        return token
        
    def setup_ui(self):
        # 设置窗口属性
        self.setMinimumWidth(400)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 语言选择
        self.lang_label = QLabel(self.i18n.get('language_label', 'Language'))
        layout.addWidget(self.lang_label)
        
        self.lang_combo = QComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(get_prefs()['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)
        
        # X.AI Authorization Token 配置
        self.key_label = QLabel(self.i18n['token_label'])
        self.key_help = QLabel()
        self.key_help.setWordWrap(True)
        self.key_help.setOpenExternalLinks(True)  # 允许打开外部链接
        self.key_help.setTextFormat(Qt.TextFormat.RichText)  # 支持 HTML 富文本
        self.key_help.setStyleSheet('color: gray; font-size: 11px;')
        self.key_help.setText(self.i18n['token_help'])
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_help)
        
        # 使用 QTextEdit 替代 QLineEdit 以支持多行显示
        self.auth_token_edit = QTextEdit(self)
        # 设置样式表，使用调色板颜色以支持主题切换
        self.auth_token_edit.setStyleSheet('''
            QTextEdit {
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: palette(base);
                color: palette(text);
                selection-background-color: palette(highlight);
                selection-color: palette(highlighted-text);
            }
            QTextEdit:focus {
                border: 1px solid palette(highlight);
            }
            QScrollBar:vertical {
                border: none;
                background: palette(window);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: palette(mid);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: palette(dark);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        ''')
        
        # 显示时移除 Bearer 前缀
        auth_token = get_prefs()['auth_token']
        if auth_token.startswith('Bearer '):
            auth_token = auth_token[7:].strip()
        self.auth_token_edit.setText(auth_token)
        
        # 设置多行显示属性
        try:
            # 尝试使用 PyQt5 的枚举方式设置换行模式
            self.auth_token_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        except AttributeError:
            # 如果枚举方式不可用，回退到整数值
            self.auth_token_edit.setLineWrapMode(1)  # 1 对应 WidgetWidth
            
        self.auth_token_edit.setAcceptRichText(False)  # 不接受富文本
        self.auth_token_edit.setTabChangesFocus(True)  # 按Tab键切换焦点
        self.auth_token_edit.setMaximumHeight(62)  # 设置最大高度，大约3行文字的高度
        self.auth_token_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 需要时显示垂直滚动条
        self.auth_token_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 不显示水平滚动条
        
        layout.addWidget(self.auth_token_edit)
        
        # API Base URL 配置
        self.base_url_label = QLabel(self.i18n['base_url_label'])
        layout.addWidget(self.base_url_label)
        
        self.base_url_edit = QLineEdit(self)
        self.base_url_edit.setText(get_prefs()['api_base_url'])
        self.base_url_edit.setPlaceholderText(self.i18n['base_url_placeholder'])
        layout.addWidget(self.base_url_edit)
        
        # Model 配置
        self.model_label = QLabel(self.i18n['model_label'])
        layout.addWidget(self.model_label)
        
        self.model_edit = QLineEdit(self)
        self.model_edit.setText(get_prefs()['model'])
        self.model_edit.setPlaceholderText(self.i18n['model_placeholder'])
        layout.addWidget(self.model_edit)
        
        # 提示词模板配置
        self.template_label = QLabel(self.i18n['template_label'])
        layout.addWidget(self.template_label)
        
        # 使用 QPlainTextEdit 替代 QTextEdit，因为它的布局计算更稳定
        self.template_edit = QPlainTextEdit(self)
        self.template_edit.setPlainText(get_prefs()['template'])
        self.template_edit.setPlaceholderText(self.i18n['template_placeholder'])
        self.template_edit.setFixedHeight(180)
        
        # 支持自动换行
        try:
            self.template_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        except AttributeError:
            self.template_edit.setLineWrapMode(1)  # 回退到整数值
        
        # 设置边距和滚动条策略
        self.template_edit.setViewportMargins(0, 0, 0, 0)
        self.template_edit.document().setDocumentMargin(6)  # 设置一个小的文档边距
        
        # 设置样式表
        self.template_edit.setStyleSheet('''
            QPlainTextEdit {
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: palette(base);
                color: palette(text);
            }
            QPlainTextEdit:focus {
                border: 1px solid palette(highlight);
            }
            QPlainTextEdit QScrollBar:vertical {
                width: 8px;
            }
            QPlainTextEdit QScrollBar::handle:vertical {
                background: palette(mid);
                min-height: 20px;
                border-radius: 4px;
            }
        ''')
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
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                min-width: 80px;
            }
            QPushButton:hover:enabled {
                background-color: #f5f5f5;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # 连接所有输入控件的信号
        self.auth_token_edit.textChanged.connect(self.on_config_changed)
        self.base_url_edit.textChanged.connect(self.on_config_changed)
        self.model_edit.textChanged.connect(self.on_config_changed)
        self.template_edit.textChanged.connect(self.on_config_changed)
        
    def load_initial_values(self):
        """加载初始值"""
        prefs = get_prefs()
        self.initial_values = {
            'auth_token': prefs['auth_token'],
            'api_base_url': prefs['api_base_url'],
            'model': prefs['model'],
            'template': prefs['template'],
            'language': prefs.get('language', 'en')
        }
        # 设置初始令牌值
        auth_token = prefs['auth_token']
        if auth_token.startswith('Bearer '):
            auth_token = auth_token[7:].strip()
        self.auth_token_edit.setPlainText(auth_token)
    
    def on_language_changed(self, index):
        """语言改变时的处理函数"""
        lang_code = self.lang_combo.currentData()
        
        # 自动保存语言设置
        prefs['language'] = lang_code
        
        # 更新界面语言
        self.i18n = get_translation(lang_code)
        
        # 更新界面文字
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
        
        # 更新成功提示文字
        if not self.save_success_label.isHidden():
            self.save_success_label.setText(self.i18n['save_success'])
        
        # 更新模板内容
        self.template_edit.setText(get_default_template(lang_code))
        
        # 发出语言改变信号
        self.language_changed.emit(lang_code)
        
    def save_settings(self):
        """保存设置"""
        # 获取并清理 token
        token = self.auth_token_edit.toPlainText().strip()
        
        # 检查 token 是否为空
        if not token:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                self.i18n.get('auth_token_required_title', 'Auth Token Required'),
                self.i18n.get('auth_token_none_message', 'No auth token, Ask Grok can not work.')
            )
            # 不返回，继续保存空token
        else:
            # 只有 token 不为空时才进行格式和长度检查
            # 检查 token 格式是否正确（以 xai- 或 Bearer xai- 开头）
            normalized_token = token.lower()
            if not (normalized_token.startswith('xai-') or 
                   normalized_token.startswith('bearer xai-')):
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    self.i18n.get('invalid_token_title', 'Invalid Token Format'),
                    self.i18n.get('invalid_token_message', 'The token format is invalid. It should start with "xai-" or "Bearer xai-".')
                )
                return
            
            # 检查 token 长度是否足够（xai- 前缀 + 至少 60 个字符）
            min_token_length = 64  # xai- 前缀 + 60 个字符
            if len(token) < min_token_length:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    self.i18n.get('invalid_token_title', 'Invalid Token Format'),
                    self.i18n.get('token_too_short_message', 'The token is too short. Please check and enter the complete token.')
                )
                return
        
        # 保存 API Token，不添加 Bearer 前缀
        prefs['auth_token'] = token
            
        # 保存其他设置
        prefs['model'] = self.model_edit.text().strip()
        prefs['api_base_url'] = self.base_url_edit.text().strip()
        prefs['template'] = self.template_edit.toPlainText().strip()
        
        # 更新按钮状态
        self.save_button.setEnabled(False)
        
        # 显示保存成功提示
        self.save_success_label.setText(self.i18n['save_success'])
        self.save_success_label.show()
        QTimer.singleShot(2000, self.save_success_label.hide)
        
        # 发出保存成功信号
        self.settings_saved.emit()
        
        # 更新初始值
        self.load_initial_values()
    
    def on_config_changed(self):
        """当任何配置发生改变时检查是否需要启用保存按钮"""
        current_values = {
            'language': self.lang_combo.currentData(),
            'auth_token': self.auth_token_edit.toPlainText(),
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
    def reset_to_initial_values(self):
        """重置到初始值"""
        self.lang_combo.setCurrentIndex(self.lang_combo.findData(self.initial_values['language']))
        # 处理令牌输入框的特殊情况
        auth_token = self.initial_values['auth_token']
        if auth_token.startswith('Bearer '):
            auth_token = auth_token[7:].strip()
        self.auth_token_edit.setPlainText(auth_token)
        self.base_url_edit.setText(self.initial_values['api_base_url'])
        self.model_edit.setText(self.initial_values['model'])
        self.template_edit.setPlainText(self.initial_values['template'])
        self.save_button.setEnabled(False)
        self.save_success_label.setText('')
        self.save_success_label.hide()
