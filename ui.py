#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import auto
from PyQt5.Qt import (Qt, QMenu, QAction, QTextCursor, QApplication, 
                     QKeySequence, QMessageBox, QPixmap, QPainter, QSize, QTimer)
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QTextEdit, QPushButton, QTabWidget, QWidget, QDialogButtonBox,
                           QTextBrowser, QSizePolicy)   
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import info_dialog
from calibre_plugins.ask_grok.config import ConfigDialog, get_prefs
from calibre_plugins.ask_grok.api import APIClient
from calibre_plugins.ask_grok.i18n import get_translation, SUGGESTION_TEMPLATES
from calibre_plugins.ask_grok.shortcuts_widget import ShortcutsWidget
from calibre.utils.resources import get_path as I
import sys
import os

# 添加 lib 目录到 Python 路径
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import markdown2
import bleach

# 导入插件实例
import calibre_plugins.ask_grok.ui as ask_grok_plugin

# 存储插件实例的全局变量
plugin_instance = None

def get_suggestion_template(lang_code):
    """获取指定语言的随机问题提示词模板"""
    return SUGGESTION_TEMPLATES.get(lang_code, SUGGESTION_TEMPLATES['en'])

class AskGrokPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 根据操作系统设置不同的快捷键
    action_spec = ('Ask Grok', 'images/ask_grok.png', 'Ask Grok about this book', 
                  'Ctrl+L')
    action_type = 'global'
    
    def __init__(self, parent, site_customization):
        try:
            InterfaceAction.__init__(self, parent, site_customization)
        except Exception as e:
            pass
        self.api = None
        self.gui = parent
        # 初始化 i18n
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 保存插件实例到全局变量
        global plugin_instance
        plugin_instance = self
        
    def genesis(self):
        icon = get_icons('images/ask_grok.png')
        self.qaction.setIcon(icon)
        
        # 创建菜单
        self.menu = QMenu(self.gui)
        self.menu.setStyleSheet("""
            QMenu {
                min-width: 80px;
            }
        """)
        
        # 添加主要动作
        self.ask_action = QAction(self.i18n['menu_title'], self)
        
        # 根据操作系统设置快捷键
        if sys.platform == 'darwin':  # macOS
            self.ask_action.setShortcut(QKeySequence("Command+L"))  # macOS 使用 Command
            self.qaction.setShortcut(QKeySequence("Command+L"))  # 同时设置主动作的快捷键
        else:
            self.ask_action.setShortcut(QKeySequence("Ctrl+L"))  # 其他系统使用 Ctrl
            self.qaction.setShortcut(QKeySequence("Ctrl+L"))  # 同时设置主动作的快捷键
        self.ask_action.triggered.connect(self.show_dialog)
        self.menu.addAction(self.ask_action)
        
        # 添加分隔符
        self.menu.addSeparator()

        # 添加配置菜单项
        self.config_action = QAction(self.i18n['config_title'], self)

        # # 根据操作系统设置快捷键，暂时注销，之后找其他办法实现
        # if sys.platform == 'darwin':  # macOS
        #     shortcut = QKeySequence("Command+K")
        # else:
        #     shortcut = QKeySequence("Ctrl+K")
        # self.config_action.setShortcut(shortcut)
        # self.config_action.setShortcutContext(Qt.ApplicationShortcut) # 设置为应用程序级别的快捷键
        
        self.config_action.triggered.connect(self.show_configuration)
        self.menu.addAction(self.config_action)
        
        #添加分隔符
        self.menu.addSeparator()

        #添加快捷键菜单项
        self.shortcuts_action = QAction(self.i18n['shortcuts_title'], self)
        self.shortcuts_action.triggered.connect(self.show_shortcuts)
        self.menu.addAction(self.shortcuts_action)      

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
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        self.config_action.setText(self.i18n['config_title'])
        self.ask_action.setText(self.i18n['menu_title'])
        self.about_action.setText(self.i18n['about_title'])
        
    def initialize_api(self):
        if not self.api:
            # 获取配置
            prefs = get_prefs()
            language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
            i18n = get_translation(language)
            
            # 从配置获取 auth_token
            auth_token = prefs.get('auth_token', '')
            
            # 创建 APIClient 实例
            self.api = APIClient(auth_token=auth_token, i18n=i18n)
    
    def apply_settings(self):
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
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
        dlg.tab_widget.setCurrentIndex(2)  # 默认显示关于标签页
        dlg.exec_()
    
    def show_shortcuts(self):
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(1)  # 默认显示快捷键标签页
        dlg.exec_()

    def update_menu_texts(self):
        """更新菜单项的文本"""
        try:
            # 保存原始状态
            original_texts = {
                'ask': self.ask_action.text(),
                'config': self.config_action.text(),
                'shortcuts': self.shortcuts_action.text(),
                'about': self.about_action.text()
            }
            
            # 更新文本
            prefs = get_prefs()
            language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
            self.i18n = get_translation(language)
            self.ask_action.setText(self.i18n['menu_title'])
            self.config_action.setText(self.i18n['config_title'])
            self.shortcuts_action.setText(self.i18n['shortcuts_title'])
            self.about_action.setText(self.i18n['about_title'])
            
        except Exception as e:
            # 发生错误时恢复原始状态
            self.ask_action.setText(original_texts['ask'])
            self.config_action.setText(original_texts['config'])
            self.shortcuts_action.setText(original_texts['shortcuts'])
            self.about_action.setText(original_texts['about'])
            raise e

class AskGrokConfigWidget(QWidget):
    """配置页面组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = parent
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
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
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建关于标签
        self.about_label = QLabel()
        self.about_label.setTextFormat(Qt.RichText)
        self.about_label.setAlignment(Qt.AlignCenter)
        self.about_label.setOpenExternalLinks(True)
        layout.addWidget(self.about_label)
        
        # 初始化内容
        self.update_content()
        
    def update_content(self):
        """更新关于页面内容"""
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        self.about_label.setText(f"""
        <div style='text-align: center'>
            <h1 style='margin-bottom: 10px'>{self.i18n['plugin_name']}</h1>
            <p style='font-weight: normal;'>{self.i18n['plugin_desc']}</p>
            <p style='color: palette(text); font-weight: normal; margin: 20px 0 10px 0;'>v1.1.18</p>
            <p style='color: palette(text); font-weight: normal; '>
                <a href='https://github.com/sheldonrrr/ask_grok' 
                   style='color: palette(text); text-decoration: none;'>
                   GitHub: Release & Issues
                </a>
            </p>
            <p style='color: palette(text); font-weight: normal; '>
                <a href='https://www.mobileread.com/forums/showthread.php?p=4503254#post4503254' 
                   style='color: palette(text); text-decoration: none;'>
                   MobileRead: calibre's Forum
                </a>
            </p>
            <p style='color: palette(text); font-weight: normal; '>
                <a href='https://t.me/sheldonrrr' 
                   style='color: palette(text); text-decoration: none;'>
                   Telegram: @sheldonrrr
                </a>
            </p>
        </div>
        """)

class TabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = parent
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['config_title'])
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        # 创建标签页
        self.tab_widget = QTabWidget()

        # 创建配置页面
        self.config_widget = AskGrokConfigWidget(self.gui)
        self.tab_widget.addTab(self.config_widget, self.i18n['config_title'])

        # 创建快捷键页面
        self.shortcuts_widget = ShortcutsWidget(self)
        self.tab_widget.addTab(self.shortcuts_widget, self.i18n['shortcuts_tab'])

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
        
        # 连接语言切换信号
        self.config_widget.config_dialog.language_changed.connect(self.on_language_changed)
    
    def on_language_changed(self, new_language):
        """当语言改变时更新所有组件"""
        self.i18n = get_translation(new_language)
        
        # 更新窗口标题
        self.setWindowTitle(self.i18n['config_title'])
        
        # 更新标签页标题
        self.tab_widget.setTabText(0, self.i18n['config_title'])
        self.tab_widget.setTabText(1, self.i18n['shortcuts_tab'])
        self.tab_widget.setTabText(2, self.i18n['about_title'])
        
        # 更新快捷键页面
        self.shortcuts_widget.update_shortcuts()
        
        # 更新关于页面
        self.about_widget.update_content()
        
        # 通知主界面更新菜单
        ask_grok_plugin.plugin_instance.update_menu_texts()
        
        # 更新 response_handler 和 suggestion_handler 的 i18n 对象
        if (hasattr(ask_grok_plugin.plugin_instance, 'ask_dialog') and 
            ask_grok_plugin.plugin_instance.ask_dialog and
            hasattr(ask_grok_plugin.plugin_instance.ask_dialog, 'suggestion_handler')):
            ask_grok_plugin.plugin_instance.ask_dialog.response_handler.update_i18n(self.i18n)
            ask_grok_plugin.plugin_instance.ask_dialog.suggestion_handler.update_i18n(self.i18n)
    
    def on_settings_saved(self):
        """当设置保存时的处理函数"""
        # 获取最新的语言设置
        new_language = get_prefs().get('language', 'en')
        # 更新界面
        self.on_language_changed(new_language)
    
    def keyPressEvent(self, event):
        """处理按键事件"""
        if event.key() == Qt.Key_Escape:
            # 如果配置页面有未保存的更改，先重置字段
            if self.config_widget.config_dialog.save_button.isEnabled():
                self.config_widget.config_dialog.reset_to_initial_values()
            # 关闭窗口
            self.reject()
        else:
            super().keyPressEvent(event)
    
    def reject(self):
        """处理关闭按钮"""
        # 如果配置页面有未保存的更改，先重置字段
        if self.config_widget.config_dialog.save_button.isEnabled():
            self.config_widget.config_dialog.reset_to_initial_values()
        super().reject()

from calibre_plugins.ask_grok.response_handler import ResponseHandler
from calibre_plugins.ask_grok.random_question import SuggestionHandler

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
        super().__init__(gui)
        self.gui = gui
        self.book_info = book_info
        self.api = api
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 初始化处理器
        self.response_handler = ResponseHandler(self)
        # 确保 SuggestionHandler 正确初始化
        self.suggestion_handler = SuggestionHandler(parent=self)
        
        # 读取保存窗口的大小
        prefs = get_prefs()
        self.saved_width = prefs.get('ask_dialog_width', 800)  # 增加默认宽度
        self.saved_height = prefs.get('ask_dialog_height', 600)
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['menu_title'])
        self.setMinimumWidth(600)  # 增加最小宽度
        self.setMinimumHeight(600)
        
        # 创建 UI
        self.setup_ui()
        
        # 设置处理器
        self.response_handler.setup(self.response_area, self.send_button, self.i18n, self.api)
        self.suggestion_handler.setup(self.response_area, self.input_area, self.suggest_button, self.api, self.i18n)
        
        # 添加事件过滤器
        self.input_area.installEventFilter(self)
        
        # 设置窗口大小
        self.resize(self.saved_width, self.saved_height)
        
        # 连接窗口大小变化信号
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        """窗口大小变化时的处理函数"""
        prefs = get_prefs()
        prefs['ask_dialog_width'] = self.width()
        prefs['ask_dialog_height'] = self.height()
        super().resizeEvent(event)

    def get_language_name(self, lang_code):
        """将语言代码转换为易读的语言名称"""
        if not lang_code:
            return None
        lang_code = lang_code.lower().strip()
        return self.LANGUAGE_MAP.get(lang_code, lang_code)
    
    def setup_ui(self):
        self.setWindowTitle(f"{self.i18n['menu_title']} - {self.book_info.title}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)  # 设置最小高度与配置对话框一致
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建书籍信息显示区域 - 使用 QTextEdit 替代 QLabel 以支持滚动条
        info_area = QTextEdit()
        info_area.setReadOnly(True)  # 设置为只读
        info_area.setFrameShape(QTextEdit.NoFrame)  # 无边框
        info_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 需要时显示滚动条
        info_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        info_area.setStyleSheet("""
            QTextEdit {
                background-color: palette(base);
                color: palette(text);
                font-size: 13px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid palette(mid);
                line-height: 1.5;
            }
        """)
        # 设置高度和滚动条策略
        info_area.setMinimumHeight(20)
        info_area.setMaximumHeight(100)
        
        # 构建书籍信息
        metadata_info = []
        if self.book_info.title:
            metadata_info.append(f"{self.i18n['metadata_title']}-{self.book_info.title}")
        if self.book_info.authors:
            metadata_info.append(f"{self.i18n['metadata_authors']}-{', '.join(self.book_info.authors)}")
        if self.book_info.publisher:
            metadata_info.append(f"{self.i18n['metadata_publisher']}-{self.book_info.publisher}")
        if hasattr(self.book_info, 'pubdate') and self.book_info.pubdate:
            year = str(self.book_info.pubdate.year) if hasattr(self.book_info.pubdate, 'year') else str(self.book_info.pubdate)
            metadata_info.append(f"{self.i18n['metadata_pubyear']}-{year}")
        if self.book_info.language:
            metadata_info.append(f"{self.i18n['metadata_language']}-{self.get_language_name(self.book_info.language)}")
        if getattr(self.book_info, 'series', None):
            metadata_info.append(f"{self.i18n['metadata_series']}-{self.book_info.series}")
        
        if len(metadata_info) == 1:  # 只有 Metadata 提示，没有实际数据
            metadata_info.append(f"{self.i18n.get('no_metadata', 'No metadata available')}.")
        
        info_area.setHtml("<br>".join(metadata_info))
        layout.addWidget(info_area)
        
        # 创建输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText(self.i18n['input_placeholder'])
        self.input_area.setFixedHeight(80)  # 设置输入框高度
        self.input_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 1px solid palette(highlight);
                border-radius: 4px;
                padding: 5px;
                outline: none;
            }
        """)
        layout.addWidget(self.input_area)
        
        # 创建操作区域
        action_layout = QHBoxLayout()
        
        # 创建随机问题按钮
        self.suggest_button = QPushButton(self.i18n['suggest_button'])
        self.suggest_button.clicked.connect(self.generate_suggestion)
        self.suggest_button.setMinimumWidth(80)
        self.suggest_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # 创建随机问题动作和快捷键
        self.suggest_action = QAction(self.i18n['suggest_button'], self)
        self.suggest_action.setShortcut(QKeySequence("Ctrl+Shift+S" if not sys.platform == 'darwin' else "Cmd+Shift+S"))

        # 设置快捷键的范围为窗口级别的
        self.suggest_action.setShortcutContext(Qt.WindowShortcut)

        self.suggest_action.triggered.connect(self.generate_suggestion)
        self.addAction(self.suggest_action)
        
        # 设置按钮样式
        self.suggest_button.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
            }
            QPushButton:hover:enabled {
                background-color: palette(midlight);
            }
            QPushButton:pressed {
                background-color: palette(mid);
                color: white;
            }
        """)
        action_layout.addWidget(self.suggest_button)
        
        # 添加弹性空间
        action_layout.addStretch()
        
        # 创建发送按钮
        self.send_button = QPushButton(self.i18n['send_button'])
        self.send_button.clicked.connect(self.send_question)
        self.send_button.setMinimumWidth(80)
        self.send_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # 创建发送动作和快捷键
        self.send_action = QAction(self.i18n['send_button'], self)
        self.send_action.setShortcut(QKeySequence("Ctrl+Enter" if not sys.platform == 'darwin' else "Cmd+Enter"))

        # 设置快捷键的范围为窗口级别的
        self.send_action.setShortcutContext(Qt.WindowShortcut)
        self.send_action.triggered.connect(self.send_question)
        self.addAction(self.send_action)

        # 设置发送按钮样式
        self.send_button.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                min-width: 80px;
            }
            QPushButton:hover:enabled {
                background-color: palette(midlight);
            }
            QPushButton:pressed {
                background-color: palette(mid);
            }
        """)
        action_layout.addWidget(self.send_button)
        
        layout.addLayout(action_layout)
        
        # 创建响应区域
        self.response_area = QTextBrowser()
        self.response_area.setOpenExternalLinks(True)  # 允许打开外部链接
        self.response_area.setMinimumHeight(280)  # 设置最小高度，允许用户拉伸
        self.response_area.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction | 
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.response_area.setStyleSheet("""
            QTextBrowser {
                border: 1px dashed palette(mid);
                color: palette(text);
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.response_area.setPlaceholderText(self.i18n['response_placeholder'])
        
        # 设置 Markdown 支持
        self.response_area.document().setDefaultStyleSheet("""
            strong { font-weight: bold; }
            em { font-style: italic; }
            h1 { font-size: 1.2em; }
            h2 { font-size: 1.1em; }
            h3 { font-size: 1.1em; }
            code { 
                background-color: palette(midlight); 
                padding: 2px 4px; 
                border-radius: 3px; 
                font-family: -apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            }
            pre { 
                background-color: palette(midlight); 
                padding: 10px; 
                border-radius: 5px; 
                margin: 10px 0; 
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
                border: 1px solid palette(midlight);
            }
            th, td {
                border: 1px solid palette(midlight);
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: palette(light);
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: palette(light);
            }
            thead, tbody {
                display: table;
                width: 100%;
            }
            blockquote { 
                border-left: 4px solid palette(midlight); 
                margin: 10px 0; 
                padding: 0 10px; 
                color: #333; 
            }
            table { 
                border-collapse: collapse; 
                margin: 10px 0; 
            }
            th, td { 
                border: 1px solid palette(midlight); 
                padding: 5px; 
            }
            ul, ol { 
                margin: 10px 0; 
                padding-left: 20px; 
            }
            li { margin: 5px 0; }
        """)
        layout.addWidget(self.response_area)
    
    def generate_suggestion(self):
        """生成问题随机问题"""
        if not self.api:
            return
            
        self.suggestion_handler.generate(self.book_info)

    def _check_auth_token(self):
        """检查 auth token 是否已设置，如果未设置则显示配置对话框"""
        from calibre_plugins.ask_grok.config import get_prefs, ConfigDialog
        
        # 从配置中获取 token
        prefs = get_prefs()
        token = prefs.get('auth_token', '') if hasattr(prefs, 'get') and callable(prefs.get) else ''
        
        # 检查 token 是否为空
        if not token or not token.strip():
            # 显示提示信息
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                self.i18n.get('auth_token_required_title', 'Auth Token Required'),
                self.i18n.get('auth_token_required_message', 'Please set your Auth Token in the configuration dialog.')
            )
            
            # 创建并显示配置对话框
            config_dialog = ConfigDialog(self.gui)  # 使用 self.gui 而不是 self
            config_dialog.show()
            return False
        
        return True

    def send_question(self):
        """发送问题"""
        # 检查 token 是否有效
        if not self._check_auth_token():
            return
            
        try:
            # 获取输入的问题
            question = self.input_area.toPlainText()
            # 标准化换行符并确保使用 UTF-8 编码
            question = question.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8')
        
            # 准备模板变量

            # 安全地获取书籍的作者或作者列表
            try:
                authors = self.book_info.authors if hasattr(self.book_info, 'authors') else []
                author_str = ', '.join(authors) if authors else self.i18n.get('unknown', 'Unknown')
            except AttributeError:
                author_str = self.i18n.get('unknown', 'Unknown')
            
            # 安全地获取书籍的出版年份
            try:
                pubyear = ''
                if hasattr(self.book_info, 'pubdate') and self.book_info.pubdate:
                    if hasattr(self.book_info.pubdate, 'year'):
                        pubyear = str(self.book_info.pubdate.year)
                    else:
                        pubyear = str(self.book_info.pubdate)
                else:
                    pubyear = self.i18n.get('unknown', 'Unknown')
            except Exception as e:
                logger.error(f"获取出版年份时出错: {str(e)}")
                pubyear = self.i18n.get('unknown', 'Unknown')
            
            # 安全地获取书籍的语言类别
            try:
                language = self.book_info.language
                language_name = self.get_language_name(language) if language else self.i18n.get('unknown', 'Unknown')
            except (AttributeError, KeyError) as e:
                language_name = self.i18n.get('unknown', 'Unknown')
            
            # 安全地获取书籍的系列名
            try:
                series = self.book_info.series if hasattr(self.book_info, 'series') and self.book_info.series else self.i18n.get('unknown', 'Unknown')
            except AttributeError:
                series = self.i18n.get('unknown', 'Unknown')
            
            # 准备模板变量
            template_vars = {
                'query': question.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'title': getattr(self.book_info, 'title', self.i18n.get('unknown', 'Unknown')).replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'author': author_str.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'publisher': (getattr(self.book_info, 'publisher', '') or '').replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'pubyear': str(pubyear).replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if pubyear else '',
                'language': language_name.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if language_name else '',
                'series': series.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if series else ''
            }
        except Exception as e:
            self.response_handler.handle_error(f"{self.i18n.get('error_preparing_request', 'Error preparing request')}: {str(e)}")
            return
        
        # 获取配置的模板
        from calibre_plugins.ask_grok.config import get_prefs
        prefs = get_prefs()
        template = prefs.get('template', '')
        
        # 如果模板为空，使用默认模板
        if not template:
            template = "User query: {query}\nBook title: {title}\nAuthor: {author}\nPublisher: {publisher}\nPublication year: {pubyear}\nLanguage: {language}\nSeries: {series}"
        
        # 检查并替换模板中的变量名，确保用户输入能够正确插入
        if '{query}' not in template and '{question}' in template:
            template = template.replace('{question}', '{query}')
        
        # 格式化提示词
        try:
            prompt = template.format(**template_vars)
        except KeyError as e:
            self.response_handler.handle_error(self.i18n.get('template_error', 'Template error: {error}').format(error=str(e)))
            return
        
        # 如果提示词过长，可能会导致超时
        if len(prompt) > 2000:  # 设置一个合理的限制
            self.response_handler.handle_error(self.i18n.get('question_too_long', 'Question is too long, please simplify and try again'))
            return
        
        # 禁用发送按钮并显示加载状态
        self.send_button.setEnabled(False)
        self.send_button.setText(self.i18n.get('sending', 'Sending...'))
        
        # 开始异步请求
        self.response_handler.start_async_request(prompt)
    
    def eventFilter(self, obj, event):
        """事件过滤器，用于处理快捷键"""
        if event.type() == event.KeyPress:
            # 检查是否按下了 Ctrl+Enter 或 Cmd+Return
            if ((event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier) and 
                (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter)):
                self.send_question()
                return True
        return False

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        # 准备关闭，让线程自然结束
        self.response_handler.prepare_close()
        self.suggestion_handler.prepare_close()  # 改用 prepare_close
        event.accept()
