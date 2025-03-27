#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import (Qt, QMenu, QAction, QTextCursor, QApplication, 
                     QKeySequence, QMessageBox, QPixmap, QPainter, QSize)
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTextEdit, QLabel)
from PyQt5.QtCore import Qt
import logging

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.ask_gpt.api import XAIClient
from calibre_plugins.ask_gpt.config import get_prefs, ConfigWidget

from calibre.utils.resources import get_path as I
from PyQt5.QtSvg import QSvgRenderer

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

        # 添加分隔符
        self.menu.addSeparator()
        
        # 添加主要动作
        self.about_action = self.create_menu_action(
            self.menu,
            'ask_gpt_about',
            '关于',
            description='关于插件',
            triggered=self.show_dialog2
        )
        
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
    def show_dialog2(self):
        """显示关于对话框"""
        msg = QMessageBox()
        msg.setWindowTitle("关于 Ask Grok")
        
        # 加载并设置图标
        icon_path = I('images/ask_gpt.png') # 显示插件图标
        icon_pixmap = QPixmap(icon_path)
        scaled_pixmap = None  # 初始化变量
        
        if not icon_pixmap.isNull():
            scaled_pixmap = icon_pixmap.scaledToHeight(
                128,
                Qt.TransformationMode.SmoothTransformation
            )

        # 创建标签并设置图标
        icon_label = QLabel()
        if scaled_pixmap:  # 检查是否成功创建了缩放图片
            icon_label.setPixmap(scaled_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)  # 居中对齐
            
            # 将图标标签添加到消息框布局
            layout = msg.layout()
            layout.addWidget(icon_label, 0, 0, 1, 1, Qt.AlignCenter)
        
        # 设置文本内容
        msg.setText("""
        <div style='text-align: left'>
            <h3 style='margin:200px 0 0 0'>Ask Grok</h3>
            <p style='font-weight: normal;'>Grok for reading.</p>
            <p style='color: #666; font-weight: normal; margin:20px 0 20px 0'>v1.0.0</p>
            <p style='color: #666; font-weight: normal; margin:0 0 0 0;'>👉 <a href='https://github.com/sheldonrrr/ask_gpt' style='color: #666; text-decoration: none; font-weight: normal; font-style: italic;'>GitHub Repo</a></p>
        </div>
        """)
        msg.setTextFormat(Qt.RichText)

        # 设置消息框整体样式
        msg.setStyleSheet("""
            QMessageBox {
                text-align: left;
                padding: 20px 40px;
            }
            QMessageBox QLabel {
                margin: 0 20px 0 0;
        """)

        # 设置对话框居中
        layout = msg.layout()
        layout.setSizeConstraint(layout.SetMinimumSize)
        msg.exec_()

class AskDialog(QDialog):
    # 语言代码映射
    LANGUAGE_MAP = {
        'zho': '中文',
        'zh': '中文',
        'eng': '英文',
        'en': '英文',
        'jpn': '日文',
        'ja': '日文',
        'kor': '韩文',
        'ko': '韩文',
        'fra': '法文',
        'fr': '法文',
        'deu': '德文',
        'de': '德文',
        'spa': '西班牙文',
        'es': '西班牙文',
        'rus': '俄文',
        'ru': '俄文',
    }

    def __init__(self, gui, book_info, api):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.book_info = book_info
        self.api = api
        self.setup_ui()
    
    def get_language_name(self, lang_code):
        """将语言代码转换为易读的语言名称"""
        if not lang_code:
            return None
        # 转换为小写并去除空格
        lang_code = lang_code.lower().strip()
        return self.LANGUAGE_MAP.get(lang_code, lang_code)
    
    def setup_ui(self):
        self.setWindowTitle(f'Ask Grok - {self.book_info.title}')
        self.setMinimumWidth(600)
        self.setMinimumHeight(800)
        
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建书籍信息标签
        metadata_info = []
        
        # 使用 HTML 格式化文本，保证每个字段都是一个段落
        title_text = f"<p><b>书名：</b>{self.book_info.title}</p>"
        authors_text = f"<p><b>作者：</b>{', '.join(self.book_info.authors)}</p>"
        metadata_info.extend([title_text, authors_text])
        
        if self.book_info.publisher:
            metadata_info.append(f"<p><b>出版社：</b>{self.book_info.publisher}</p>")
        if self.book_info.pubdate:
            metadata_info.append(f"<p><b>出版日期：</b>{self.book_info.pubdate.year}</p>")
        if self.book_info.language:
            lang_name = self.get_language_name(self.book_info.language)
            metadata_info.append(f"<p><b>语言：</b>{lang_name}</p>")
        if getattr(self.book_info, 'series', None):
            metadata_info.append(f"<p><b>系列：</b>{self.book_info.series}</p>")
            
        book_info = QLabel("".join(metadata_info))
        book_info.setWordWrap(True)  # 启用自动换行
        book_info.setTextFormat(Qt.RichText)  # 使用富文本格式
        book_info.setStyleSheet("""
            QLabel {
                color: #666666;
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 4px;
                line-height: 150%;
            }
            QLabel p {
                margin: 0;
                margin-bottom: 5px;
            }
            QLabel p:last-child {
                margin-bottom: 0;
            }
        """)
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
        metadata_info = []
        if self.book_info.publisher:
            metadata_info.append(f"出版社：{self.book_info.publisher}")
        if self.book_info.pubdate:
            metadata_info.append(f"出版日期：{self.book_info.pubdate.year}")
        if self.book_info.language:
            metadata_info.append(f"语言：{self.get_language_name(self.book_info.language)}")
        if getattr(self.book_info, 'series', None):
            metadata_info.append(f"系列：{self.book_info.series}")
            
        metadata_str = '；'.join(metadata_info)
        prompt = f"关于《{self.book_info.title}》（作者：{', '.join(self.book_info.authors)}）这本书的信息：\n{metadata_str}\n\n问题：{question}"
        
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
