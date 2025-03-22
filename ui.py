#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt, QMenu, QAction, QTextCursor, QApplication
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLabel)
from PyQt5.QtGui import QIcon
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
    action_spec = ('Ask Grok', None, 'Ask Grok about this book', None)
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
        
        # 添加配置菜单项
        self.config_action = QAction(
            QIcon(I('images/config.png')), 
            '配置插件', 
            self.menu
        )
        self.config_action.triggered.connect(self.show_configuration)
        self.menu.addAction(self.config_action)
        
        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加主要动作
        self.ask_action = QAction(
            QIcon(I('dialog_question.png')),
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
        self.use_stream = True  # 默认开启流式输出
        
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
        self.response_area.setPlaceholderText("Grok 的回答将显示在这里...")
        layout.addWidget(self.response_area)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 发送按钮
        self.send_button = QPushButton('发送', self)
        self.send_button.clicked.connect(self.send_question)
        button_layout.addWidget(self.send_button)
        
        # 流式输出切换按钮
        self.stream_toggle = QPushButton('流式输出：开', self)  # 默认显示"开"
        self.stream_toggle.setCheckable(True)  # 使按钮可切换
        self.stream_toggle.setChecked(True)  # 默认选中
        self.stream_toggle.clicked.connect(self.toggle_stream)
        button_layout.addWidget(self.stream_toggle)
        
        layout.addLayout(button_layout)
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
    
    def toggle_stream(self):
        """切换流式输出状态"""
        self.use_stream = not self.use_stream
        self.stream_toggle.setText(f'流式输出：{"开" if self.use_stream else "关"}')
    
    def send_question(self):
        question = self.input_area.toPlainText()
        if not question:
            return
            
        # 构建提示词
        prompt = f"关于《{self.book_info.title}》这本书，{question}"
        
        # 清空响应区域
        self.response_area.clear()
        
        if self.use_stream:
            # 使用流式输出
            for chunk in self.api.ask_stream(prompt):
                cursor = self.response_area.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.insertText(chunk)
                self.response_area.setTextCursor(cursor)
                self.response_area.ensureCursorVisible()
                QApplication.processEvents() #强制处理事件，刷新界面
        else:
            # 使用普通输出
            try:
                response = self.api.ask(prompt)
                self.response_area.setText(response)
            except Exception as e:
                self.response_area.setText(f"错误：{str(e)}")
