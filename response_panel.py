#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
响应面板组件 - 用于多AI并行请求功能
每个面板包含：AI选择器、响应区域、操作按钮
"""

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QTextBrowser, QPushButton, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal

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
    
    def __init__(self, panel_index, parent, api, i18n):
        """初始化响应面板
        
        Args:
            panel_index: 面板索引（0-3）
            parent: 父窗口
            api: API客户端实例
            i18n: 国际化字典
        """
        super().__init__(parent)
        self.panel_index = panel_index
        self.parent_dialog = parent
        self.api = api
        self.i18n = i18n
        self.response_handler = None  # 将在setup后初始化
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI布局"""
        # 主布局：垂直
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(8)
        
        # === Header 区域（横向） ===
        header_layout = QHBoxLayout()
        
        # AI切换器（直接显示模型名称，不需要"AI 1:"标签）
        self.ai_switcher = QComboBox()
        self.ai_switcher.setMinimumWidth(200)
        self.ai_switcher.currentIndexChanged.connect(self.on_ai_switched)
        # 修复hover时字体消失的问题
        # 完全使用系统默认样式，不自定义 drop-down 和 down-arrow
        self.ai_switcher.setStyleSheet("""
            QComboBox {
                color: palette(text);
                background: palette(base);
                border: 1px solid palette(mid);
                border-radius: 3px;
                padding: 3px 5px;
            }
            QComboBox:hover {
                color: palette(text);
                background: palette(midlight);
                border: 1px solid palette(highlight);
            }
            QComboBox QAbstractItemView {
                color: palette(text);
                background: palette(base);
                selection-color: palette(highlighted-text);
                selection-background-color: palette(highlight);
            }
            QComboBox QAbstractItemView::item {
                color: palette(text);
                padding: 5px;
            }
            QComboBox QAbstractItemView::item:hover {
                color: palette(text);
                background: palette(midlight);
            }
            QComboBox QAbstractItemView::item:selected {
                color: palette(highlighted-text);
                background: palette(highlight);
            }
        """)
        header_layout.addWidget(self.ai_switcher)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
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
        
        # === Button Bar（横向） ===
        button_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton(self.i18n.get('copy_response', 'Copy Response'))
        self.copy_btn.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: transparent;
            }
            QPushButton:hover {
                background: palette(midlight);
            }
        """)
        self.copy_btn.clicked.connect(self.copy_response)
        
        self.copy_qa_btn = QPushButton(self.i18n.get('copy_question_response', 'Copy Q&A'))
        self.copy_qa_btn.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: transparent;
            }
            QPushButton:hover {
                background: palette(midlight);
            }
        """)
        self.copy_qa_btn.clicked.connect(self.copy_question_response)
        
        self.export_btn = QPushButton(self.i18n.get('export_pdf', 'Export PDF'))
        self.export_btn.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                border: 1px solid palette(mid);
                border-radius: 3px;
                background: transparent;
            }
            QPushButton:hover {
                background: palette(midlight);
            }
        """)
        self.export_btn.clicked.connect(self.export_to_pdf)
        
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.copy_qa_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # 设置最小高度，防止按钮覆盖响应区域
        self.setMinimumHeight(350)  # 确保有足够空间显示所有元素
        
        # 添加边框样式（使用QWidget而不是类名）
        self.setStyleSheet("""
            QWidget {
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
            self.ai_changed.emit(self.panel_index, ai_id)
    
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
        if hasattr(self.parent_dialog, 'input_area'):
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
        if hasattr(self.parent_dialog, 'input_area'):
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
            logger.debug(f"面板 {self.panel_index} 用户取消了PDF导出")
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
                    logger.debug(f"面板 {self.panel_index} API对象存在: {self.api}")
                    
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
            content_parts.append(f"{plugin_label}: Ask AI Plugin (Calibre Plugin)")
            content_parts.append(f"{github_label}: https://github.com/sheldonrrr/ask_grok")
            content_parts.append(f"{software_label}: Calibre E-book Manager (https://calibre-ebook.com)")
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
    
    def _show_copy_tooltip(self, button, text):
        """在按钮位置显示复制成功的提示"""
        from PyQt5.QtWidgets import QToolTip
        QToolTip.showText(button.mapToGlobal(button.rect().bottomLeft()), text, button, button.rect(), 2000)
    
    def clear_response(self):
        """清空响应区域"""
        self.response_area.clear()
