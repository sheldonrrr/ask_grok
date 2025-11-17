#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
响应面板组件 - 用于多AI并行请求功能
每个面板包含：AI选择器、响应区域、操作按钮
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextBrowser, QPushButton, QSizePolicy)
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
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI布局"""
        # 主布局：垂直
        main_layout = QVBoxLayout(self)
        # 使用紧凑间距，让AI回复区域更大
        from .ui_constants import SPACING_ASK_COMPACT
        main_layout.setContentsMargins(0, 0, 0, SPACING_ASK_COMPACT)  # 上边距0，下边距4px
        main_layout.setSpacing(SPACING_ASK_COMPACT)  # 内部元素间距4px
        
        # === Header 区域（横向） ===
        # 只有当 show_ai_switcher 为 True 时才显示 header
        if self.show_ai_switcher:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(SPACING_SMALL)
            
            # AI切换器（直接显示模型名称，不需要"AI 1:"标签）
            from .ui_constants import BUTTON_HEIGHT
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
            from .ui_constants import BUTTON_HEIGHT
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
        self.response_area.setOpenExternalLinks(True)
        self.response_area.setMinimumHeight(200)
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
        """)
        
        main_layout.addWidget(self.response_area, stretch=1)  # stretch=1 让它占据剩余空间
        
        # === Button Bar（操作按钮 - 紧凑布局） ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SPACING_SMALL)
        
        # 使用更紧凑的按钮宽度
        self.copy_btn = QPushButton(self.i18n.get('copy_response', 'Copy'))
        apply_button_style(self.copy_btn, min_width=70)
        self.copy_btn.clicked.connect(self.copy_response)
        self.copy_btn.setEnabled(False)  # 默认禁用，收到回复后启用
        
        self.copy_qa_btn = QPushButton(self.i18n.get('copy_question_response', 'Copy Q&A'))
        apply_button_style(self.copy_qa_btn, min_width=90)
        self.copy_qa_btn.clicked.connect(self.copy_question_response)
        self.copy_qa_btn.setEnabled(False)  # 默认禁用，有问题和回答后启用
        
        self.export_btn = QPushButton(self.i18n.get('export_current_qa', 'Export Q&A'))
        apply_button_style(self.export_btn, min_width=100)
        self.export_btn.clicked.connect(self.export_to_pdf)
        self.export_btn.setEnabled(False)  # 默认禁用，有问题和回答后启用
        
        self.export_all_btn = QPushButton(self.i18n.get('export_history', 'Export All'))
        apply_button_style(self.export_all_btn, min_width=90)
        self.export_all_btn.clicked.connect(self.export_all_history_to_pdf)
        self.export_all_btn.setEnabled(False)  # 默认禁用，当历史记录>=2时启用
        
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.copy_qa_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.export_all_btn)
        button_layout.addStretch()
        
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
        
        # 阻止信号触发
        self.ai_switcher.blockSignals(True)
        
        current_ai = self.ai_switcher.currentData()
        self.ai_switcher.clear()
        
        # 添加一个空选项（用于留空）
        self.ai_switcher.addItem(
            self.i18n.get('select_ai', '-- Select AI --'),
            None
        )
        
        # 检查是否有可用的AI
        available_ais = [(ai_id, name) for ai_id, name in configured_ais if ai_id not in used_ais or ai_id == current_ai]
        
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
    
    def send_request(self, prompt, model_id=None):
        """发送请求到选中的AI
        
        Args:
            prompt: 提示词
            model_id: 可选，指定使用的模型ID。如果为None，使用当前选中的AI
        """
        if not self.response_handler:
            logger.error(f"面板 {self.panel_index} 的 ResponseHandler 未初始化")
            return
        
        # 使用指定的model_id或当前选中的AI
        target_model_id = model_id if model_id else self.get_selected_ai()
        
        if not target_model_id:
            logger.warning(f"面板 {self.panel_index} 没有选中的AI")
            return
        
        logger.info(f"[面板 {self.panel_index}] 开始请求 AI: {target_model_id}")
        self.request_started.emit(self.panel_index)
        
        # 更新响应处理器的AI标识符（用于历史记录）
        self.response_handler.ai_id = target_model_id
        logger.info(f"[面板 {self.panel_index}] 已设置 ai_id={target_model_id} 用于历史记录")
        
        # 调用响应处理器发送请求，传递model_id参数
        self.response_handler.start_async_request(prompt, model_id=target_model_id)
        logger.info(f"[面板 {self.panel_index}] 异步请求已启动")
    
    def get_response_text(self):
        """获取响应文本
        
        Returns:
            str: 响应文本
        """
        return self.response_area.toPlainText()
    
    def copy_response(self):
        """复制响应内容到剪贴板"""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        response_text = self.response_area.toPlainText()
        if response_text.strip():
            clipboard.setText(response_text)
            self._show_copy_tooltip(self.copy_btn, self.i18n.get('copied', 'Copied!'))
    
    def copy_question_response(self):
        """复制问题和响应内容到剪贴板"""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        
        # 从父对话框获取问题
        question = ""
        if hasattr(self.parent_dialog, 'input_area') and self.parent_dialog.input_area:
            question = self.parent_dialog.input_area.toPlainText().strip()
        
        response = self.response_area.toPlainText().strip()
        
        if not question and not response:
            return
        
        # 组合问题和答案
        text = f"{question}\n\n----\n\n{response}" if question and response else (question or response)
        clipboard.setText(text)
        self._show_copy_tooltip(self.copy_qa_btn, self.i18n.get('copied', 'Copied!'))
    
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
        
        # 生成默认文件名（使用时间戳和面板索引）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ai_name = self.get_selected_ai() or "unknown"
        default_filename = f"ask_ai_qa_{ai_name}_panel{self.panel_index + 1}_{timestamp}.pdf"
        
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
            
            # 构建书籍元数据信息
            separator = "=" * 40
            metadata_lines = []
            
            # 从父对话框获取书籍元数据
            if hasattr(self.parent_dialog, 'book_metadata') and self.parent_dialog.book_metadata:
                book_metadata = self.parent_dialog.book_metadata
                metadata_lines.append(separator)
                metadata_lines.append(self.i18n.get('pdf_book_metadata', 'BOOK METADATA'))
                metadata_lines.append(separator)
                
                if book_metadata.get('title'):
                    title_label = self.i18n.get('metadata_title', 'Title')
                    metadata_lines.append(f"{title_label}: {book_metadata['title']}")
                
                if book_metadata.get('authors'):
                    authors = ', '.join(book_metadata['authors']) if isinstance(book_metadata['authors'], list) else str(book_metadata['authors'])
                    authors_label = self.i18n.get('metadata_authors', 'Authors')
                    metadata_lines.append(f"{authors_label}: {authors}")
                
                if book_metadata.get('publisher'):
                    publisher_label = self.i18n.get('metadata_publisher', 'Publisher')
                    metadata_lines.append(f"{publisher_label}: {book_metadata['publisher']}")
                
                if book_metadata.get('pubdate'):
                    pubdate = str(book_metadata['pubdate'])
                    # 只保留年月，去掉详细时间
                    if 'T' in pubdate:
                        pubdate = pubdate.split('T')[0]
                    if len(pubdate) > 7:
                        pubdate = pubdate[:7]
                    pubdate_label = self.i18n.get('metadata_pubyear', 'Publication Date')
                    metadata_lines.append(f"{pubdate_label}: {pubdate}")
                
                if book_metadata.get('languages'):
                    languages = ', '.join(book_metadata['languages']) if isinstance(book_metadata['languages'], list) else str(book_metadata['languages'])
                    languages_label = self.i18n.get('metadata_language', 'Languages')
                    metadata_lines.append(f"{languages_label}: {languages}")
                
                metadata_lines.append("")
            
            # 获取当前使用的AI模型信息
            model_info_lines = []
            try:
                if hasattr(self, 'api') and self.api:
                    
                    model_info_lines.append("")
                    model_info_lines.append(separator)
                    model_info_lines.append(self.i18n.get('pdf_ai_model_info', 'AI MODEL INFORMATION'))
                    model_info_lines.append(separator)
                    
                    # 使用provider_name属性获取提供商名称
                    provider = getattr(self.api, 'provider_name', 'Unknown')
                    model_name = getattr(self.api, 'model', 'Unknown')
                    api_url = getattr(self.api, 'api_base', '')
                    
                    provider_label = self.i18n.get('pdf_provider', 'Provider')
                    model_label = self.i18n.get('pdf_model', 'Model')
                    api_url_label = self.i18n.get('pdf_api_base_url', 'API Base URL')
                    
                    model_info_lines.append(f"{provider_label}: {provider}")
                    model_info_lines.append(f"{model_label}: {model_name}")
                    if api_url:
                        model_info_lines.append(f"{api_url_label}: {api_url}")
                else:
                    logger.warning(f"面板 {self.panel_index} 没有API对象")
                    info_not_available = self.i18n.get('pdf_info_not_available', 'Information not available')
                    model_info_lines.append(f"{self.i18n.get('pdf_provider', 'Provider')}: {info_not_available}")
            except Exception as e:
                logger.error(f"面板 {self.panel_index} 获取模型信息失败: {str(e)}", exc_info=True)
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
            content_parts.append(f"{plugin_label}: Ask AI Plugin (calibre Plugin)")
            content_parts.append(f"{github_label}: https://github.com/sheldonrrr/ask_grok")
            content_parts.append(f"{software_label}: calibre E-book Manager (https://calibre-ebook.com)")
            content_parts.append(f"{time_label}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            content_parts.append(separator)
            
            content = '\n'.join(content_parts)
            
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
        """更新导出历史记录按钮的状态"""
        if not hasattr(self, 'export_all_btn'):
            return
        
        # 获取当前书籍的历史记录数量
        history_count = 0
        if hasattr(self.parent_dialog, 'books_info') and hasattr(self.parent_dialog, 'response_handler'):
            if hasattr(self.parent_dialog.response_handler, 'history_manager'):
                book_ids = [book.id for book in self.parent_dialog.books_info]
                all_histories = self.parent_dialog.response_handler.history_manager.get_related_histories(book_ids)
                history_count = len(all_histories)
        
        # 历史记录>=1条时启用按钮
        self.export_all_btn.setEnabled(history_count >= 1)
    
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        book_title = self.parent_dialog.books_info[0].title if self.parent_dialog.books_info else "unknown"
        # 清理文件名中的非法字符
        safe_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
        default_filename = f"ask_ai_all_history_{safe_title}_{timestamp}.pdf"
        
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
            separator = "=" * 60
            
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
            self._show_copy_tooltip(self.export_all_btn, success_msg)
            
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
        html_text = self.response_area.toHtml().strip()
        
        # 只要有纯文本或 HTML 内容就认为有回答
        has_response = bool(plain_text) or (bool(html_text) and len(html_text) > 100)  # HTML 长度 > 100 避免空标签
        has_question = bool(self.current_question.strip()) if hasattr(self, 'current_question') and self.current_question else False
        
        # 复制回答按钮：只要有回答就启用
        self.copy_btn.setEnabled(has_response)
        
        # 复制问答按钮：只要有回答就启用（问题可以为空）
        self.copy_qa_btn.setEnabled(has_response)
        
        # 导出当前问答按钮：只要有回答就启用（问题可以为空）
        self.export_btn.setEnabled(has_response)
        
        # 导出历史按钮：独立判断，基于历史记录数量
        self.update_export_all_button_state()
        
    
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
        from .config import get_prefs
        from .ui_constants import SPACING_TINY
        from .api import APIClient
        from .models.base import DEFAULT_MODELS
        
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
