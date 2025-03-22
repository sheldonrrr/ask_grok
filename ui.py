#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt, QMenu, QAction, QTextCursor, QApplication, QKeySequence, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLabel)
import logging

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.ask_gpt.api import XAIClient
from calibre_plugins.ask_gpt.config import get_prefs, ConfigWidget

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AskGPTPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 使用相对路径指定图标
    action_spec = ('Ask Grok', 'images/ask_gpt.png', 'Ask Grok about this book', 'Ctrl+L')
    action_type = 'global'

    def __init__(self, parent, site_customization):
        try:
            InterfaceAction.__init__(self, parent, site_customization)
        except Exception as e:
            logger.debug(f"初始化插件时出现非致命错误（可以忽略）：{str(e)}")
        self.api = None
        self.gui = parent
        logger.info("AskGPTPluginUI initialized")

    def genesis(self):
        logger.info("AskGPTPluginUI genesis called")

        # 获取插件版本
        base = self.interface_action_base_plugin
        self.version = base.name+"v%d.%d.%d"%base.version

        # 创建菜单
        self.menu = QMenu()
        self.menu.setToolTip(self.action_spec[2])
        self.qaction.setMenu(self.menu)
        
        # 官方文档指引设置图标
        icon = get_icons('images/ask_gpt.png', 'Ask Grok')
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)
        self.qaction.shortcut = QKeySequence(self.action_spec[3])

        # 添加配置菜单项
        self.config_action = self.create_menu_action(
            self.menu,
            'ask_gpt_config',
            '配置插件',
            description='配置 Ask Grok 插件',
            triggered=self.show_configuration
        )
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加主要动作
        self.ask_action = self.create_menu_action(
            self.menu,
            'ask_gpt_ask',
            'Ask Grok',
            description='开启弹窗',
            triggered=self.show_dialog
        )
        
        # 初始化 API
        self.initialize_api()
        
    def initialize_api(self):
        """Initialize the API client"""
        try:
            # 从环境变量或配置中获取认证令牌
            prefs = get_prefs()
            auth_token = prefs['auth_token']
            api_base = prefs['api_base_url']
            model = prefs['model']
            
            self.api = XAIClient(auth_token=auth_token, api_base=api_base, model=model)
        except Exception as e:
            from calibre.gui2 import error_dialog
            error_dialog(
                self.gui,
                'API 初始化失败',
                f'初始化 X.AI API 客户端失败：{str(e)}\n\n请检查配置中的 Authorization Token 是否正确设置。',
                show=True
            )
            self.api = None
        
    def apply_settings(self):
        self.initialize_api()

    def show_configuration(self):
        """显示配置对话框"""
        self.interface_action_base_plugin.do_user_config(parent=self.gui)

    def show_dialog(self):
        # 获取当前选中的书籍
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return
            
        # 如果 API 未初始化，尝试重新初始化
        if self.api is None:
            self.initialize_api()
            if self.api is None:
                return
        
        # 获取书籍信息
        book_id = self.gui.library_view.model().id(rows[0])
        mi = self.gui.current_db.new_api.get_metadata(book_id)
        
        # 显示对话框
        d = AskDialog(self.gui, mi, self.api)
        d.exec_()

class AskDialog(QDialog):
    def __init__(self, gui, book_info, api):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.book_info = book_info
        self.api = api
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle(f'Ask Grok - {self.book_info.title}')
        self.setMinimumWidth(600)
        self.setMinimumHeight(800)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建书籍信息标签
        book_info = QLabel(f"书名：{self.book_info.title}\n作者：{', '.join(self.book_info.authors)}")
        layout.addWidget(book_info)
        
        # 创建输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("在这里输入你的问题...")
        self.input_area.setMaximumHeight(100)
        layout.addWidget(self.input_area)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        # 创建发送按钮和快捷键提示的容器
        send_container = QVBoxLayout()
        
        self.send_button = QPushButton("发送")
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
            shortcut_text = "Ctrl + Enter"
        else:
            shortcut_text = "⌘ + Return"
        shortcut_label = QLabel(shortcut_text)
        shortcut_label.setStyleSheet("color: gray; font-size: 11px;")
        shortcut_label.setAlignment(Qt.AlignCenter)
        send_container.addWidget(shortcut_label)
        
        # 将发送按钮容器添加到按钮布局
        button_layout.addStretch()
        button_layout.addLayout(send_container)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # 创建响应区域
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        layout.addWidget(self.response_area)
        
        # 设置快捷键
        if hasattr(Qt, 'ControlModifier'):
            send_shortcut = QKeySequence(Qt.ControlModifier | Qt.Key_Return)
        else:
            send_shortcut = QKeySequence(Qt.MetaModifier | Qt.Key_Return)
            
        self.send_shortcut = QAction(self)
        self.send_shortcut.setShortcut(send_shortcut)
        self.send_shortcut.triggered.connect(self.send_question)
        self.addAction(self.send_shortcut)
        
        # 设置输入框焦点
        self.input_area.setFocus()
    
    def send_question(self):
        question = self.input_area.toPlainText()
        if not question:
            return
            
        # 禁用发送按钮
        self.send_button.setEnabled(False)
        
        # 构建提示词
        prompt = f"关于《{self.book_info.title}》这本书，{question}"
        
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
            self.response_area.setText(f"错误：{str(e)}")
        finally:
            # 重新启用发送按钮
            self.send_button.setEnabled(True)
