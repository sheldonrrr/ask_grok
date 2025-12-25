#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPlainTextEdit, 
                            QPushButton, QHBoxLayout, QGroupBox, QScrollArea, 
                            QSizePolicy, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics

from .i18n import get_default_template, get_suggestion_template, get_multi_book_template
from .ui_constants import (
    SPACING_SMALL, SPACING_LARGE,
    get_groupbox_style, get_section_title_style, get_subtitle_style,
    TEXT_COLOR_SECONDARY_STRONG
)

logger = logging.getLogger(__name__)


class PromptsWidget(QWidget):
    """提示词配置页面"""
    
    # 配置变更信号
    config_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_dialog = parent
        self.i18n = parent.i18n if parent else {}
        self.initial_values = {}
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setObjectName("prompts_scroll")
        
        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(SPACING_LARGE, SPACING_LARGE, SPACING_LARGE, SPACING_LARGE)
        content_layout.setSpacing(SPACING_LARGE)
        content_widget.setLayout(content_layout)
        
        # 添加说明部分
        self.add_explanation_section(content_layout)
        
        # 添加语言偏好设置部分
        self.add_language_preference_section(content_layout)
        
        # 添加提示词模板部分
        self.add_prompts_section(content_layout)
        
        # 添加重置按钮
        self.add_reset_button(content_layout)
        
        # 添加弹性空间
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
    def add_explanation_section(self, parent_layout):
        """添加说明部分"""
        # 创建说明组
        explanation_group = QGroupBox()
        explanation_group.setStyleSheet(get_groupbox_style())
        explanation_layout = QVBoxLayout()
        explanation_layout.setSpacing(SPACING_SMALL)
        
        # 标题
        title = QLabel(self.i18n.get('prompts_explanation_title', 'How Prompts Work'))
        title.setStyleSheet(get_section_title_style())
        title.setObjectName('title_prompts_explanation')
        explanation_layout.addWidget(title)
        
        # 说明文字
        explanation = QLabel(self.i18n.get('prompts_explanation', 
            'When you click Send, the plugin extracts and combines dynamic fields from your prompt template, '
            'then submits them to the AI. The underlying principle is that the AI relies on training data that '
            'includes information about the book, rather than sending the full text of the book to the AI.'))
        explanation.setWordWrap(True)
        explanation.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-size: 1em; padding: 0; margin: 0 0 8px 0;")
        explanation.setObjectName('subtitle_prompts_explanation')
        explanation_layout.addWidget(explanation)
        
        explanation_group.setLayout(explanation_layout)
        parent_layout.addWidget(explanation_group)
        
    def add_language_preference_section(self, parent_layout):
        """添加语言偏好设置部分"""
        from PyQt5.QtWidgets import QCheckBox
        
        # 创建语言偏好组
        lang_pref_group = QGroupBox()
        lang_pref_group.setStyleSheet(get_groupbox_style())
        lang_pref_layout = QVBoxLayout()
        lang_pref_layout.setSpacing(SPACING_SMALL)
        
        # 复选框
        self.use_interface_language_checkbox = QCheckBox(
            self.i18n.get('use_interface_language', 'Always ask AI to respond in current plugin interface language')
        )
        self.use_interface_language_checkbox.setChecked(True)  # 默认勾选
        self.use_interface_language_checkbox.stateChanged.connect(self.on_language_preference_changed)
        lang_pref_layout.addWidget(self.use_interface_language_checkbox)
        
        # 语言指令显示标签
        self.language_instruction_label = QLabel()
        self.language_instruction_label.setWordWrap(True)
        self.language_instruction_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 5px 0;")
        lang_pref_layout.addWidget(self.language_instruction_label)
        
        # 更新语言指令显示
        self.update_language_instruction_display()
        
        lang_pref_group.setLayout(lang_pref_layout)
        parent_layout.addWidget(lang_pref_group)
    
    def add_prompts_section(self, parent_layout):
        """添加提示词模板部分"""
        # 创建提示词组
        prompts_group = QGroupBox()
        prompts_group.setStyleSheet(get_groupbox_style())
        prompts_layout = QVBoxLayout()
        prompts_layout.setSpacing(SPACING_LARGE)
        
        # Ask Prompts
        ask_layout = QVBoxLayout()
        ask_layout.setSpacing(SPACING_SMALL)
        ask_label = QLabel(self.i18n.get('ask_prompts', 'Ask Prompts'))
        ask_label.setObjectName('label_ask_prompts')
        ask_layout.addWidget(ask_label)
        
        self.template_edit = QPlainTextEdit(self)
        self.template_edit.textChanged.connect(self.on_config_changed)
        self.setup_text_edit_height(self.template_edit)
        ask_layout.addWidget(self.template_edit)
        
        prompts_layout.addLayout(ask_layout)
        
        # Random Questions Prompts
        random_layout = QVBoxLayout()
        random_layout.setSpacing(SPACING_SMALL)
        random_label = QLabel(self.i18n.get('random_questions_prompts', 'Random Questions Prompts'))
        random_label.setObjectName('label_random_questions_prompts')
        random_layout.addWidget(random_label)
        
        self.random_questions_edit = QPlainTextEdit(self)
        self.random_questions_edit.textChanged.connect(self.on_config_changed)
        self.setup_text_edit_height(self.random_questions_edit)
        random_layout.addWidget(self.random_questions_edit)
        
        prompts_layout.addLayout(random_layout)
        
        # Multi-Book Template
        multi_layout = QVBoxLayout()
        multi_layout.setSpacing(SPACING_SMALL)
        multi_label = QLabel(self.i18n.get('multi_book_template_label', 'Multi-Book Prompt Template'))
        multi_label.setObjectName('label_multi_book_template')
        multi_layout.addWidget(multi_label)
        
        self.multi_book_template_edit = QPlainTextEdit(self)
        self.multi_book_template_edit.textChanged.connect(self.on_config_changed)
        self.setup_text_edit_height(self.multi_book_template_edit)
        multi_layout.addWidget(self.multi_book_template_edit)
        
        # 添加占位符说明
        placeholder_hint = QLabel(self.i18n.get('multi_book_placeholder_hint', 
            'Use {books_metadata} for book information, {query} for user question'))
        placeholder_hint.setObjectName('label_multi_book_placeholder_hint')
        placeholder_hint.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 5px 0;")
        placeholder_hint.setWordWrap(True)
        multi_layout.addWidget(placeholder_hint)
        
        prompts_layout.addLayout(multi_layout)
        
        prompts_group.setLayout(prompts_layout)
        parent_layout.addWidget(prompts_group)
        
    def setup_text_edit_height(self, text_edit):
        """设置文本编辑框的高度"""
        font_metrics = QFontMetrics(text_edit.font())
        line_height = font_metrics.lineSpacing()
        padding = 10
        five_lines_height = line_height * 5 + padding
        ten_lines_height = line_height * 10 + padding
        
        text_edit.setMinimumHeight(five_lines_height)
        text_edit.setMaximumHeight(ten_lines_height)
        text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
    def add_reset_button(self, parent_layout):
        """添加重置按钮"""
        reset_layout = QHBoxLayout()
        reset_layout.addStretch()
        
        reset_button = QPushButton(self.i18n.get('reset_prompts', 'Reset Prompts to Default'))
        reset_button.setObjectName('button_reset_prompts')
        reset_button.clicked.connect(self.on_reset_prompts)
        reset_layout.addWidget(reset_button)
        
        parent_layout.addLayout(reset_layout)
        
    def on_config_changed(self):
        """配置变更时触发"""
        self.config_changed.emit()
    
    def on_language_preference_changed(self):
        """语言偏好变更时触发"""
        self.update_language_instruction_display()
        # 更新提示词模板中的语言指令
        self.update_prompts_with_language_instruction()
        self.on_config_changed()
    
    def get_language_instruction_text(self):
        """获取语言指令文本"""
        if not self.use_interface_language_checkbox.isChecked():
            return ""
        
        # 获取当前语言名称
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        from .i18n import get_all_languages
        all_languages = get_all_languages()
        
        if current_lang in all_languages:
            language_name = all_languages[current_lang]
        else:
            language_name = "English"
        
        # 生成语言指令
        instruction_template = self.i18n.get('language_instruction_text', 'Please respond in {language_name}.')
        instruction_text = instruction_template.format(language_name=language_name)
        
        return f"\n\n{instruction_text}"
    
    def remove_language_instruction(self, text):
        """从文本中移除语言指令"""
        if not text:
            return text
            
        # 移除所有可能的语言指令格式
        lines = text.split('\n')
        
        # 获取所有支持语言的语言指令文本（使用 i18n key）
        from .i18n import get_all_languages
        all_languages = get_all_languages()
        
        # 生成所有可能的语言指令文本
        possible_instructions = set()
        for lang_code, lang_name in all_languages.items():
            # 临时切换到该语言获取翻译
            from .i18n import get_translation
            temp_i18n = get_translation(lang_code)
            instruction_template = temp_i18n.get('language_instruction_text', '')
            if instruction_template:
                instruction_text = instruction_template.format(language_name=lang_name)
                possible_instructions.add(instruction_text.strip())
        
        # 从末尾开始检查，移除空行和语言指令
        while lines:
            last_line = lines[-1].strip()
            
            # 如果是空行，移除
            if not last_line:
                lines.pop()
                continue
            
            # 检查是否是语言指令（通过匹配所有可能的语言指令）
            if last_line in possible_instructions:
                lines.pop()
            else:
                break
        
        return '\n'.join(lines)
    
    def update_prompts_with_language_instruction(self):
        """更新所有提示词模板，添加或移除语言指令"""
        language_instruction = self.get_language_instruction_text()
        
        # 更新 Ask Prompts
        current_template = self.template_edit.toPlainText()
        clean_template = self.remove_language_instruction(current_template)
        self.template_edit.setPlainText(clean_template + language_instruction)
        
        # 更新 Random Questions
        current_random = self.random_questions_edit.toPlainText()
        clean_random = self.remove_language_instruction(current_random)
        self.random_questions_edit.setPlainText(clean_random + language_instruction)
        
        # 更新 Multi-Book Template
        current_multi = self.multi_book_template_edit.toPlainText()
        clean_multi = self.remove_language_instruction(current_multi)
        self.multi_book_template_edit.setPlainText(clean_multi + language_instruction)
    
    def update_language_instruction_display(self):
        """更新语言指令显示"""
        if not hasattr(self, 'language_instruction_label'):
            return
        
        if self.use_interface_language_checkbox.isChecked():
            # 获取当前语言名称
            current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
            from .i18n import get_all_languages
            all_languages = get_all_languages()
            
            # get_all_languages() 返回 {code: name} 格式，直接使用名称
            if current_lang in all_languages:
                language_name = all_languages[current_lang]
            else:
                language_name = "English"
            
            # 显示语言指令
            instruction_template = self.i18n.get('language_instruction_text', 'Please respond in {language_name}.')
            instruction_text = instruction_template.format(language_name=language_name)
            
            label_text = self.i18n.get('language_instruction_label', 'Language instruction added to prompts:')
            self.language_instruction_label.setText(f"{label_text} {instruction_text}")
            self.language_instruction_label.show()
        else:
            self.language_instruction_label.hide()
        
    def on_reset_prompts(self):
        """重置提示词"""
        reply = QMessageBox.question(
            self,
            self.i18n.get('reset_prompts', 'Reset Prompts to Default'),
            self.i18n.get('reset_prompts_confirm', 
                'Are you sure you want to reset all prompt templates to their default values? '
                'This action cannot be undone.'),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 获取当前语言
            current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
            
            # 重置为默认模板
            self.template_edit.setPlainText(get_default_template(current_lang))
            self.random_questions_edit.setPlainText(get_suggestion_template(current_lang))
            self.multi_book_template_edit.setPlainText(get_multi_book_template(current_lang))
            
            # 如果启用了语言偏好，重新添加语言指令
            if self.use_interface_language_checkbox.isChecked():
                self.update_prompts_with_language_instruction()
            
            logger.info("提示词已重置为默认值")
            
    def load_initial_values(self, lang_code):
        """加载初始值"""
        from .config import get_prefs
        prefs = get_prefs()
        
        # 加载提示词（不包含语言指令）
        self.template_edit.setPlainText(prefs.get('template', get_default_template(lang_code)))
        self.random_questions_edit.setPlainText(get_suggestion_template(lang_code))
        
        # 加载多书提示词，如果为空则使用默认模板
        multi_book_template = prefs.get('multi_book_template', '')
        if not multi_book_template or not multi_book_template.strip():
            multi_book_template = get_multi_book_template(lang_code)
        self.multi_book_template_edit.setPlainText(multi_book_template)
        
        # 加载语言偏好设置（默认为True）
        use_interface_lang = prefs.get('use_interface_language', True)
        self.use_interface_language_checkbox.setChecked(use_interface_lang)
        self.update_language_instruction_display()
        
        # 如果启用了语言偏好，添加语言指令到提示词
        if use_interface_lang:
            self.update_prompts_with_language_instruction()
        
        # 保存初始值用于变更检测（保存不含语言指令的原始值）
        self.initial_values = {
            'template': self.remove_language_instruction(self.template_edit.toPlainText()),
            'random_questions': self.remove_language_instruction(self.random_questions_edit.toPlainText()),
            'multi_book_template': self.remove_language_instruction(self.multi_book_template_edit.toPlainText()),
            'use_interface_language': use_interface_lang
        }
        
    def save_settings(self):
        """保存设置"""
        from .config import get_prefs
        prefs = get_prefs()
        
        # 获取当前语言
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        
        # 保存提示词（移除语言指令，只保存原始模板）
        # 检查是否是默认模板，如果是默认模板则保存为空字符串，让系统自动使用默认模板
        current_template = self.remove_language_instruction(self.template_edit.toPlainText())
        default_template = get_default_template(current_lang)
        
        # 如果当前模板与默认模板相同，保存为空字符串（表示使用默认模板）
        if current_template.strip() == default_template.strip():
            prefs['template'] = ''
        else:
            prefs['template'] = current_template
        
        # 同样处理多书模板
        current_multi = self.remove_language_instruction(self.multi_book_template_edit.toPlainText())
        default_multi = get_multi_book_template(current_lang)
        
        if current_multi.strip() == default_multi.strip():
            prefs['multi_book_template'] = ''
        else:
            prefs['multi_book_template'] = current_multi
        
        # 保存语言偏好设置
        prefs['use_interface_language'] = self.use_interface_language_checkbox.isChecked()
        
        # 注意：random_questions 不保存，始终使用默认模板
        
        prefs.commit()
        
        # 更新初始值（保存不含语言指令的原始值，与 check_for_changes 保持一致）
        self.initial_values = {
            'template': self.remove_language_instruction(self.template_edit.toPlainText()),
            'random_questions': self.remove_language_instruction(self.random_questions_edit.toPlainText()),
            'multi_book_template': self.remove_language_instruction(self.multi_book_template_edit.toPlainText()),
            'use_interface_language': self.use_interface_language_checkbox.isChecked()
        }
        
        logger.info("提示词设置已保存")
        
    def check_for_changes(self):
        """检查是否有未保存的更改"""
        if not hasattr(self, 'initial_values'):
            return False
            
        # 移除语言指令后比较（因为语言指令是动态添加的）
        current_template = self.remove_language_instruction(self.template_edit.toPlainText())
        current_random = self.remove_language_instruction(self.random_questions_edit.toPlainText())
        current_multi = self.remove_language_instruction(self.multi_book_template_edit.toPlainText())
        current_use_lang = self.use_interface_language_checkbox.isChecked()
        
        template_changed = current_template != self.initial_values.get('template', '')
        random_changed = current_random != self.initial_values.get('random_questions', '')
        multi_changed = current_multi != self.initial_values.get('multi_book_template', '')
        lang_pref_changed = current_use_lang != self.initial_values.get('use_interface_language', True)
        
        return template_changed or random_changed or multi_changed or lang_pref_changed
        
    def retranslate_ui(self):
        """更新界面语言"""
        # 更新所有标签
        label_map = {
            'title_prompts_explanation': ('prompts_explanation_title', 'How Prompts Work'),
            'subtitle_prompts_explanation': ('prompts_explanation', 
                'When you click Send, the plugin extracts and combines dynamic fields from your prompt template, '
                'then submits them to the AI. The underlying principle is that the AI relies on training data that '
                'includes information about the book, rather than sending the full text of the book to the AI.'),
            'label_ask_prompts': ('ask_prompts', 'Ask Prompts'),
            'label_random_questions_prompts': ('random_questions_prompts', 'Random Questions Prompts'),
            'label_multi_book_template': ('multi_book_template_label', 'Multi-Book Prompt Template'),
            'label_multi_book_placeholder_hint': ('multi_book_placeholder_hint', 
                'Use {books_metadata} for book information, {query} for user question'),
        }
        
        for label in self.findChildren(QLabel):
            obj_name = label.objectName()
            if obj_name in label_map:
                i18n_key, fallback = label_map[obj_name]
                label.setText(self.i18n.get(i18n_key, fallback))
                
        # 更新复选框
        if hasattr(self, 'use_interface_language_checkbox'):
            self.use_interface_language_checkbox.setText(
                self.i18n.get('use_interface_language', 'Always ask AI to respond in current plugin interface language')
            )
        
        # 更新语言指令显示
        self.update_language_instruction_display()
        
        # 获取当前语言
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        
        # 重新加载提示词模板（使用新语言的默认模板）
        # Ask Prompts - 使用新语言的默认模板
        self.template_edit.setPlainText(get_default_template(current_lang))
        
        # Random Questions - 使用新语言的默认模板
        self.random_questions_edit.setPlainText(get_suggestion_template(current_lang))
        
        # Multi-Book Template - 使用新语言的默认模板
        self.multi_book_template_edit.setPlainText(get_multi_book_template(current_lang))
        
        # 如果启用了语言偏好，添加语言指令
        if hasattr(self, 'use_interface_language_checkbox') and self.use_interface_language_checkbox.isChecked():
            self.update_prompts_with_language_instruction()
        
        # 更新初始值，避免误判为有变更
        # 因为切换语言后加载了新语言的默认模板，需要更新 initial_values
        self.initial_values = {
            'template': self.remove_language_instruction(self.template_edit.toPlainText()),
            'random_questions': self.remove_language_instruction(self.random_questions_edit.toPlainText()),
            'multi_book_template': self.remove_language_instruction(self.multi_book_template_edit.toPlainText()),
            'use_interface_language': self.use_interface_language_checkbox.isChecked()
        }
        
        # 更新按钮
        button_map = {
            'button_reset_prompts': ('reset_prompts', 'Reset Prompts to Default'),
        }
        
        for button in self.findChildren(QPushButton):
            obj_name = button.objectName()
            if obj_name in button_map:
                i18n_key, fallback = button_map[obj_name]
                button.setText(self.i18n.get(i18n_key, fallback))
