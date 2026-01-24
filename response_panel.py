#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
响应面板组件 - 用于多AI并行请求功能
每个面板包含：AI选择器、响应区域、操作按钮
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextBrowser, QPushButton, QSizePolicy, QToolButton, QMenu)
from PyQt5.QtCore import Qt, pyqtSignal
from calibre_plugins.ask_ai_plugin.widgets import NoScrollComboBox, apply_button_style
from calibre_plugins.ask_ai_plugin.ui_constants import (
    SPACING_SMALL, SPACING_MEDIUM, PADDING_MEDIUM
)

logger = logging.getLogger(__name__)


class ResponsePanel(QWidget):
    """单个AI响应面板组件
    
    包含：
    - Header: AI标签 + AI切换器
    - Response Area: 响应文本显示区域
    - Button Bar: 复制、导出按钮
    """
    
    # 信号
    ai_changed = pyqtSignal(int, str)  # (panel_index, new_ai_id)
    request_started = pyqtSignal(int)  # panel_index
    request_finished = pyqtSignal(int)  # panel_index
    
    def __init__(self, panel_index, parent, api, i18n, show_ai_switcher=True):
        """初始化响应面板
        
        Args:
            panel_index: 面板索引（0-3）
            parent: 父窗口
            api: API客户端实例
            i18n: 国际化字典
            show_ai_switcher: 是否在面板内显示 AI 切换器（默认 True）
        """
        super().__init__(parent)
        self.panel_index = panel_index
        self.parent_dialog = parent
        self.api = api
        self.i18n = i18n
        self.response_handler = None  # 将在setup后初始化
        self.show_ai_switcher = show_ai_switcher
        
        # 标志：是否正在初始化（用于避免初始化时弹出确认对话框）
        self._is_initializing = True
        
        # 当前问题（用于按钮状态判断）
        self.current_question = ""
        
        # 存储原始Markdown文本（用于复制Markdown格式）
        self._original_markdown_text = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI布局"""
        # 检查是否为AI搜索模式
        is_ai_search_mode = hasattr(self.parent_dialog, 'books_info') and not self.parent_dialog.books_info
        
        # 主布局：垂直
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(SPACING_SMALL)
        
        # === Header 区域（横向） ===
        # 只有当 show_ai_switcher 为 True 时才显示 header
        if self.show_ai_switcher:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(SPACING_SMALL)
            
            # AI切换器（直接显示模型名称，不需要"AI 1:"标签）
            from calibre_plugins.ask_ai_plugin.ui_constants import BUTTON_HEIGHT
            self.ai_switcher = NoScrollComboBox()
            self.ai_switcher.setMinimumWidth(200)
            self.ai_switcher.setFixedHeight(BUTTON_HEIGHT)  # 与按钮保持相同高度
            # 设置样式：文字左对齐
            self.ai_switcher.setStyleSheet("""
                QComboBox {
                    text-align: left;
                    padding-left: 8px;
                }
            """)
            self.ai_switcher.currentIndexChanged.connect(self.on_ai_switched)
            header_layout.addWidget(self.ai_switcher)
            header_layout.addStretch()
            
            main_layout.addLayout(header_layout)
        else:
            # 不显示 header，但仍然创建 ai_switcher（将被添加到外部布局）
            from calibre_plugins.ask_ai_plugin.ui_constants import BUTTON_HEIGHT
            self.ai_switcher = NoScrollComboBox()
            self.ai_switcher.setMinimumWidth(200)
            self.ai_switcher.setFixedHeight(BUTTON_HEIGHT)
            self.ai_switcher.setStyleSheet("""
                QComboBox {
                    text-align: left;
                    padding-left: 8px;
                }
            """)
            self.ai_switcher.currentIndexChanged.connect(self.on_ai_switched)
        
        # === 历史记录信息栏（可选显示） ===
        self.history_info_bar = None  # 初始为None，加载历史时才创建
        
        # === Response Area（占据主要空间） ===
        self.response_area = QTextBrowser()
        self.response_area.setOpenExternalLinks(False)  # 禁用外部链接，使用自定义处理
        self.response_area.setMinimumHeight(200)
        self.response_area.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction | 
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        # 连接链接点击信号
        self.response_area.anchorClicked.connect(self._on_anchor_clicked)
        self.response_area.setStyleSheet("""
            QTextBrowser {
                border: 1px dashed palette(mid);
                color: palette(text);
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.response_area.setPlaceholderText(self.i18n.get('response_placeholder', 'Response soon...'))
        
        # 设置Markdown样式
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
                margin: 15px 0;
            }
            th, td {
                border: 1px solid palette(midlight);
                padding: 8px 12px;
                text-align: left;
            }
            a {
                color: #0066cc;
                text-decoration: underline;
                cursor: pointer;
            }
            a:hover {
                color: #0044aa;
            }
        """)
        
        main_layout.addWidget(self.response_area, stretch=1)  # stretch=1 让它占据剩余空间
        
        # === Button Bar（操作按钮 - 紧凑布局） ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SPACING_SMALL)
        
        # 从config读取用户上次的选择和parallel_ai_count
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        self.copy_mode = prefs.get('copy_mode', 'response')  # 'response' or 'qa'
        self.copy_format = prefs.get('copy_format', 'plain')  # 'plain' or 'markdown'
        self.export_mode = prefs.get('export_mode', 'current')  # 'current' or 'history'
        parallel_ai_count = prefs.get('parallel_ai_count', 1)
        
        # 创建复制按钮（QToolButton with menu）
        self.copy_btn = QToolButton()
        self.copy_btn.setPopupMode(QToolButton.MenuButtonPopup)  # 分离式下拉按钮
        self._update_copy_button_text()
        apply_button_style(self.copy_btn, min_width=100)
        self.copy_btn.clicked.connect(self._on_copy_clicked)
        self.copy_btn.setEnabled(False)  # 默认禁用，收到回复后启用
        
        # 创建复制按钮的菜单
        copy_menu = QMenu(self)
        self.copy_response_action = copy_menu.addAction(self.i18n.get('copy_mode_response', 'Answer'))
        self.copy_response_action.triggered.connect(lambda: self._switch_copy_mode('response'))
        self.copy_qa_action = copy_menu.addAction(self.i18n.get('copy_mode_qa', 'Q&A'))
        self.copy_qa_action.triggered.connect(lambda: self._switch_copy_mode('qa'))
        
        # 添加分隔符和格式选项
        copy_menu.addSeparator()
        self.copy_plain_action = copy_menu.addAction(self.i18n.get('copy_format_plain', 'Plain Text'))
        self.copy_plain_action.triggered.connect(lambda: self._switch_copy_format('plain'))
        self.copy_markdown_action = copy_menu.addAction(self.i18n.get('copy_format_markdown', 'Markdown'))
        self.copy_markdown_action.triggered.connect(lambda: self._switch_copy_format('markdown'))
        
        self.copy_btn.setMenu(copy_menu)
        self._update_copy_menu_checkmarks()
        
        # 根据parallel_ai_count决定按钮布局
        if parallel_ai_count == 1:
            # 单AI模式：显示复制和导出两个按钮
            # 创建导出按钮（QToolButton with menu）
            self.export_btn = QToolButton()
            self.export_btn.setPopupMode(QToolButton.MenuButtonPopup)  # 分离式下拉按钮
            self._update_export_button_text()
            apply_button_style(self.export_btn, min_width=150)
            self.export_btn.clicked.connect(self._on_export_clicked)
            self.export_btn.setEnabled(False)  # 默认禁用，有问题和回答后启用
            
            # 创建导出按钮的菜单
            export_menu = QMenu(self)
            self.export_current_action = export_menu.addAction(self.i18n.get('export_mode_current', 'Current Q&A'))
            self.export_current_action.triggered.connect(lambda: self._switch_export_mode('current'))
            self.export_history_action = export_menu.addAction(self.i18n.get('export_mode_history', 'History'))
            self.export_history_action.triggered.connect(lambda: self._switch_export_mode('history'))
            self.export_btn.setMenu(export_menu)
            self._update_export_menu_checkmarks()
            
            # AI搜索模式下隐藏复制和导出按钮
            if not is_ai_search_mode:
                button_layout.addWidget(self.copy_btn)
                button_layout.addWidget(self.export_btn)
            button_layout.addStretch()
        else:
            # 多AI模式（2个面板）
            # 所有面板都显示复制按钮（左对齐）
            if not is_ai_search_mode:
                button_layout.addWidget(self.copy_btn)
            button_layout.addStretch()
            
            # 只有最后一个面板（右侧）显示导出按钮（右对齐）
            # 获取总面板数（从父对话框）
            total_panels = parallel_ai_count
            is_last_panel = (self.panel_index == total_panels - 1)
            
            if is_last_panel:
                # 创建导出按钮（QToolButton with menu）
                self.export_btn = QToolButton()
                self.export_btn.setPopupMode(QToolButton.MenuButtonPopup)
                self._update_export_button_text()
                apply_button_style(self.export_btn, min_width=150)
                self.export_btn.clicked.connect(self._on_export_clicked_multi_ai)
                self.export_btn.setEnabled(False)
                
                # 创建导出按钮的菜单
                export_menu = QMenu(self)
                self.export_current_action = export_menu.addAction(self.i18n.get('export_mode_current', 'Current Q&A'))
                self.export_current_action.triggered.connect(lambda: self._switch_export_mode('current'))
                self.export_history_action = export_menu.addAction(self.i18n.get('export_mode_history', 'History'))
                self.export_history_action.triggered.connect(lambda: self._switch_export_mode('history'))
                self.export_btn.setMenu(export_menu)
                self._update_export_menu_checkmarks()
                
                # AI搜索模式下隐藏导出按钮
                if not is_ai_search_mode:
                    button_layout.addWidget(self.export_btn)
            else:
                # 非最后一个面板，不创建导出按钮
                self.export_btn = None
        
        main_layout.addLayout(button_layout)
        
        # 设置最小高度，防止按钮覆盖响应区域
        self.setMinimumHeight(350)  # 确保有足够空间显示所有元素
        
        # 添加边框样式
        # 使用 ResponsePanel 类名选择器，避免影响子控件（如 QComboBox 的下拉列表）
        self.setObjectName("ResponsePanel")
        self.setStyleSheet("""
            #ResponsePanel {
                border: 1px solid palette(mid);
                border-radius: 4px;
                background: palette(base);
            }
        """)
        
    def setup_response_handler(self, response_handler):
        """设置响应处理器
        
        Args:
            response_handler: ResponseHandler实例
        """
        self.response_handler = response_handler
        # 设置AI标识符，用于历史记录
        self.response_handler.ai_id = None  # 初始为None，在发送请求时更新
        
    def get_selected_ai(self):
        """获取当前选中的AI ID
        
        Returns:
            str: AI ID，如果没有选中则返回None
        """
        return self.ai_switcher.currentData()
    
    def populate_ai_switcher(self, configured_ais, used_ais=None):
        """填充AI切换器
        
        Args:
            configured_ais: 已配置的AI列表 [(ai_id, display_name), ...]
            used_ais: 已被其他面板使用的AI ID集合
        """
        if used_ais is None:
            used_ais = set()
        
        logger.info(f"[Panel {self.panel_index}] populate_ai_switcher - configured_ais数量: {len(configured_ais)}, used_ais: {used_ais}")
        
        # 阻止信号触发
        self.ai_switcher.blockSignals(True)
        
        current_ai = self.ai_switcher.currentData()
        logger.info(f"[Panel {self.panel_index}] 当前选中的AI: {current_ai}")
        self.ai_switcher.clear()
        
        # 添加一个空选项（用于留空）
        self.ai_switcher.addItem(
            self.i18n.get('select_ai', '-- Select AI --'),
            None
        )
        
        # 检查是否有可用的AI
        available_ais = [(ai_id, name) for ai_id, name in configured_ais if ai_id not in used_ais or ai_id == current_ai]
        logger.info(f"[Panel {self.panel_index}] 过滤后可用的AI数量: {len(available_ais)}, AI列表: {[ai_id for ai_id, _ in available_ais]}")
        
        if not available_ais:
            # 没有可用的AI，只显示提示
            self.ai_switcher.addItem(
                self.i18n.get('add_more_ai_providers', 'Please add more AI providers in settings'),
                None
            )
            self.ai_switcher.setEnabled(True)  # 保持启用，让用户看到提示
            self.response_area.setPlaceholderText(
                self.i18n.get('no_ai_available', 'No AI available for this panel')
            )
        else:
            # 有可用的AI
            for ai_id, display_name in available_ais:
                self.ai_switcher.addItem(display_name, ai_id)
            
            # 尝试恢复之前的选择
            if current_ai:
                index = self.ai_switcher.findData(current_ai)
                if index >= 0:
                    self.ai_switcher.setCurrentIndex(index)
                else:
                    # 如果之前的选择不可用，设置为空选项
                    self.ai_switcher.setCurrentIndex(0)
            
            self.ai_switcher.setEnabled(True)
        
        # 恢复信号
        self.ai_switcher.blockSignals(False)
    
    def on_ai_switched(self, index):
        """AI切换事件处理"""
        ai_id = self.ai_switcher.currentData()
        if ai_id:
            logger.info(f"面板 {self.panel_index} 切换到 AI: {ai_id}")
            
            # 检查是否需要询问用户是否设为默认AI
            # 如果用户取消切换，则不触发 ai_changed 信号
            if not self._check_and_prompt_default_ai(ai_id):
                return
            
            self.ai_changed.emit(self.panel_index, ai_id)
    
    def _check_and_prompt_default_ai(self, selected_ai_id):
        """检查并询问用户是否将选择的AI设为默认
        
        Args:
            selected_ai_id: 用户选择的AI ID
            
        Returns:
            bool: True表示继续切换AI，False表示用户取消切换
        """
        from PyQt5.QtWidgets import QMessageBox, QPushButton
        from calibre_plugins.ask_ai_plugin.config import prefs
        
        # 如果正在初始化，跳过提示（避免在恢复上次选择时弹出确认框）
        if self._is_initializing:
            return True
        
        # 只在单面板模式下提示
        if not hasattr(self.parent_dialog, 'response_panels'):
            return True
        
        panel_count = len(self.parent_dialog.response_panels)
        if panel_count != 1:
            return True
        
        # 获取config中当前的默认AI
        current_default_ai = prefs.get('selected_model', 'grok')
        
        # 如果选择的AI与默认AI相同，不提示
        if selected_ai_id == current_default_ai:
            return True
        
        # 获取AI的显示名称
        ai_display_name = self.ai_switcher.currentText()
        
        # 弹出确认对话框（使用自定义按钮文字以支持本地化）
        msg_title = self.i18n.get('set_default_ai_title', 'Set Default AI')
        msg_text = self.i18n.get(
            'set_default_ai_message',
            'You have switched to "{0}". Would you like to set it as the default AI for future queries?'
        ).format(ai_display_name)
        
        # 创建消息框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(msg_title)
        msg_box.setText(msg_text)
        msg_box.setIcon(QMessageBox.Question)
        
        # 添加本地化的按钮
        yes_text = self.i18n.get('yes', 'Yes')
        no_text = self.i18n.get('no', 'No')
        yes_button = msg_box.addButton(yes_text, QMessageBox.YesRole)
        no_button = msg_box.addButton(no_text, QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)  # 默认选择No，避免误操作
        
        msg_box.exec_()
        clicked_button = msg_box.clickedButton()
        
        if clicked_button == yes_button:
            # 用户选择Yes，更新config
            prefs.set('selected_model', selected_ai_id)
            logger.info(f"用户确认将 {selected_ai_id} 设为默认AI")
            
            # 显示成功提示
            success_msg = self.i18n.get(
                'set_default_ai_success',
                'Default AI has been set to "{0}".'
            ).format(ai_display_name)
            QMessageBox.information(self, self.i18n.get('info', 'Information'), success_msg)
            return True
        else:
            # 用户选择No，恢复到之前的AI选择
            
            # 阻止信号，避免递归调用
            self.ai_switcher.blockSignals(True)
            
            # 恢复到默认AI
            index = self.ai_switcher.findData(current_default_ai)
            if index >= 0:
                self.ai_switcher.setCurrentIndex(index)
            
            # 恢复信号
            self.ai_switcher.blockSignals(False)
            
            return False
    
    def send_request(self, prompt, model_id=None, use_library_chat=False):
        """发送请求到选中的AI
        
        Args:
            prompt: 提示词
            model_id: 可选，指定使用的模型ID。如果为None，使用当前选中的AI
            use_library_chat: 是否使用Library Chat功能
        """
        if not self.response_handler:
            logger.error(f"面板 {self.panel_index} 的 ResponseHandler 未初始化")
            return
        
        # 使用指定的model_id或当前选中的AI
        target_model_id = model_id if model_id else self.get_selected_ai()
        
        if not target_model_id:
            logger.warning(f"面板 {self.panel_index} 没有选中的AI")
            return
        
        logger.info(f"[面板 {self.panel_index}] 开始请求 AI: {target_model_id}, use_library_chat={use_library_chat}")
        self.request_started.emit(self.panel_index)
        
        # 更新响应处理器的AI标识符（用于历史记录）
        self.response_handler.ai_id = target_model_id
        logger.info(f"[面板 {self.panel_index}] 已设置 ai_id={target_model_id} 用于历史记录")
        
        # 调用响应处理器发送请求，传递model_id和use_library_chat参数
        self.response_handler.start_async_request(prompt, model_id=target_model_id, use_library_chat=use_library_chat)
        logger.info(f"[面板 {self.panel_index}] 异步请求已启动")
    
    def get_response_text(self):
        """获取响应文本
        
        Returns:
            str: 响应文本
        """
        return self.response_area.toPlainText()
    
    def _get_clean_text(self):
        """获取干净的文本内容（根据copy_format返回不同格式）
        
        Returns:
            str: 根据copy_format设置返回Markdown或纯文本
        """
        if self.copy_format == 'markdown':
            # 尝试从ResponseHandler获取原始Markdown文本
            if self.response_handler and hasattr(self.response_handler, '_response_text'):
                original_text = self.response_handler._response_text
                if original_text:
                    return original_text
            # 如果没有，尝试从流式响应获取
            if self.response_handler and hasattr(self.response_handler, '_stream_response'):
                stream_text = self.response_handler._stream_response
                if stream_text:
                    return stream_text
            # 如果都没有，使用存储的原始文本
            if self._original_markdown_text:
                return self._original_markdown_text
        
        # toPlainText() 已经自动移除所有HTML标签和CSS，返回纯文本
        return self.response_area.toPlainText()
    
    def copy_response(self):
        """复制响应内容到剪贴板"""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        
        # 根据copy_format设置返回不同格式的文本
        # 'markdown': 返回原始Markdown文本（保留**bold**、`code`等格式符号）
        # 'plain': 返回纯文本（移除所有HTML/CSS和Markdown符号）
        response_text = self._get_clean_text()
        
        if response_text.strip():
            clipboard.setText(response_text)
            self._show_copy_tooltip(self.copy_btn, self.i18n.get('copied', 'Copied!'))
    
    def copy_question_response(self):
        """复制问题和响应内容到剪贴板（包含完整元数据和模型信息）"""
        from PyQt5.QtWidgets import QApplication
        from datetime import datetime
        clipboard = QApplication.clipboard()
        
        # 从父对话框获取问题
        question = ""
        if hasattr(self.parent_dialog, 'input_area') and self.parent_dialog.input_area:
            question = self.parent_dialog.input_area.toPlainText().strip()
        
        # 获取干净的响应文本
        response = self._get_clean_text()
        
        if not question and not response:
            return
        
        # 使用统一的格式化函数
        text = self._format_qa_content(question, response, include_metadata=True, include_model_info=True)
        clipboard.setText(text)
        self._show_copy_tooltip(self.copy_btn, self.i18n.get('copied', 'Copied!'))
    
    def _get_ai_display_name(self, ai_name):
        """获取AI的友好显示名称（正确大小写）
        
        Args:
            ai_name: AI的内部名称（如 'openai', 'grok'）
            
        Returns:
            str: 友好的显示名称（如 'OpenAI', 'Grok'）
        """
        display_names = {
            'openai': 'OpenAI',
            'grok': 'Grok',
            'gemini': 'Gemini',
            'deepseek': 'DeepSeek',
            'anthropic': 'Claude',
            'nvidia': 'Nvidia',
            'openrouter': 'OpenRouter',
            'ollama': 'Ollama',
            'custom': 'Custom'
        }
        return display_names.get(ai_name.lower(), ai_name.capitalize())
    
    def _format_qa_content(self, question, response, include_metadata=True, include_model_info=True):
        """统一格式化问答内容
        
        Args:
            question: 问题文本
            response: 回答文本
            include_metadata: 是否包含书籍元数据
            include_model_info: 是否包含AI模型信息
            
        Returns:
            格式化后的文本
        """
        from datetime import datetime
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        
        separator = "────"
        content_parts = []
        
        # 1. 书籍元数据（支持多书模式）
        if include_metadata and hasattr(self.parent_dialog, 'books_metadata') and self.parent_dialog.books_metadata:
            books_metadata = self.parent_dialog.books_metadata
            is_multi_book = len(books_metadata) > 1
            
            content_parts.append(self.i18n.get('pdf_book_metadata', '书籍元数据'))
            content_parts.append(separator)
            
            for idx, book_metadata in enumerate(books_metadata, 1):
                # 多书模式时添加书籍序号
                if is_multi_book:
                    content_parts.append(f"[{self.i18n.get('book', 'Book')} {idx}]")
                
                if book_metadata.get('title'):
                    content_parts.append(f"{self.i18n.get('metadata_title', 'Title')}: {book_metadata['title']}")
                if book_metadata.get('authors'):
                    authors = ', '.join(book_metadata['authors']) if isinstance(book_metadata['authors'], list) else str(book_metadata['authors'])
                    content_parts.append(f"{self.i18n.get('metadata_authors', 'Authors')}: {authors}")
                if book_metadata.get('publisher'):
                    content_parts.append(f"{self.i18n.get('metadata_publisher', 'Publisher')}: {book_metadata['publisher']}")
                if book_metadata.get('pubdate'):
                    content_parts.append(f"{self.i18n.get('metadata_pubdate', 'Publication Date')}: {book_metadata['pubdate']}")
                if book_metadata.get('languages'):
                    langs = ', '.join(book_metadata['languages']) if isinstance(book_metadata['languages'], list) else str(book_metadata['languages'])
                    content_parts.append(f"{self.i18n.get('metadata_language', 'Languages')}: {langs}")
                
                # 多书模式时在每本书之间添加空行
                if is_multi_book and idx < len(books_metadata):
                    content_parts.append("")
            
            content_parts.append("")
            content_parts.append("")
        
        # 2. 问题
        content_parts.append(self.i18n.get('pdf_question', 'QUESTION'))
        content_parts.append(separator)
        content_parts.append(question if question else self.i18n.get('no_question', 'No question'))
        content_parts.append("")
        content_parts.append("")
        
        # 3. 回答
        content_parts.append(self.i18n.get('pdf_answer', 'ANSWER'))
        content_parts.append(separator)
        content_parts.append(response if response else self.i18n.get('no_response', 'No response'))
        content_parts.append("")
        content_parts.append("")
        
        # 4. AI模型信息
        if include_model_info:
            prefs = get_prefs()
            ai_id = self.get_selected_ai() or "unknown"
            models_config = prefs.get('models', {})
            model_config = models_config.get(ai_id, {})
            
            content_parts.append(self.i18n.get('pdf_model_info', 'AI MODEL INFORMATION'))
            content_parts.append(separator)
            
            if model_config.get('display_name'):
                content_parts.append(f"{self.i18n.get('model_provider', 'Provider')}: {model_config['display_name']}")
            if model_config.get('model'):
                content_parts.append(f"{self.i18n.get('model_name', 'Model')}: {model_config['model']}")
            if model_config.get('api_base_url'):
                content_parts.append(f"{self.i18n.get('model_api_url', 'API Base URL')}: {model_config['api_base_url']}")
            
            content_parts.append("")
            content_parts.append("")
        
        # 5. 生成信息
        content_parts.append(self.i18n.get('pdf_generated_by', 'GENERATED BY'))
        content_parts.append(separator)
        content_parts.append(f"{self.i18n.get('pdf_plugin', 'Plugin')}: Ask AI Plugin (calibre Plugin)")
        content_parts.append(f"GitHub: https://github.com/sheldonrrr/ask_grok")
        content_parts.append(f"{self.i18n.get('pdf_software', 'Software')}: calibre E-book Manager (https://calibre-ebook.com)")
        content_parts.append(f"{self.i18n.get('pdf_generated_time', 'Generated Time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return '\n'.join(content_parts)
    
    def _update_copy_button_text(self):
        """更新复制按钮文字"""
        if self.copy_mode == 'response':
            self.copy_btn.setText(self.i18n.get('copy_response_btn', 'Copy Answer'))
        else:  # 'qa'
            self.copy_btn.setText(self.i18n.get('copy_qa_btn', 'Copy Q&A'))
    
    def _update_export_button_text(self):
        """更新导出按钮文字"""
        if not hasattr(self, 'export_btn') or self.export_btn is None:
            return
        
        if self.export_mode == 'current':
            self.export_btn.setText(self.i18n.get('export_current_btn', 'Export Q&A as PDF'))
        else:  # 'history'
            self.export_btn.setText(self.i18n.get('export_history_btn', 'Export History as PDF'))
    
    def _update_copy_menu_checkmarks(self):
        """更新复制菜单的勾选标记"""
        self.copy_response_action.setText(
            ('✓ ' if self.copy_mode == 'response' else '') + 
            self.i18n.get('copy_mode_response', 'Answer')
        )
        self.copy_qa_action.setText(
            ('✓ ' if self.copy_mode == 'qa' else '') + 
            self.i18n.get('copy_mode_qa', 'Q&A')
        )
        
        # 更新格式选项的勾选标记
        self.copy_plain_action.setText(
            ('✓ ' if self.copy_format == 'plain' else '') + 
            self.i18n.get('copy_format_plain', 'Plain Text')
        )
        self.copy_markdown_action.setText(
            ('✓ ' if self.copy_format == 'markdown' else '') + 
            self.i18n.get('copy_format_markdown', 'Markdown')
        )
    
    def _update_export_menu_checkmarks(self):
        """更新导出菜单的勾选标记"""
        if not hasattr(self, 'export_btn') or self.export_btn is None:
            return
        
        self.export_current_action.setText(
            ('✓ ' if self.export_mode == 'current' else '') + 
            self.i18n.get('export_mode_current', 'Current Q&A')
        )
        self.export_history_action.setText(
            ('✓ ' if self.export_mode == 'history' else '') + 
            self.i18n.get('export_mode_history', 'History')
        )
    
    def _on_copy_clicked(self):
        """复制按钮点击事件"""
        if self.copy_mode == 'response':
            self.copy_response()
        else:  # 'qa'
            self.copy_question_response()
    
    def _on_export_clicked(self):
        """导出按钮点击事件（单AI模式）"""
        if self.export_mode == 'current':
            self.export_to_pdf()
        else:  # 'history'
            self.export_all_history_to_pdf()
    
    def _on_export_clicked_multi_ai(self):
        """导出按钮点击事件（多AI模式）"""
        if self.export_mode == 'current':
            self.export_multi_ai_to_pdf()
        else:  # 'history'
            self.export_all_history_to_pdf()
    
    def _switch_copy_mode(self, mode):
        """切换复制模式"""
        self.copy_mode = mode
        self._update_copy_button_text()
        self._update_copy_menu_checkmarks()
        
        # 切换模式后更新按钮状态
        self.update_button_states()
        
        # 保存到config
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        prefs['copy_mode'] = mode
    
    def _switch_copy_format(self, format_type):
        """切换复制格式"""
        self.copy_format = format_type
        self._update_copy_menu_checkmarks()
        
        # 保存到config
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        prefs['copy_format'] = format_type
    
    def _switch_export_mode(self, mode):
        """切换导出模式"""
        self.export_mode = mode
        self._update_export_button_text()
        self._update_export_menu_checkmarks()
        
        # 保存到config
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        prefs['export_mode'] = mode
    
    def export_multi_ai_to_pdf(self):
        """导出所有AI面板的问答为单个PDF文件（多AI模式）"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from PyQt5.QtPrintSupport import QPrinter
        from PyQt5.QtGui import QTextDocument
        from datetime import datetime
        
        logger.info("开始导出多AI问答PDF")
        
        # 从父对话框获取所有面板
        if not hasattr(self.parent_dialog, 'response_panels'):
            logger.warning("无法获取响应面板列表")
            return
        
        panels = self.parent_dialog.response_panels
        
        # 从父对话框获取问题
        question = ""
        if hasattr(self.parent_dialog, 'input_area') and self.parent_dialog.input_area:
            question = self.parent_dialog.input_area.toPlainText().strip()
        
        # 检查是否有内容
        has_content = False
        for panel in panels:
            if panel.response_area.toPlainText().strip():
                has_content = True
                break
        
        if not has_content:
            logger.warning("所有面板都没有内容可导出")
            return
        
        # 生成默认文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        default_filename = f"Multi-AI_QA_{timestamp}.pdf"
        
        # 检查是否启用默认导出文件夹（强制重新加载最新配置）
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        # 强制刷新配置以获取最新值
        if hasattr(prefs, 'refresh'):
            prefs.refresh()
        enable_default_folder = prefs.get('enable_default_export_folder', False)
        default_folder = prefs.get('default_export_folder', '')
        logger.info(f"[Multi-AI Export] 读取导出配置 - enable: {enable_default_folder}, folder: {default_folder}")
        
        # 决定文件路径
        if enable_default_folder and default_folder:
            import os
            file_path = os.path.join(default_folder, default_filename)
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                self.i18n.get('export_pdf_dialog_title', 'Export to PDF'),
                default_filename,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
        
        try:
            printer = QPrinter()
            printer.setOutputFileName(file_path)
            
            # 构建内容（多AI模式）
            from calibre_plugins.ask_ai_plugin.config import get_prefs
            separator = "────"
            content_parts = []
            
            # 1. 书籍元数据
            if hasattr(self.parent_dialog, 'book_metadata') and self.parent_dialog.book_metadata:
                book_metadata = self.parent_dialog.book_metadata
                content_parts.append(self.i18n.get('pdf_book_metadata', 'BOOK METADATA'))
                content_parts.append(separator)
                
                if book_metadata.get('title'):
                    content_parts.append(f"{self.i18n.get('metadata_title', 'Title')}: {book_metadata['title']}")
                if book_metadata.get('authors'):
                    authors = ', '.join(book_metadata['authors']) if isinstance(book_metadata['authors'], list) else str(book_metadata['authors'])
                    content_parts.append(f"{self.i18n.get('metadata_authors', 'Authors')}: {authors}")
                if book_metadata.get('publisher'):
                    content_parts.append(f"{self.i18n.get('metadata_publisher', 'Publisher')}: {book_metadata['publisher']}")
                if book_metadata.get('pubdate'):
                    content_parts.append(f"{self.i18n.get('metadata_pubdate', 'Publication Date')}: {book_metadata['pubdate']}")
                if book_metadata.get('languages'):
                    langs = ', '.join(book_metadata['languages']) if isinstance(book_metadata['languages'], list) else str(book_metadata['languages'])
                    content_parts.append(f"{self.i18n.get('metadata_language', 'Languages')}: {langs}")
                
                content_parts.append("")
                content_parts.append("")
            
            # 2. 问题
            content_parts.append(self.i18n.get('pdf_question', 'QUESTION'))
            content_parts.append(separator)
            content_parts.append(question if question else self.i18n.get('no_question', 'No question'))
            content_parts.append("")
            content_parts.append("")
            
            # 3. 所有AI的回答（包含模型信息）
            prefs = get_prefs()
            models_config = prefs.get('models', {})
            
            for i, panel in enumerate(panels):
                response = panel.response_area.toPlainText().strip()
                if not response:
                    continue
                
                # AI信息
                ai_id = panel.get_selected_ai() or "unknown"
                model_config = models_config.get(ai_id, {})
                ai_display_name = model_config.get('display_name', ai_id)
                
                content_parts.append(f"{self.i18n.get('pdf_answer', 'ANSWER')} {i + 1} ({ai_display_name})")
                content_parts.append(separator)
                content_parts.append(response)
                content_parts.append("")
                content_parts.append("")
                
                # 添加该AI的模型信息
                content_parts.append(f"{self.i18n.get('pdf_model_info', 'AI MODEL INFORMATION')} {i + 1}")
                content_parts.append(separator)
                if model_config.get('display_name'):
                    content_parts.append(f"{self.i18n.get('model_provider', 'Provider')}: {model_config['display_name']}")
                if model_config.get('model'):
                    content_parts.append(f"{self.i18n.get('model_name', 'Model')}: {model_config['model']}")
                if model_config.get('api_base_url'):
                    content_parts.append(f"{self.i18n.get('model_api_url', 'API Base URL')}: {model_config['api_base_url']}")
                content_parts.append("")
                content_parts.append("")
            
            # 4. 生成信息
            content_parts.append(self.i18n.get('pdf_generated_by', 'GENERATED BY'))
            content_parts.append(separator)
            content_parts.append(f"{self.i18n.get('pdf_plugin', 'Plugin')}: Ask AI Plugin (calibre Plugin)")
            content_parts.append(f"GitHub: https://github.com/sheldonrrr/ask_grok")
            content_parts.append(f"{self.i18n.get('pdf_software', 'Software')}: calibre E-book Manager (https://calibre-ebook.com)")
            content_parts.append(f"{self.i18n.get('pdf_generated_time', 'Generated Time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            content = '\n'.join(content_parts)
            
            # 打印到PDF
            doc = QTextDocument()
            doc.setPlainText(content)
            doc.print(printer)
            
            logger.info(f"多AI问答PDF导出成功: {file_path}")
            self._show_copy_tooltip(self.export_btn, self.i18n.get('pdf_exported', 'PDF Exported!'))
            
        except Exception as e:
            logger.error(f"导出多AI问答PDF失败: {str(e)}", exc_info=True)
            QMessageBox.warning(
                self,
                self.i18n.get('error', 'Error'),
                self.i18n.get('export_pdf_error', 'Failed to export PDF: {0}').format(str(e))
            )
    
    def export_to_pdf(self):
        """导出当前面板的问答为PDF文件"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from PyQt5.QtPrintSupport import QPrinter
        from PyQt5.QtGui import QTextDocument
        from datetime import datetime
        
        logger.info(f"面板 {self.panel_index} 开始导出PDF")
        
        # 从父对话框获取问题
        question = ""
        if hasattr(self.parent_dialog, 'input_area') and self.parent_dialog.input_area:
            question = self.parent_dialog.input_area.toPlainText().strip()
        
        # 获取当前面板的响应
        response = self.response_area.toPlainText().strip()
        
        if not question and not response:
            logger.warning(f"面板 {self.panel_index} 没有内容可导出")
            return
        
        # 生成默认文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        ai_name = self.get_selected_ai() or "Unknown"
        # 获取AI显示名称（带正确大小写）
        ai_display_name = self._get_ai_display_name(ai_name)
        # 获取书名
        book_title = ""
        if hasattr(self.parent_dialog, 'books_info') and self.parent_dialog.books_info:
            book_title = self.parent_dialog.books_info[0].title
            # 清理文件名中的非法字符
            book_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
            book_title = f"_{book_title}" if book_title else ""
        default_filename = f"{ai_display_name}_QA{book_title}_{timestamp}.pdf"
        
        # 检查是否启用默认导出文件夹（强制重新加载最新配置）
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        # 强制刷新配置以获取最新值
        if hasattr(prefs, 'refresh'):
            prefs.refresh()
        enable_default_folder = prefs.get('enable_default_export_folder', False)
        default_folder = prefs.get('default_export_folder', '')
        logger.info(f"[Panel {self.panel_index} Export] 读取导出配置 - enable: {enable_default_folder}, folder: {default_folder}")
        
        # 决定文件路径
        if enable_default_folder and default_folder:
            # 直接导出到默认文件夹
            import os
            file_path = os.path.join(default_folder, default_filename)
        else:
            # 打开文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                self.i18n.get('export_pdf_dialog_title', 'Export to PDF'),
                default_filename,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
        
        try:
            # 创建打印机对象
            printer = QPrinter()
            printer.setOutputFileName(file_path)
            
            # 使用统一的格式化函数
            content = self._format_qa_content(question, response, include_metadata=True, include_model_info=True)
            
            # 使用QTextDocument打印
            doc = QTextDocument()
            doc.setPlainText(content)
            doc.print(printer)
            
            logger.info(f"面板 {self.panel_index} PDF导出成功: {file_path}")
            
            # 显示成功提示
            success_msg = self.i18n.get('pdf_exported', 'PDF Exported!')
            self._show_copy_tooltip(self.export_btn, success_msg)
            
        except Exception as e:
            logger.error(f"面板 {self.panel_index} 导出PDF失败: {str(e)}", exc_info=True)
            error_msg = self.i18n.get('export_pdf_error', 'Failed to export PDF: {0}').format(str(e))
            QMessageBox.warning(
                self,
                self.i18n.get('error', 'Error'),
                error_msg
            )
    
    def update_export_all_button_state(self):
        """更新导出历史记录按钮的状态（仅当export_mode为'history'时调用）"""
        if not hasattr(self, 'export_btn'):
            return
        
        # 只有在导出模式为'history'时才更新按钮状态
        if self.export_mode != 'history':
            return
        
        # 获取当前书籍的历史记录数量
        history_count = 0
        if hasattr(self.parent_dialog, 'books_info') and hasattr(self.parent_dialog, 'response_handler'):
            if hasattr(self.parent_dialog.response_handler, 'history_manager'):
                book_ids = [book.id for book in self.parent_dialog.books_info]
                all_histories = self.parent_dialog.response_handler.history_manager.get_related_histories(book_ids)
                history_count = len(all_histories)
        
        # 历史记录>=1条时启用按钮
        self.export_btn.setEnabled(history_count >= 1)
    
    def export_all_history_to_pdf(self):
        """导出当前书籍的所有历史记录为单个PDF文件"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        from PyQt5.QtPrintSupport import QPrinter
        from PyQt5.QtGui import QTextDocument
        from datetime import datetime
        import re
        
        logger.info(f"面板 {self.panel_index} 开始导出全部历史记录PDF")
        
        # 获取当前书籍的所有历史记录
        if not hasattr(self.parent_dialog, 'books_info') or not hasattr(self.parent_dialog, 'response_handler'):
            logger.warning("无法获取父对话框信息")
            return
        
        if not hasattr(self.parent_dialog.response_handler, 'history_manager'):
            logger.warning("无法获取历史记录管理器")
            return
        
        book_ids = [book.id for book in self.parent_dialog.books_info]
        all_histories = self.parent_dialog.response_handler.history_manager.get_related_histories(book_ids)
        
        if len(all_histories) < 1:
            logger.warning(f"历史记录数量不足: {len(all_histories)}")
            QMessageBox.information(
                self,
                self.i18n.get('info', 'Information'),
                self.i18n.get('export_history_insufficient', 'Need at least 1 history record to export.')
            )
            return
        
        # 生成默认文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        book_title = self.parent_dialog.books_info[0].title if self.parent_dialog.books_info else "Unknown"
        # 清理文件名中的非法字符
        safe_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
        default_filename = f"History_{safe_title}_{timestamp}.pdf"
        
        # 检查是否启用默认导出文件夹（强制重新加载最新配置）
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        # 强制刷新配置以获取最新值
        if hasattr(prefs, 'refresh'):
            prefs.refresh()
        enable_default_folder = prefs.get('enable_default_export_folder', False)
        default_folder = prefs.get('default_export_folder', '')
        logger.info(f"[History Export] 读取导出配置 - enable: {enable_default_folder}, folder: {default_folder}")
        
        # 决定文件路径
        if enable_default_folder and default_folder:
            # 直接导出到默认文件夹
            import os
            file_path = os.path.join(default_folder, default_filename)
        else:
            # 打开文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                self.i18n.get('export_all_history_dialog_title', 'Export All History to PDF'),
                default_filename,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
        
        try:
            # 创建打印机对象
            printer = QPrinter()
            printer.setOutputFileName(file_path)
            
            # 构建完整内容
            content_parts = []
            separator = "────"
            
            # 1. 添加标题
            content_parts.append(separator)
            content_parts.append(self.i18n.get('export_all_history_title', 'ALL Q&A HISTORY'))
            content_parts.append(separator)
            content_parts.append("")
            
            # 2. 添加完整的书籍元数据信息（与导出当前问答一致）
            if hasattr(self.parent_dialog, 'book_metadata') and self.parent_dialog.book_metadata:
                book_metadata = self.parent_dialog.book_metadata
                content_parts.append(separator)
                content_parts.append(self.i18n.get('pdf_book_metadata', 'BOOK METADATA'))
                content_parts.append(separator)
                
                if book_metadata.get('title'):
                    title_label = self.i18n.get('metadata_title', 'Title')
                    content_parts.append(f"{title_label}: {book_metadata['title']}")
                
                if book_metadata.get('authors'):
                    authors = ', '.join(book_metadata['authors']) if isinstance(book_metadata['authors'], list) else str(book_metadata['authors'])
                    authors_label = self.i18n.get('metadata_authors', 'Authors')
                    content_parts.append(f"{authors_label}: {authors}")
                
                if book_metadata.get('publisher'):
                    publisher_label = self.i18n.get('metadata_publisher', 'Publisher')
                    content_parts.append(f"{publisher_label}: {book_metadata['publisher']}")
                
                if book_metadata.get('pubdate'):
                    pubdate = str(book_metadata['pubdate'])
                    # 只保留年月，去掉详细时间
                    if 'T' in pubdate:
                        pubdate = pubdate.split('T')[0]
                    if len(pubdate) > 7:
                        pubdate = pubdate[:7]
                    pubdate_label = self.i18n.get('metadata_pubyear', 'Publication Date')
                    content_parts.append(f"{pubdate_label}: {pubdate}")
                
                if book_metadata.get('languages'):
                    languages = ', '.join(book_metadata['languages']) if isinstance(book_metadata['languages'], list) else str(book_metadata['languages'])
                    languages_label = self.i18n.get('metadata_language', 'Languages')
                    content_parts.append(f"{languages_label}: {languages}")
                
                content_parts.append("")
            
            # 3. 添加每条历史记录
            for idx, history in enumerate(all_histories, 1):
                content_parts.append(separator)
                content_parts.append(f"{self.i18n.get('history_record', 'Record')} #{idx} - {history['timestamp']}")
                content_parts.append(separator)
                content_parts.append("")
                
                # 问题
                question_label = self.i18n.get('question_label', 'Question')
                content_parts.append(f"{question_label}:")
                question_text = history.get('question', self.i18n.get('no_question', 'No question'))
                content_parts.append(question_text)
                content_parts.append("")
                
                # 所有AI的回答
                answers = history.get('answers', {})
                if answers:
                    answer_label = self.i18n.get('answer_label', 'Answer')
                    for ai_id, answer_data in answers.items():
                        # 获取模型信息（只获取一次）
                        model_info = answer_data.get('model_info', {})
                        
                        # AI模型标识 - 优先使用model_info中的provider_name（有正确大小写）
                        if model_info and model_info.get('provider_name'):
                            ai_display = model_info.get('provider_name')
                        elif ai_id != 'default':
                            # 将ai_id首字母大写，使其更规范
                            ai_display = ai_id.capitalize() if ai_id else 'Unknown'
                        else:
                            ai_display = self.i18n.get('default_ai', 'Default AI')
                        
                        content_parts.append(f"{answer_label} ({ai_display}):")
                        content_parts.append("-" * 40)
                        
                        # 获取回答并去除Markdown格式
                        answer_text = answer_data.get('answer', self.i18n.get('no_response', 'No response'))
                        # 去除Markdown格式：标题、粗体、斜体、代码块等
                        answer_text = re.sub(r'#{1,6}\s+', '', answer_text)  # 去除标题
                        answer_text = re.sub(r'\*\*(.+?)\*\*', r'\1', answer_text)  # 去除粗体
                        answer_text = re.sub(r'\*(.+?)\*', r'\1', answer_text)  # 去除斜体
                        answer_text = re.sub(r'`(.+?)`', r'\1', answer_text)  # 去除行内代码
                        answer_text = re.sub(r'```[\s\S]*?```', '', answer_text)  # 去除代码块
                        answer_text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', answer_text)  # 去除链接，保留文本
                        
                        content_parts.append(answer_text)
                        content_parts.append("")
                        
                        # 添加该回答的AI模型信息
                        content_parts.append(f"[{self.i18n.get('pdf_ai_model_info', 'AI MODEL')}]")
                        
                        # 使用之前获取的model_info（第628行）
                        if model_info:
                            provider = model_info.get('provider_name', ai_display)
                            model_name = model_info.get('model', '')
                            api_base = model_info.get('api_base', '')
                            
                            provider_label = self.i18n.get('pdf_provider', 'Provider')
                            model_label = self.i18n.get('pdf_model', 'Model')
                            
                            content_parts.append(f"  {provider_label}: {provider}")
                            if model_name:
                                content_parts.append(f"  {model_label}: {model_name}")
                            if api_base:
                                api_url_label = self.i18n.get('pdf_api_base_url', 'API Base URL')
                                content_parts.append(f"  {api_url_label}: {api_base}")
                        else:
                            # 向后兼容：如果没有model_info，只显示AI提供商名称（已经首字母大写）
                            content_parts.append(f"  {self.i18n.get('pdf_provider', 'Provider')}: {ai_display}")
                        
                        answer_timestamp = answer_data.get('timestamp', '')
                        if answer_timestamp:
                            content_parts.append(f"  {self.i18n.get('pdf_generated_time', 'Time')}: {answer_timestamp}")
                        content_parts.append("")
                else:
                    content_parts.append(self.i18n.get('no_response', 'No response'))
                    content_parts.append("")
            
            # 4. 添加生成信息（与导出当前问答一致）
            content_parts.append("")
            content_parts.append(separator)
            content_parts.append(self.i18n.get('pdf_generated_by', 'GENERATED BY'))
            content_parts.append(separator)
            plugin_label = self.i18n.get('pdf_plugin', 'Plugin')
            github_label = self.i18n.get('pdf_github', 'GitHub')
            software_label = self.i18n.get('pdf_software', 'Software')
            time_label = self.i18n.get('pdf_generated_time', 'Generated Time')
            total_records_label = self.i18n.get('total_records', 'Total Records')
            content_parts.append(f"{plugin_label}: Ask AI Plugin (calibre Plugin)")
            content_parts.append(f"{github_label}: https://github.com/sheldonrrr/ask_grok")
            content_parts.append(f"{software_label}: calibre E-book Manager (https://calibre-ebook.com)")
            content_parts.append(f"{time_label}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            content_parts.append(f"{total_records_label}: {len(all_histories)}")
            content_parts.append(separator)
            
            # 合并内容并导出
            content = "\n".join(content_parts)
            doc = QTextDocument()
            doc.setPlainText(content)
            doc.print(printer)
            
            logger.info(f"全部历史记录PDF导出成功: {file_path}, 共 {len(all_histories)} 条记录")
            
            # 显示成功提示
            success_msg = self.i18n.get('pdf_exported', 'PDF Exported!')
            self._show_copy_tooltip(self.export_btn, success_msg)
            
        except Exception as e:
            logger.error(f"导出全部历史记录PDF失败: {str(e)}", exc_info=True)
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
    
    def clear_response(self):
        """清空响应区域"""
        self.response_area.clear()
        # 同时隐藏历史信息栏（如果存在）
        self.hide_history_info()
    
    def update_button_states(self):
        """根据当前内容更新按钮状态"""
        # 获取当前的问题和回答
        # 检查纯文本内容或 HTML 内容（因为 setHtml 后 toPlainText 可能需要时间更新）
        plain_text = self.response_area.toPlainText().strip()
        has_response = bool(plain_text)
        has_question = bool(self.current_question.strip()) if hasattr(self, 'current_question') and self.current_question else False

        # 复制按钮：根据复制模式决定是否启用
        if self.copy_mode == 'response':
            # 复制回答模式：只有有回答时才启用
            should_enable = has_response
        else:  # 'qa'
            # 复制问答模式：只要有问题就启用（即使没有回答）
            should_enable = has_question

        self.copy_btn.setEnabled(should_enable)

        # 导出按钮：支持两种模式
        # 注意：多AI模式下，非最后一个面板没有导出按钮
        if hasattr(self, 'export_btn') and self.export_btn is not None:
            from calibre_plugins.ask_ai_plugin.config import get_prefs
            prefs = get_prefs()
            parallel_ai_count = prefs.get('parallel_ai_count', 1)

            # 导出按钮始终启用（简化逻辑，无论单AI还是多AI模式）
            # 导出时如果内容为空，会有相应的提示或处理
            self.export_btn.setEnabled(True)

            # 菜单项也始终启用
            if hasattr(self, 'export_current_action'):
                self.export_current_action.setEnabled(True)
            if hasattr(self, 'export_history_action'):
                self.export_history_action.setEnabled(True)

    def set_current_question(self, question):
        """设置当前问题（用于按钮状态判断）"""
        self.current_question = question
        self.update_button_states()
    
    def show_history_info(self, ai_id, timestamp, ai_available=True):
        """显示历史记录信息栏
        
        Args:
            ai_id: 历史记录使用的AI ID
            timestamp: 历史记录时间戳
            ai_available: 该AI是否仍然可用
        """
        from PyQt5.QtWidgets import QLabel
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        from calibre_plugins.ask_ai_plugin.ui_constants import SPACING_TINY
        from calibre_plugins.ask_ai_plugin.api import APIClient
        from calibre_plugins.ask_ai_plugin.models.base import DEFAULT_MODELS
        
        # 如果已存在信息栏，先移除
        if self.history_info_bar:
            self.hide_history_info()
        
        # 创建信息栏（使用简单的QLabel）
        self.history_info_bar = QLabel()
        
        # 获取AI的完整显示名称（包含模型信息）
        prefs = get_prefs()
        ai_configs = prefs.get('ai_configs', {})
        
        # 先尝试从配置中获取
        if ai_id in ai_configs:
            config = ai_configs[ai_id]
            display_name = config.get('display_name', ai_id)
            model_name = config.get('model', '')
            if model_name:
                ai_full_display = f"{display_name} - {model_name}"
            else:
                ai_full_display = display_name
        else:
            # AI 配置不存在，尝试从 DEFAULT_MODELS 获取显示名称
            ai_provider = APIClient._MODEL_TO_PROVIDER.get(ai_id)
            if ai_provider and ai_provider in DEFAULT_MODELS:
                display_name = DEFAULT_MODELS[ai_provider].display_name
                # 尝试获取模型名称
                model_name = ai_id if ai_id != 'default' else ''
                if model_name:
                    ai_full_display = f"{display_name} - {model_name}"
                else:
                    ai_full_display = display_name
            else:
                # 完全找不到，使用 ai_id
                ai_full_display = ai_id
        
        # 构建提示文本
        if ai_available:
            info_text = f"{ai_full_display} | 生成于: {timestamp}"
        else:
            info_text = f"{ai_full_display} (已移除) | 生成于: {timestamp}"
        
        self.history_info_bar.setText(info_text)
        self.history_info_bar.setStyleSheet(f"""
            QLabel {{
                color: palette(dark);
                font-size: 0.85em;
                padding: 0px;
                margin-top: {SPACING_TINY}px;
                margin-bottom: 0px;
            }}
        """)
        
        # 将信息栏插入到响应区域和按钮栏之间
        main_layout = self.layout()
        # 找到response_area的位置
        response_area_index = -1
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if item.widget() == self.response_area:
                response_area_index = i
                break
        
        # 插入到响应区域的下一个位置（即按钮栏之前）
        if response_area_index >= 0:
            main_layout.insertWidget(response_area_index + 1, self.history_info_bar)
    
    def hide_history_info(self):
        """隐藏并移除历史记录信息栏"""
        if self.history_info_bar:
            self.history_info_bar.setParent(None)
            self.history_info_bar.deleteLater()
            self.history_info_bar = None
    
    def _on_anchor_clicked(self, url):
        """处理链接点击事件
        
        支持的链接格式：
        - calibre://book/BOOK_ID - 在Calibre中打开书籍
        - http://... 或 https://... - 在浏览器中打开外部链接
        """
        from PyQt5.QtCore import QUrl
        from PyQt5.QtGui import QDesktopServices
        
        url_str = url.toString()
        logger.info("="*80)
        logger.info(f"[BOOK_LINK_CLICK] 链接被点击: {url_str}")
        logger.info(f"[BOOK_LINK_CLICK] 父对话框状态: visible={self.parent_dialog.isVisible()}, modal={self.parent_dialog.isModal()}")
        logger.info(f"[BOOK_LINK_CLICK] 响应区域内容长度: {len(self.response_area.toPlainText())}")
        
        try:
            if url_str.startswith('calibre://book/'):
                # 提取书籍ID
                book_id_str = url_str.replace('calibre://book/', '')
                book_id = int(book_id_str)
                logger.info(f"[BOOK_LINK_CLICK] 提取书籍 ID: {book_id}")
                
                # 使用Calibre的正确API打开书籍
                if hasattr(self.parent_dialog, 'gui') and self.parent_dialog.gui:
                    gui = self.parent_dialog.gui
                    logger.info(f"[BOOK_LINK_CLICK] GUI 实例可用")
                    logger.info(f"[BOOK_LINK_CLICK] 当前库视图选择: {gui.library_view.selectionModel().selectedRows()}")
                    
                    # 直接使用EbookViewer打开书籍，不改变库视图选择
                    # 这样可以避免触发show_dialog()，保持AI Search对话框内容
                    try:
                        from calibre.gui2.viewer.main import EbookViewer
                        logger.info(f"[BOOK_LINK_CLICK] 导入 EbookViewer 成功")
                        
                        db = gui.current_db
                        fmt = db.formats(book_id, index_is_id=True)
                        logger.info(f"[BOOK_LINK_CLICK] 书籍格式: {fmt}")
                        
                        if fmt:
                            fmt = fmt.split(',')[0].lower()
                            path = db.format_abspath(book_id, fmt, index_is_id=True)
                            logger.info(f"[BOOK_LINK_CLICK] 书籍路径: {path}")
                            
                            if path:
                                print(f"[BOOK_LINK_CLICK] 准备打开书籍")
                                print(f"[BOOK_LINK_CLICK] 打开前对话框状态: visible={self.parent_dialog.isVisible()}")
                                logger.info(f"[BOOK_LINK_CLICK] 准备打开书籍")
                                logger.info(f"[BOOK_LINK_CLICK] 打开前对话框状态: visible={self.parent_dialog.isVisible()}")
                                
                                # 使用Calibre的View action来打开书籍，但通过直接调用view_book方法
                                # 这样可以避免改变库视图选择，同时避免EbookViewer直接实例化导致的崩溃
                                if 'View' in gui.iactions:
                                    view_action = gui.iactions['View']
                                    # 使用内部方法直接打开书籍，传入book_id
                                    try:
                                        # view_book方法需要book_id作为参数
                                        view_action._view_calibre_books([book_id])
                                        logger.info(f"[BOOK_LINK_CLICK] 使用View action打开书籍成功")
                                    except AttributeError:
                                        # 如果_view_calibre_books不存在，尝试其他方法
                                        # 临时选中书籍，打开后立即恢复选择
                                        old_selection = [gui.library_view.model().id(row) for row in gui.library_view.selectionModel().selectedRows()]
                                        gui.library_view.select_rows([book_id])
                                        view_action.qaction.trigger()
                                        # 恢复原来的选择（如果是AI Search模式，原来没有选择）
                                        if old_selection:
                                            gui.library_view.select_rows(old_selection)
                                        else:
                                            gui.library_view.selectionModel().clear()
                                        logger.info(f"[BOOK_LINK_CLICK] 使用View action trigger打开书籍成功")
                                else:
                                    logger.error(f"[BOOK_LINK_CLICK] View action不可用")
                            
                                # 使用QTimer延迟检查，因为对话框可能在稍后被关闭
                                from PyQt5.QtCore import QTimer
                                def check_dialog_state():
                                    print(f"[BOOK_LINK_CLICK] 打开后对话框状态: visible={self.parent_dialog.isVisible()}")
                                    print(f"[BOOK_LINK_CLICK] 打开后响应区域内容长度: {len(self.response_area.toPlainText())}")
                                    print(f"[BOOK_LINK_CLICK] 对话框是否被关闭: {self.parent_dialog.isHidden()}")
                                    print(f"[BOOK_LINK_CLICK] 成功打开书籍: {path}")
                                    print("="*80)
                                
                                # 立即检查
                                check_dialog_state()
                                # 1秒后再检查一次
                                QTimer.singleShot(1000, check_dialog_state)
                            else:
                                logger.error(f"[BOOK_LINK_CLICK] 找不到书籍文件路径")
                        else:
                            logger.error(f"[BOOK_LINK_CLICK] 书籍 {book_id} 没有可用格式")
                    except Exception as e:
                        logger.error(f"[BOOK_LINK_CLICK] 打开书籍失败: {str(e)}", exc_info=True)
                else:
                    logger.warning("[BOOK_LINK_CLICK] GUI 实例不可用")
            elif url_str.startswith('http://') or url_str.startswith('https://'):
                # 外部链接，在浏览器中打开
                QDesktopServices.openUrl(url)
                logger.info(f"在浏览器中打开: {url_str}")
            else:
                logger.warning(f"[BOOK_LINK_CLICK] 未知的链接格式: {url_str}")
        except Exception as e:
            logger.error(f"[BOOK_LINK_CLICK] 处理链接点击时出错: {str(e)}", exc_info=True)
        finally:
            logger.info(f"[BOOK_LINK_CLICK] _on_anchor_clicked 执行完成")
            logger.info("="*80)
