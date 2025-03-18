#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt, QMenu, QAction
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLabel)
from PyQt5.QtGui import QIcon
import os
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
    action_spec = ('Ask Grok', 'images/ask_gpt.png', 'Ask Grok about this book', None)

    def __init__(self, parent, site_customization):
        try:
            InterfaceAction.__init__(self, parent, site_customization)
        except Exception as e:
            logger.debug(f"初始化插件时出现非致命错误（可以忽略）：{str(e)}")
        self.api = None
        
    def genesis(self):

        # 获取插件版本
        base = self.interface_action_base_plugin
        self.version = base.name+"v%d.%d.%d"%base.version

        # 创建菜单
        self.menu = QMenu()
        self.menu.setToolTip(self.action_spec[2])
        self.qaction.setMenu(self.menu)
        
        # 添加配置菜单项
        self.config_action = QAction(
            QIcon('images/ask_gpt.png'), 
            '配置插件', 
            self.menu
        )
        self.config_action.triggered.connect(self.show_configuration)
        self.menu.addAction(self.config_action)
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加主要动作
        self.ask_action = QAction(
            QIcon('images/ask_gpt.png'),
            'Ask Grok',
            self.menu
        )
        self.ask_action.triggered.connect(self.show_dialog)
        self.menu.addAction(self.ask_action)
        
        # 初始化 API
        self.initialize_api()
        
    def initialize_api(self):
        """Initialize the API client"""
        try:
            self.api = XAIClient()
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
        self.setWindowTitle('Ask Grok')
        layout = QVBoxLayout(self)
        
        # 显示书籍信息
        book_info = QLabel(f"书名：{self.book_info.title}\n作者：{', '.join(self.book_info.authors)}")
        layout.addWidget(book_info)
        
        # 输入区域
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("输入你的问题...")
        self.input_area.setMaximumHeight(100)
        layout.addWidget(self.input_area)
        
        # 响应区域
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setPlaceholderText("ChatGPT 的回答将显示在这里...")
        layout.addWidget(self.response_area)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.send_button = QPushButton('发送', self)
        self.send_button.clicked.connect(self.send_question)
        button_layout.addWidget(self.send_button)
        
        layout.addLayout(button_layout)
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
    
    def send_question(self):
        question = self.input_area.toPlainText()
        if not question:
            return
            
        # 构建提示词
        prompt = f"关于《{self.book_info.title}》这本书，{question}"
        
        # 调用API
        try:
            response = self.api.ask(prompt)
            self.response_area.setText(response)
        except Exception as e:
            self.response_area.setText(f"错误：{str(e)}")
