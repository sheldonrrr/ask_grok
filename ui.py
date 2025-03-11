#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLabel)
from PyQt5.QtGui import QIcon
import os

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.ask_gpt.api import XAIClient
from calibre_plugins.ask_gpt.config import get_prefs

class AskGPTPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 使用相对路径指定图标
    action_spec = ('Ask Grok', 'images/ask_gpt.png', 'Ask Grok about this book', None)

    def __init__(self, parent, site_customization):
        InterfaceAction.__init__(self, parent, site_customization)
        self.api = None
        
    def genesis(self):
        # 连接事件
        self.qaction.triggered.connect(self.show_dialog)
        # 初始化 API
        self.initialize_api()
        
    def initialize_api(self):
        """Initialize the API client"""
        try:
            self.api = XAIClient()
        except Exception as e:
            self.api = None
        
    def apply_settings(self):
        self.initialize_api()

    def show_dialog(self):
        # 获取当前选中的书籍
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
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
