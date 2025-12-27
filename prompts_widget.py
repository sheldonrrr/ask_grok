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
    SPACING_SMALL, SPACING_MEDIUM, SPACING_ASK_COMPACT,
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
        content_layout.setContentsMargins(SPACING_SMALL, 0, SPACING_SMALL, 0)
        content_layout.setSpacing(SPACING_ASK_COMPACT)  # 使用紧凑间距匹配General Tab
        content_widget.setLayout(content_layout)
        
        # 添加语言偏好设置部分
        self.add_language_preference_section(content_layout)
        
        # 添加 Persona 部分
        self.add_persona_section(content_layout)
        
        # 添加提示词模板部分
        self.add_prompts_section(content_layout)
        
        # 添加动态字段示例部分
        self.add_dynamic_fields_examples(content_layout)
        
        # 添加重置按钮
        self.add_reset_button(content_layout)
        
        # 添加弹性空间
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        
    def add_language_preference_section(self, parent_layout):
        """添加语言偏好设置部分"""
        from PyQt5.QtWidgets import QCheckBox
        
        # Section Title - 第一个section，顶部间距较小
        lang_pref_title = QLabel(self.i18n.get('language_preference_title', 'Language Preference'))
        lang_pref_title.setObjectName('title_language_preference')
        first_section_style = f"""
            font-weight: bold;
            font-size: 1.08em;
            color: palette(text);
            text-transform: uppercase;
            padding: 0;
            margin: {SPACING_SMALL}px 0 {SPACING_SMALL}px 0;
        """
        lang_pref_title.setStyleSheet(first_section_style)
        parent_layout.addWidget(lang_pref_title)
        
        # Subtitle
        lang_pref_subtitle = QLabel(self.i18n.get('language_preference_subtitle', 
            'Control whether AI responses should match your interface language'))
        lang_pref_subtitle.setObjectName('subtitle_language_preference')
        lang_pref_subtitle.setWordWrap(True)
        lang_pref_subtitle.setStyleSheet(get_subtitle_style())
        parent_layout.addWidget(lang_pref_subtitle)
        
        # 创建语言偏好组
        lang_pref_group = QGroupBox()
        lang_pref_group.setStyleSheet(get_groupbox_style())
        lang_pref_layout = QVBoxLayout()
        lang_pref_layout.setSpacing(SPACING_SMALL)
        
        # 复选框
        self.use_interface_language_checkbox = QCheckBox(
            self.i18n.get('use_interface_language', 'Always ask AI to respond in current plugin interface language')
        )
        self.use_interface_language_checkbox.setChecked(False)  # 默认不勾选
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
    
    def add_persona_section(self, parent_layout):
        """添加 Persona 部分"""
        from PyQt5.QtWidgets import QCheckBox, QLineEdit
        
        # Section Title
        persona_title = QLabel(self.i18n.get('persona_title', 'Persona'))
        persona_title.setObjectName('title_persona')
        persona_title.setStyleSheet(get_section_title_style())
        parent_layout.addWidget(persona_title)
        
        # Subtitle
        persona_subtitle = QLabel(self.i18n.get('persona_subtitle', 
            'Define your research background and goals to help AI provide more relevant responses'))
        persona_subtitle.setObjectName('subtitle_persona')
        persona_subtitle.setWordWrap(True)
        persona_subtitle.setStyleSheet(get_subtitle_style())
        parent_layout.addWidget(persona_subtitle)
        
        # 创建 Persona 组
        persona_group = QGroupBox()
        persona_group.setStyleSheet(get_groupbox_style())
        persona_layout = QVBoxLayout()
        persona_layout.setSpacing(SPACING_SMALL)
        
        # 复选框：Use persona
        self.use_persona_checkbox = QCheckBox(
            self.i18n.get('use_persona', 'Use persona')
        )
        self.use_persona_checkbox.setObjectName('checkbox_use_persona')
        self.use_persona_checkbox.setChecked(True)  # 默认勾选
        self.use_persona_checkbox.stateChanged.connect(self.on_persona_checkbox_changed)
        persona_layout.addWidget(self.use_persona_checkbox)
        
        # Persona 输入框
        self.persona_edit = QLineEdit(self)
        self.persona_edit.setObjectName('edit_persona')
        self.persona_edit.setPlaceholderText(
            self.i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
        )
        self.persona_edit.textChanged.connect(self.on_config_changed)
        self.persona_edit.setMinimumHeight(30)
        persona_layout.addWidget(self.persona_edit)
        
        # 提示信息
        persona_hint = QLabel(self.i18n.get('persona_hint', 
            'The more AI knows about your target and background, the better the research or generation.'))
        persona_hint.setObjectName('label_persona_hint')
        persona_hint.setWordWrap(True)
        persona_hint.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 5px 0;")
        persona_layout.addWidget(persona_hint)
        
        persona_group.setLayout(persona_layout)
        parent_layout.addWidget(persona_group)
    
    def on_persona_checkbox_changed(self):
        """Persona 复选框变更时触发"""
        # 更新输入框的启用状态
        is_checked = self.use_persona_checkbox.isChecked()
        self.persona_edit.setEnabled(is_checked)
        self.on_config_changed()
    
    def add_prompts_section(self, parent_layout):
        """添加提示词模板部分"""
        # Section Title
        prompts_title = QLabel(self.i18n.get('prompt_templates_title', 'Prompt Templates'))
        prompts_title.setObjectName('title_prompt_templates')
        prompts_title.setStyleSheet(get_section_title_style())
        parent_layout.addWidget(prompts_title)
        
        # Subtitle
        prompts_subtitle = QLabel(self.i18n.get('prompt_templates_subtitle', 
            'Customize how book information is sent to AI using dynamic fields like {title}, {author}, {query}'))
        prompts_subtitle.setObjectName('subtitle_prompt_templates')
        prompts_subtitle.setWordWrap(True)
        prompts_subtitle.setStyleSheet(get_subtitle_style())
        parent_layout.addWidget(prompts_subtitle)
        
        # 创建提示词组
        prompts_group = QGroupBox()
        prompts_group.setStyleSheet(get_groupbox_style())
        prompts_layout = QVBoxLayout()
        prompts_layout.setSpacing(SPACING_MEDIUM)
        
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
        
        # Multi-Book Prompts
        multi_layout = QVBoxLayout()
        multi_layout.setSpacing(SPACING_SMALL)
        multi_label = QLabel(self.i18n.get('multi_book_prompts_label', 'Multi-Book Prompts'))
        multi_label.setObjectName('label_multi_book_prompts')
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
    
    def add_dynamic_fields_examples(self, parent_layout):
        """添加动态字段使用示例"""
        # Section Title
        examples_title = QLabel(self.i18n.get('dynamic_fields_title', 'Dynamic Fields Reference'))
        examples_title.setObjectName('title_dynamic_fields')
        examples_title.setStyleSheet(get_section_title_style())
        parent_layout.addWidget(examples_title)
        
        # Subtitle
        examples_subtitle = QLabel(self.i18n.get('dynamic_fields_subtitle', 
            'Available fields and example values from "Frankenstein" by Mary Shelley'))
        examples_subtitle.setObjectName('subtitle_dynamic_fields')
        examples_subtitle.setWordWrap(True)
        examples_subtitle.setStyleSheet(get_subtitle_style())
        parent_layout.addWidget(examples_subtitle)
        
        # 创建示例组
        examples_group = QGroupBox()
        examples_group.setStyleSheet(get_groupbox_style())
        examples_layout = QVBoxLayout()
        examples_layout.setSpacing(SPACING_SMALL)
        
        # 创建示例表格
        example_text = self.i18n.get('dynamic_fields_examples', 
            '<b>{title}</b> → Frankenstein<br>'
            '<b>{author}</b> → Mary Shelley<br>'
            '<b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br>'
            '<b>{pubyear}</b> → 1818<br>'
            '<b>{language}</b> → English<br>'
            '<b>{series}</b> → (none)<br>'
            '<b>{query}</b> → Your question text')
        
        examples_label = QLabel(example_text)
        examples_label.setObjectName('label_dynamic_fields_examples')
        examples_label.setWordWrap(True)
        examples_label.setTextFormat(Qt.RichText)
        examples_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 0; line-height: 1.6;")
        examples_layout.addWidget(examples_label)
        
        examples_group.setLayout(examples_layout)
        parent_layout.addWidget(examples_group)
        
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
        # 隐藏提示词系统：不再自动添加到文本框
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
    
    def get_final_prompt(self, base_prompt):
        """获取最终提示词（添加 persona 和隐藏的语言指令）
        
        Args:
            base_prompt: 基础提示词（用户在配置中编辑的内容）
            
        Returns:
            str: 添加了 persona（开头）和语言指令（结尾）的提示词
        """
        result = base_prompt
        
        # 在开头添加 persona（如果启用）
        if self.use_persona_checkbox.isChecked():
            persona_text = self.persona_edit.text().strip()
            if persona_text:
                result = persona_text + '\n\n' + result
        
        # 在结尾添加语言指令（如果启用）
        if self.use_interface_language_checkbox.isChecked():
            language_instruction = self.get_language_instruction_text()
            result = result + language_instruction
        
        return result
    
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
            
            # 重置为默认模板（不添加语言指令，因为是隐藏提示词）
            self.template_edit.setPlainText(get_default_template(current_lang))
            self.random_questions_edit.setPlainText(get_suggestion_template(current_lang))
            self.multi_book_template_edit.setPlainText(get_multi_book_template(current_lang))
            
            # 重置 Persona 设置（默认开启，使用默认文本）
            self.use_persona_checkbox.setChecked(True)
            default_persona = self.i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
            self.persona_edit.setText(default_persona)
            self.persona_edit.setEnabled(True)
            
            # 重置语言偏好设置（默认关闭）
            self.use_interface_language_checkbox.setChecked(False)
            self.update_language_instruction_display()
            
            logger.info("提示词已重置为默认值")
            
    def load_initial_values(self, lang_code):
        """加载初始值"""
        from .config import get_prefs
        from .i18n import get_all_languages
        prefs = get_prefs()
        
        # 加载提示词（隐藏提示词系统：不在文本框中显示语言指令）
        saved_template = prefs.get('template', '')
        
        # 检查保存的模板是否是其他语言的默认模板，如果是则替换为当前语言的默认模板
        if saved_template:
            is_default_from_other_lang = False
            all_languages = get_all_languages()
            for other_lang_code in all_languages.keys():
                if other_lang_code != lang_code:
                    other_default = get_default_template(other_lang_code)
                    if saved_template.strip() == other_default.strip():
                        is_default_from_other_lang = True
                        break
            
            if is_default_from_other_lang:
                # 使用当前语言的默认模板
                self.template_edit.setPlainText(get_default_template(lang_code))
            else:
                # 使用保存的自定义模板
                self.template_edit.setPlainText(saved_template)
        else:
            # 没有保存的模板，使用当前语言的默认模板
            self.template_edit.setPlainText(get_default_template(lang_code))
        
        self.random_questions_edit.setPlainText(get_suggestion_template(lang_code))
        
        # 加载多书提示词，如果为空则使用默认模板
        multi_book_template = prefs.get('multi_book_template', '')
        
        # 检查保存的多书模板是否是其他语言的默认模板
        if multi_book_template and multi_book_template.strip():
            is_default_from_other_lang = False
            all_languages = get_all_languages()
            for other_lang_code in all_languages.keys():
                if other_lang_code != lang_code:
                    other_default = get_multi_book_template(other_lang_code)
                    if multi_book_template.strip() == other_default.strip():
                        is_default_from_other_lang = True
                        break
            
            if is_default_from_other_lang:
                # 使用当前语言的默认模板
                multi_book_template = get_multi_book_template(lang_code)
        else:
            # 没有保存的模板，使用当前语言的默认模板
            multi_book_template = get_multi_book_template(lang_code)
        
        self.multi_book_template_edit.setPlainText(multi_book_template)
        
        # 加载语言偏好设置（默认为False）
        use_interface_lang = prefs.get('use_interface_language', False)
        self.use_interface_language_checkbox.setChecked(use_interface_lang)
        self.update_language_instruction_display()
        
        # 加载 Persona 设置
        use_persona = prefs.get('use_persona', True)
        self.use_persona_checkbox.setChecked(use_persona)
        default_persona = self.i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
        saved_persona = prefs.get('persona', default_persona)
        
        # 检查保存的 persona 是否是任何语言的默认值
        # 如果是，则使用当前语言的默认值
        from .i18n import get_translation
        default_personas = []
        for lang_code in ['en', 'zh', 'zht', 'de', 'es', 'fr', 'ja', 'ru']:
            lang_i18n = get_translation(lang_code)
            default_personas.append(lang_i18n.get('persona_placeholder', ''))
        
        # 如果保存的是空字符串或任何语言的默认值，使用当前语言的默认值
        if not saved_persona or saved_persona in default_personas:
            saved_persona = default_persona
        self.persona_edit.setText(saved_persona)
        self.persona_edit.setEnabled(use_persona)
        
        # 保存初始值用于变更检测（隐藏提示词系统：直接保存文本框内容）
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': use_interface_lang,
            'use_persona': use_persona,
            'persona': saved_persona
        }
        
    def save_settings(self):
        """保存设置"""
        from .config import get_prefs
        prefs = get_prefs()
        
        # 获取当前语言
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        
        # 保存提示词（隐藏提示词系统：直接保存文本框内容，无需移除语言指令）
        # 检查是否是默认模板，如果是默认模板则保存为空字符串，让系统自动使用默认模板
        current_template = self.template_edit.toPlainText()
        default_template = get_default_template(current_lang)
        
        # 如果当前模板与默认模板相同，保存为空字符串（表示使用默认模板）
        if current_template.strip() == default_template.strip():
            prefs['template'] = ''
        else:
            prefs['template'] = current_template
        
        # 同样处理多书模板
        current_multi = self.multi_book_template_edit.toPlainText()
        default_multi = get_multi_book_template(current_lang)
        
        if current_multi.strip() == default_multi.strip():
            prefs['multi_book_template'] = ''
        else:
            prefs['multi_book_template'] = current_multi
        
        # 保存语言偏好设置
        prefs['use_interface_language'] = self.use_interface_language_checkbox.isChecked()
        
        # 保存 Persona 设置
        prefs['use_persona'] = self.use_persona_checkbox.isChecked()
        prefs['persona'] = self.persona_edit.text().strip()
        
        # 注意：random_questions 不保存，始终使用默认模板
        
        prefs.commit()
        
        # 更新初始值（隐藏提示词系统：直接保存文本框内容）
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': self.use_interface_language_checkbox.isChecked(),
            'use_persona': self.use_persona_checkbox.isChecked(),
            'persona': self.persona_edit.text().strip()
        }
        
        logger.info("提示词设置已保存")
        
    def check_for_changes(self):
        """检查是否有未保存的更改"""
        if not hasattr(self, 'initial_values'):
            return False
            
        # 隐藏提示词系统：直接比较文本框内容
        current_template = self.template_edit.toPlainText()
        current_random = self.random_questions_edit.toPlainText()
        current_multi = self.multi_book_template_edit.toPlainText()
        current_use_lang = self.use_interface_language_checkbox.isChecked()
        
        template_changed = current_template != self.initial_values.get('template', '')
        random_changed = current_random != self.initial_values.get('random_questions', '')
        multi_changed = current_multi != self.initial_values.get('multi_book_template', '')
        lang_pref_changed = current_use_lang != self.initial_values.get('use_interface_language', False)
        
        # 检查 Persona 变更
        current_use_persona = self.use_persona_checkbox.isChecked()
        current_persona = self.persona_edit.text().strip()
        persona_checkbox_changed = current_use_persona != self.initial_values.get('use_persona', True)
        persona_text_changed = current_persona != self.initial_values.get('persona', '')
        
        return template_changed or random_changed or multi_changed or lang_pref_changed or persona_checkbox_changed or persona_text_changed
        
    def retranslate_ui(self):
        """更新界面语言"""
        # 更新所有标签
        label_map = {
            'title_language_preference': ('language_preference_title', 'Language Preference'),
            'subtitle_language_preference': ('language_preference_subtitle', 
                'Control whether AI responses should match your interface language'),
            'title_persona': ('persona_title', 'Persona'),
            'subtitle_persona': ('persona_subtitle', 
                'Define your research background and goals to help AI provide more relevant responses'),
            'label_persona_hint': ('persona_hint', 
                'The more AI knows about your target and background, the better the research or generation.'),
            'title_prompt_templates': ('prompt_templates_title', 'Prompt Templates'),
            'subtitle_prompt_templates': ('prompt_templates_subtitle', 
                'Customize how book information is sent to AI using dynamic fields like {title}, {author}, {query}'),
            'label_ask_prompts': ('ask_prompts', 'Ask Prompts'),
            'label_random_questions_prompts': ('random_questions_prompts', 'Random Questions Prompts'),
            'label_multi_book_prompts': ('multi_book_prompts_label', 'Multi-Book Prompts'),
            'label_multi_book_placeholder_hint': ('multi_book_placeholder_hint', 
                'Use {books_metadata} for book information, {query} for user question'),
            'title_dynamic_fields': ('dynamic_fields_title', 'Dynamic Fields Reference'),
            'subtitle_dynamic_fields': ('dynamic_fields_subtitle', 
                'Available fields and example values from "Frankenstein" by Mary Shelley'),
            'label_dynamic_fields_examples': ('dynamic_fields_examples', 
                '<b>{title}</b> → Frankenstein<br>'
                '<b>{author}</b> → Mary Shelley<br>'
                '<b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br>'
                '<b>{pubyear}</b> → 1818<br>'
                '<b>{language}</b> → English<br>'
                '<b>{series}</b> → (none)<br>'
                '<b>{query}</b> → Your question text'),
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
        
        # 更新 Persona 复选框和输入框
        if hasattr(self, 'use_persona_checkbox'):
            self.use_persona_checkbox.setText(
                self.i18n.get('use_persona', 'Use persona')
            )
        if hasattr(self, 'persona_edit'):
            self.persona_edit.setPlaceholderText(
                self.i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
            )
        
        # 更新语言指令显示
        self.update_language_instruction_display()
        
        # 获取当前语言
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        
        # 重新加载提示词模板（使用新语言的默认模板）
        # 隐藏提示词系统：不在文本框中添加语言指令
        self.template_edit.setPlainText(get_default_template(current_lang))
        self.random_questions_edit.setPlainText(get_suggestion_template(current_lang))
        self.multi_book_template_edit.setPlainText(get_multi_book_template(current_lang))
        
        # 更新初始值，避免误判为有变更
        # 因为切换语言后加载了新语言的默认模板，需要更新 initial_values
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': self.use_interface_language_checkbox.isChecked(),
            'use_persona': self.use_persona_checkbox.isChecked(),
            'persona': self.persona_edit.text().strip()
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


def apply_prompt_enhancements(base_prompt):
    """应用 persona 和语言指令到提示词（独立函数，直接从配置读取）
    
    Args:
        base_prompt: 基础提示词
        
    Returns:
        str: 添加了 persona（开头）和语言指令（结尾）的提示词
    """
    from .config import get_prefs
    from .i18n import get_translation, get_all_languages
    
    prefs = get_prefs()
    result = base_prompt
    
    # 在开头添加 persona（如果启用）
    use_persona = prefs.get('use_persona', True)
    if use_persona:
        persona_text = prefs.get('persona', '').strip()
        if persona_text:
            result = persona_text + '\n\n' + result
            logger.info(f"已添加 persona 到提示词开头: {persona_text[:50]}...")
    
    # 在结尾添加语言指令（如果启用）
    use_interface_language = prefs.get('use_interface_language', False)
    if use_interface_language:
        lang_code = prefs.get('language', 'en')
        all_languages = get_all_languages()
        language_name = all_languages.get(lang_code, 'English')
        
        i18n = get_translation(lang_code)
        instruction_template = i18n.get('language_instruction_text', 'Please respond in {language_name}.')
        language_instruction = '\n\n' + instruction_template.format(language_name=language_name)
        result = result + language_instruction
        logger.info(f"已添加语言指令到提示词结尾")
    
    return result
