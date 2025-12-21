#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from enum import auto
from .utils import mask_api_key, mask_api_key_in_text, safe_log_config
from PyQt5.Qt import (Qt, QMenu, QAction, QTextCursor, QApplication, 
                     QKeySequence, QMessageBox, QPixmap, QPainter, QSize, QTimer)
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextEdit, QPushButton, 
                            QHBoxLayout, QLabel, QComboBox, QApplication, 
                            QMessageBox, QScrollArea, QWidget, QSizePolicy, 
                            QFrame, QSplitter, QStatusBar, QTextBrowser, QTabWidget, QDialogButtonBox, QToolButton, QMenu, QAction, QToolTip, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal, QPoint, QRect, QEvent, QObject, QUrl
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import info_dialog
from calibre.gui2.keyboard import NameConflict
from calibre_plugins.ask_ai_plugin.config import ConfigDialog, get_prefs
from calibre_plugins.ask_ai_plugin.api import APIClient
from .i18n import get_translation, get_suggestion_template
from calibre_plugins.ask_ai_plugin.shortcuts_widget import ShortcutsWidget
from calibre_plugins.ask_ai_plugin.version import VERSION_DISPLAY
from calibre_plugins.ask_ai_plugin.widgets import apply_button_style
from calibre_plugins.ask_ai_plugin.ui_constants import (
    SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
    MARGIN_MEDIUM, PADDING_MEDIUM,
    FONT_SIZE_LARGE
)
from calibre.utils.resources import get_path as I
import sys
import os
import time

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import markdown2
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import bleach

# 存储插件实例的全局变量
# 注意：不要在这里导入自己，会导致循环导入
plugin_instance = None

def get_suggestion_template_from_ui(lang_code):
    """获取指定语言的随机问题提示词模板"""
    from .i18n import get_suggestion_template
    return get_suggestion_template(lang_code)

class AskAIPluginUI(InterfaceAction):
    name = 'Ask AI Plugin'
    # 所有平台统一使用F3，避免Qt键盘映射冲突
    action_spec = ('Ask AI Plugin', 'images/ask_ai_plugin.png', 'Ask AI about this book', 'F3')
    action_shortcut_name = 'Ask AI: Ask'
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
        
        # 保存对话框实例的引用
        self.ask_dialog = None
        
        # 保存插件实例到全局变量
        global plugin_instance
        plugin_instance = self
        
    def genesis(self):
        icon = get_icons('images/ask_ai_plugin.png')
        self.qaction.setIcon(icon)
        
        # 创建菜单
        self.menu = QMenu(self.gui)
        self.menu.setStyleSheet("""
            QMenu {
                min-width: 80px;
            }
        """)
        
        # 添加主要动作（在菜单中显示当前生效的快捷键提示）
        self.ask_action = QAction(self.i18n['menu_title'], self)
        self.ask_action.triggered.connect(self.show_dialog)
        try:
            # 复用 calibre 管理的主快捷键（实际注册在 menuless_qaction 上）
            self.ask_action.setShortcuts(self.menuless_qaction.shortcuts())
        except Exception:
            pass
        self.menu.addAction(self.ask_action)
        
        # 添加分隔符
        self.menu.addSeparator()

        # 添加配置菜单项（通过 calibre 快捷键系统注册，允许用户在 Preferences -> Shortcuts 中自定义）
        self.config_action = self.create_menu_action(
            self.menu,
            unique_name='open_configuration',
            text=self.i18n['config_title'],
            shortcut='F2',
            description=None,
            triggered=self.show_configuration,
            shortcut_name='Ask AI: Open Configuration',
            persist_shortcut=True,
        )

        # 注册对话框内快捷键（始终出现在 Preferences -> Shortcuts 中）
        # 注意：实际 QAction 会在 AskDialog 创建时通过 replace_action 绑定到对话框 action 上
        try:
            self.gui.keyboard.register_shortcut(
                self.unique_name + ' - ask_dialog_send',
                'Ask AI: Send (in dialog)',
                default_keys=('Ctrl+Enter',),
                action=None,
                description=None,
                group=self.action_spec[0],
                persist_shortcut=True,
            )
        except NameConflict:
            pass
        except Exception:
            pass

        try:
            self.gui.keyboard.register_shortcut(
                self.unique_name + ' - ask_dialog_random_question',
                'Ask AI: Random Question (in dialog)',
                default_keys=('Ctrl+R',),
                action=None,
                description=None,
                group=self.action_spec[0],
                persist_shortcut=True,
            )
        except NameConflict:
            pass
        except Exception:
            pass

        # 如果快捷键被标记为 Custom 但 keys 为空（通常来自冲突或旧版本遗留），
        # 则清理该空映射，让 calibre 回退使用 default_keys。
        try:
            send_un = self.unique_name + ' - ask_dialog_send'
            rand_un = self.unique_name + ' - ask_dialog_random_question'
            m = self.gui.keyboard.config.get('map', {}) or {}
            if m.get(send_un) in ((), [], None):
                with self.gui.keyboard.config:
                    m2 = self.gui.keyboard.config.get('map', {}) or {}
                    if m2.get(send_un) in ((), [], None):
                        m2.pop(send_un, None)
                        self.gui.keyboard.config['map'] = m2
            if m.get(rand_un) in ((), [], None):
                with self.gui.keyboard.config:
                    m2 = self.gui.keyboard.config.get('map', {}) or {}
                    if m2.get(rand_un) in ((), [], None):
                        m2.pop(rand_un, None)
                        self.gui.keyboard.config['map'] = m2
        except Exception:
            pass

        try:
            self.gui.keyboard.finalize()
        except Exception:
            pass
        
        #添加分隔符
        self.menu.addSeparator()

        #添加快捷键菜单项
        self.shortcuts_action = QAction(self.i18n['shortcuts'], self)
        self.shortcuts_action.triggered.connect(self.show_shortcuts)
        self.menu.addAction(self.shortcuts_action)      

        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加教程菜单项
        self.tutorial_action = QAction(self.i18n.get('tutorial', 'Tutorial'), self)
        self.tutorial_action.triggered.connect(self.show_tutorial)
        self.menu.addAction(self.tutorial_action)
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加关于菜单项
        self.about_action = QAction(self.i18n['about'], self)
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
        self.about_action.setText(self.i18n['about'])

        # 同步 Ask 菜单项显示的快捷键（跟随用户在 Preferences->Shortcuts 的自定义）
        try:
            self.ask_action.setShortcuts(self.menuless_qaction.shortcuts())
        except Exception:
            pass
        
    def initialize_api(self):
        try:
            # 初始化 API 客户端
            prefs = get_prefs()
            language = prefs.get('language', 'en')
            self.i18n = get_translation(language)
            
            # 创建新的 API 客户端，不再需要传递 api_base、model 和 auth_token 参数
            # 因为这些参数现在由 AIModelFactory 根据配置动态创建
            self.api = APIClient(i18n=self.i18n)
            
            # 记录当前使用的模型
            model_name = self.api.model_name
            model_display_name = self.api.model_display_name
            logger.info(f"API 客户端初始化成功，使用模型: {model_display_name} ({model_name})")
        except Exception as e:
            logger.error(f"初始化 API 客户端时出错: {str(e)}")
    
    def apply_settings(self):
        # 应用新的设置
        prefs = get_prefs()
        language = prefs.get('language', 'en')
        self.i18n = get_translation(language)
        
        # 重新加载 API 模型
        if self.api:
            self.api.reload_model()
            model_name = self.api.model_name
            model_display_name = self.api.model_display_name
            logger.info(f"设置已应用，当前使用模型: {model_display_name} ({model_name})")
    
    def show_configuration(self):
        """显示配置对话框"""
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(0)  # 默认显示配置标签页
        dlg.exec_()
    
    def show_dialog(self):
        logger.info("=" * 50)
        logger.info("show_dialog() 被调用")
        
        try:
            self.initialize_api()
            logger.info("API 初始化完成")
            
            # 检查是否有配置的AI模型
            if not self.api or not self.api._ai_model:
                logger.warning("未配置AI模型，显示友好提示")
                from PyQt5.QtWidgets import QMessageBox
                
                # 创建自定义消息框
                msg_box = QMessageBox(self.gui)
                msg_box.setWindowTitle(self.i18n.get('no_ai_configured_title', 'No AI Configured'))
                msg_box.setText(self.i18n.get('no_ai_configured_message', 
                    'Welcome! To start asking questions about your books, you need to configure an AI provider first.\n\n'
                    'Recommended for Beginners:\n'
                    '• Nvidia AI - Get 6 months FREE API access with just your phone number (no credit card required)\n'
                    '• Ollama - Run AI models locally on your computer (completely free and private)\n\n'
                    'Would you like to open the plugin configuration to set up an AI provider now?'))
                msg_box.setIcon(QMessageBox.Information)
                
                # 添加自定义按钮（按从左到右的顺序）
                open_settings_btn = msg_box.addButton(
                    self.i18n.get('open_settings', 'Plugin Configuration'), 
                    QMessageBox.AcceptRole
                )
                ask_anyway_btn = msg_box.addButton(
                    self.i18n.get('ask_anyway', 'Ask Anyway'), 
                    QMessageBox.ActionRole
                )
                later_btn = msg_box.addButton(
                    self.i18n.get('later', 'Later'), 
                    QMessageBox.RejectRole
                )
                
                msg_box.exec_()
                
                clicked_btn = msg_box.clickedButton()
                
                # 如果用户点击"打开设置"
                if clicked_btn == open_settings_btn:
                    self.show_configuration()
                    return
                # 如果用户点击"仍要询问"，继续执行，打开询问弹窗
                elif clicked_btn == ask_anyway_btn:
                    logger.info("用户选择仍要询问，继续打开询问弹窗")
                    # 不return，继续执行下面的代码
                # 如果用户点击"稍后"，直接返回
                else:
                    return
            
            # 获取选中的书籍
            rows = self.gui.library_view.selectionModel().selectedRows()
            logger.info(f"获取选中的书籍行数: {len(rows) if rows else 0}")
            
            if not rows or len(rows) == 0:
                logger.warning("没有选中的书籍，提示用户选择书籍")
                # 提示用户选择书籍
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self.gui,
                    self.i18n.get('no_book_selected_title', 'No Book Selected'),
                    self.i18n.get('no_book_selected_message', 'Please select a book before asking questions.')
                )
                return
            
            # 获取书籍信息
            db = self.gui.current_db
            logger.info("获取数据库实例成功")
            
            # 支持多书选择
            if len(rows) == 1:
                # 单书模式（向后兼容）
                book_id = self.gui.library_view.model().id(rows[0])
                mi = db.get_metadata(book_id, index_is_id=True)
                books_info = mi
                logger.info(f"单书模式: book_id={book_id}, title={mi.title}")
            else:
                # 多书模式
                books_info = []
                for row in rows:
                    book_id = self.gui.library_view.model().id(row)
                    mi = db.get_metadata(book_id, index_is_id=True)
                    books_info.append(mi)
                logger.info(f"多书模式: 共 {len(books_info)} 本书")
            
            # 显示对话框
            d = AskDialog(self.gui, books_info, self.api)
            
            # 保存对话框实例的引用
            self.ask_dialog = d
            
            # 对话框关闭时清除引用
            d.finished.connect(lambda result: setattr(self, 'ask_dialog', None))
            
            d.exec_()
            
        except Exception as e:
            logger.error(f"show_dialog() 发生异常: {str(e)}", exc_info=True)
            # 显示错误消息给用户
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self.gui,
                "错误",
                f"打开询问弹窗时发生错误:\n{str(e)}"
            )
    
    def _show_deprecation_notice(self):
        """显示弃用通知对话框"""
        # 创建消息框
        msg_box = QMessageBox(self.gui)
        msg_box.setWindowTitle(self.i18n['deprecation_notice_title'])
        msg_box.setText(self.i18n['deprecation_notice_message'])
        msg_box.setIcon(QMessageBox.Information)
        
        # 添加按钮（按照添加顺序：左侧到右侧）
        # ActionRole 按钮显示在左侧，RejectRole 按钮显示在右侧
        dont_show_btn = msg_box.addButton(self.i18n['deprecation_dont_show_again'], QMessageBox.ActionRole)
        got_it_btn = msg_box.addButton(self.i18n['deprecation_got_it'], QMessageBox.RejectRole)
        msg_box.setDefaultButton(got_it_btn)
        
        # 显示对话框
        msg_box.exec_()
        
        # 处理用户选择
        clicked_button = msg_box.clickedButton()
        prefs = get_prefs()
        
        if clicked_button == dont_show_btn:
            # 用户选择"不再提醒"
            prefs['show_deprecation_notice'] = False
            logger.info("Deprecation notice disabled by user")
    
    def show_about(self):
        """显示关于对话框"""
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(3)  # 默认显示关于标签页（现在是第4个）
        dlg.exec_()
    
    def show_shortcuts(self):
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(1)  # 默认显示快捷键标签页
        dlg.exec_()
    
    def show_tutorial(self):
        """显示教程对话框"""
        dlg = TabDialog(self.gui)
        dlg.tab_widget.setCurrentIndex(2)  # 默认显示教程标签页（现在是第3个）
        dlg.exec_()
    
    def config_widget(self):
        """
        返回配置对话框组件
        这个方法被 calibre 的插件系统调用，用于显示插件配置界面
        """
        from calibre_plugins.ask_ai_plugin.config import ConfigDialog
        return ConfigDialog(self.gui)
    
    def save_settings(self, config_widget):
        """
        保存配置对话框中的设置
        
        Args:
            config_widget: 由 config_widget() 方法返回的配置组件
        """
        if hasattr(config_widget, 'save_settings'):
            config_widget.save_settings()

    def update_menu_texts(self, language=None):
        """更新菜单项的文本
        
        Args:
            language: 可选参数，指定要使用的语言。如果不指定，则从配置中读取。
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 保存原始状态
            original_texts = {
                'ask': self.ask_action.text(),
                'config': self.config_action.text(),
                'shortcuts': self.shortcuts_action.text(),
                'tutorial': self.tutorial_action.text(),
                'about': self.about_action.text()
            }
            
            # 如果没有指定语言，从配置中读取
            if language is None:
                prefs = get_prefs()
                language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
            
            logger.debug(f"更新菜单文本，使用语言: {language}")
            
            # 更新文本
            self.i18n = get_translation(language)
            self.ask_action.setText(self.i18n['menu_title'])
            self.config_action.setText(self.i18n['config_title'])
            self.shortcuts_action.setText(self.i18n['shortcuts'])
            self.tutorial_action.setText(self.i18n.get('tutorial', 'Tutorial'))
            self.about_action.setText(self.i18n['about'])
            
        except Exception as e:
            # 发生错误时恢复原始状态
            logger.error(f"更新菜单文本时出错: {str(e)}")
            self.ask_action.setText(original_texts['ask'])
            self.config_action.setText(original_texts['config'])
            self.shortcuts_action.setText(original_texts['shortcuts'])
            self.tutorial_action.setText(original_texts['tutorial'])
            self.about_action.setText(original_texts['about'])

class AskGrokConfigWidget(QWidget):
    """配置页面组件"""
    # 定义与 ConfigDialog 相同的信号
    language_changed = pyqtSignal(str)
    settings_saved = pyqtSignal()  # 添加设置保存信号
    
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
        
        # 连接 ConfigDialog 的信号，并转发出去
        self.config_dialog.language_changed.connect(self.on_language_changed)
        self.config_dialog.settings_saved.connect(self.settings_saved.emit)  # 转发设置保存信号
    
    def on_language_changed(self, lang_code):
        """当语言改变时更新界面并转发信号"""
        # 更新自身的语言
        self.i18n = get_translation(lang_code)
        
        # 在日志中输出语言变更信息
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"语言已切换为: {lang_code}")
        
        # 转发语言变更信号
        self.language_changed.emit(lang_code)

class AboutWidget(QWidget):
    """关于页面组件 - 显示 about.md 内容"""
    def __init__(self, parent=None):
        super().__init__(parent)
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建文本浏览器
        from PyQt5.QtWidgets import QTextBrowser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # About 页面允许点击链接
        self.text_browser.setReadOnly(True)
        layout.addWidget(self.text_browser)
        
        # 加载内容
        self.load_content()
        
    def load_content(self):
        """加载 about.md 内容"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 从插件资源读取 about.md
            from calibre.customize.ui import find_plugin
            plugin = find_plugin('Ask AI Plugin')
            
            if not plugin:
                self.text_browser.setHtml("<h2>Error: Plugin not found</h2>")
                return
            
            # 读取 about.md
            about_data = plugin.get_resources('tutorial/about.md')
            
            if not about_data:
                self.text_browser.setHtml("<h2>Error: About file not found</h2>")
                return
            
            about_content = about_data.decode('utf-8')
            
            # 转换 markdown 到 HTML（复用 TutorialWidget 的方法）
            html_content = self._markdown_to_html(about_content)
            
            # 设置 HTML 内容
            self.text_browser.setHtml(html_content)
            
            logger.info(f"About content loaded: {len(about_content)} bytes")
            
        except Exception as e:
            logger.error(f"Failed to load about content: {str(e)}")
            self.text_browser.setHtml(f"<h2>Error loading about content</h2><p>{str(e)}</p>")
    
    def _markdown_to_html(self, markdown_text):
        """简单的 markdown 转 HTML - 极简风格（复用 TutorialWidget 逻辑）"""
        import re
        
        lines = markdown_text.split('\n')
        result = []
        in_paragraph = False
        
        for line in lines:
            stripped = line.strip()
            
            # Headers
            if stripped.startswith('# '):
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                content = stripped[2:]
                result.append(f'<h1>{content}</h1>')
            # Empty line
            elif not stripped:
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
            # Regular text
            else:
                if not in_paragraph:
                    result.append('<p>')
                    in_paragraph = True
                else:
                    result.append('<br>')
                result.append(self._process_inline(stripped))
        
        # Close any open tags
        if in_paragraph:
            result.append('</p>')
        
        html = '\n'.join(result)
        
        # 添加样式 - 极简主义风格，支持明暗模式
        styled_html = f"""
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                line-height: 1.65; 
                padding: 20px;
                color: palette(window-text);
                background: palette(base);
            }}
            h1 {{ 
                color: palette(window-text); 
                border-bottom: 2px solid palette(mid); 
                padding-bottom: 10px;
                font-size: 1.5em;
                margin-top: 0.5em;
                margin-bottom: 0.8em;
            }}
            p {{
                color: palette(window-text);
                margin: 0.5em 0;
            }}
            strong {{
                color: palette(window-text);
                font-weight: bold;
            }}
            a {{
                color: palette(link);
                text-decoration: none;
            }}
        </style>
        {html}
        """
        
        return styled_html
    
    def _process_inline(self, text):
        """处理行内元素：粗体、链接"""
        import re
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Links (keep clickable in About page)
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
        return text
        
    def update_content(self):
        """更新内容（语言切换时调用）"""
        self.load_content()


class TutorialWidget(QWidget):
    """教程页面组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建文本浏览器
        from PyQt5.QtWidgets import QTextBrowser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(False)  # 禁用链接点击
        self.text_browser.setReadOnly(True)  # 只读
        layout.addWidget(self.text_browser)
        
        # 加载教程内容
        self.load_tutorial()
        
    def load_tutorial(self):
        """加载教程内容"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 从插件资源读取教程
            from calibre.customize.ui import find_plugin
            plugin = find_plugin('Ask AI Plugin')
            
            if not plugin:
                self.text_browser.setHtml("<h2>Error: Plugin not found</h2>")
                return
            
            # 读取教程（英文文档，优先加载最新版本；若打包缺失则回退旧文件名）
            tutorial_data = plugin.get_resources('tutorial/tutorial_v0.4.md')
            if not tutorial_data:
                tutorial_data = plugin.get_resources('tutorial/tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md')
            
            if not tutorial_data:
                self.text_browser.setHtml("<h2>Error: Tutorial file not found</h2>")
                return
            
            tutorial_content = tutorial_data.decode('utf-8')
            
            # 转换 markdown 到 HTML
            html_content = self.markdown_to_html(tutorial_content)
            
            # 设置 HTML 内容
            self.text_browser.setHtml(html_content)
            
            logger.info(f"Tutorial loaded: {len(tutorial_content)} bytes")
            
        except Exception as e:
            logger.error(f"Failed to load tutorial: {str(e)}")
            self.text_browser.setHtml(f"<h2>Error loading tutorial</h2><p>{str(e)}</p>")
    
    def markdown_to_html(self, markdown_text):
        """简单的 markdown 转 HTML - 极简风格"""
        import re
        
        lines = markdown_text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        in_paragraph = False
        
        for line in lines:
            stripped = line.strip()
            
            # Headers
            if stripped.startswith('# '):
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                content = stripped[2:]
                result.append(f'<h1>{content}</h1>')
            elif stripped.startswith('## '):
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                content = stripped[3:]
                result.append(f'<h2>{content}</h2>')
            elif stripped.startswith('### '):
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                content = stripped[4:]
                result.append(f'<h3>{content}</h3>')
            # Horizontal rule
            elif stripped == '---':
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                result.append('<hr>')
            # Unordered list
            elif stripped.startswith('- '):
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                if not in_ul:
                    result.append('<ul>')
                    in_ul = True
                content = self._process_inline(stripped[2:])
                result.append(f'<li>{content}</li>')
            # Ordered list
            elif re.match(r'^\d+\.\s+', stripped):
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                if not in_ol:
                    result.append('<ol>')
                    in_ol = True
                content = self._process_inline(re.sub(r'^\d+\.\s+', '', stripped))
                result.append(f'<li>{content}</li>')
            # Empty line
            elif not stripped:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
            # Regular text
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                if not in_paragraph:
                    result.append('<p>')
                    in_paragraph = True
                else:
                    result.append('<br>')
                result.append(self._process_inline(stripped))
        
        # Close any open tags
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        if in_paragraph:
            result.append('</p>')
        
        html = '\n'.join(result)
        
        # 添加样式 - 极简主义风格，支持明暗模式
        styled_html = f"""
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                line-height: 1.65; 
                padding: 20px;
                color: palette(window-text);
                background: palette(base);
            }}
            h1 {{ 
                color: palette(window-text); 
                border-bottom: 2px solid palette(mid); 
                padding-bottom: 10px;
                font-size: 1.5em;
                margin-top: 0.5em;
                margin-bottom: 0.8em;
            }}
            h2 {{ 
                color: palette(window-text); 
                font-weight: bold;
                font-size: 1em;
                margin-top: 1.5em;
                margin-bottom: 0.6em;
            }}
            h3 {{ 
                color: palette(window-text); 
                margin-top: 1.2em;
                margin-bottom: 0.5em;
                font-size: 1em;
                opacity: 0.85;
            }}
            code {{ 
                background: palette(alternate-base); 
                padding: 2px 5px; 
                font-family: monospace;
                color: palette(text);
                border-radius: 3px;
            }}
            ul {{ 
                margin-left: 12px;
                padding-left: 12px;
                color: palette(window-text);
                margin-top: 0.4em;
                margin-bottom: 0.6em;
            }}
            ol {{ 
                margin-left: 12px;
                padding-left: 12px;
                color: palette(window-text);
                margin-top: 0.4em;
                margin-bottom: 0.6em;
            }}
            li {{ 
                margin-bottom: 0.3em;
            }}
            hr {{ 
                border: none; 
                border-top: 1px solid palette(mid); 
                margin: 1.2em 0;
                opacity: 0.5;
            }}
            p {{
                color: palette(window-text);
                margin: 0.5em 0;
            }}
            strong {{
                color: palette(window-text);
                font-weight: bold;
            }}
        </style>
        {html}
        """
        
        return styled_html
    
    def _process_inline(self, text):
        """处理行内元素：粗体、代码、链接"""
        import re
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Links (keep text but remove link functionality)
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<span style="color: palette(link);">\1</span>', text)
        return text
    
    def update_content(self):
        """更新内容（语言切换时调用）"""
        self.load_tutorial()


class TabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gui = parent
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['config_title'])
        self.setMinimumWidth(780)
        self.setMinimumHeight(650)
        # 设置初始窗口大小，确保有足够空间显示所有内容
        self.resize(900, 780)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 连接标签页切换信号
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # 创建General页面
        self.config_widget = AskGrokConfigWidget(self.gui)
        self.tab_widget.addTab(self.config_widget, self.i18n['general_tab'])
        
        # 语言变更信号已在下方连接到config_widget.config_dialog.language_changed

        # 创建快捷键页面
        self.shortcuts_widget = ShortcutsWidget(self)
        self.tab_widget.addTab(self.shortcuts_widget, self.i18n['shortcuts'])

        # 创建教程页面
        self.tutorial_widget = TutorialWidget()
        self.tab_widget.addTab(self.tutorial_widget, self.i18n.get('tutorial', 'Tutorial'))
        
        # 创建关于页面
        self.about_widget = AboutWidget()
        self.tab_widget.addTab(self.about_widget, self.i18n['about'])
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 添加左侧间距
        button_layout.addSpacing(10)
        
        # 获取配置对话框实例
        config_dialog = self.config_widget.config_dialog
        
        # 创建保存按钮（左侧）
        self.save_button = QPushButton(self.i18n.get('save_button', 'Save'))
        self.save_button.clicked.connect(self.on_save_clicked)
        self.save_button.setEnabled(False)  # 初始化时禁用保存按钮
        button_layout.addWidget(self.save_button)
        
        # 创建保存成功提示标签
        self.save_feedback_label = QLabel("")
        self.save_feedback_label.setStyleSheet("color: green; font-weight: bold;")
        self.save_feedback_label.hide()
        button_layout.addWidget(self.save_feedback_label)
        
        # 将配置对话框的配置变更信号连接到更新保存按钮状态的方法
        config_dialog.config_changed.connect(self.update_save_button_state)
        
        # 连接保存成功信号
        config_dialog.settings_saved.connect(self.on_settings_saved)
        
        # 添加弹性空间，使按钮分别位于左右两侧
        button_layout.addStretch()

        # 添加 Reddit 链接（关闭按钮左侧）
        self.reddit_link = QLabel()
        self.reddit_link.setTextFormat(Qt.RichText)
        self.reddit_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.reddit_link.setOpenExternalLinks(True)
        self.reddit_link.setCursor(Qt.PointingHandCursor)
        self.reddit_link.setText('<a href="https://www.reddit.com/r/AskGrokPlugin/">Reddit</a>')
        button_layout.addWidget(self.reddit_link)
        button_layout.addSpacing(12)
        
        # 添加Close按钮（右侧）
        self.close_button = QPushButton(self.i18n.get('close_button', 'Close'))
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        
        # 添加右侧间距
        button_layout.addSpacing(10)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 连接配置组件的信号
        self.config_widget.settings_saved.connect(self.on_settings_saved)
        self.config_widget.language_changed.connect(self.on_language_changed)
    
    def on_language_changed(self, new_language):
        """当语言改变时更新所有组件"""
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"TabDialog接收到语言变更信号: {new_language}")
        
        self.i18n = get_translation(new_language)
        
        # 更新窗口标题
        self.setWindowTitle(self.i18n['config_title'])
        logger.debug(f"更新窗口标题为: {self.i18n['config_title']}")
        
        # 更新标签页标题
        self.tab_widget.setTabText(0, self.i18n['general_tab'])
        self.tab_widget.setTabText(1, self.i18n['shortcuts'])
        self.tab_widget.setTabText(2, self.i18n.get('tutorial', 'Tutorial'))
        self.tab_widget.setTabText(3, self.i18n['about'])
        logger.debug("已更新标签页标题")
        
        # 更新保存按钮文本
        if hasattr(self, 'save_button'):
            self.save_button.setText(self.i18n.get('save_button', 'Save'))
            logger.debug("已更新保存按钮文本")
        
        # 更新所有按钮文本（包括关闭按钮）
        for button in self.findChildren(QPushButton):
            button_text = button.text()
            # 更新关闭按钮
            if button_text in ['Close', '关闭', 'Закрыть', 'Fermer', 'Schließen', 'Cerrar', 'Chiudi', 'Fechar', 'Sluiten', 'Stäng', 'Lukk', 'Sulje', 'Luk', '閉じる', '關閉', '闭']:
                button.setText(self.i18n.get('close_button', 'Close'))
                logger.debug("已更新关闭按钮文本")
        
        # 也更新QDialogButtonBox中的按钮（如果存在）
        for button_box in self.findChildren(QDialogButtonBox):
            close_button = button_box.button(QDialogButtonBox.Close)
            if close_button:
                close_button.setText(self.i18n.get('close_button', 'Close'))
                logger.debug("已更新QDialogButtonBox关闭按钮文本")
        
        # 确保 ConfigDialog 实例也更新了语言
        if hasattr(self.config_widget, 'config_dialog'):
            logger.debug("更新ConfigDialog实例的语言")
            self.config_widget.config_dialog.i18n = self.i18n
            self.config_widget.config_dialog.retranslate_ui()
        
        # 更新快捷键页面
        logger.debug("更新快捷键页面")
        self.shortcuts_widget.update_shortcuts()
        
        # 更新关于页面
        logger.debug("更新关于页面")
        self.about_widget.update_content()
        
        # 通知主界面更新菜单，直接传递新语言参数
        if plugin_instance:
            logger.debug(f"通知主界面更新菜单，语言: {new_language}")
            plugin_instance.update_menu_texts(new_language)
            
            # 更新主对话框的界面语言
            if hasattr(plugin_instance, 'ask_dialog') and plugin_instance.ask_dialog:
                logger.debug(f"更新主对话框的界面语言为: {new_language}")
                # 如果存在update_language方法，直接调用
                if hasattr(plugin_instance.ask_dialog, 'update_language'):
                    plugin_instance.ask_dialog.update_language(new_language)
                
                # 更新 response_handler 和 suggestion_handler 的 i18n 对象
                if hasattr(plugin_instance.ask_dialog, 'suggestion_handler'):
                    logger.debug("更新对话框组件的i18n对象")
                    plugin_instance.ask_dialog.response_handler.update_i18n(self.i18n)
                    plugin_instance.ask_dialog.suggestion_handler.update_i18n(self.i18n)
    
    def show_deprecation_notice(self):
        """显示弃用通知对话框"""
        # 创建消息框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.i18n['deprecation_notice_title'])
        msg_box.setText(self.i18n['deprecation_notice_message'])
        msg_box.setIcon(QMessageBox.Information)
        
        # 添加按钮（按照添加顺序：左侧到右侧）
        # ActionRole 按钮显示在左侧，RejectRole 按钮显示在右侧
        dont_show_btn = msg_box.addButton(self.i18n['deprecation_dont_show_again'], QMessageBox.ActionRole)
        got_it_btn = msg_box.addButton(self.i18n['deprecation_got_it'], QMessageBox.RejectRole)
        msg_box.setDefaultButton(got_it_btn)
        
        # 显示对话框
        msg_box.exec_()
        
        # 处理用户选择
        clicked_button = msg_box.clickedButton()
        prefs = get_prefs()
        
        if clicked_button == dont_show_btn:
            # 用户选择"不再提醒"
            prefs['show_deprecation_notice'] = False
            logger.info("Deprecation notice disabled by user from config dialog")
    
    def on_settings_saved(self):
        """当设置保存时的处理函数"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 重新加载全局 API 实例
        from calibre_plugins.ask_ai_plugin.api import api
        api.reload_model()
        
        # 更新已打开的AskDialog实例的模型信息
        try:
            if plugin_instance and hasattr(plugin_instance, 'ask_dialog') and plugin_instance.ask_dialog:
                # 确保 AskDialog 的 API 实例也被重新加载
                if hasattr(plugin_instance.ask_dialog, 'api'):
                    plugin_instance.ask_dialog.api.reload_model()
                # 然后更新 UI 显示
                plugin_instance.ask_dialog.update_model_info()
                logger.info("配置已保存，模型信息已更新")
        except Exception as e:
            logger.error(f"更新模型信息时出错: {str(e)}")
        
        # 获取最新的语言设置
        new_language = get_prefs().get('language', 'en')
        # 更新界面
        self.on_language_changed(new_language)
    
    def keyPressEvent(self, event):
        """处理按键事件"""
        if event.key() == Qt.Key_Escape:
            # 如果配置页面有未保存的更改，先重置字段
            if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog') and hasattr(self.config_widget.config_dialog, 'check_for_changes'):
                # 使用check_for_changes方法检查是否有未保存的更改
                if self.config_widget.config_dialog.check_for_changes():
                    self.config_widget.config_dialog.reset_to_initial_values()
            # 关闭窗口
            self.reject()
        else:
            super().keyPressEvent(event)
    
    def on_tab_changed(self, index):
        """处理标签页切换事件
        
        :param index: 当前标签页索引
        """
        # 仅在 General 标签页（索引为0）显示保存按钮
        if hasattr(self, 'save_button'):
            self.save_button.setVisible(index == 0)
            
            # 如果切换到 General 标签页，更新保存按钮状态
            if index == 0:
                self.update_save_button_state()
    
    def on_save_clicked(self):
        """处理保存按钮点击事件"""
        if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog'):
            # 调用配置对话框的保存方法
            self.config_widget.config_dialog.save_settings()
    
    def on_settings_saved(self):
        """处理设置保存成功事件"""
        # 禁用保存按钮
        if hasattr(self, 'save_button'):
            self.save_button.setEnabled(False)
        
        # 显示保存成功提示
        if hasattr(self, 'save_feedback_label'):
            self.save_feedback_label.setText(self.i18n.get('saved', 'Saved'))
            self.save_feedback_label.show()
            
            # 1秒后隐藏提示
            QTimer.singleShot(1000, self.save_feedback_label.hide)
    
    def update_save_button_state(self):
        """更新保存按钮的启用/禁用状态"""
        if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog'):
            # 检查是否有配置变更
            config_dialog = self.config_widget.config_dialog
            has_changes = config_dialog.check_for_changes()
            
            # 根据是否有变更设置保存按钮状态
            if hasattr(self, 'save_button'):
                self.save_button.setEnabled(has_changes)
                
            # 如果有变更，隐藏保存成功提示
            if has_changes and hasattr(self, 'save_feedback_label'):
                self.save_feedback_label.hide()
    
    def reject(self):
        """处理关闭按钮"""
        import logging
        from PyQt5.QtWidgets import QMessageBox
        logger = logging.getLogger(__name__)
        
        # 检查是否有未保存的输入框变化
        if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog'):
            config_dialog = self.config_widget.config_dialog
            
            if config_dialog.has_unsaved_input_changes:
                logger.info("检测到未保存的输入框变化，显示确认对话框")
                
                # 创建自定义按钮的确认对话框
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle(self.i18n.get('unsaved_changes_title', 'Unsaved Changes'))
                msg_box.setText(self.i18n.get('unsaved_changes_message', 'You have unsaved changes. What would you like to do?'))
                msg_box.setIcon(QMessageBox.Question)
                
                # 添加自定义按钮（支持 i18n）
                save_button = msg_box.addButton(
                    self.i18n.get('save_and_close', 'Save and Close'), 
                    QMessageBox.AcceptRole
                )
                discard_button = msg_box.addButton(
                    self.i18n.get('discard_changes', 'Discard Changes'), 
                    QMessageBox.DestructiveRole
                )
                cancel_button = msg_box.addButton(
                    self.i18n.get('cancel', 'Cancel'), 
                    QMessageBox.RejectRole
                )
                
                # 设置默认按钮为取消
                msg_box.setDefaultButton(cancel_button)
                
                # 显示对话框
                msg_box.exec_()
                clicked_button = msg_box.clickedButton()
                
                if clicked_button == save_button:
                    # 保存并关闭
                    logger.info("用户选择保存并关闭")
                    config_dialog.save_settings()
                    super().reject()
                elif clicked_button == discard_button:
                    # 不保存，直接关闭
                    logger.info("用户选择不保存，直接关闭")
                    super().reject()
                else:
                    # 取消关闭
                    logger.info("用户取消关闭操作")
                    return
            else:
                # 没有未保存的变化，检查默认 AI 是否有效配置
                if not self._check_default_ai_before_close():
                    # 用户取消关闭或选择切换默认 AI
                    return
                super().reject()
        else:
            super().reject()
    
    def _check_default_ai_before_close(self):
        """关闭前检查默认 AI 是否有效配置
        
        Returns:
            bool: True 表示可以关闭，False 表示用户取消关闭
        """
        import logging
        from PyQt5.QtWidgets import QMessageBox
        logger = logging.getLogger(__name__)
        
        prefs = get_prefs()
        default_ai = prefs.get('selected_model', 'grok')
        
        # 获取已配置的 AI 列表（复用 AskDialog 的逻辑）
        models_config = prefs.get('models', {})
        configured_ai_ids = []
        
        for ai_id, config in models_config.items():
            # 检查是否有模型名称
            has_model = bool(config.get('model', '').strip())
            if not has_model:
                continue
            
            # 检查是否有有效配置
            if ai_id == 'ollama':
                has_valid_config = bool(config.get('api_base_url', '').strip())
                if not has_valid_config:
                    continue
            else:
                token_field = 'auth_token' if ai_id == 'grok' else 'api_key'
                has_token = bool(config.get(token_field, '').strip())
                if not has_token:
                    continue
            
            configured_ai_ids.append(ai_id)
        
        # 检查默认 AI 是否在已配置列表中
        if default_ai not in configured_ai_ids:
            logger.warning(f"默认 AI ({default_ai}) 未有效配置")
            
            # 如果没有任何已配置的 AI，直接关闭
            if not configured_ai_ids:
                logger.warning("没有任何已配置的 AI")
                return True
            
            # 获取第一个已配置的 AI 的显示名称
            first_ai_id = configured_ai_ids[0]
            first_ai_config = models_config.get(first_ai_id, {})
            first_ai_name = first_ai_config.get('display_name', first_ai_id)
            
            # 获取默认 AI 的显示名称
            default_ai_config = models_config.get(default_ai, {})
            default_ai_name = default_ai_config.get('display_name', default_ai)
            
            # 弹窗询问用户
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(self.i18n.get('invalid_default_ai_title', 'Invalid Default AI'))
            msg_box.setText(self.i18n.get('invalid_default_ai_message', 
                'The default AI "{default_ai}" is not properly configured.\n\n'
                'Would you like to switch to "{first_ai}" instead?').format(
                    default_ai=default_ai_name,
                    first_ai=first_ai_name
                ))
            msg_box.setIcon(QMessageBox.Warning)
            
            switch_button = msg_box.addButton(
                self.i18n.get('switch_to_ai', 'Switch to {ai}').format(ai=first_ai_name),
                QMessageBox.AcceptRole
            )
            keep_button = msg_box.addButton(
                self.i18n.get('keep_current', 'Keep Current'),
                QMessageBox.RejectRole
            )
            
            msg_box.setDefaultButton(switch_button)
            msg_box.exec_()
            
            if msg_box.clickedButton() == switch_button:
                # 切换到第一个已配置的 AI
                logger.info(f"用户选择切换默认 AI 到: {first_ai_id}")
                prefs['selected_model'] = first_ai_id
                
                # 更新 ConfigDialog 中的选择
                if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog'):
                    config_dialog = self.config_widget.config_dialog
                    if hasattr(config_dialog, 'model_combo'):
                        index = config_dialog.model_combo.findData(first_ai_id)
                        if index >= 0:
                            config_dialog.model_combo.setCurrentIndex(index)
                            logger.info(f"已更新 ConfigDialog 中的默认 AI 选择")
                
                return True
            else:
                # 保持当前设置
                logger.info("用户选择保持当前默认 AI 设置")
                return True
        
        # 默认 AI 有效配置，可以关闭
        return True


from calibre_plugins.ask_ai_plugin.response_handler import ResponseHandler
from calibre_plugins.ask_ai_plugin.random_question import SuggestionHandler

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
    
    def __init__(self, gui, books_info, api, history_uid=None):
        """
        Args:
            books_info: 单个 Metadata 对象（单书模式）或 Metadata 列表（多书模式）
            history_uid: 可选，用于加载特定历史记录
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            super().__init__(gui)
            logger.info("QDialog 初始化完成")
            
            self.gui = gui
            self.api = api
            prefs = get_prefs()
            language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
            self.i18n = get_translation(language)
            logger.info(f"语言设置: {language}")
        except Exception as e:
            logger.error(f"AskDialog.__init__() 初始化阶段1失败: {str(e)}", exc_info=True)
            raise
        
        # 统一处理为列表
        if isinstance(books_info, list):
            self.books_info = books_info  # 多书模式
            self.is_multi_book = len(books_info) > 1
        else:
            self.books_info = [books_info]  # 单书模式
            self.is_multi_book = False
        
        # 向后兼容：保留 self.book_info 指向第一本书
        self.book_info = self.books_info[0]
        
        # 生成或加载 UID
        self._explicit_history_uid = history_uid
        if history_uid:
            self.current_uid = history_uid
        else:
            self.current_uid = self._generate_uid()
        
        # 准备书籍元数据列表
        self.books_metadata = [self._extract_metadata(book) for book in self.books_info]
        
        # 向后兼容：保留 self.book_metadata
        self.book_metadata = self.books_metadata[0]
        
        # 初始化处理器
        self.response_handler = ResponseHandler(self)
        # 确保 SuggestionHandler 正确初始化
        self.suggestion_handler = SuggestionHandler(parent=self)
        
        # 临时缓存：用于暂存随机问题（在用户点击发送前不保存历史）
        self._pending_random_question = None
        self._is_generating_random_question = False
        
        # 连接语言变更信号
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("连接AskDialog到语言变更信号")
        
        # 将当前对话框保存到插件实例中，方便其他组件访问
        if plugin_instance:
            plugin_instance.ask_dialog = self
            logger.debug("已将AskDialog实例保存到插件实例中")
        
        
        # 设置当前书籍元数据到response_handler
        if hasattr(self.response_handler, 'history_manager'):
            self.response_handler.current_metadata = self.book_metadata
        
        # 读取保存窗口的大小
        prefs = get_prefs()
        self.saved_width = prefs.get('ask_dialog_width', 800)  # 增加默认宽度
        self.saved_height = prefs.get('ask_dialog_height', 600)
        
        # 设置窗口属性
        self.setWindowTitle(self.i18n['menu_title'])
        self.setMinimumWidth(500)  # 增加最小宽度
        self.setMinimumHeight(600)
        
        # 设置窗口标志，启用最大化和最小化按钮
        from PyQt5.QtCore import Qt
        self.setWindowFlags(
            Qt.Window |  # 作为独立窗口
            Qt.WindowMaximizeButtonHint |  # 启用最大化按钮
            Qt.WindowCloseButtonHint |  # 启用关闭按钮
            Qt.WindowTitleHint  # 显示标题栏
        )
        
        # 创建 UI
        self.setup_ui()
        
        # 设置处理器
        self.response_handler.setup(
            response_area=self.response_area,
            send_button=self.send_button,
            i18n=self.i18n,
            api=self.api,
            input_area=self.input_area,  # 添加输入区域
            stop_button=self.stop_button  # 添加停止按钮
        )
        self.suggestion_handler.setup(self.response_area, self.input_area, self.suggest_button, self.api, self.i18n, self.stop_button)
        
        # 添加事件过滤器
        self.input_area.installEventFilter(self)
        
        # 监听输入框内容变化，动态切换按钮高光状态
        self.input_area.textChanged.connect(self._update_button_focus)
        
        # 加载历史记录（仅在显式指定 history_uid 时加载）
        has_loaded_history = self._load_history()

        # 将 Preferences->Shortcuts 中的快捷键绑定到对话框 action（仅对话框窗口内生效）
        try:
            if plugin_instance and hasattr(plugin_instance, 'gui'):
                send_un = plugin_instance.unique_name + ' - ask_dialog_send'
                rand_un = plugin_instance.unique_name + ' - ask_dialog_random_question'

                plugin_instance.gui.keyboard.replace_action(send_un, self.send_action)
                plugin_instance.gui.keyboard.replace_action(rand_un, self.suggest_action)
                plugin_instance.gui.keyboard.finalize()

                # Fallback defaults: if calibre clears defaults due to conflicts,
                # keep dialog usable by applying a local WindowShortcut.
                # Do NOT override user customizations in Preferences->Shortcuts (including disabling).
                cfg_map = {}
                try:
                    cfg_map = plugin_instance.gui.keyboard.config.get('map', {}) or {}
                except Exception:
                    cfg_map = {}

                if (cfg_map.get(send_un) in (None, (), [])) and not self.send_action.shortcuts():
                    key = 'Ctrl+Enter'
                    self.send_action.setShortcuts([QKeySequence(key, QKeySequence.SequenceFormat.PortableText)])

                if (cfg_map.get(rand_un) in (None, (), [])) and not self.suggest_action.shortcuts():
                    key = 'Ctrl+R'
                    self.suggest_action.setShortcuts([QKeySequence(key, QKeySequence.SequenceFormat.PortableText)])
        except Exception:
            pass

        # 初始化后更新所有面板的按钮状态（包括导出历史按钮）
        if hasattr(self, 'response_panels') and self.response_panels:
            for panel in self.response_panels:
                if hasattr(panel, 'update_button_states'):
                    panel.update_button_states()
        
        # 设置窗口大小
        self.resize(self.saved_width, self.saved_height)

        # 连接窗口大小变化信号
        self.resizeEvent = self.on_resize
        
        # 检查默认 AI 是否与当前选中的 AI 一致
        # 只有在没有加载历史记录时才检查（新对话），避免与历史记录的AI冲突
        if not has_loaded_history:
            self._check_default_ai_mismatch()

    def _register_dialog_shortcut(self, action, unique_suffix, shortcut_name, default_keys):
        try:
            if plugin_instance is not None and hasattr(plugin_instance, 'unique_name'):
                unique_name = f'{plugin_instance.unique_name} - {unique_suffix}'
            else:
                unique_name = f'Ask AI Plugin - {unique_suffix}'

            keys = ((default_keys,) if isinstance(default_keys, (str, bytes)) else tuple(default_keys))
            self.gui.keyboard.register_shortcut(
                unique_name,
                shortcut_name,
                default_keys=keys,
                action=action,
                description=None,
                group='Ask AI Plugin',
                persist_shortcut=True,
            )
            # Ensure shortcut dicts get fully initialized (including set_to_default)
            # and key conflicts are resolved for the newly registered shortcut.
            self.gui.keyboard.finalize()
        except NameConflict:
            pass
        except Exception:
            pass

    def _generate_uid(self):
        """生成唯一 UID"""
        import hashlib
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        book_ids = sorted([str(book.id) for book in self.books_info])
        book_ids_str = ','.join(book_ids)
        unique_string = f"{timestamp}_{book_ids_str}"
        uid_hash = hashlib.md5(unique_string.encode()).hexdigest()[:12]
        return f"{timestamp}_{uid_hash}"
    
    def _update_history_info_label(self, ai_id, timestamp, model_info=None):
        """更新历史信息标签
        
        Args:
            ai_id: AI ID
            timestamp: 时间戳
            model_info: 可选，模型信息字典 {'provider_name': str, 'model': str, 'api_base': str}
        """
        from .config import get_prefs
        from .api import APIClient
        from .models.base import DEFAULT_MODELS
        
        # 优先使用 model_info（从历史记录中获取）
        if model_info and isinstance(model_info, dict):
            provider_name = model_info.get('provider_name', '')
            model_name = model_info.get('model', '')
            
            if provider_name and model_name:
                ai_display = f"{provider_name} - {model_name}"
            elif provider_name:
                ai_display = provider_name
            elif model_name:
                ai_display = model_name
            else:
                ai_display = ai_id
        else:
            # 回退到从配置中获取
            prefs = get_prefs()
            ai_configs = prefs.get('ai_configs', {})
            
            if ai_id in ai_configs:
                config = ai_configs[ai_id]
                display_name = config.get('display_name', ai_id)
                model_name = config.get('model', '')
                if model_name:
                    ai_display = f"{display_name} - {model_name}"
                else:
                    ai_display = display_name
            else:
                ai_provider = APIClient._MODEL_TO_PROVIDER.get(ai_id)
                if ai_provider and ai_provider in DEFAULT_MODELS:
                    display_name = DEFAULT_MODELS[ai_provider].display_name
                    model_name = ai_id if ai_id != 'default' else ''
                    if model_name:
                        ai_display = f"{display_name} - {model_name}"
                    else:
                        ai_display = display_name
                else:
                    ai_display = ai_id
        
        # 格式化时间戳（缩略显示）
        try:
            from datetime import datetime
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            # 只显示日期和时间，不显示秒
            time_display = dt.strftime('%m-%d %H:%M')
        except:
            time_display = timestamp
        
        # 更新标签文本（去掉 AI: 前缀）
        info_text = f"{ai_display} | {time_display}"
        logger.info(f"[历史信息标签] 更新标签文本: {info_text}")
        logger.info(f"[历史信息标签] AI ID: {ai_id}, Provider: {model_info.get('provider_name') if model_info else 'N/A'}, Model: {model_info.get('model') if model_info else 'N/A'}")
        self.history_info_label.setText(info_text)
        self.history_info_label.setVisible(True)
        logger.info(f"[历史信息标签] 标签已设置为可见")

    def _extract_metadata(self, book_info):
        """提取单本书的元数据"""
        pubdate = book_info.get('pubdate', '')
        if hasattr(pubdate, 'strftime'):
            pubdate = pubdate.strftime('%Y-%m-%d')
        elif isinstance(pubdate, str) and 'T' in pubdate:
            pubdate = pubdate.split('T')[0]
        
        # 检查书籍是否仍存在于数据库
        try:
            db = self.gui.current_db
            db.get_metadata(book_info.id, index_is_id=True)
            deleted = False
        except:
            deleted = True
        
        return {
            'id': book_info.id,
            'title': book_info.get('title', ''),
            'authors': book_info.get('authors', []),
            'publisher': book_info.get('publisher', ''),
            'pubdate': pubdate,
            'languages': book_info.get('languages', []),
            'series': book_info.get('series', ''),
            'deleted': deleted
        }
    
    def _update_window_title(self):
        """更新窗口标题"""
        if self.is_multi_book:
            book_count = len(self.books_info)
            title = f"{self.i18n['menu_title']} - {book_count}{self.i18n.get('books_unit', '本书')}"
        else:
            title = f"{self.i18n['menu_title']} - {self.book_info.title}"
        
        self.setWindowTitle(title)
    
    def _create_metadata_widget(self):
        """创建可折叠的元数据展示组件"""
        from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
        from PyQt5.QtGui import QColor
        from PyQt5.QtCore import Qt
        
        self.metadata_tree = QTreeWidget()
        self.metadata_tree.setHeaderHidden(True)
        # 设置为3行文字的高度（每行约20px，加上一些边距）
        self.metadata_tree.setMaximumHeight(70)  # 3行 x 20px + 边距 ≈ 70px
        # 确保在内容超出时显示垂直滚动条
        self.metadata_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 禁用水平滚动条，避免横向滚动
        self.metadata_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        for idx, book_meta in enumerate(self.books_metadata):
            # 创建书籍节点
            book_item = QTreeWidgetItem(self.metadata_tree)
            
            # 设置书籍标题
            title_text = f"{idx + 1}. {book_meta['title']}"
            if book_meta['deleted']:
                title_text += f" ({self.i18n.get('deleted', '已删除')})"
                book_item.setForeground(0, QColor(128, 128, 128))
            
            book_item.setText(0, title_text)
            
            # 添加元数据子节点
            if book_meta['authors']:
                author_item = QTreeWidgetItem(book_item)
                author_item.setText(0, f"{self.i18n['metadata_authors']}: {', '.join(book_meta['authors'])}")
            
            if book_meta['publisher']:
                pub_item = QTreeWidgetItem(book_item)
                pub_item.setText(0, f"{self.i18n['metadata_publisher']}: {book_meta['publisher']}")
            
            if book_meta['pubdate']:
                date_item = QTreeWidgetItem(book_item)
                date_item.setText(0, f"{self.i18n['metadata_pubyear']}: {book_meta['pubdate']}")
            
            if book_meta['languages']:
                lang_item = QTreeWidgetItem(book_item)
                lang_name = self.get_language_name(book_meta['languages'][0])
                lang_item.setText(0, f"{self.i18n['metadata_language']}: {lang_name}")
            
            if book_meta['series']:
                series_item = QTreeWidgetItem(book_item)
                series_item.setText(0, f"{self.i18n['metadata_series']}: {book_meta['series']}")
            
            # 设置默认展开/收起状态
            # 单书模式：展开；多书模式：收起
            # 但两种模式都显示书名（作为树节点的根节点文本）
            book_item.setExpanded(not self.is_multi_book)
        
        return self.metadata_tree
    
    def _build_multi_book_prompt(self, question):
        """构建多书提示词"""
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        
        template = prefs.get('multi_book_template', '')
        if not template:
            template = """以下是关于多本书籍的信息：

{books_metadata}

用户问题：{query}

请基于以上书籍信息回答问题。"""
        
        # 拼接所有书籍元数据（包含所有字段：标题、作者、出版日期、系列、出版社、语言）
        books_metadata_text = []
        for idx, book in enumerate(self.books_info, 1):
            book_text = f"书籍 {idx}:\n"
            book_text += f"  标题: {book.title}\n"
            
            if book.authors:
                book_text += f"  作者: {', '.join(book.authors)}\n"
            
            if hasattr(book, 'pubdate') and book.pubdate:
                year = str(book.pubdate.year) if hasattr(book.pubdate, 'year') else str(book.pubdate)
                book_text += f"  出版日期: {year}\n"
            
            if hasattr(book, 'series') and book.series:
                book_text += f"  系列: {book.series}\n"
            
            if book.publisher:
                book_text += f"  出版社: {book.publisher}\n"
            
            if book.language:
                lang_name = self.get_language_name(book.language)
                book_text += f"  语言: {lang_name}\n"
            
            books_metadata_text.append(book_text)
        
        prompt = template.format(
            books_metadata='\n'.join(books_metadata_text),
            query=question
        )
        
        return prompt
    
    def _create_history_switcher(self):
        """创建历史记录切换按钮和菜单"""
        from PyQt5.QtWidgets import QToolButton, QMenu, QActionGroup
        from .ui_constants import BUTTON_HEIGHT
        
        self.history_button = QToolButton()
        self.history_button.setText(self.i18n.get('history', '历史记录'))
        self.history_button.setPopupMode(QToolButton.InstantPopup)  # 点击整个按钮弹出菜单
        
        self.history_menu = QMenu()
        self.history_button.setMenu(self.history_menu)
        
        # 创建动作组，用于实现单选效果
        self.history_action_group = QActionGroup(self)
        self.history_action_group.setExclusive(True)
        
        # 设置与 AI 切换器一致的样式和大小
        self.history_button.setMinimumWidth(200)  # 与 AI 切换器相同
        self.history_button.setFixedHeight(BUTTON_HEIGHT)  # 与 AI 切换器相同高度
        
        # 应用标准的 ToolButton 菜单样式
        from .ui_constants import get_toolbutton_menu_style
        self.history_button.setStyleSheet(get_toolbutton_menu_style())
        
        self._load_related_histories()
        
        return self.history_button
    
    def _load_related_histories(self):
        """加载当前书籍关联的所有历史记录"""
        import logging
        logger = logging.getLogger(__name__)
        
        if not hasattr(self.response_handler, 'history_manager'):
            return
        
        # 动态调整菜单最大宽度，防止超出窗口
        window_width = self.width()
        # 菜单最大宽度为窗口宽度的 70%，但不超过 500px，不小于 250px
        max_menu_width = max(250, min(500, int(window_width * 0.7)))
        
        # 使用 setMaximumWidth 而不是 setStyleSheet，这样可以保留 Qt 默认的 hover 效果
        self.history_menu.setMaximumWidth(max_menu_width)
        
        
        # 清空菜单和动作组
        self.history_menu.clear()
        # 清空动作组中的所有动作
        for action in self.history_action_group.actions():
            self.history_action_group.removeAction(action)
        
        # 获取当前书籍的所有历史记录
        book_ids = [book.id for book in self.books_info]
        all_histories = self.response_handler.history_manager.get_related_histories(book_ids)
        
        if not all_histories:
            # 如果没有历史记录，只显示提示，不显示其他选项
            no_history_action = self.history_menu.addAction(self.i18n.get('no_history', 'No history records'))
            no_history_action.setEnabled(False)
            return
        
        # 有历史记录时，添加“新对话”选项
        new_conversation_action = self.history_menu.addAction(self.i18n.get('new_conversation', 'New Conversation'))
        new_conversation_action.setCheckable(True)
        new_conversation_action.triggered.connect(self._on_new_conversation)
        self.history_action_group.addAction(new_conversation_action)
        
        # 添加分隔线
        self.history_menu.addSeparator()
        
        # 历史记录列表（按时间倒序显示）
        # 根据菜单宽度动态计算问题预览的最大字符数
        # 估算：每个字符约占 8-10px，时间戳约占 150px，留出边距和图标空间
        max_question_chars = max(15, int((max_menu_width - 200) / 10))
        
        # 标记是否找到匹配的历史记录
        found_match = False
        
        for idx, history in enumerate(all_histories):
            book_count = len(history['books'])
            # 显示问题的前 N 个字符（根据菜单宽度动态调整）
            question_text = history.get('question', '').strip()
            if not question_text:
                # 使用占位符文本显示空问题
                question_preview = self.i18n.get('empty_question_placeholder', '(No question)')
            else:
                question_preview = question_text[:max_question_chars]
                if len(question_text) > max_question_chars:
                    question_preview += '...'
            display_text = f"{question_preview} - {history['timestamp']}"
            
            
            action = self.history_menu.addAction(display_text)
            action.setCheckable(True)
            # 如果是当前UID，设置为选中状态
            if history['uid'] == self.current_uid:
                action.setChecked(True)
                found_match = True
            else:
                pass
            action.triggered.connect(lambda checked, uid=history['uid']: self._on_history_switched(uid))
            # 添加到动作组，实现单选效果
            self.history_action_group.addAction(action)
        
        # 如果没有找到匹配的历史记录，选中"新对话"
        if not found_match:
            new_conversation_action.setChecked(True)
        else:
            pass
        
        # 在底部添加分隔线和清空选项
        self.history_menu.addSeparator()
        clear_action = self.history_menu.addAction(self.i18n.get('clear_current_book_history', 'Clear Current Book History'))
        clear_action.triggered.connect(self._on_clear_current_book_history)
    
    def _on_new_conversation(self):
        """新对话事件：清空输入和响应区域，并生成新的UID"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 生成新的UID，确保新对话不会覆盖旧的历史记录
        self.current_uid = self._generate_uid()
        logger.info(f"新对话已生成新的UID: {self.current_uid}")
        
        # 清空输入区域
        self.input_area.clear()
        
        # 清空所有面板的响应区域
        if hasattr(self, 'response_panels') and self.response_panels:
            for panel in self.response_panels:
                panel.clear_response()
            logger.info(f"切换到新对话，已清空 {len(self.response_panels)} 个面板")
        else:
            # 单面板模式（向后兼容）
            self.response_area.clear()
            logger.info("切换到新对话，已清空响应区域")
        
        # 刷新历史记录菜单，更新选中状态
        self._load_related_histories()
    
    def _on_history_switched(self, uid):
        """历史记录切换事件"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取历史记录
        history = self.response_handler.history_manager.get_history_by_uid(uid)
        if not history:
            logger.warning(f"未找到历史记录: {uid}")
            return
        
        
        # 重建书籍列表
        books_info = []
        book_ids_to_select = []  # 用于反向选择
        
        for book_meta in history['books']:
            book_ids_to_select.append(book_meta['id'])
            if not book_meta['deleted']:
                try:
                    db = self.gui.current_db
                    mi = db.get_metadata(book_meta['id'], index_is_id=True)
                    books_info.append(mi)
                except Exception as e:
                    logger.warning(f"无法加载书籍 {book_meta['id']}: {str(e)}")
        
        # 更新当前状态
        if books_info:
            self.books_info = books_info
            self.book_info = books_info[0]
        self.is_multi_book = len(history['books']) > 1
        self.current_uid = uid
        
        # 重新提取元数据
        self.books_metadata = [self._extract_metadata(book) for book in self.books_info]
        self.book_metadata = self.books_metadata[0]
        
        # 反向选择：在 Calibre 中选中这些书籍（如果技术可行）
        self._select_books_in_calibre(book_ids_to_select)
        
        # 更新 UI
        self._update_window_title()
        self._rebuild_metadata_widget()
        
        # 加载问答内容
        self.input_area.setPlainText(history['question'])
        
        # 处理多AI响应格式
        if 'answers' in history and isinstance(history['answers'], dict):
            # 新格式：多AI响应
            if hasattr(self, 'response_panels') and self.response_panels:
                # 多面板模式：根据历史记录中的AI响应来加载
                # 获取历史记录中所有AI的ID（排除'default'）
                history_ai_ids = [ai_id for ai_id in history['answers'].keys() if ai_id != 'default']
                
                # 如果历史记录中没有具体AI ID，只有default，则使用default
                if not history_ai_ids and 'default' in history['answers']:
                    history_ai_ids = ['default']
                
                logger.info(f"历史记录中包含 {len(history_ai_ids)} 个AI响应: {history_ai_ids}")
                
                # 为每个历史AI响应分配一个面板
                for idx, ai_id in enumerate(history_ai_ids):
                    if idx >= len(self.response_panels):
                        logger.warning(f"历史记录有 {len(history_ai_ids)} 个AI响应，但只有 {len(self.response_panels)} 个面板")
                        break
                    
                    panel = self.response_panels[idx]
                    answer_data = history['answers'][ai_id]
                    answer_text = answer_data.get('answer', answer_data) if isinstance(answer_data, dict) else answer_data
                    
                    # 智能AI切换：检查历史AI是否仍然可用
                    if ai_id != 'default':
                        # 阻止信号触发，避免重复调用_update_all_panel_ai_switchers
                        panel.ai_switcher.blockSignals(True)
                        
                        # 检查历史AI是否在当前可用的AI列表中
                        ai_found = False
                        for i in range(panel.ai_switcher.count()):
                            if panel.ai_switcher.itemData(i) == ai_id:
                                panel.ai_switcher.setCurrentIndex(i)
                                logger.info(f"面板 {idx} 切换到历史AI: {ai_id}")
                                ai_found = True
                                break
                        
                        # 如果历史AI不可用，使用默认AI
                        if not ai_found:
                            prefs = get_prefs()
                            default_ai = prefs.get('selected_model', 'grok')
                            logger.warning(f"历史AI {ai_id} 不可用，切换到默认AI: {default_ai}")
                            
                            # 尝试切换到默认AI
                            for i in range(panel.ai_switcher.count()):
                                if panel.ai_switcher.itemData(i) == default_ai:
                                    panel.ai_switcher.setCurrentIndex(i)
                                    logger.info(f"面板 {idx} 已切换到默认AI: {default_ai}")
                                    break
                        
                        panel.ai_switcher.blockSignals(False)
                    
                    # 先设置当前问题
                    panel.set_current_question(history['question'])
                    
                    # 加载历史响应
                    panel.response_handler._update_ui_from_signal(
                        answer_text,
                        is_response=True,
                        is_history=True
                    )
                    logger.info(f"为面板 {idx} 加载AI {ai_id} 的历史响应（长度: {len(answer_text)}）")
                    
                    # 更新历史信息标签（只在第一个面板时更新）
                    if idx == 0:
                        timestamp = history.get('timestamp', '未知时间')
                        # 从answer_data中获取model_info（正确的位置）
                        model_info = answer_data.get('model_info', None) if isinstance(answer_data, dict) else None
                        logger.info(f"[加载历史] AI={ai_id}, model_info={'存在' if model_info else '不存在'}")
                        
                        # 如果历史记录中没有model_info（旧版本），从面板API获取
                        if not model_info and hasattr(panel, 'api'):
                            api_obj = panel.api
                            model_info = {
                                'provider_name': getattr(api_obj, 'provider_name', 'Unknown'),
                                'model': getattr(api_obj, 'model', 'Unknown'),
                                'api_base': getattr(api_obj, 'api_base', '')
                            }
                        
                        self._update_history_info_label(ai_id, timestamp, model_info)
                    
                    # 再次更新按钮状态（确保在响应加载后更新）
                    panel.update_button_states()
                
                # 清空未使用的面板
                for idx in range(len(history_ai_ids), len(self.response_panels)):
                    self.response_panels[idx].response_area.clear()
                    logger.debug(f"清空未使用的面板 {idx}")
                
                # 统一更新所有面板的AI切换器（实现互斥逻辑）
                self._update_all_panel_ai_switchers()
            else:
                # 单面板模式：加载default或第一个AI的响应
                if 'default' in history['answers']:
                    answer_data = history['answers']['default']
                elif history['answers']:
                    answer_data = list(history['answers'].values())[0]
                else:
                    answer_data = ''
                
                answer_text = answer_data.get('answer', answer_data) if isinstance(answer_data, dict) else answer_data
                self.response_handler._update_ui_from_signal(
                    answer_text,
                    is_response=True,
                    is_history=True
                )
        else:
            # 旧格式：单一响应（向后兼容）
            answer = history.get('answer', '')
            self.response_handler._update_ui_from_signal(
                answer,
                is_response=True,
                is_history=True
            )
        
        
        # 刷新历史记录菜单，更新选中状态
        self._load_related_histories()
    
    def _on_clear_current_book_history(self):
        """清空当前书籍的历史记录"""
        from PyQt5.QtWidgets import QMessageBox
        import logging
        logger = logging.getLogger(__name__)
        
        # 确认对话框
        book_count = len(self.books_info)
        book_titles = ', '.join([book.title[:20] for book in self.books_info[:3]])
        if book_count > 3:
            book_titles += f" ... ({book_count} books)"
        
        confirm_msg = self.i18n.get(
            'confirm_clear_book_history',
            'Are you sure you want to clear all history for:\n{book_titles}?'
        ).format(book_titles=book_titles)
        
        reply = QMessageBox.question(
            self,
            self.i18n.get('confirm', 'Confirm'),
            confirm_msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 获取当前书籍的所有历史记录
        book_ids = [book.id for book in self.books_info]
        all_histories = self.response_handler.history_manager.get_related_histories(book_ids)
        
        # 删除所有相关历史记录
        deleted_count = 0
        for history in all_histories:
            uid = history['uid']
            if self.response_handler.history_manager.delete_history(uid):
                deleted_count += 1
        
        
        # 清空当前界面
        self.input_area.clear()
        if hasattr(self, 'response_panels') and self.response_panels:
            for panel in self.response_panels:
                panel.clear_response()
        else:
            self.response_area.clear()
        
        # 重新加载历史记录菜单
        self._load_related_histories()
        
        # 显示成功消息
        success_msg = self.i18n.get('history_cleared', '{deleted_count} history records cleared.').format(deleted_count=deleted_count)
        QMessageBox.information(
            self,
            self.i18n.get('success', 'Success'),
            success_msg
        )
    
    def _select_books_in_calibre(self, book_ids):
        """在 Calibre 主界面中选中指定书籍"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            from PyQt5.QtCore import QItemSelectionModel
            
            # 清除当前选择
            self.gui.library_view.selectionModel().clear()
            
            # 选中指定书籍
            db = self.gui.current_db
            selected_count = 0
            
            for book_id in book_ids:
                try:
                    # 使用 Calibre 的 API 选中书籍
                    # 通过 set_current_row 方法选中书籍
                    if db.has_id(book_id):
                        # 使用 select_rows 方法选中多本书
                        self.gui.library_view.select_rows([book_id], using_ids=True, change_current=False)
                        selected_count += 1
                    else:
                        logger.debug(f"书籍 {book_id} 不存在于数据库中")
                except Exception as e:
                    logger.debug(f"书籍 {book_id} 可能已被删除或不在当前视图中: {str(e)}")
            
            logger.info(f"在 Calibre 中选中了 {selected_count}/{len(book_ids)} 本书")
            
        except Exception as e:
            logger.warning(f"无法在 Calibre 中选中书籍: {str(e)}")
    
    def _rebuild_metadata_widget(self):
        """重建元数据组件"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 查找并移除旧的元数据树
            if hasattr(self, 'metadata_tree'):
                self.metadata_tree.setParent(None)
                self.metadata_tree.deleteLater()
            
            # 创建新的元数据树
            new_metadata_tree = self._create_metadata_widget()
            
            # 找到滚动内容的布局并插入
            # 由于使用了滚动区域，需要获取 scroll_content 的布局
            scroll_content = self.scroll_area.widget()
            layout = scroll_content.layout()
            # 元数据树应该在顶部栏之后，输入区域之前
            # 索引 1 的位置（0是顶部栏，1是元数据树，2是输入区域...）
            layout.insertWidget(1, new_metadata_tree)
            
            # 更新顶部书籍信息标签
            if hasattr(self, 'books_info_label'):
                if self.is_multi_book:
                    book_count = len(self.books_info)
                    books_info_text = f"({book_count}{self.i18n.get('books_unit', '本书')})"
                else:
                    books_info_text = f"({self.book_info.title[:30]}{'...' if len(self.book_info.title) > 30 else ''})"
                self.books_info_label.setText(books_info_text)
                logger.debug(f"已更新书籍信息标签: {books_info_text}")
            
            logger.info("元数据组件已重建")
            
        except Exception as e:
            logger.error(f"重建元数据组件失败: {str(e)}")

    def _load_history(self):
        """加载历史记录 - 智能匹配当前书籍组合
        
        Returns:
            bool: 如果成功加载了历史记录返回True，否则返回False
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 首先检查是否有待发送的随机问题
            book_ids = tuple(sorted([book.id for book in self.books_info]))
            prefs = get_prefs()
            pending_questions = prefs.get('pending_random_questions', {})
            
            if str(book_ids) in pending_questions:
                pending_data = pending_questions[str(book_ids)]
                
                # 恢复待发送的随机问题状态
                self.current_uid = pending_data['uid']
                self._pending_random_question = pending_data['question']
                self._is_generating_random_question = True
                self.input_area.setPlainText(pending_data['question'])
                
                # 清空响应区域（因为还没有AI回答）
                if hasattr(self, 'response_panels') and self.response_panels:
                    for panel in self.response_panels:
                        panel.clear_response()
                else:
                    self.response_area.clear()
                
                logger.info("已恢复待发送的随机问题状态，等待用户点击发送")
                # 不从临时存储中删除，等用户发送后再删除
                # 这不算加载历史记录，因为还没有AI回答
                return False

            # 新打开对话框默认视为“新对话”，不自动加载最近历史
            # 否则会覆盖 Config 中的默认 AI / 用户当前选择
            if not self._explicit_history_uid:
                return False
            
            # 获取当前书籍ID集合
            current_book_ids = set([book.id for book in self.books_info])
            
            # 获取所有相关历史记录
            all_histories = self.response_handler.history_manager.get_related_histories(list(current_book_ids))
            
            if not all_histories:
                return False
            
            # 查找最佳匹配的历史记录（始终加载最新的，不过滤空问题）
            matched_history = None
            
            # 优先级1: 完全匹配（UID相同的书籍组合）
            for history in all_histories:
                history_book_ids = set([book['id'] for book in history['books']])
                if history_book_ids == current_book_ids:
                    matched_history = history
                    question = history.get('question', '').strip()
                    question_preview = question[:30] + '...' if len(question) > 30 else question if question else '(空问题)'
                    # 使用现有 UID，不创建新的
                    old_uid = self.current_uid
                    self.current_uid = history['uid']
                    break
            
            # 优先级2: 当前选择被包含在某个历史记录中
            if not matched_history:
                for history in all_histories:
                    history_book_ids = set([book['id'] for book in history['books']])
                    if current_book_ids.issubset(history_book_ids):
                        matched_history = history
                        question = history.get('question', '').strip()
                        question_preview = question[:30] + '...' if len(question) > 30 else question if question else '(空问题)'
                        # 保持当前 UID，只有发起新对话时才会创建新 UID
                        break
            
            # 如果找到匹配的历史记录，加载它
            if matched_history:
                self.input_area.setPlainText(matched_history['question'])
                
                # 检查是否有多面板模式
                if hasattr(self, 'response_panels') and self.response_panels:
                    # 多面板模式：为每个面板加载对应AI的历史响应
                    
                    if 'answers' in matched_history and matched_history['answers']:
                        # 获取历史记录中所有AI的ID（排除'default'）
                        history_ai_ids = [ai_id for ai_id in matched_history['answers'].keys() if ai_id != 'default']
                        
                        # 如果历史记录中没有具体AI ID，只有default，则使用default
                        if not history_ai_ids and 'default' in matched_history['answers']:
                            history_ai_ids = ['default']
                        
                        
                        # 为每个历史AI响应分配一个面板
                        for idx, ai_id in enumerate(history_ai_ids):
                            if idx >= len(self.response_panels):
                                logger.warning(f"历史记录有 {len(history_ai_ids)} 个AI响应，但只有 {len(self.response_panels)} 个面板")
                                break
                            
                            panel = self.response_panels[idx]
                            answer_data = matched_history['answers'][ai_id]
                            answer_text = answer_data.get('answer', answer_data) if isinstance(answer_data, dict) else answer_data
                            
                            # 智能AI切换：检查历史AI是否仍然可用
                            if ai_id != 'default':
                                # 阻止信号触发，避免重复调用_update_all_panel_ai_switchers
                                panel.ai_switcher.blockSignals(True)
                                
                                # 检查历史AI是否在当前可用的AI列表中
                                ai_found = False
                                for i in range(panel.ai_switcher.count()):
                                    if panel.ai_switcher.itemData(i) == ai_id:
                                        panel.ai_switcher.setCurrentIndex(i)
                                        logger.info(f"面板 {idx} 切换到历史AI: {ai_id}")
                                        ai_found = True
                                        break
                                
                                # 如果历史AI不可用，使用默认AI
                                if not ai_found:
                                    prefs = get_prefs()
                                    default_ai = prefs.get('selected_model', 'grok')
                                    logger.warning(f"历史AI {ai_id} 不可用，切换到默认AI: {default_ai}")
                                    
                                    # 尝试切换到默认AI
                                    for i in range(panel.ai_switcher.count()):
                                        if panel.ai_switcher.itemData(i) == default_ai:
                                            panel.ai_switcher.setCurrentIndex(i)
                                            logger.info(f"面板 {idx} 已切换到默认AI: {default_ai}")
                                            break
                                
                                panel.ai_switcher.blockSignals(False)
                            
                            # 先设置当前问题
                            panel.set_current_question(matched_history['question'])
                            
                            # 加载历史响应
                            panel.response_handler._update_ui_from_signal(
                                answer_text,
                                is_response=True,
                                is_history=True
                            )
                            logger.info(f"为面板 {idx} 加载AI {ai_id} 的历史响应（长度: {len(answer_text)}）")
                            
                            # 更新历史信息标签（只在第一个面板时更新）
                            if idx == 0:
                                timestamp = matched_history.get('timestamp', '未知时间')
                                # 从answer_data中获取model_info（正确的位置）
                                model_info = answer_data.get('model_info', None) if isinstance(answer_data, dict) else None
                                logger.info(f"[加载历史] AI={ai_id}, model_info={'存在' if model_info else '不存在'}")
                                
                                # 如果历史记录中没有model_info（旧版本），从面板API获取
                                if not model_info and hasattr(panel, 'api'):
                                    api_obj = panel.api
                                    model_info = {
                                        'provider_name': getattr(api_obj, 'provider_name', 'Unknown'),
                                        'model': getattr(api_obj, 'model', 'Unknown'),
                                        'api_base': getattr(api_obj, 'api_base', '')
                                    }
                                
                                self._update_history_info_label(ai_id, timestamp, model_info)
                            
                            # 再次更新按钮状态（确保在响应加载后更新）
                            panel.update_button_states()
                        
                        # 清空未使用的面板
                        logger.info(f"准备清空未使用的面板，范围: {len(history_ai_ids)} 到 {len(self.response_panels)}")
                        for idx in range(len(history_ai_ids), len(self.response_panels)):
                            panel = self.response_panels[idx]
                            logger.info(f"准备清空面板 {idx}，panel_index={panel.panel_index}")
                            panel.response_area.clear()
                            # 清空后更新按钮状态，禁用复制按钮
                            logger.info(f"面板 {idx} 已清空，准备更新按钮状态")
                            panel.update_button_states()
                            logger.info(f"面板 {idx} 按钮状态已更新")
                        
                        # 统一更新所有面板的AI切换器（实现互斥逻辑）
                        self._update_all_panel_ai_switchers()
                    else:
                        logger.warning("历史记录中没有answers字段")
                else:
                    # 单面板模式（向后兼容）
                    logger.info("单面板模式，加载历史记录")
                    
                    # 兼容新旧格式：优先使用answers字典，回退到answer字段
                    if 'answers' in matched_history and matched_history['answers']:
                        # 新格式：从answers字典中获取第一个响应（通常是'default'或第一个AI的响应）
                        first_ai_id = list(matched_history['answers'].keys())[0]
                        answer_data = matched_history['answers'][first_ai_id]
                        answer_text = answer_data['answer'] if isinstance(answer_data, dict) else answer_data
                    elif 'answer' in matched_history:
                        # 旧格式：直接使用answer字段
                        answer_text = matched_history['answer']
                        logger.info("加载旧格式历史记录")
                    else:
                        answer_text = ""
                        logger.warning("历史记录中没有找到答案内容")
                    
                    if answer_text:
                        self.response_handler._update_ui_from_signal(
                            answer_text, 
                            is_response=True,
                            is_history=True
                        )
                
                logger.info(f"已加载历史记录，时间: {matched_history.get('timestamp', '未知')}")
                
                # 更新导出历史按钮状态
                if hasattr(self, 'response_panels') and self.response_panels:
                    for panel in self.response_panels:
                        if hasattr(panel, 'update_export_all_button_state'):
                            panel.update_export_all_button_state()
                
                # 刷新历史记录菜单，更新选中状态
                self._load_related_histories()
                
                # 成功加载了历史记录
                return True
            else:
                logger.info("没有找到匹配的历史记录（书籍组合不同），显示新对话")
                
                # 即使没有匹配的历史记录，也要更新按钮状态（可能有其他历史记录）
                if hasattr(self, 'response_panels') and self.response_panels:
                    for panel in self.response_panels:
                        if hasattr(panel, 'update_export_all_button_state'):
                            panel.update_export_all_button_state()
                
                # 没有加载历史记录
                return False
                
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    # 注意：clear_history() 方法已废弃，使用 _on_clear_current_book_history() 代替
    
    def closeEvent(self, event):
        # 保存窗口大小
        prefs = get_prefs()
        prefs['ask_dialog_width'] = self.width()
        prefs['ask_dialog_height'] = self.height()
        
        # 清理资源
        if hasattr(self.response_handler, 'cleanup'):
            self.response_handler.cleanup()
        if hasattr(self.suggestion_handler, 'cleanup'):
            self.suggestion_handler.cleanup()
            
        event.accept()
        
    def copy_response(self):
        """复制响应内容到剪贴板"""
        clipboard = QApplication.clipboard()
        response_text = self.response_area.toPlainText()
        if response_text.strip():
            clipboard.setText(response_text)
            self._show_copy_tooltip(self.copy_response_btn, self.i18n.get('copied', 'Copied!'))
            
    def copy_question_response(self):
        """复制问题和响应内容到剪贴板"""
        clipboard = QApplication.clipboard()
        question = self.input_area.toPlainText().strip()
        response = self.response_area.toPlainText().strip()
        
        if not question and not response:
            return
            
        # 组合问题和答案，用分隔线隔开
        text = f"{question}\n\n----\n\n{response}" if question and response else (question or response)
        clipboard.setText(text)
        self._show_copy_tooltip(self.copy_qr_btn, self.i18n.get('copied', 'Copied!'))
    
    def _show_copy_tooltip(self, button, text):
        """在按钮位置显示复制成功的提示"""
        from PyQt5.QtWidgets import QToolTip
        QToolTip.showText(button.mapToGlobal(button.rect().bottomLeft()), text, button, button.rect(), 2000)

    def on_resize(self, event):
        """窗口大小变化时的处理函数（包含响应式布局调整）"""
        prefs = get_prefs()
        prefs['ask_dialog_width'] = self.width()
        prefs['ask_dialog_height'] = self.height()
        
        # 响应式布局调整
        height = self.height()
        
        # 小屏幕优化（高度 < 650px）
        if height < 650:
            # 折叠元数据树（如果是多书模式）
            if hasattr(self, 'metadata_tree') and self.is_multi_book:
                for i in range(self.metadata_tree.topLevelItemCount()):
                    item = self.metadata_tree.topLevelItem(i)
                    if item:
                        item.setExpanded(False)
            
            # 减小输入框高度
            if hasattr(self, 'input_area'):
                self.input_area.setFixedHeight(60)
            
            # 减小响应面板最小高度
            if hasattr(self, 'response_panels'):
                for panel in self.response_panels:
                    panel.setMinimumHeight(250)
        else:
            # 正常尺寸：恢复默认设置
            if hasattr(self, 'input_area'):
                self.input_area.setFixedHeight(80)
            
            # 恢复响应面板最小高度
            if hasattr(self, 'response_panels'):
                for panel in self.response_panels:
                    panel.setMinimumHeight(350)
        
        super().resizeEvent(event)

    def update_model_info(self):
        """更新模型信息显示
        在配置更改后调用此方法，更新界面上显示的模型信息
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 确保模型已经重新加载
            self.api.reload_model()
            
            # 获取最新的模型显示名称
            model_display_name = self.api.model_display_name
            logger.debug(f"更新模型信息: {model_display_name}")
            
            # 更新窗口标题
            if hasattr(self, 'book_info') and self.book_info:
                self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
                logger.debug("已更新窗口标题")
            else:
                logger.warning("无法更新窗口标题: 书籍信息不可用")
                
        except Exception as e:
            logger.error(f"更新模型信息时出错: {str(e)}")
    
    # 注意：_populate_model_switcher() 方法已废弃，因为全局模型切换器已被移除
    
    # 注意：on_model_switched() 方法已废弃，因为全局模型切换器已被移除
    # 现在每个面板都有自己的AI切换器，切换逻辑在 response_panel.py 中处理
    
    def get_language_name(self, lang_code):
        """将语言代码转换为易读的语言名称"""
        if not lang_code:
            return None
        lang_code = lang_code.lower().strip()
        return self.LANGUAGE_MAP.get(lang_code, lang_code)
    
    def _create_response_container(self, count: int, action_layout=None):
        """根据并行AI数量创建响应容器
        
        Args:
            count: 并行AI数量 (目前仅支持1-2)
            action_layout: 操作区域的布局，用于添加 AI 切换器
        
        Returns:
            包含响应面板的容器组件
        """
        from .response_panel import ResponsePanel
        
        # 限制为1-2个（3-4功能暂未完成）
        if count > 2:
            logger.warning(f"并行AI数量 {count} 超过限制，自动降级到2")
            count = 2
        
        container = QWidget()
        
        # 根据数量选择布局
        if count == 1:
            # 单列布局
            layout = QVBoxLayout(container)
        else:  # count == 2
            # 横向2个
            layout = QHBoxLayout(container)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建响应面板列表
        self.response_panels = []
        
        # 获取已配置的AI列表
        configured_ais = self._get_configured_ais()
        
        # 简化逻辑：只处理1-2个面板
        for i in range(count):
            # 根据是否传入 action_layout 决定 AI 切换器的位置
            # action_layout 不为 None：单AI模式，第一个面板的 AI 切换器放在 action_layout
            # action_layout 为 None：多AI模式，所有面板的 AI 切换器都在自己的 header
            if action_layout is not None:
                # 单AI模式：第一个面板不显示header，AI切换器将添加到action_layout
                show_ai_switcher_in_panel = (i > 0)
            else:
                # 多AI模式：所有面板都显示header中的AI切换器
                show_ai_switcher_in_panel = True
            
            panel = ResponsePanel(i, self, self.api, self.i18n, show_ai_switcher=show_ai_switcher_in_panel)
            panel.ai_changed.connect(self._on_panel_ai_changed)
            self._setup_panel_handler(panel)
            self.response_panels.append(panel)
            layout.addWidget(panel)
        
        # 初始化所有面板的AI切换器，并设置默认选择
        self._update_all_panel_ai_switchers()
        self._set_default_ai_selections()
        
        # 如果有 action_layout（单AI模式），将第一个面板的 AI 切换器添加到操作区域
        if action_layout and self.response_panels:
            first_panel = self.response_panels[0]
            if hasattr(first_panel, 'ai_switcher'):
                # 在 action_layout 的最左侧插入 AI 切换器
                action_layout.insertWidget(0, first_panel.ai_switcher)
        
        return container
    
    def _get_configured_ais(self):
        """获取已配置的AI列表
        
        Returns:
            list: [(ai_id, display_name), ...]
        """
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        
        configured_ais = []
        for ai_id, config in models_config.items():
            # 实际检查配置是否有效，而不仅仅依赖 is_configured 标志
            # 因为 is_configured 可能没有被正确更新
            
            # 检查是否有模型名称
            has_model = bool(config.get('model', '').strip())
            if not has_model:
                continue
            
            # 检查是否有API Key（Ollama除外，它是本地服务）
            if ai_id == 'ollama':
                # Ollama特殊处理：需要有api_base_url和model
                has_valid_config = bool(config.get('api_base_url', '').strip())
                if not has_valid_config:
                    continue
            else:
                # 其他AI必须有token
                token_field = 'auth_token' if ai_id == 'grok' else 'api_key'
                has_token = bool(config.get(token_field, '').strip())
                if not has_token:
                    continue
            
            display_name = config.get('display_name', ai_id)
            model_name = config.get('model', 'unknown')
            full_display = f"{display_name} - {model_name}"
            configured_ais.append((ai_id, full_display))
        
        return configured_ais
    
    def _update_all_panel_ai_switchers(self):
        """更新所有面板的AI切换器（实现互斥逻辑）"""
        if not hasattr(self, 'response_panels') or not self.response_panels:
            return
        
        # 获取已配置的AI列表
        configured_ais = self._get_configured_ais()
        
        # 获取当前并行AI数量
        prefs = get_prefs()
        parallel_ai_count = prefs.get('parallel_ai_count', 1)
        
        # 如果是单面板模式，不应用互斥逻辑
        if parallel_ai_count == 1:
            # 单面板模式：所有AI都可用
            for i, panel in enumerate(self.response_panels):
                if i < parallel_ai_count:
                    panel.populate_ai_switcher(configured_ais, set())
            return
        
        # 多面板模式：应用互斥逻辑
        # 收集已被使用的AI（只收集可见面板的）
        used_ais = set()
        for i, panel in enumerate(self.response_panels):
            # 只收集可见面板（根据 parallel_ai_count）的 AI 使用情况
            if i < parallel_ai_count:
                ai_id = panel.get_selected_ai()
                if ai_id:
                    used_ais.add(ai_id)
        
        # 更新每个面板
        for i, panel in enumerate(self.response_panels):
            # 只更新可见面板
            if i < parallel_ai_count:
                current_ai = panel.get_selected_ai()
                # 排除其他面板使用的AI（但保留当前面板自己选中的）
                other_used_ais = used_ais - {current_ai} if current_ai else used_ais
                panel.populate_ai_switcher(configured_ais, other_used_ais)
    
    def _setup_panel_handler(self, panel):
        """为面板设置ResponseHandler
        
        Args:
            panel: ResponsePanel实例
        """
        from calibre_plugins.ask_ai_plugin.response_handler import ResponseHandler
        from calibre_plugins.ask_ai_plugin.api import APIClient
        
        # 为每个面板创建独立的APIClient实例
        # 这样可以避免多面板并发时的模型切换冲突
        panel_api = APIClient()
        
        # 创建独立的ResponseHandler实例
        handler = ResponseHandler(self)
        
        # 设置handler，使用面板独立的API实例
        handler.setup(
            response_area=panel.response_area,
            send_button=self.send_button,
            i18n=self.i18n,
            api=panel_api,  # 使用独立的API实例
            input_area=self.input_area,
            stop_button=self.stop_button
        )
        
        # 将handler和api关联到面板
        panel.setup_response_handler(handler)
        panel.api = panel_api  # 更新面板的API引用
        
        # 连接面板的请求完成信号
        panel.request_finished.connect(self._on_panel_request_finished)
        
        logger.info(f"已为面板 {panel.panel_index} 设置独立的ResponseHandler和APIClient")
    
    def _on_panel_request_finished(self, panel_index):
        """面板请求完成事件处理
        
        Args:
            panel_index: 完成的面板索引
        """
        logger.info(f"面板 {panel_index} 请求完成")
        
        # 检查是否所有面板都已完成
        # 这里简化处理：任何一个面板完成都不改变按钮状态
        # 实际上应该等所有面板都完成，但这需要更复杂的状态管理
        # 暂时保持按钮状态不变，让用户手动点击停止按钮来恢复
    
    def _set_default_ai_selections(self):
        """为每个面板设置默认的AI选择
        
        规则：
        1. 从配置中读取上次的选择（记忆功能）
        2. 如果没有记忆，按顺序分配不同的AI
        3. 如果AI数量不足，超出的面板留空
        """
        prefs = get_prefs()
        
        # 读取上次的AI选择记忆
        saved_selections = prefs.get('panel_ai_selections', {}) or {}
        
        # 获取已配置的AI列表
        configured_ais = self._get_configured_ais()
        
        if not configured_ais:
            logger.warning("没有已配置的AI，无法设置默认选择")
            return
        
        # 读取当前配置中的默认AI
        parallel_ai_count = prefs.get('parallel_ai_count', 1)
        default_ai = prefs.get('selected_model', 'grok')
        
        # 为每个面板设置默认AI
        for i, panel in enumerate(self.response_panels):
            panel_key = f"panel_{i}"

            # 始终优先：第一个面板使用当前配置中的默认AI
            # 说明：
            # - 用户在 Config 里切换默认 AI 的意图应覆盖历史记忆（panel_ai_selections）
            # - 否则会出现“Config 已改默认 AI，但 Ask 仍使用上次记忆”的体验不一致
            if i == 0:
                if any(ai_id == default_ai for ai_id, _ in configured_ais):
                    index = panel.ai_switcher.findData(default_ai)
                    if index >= 0:
                        panel.ai_switcher.setCurrentIndex(index)
                        saved_selections[panel_key] = default_ai
                        logger.info(f"面板 {i} 使用配置中的默认AI: {default_ai}")
                        continue
                # 如果默认AI不在已配置列表中，则继续走通用逻辑
            
            # 1. 优先使用记忆的选择
            if panel_key in saved_selections:
                saved_ai_id = saved_selections[panel_key]
                # 检查这个AI是否还存在且可用
                if any(ai_id == saved_ai_id for ai_id, _ in configured_ais):
                    index = panel.ai_switcher.findData(saved_ai_id)
                    if index >= 0:
                        panel.ai_switcher.setCurrentIndex(index)
                        logger.info(f"面板 {i} 恢复上次选择: {saved_ai_id}")
                        continue
            
            # 2. 如果没有记忆或记忆的AI不可用，按顺序分配
            if i < len(configured_ais):
                ai_id, _ = configured_ais[i]
                index = panel.ai_switcher.findData(ai_id)
                if index >= 0:
                    panel.ai_switcher.setCurrentIndex(index)
                    saved_selections[panel_key] = ai_id
                    logger.info(f"面板 {i} 默认选择: {ai_id}")
            else:
                # 3. AI数量不足，留空
                panel.ai_switcher.setCurrentIndex(-1)
                saved_selections.pop(panel_key, None)
                logger.info(f"面板 {i} 留空（AI数量不足）")
        
        # 将更新后的面板选择记忆回写到配置中
        prefs['panel_ai_selections'] = saved_selections

        # 更新所有面板的AI切换器（实现互斥）
        self._update_all_panel_ai_switchers()
    
    def _check_default_ai_mismatch(self):
        """检查配置中的默认 AI 是否与当前选中的 AI 一致
        
        如果不一致，弹窗询问用户是否切换到默认 AI
        
        注意：只在 Parallel AI Count 为 1 时才检查，为 2 时跳过
        """
        from PyQt5.QtWidgets import QMessageBox
        from PyQt5.QtCore import QTimer
        
        prefs = get_prefs()
        
        # 获取并行AI数量
        parallel_ai_count = prefs.get('parallel_ai_count', 1)
        
        # 如果是并行模式（2个AI），跳过检查
        # 因为并行模式下，用户已经在配置中明确选择了要使用的AI
        if parallel_ai_count == 2:
            logger.debug("并行AI模式（2个AI），跳过默认AI检查")
            return
        
        default_ai = prefs.get('selected_model', 'grok')
        
        # 获取第一个面板当前选中的 AI
        if not self.response_panels:
            return
        
        first_panel = self.response_panels[0]
        current_ai_id = first_panel.ai_switcher.currentData()
        
        # 如果当前 AI 是 None（未选择），不需要提示，直接返回
        if current_ai_id is None:
            logger.debug("当前未选择 AI，跳过默认 AI 检查")
            return
        
        # 如果一致，也需要确保 API 使用的是面板选中的 AI（而不是配置中的默认 AI）
        # 因为用户可能之前选择了"否"，导致面板 AI 与配置不一致
        if current_ai_id == default_ai:
            logger.debug(f"当前 AI ({current_ai_id}) 与默认 AI ({default_ai}) 一致")
            # 仍然需要切换 API 到面板选中的 AI，确保一致性
            self._switch_api_to_panel_ai(current_ai_id)
            return
        
        # 获取 AI 显示名称
        from .models.base import DEFAULT_MODELS, AIProvider
        from .api import APIClient
        
        default_ai_provider = APIClient._MODEL_TO_PROVIDER.get(default_ai)
        current_ai_provider = APIClient._MODEL_TO_PROVIDER.get(current_ai_id)
        
        default_ai_name = DEFAULT_MODELS.get(default_ai_provider).display_name if default_ai_provider else default_ai
        # 处理 None 的情况，使用 i18n
        if current_ai_id is None:
            current_ai_name = self.i18n.get('select_ai', '-- Select AI --')
        else:
            current_ai_name = DEFAULT_MODELS.get(current_ai_provider).display_name if current_ai_provider else current_ai_id
        
        logger.info(f"检测到 AI 不一致 - 当前: {current_ai_name} ({current_ai_id}), 默认: {default_ai_name} ({default_ai})")
        
        # 使用 QTimer 延迟弹窗，避免在初始化过程中阻塞
        def show_dialog():
            reply = QMessageBox.question(
                self,
                self.i18n.get('default_ai_mismatch_title', '默认 AI 已更改'),
                self.i18n.get('default_ai_mismatch_message', 
                    '检测到配置中的默认 AI 已更改为 "{default_ai}"，\n'
                    '但当前对话使用的是 "{current_ai}"。\n\n'
                    '是否切换到新的默认 AI？').format(
                        default_ai=default_ai_name,
                        current_ai=current_ai_name
                    ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # 切换到默认 AI
                logger.info(f"用户选择切换到默认 AI: {default_ai}")
                
                # 先重新更新面板的AI切换器，确保所有AI都可用
                logger.info(f"重新更新面板AI切换器，确保 {default_ai} 可用")
                self._update_all_panel_ai_switchers()
                
                # 更新第一个面板的 AI 选择
                index = first_panel.ai_switcher.findData(default_ai)
                logger.info(f"在面板 0 的AI切换器中查找 {default_ai}，index={index}")
                
                # 调试：打印面板中所有可用的AI
                available_ais = []
                for i in range(first_panel.ai_switcher.count()):
                    ai_id = first_panel.ai_switcher.itemData(i)
                    ai_text = first_panel.ai_switcher.itemText(i)
                    available_ais.append(f"{ai_text}({ai_id})")
                logger.info(f"面板 0 当前可用的AI: {', '.join(available_ais)}")
                
                if index >= 0:
                    first_panel.ai_switcher.setCurrentIndex(index)
                    
                    # 重新加载 API 模型
                    self.api.reload_model()
                    
                    # 更新窗口标题
                    self._update_window_title()
                    
                    logger.info(f"已切换到默认 AI: {default_ai_name}")
                else:
                    logger.warning(f"未找到默认 AI: {default_ai}")
            else:
                # 用户选择继续使用当前 AI
                logger.info(f"用户选择继续使用当前 AI: {current_ai_name} ({current_ai_id})")
                
                # 强制 API 使用当前面板选中的 AI，而不是配置中的默认 AI
                self._switch_api_to_panel_ai(current_ai_id)
        
        # 延迟 100ms 后显示对话框
        QTimer.singleShot(100, show_dialog)
        
        # 初始化完成，允许弹出确认对话框
        for panel in self.response_panels:
            panel._is_initializing = False
    
    def _switch_api_to_panel_ai(self, ai_id: str):
        """强制 API 切换到指定的 AI
        
        当用户选择不切换到默认 AI 时，需要确保 API 使用面板选中的 AI
        
        Args:
            ai_id: AI 模型 ID（如 'openrouter', 'gemini' 等）
        """
        try:
            # 使用 API 的内部方法切换模型
            self.api._switch_to_model(ai_id)
            logger.info(f"API 已切换到面板选中的 AI: {ai_id}")
            
            # 更新窗口标题
            self._update_window_title()
        except Exception as e:
            logger.error(f"切换 API 到面板 AI 失败: {str(e)}")
    
    def _save_panel_ai_selections(self):
        """保存所有面板的AI选择到配置"""
        prefs = get_prefs()
        
        selections = {}
        for i, panel in enumerate(self.response_panels):
            ai_id = panel.get_selected_ai()
            if ai_id:
                selections[f"panel_{i}"] = ai_id
        
        prefs['panel_ai_selections'] = selections
        logger.info(f"已保存面板AI选择: {selections}")
    
    def _on_panel_ai_changed(self, panel_index, new_ai_id):
        """面板AI切换事件处理
        
        Args:
            panel_index: 面板索引
            new_ai_id: 新选中的AI ID
        """
        # 更新对应面板的API对象（修复模型信息显示错误）
        if panel_index < len(self.response_panels) and new_ai_id:
            panel = self.response_panels[panel_index]
            # 切换面板的API到选中的AI
            panel.api._switch_to_model(new_ai_id)
            logger.info(f"[面板AI切换] 面板{panel_index}: {new_ai_id}")
        
        # 如果是第一个面板切换 AI，同步更新 API 使用的模型
        # 这样随机问题和发送请求都会使用面板选中的 AI
        if panel_index == 0 and new_ai_id:
            self._switch_api_to_panel_ai(new_ai_id)
        
        # 更新所有面板的AI切换器（实现互斥）
        self._update_all_panel_ai_switchers()
        
        # 保存选择到配置
        self._save_panel_ai_selections()
    
    def setup_ui(self):
        # 确保模型已经加载
        self.api.reload_model()
        
        # 获取当前使用的模型显示名称
        model_display_name = self.api.model_display_name
        
        # 更新窗口标题
        self._update_window_title()
        
        # 获取并行AI数量配置
        prefs = get_prefs()
        self.parallel_ai_count = prefs.get('parallel_ai_count', 1)
        
        # 限制为1-2个AI（3-4功能暂未完成）
        if self.parallel_ai_count > 2:
            logger.warning(f"并行AI数量 {self.parallel_ai_count} 超过限制，自动降级到2")
            self.parallel_ai_count = 2
            prefs['parallel_ai_count'] = 2
        
        # 根据并行AI数量动态设置最小宽度和高度（降低最小高度以适应小屏幕）
        min_widths = {
            1: 600,   # 单个：保持现有
            2: 1000,  # 2个：每个500px
        }
        min_heights = {
            1: 500,   # 单个：降低到500px以适应笔记本
            2: 500,   # 2个横向：同样高度
        }
        self.setMinimumWidth(min_widths.get(self.parallel_ai_count, 600))
        self.setMinimumHeight(min_heights.get(self.parallel_ai_count, 500))
        
        # 创建主布局（用于包含滚动区域）
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # 创建滚动区域
        from PyQt5.QtWidgets import QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)  # 手动控制每个元素的间距
        layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM)
        scroll_content.setLayout(layout)
        
        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)
        
        # 创建顶部栏：标题 + 书籍信息
        top_bar = QHBoxLayout()
        top_bar.setSpacing(SPACING_SMALL)
        
        # 左侧：对话标题
        title_label = QLabel(self.i18n['menu_title'])
        title_label.setStyleSheet(f"font-weight: bold; font-size: {FONT_SIZE_LARGE}pt;")
        top_bar.addWidget(title_label)
        
        # 书籍信息标签（仅在多书模式下显示）
        if self.is_multi_book:
            book_count = len(self.books_info)
            books_info_text = f"({book_count}{self.i18n.get('books_unit', '本书')})"
            self.books_info_label = QLabel(books_info_text)
            self.books_info_label.setStyleSheet("color: palette(dark); font-size: 0.9em; margin-left: 8px;")
            top_bar.addWidget(self.books_info_label)
        
        top_bar.addStretch()
        
        layout.addLayout(top_bar)
        
        # 区域1：输入区域（使用紧凑间距）
        from .ui_constants import SPACING_ASK_COMPACT, SPACING_ASK_SECTION
        
        layout.addSpacing(SPACING_ASK_COMPACT)
        
        # 创建可折叠的书籍元数据树形组件
        metadata_widget = self._create_metadata_widget()
        layout.addWidget(metadata_widget)
        
        layout.addSpacing(SPACING_ASK_COMPACT)
        
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
        
        layout.addSpacing(SPACING_ASK_COMPACT)
        
        # 创建操作区域
        action_layout = QHBoxLayout()
        action_layout.setSpacing(SPACING_SMALL)
        
        # 左侧：AI 切换器（单AI模式）或历史记录按钮（多AI模式）
        # 注意：具体内容将在后续根据 parallel_ai_count 添加
        
        # 添加弹性空间，将右侧按钮推到右边
        action_layout.addStretch()
        
        # 右侧：随机问题按钮
        self.suggest_button = QPushButton(self.i18n['suggest_button'])
        self.suggest_button.clicked.connect(self.generate_suggestion)
        apply_button_style(self.suggest_button, min_width=120)  # 设置固定宽度，与加载状态一致
        self.suggest_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.suggest_button.setDefault(True)  # 初始设置为默认按钮（高光状态）
        
        # 创建随机问题动作和快捷键
        self.suggest_action = QAction(self.i18n['suggest_button'], self)
        self.suggest_action.setShortcutContext(Qt.WindowShortcut)
        self.suggest_action.triggered.connect(self.generate_suggestion)
        self.addAction(self.suggest_action)
        
        action_layout.addWidget(self.suggest_button)
        
        # 右侧：停止按钮（初始隐藏）
        self.stop_button = QPushButton(self.i18n.get('stop_button', 'Stop'))
        self.stop_button.clicked.connect(self.stop_request)
        apply_button_style(self.stop_button, min_width=120)  # 使用标准样式和固定宽度
        self.stop_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stop_button.setVisible(False)  # 初始隐藏
        action_layout.addWidget(self.stop_button)
        
        # 右侧：发送按钮
        self.send_button = QPushButton(self.i18n['send_button'])
        self.send_button.clicked.connect(self.send_question)
        apply_button_style(self.send_button, min_width=120)  # 设置固定宽度，与加载状态一致
        self.send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.send_button.setDefault(False)  # 初始不是默认按钮

        # 创建发送动作和快捷键
        self.send_action = QAction(self.i18n['send_button'], self)
        self.send_action.setShortcutContext(Qt.WindowShortcut)
        self.send_action.triggered.connect(self.send_question)
        self.addAction(self.send_action)

        action_layout.addWidget(self.send_button)
        
        # 根据并行AI数量决定布局
        if self.parallel_ai_count == 1:
            # 单AI模式：历史记录按钮在响应区域上方，AI切换器在action_layout
            layout.addLayout(action_layout)
            
            # 区域1和区域2之间使用较大间距
            layout.addSpacing(SPACING_ASK_SECTION)
            
            # 区域2：响应区域（使用紧凑间距）
            
            # 创建历史记录信息栏（在响应面板之前）
            history_info_layout = QHBoxLayout()
            history_info_layout.setSpacing(SPACING_SMALL)
            history_info_layout.setContentsMargins(0, 0, 0, 0)
            
            # 左侧：历史记录按钮
            history_button = self._create_history_switcher()
            history_info_layout.addWidget(history_button)
            
            # 右侧：历史信息标签（初始隐藏）
            self.history_info_label = QLabel()
            self.history_info_label.setStyleSheet("""
                QLabel {
                    color: palette(dark);
                    font-size: 0.9em;
                    padding: 5px;
                }
            """)
            self.history_info_label.setVisible(False)
            history_info_layout.addWidget(self.history_info_label)
            history_info_layout.addStretch()
            
            layout.addLayout(history_info_layout)
            
            layout.addSpacing(SPACING_ASK_COMPACT)
            
            # 创建响应面板容器（AI切换器在action_layout）
            response_container = self._create_response_container(self.parallel_ai_count, action_layout)
        else:
            # 多AI模式：历史记录按钮在action_layout，AI切换器在各自面板header
            # 在action_layout左侧添加历史记录按钮
            history_button = self._create_history_switcher()
            action_layout.insertWidget(0, history_button)
            
            layout.addLayout(action_layout)
            
            # 区域1和区域2之间使用较大间距
            layout.addSpacing(SPACING_ASK_SECTION)
            
            # 创建历史信息标签（放在响应面板上方，但不创建单独的layout）
            self.history_info_label = QLabel()
            self.history_info_label.setStyleSheet("""
                QLabel {
                    color: palette(dark);
                    font-size: 0.9em;
                    padding: 5px;
                }
            """)
            self.history_info_label.setVisible(False)
            layout.addWidget(self.history_info_label)
            
            layout.addSpacing(SPACING_ASK_COMPACT)
            
            # 创建响应面板容器（AI切换器在各自面板header）
            response_container = self._create_response_container(self.parallel_ai_count, None)
        layout.addWidget(response_container)
        
        # 为向后兼容，保留 response_area 和 response_handler 引用（指向第一个面板）
        if self.response_panels:
            self.response_area = self.response_panels[0].response_area
            self.response_handler = self.response_panels[0].response_handler
    
    def _update_button_focus(self):
        """根据输入框内容动态切换按钮的高光状态"""
        has_text = bool(self.input_area.toPlainText().strip())
        
        # 如果用户修改了输入框内容，清除随机问题相关的临时状态
        if hasattr(self, '_pending_random_question'):
            current_text = self.input_area.toPlainText()
            if current_text != self._pending_random_question:
                # 用户修改了随机问题，清除临时缓存和标记
                if self._pending_random_question is not None:
                    logger.debug("用户修改了输入框内容，清除随机问题临时状态")
                    self._pending_random_question = None
                    if hasattr(self, '_is_generating_random_question'):
                        self._is_generating_random_question = False
        
        if has_text:
            # 输入框有内容：发送按钮高光，随机问题按钮取消高光
            self.send_button.setDefault(True)
            self.suggest_button.setDefault(False)
        else:
            # 输入框为空：随机问题按钮高光，发送按钮取消高光
            self.suggest_button.setDefault(True)
            self.send_button.setDefault(False)
    
    def _has_history_data(self):
        """检查当前UID是否有历史记录（有AI回答）
        
        Returns:
            bool: 如果有历史记录且包含AI回答返回True，否则返回False
        """
        if not hasattr(self, 'response_handler') or not hasattr(self.response_handler, 'history_manager'):
            return False
        
        history = self.response_handler.history_manager.get_history_by_uid(self.current_uid)
        if not history:
            return False
        
        # 检查是否有AI回答
        answers = history.get('answers', {})
        if not answers:
            return False
        
        # 检查是否有任何非空的回答
        for ai_id, answer_data in answers.items():
            if isinstance(answer_data, dict):
                answer = answer_data.get('answer', '')
            else:
                answer = answer_data
            if answer and answer.strip():
                return True
        
        return False
    
    def generate_suggestion(self):
        """生成随机问题（只发送到第一个AI面板）"""
        # 检查是否有有效的AI配置
        if not self.api or not self.api._ai_model:
            logger.warning("未配置有效的AI服务，显示提示")
            self._show_ai_service_required_dialog()
            return
        
        # 随机问题只使用第一个AI（不并行），并显式使用其当前选中的模型
        model_id = None
        if hasattr(self, 'response_panels') and self.response_panels:
            # 确保第一个面板有选中的AI
            first_panel = self.response_panels[0]
            model_id = first_panel.get_selected_ai()
            if not model_id:
                logger.warning("第一个面板没有选中AI，无法生成随机问题")
                self._show_ai_service_required_dialog()
                return
        
        # 检查是否有历史数据
        if self._has_history_data():
            logger.info("检测到当前有历史记录，点击随机问题将创建新会话")
            # 创建新会话
            self._on_new_conversation()
        
        # 标记这是一个随机问题请求
        self._is_generating_random_question = True
        
        # 使用选中的模型生成随机问题
        self.suggestion_handler.generate(self.book_info, model_id=model_id)

    def _show_ai_service_required_dialog(self):
        """显示需要AI服务的提示对话框"""
        from PyQt5.QtWidgets import QMessageBox
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.i18n.get('auth_token_required_title', 'AI Service Required'))
        msg_box.setText(self.i18n.get('auth_token_required_message', 
            'Please configure a valid AI service in Plugin Configuration.'))
        msg_box.setIcon(QMessageBox.Information)
        
        # 只添加确认按钮（避免在Ask对话框打开时再打开配置对话框导致错误）
        msg_box.addButton(
            self.i18n.get('confirm', 'OK'),
            QMessageBox.AcceptRole
        )
        
        msg_box.exec_()
    
    def _check_auth_token(self):
        """检查当前选择的模型是否设置了API Key"""
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        
        prefs = get_prefs()
        selected_model = prefs.get('selected_model', 'grok')
        models_config = prefs.get('models', {})
        model_config = models_config.get(selected_model, {})
        
        # 获取token字段名，不同模型可能使用不同的字段名
        token_field = 'auth_token' if selected_model == 'grok' else 'api_key'
        token = model_config.get(token_field, '')
        
        # 如果是Ollama模型，不强制要求API Key（本地服务）
        if selected_model == 'ollama':
            return True
            
        if not token or not token.strip():
            # 显示友好的提示对话框
            self._show_ai_service_required_dialog()
            
            # 直接返回False，表示验证失败
            return False
        
        return True
    
    def send_question(self):
        """发送问题"""
        import logging
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        logger = logging.getLogger(__name__)
        
        # 检查是否是随机问题请求
        is_random_question = hasattr(self, '_is_generating_random_question') and self._is_generating_random_question
        
        # 如果是随机问题，已经在generate_suggestion中创建了新会话，这里不需要再创建
        # 如果不是随机问题，检查当前UID是否已有历史记录
        if not is_random_question:
            if hasattr(self, 'response_handler') and hasattr(self.response_handler, 'history_manager'):
                if self.current_uid in self.response_handler.history_manager.histories:
                    old_uid = self.current_uid
                    self.current_uid = self._generate_uid()
                    logger.info(f"检测到已有历史记录，生成新UID: {old_uid} -> {self.current_uid}")
        else:
            logger.info("随机问题请求，使用已创建的新会话UID")
            # 清除临时存储中的待发送随机问题（因为用户已经点击发送）
            book_ids = tuple(sorted([book.id for book in self.books_info]))
            prefs = get_prefs()
            pending_questions = prefs.get('pending_random_questions', {})
            if str(book_ids) in pending_questions:
                del pending_questions[str(book_ids)]
                prefs['pending_random_questions'] = pending_questions
                logger.info(f"已清除临时存储中的待发送随机问题: book_ids={book_ids}")
            
            # 重置标记和临时缓存
            self._is_generating_random_question = False
            self._pending_random_question = None
        
        # 检查 token 是否有效
        if not self._check_auth_token():
            logger.error("Token 验证失败")
            return
            
        try:
            # 获取输入的问题
            question = self.input_area.toPlainText()
            # 标准化换行符并确保使用 UTF-8 编码
            question = question.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8')
        
            # 根据模式构建提示词
            if self.is_multi_book:
                # 多书模式：使用多书提示词
                logger.info("使用多书模式构建提示词...")
                prompt = self._build_multi_book_prompt(question)
            else:
                # 单书模式：使用原有逻辑
                logger.info("使用单书模式构建提示词...")
                
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
                
                # 获取配置的模板
                prefs = get_prefs()
                template = prefs.get('template', '')
                
                # 如果模板为空，使用默认模板
                if not template:
                    template = "User query: {query}\nBook title: {title}\nAuthor: {author}\nPublisher: {publisher}\nPublication year: {pubyear}\nLanguage: {language}\nSeries: {series}"
                
                logger.info(f"使用的模板: {template}")
                
                # 检查并替换模板中的变量名，确保用户输入能够正确插入
                if '{query}' not in template and '{question}' in template:
                    logger.info("检测到旧版模板变量 {question}，自动替换为 {query}")
                    template = template.replace('{question}', '{query}')
                
                # 格式化提示词
                try:
                    prompt = template.format(**template_vars)
                except KeyError as e:
                    self.response_handler.handle_error(self.i18n.get('template_error', 'Template error: {error}').format(error=str(e)))
                    return
            
            logger.info(f"最终提示词长度: {len(prompt)}")
            
        except Exception as e:
            self.response_handler.handle_error(f"{self.i18n.get('error_preparing_request', 'Error preparing request')}: {str(e)}")
            return
        
        # 如果提示词过长，可能会导致超时（多书模式允许更长）
        max_length = 4000 if self.is_multi_book else 2000
        if len(prompt) > max_length:
            self.response_handler.handle_error(self.i18n.get('question_too_long', 'Question is too long, please simplify and try again'))
            return
        
        # 隐藏历史信息标签（发送新问题时）
        if hasattr(self, 'history_info_label'):
            old_text = self.history_info_label.text()
            logger.info(f"[历史信息标签] 发送新问题，隐藏标签。旧内容: {old_text}")
            self.history_info_label.setVisible(False)
        
        # 禁用发送按钮并显示加载状态，显示停止按钮
        self.send_button.setVisible(False)
        self.stop_button.setVisible(True)
        
        # 开始异步请求 - 并行发送到所有面板
        parallel_start_time = time.time()
        try:
            if hasattr(self, 'response_panels') and self.response_panels:
                # 多面板模式：并行发送到所有面板
                for panel in self.response_panels:
                    # 设置当前问题（用于按钮状态判断）
                    panel.set_current_question(question)
                    
                    selected_ai = panel.get_selected_ai()
                    if selected_ai:
                        request_time = time.time()
                        elapsed_ms = (request_time - parallel_start_time) * 1000
                        panel.send_request(prompt, model_id=selected_ai)
                    else:
                        logger.warning(f"面板 {panel.panel_index} 没有选中AI，跳过")
                total_time = (time.time() - parallel_start_time) * 1000
                logger.info(f"所有请求已发出，总耗时: {total_time:.2f}ms，面板数: {len(self.response_panels)}")
            else:
                # 向后兼容：单面板模式
                self.response_handler.start_async_request(prompt)
                logger.info("异步请求已启动（单面板模式）")
        except Exception as e:
            logger.error(f"启动异步请求时出错: {str(e)}")
            if hasattr(self, 'response_handler'):
                self.response_handler.handle_error(f"启动请求时出错: {str(e)}")
            # 恢复按钮状态
            self.send_button.setVisible(True)
            self.stop_button.setVisible(False)
    
    def stop_request(self):
        """停止当前请求（包括发送请求和随机问题生成）"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("用户请求停止当前请求")
        
        # 检查是否是随机问题生成请求
        if hasattr(self, 'suggestion_handler') and self.suggestion_handler:
            # 检查是否有正在进行的随机问题生成
            if hasattr(self.suggestion_handler, '_worker') and self.suggestion_handler._worker and not self.suggestion_handler._worker.is_finished():
                logger.info("停止随机问题生成")
                self.suggestion_handler.stop()
                return
        
        # 停止所有面板的请求
        if hasattr(self, 'response_panels') and self.response_panels:
            for panel in self.response_panels:
                if hasattr(panel, 'response_handler') and panel.response_handler:
                    panel.response_handler.cancel_request()
            logger.info(f"已停止 {len(self.response_panels)} 个面板的请求")
        elif hasattr(self, 'response_handler'):
            # 向后兼容：单面板模式
            self.response_handler.cancel_request()
        
        # 恢复按钮状态
        self.send_button.setVisible(True)
        self.stop_button.setVisible(False)
        
        logger.info("请求已停止，按钮状态已恢复")
    
    def eventFilter(self, obj, event):
        """事件过滤器，用于处理快捷键"""
        if event.type() == event.KeyPress:
            # 处理单独的 Enter 键：根据输入框内容决定触发哪个按钮
            # 注意：Ctrl/Cmd+Enter 由 QAction shortcut 处理，以保证在对话框任意控件聚焦时均可触发。
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 检查是否有修饰键（Shift等），如果有则不处理（允许换行）
                if event.modifiers() & (Qt.ShiftModifier | Qt.AltModifier):
                    return False
                
                has_text = bool(self.input_area.toPlainText().strip())
                if has_text:
                    # 输入框有内容：触发发送
                    self.send_question()
                else:
                    # 输入框为空：触发随机问题
                    self.generate_suggestion()
                return True
        return False

    def copy_response(self):
        """复制响应内容到剪贴板"""
        clipboard = QApplication.clipboard()
        response_text = self.response_area.toPlainText()
        if response_text.strip():
            clipboard.setText(response_text)
            self._show_copy_tooltip(self.copy_response_btn, self.i18n.get('copied', 'Copied!'))
            
    def copy_question_response(self):
        """复制问题和响应内容到剪贴板"""
        clipboard = QApplication.clipboard()
        question = self.input_area.toPlainText().strip()
        response = self.response_area.toPlainText().strip()
        
        if not question and not response:
            return
            
        # 组合问题和答案，用分隔线隔开
        text = f"{question}\n\n----\n\n{response}" if question and response else (question or response)
        clipboard.setText(text)
        self._show_copy_tooltip(self.copy_qr_btn, self.i18n.get('copied', 'Copied!'))
    
    def export_to_pdf(self):
        """导出当前问答为PDF文件"""
        import logging
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from datetime import datetime
        
        logger = logging.getLogger(__name__)
        
        # 获取问题和回答
        question = self.input_area.toPlainText().strip()
        response = self.response_area.toPlainText().strip()
        
        if not question and not response:
            logger.warning("没有内容可导出")
            return
        
        # 生成默认文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"ask_ai_qa_{timestamp}.pdf"
        
        # 打开文件保存对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get('export_pdf_dialog_title', 'Export to PDF'),
            default_filename,
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            logger.debug("用户取消了PDF导出")
            return
        
        try:
            # 使用最简单的方式：直接使用 response_area 的打印功能
            from PyQt5.QtPrintSupport import QPrinter
            
            printer = QPrinter()
            printer.setOutputFileName(file_path)
            
            # 构建书籍元数据信息
            separator = "=" * 40  # 缩短分隔线从60到40字符
            metadata_lines = []
            if hasattr(self, 'book_metadata') and self.book_metadata:
                metadata_lines.append(separator)
                metadata_lines.append(self.i18n.get('pdf_book_metadata', 'BOOK METADATA'))
                metadata_lines.append(separator)
                
                if self.book_metadata.get('title'):
                    title_label = self.i18n.get('metadata_title', 'Title')
                    metadata_lines.append(f"{title_label}: {self.book_metadata['title']}")
                
                if self.book_metadata.get('authors'):
                    authors = ', '.join(self.book_metadata['authors']) if isinstance(self.book_metadata['authors'], list) else str(self.book_metadata['authors'])
                    authors_label = self.i18n.get('metadata_authors', 'Authors')
                    metadata_lines.append(f"{authors_label}: {authors}")
                
                if self.book_metadata.get('publisher'):
                    publisher_label = self.i18n.get('metadata_publisher', 'Publisher')
                    metadata_lines.append(f"{publisher_label}: {self.book_metadata['publisher']}")
                
                if self.book_metadata.get('pubdate'):
                    pubdate = str(self.book_metadata['pubdate'])
                    # 只保留年月，去掉详细时间
                    if 'T' in pubdate:
                        pubdate = pubdate.split('T')[0]  # 去掉时间部分
                    if len(pubdate) > 7:
                        pubdate = pubdate[:7]  # 只保留 YYYY-MM
                    pubdate_label = self.i18n.get('metadata_pubyear', 'Publication Date')
                    metadata_lines.append(f"{pubdate_label}: {pubdate}")
                
                if self.book_metadata.get('languages'):
                    languages = ', '.join(self.book_metadata['languages']) if isinstance(self.book_metadata['languages'], list) else str(self.book_metadata['languages'])
                    languages_label = self.i18n.get('metadata_language', 'Languages')
                    metadata_lines.append(f"{languages_label}: {languages}")
                
                metadata_lines.append("")
            
            # 获取当前使用的AI模型信息
            model_info_lines = []
            try:
                if hasattr(self, 'api') and self.api:
                    logger.debug(f"API对象存在: {self.api}")
                    
                    model_info_lines.append("")
                    model_info_lines.append(separator)
                    model_info_lines.append(self.i18n.get('pdf_ai_model_info', 'AI MODEL INFORMATION'))
                    model_info_lines.append(separator)
                    
                    # 使用新的provider_name属性获取提供商名称
                    provider = self.api.provider_name
                    model_name = self.api.model
                    api_url = self.api.api_base
                    
                    provider_label = self.i18n.get('pdf_provider', 'Provider')
                    model_label = self.i18n.get('pdf_model', 'Model')
                    api_url_label = self.i18n.get('pdf_api_base_url', 'API Base URL')
                    
                    model_info_lines.append(f"{provider_label}: {provider}")
                    model_info_lines.append(f"{model_label}: {model_name}")
                    if api_url:
                        model_info_lines.append(f"{api_url_label}: {api_url}")
                else:
                    logger.warning("没有API对象")
                    info_not_available = self.i18n.get('pdf_info_not_available', 'Information not available')
                    model_info_lines.append(f"{self.i18n.get('pdf_provider', 'Provider')}: {info_not_available}")
            except Exception as e:
                logger.error(f"获取模型信息失败: {str(e)}", exc_info=True)
                info_not_available = self.i18n.get('pdf_info_not_available', 'Information not available')
                model_info_lines.append(f"{self.i18n.get('pdf_provider', 'Provider')}: {info_not_available}")
            
            # 组合所有内容
            content_parts = []
            
            # 1. 书籍元数据（最开头）
            if metadata_lines:
                content_parts.append('\n'.join(metadata_lines))
            
            # 2. 问题
            content_parts.append(separator)
            content_parts.append(self.i18n.get('pdf_question', 'QUESTION'))
            content_parts.append(separator)
            content_parts.append(question if question else self.i18n.get('no_question', 'No question'))
            content_parts.append("")
            
            # 3. 回答
            content_parts.append(separator)
            content_parts.append(self.i18n.get('pdf_answer', 'ANSWER'))
            content_parts.append(separator)
            content_parts.append(response if response else self.i18n.get('no_response', 'No response'))
            
            # 4. AI模型信息（最后）
            if model_info_lines:
                content_parts.extend(model_info_lines)
            
            # 5. 生成信息
            content_parts.append("")
            content_parts.append(separator)
            content_parts.append(self.i18n.get('pdf_generated_by', 'GENERATED BY'))
            content_parts.append(separator)
            plugin_label = self.i18n.get('pdf_plugin', 'Plugin')
            github_label = self.i18n.get('pdf_github', 'GitHub')
            software_label = self.i18n.get('pdf_software', 'Software')
            time_label = self.i18n.get('pdf_generated_time', 'Generated Time')
            content_parts.append(f"{plugin_label}: Ask AI Plugin (Calibre Plugin)")
            content_parts.append(f"{github_label}: https://github.com/sheldonrrr/ask_grok")
            content_parts.append(f"{software_label}: Calibre E-book Manager (https://calibre-ebook.com)")
            content_parts.append(f"{time_label}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            content_parts.append(separator)
            
            content = '\n'.join(content_parts)
            
            # 使用 response_area 的文档直接打印
            from PyQt5.QtGui import QTextDocument
            doc = QTextDocument()
            doc.setPlainText(content)
            doc.print(printer)
            
            logger.info(f"PDF导出成功: {file_path}")
            # 显示成功提示
            success_msg = self.i18n.get('pdf_exported', 'PDF Exported!')
            self._show_copy_tooltip(self.export_pdf_btn, success_msg)
            
            # 同时在状态栏显示消息（如果可用）
            try:
                from PyQt5.QtWidgets import QApplication
                if QApplication.instance():
                    main_window = QApplication.instance().activeWindow()
                    if main_window and hasattr(main_window, 'statusBar'):
                        main_window.statusBar().showMessage(f"{success_msg} - {file_path}", 3000)
            except:
                pass
            
        except Exception as e:
            logger.error(f"导出PDF失败: {str(e)}", exc_info=True)
            error_msg = self.i18n.get('export_pdf_error', 'Failed to export PDF: {0}').format(str(e))
            QMessageBox.warning(
                self,
                self.i18n.get('error', 'Error'),
                error_msg
            )
    
    def _show_copy_tooltip(self, button, text):
        """在按钮位置显示复制成功的提示"""
        from PyQt5.QtWidgets import QToolTip
        QToolTip.showText(button.mapToGlobal(button.rect().bottomLeft()), text, button, button.rect(), 2000)
        
    def update_language(self, new_language=None):
        """更新界面语言"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 如果没有指定语言，从配置中获取
        if not new_language:
            from calibre_plugins.ask_ai_plugin.config import get_prefs
            prefs = get_prefs()
            new_language = prefs.get('language', 'en')
        
        logger.debug(f"AskDialog 更新语言为: {new_language}")
        
        # 更新i18n对象
        from .i18n import get_translation
        self.i18n = get_translation(new_language)
        
        # 更新窗口标题
        model_display_name = self.api.model_display_name
        self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.get('title', '')}")
        
        # 更新发送按钮文本
        if hasattr(self, 'send_button'):
            self.send_button.setText(self.i18n.get('send', 'Send'))
        
        # 更新输入区域占位符文本
        if hasattr(self, 'input_area'):
            self.input_area.setPlaceholderText(self.i18n.get('ask_placeholder', 'Ask about this book...'))
        
        # 更新复制按钮文本
        if hasattr(self, 'copy_response_btn'):
            self.copy_response_btn.setToolTip(self.i18n.get('copy_response', 'Copy response'))
        
        if hasattr(self, 'copy_qr_btn'):
            self.copy_qr_btn.setToolTip(self.i18n.get('copy_qr', 'Copy Q&R'))
        
        # 更新随机问题按钮文本
        if hasattr(self, 'random_question_btn'):
            self.random_question_btn.setToolTip(self.i18n.get('random_question', 'Random question'))
        
        logger.debug("AskDialog 界面语言更新完成")
    
    def closeEvent(self, event):
        """处理窗口关闭事件"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 如果有待发送的随机问题，保存到临时存储
        if hasattr(self, '_pending_random_question') and self._pending_random_question:
            # 使用书籍ID作为key保存待发送的随机问题和新会话UID
            book_ids = tuple(sorted([book.id for book in self.books_info]))
            prefs = get_prefs()
            pending_questions = prefs.get('pending_random_questions', {})
            pending_questions[str(book_ids)] = {
                'question': self._pending_random_question,
                'uid': self.current_uid,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            prefs['pending_random_questions'] = pending_questions
            logger.info(f"保存待发送的随机问题到临时存储: book_ids={book_ids}, uid={self.current_uid}")
        
        # 准备关闭，让线程自然结束
        self.response_handler.prepare_close()
        self.suggestion_handler.prepare_close()  # 改用 prepare_close
        event.accept()
