#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import (Qt, QMenu, QAction, QTextCursor, QApplication, 
                     QKeySequence, QMessageBox, QPixmap, QPainter, QSize)
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QTextEdit, QPushButton)
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import info_dialog
from calibre_plugins.ask_gpt.config import ConfigWidget, get_prefs
from calibre_plugins.ask_gpt.api import APIClient
from calibre_plugins.ask_gpt.i18n import get_translation
from calibre.utils.resources import get_path as I
import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AskGPTPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 根据操作系统设置不同的快捷键
    action_spec = ('Ask Grok', 'images/ask_gpt.png', 'Ask Grok about this book', 
                  'Ctrl+L')
    action_type = 'global'
    
    def __init__(self, parent, site_customization):
        try:
            InterfaceAction.__init__(self, parent, site_customization)
        except Exception as e:
            logger.debug(f"初始化插件时出现非致命错误（可以忽略）：{str(e)}")
        self.api = None
        self.gui = parent
        self.i18n = get_translation(get_prefs()['language'])
        logger.info("AskGPTPluginUI initialized")
        
    def genesis(self):
        icon = get_icons('images/ask_gpt.png')
        self.qaction.setIcon(icon)
        
        # 创建菜单
        self.menu = QMenu(self.gui)
        
        # 添加主要动作
        self.ask_action = QAction(self.i18n['menu_title'], self)
        self.ask_action.triggered.connect(self.show_dialog)
        self.menu.addAction(self.ask_action)
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加配置菜单项
        self.config_action = QAction(self.i18n['config_title'], self)
        self.config_action.triggered.connect(self.show_configuration)
        self.menu.addAction(self.config_action)
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加关于菜单项
        self.about_action = QAction(self.i18n['about_title'], self)
        self.about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.about_action)
        
        # 设置菜单更新事件
        self.menu.aboutToShow.connect(self.about_to_show_menu)
        
        # 设置主图标点击和菜单
        self.qaction.triggered.connect(self.show_dialog)
        self.qaction.setMenu(self.menu)
        
    def about_to_show_menu(self):
        # 更新菜单项的文本
        self.i18n = get_translation(get_prefs()['language'])
        self.config_action.setText(self.i18n['config_title'])
        self.ask_action.setText(self.i18n['menu_title'])
        self.about_action.setText(self.i18n['about_title'])
        
    def initialize_api(self):
        if not self.api:
            prefs = get_prefs()
            self.api = APIClient(
                auth_token=prefs['auth_token'],
                api_base=prefs['api_base_url'],
                model=prefs['model']
            )
    
    def apply_settings(self):
        prefs = get_prefs()
        self.i18n = get_translation(prefs['language'])
        self.initialize_api()

    def show_configuration(self):
        self.interface_action_base_plugin.do_user_config(self.gui)

    def show_dialog(self):
        self.initialize_api()
        
        # 获取选中的书籍
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return
        
        # 获取书籍信息
        db = self.gui.current_db
        book_id = self.gui.library_view.model().id(rows[0])
        mi = db.get_metadata(book_id, index_is_id=True)
        
        # 显示对话框
        d = AskDialog(self.gui, mi, self.api)
        d.exec_()
    
    def show_about(self):
        """显示关于对话框"""
        msg = QMessageBox(self.gui)
        msg.setWindowTitle(self.i18n['about_title'])
        
        # 加载图标
        icon_path = I('images/ask_gpt.png')
        
        # 设置文本内容，将图标嵌入到HTML中
        msg.setText(f"""
        <div style='text-align: center'>
            <img src='{icon_path}' height='128' style='margin-bottom: 20px'>
            <h1 style='margin-bottom: 10px'>{self.i18n['plugin_name']}</h1>
            <p style='font-weight: normal;'>{self.i18n['plugin_desc']}</p>
            <p style='color: #666; font-weight: normal; margin: 20px 0 10px 0;'>v1.0.0</p>
            <p style='color: #666; font-weight: normal; '>
                <a href='https://github.com/sheldonrrr/ask_gpt' 
                   style='color: #666; text-decoration: none;'>
                   GitHub
                </a>
            </p>
        </div>
        """)
        msg.setTextFormat(Qt.RichText)
        
        # 设置消息框样式
        msg.setStyleSheet("""
            QMessageBox {
                text-align: center;
                padding: 20px;
            }
        """)
        
        msg.exec_()
        
class AskDialog(QDialog):
    LANGUAGE_MAP = {
        # 英语（默认语言）
        'en': 'English (default)',
        'eng': 'English (default)',
        
        # 丹麦语
        'da': 'Dansk',
        'dan': 'Dansk',
        
        # 德语
        'de': 'Deutsch',
        'deu': 'Deutsch',
        
        # 西班牙语
        'es': 'Español',
        'spa': 'Español',
        
        # 芬兰语
        'fi': 'Suomi',
        'fin': 'Suomi',
        
        # 法语
        'fr': 'Français',
        'fra': 'Français',
        
        # 日语
        'ja': '日本語',
        'jpn': '日本語',
        
        # 荷兰语
        'nl': 'Nederlands',
        'nld': 'Nederlands',
        
        # 挪威语
        'no': 'Norsk',
        'nor': 'Norsk',
        
        # 葡萄牙语
        'pt': 'Português',
        'por': 'Português',
        
        # 俄语
        'ru': 'Русский',
        'rus': 'Русский',
        
        # 瑞典语
        'sv': 'Svenska',
        'swe': 'Svenska',
        
        # 简体中文
        'zh': '简体中文',
        'zho': '简体中文',
        
        # 繁体中文
        'zh-hk': '繁體中文',
        'zh-tw': '繁體中文',
        'zht': '繁體中文',
        
        # 粤语
        'yue': '粵語',
        'zh-yue': '粵語',
    }
    
    def __init__(self, gui, book_info, api):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.book_info = book_info
        self.api = api
        self.i18n = get_translation(get_prefs()['language'])
        self.setup_ui()
    
    def get_language_name(self, lang_code):
        """将语言代码转换为易读的语言名称"""
        if not lang_code:
            return None
        lang_code = lang_code.lower().strip()
        return self.LANGUAGE_MAP.get(lang_code, lang_code)
    
    def setup_ui(self):
        self.setWindowTitle(f"{self.i18n['menu_title']} - {self.book_info.title}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建书籍信息显示区域
        info_area = QLabel()
        info_area.setWordWrap(True)
        info_area.setTextFormat(Qt.RichText)
        info_area.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 5px;
                line-height: 150%;
            }
        """)
        
        # 构建书籍信息HTML
        metadata_info = []
        if self.book_info.title:
            metadata_info.append(f"<p><b>{self.i18n['metadata_title']}：</b>{self.book_info.title}</p>")
        if self.book_info.authors:
            metadata_info.append(f"<p><b>{self.i18n['metadata_authors']}：</b>{', '.join(self.book_info.authors)}</p>")
        if self.book_info.publisher:
            metadata_info.append(f"<p><b>{self.i18n['metadata_publisher']}：</b>{self.book_info.publisher}</p>")
        if self.book_info.pubdate:
            metadata_info.append(f"<p><b>{self.i18n['metadata_pubdate']}：</b>{self.book_info.pubdate.year}</p>")
        if self.book_info.language:
            metadata_info.append(f"<p><b>{self.i18n['metadata_language']}：</b>{self.get_language_name(self.book_info.language)}</p>")
        if getattr(self.book_info, 'series', None):
            metadata_info.append(f"<p><b>{self.i18n['metadata_series']}：</b>{self.book_info.series}</p>")
        
        info_area.setText("".join(metadata_info))
        layout.addWidget(info_area)
        
        # 创建输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText(self.i18n['input_placeholder'])
        self.input_area.setMinimumHeight(100)
        layout.addWidget(self.input_area)
        
        # 创建响应区域
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setMinimumHeight(150)
        layout.addWidget(self.response_area)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        # 创建发送按钮和快捷键提示的容器
        send_container = QVBoxLayout()
        
        self.send_button = QPushButton(self.i18n['send_button'])
        self.send_button.clicked.connect(self.send_question)
        
        # 设置按钮样式
        self.send_button.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                border: 1px solid #4CAF50;
                border-radius: 4px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
                border-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #cccccc;
                color: #666666;
            }
        """)
        send_container.addWidget(self.send_button)
        
        # 添加快捷键提示标签
        if hasattr(Qt, 'ControlModifier'):
            shortcut_text = self.i18n['shortcut_enter']
        else:
            shortcut_text = self.i18n['shortcut_return']
        shortcut_label = QLabel(shortcut_text)
        shortcut_label.setStyleSheet("color: gray; font-size: 11px;")
        shortcut_label.setAlignment(Qt.AlignCenter)
        send_container.addWidget(shortcut_label)
        
        # 将发送按钮容器添加到按钮布局
        button_layout.addStretch()
        button_layout.addLayout(send_container)
        
        layout.addLayout(button_layout)
        
        # 设置快捷键
        QApplication.instance().installEventFilter(self)
        
        # 设置初始焦点
        self.input_area.setFocus()
    
    def send_question(self):
        self.send_button.setEnabled(False)
        question = self.input_area.toPlainText()
        
        # 获取配置的模板
        from calibre_plugins.ask_gpt.config import get_prefs
        prefs = get_prefs()
        template = prefs['template']
        
        # 准备模板变量
        template_vars = {
            'title': self.book_info.title,
            'author': ', '.join(self.book_info.authors),
            'publisher': self.book_info.publisher or '',
            'pubdate': self.book_info.pubdate.year if self.book_info.pubdate else '',
            'language': self.get_language_name(self.book_info.language) if self.book_info.language else '',
            'series': getattr(self.book_info, 'series', ''),
            'query': question
        }
        
        # 使用模板格式化提示词
        prompt = template.format(**template_vars)
        
        # 清空响应区域
        self.response_area.clear()
        
        try:
            # 使用流式输出
            for chunk in self.api.ask_stream(prompt):
                cursor = self.response_area.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.insertText(chunk)
                self.response_area.setTextCursor(cursor)
                self.response_area.ensureCursorVisible()
                QApplication.processEvents()
        except Exception as e:
            self.response_area.setText(f"{self.i18n['error_prefix']}{str(e)}")
        finally:
            # 重新启用发送按钮
            self.send_button.setEnabled(True)
    
    def eventFilter(self, obj, event):
        """事件过滤器，用于处理快捷键"""
        if event.type() == event.KeyPress:
            # 检查是否按下了 Ctrl+Enter 或 Cmd+Return
            if ((event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier) and 
                (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter)):
                self.send_question()
                return True
        return False
