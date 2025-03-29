#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import (Qt, QMenu, QAction, QTextCursor, QApplication, 
                     QKeySequence, QMessageBox, QPixmap, QPainter, QSize, QTimer)
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QTextEdit, QPushButton, QTabWidget, QWidget, QDialogButtonBox)
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import info_dialog
from calibre_plugins.ask_gpt.config import ConfigDialog, get_prefs
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
        """显示配置对话框"""
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(0)  # 默认显示配置标签页
        dlg.exec_()
    
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
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(1)  # 默认显示关于标签页
        dlg.exec_()

class AskGPTConfigWidget(QWidget):
    """配置页面组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = parent
        self.i18n = get_translation(get_prefs()['language'])
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 复用现有的 ConfigDialog
        self.config_dialog = ConfigDialog(self.gui)
        layout.addWidget(self.config_dialog)

class AboutWidget(QWidget):
    """关于页面组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = get_translation(get_prefs()['language'])
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 加载图标
        icon_path = I('images/ask_gpt.png')
        
        # 创建关于内容
        about_label = QLabel()
        about_label.setText(f"""
        <div style='text-align: center'>
            <img src='{icon_path}' height='128' style='margin-bottom: 20px'>
            <h1 style='margin-bottom: 10px'>{self.i18n['plugin_name']}</h1>
            <p style='font-weight: normal;'>{self.i18n['plugin_desc']}</p>
            <p style='color: #666; font-weight: normal; margin: 20px 0 10px 0;'>v1.0.0</p>
            <p style='color: #666; font-weight: normal; '>
                <a href='https://github.com/sheldonrrr/ask_gpt' 
                   style='color: #666;'>
                   GitHub
                </a>
            </p>
        </div>
        """)
        about_label.setTextFormat(Qt.RichText)
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setOpenExternalLinks(True)
        layout.addWidget(about_label)

class TabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = parent
        self.i18n = get_translation(get_prefs()['language'])
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['config_title'])
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 创建配置页面
        self.config_widget = AskGPTConfigWidget(self.gui)
        self.tab_widget.addTab(self.config_widget, self.i18n['config_title'])
        
        # 创建关于页面
        self.about_widget = AboutWidget()
        self.tab_widget.addTab(self.about_widget, self.i18n['about_title'])
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        
        # 创建按钮布局
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # 连接配置对话框的信号
        self.config_widget.config_dialog.settings_saved.connect(self.on_settings_saved)
    
    def on_settings_saved(self):
        """当设置保存时的处理函数"""
        # 这里可以添加任何需要在设置保存后执行的操作
        pass

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
        self.input_area.setFixedHeight(72)  # 设置为三行文字的高度
        self.input_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 1px solid #4a90e2;
                outline: none;
            }
        """)
        layout.addWidget(self.input_area)
        
        # 创建响应区域
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setMinimumHeight(150)
        self.response_area.setStyleSheet("""
            QTextEdit {
                border: 1px dashed #999;
                border-radius: 4px;
                padding: 5px;
                background-color: #fafafa;
            }
        """)
        # 设置占位符文字，使用当前语言
        self.response_area.setPlaceholderText(self.i18n['response_placeholder'])
        layout.addWidget(self.response_area)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        # 创建发送按钮和快捷键提示的容器
        send_container = QVBoxLayout()
        
        self.send_button = QPushButton(self.i18n['send_button'])
        self.send_button.clicked.connect(self.send_question)
        self.send_button.setFixedWidth(80)  # 设置固定宽度
        self.send_button.setFixedHeight(24)  # 设置固定高度
        
        # 设置按钮样式
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
            }
            QPushButton:hover:enabled {
                background-color: #f5f5f5;
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
        
        # 设置加载动画
        loading_text = self.i18n['loading_text'] if 'loading_text' in self.i18n else 'Loading'
        dots = ['', '.', '..', '...']
        current_dot = 0
        self._response_text = ''  # 初始化响应文本
        
        def update_loading():
            nonlocal current_dot
            if not self._response_text:  # 只有在没有响应时才显示加载动画
                self.response_area.setText(f"{loading_text}{dots[current_dot]}")
                current_dot = (current_dot + 1) % len(dots)
            else:  # 如果有响应，显示响应内容
                timer.stop()
                self.response_area.setText(self._response_text)
        
        # 创建定时器
        timer = QTimer()
        timer.timeout.connect(update_loading)
        timer.start(250)  # 每250毫秒更新一次，这样1秒会循环一遍
        
        # 1秒后停止加载动画
        QTimer.singleShot(1000, timer.stop)
        
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
        
        # 格式化提示词
        try:
            prompt = template.format(**template_vars)
        except KeyError as e:
            self.response_area.setText(f"{self.i18n['error_prefix']}Template error: {str(e)}")
            self.send_button.setEnabled(True)
            return
        
        # 发送请求并处理流式响应
        try:
            for chunk in self.api.ask_stream(prompt):
                self._response_text += chunk  # 累积响应文本
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
