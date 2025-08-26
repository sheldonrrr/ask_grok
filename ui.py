#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

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
from calibre_plugins.ask_grok.config import ConfigDialog, get_prefs
from calibre_plugins.ask_grok.api import APIClient
from .i18n import get_translation, get_suggestion_template
from calibre_plugins.ask_grok.shortcuts_widget import ShortcutsWidget
from calibre_plugins.ask_grok.version import VERSION_DISPLAY
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

def get_suggestion_template_from_ui(lang_code):
    """获取指定语言的随机问题提示词模板"""
    from .i18n import get_suggestion_template
    return get_suggestion_template(lang_code)

class AskGrokPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 根据操作系统设置不同的快捷键
    action_spec = ('Ask Grok', 'images/ask_grok.png', 'Ask Grok about this book', 
                  'Ctrl+L')
    action_shortcut_name = 'Ask Grok'
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
        
        # 快捷键已经在action_spec中设置，这里不需要再设置
        self.ask_action.triggered.connect(self.show_dialog)
        self.menu.addAction(self.ask_action)
        
        # 添加分隔符
        self.menu.addSeparator()

        # 添加配置菜单项
        self.config_action = QAction(self.i18n['config_title'], self)

        # 根据操作系统设置快捷键
        if sys.platform == 'darwin':  # macOS
            shortcut = QKeySequence("Command+K")
        else:
            shortcut = QKeySequence("Ctrl+K")
        self.config_action.setShortcut(shortcut)
        self.config_action.setShortcutContext(Qt.ApplicationShortcut) # 设置为应用程序级别的快捷键
        
        self.config_action.triggered.connect(self.show_configuration)
        self.menu.addAction(self.config_action)
        
        #添加分隔符
        self.menu.addSeparator()

        #添加快捷键菜单项
        self.shortcuts_action = QAction(self.i18n['shortcuts'], self)
        self.shortcuts_action.triggered.connect(self.show_shortcuts)
        self.menu.addAction(self.shortcuts_action)      

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
        
        # 保存对话框实例的引用
        self.ask_dialog = d
        
        # 对话框关闭时清除引用
        d.finished.connect(lambda result: setattr(self, 'ask_dialog', None))
        
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
            self.about_action.setText(self.i18n['about'])
            
        except Exception as e:
            # 发生错误时恢复原始状态
            logger.error(f"更新菜单文本时出错: {str(e)}")
            self.ask_action.setText(original_texts['ask'])
            self.config_action.setText(original_texts['config'])
            self.shortcuts_action.setText(original_texts['shortcuts'])
            self.about_action.setText(original_texts['about'])

class AskGrokConfigWidget(QWidget):
    """配置页面组件"""
    # 定义一个与 ConfigDialog 相同的语言变更信号
    language_changed = pyqtSignal(str)
    
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
        
        # 连接 ConfigDialog 的语言变更信号，并转发出去
        self.config_dialog.language_changed.connect(self.on_language_changed)
    
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
        # 使用系统颜色，确保在亮色和暗色主题下都能正常显示
        self.about_label.setText(f"""
        <div style='text-align: center; max-width: 500px; margin: 0 auto; padding: 20px; display: flex; flex-direction: column; justify-content: center; height: 100%;'>
            <div style='font-size: 24px; font-weight: bold; color: palette(window-text); margin: 10px 0;'>Ask Grok</div>
            <div style='font-size: 14px; color: palette(window-text); margin-bottom: 15px; line-height: 1.4; opacity: 0.9;'>{self.i18n['plugin_desc']}</div>
            <div style='font-size: 13px; color: palette(window-text); margin-bottom: 25px; opacity: 0.7;'>{VERSION_DISPLAY}</div>
            
            <div style='display: flex; flex-direction: column; align-items: center; margin: 15px 0;'>
                <div style='margin: 8px 0;'>
                    <a href='http://simp.ly/publish/FwMSSr' 
                       style='color: palette(link); text-decoration: none; font-size: 14px;'>
                       {self.i18n.get('user_manual', 'User Manual')} ↗
                    </a>
                </div>
                
                <div style='margin: 8px 0;'>
                    <a href='http://simp.ly/publish/xYW5Tr' 
                       style='color: palette(link); text-decoration: none; font-size: 14px;'>
                       {self.i18n.get('about_plugin', 'Why Ask Grok?')} ↗
                    </a>
                </div>
                
                <div style='margin: 8px 0;'>
                    <a href='https://youtu.be/QdeZgkT1fpw' 
                       style='color: palette(link); text-decoration: none; font-size: 14px;'>
                       {self.i18n.get('learn_how_to_use', 'How to Use')} ↗
                    </a>
                </div>
                
                <div style='margin: 8px 0;'>
                    <a href='imessage://sheldonrrr@gmail.com' 
                       style='color: palette(link); text-decoration: none; font-size: 14px;'>
                       {self.i18n.get('email', 'iMessage')}: sheldonrrr@gmail.com
                    </a>
                </div>
            </div>
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
        
        # 连接标签页切换信号
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # 创建General页面
        self.config_widget = AskGrokConfigWidget(self.gui)
        self.tab_widget.addTab(self.config_widget, self.i18n['general_tab'])
        
        # 语言变更信号已在下方连接到config_widget.config_dialog.language_changed

        # 创建快捷键页面
        self.shortcuts_widget = ShortcutsWidget(self)
        self.tab_widget.addTab(self.shortcuts_widget, self.i18n['shortcuts'])

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
        
        # 添加Close按钮（右侧）
        close_button = QPushButton(self.i18n.get('close_button', 'Close'))
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        # 添加右侧间距
        button_layout.addSpacing(10)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 连接配置对话框的信号
        self.config_widget.config_dialog.settings_saved.connect(self.on_settings_saved)
    
        # 连接语言切换信号
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
        self.tab_widget.setTabText(2, self.i18n['about'])
        logger.debug("已更新标签页标题")
        
        # 更新关闭按钮文本
        for button_box in self.findChildren(QDialogButtonBox):
            close_button = button_box.button(QDialogButtonBox.Close)
            if close_button:
                close_button.setText(self.i18n.get('close_button', 'Close'))
                logger.debug("已更新关闭按钮文本")
        
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
        logger.debug(f"通知主界面更新菜单，语言: {new_language}")
        ask_grok_plugin.plugin_instance.update_menu_texts(new_language)
        
        # 更新主对话框的界面语言
        if (hasattr(ask_grok_plugin.plugin_instance, 'ask_dialog') and 
            ask_grok_plugin.plugin_instance.ask_dialog):
            logger.debug(f"更新主对话框的界面语言为: {new_language}")
            # 如果存在update_language方法，直接调用
            if hasattr(ask_grok_plugin.plugin_instance.ask_dialog, 'update_language'):
                ask_grok_plugin.plugin_instance.ask_dialog.update_language(new_language)
            
            # 更新 response_handler 和 suggestion_handler 的 i18n 对象
            if hasattr(ask_grok_plugin.plugin_instance.ask_dialog, 'suggestion_handler'):
                logger.debug("更新对话框组件的i18n对象")
                ask_grok_plugin.plugin_instance.ask_dialog.response_handler.update_i18n(self.i18n)
                ask_grok_plugin.plugin_instance.ask_dialog.suggestion_handler.update_i18n(self.i18n)
    
    def on_settings_saved(self):
        """当设置保存时的处理函数"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 重新加载模型，确保使用最新选择的模型
        from calibre_plugins.ask_grok.api import api
        api.reload_model()
        logger.debug("已重新加载模型")
        
        # 更新已打开的AskDialog实例的模型信息
        try:
            if (hasattr(ask_grok_plugin, 'plugin_instance') and 
                ask_grok_plugin.plugin_instance and 
                hasattr(ask_grok_plugin.plugin_instance, 'ask_dialog') and 
                ask_grok_plugin.plugin_instance.ask_dialog):
                
                logger.debug("正在更新已打开的AskDialog实例的模型信息")
                ask_grok_plugin.plugin_instance.ask_dialog.update_model_info()
                logger.debug("已更新AskDialog实例的模型信息")
        except Exception as e:
            logger.error(f"更新AskDialog实例的模型信息时出错: {str(e)}")
        
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
        # 如果配置页面有未保存的更改，先重置字段
        if hasattr(self, 'config_widget') and hasattr(self.config_widget, 'config_dialog'):
            # 直接调用重置方法
            self.config_widget.config_dialog.reset_to_initial_values()
            # 重置保存按钮状态
            if hasattr(self, 'save_button'):
                self.save_button.setEnabled(False)
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
        
        # 准备书籍元数据用于历史记录
        pubdate = book_info.get('pubdate', '')
        # 处理日期对象，确保它是 YYYY-MM-DD 格式的字符串
        if hasattr(pubdate, 'strftime'):
            pubdate = pubdate.strftime('%Y-%m-%d')
        elif isinstance(pubdate, str) and pubdate:
            # 如果已经是字符串，尝试解析并格式化为 YYYY-MM-DD
            try:
                from calibre.utils.date import parse_date
                pubdate = parse_date(pubdate).strftime('%Y-%m-%d')
            except:
                # 如果解析失败，尝试提取日期部分（格式如 YYYY-MM-DDTHH:MM:SS+HH:MM）
                if 'T' in pubdate:
                    pubdate = pubdate.split('T')[0]
        
        self.book_metadata = {
            'title': book_info.get('title', ''),
            'authors': book_info.get('authors', []),
            'publisher': book_info.get('publisher', ''),
            'pubdate': book_info.get('pubdate', ''),
            'languages': book_info.get('languages', [])
        }
        
        # 初始化处理器
        self.response_handler = ResponseHandler(self)
        # 确保 SuggestionHandler 正确初始化
        self.suggestion_handler = SuggestionHandler(parent=self)
        
        # 连接语言变更信号
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("连接AskDialog到语言变更信号")
        
        # 获取TabDialog实例并连接语言变更信号
        try:
            from calibre_plugins.ask_grok import ask_grok_plugin
            if hasattr(ask_grok_plugin, 'plugin_instance') and ask_grok_plugin.plugin_instance:
                # 将当前对话框保存到插件实例中，方便其他组件访问
                ask_grok_plugin.plugin_instance.ask_dialog = self
                logger.debug("已将AskDialog实例保存到插件实例中")
        except Exception as e:
            logger.error(f"连接语言变更信号时出错: {str(e)}")
        
        
        # 设置当前书籍元数据到response_handler
        if hasattr(self.response_handler, 'history_manager'):
            self.response_handler.current_metadata = self.book_metadata
        
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
        self.response_handler.setup(
            response_area=self.response_area,
            send_button=self.send_button,
            i18n=self.i18n,
            api=self.api,
            input_area=self.input_area  # 添加输入区域
        )
        self.suggestion_handler.setup(self.response_area, self.input_area, self.suggest_button, self.api, self.i18n)
        
        # 添加事件过滤器
        self.input_area.installEventFilter(self)
        
        # 加载历史记录
        self._load_history()
        
        # 设置窗口大小
        self.resize(self.saved_width, self.saved_height)
        
        # 连接窗口大小变化信号
        self.resizeEvent = self.on_resize

    def _load_history(self):
        """加载历史记录"""
        if not hasattr(self, 'book_metadata') or not self.book_metadata:
            return
            
        try:
            if hasattr(self.response_handler, 'history_manager'):
                history = self.response_handler.history_manager.get_history(self.book_metadata)
                if history:
                    # 显示历史记录
                    self.input_area.setPlainText(history['question'])
                    # 标记为历史记录加载，避免重复保存
                    self.response_handler._update_ui_from_signal(
                        history['answer'], 
                        is_response=True,
                        is_history=True
                    )
                    logger.info(f"已加载历史记录，时间: {history.get('timestamp', '未知')}")
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
    
    def clear_history(self):
        """清除当前书籍的历史记录"""
        if not hasattr(self, 'book_metadata') or not self.book_metadata:
            return
            
        try:
            if hasattr(self.response_handler, 'history_manager'):
                # 这里需要实现清除特定书籍历史记录的逻辑
                # 由于当前设计是所有历史记录在一个文件中，我们需要更新文件内容
                # 这需要修改HistoryManager类
                self.statusBar.showMessage(self.i18n.get('clear_history_not_supported', 'Clear history for single book is not supported yet'))
        except Exception as e:
            logger.error(f"清除历史记录失败: {str(e)}")
            self.statusBar.showMessage(self.i18n.get('clear_history_failed', 'Failed to clear history'))
    
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
        """窗口大小变化时的处理函数"""
        prefs = get_prefs()
        prefs['ask_dialog_width'] = self.width()
        prefs['ask_dialog_height'] = self.height()
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
            
            # 更新状态栏中的模型信息标签
            if hasattr(self, 'model_info_label') and self.model_info_label:
                self.model_info_label.setText(f"{self.i18n.get('using_model', 'Model')}: {model_display_name}")
                logger.debug("已更新状态栏模型信息标签")
            else:
                logger.warning("无法更新模型信息标签: 标签不存在")
            
            # 更新窗口标题
            if hasattr(self, 'book_info') and self.book_info:
                self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
                logger.debug("已更新窗口标题")
            else:
                logger.warning("无法更新窗口标题: 书籍信息不可用")
                
        except Exception as e:
            logger.error(f"更新模型信息时出错: {str(e)}")
    
    def get_language_name(self, lang_code):
        """将语言代码转换为易读的语言名称"""
        if not lang_code:
            return None
        lang_code = lang_code.lower().strip()
        return self.LANGUAGE_MAP.get(lang_code, lang_code)
    
    def setup_ui(self):
        # 确保模型已经加载
        self.api.reload_model()
        
        # 获取当前使用的模型显示名称
        model_display_name = self.api.model_display_name
        
        # 更新窗口标题，包含模型信息
        self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)  # 设置最小高度与配置对话框一致
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 添加一个状态栏用于显示加载状态和模型信息
        self.statusBar = QStatusBar()
        
        # 添加模型信息到状态栏
        # 确保显示正确的模型名称，而不是 "Unknown Model"
        model_display_name = self.api.model_display_name
        self.model_info_label = QLabel(f"{self.i18n.get('using_model', 'Model')}: {model_display_name}")
        self.model_info_label.setStyleSheet("color: #666; font-size: 12px; padding-right: 10px;")
        self.statusBar.addPermanentWidget(self.model_info_label)
        
        layout.addWidget(self.statusBar)
        
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
        self.suggest_action.setShortcut(QKeySequence("Ctrl+R"))

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
        
        # 创建响应区域容器
        response_container = QWidget()
        response_layout = QVBoxLayout(response_container)
        response_layout.setContentsMargins(0, 0, 0, 0)
        response_layout.setSpacing(5)
        
        # 创建响应区域
        self.response_area = QTextBrowser()
        self.response_area.setOpenExternalLinks(True)  # 允许打开外部链接
        self.response_area.setMinimumHeight(250)  # 设置最小高度，允许用户拉伸
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
        
        # 创建按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        
        # 复制响应按钮
        self.copy_response_btn = QPushButton(self.i18n.get('copy_response', 'Copy Response'))
        self.copy_response_btn.setStyleSheet("""
            QPushButton {
                padding: 3px 8px;
                font-size: 12px;
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: transparent;
            }
            QPushButton:hover {
                background: palette(midlight);
            }
        """)
        self.copy_response_btn.clicked.connect(self.copy_response)
        
        # 复制问题和响应按钮
        copy_qa_text = self.i18n.get('copy_question_response', 'Copy Q&A')
        copy_qa_text = copy_qa_text.replace('&', '&&')
        self.copy_qr_btn = QPushButton(copy_qa_text)
        self.copy_qr_btn.setStyleSheet("""
            QPushButton {
                padding: 3px 8px;
                font-size: 12px;
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: transparent;
            }
            QPushButton:hover {
                background: palette(midlight);
            }
        """)
        self.copy_qr_btn.clicked.connect(self.copy_question_response)
        
        # 添加按钮到布局
        button_layout.addWidget(self.copy_response_btn)
        button_layout.addWidget(self.copy_qr_btn)
        button_layout.addStretch()
        
        # 将响应区域和按钮添加到容器
        response_layout.addWidget(self.response_area)
        response_layout.addWidget(button_container)
        
        # 添加到主布局
        layout.addWidget(response_container)
        
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
            /* 基础表格样式 */
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                border: 1px solid palette(midlight);
                font-size: 0.95em;
                line-height: 1.5;
            }
            /* 表格单元格 */
            th, td {
                border: 1px solid palette(midlight);
                padding: 8px 12px;
                text-align: left;
                vertical-align: top;
            }
            /* 表头样式 */
            thead {
                background-color: palette(light);
                font-weight: bold;
            }
            /* 表格行 */
            tr {
                border-bottom: 1px solid palette(midlight);
            }
            /* 最后一行不需要下边框 */
            tr:last-child {
                border-bottom: none;
            }
            /* 斑马纹 */
            tr:nth-child(even) {
                background-color: rgba(0, 0, 0, 0.02);
            }
            blockquote { 
                border-left: 4px solid palette(midlight); 
                margin: 10px 0; 
                padding: 0 10px; 
                color: #333;
                background-color: rgba(0, 0, 0, 0.02);
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
        """检查当前选择的模型是否设置了API Key"""
        from calibre_plugins.ask_grok.config import get_prefs
        
        prefs = get_prefs()
        selected_model = prefs.get('selected_model', 'grok')
        models_config = prefs.get('models', {})
        model_config = models_config.get(selected_model, {})
        
        # 获取token字段名，不同模型可能使用不同的字段名
        token_field = 'auth_token' if selected_model == 'grok' else 'api_key'
        token = model_config.get(token_field, '')
        
        # 如果是Custom模型，不强制要求API Key
        if selected_model == 'custom':
            return True
            
        if not token or not token.strip():
            # 只显示一个警告对话框，不自动打开配置窗口
            from PyQt5.QtWidgets import QMessageBox
            
            # 显示警告信息
            QMessageBox.information(
                self,
                self.i18n.get('auth_token_required_title', 'API Key Required'),
                self.i18n.get('auth_token_required_message', 'Please set your API Key in the configuration dialog.')
            )
            
            # 直接返回False，表示验证失败
            return False
        
        return True
    
    def send_question(self):
        """发送问题"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("=== 开始处理用户问题 ===")
        
        # 检查 token 是否有效
        if not self._check_auth_token():
            logger.error("Token 验证失败")
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
            logger.info("准备模板变量...")
            template_vars = {
                'query': question.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'title': getattr(self.book_info, 'title', self.i18n.get('unknown', 'Unknown')).replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'author': author_str.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'publisher': (getattr(self.book_info, 'publisher', '') or '').replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8'),
                'pubyear': str(pubyear).replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if pubyear else '',
                'language': language_name.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if language_name else '',
                'series': series.replace('\u2028', '\n').replace('\u2029', '\n').encode('utf-8').decode('utf-8') if series else ''
            }
            logger.info(f"模板变量准备完成: {template_vars}")
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
        
        logger.info(f"使用的模板: {template}")
        
        # 检查并替换模板中的变量名，确保用户输入能够正确插入
        if '{query}' not in template and '{question}' in template:
            logger.info("检测到旧版模板变量 {question}，自动替换为 {query}")
            template = template.replace('{question}', '{query}')
        
        # 格式化提示词
        try:
            logger.info("正在格式化提示词...")
            prompt = template.format(**template_vars)
            logger.info(f"格式化后的提示词: {prompt[:500]}{'...' if len(prompt) > 500 else ''}")
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
        logger.info("开始异步请求...")
        try:
            self.response_handler.start_async_request(prompt)
            logger.info("异步请求已启动")
        except Exception as e:
            logger.error(f"启动异步请求时出错: {str(e)}")
            self.response_handler.handle_error(f"启动请求时出错: {str(e)}")
    
    def eventFilter(self, obj, event):
        """事件过滤器，用于处理快捷键"""
        if event.type() == event.KeyPress:
            # 检查是否按下了 Ctrl+Enter 或 Cmd+Return
            if ((event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier) and 
                (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter)):
                self.send_question()
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
            from calibre_plugins.ask_grok.config import get_prefs
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
        
        # 更新模型信息标签
        if hasattr(self, 'model_info_label'):
            self.model_info_label.setText(f"{self.i18n.get('using_model', 'Model')}: {model_display_name}")
        
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
        # 准备关闭，让线程自然结束
        self.response_handler.prepare_close()
        self.suggestion_handler.prepare_close()  # 改用 prepare_close
        event.accept()
