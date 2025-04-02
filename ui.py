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
from calibre_plugins.ask_gpt.i18n import get_translation, SUGGESTION_TEMPLATES
from calibre_plugins.ask_gpt.shortcuts_widget import ShortcutsWidget
from calibre.utils.resources import get_path as I
import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_suggestion_template(lang_code):
    """获取指定语言的建议提示词模板"""
    return SUGGESTION_TEMPLATES.get(lang_code, SUGGESTION_TEMPLATES['en'])

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
        # 根据操作系统设置快捷键
        if sys.platform == 'darwin':  # macOS
            self.config_action.setShortcut(QKeySequence("Command+Shift+L"))
        else:
            self.config_action.setShortcut(QKeySequence("Ctrl+Shift+L"))
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
        dlg.tab_widget.setCurrentIndex(2)  # 默认显示关于标签页
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
        self.i18n = get_translation(get_prefs()['language'])
        self.about_label.setText(f"""
        <div style='text-align: center'>
            <h1 style='margin-bottom: 10px'>{self.i18n['plugin_name']}</h1>
            <p style='font-weight: normal;'>{self.i18n['plugin_desc']}</p>
            <p style='color: #666; font-weight: normal; margin: 20px 0 10px 0;'>v1.0.0</p>
            <p style='color: #666; font-weight: normal; '>
                <a href='https://github.com/sheldonrrr/ask_gpt' 
                   style='color: #666; text-decoration: none;'>
                   💻 GitHub 💻
                </a>
            </p>
            <p style='color: #666; font-weight: normal; '>
                <a href='https://t.me/sheldonrrr' 
                   style='color: #666; text-decoration: none;'>
                   ✈️ Telegram with {self.i18n['author_name']} ✈️
                </a>
            </p>
        </div>
        """)

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
    
    def on_settings_saved(self):
        """当设置保存时的处理函数"""
        pass  # 不再需要在这里处理语言更新
    
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
        self.setMinimumHeight(500)  # 设置最小高度与配置对话框一致
        
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
        info_area.setFixedHeight(150)  # 设置固定高度
        
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
        self.input_area.setFixedHeight(80)  # 设置输入框高度
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
        
        # 创建操作区域
        action_layout = QHBoxLayout()
        
        # 创建建议按钮
        self.suggest_button = QPushButton(self.i18n['suggest_button'])
        self.suggest_button.clicked.connect(self.generate_suggestion)
        self.suggest_button.setFixedWidth(80)  # 设置固定宽度
        self.suggest_button.setFixedHeight(24)  # 设置固定高度
        
        # 创建建议动作和快捷键
        self.suggest_action = QAction(self.i18n['suggest_button'], self)
        self.suggest_action.setShortcut(QKeySequence("Ctrl+Shift+S" if not sys.platform == 'darwin' else "Cmd+Shift+S"))
        self.suggest_action.triggered.connect(self.generate_suggestion)
        self.addAction(self.suggest_action)
        
        # 设置按钮样式
        self.suggest_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                padding: 2px 8px;
            }
            QPushButton:hover:enabled {
                background-color: #f5f5f5;
            }
        """)
        action_layout.addWidget(self.suggest_button)
        
        # 添加弹性空间
        action_layout.addStretch()
        
        # 创建发送按钮
        self.send_button = QPushButton(self.i18n['send_button'])
        self.send_button.clicked.connect(self.send_question)
        self.send_button.setFixedWidth(80)  # 设置固定宽度
        self.send_button.setFixedHeight(24)  # 设置固定高度
        # 设置按钮样式
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                padding: 2px 8px;
            }
            QPushButton:hover:enabled {
                background-color: #f5f5f5;
            }
        """)
        action_layout.addWidget(self.send_button)
        
        layout.addLayout(action_layout)
        
        # 创建响应区域
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setMinimumHeight(280)  # 设置最小高度，允许用户拉伸
        self.response_area.setStyleSheet("""
            QTextEdit {
                border: 1px dashed #999;
                border-radius: 4px;
                padding: 5px;
                background-color: #fafafa;
            }
        """)
        self.response_area.setPlaceholderText(self.i18n['response_placeholder'])
        layout.addWidget(self.response_area)
    
    def generate_suggestion(self):
        """生成问题建议
        点击"建议？"按钮后，使用 AI 生成一个关于当前书籍的问题建议，
        并将这个建议直接填入输入框中，作为用户的问题。
        """
        if not self.api:
            return
            
        # 禁用建议按钮，显示加载状态
        self.suggest_button.setEnabled(False)
        original_text = self.suggest_button.text()
        self.suggest_button.setText(self.i18n['loading'])
        self.suggest_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                color: #666;
                padding: 2px 8px;
            }
        """)
        
        # 清空输入框，显示加载状态
        original_input = self.input_area.toPlainText()
        self.input_area.clear()
        self.input_area.setPlaceholderText(self.i18n['loading'])
        
        # 确保 UI 更新
        QApplication.processEvents()
        
        # 延迟执行 API 调用，确保 UI 状态已更新
        QTimer.singleShot(100, lambda: self._do_generate_suggestion(original_text, original_input))
        
    def _do_generate_suggestion(self, original_button_text, original_input):
        """实际执行生成建议的逻辑"""
        try:
            # 准备提示词
            template = get_suggestion_template(get_prefs()['language'])
            prompt = template.format(
                title=self.book_info.title,
                author=', '.join(self.book_info.authors) if self.book_info.authors else 'Unknown'
            )
            
            # 调用 API 获取建议
            suggestion = ""
            for chunk in self.api.ask_stream(prompt):
                suggestion += chunk
            
            # 将建议设置到输入框
            if suggestion:
                self.input_area.setText(suggestion)
            else:
                # 如果没有得到建议，恢复原来的输入
                self.input_area.setText(original_input)
            
        except Exception as e:
            logger.error(f"生成建议时出错：{str(e)}")
            # 发生错误时恢复原来的输入
            self.input_area.setText(original_input)
        
        finally:
            # 恢复输入框占位符
            self.input_area.setPlaceholderText(self.i18n['input_placeholder'])
            
            # 恢复按钮状态
            self.suggest_button.setText(original_button_text)
            self.suggest_button.setEnabled(True)
            self.suggest_button.setStyleSheet("""
                QPushButton {
                    font-size: 12px;
                    padding: 2px 8px;
                }
                QPushButton:hover:enabled {
                    background-color: #f5f5f5;
                }
            """)
    
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
