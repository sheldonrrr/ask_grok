#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPlainTextEdit, 
                            QPushButton, QHBoxLayout, QGroupBox, QScrollArea, 
                            QSizePolicy, QMessageBox, QSpinBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics

from .i18n import get_default_template, get_suggestion_template, get_multi_book_template
from .widgets import apply_button_style
try:
    from .epub_reader import READER_PROMPT_INTRO_FALLBACK, stored_reader_intro
except ImportError:
    from epub_reader import READER_PROMPT_INTRO_FALLBACK, stored_reader_intro
from .ui_constants import (
    SPACING_SMALL, SPACING_MEDIUM, SPACING_ASK_COMPACT,
    get_groupbox_style, get_section_title_style, get_subtitle_style,
    TEXT_COLOR_SECONDARY_STRONG,
    setup_settings_tab_content, add_settings_section, configure_layout,
)

logger = logging.getLogger(__name__)


class ReaderEditableField(QWidget):
    """A setting that stays as plain text until the user finishes an edit."""

    value_committed = pyqtSignal()

    def __init__(self, title, kind='text', parent=None):
        super().__init__(parent)
        self.kind = kind
        self._editing = False
        self._value = '' if kind == 'text' else 500
        self._edit_label = 'Edit'
        self._done_label = 'Done'
        self._cancel_label = 'Cancel'

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, SPACING_SMALL, 0, 0)
        layout.setSpacing(SPACING_SMALL)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(SPACING_SMALL)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet('font-weight: 600;')
        header.addWidget(self.title_label, 1)
        self.edit_button = QPushButton(self._edit_label)
        self.cancel_button = QPushButton(self._cancel_label)
        self.cancel_button.setVisible(False)
        self.edit_button.clicked.connect(self._on_primary)
        self.cancel_button.clicked.connect(self.cancel_edit)
        header.addWidget(self.edit_button)
        header.addWidget(self.cancel_button)
        layout.addLayout(header)

        self.view_label = QLabel('')
        self.view_label.setWordWrap(True)
        self.view_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.view_label.setStyleSheet(
            'color: {0};'.format(TEXT_COLOR_SECONDARY_STRONG)
        )
        layout.addWidget(self.view_label)

        if kind == 'number':
            self.editor = QSpinBox(self)
            self.editor.setRange(50, 2000)
            self.editor.setSingleStep(50)
            self.editor.setMinimumWidth(120)
        else:
            self.editor = QPlainTextEdit(self)
            self.editor.setMinimumHeight(72)
            self.editor.setMaximumHeight(140)
        self.editor.setVisible(False)
        layout.addWidget(self.editor)
        self._show_view()

    def set_range(self, minimum, maximum):
        if self.kind == 'number':
            self.editor.setRange(minimum, maximum)

    def set_action_labels(self, edit, done, cancel):
        self._edit_label = edit
        self._done_label = done
        self._cancel_label = cancel
        self.cancel_button.setText(cancel)
        self.edit_button.setText(self._done_label if self._editing else self._edit_label)

    def value(self):
        return self._value

    def set_value(self, value):
        if self.kind == 'number':
            try:
                self._value = int(value)
            except (TypeError, ValueError):
                self._value = 500
        else:
            self._value = value.strip() if isinstance(value, str) else str(value or '')
        if self._editing:
            self._editing = False
        self._show_view()

    def commit_if_editing(self):
        if self._editing:
            self._finish(True)

    def cancel_edit(self):
        if self._editing:
            self._finish(False)

    def _on_primary(self):
        if self._editing:
            self._finish(True)
        else:
            self._begin()

    def _begin(self):
        self._editing = True
        if self.kind == 'number':
            self.editor.setValue(int(self._value))
        else:
            self.editor.setPlainText(self._value)
        self.view_label.setVisible(False)
        self.editor.setVisible(True)
        self.cancel_button.setVisible(True)
        self.edit_button.setText(self._done_label)
        self.editor.setFocus()

    def _finish(self, commit):
        if commit:
            if self.kind == 'number':
                self._value = int(self.editor.value())
            else:
                self._value = self.editor.toPlainText().strip()
        self._editing = False
        self._show_view()
        if commit:
            self.value_committed.emit()

    def _show_view(self):
        self.editor.setVisible(False)
        self.cancel_button.setVisible(False)
        self.edit_button.setText(self._edit_label)
        shown = str(self._value) if self.kind == 'number' else self._value
        self.view_label.setText(shown)
        self.view_label.setVisible(True)


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
        from .ui_constants import setup_tab_widget_layout, get_tab_scroll_area_style
        
        main_layout = setup_tab_widget_layout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setObjectName("prompts_scroll")
        scroll.setStyleSheet(get_tab_scroll_area_style("prompts_scroll"))
        if scroll.viewport():
            scroll.viewport().setContentsMargins(0, 0, 0, 0)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("QWidget#prompts_content_container { background: transparent; border: none; }")
        content_widget.setObjectName("prompts_content_container")
        content_layout = setup_settings_tab_content(content_widget)
        
        # 添加语言偏好设置部分
        self.add_language_preference_section(content_layout)
        
        # 添加 Persona 部分
        self.add_persona_section(content_layout)
        
        # 阅读模式：勾选要提交的内容，和下面的模板编辑分开
        self.add_reader_prompt_section(content_layout)

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
        
        lang_section, lang_pref_title, lang_pref_subtitle = add_settings_section(
            parent_layout,
            self.i18n.get('language_preference_title', 'Language Preference'),
            self.i18n.get('language_preference_subtitle',
                'Control whether AI responses should match your interface language'),
        )
        lang_pref_title.setObjectName('title_language_preference')
        lang_pref_subtitle.setObjectName('subtitle_language_preference')
        
        lang_pref_group = QGroupBox()
        lang_pref_group.setStyleSheet(get_groupbox_style())
        lang_pref_layout = QVBoxLayout()
        configure_layout(lang_pref_layout, 'settings_section')
        
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
        lang_section.addWidget(lang_pref_group)
    
    def add_persona_section(self, parent_layout):
        """添加 Persona 部分"""
        from PyQt5.QtWidgets import QCheckBox, QLineEdit
        
        persona_section, persona_title, persona_subtitle = add_settings_section(
            parent_layout,
            self.i18n.get('persona_title', 'Persona'),
            self.i18n.get('persona_subtitle',
                'Define your research background and goals to help AI provide more relevant responses'),
        )
        persona_title.setObjectName('title_persona')
        persona_subtitle.setObjectName('subtitle_persona')
        
        persona_group = QGroupBox()
        persona_group.setStyleSheet(get_groupbox_style())
        persona_layout = QVBoxLayout()
        configure_layout(persona_layout, 'settings_section')
        
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
        persona_section.addWidget(persona_group)
    
    def on_persona_checkbox_changed(self):
        """Persona 复选框变更时触发"""
        # 更新输入框的启用状态
        is_checked = self.use_persona_checkbox.isChecked()
        self.persona_edit.setEnabled(is_checked)
        self.on_config_changed()
    
    def add_reader_prompt_section(self, parent_layout):
        """阅读模式提交哪些内容，用勾选控制，不要求用户写模板字段。"""
        from PyQt5.QtWidgets import QCheckBox
        try:
            from .epub_reader import READER_CONTEXT_CHARS, READER_CONTEXT_CHARS_MAX, READER_CONTEXT_CHARS_MIN
        except ImportError:
            from epub_reader import READER_CONTEXT_CHARS, READER_CONTEXT_CHARS_MAX, READER_CONTEXT_CHARS_MIN

        section, title, subtitle = add_settings_section(
            parent_layout,
            self.i18n.get('reader_prompt_section_title', 'Reading mode'),
            self.i18n.get(
                'reader_prompt_section_subtitle',
                'Choose what is sent when you ask from the reader. The selected passage, its chapter, and the surrounding text can each be included.',
            ),
        )
        title.setObjectName('title_reader_prompt')
        subtitle.setObjectName('subtitle_reader_prompt')

        group = QGroupBox()
        group.setStyleSheet(get_groupbox_style())
        layout = QVBoxLayout()
        configure_layout(layout, 'settings_section')
        self.reader_prompt_checks = {}
        for key, label_key, fallback in (
            ('reader_include_book', 'reader_include_book', 'Book information'),
            ('reader_include_chapter', 'reader_include_chapter', 'Current chapter'),
            ('reader_include_context', 'reader_include_context', 'Text around the selection'),
            ('reader_include_selection', 'reader_include_selection', 'Selected text'),
            ('reader_include_note', 'reader_include_note', 'Your note'),
        ):
            box = QCheckBox(self.i18n.get(label_key, fallback))
            box.setObjectName('checkbox_' + key)
            box.setChecked(True)
            box.stateChanged.connect(self._on_reader_section_toggled)
            self.reader_prompt_checks[key] = box
            layout.addWidget(box)

        self.reader_intro_field = ReaderEditableField(
            self.i18n.get('reader_prompt_intro_label', 'Reading task'),
            'text',
            self,
        )
        self.reader_intro_field.title_label.setObjectName('label_reader_intro')
        self.reader_intro_field.set_value(self._reader_text_default(
            'reader_prompt_intro', READER_PROMPT_INTRO_FALLBACK,
        ))
        self.reader_intro_field.value_committed.connect(self._on_reader_field_committed)

        self.reader_chars_field = ReaderEditableField(
            self.i18n.get('reader_prompt_context_chars', 'Characters before and after the selection'),
            'number',
            self,
        )
        self.reader_chars_field.title_label.setObjectName('label_reader_context_chars')
        self.reader_chars_field.set_range(READER_CONTEXT_CHARS_MIN, READER_CONTEXT_CHARS_MAX)
        self.reader_chars_field.set_value(READER_CONTEXT_CHARS)
        self.reader_chars_field.value_committed.connect(self._on_reader_field_committed)

        self.reader_note_field = ReaderEditableField(
            self.i18n.get('reader_prompt_default_note_label', 'Default note'),
            'text',
            self,
        )
        self.reader_note_field.title_label.setObjectName('label_reader_default_note')
        self.reader_note_field.set_value(self._reader_text_default(
            'reader_prompt_default_question',
            'Explain this passage using the chapter context.',
        ))
        self.reader_note_field.value_committed.connect(self._on_reader_field_committed)
        self._apply_reader_action_labels()

        preview_title = QLabel(self.i18n.get('reader_prompt_preview_title', 'Example preview'))
        preview_title.setObjectName('label_reader_preview_title')
        preview_title.setStyleSheet('font-weight: 600;')
        preview_hint = QLabel(self.i18n.get(
            'reader_prompt_preview_hint',
            'This preview uses a passage from Frankenstein by Mary Shelley. Checking a box adds or removes that part.',
        ))
        preview_hint.setObjectName('label_reader_preview_hint')
        preview_hint.setWordWrap(True)
        preview_hint.setStyleSheet('color: {0};'.format(TEXT_COLOR_SECONDARY_STRONG))
        self.reader_preview = QPlainTextEdit(self)
        self.reader_preview.setObjectName('reader_prompt_preview')
        self.reader_preview.setReadOnly(True)
        self.reader_preview.setMinimumHeight(180)
        self.reader_preview.setMaximumHeight(320)

        layout.addWidget(self.reader_intro_field)
        layout.addWidget(self.reader_chars_field)
        layout.addWidget(self.reader_note_field)
        layout.addWidget(preview_title)
        layout.addWidget(preview_hint)
        layout.addWidget(self.reader_preview)
        group.setLayout(layout)
        section.addWidget(group)
        self._refresh_reader_preview()

    def add_prompts_section(self, parent_layout):
        """添加提示词模板部分"""
        prompts_section, prompts_title, prompts_subtitle = add_settings_section(
            parent_layout,
            self.i18n.get('prompt_templates_title', 'Prompt Templates'),
            self.i18n.get('prompt_templates_subtitle',
                'Customize how book information is sent to AI using dynamic fields like {title}, {author}, {query}'),
        )
        prompts_title.setObjectName('title_prompt_templates')
        prompts_subtitle.setObjectName('subtitle_prompt_templates')
        
        prompts_group = QGroupBox()
        prompts_group.setStyleSheet(get_groupbox_style())
        prompts_layout = QVBoxLayout()
        configure_layout(prompts_layout, 'settings_section')
        
        ask_layout = QVBoxLayout()
        configure_layout(ask_layout, 'settings_section')
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
        configure_layout(random_layout, 'settings_section')
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
        configure_layout(multi_layout, 'settings_section')
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
        prompts_section.addWidget(prompts_group)
    
    def add_dynamic_fields_examples(self, parent_layout):
        """添加动态字段使用示例"""
        examples_section, examples_title, examples_subtitle = add_settings_section(
            parent_layout,
            self.i18n.get('dynamic_fields_title', 'Dynamic Fields Reference'),
            self.i18n.get('dynamic_fields_subtitle',
                'Available fields and example values from "Frankenstein" by Mary Shelley'),
        )
        examples_title.setObjectName('title_dynamic_fields')
        examples_subtitle.setObjectName('subtitle_dynamic_fields')
        
        examples_group = QGroupBox()
        examples_group.setStyleSheet(get_groupbox_style())
        examples_layout = QVBoxLayout()
        configure_layout(examples_layout, 'settings_section')
        
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
        examples_section.addWidget(examples_group)
        
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
        configure_layout(reset_layout, 'footer')
        reset_layout.addStretch()
        
        reset_button = QPushButton(self.i18n.get('reset_prompts', 'Reset Prompts to Default'))
        reset_button.setObjectName('button_reset_prompts')
        apply_button_style(reset_button)
        reset_button.clicked.connect(self.on_reset_prompts)
        reset_layout.addWidget(reset_button)
        
        parent_layout.addLayout(reset_layout)
        
    def on_config_changed(self):
        """配置变更时触发"""
        self.config_changed.emit()
    
    def _disable_save_button(self):
        """禁用保存按钮（在自动保存后调用）"""
        if hasattr(self, 'parent_dialog') and self.parent_dialog:
            if hasattr(self.parent_dialog, 'save_button'):
                self.parent_dialog.save_button.setEnabled(False)
                logger.debug("保存按钮已禁用（自动保存后）")
    
    def on_language_preference_changed(self):
        """语言偏好变更时触发"""
        self.update_language_instruction_display()
        # 隐藏提示词系统：不再自动添加到文本框
        self.on_config_changed()
        
        # 自动保存语言偏好设置
        from .config import get_prefs
        prefs = get_prefs()
        prefs['use_interface_language'] = self.use_interface_language_checkbox.isChecked()
        prefs.commit()
        
        # 更新初始值，避免误判为有变更
        if hasattr(self, 'initial_values'):
            self.initial_values['use_interface_language'] = self.use_interface_language_checkbox.isChecked()
        
        # 禁用保存按钮（因为已自动保存）
        self._disable_save_button()
        
        logger.info(f"语言偏好设置已自动保存: {self.use_interface_language_checkbox.isChecked()}")
    
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
            for box in getattr(self, 'reader_prompt_checks', {}).values():
                box.setChecked(True)
            if hasattr(self, 'reader_intro_field'):
                self.reader_intro_field.cancel_edit()
                self.reader_intro_field.set_value(self._reader_text_default(
                    'reader_prompt_intro', READER_PROMPT_INTRO_FALLBACK,
                ))
            if hasattr(self, 'reader_note_field'):
                self.reader_note_field.cancel_edit()
                self.reader_note_field.set_value(self._reader_text_default(
                    'reader_prompt_default_question',
                    'Explain this passage using the chapter context.',
                ))
            if hasattr(self, 'reader_chars_field'):
                self.reader_chars_field.cancel_edit()
                self.reader_chars_field.set_value(500)
            self._refresh_reader_preview()
            
            logger.info("提示词已重置为默认值")
            
            # 自动保存重置后的设置
            self.save_settings()
            logger.info("重置后的提示词已自动保存")
            
            # 禁用保存按钮（因为已自动保存）
            self._disable_save_button()
            
    def _is_legacy_default_template(self, saved_value):
        """检查是否是 v1.4.0 或更早版本的旧默认模板
        
        v1.4.0 的默认模板特征：
        1. 包含所有必需的占位符 ({title}, {author}, {query})
        2. 长度较短（< 300 字符），因为只是简单列出书籍信息
        3. 不包含 v1.4.1 新增的详细上下文说明（如 "calibre", "Ask AI Plugin" 等）
        
        Args:
            saved_value: 保存的模板值
            
        Returns:
            bool: 如果是旧版本默认模板返回 True
        """
        if not saved_value:
            return False
        
        saved_stripped = saved_value.strip()
        
        # 必需的占位符
        required_placeholders = ['{title}', '{author}', '{query}']
        has_all_placeholders = all(p in saved_stripped for p in required_placeholders)
        
        if not has_all_placeholders:
            return False
        
        # v1.4.0 的模板较短（通常 < 300 字符），v1.4.1 的模板更详细（> 400 字符）
        is_short_template = len(saved_stripped) < 350
        
        # v1.4.1 的模板包含更详细的上下文说明
        has_new_context = 'calibre' in saved_stripped.lower() or 'ask ai' in saved_stripped.lower()
        
        # 如果包含所有占位符、长度较短、且不包含新版本的上下文说明，则认为是旧版本模板
        if is_short_template and not has_new_context:
            logger.debug(f"检测到 v1.4.0 旧版本默认模板（长度: {len(saved_stripped)}）")
            return True
        
        return False
    
    def _is_default_value_from_any_language(self, saved_value, get_default_func):
        """检查保存的值是否是任何语言的默认值（包括旧版本）
        
        Args:
            saved_value: 保存的值
            get_default_func: 获取默认值的函数，接受 lang_code 参数
            
        Returns:
            bool: 如果是任何语言的默认值返回 True，否则返回 False
        """
        # 类型检查：如果不是字符串，视为需要使用默认值
        if not isinstance(saved_value, str):
            return True
            
        if not saved_value:
            return True
        
        # 检查是否是 v1.4.0 旧版本的默认模板（仅对 Ask Prompts 模板进行检查）
        if get_default_func == get_default_template:
            if self._is_legacy_default_template(saved_value):
                logger.info("检测到 v1.4.0 旧版本默认模板，将使用新版本默认模板")
                return True
        
        from .i18n import get_all_languages
        all_languages = get_all_languages()
        
        for lang_code in all_languages.keys():
            default_value = get_default_func(lang_code)
            # 简单比较：所有模板现在都是单行字符串，只需去除首尾空白
            if saved_value.strip() == default_value.strip():
                logger.debug(f"匹配到语言 {lang_code} 的默认模板")
                return True
        
        return False
    
    def _load_prompt_with_language_fallback(self, saved_value, get_default_func, current_lang):
        """加载提示词，如果是默认值则使用当前语言的默认值
        
        Args:
            saved_value: 保存的值
            get_default_func: 获取默认值的函数，接受 lang_code 参数
            current_lang: 当前语言代码
            
        Returns:
            str: 最终使用的提示词
        """
        # v1.3.9 兼容性处理：如果 saved_value 是 dict 类型（旧版本格式），使用默认模板
        if isinstance(saved_value, dict):
            logger.info(f"[Migration] Detected dict type for prompt, using default template for {current_lang}")
            return get_default_func(current_lang)
        
        if self._is_default_value_from_any_language(saved_value, get_default_func):
            return get_default_func(current_lang)
        else:
            return saved_value
    
    def load_initial_values(self, lang_code):
        """加载初始值"""
        from .config import get_prefs
        prefs = get_prefs()
        
        # 加载 Ask 提示词
        saved_template = prefs.get('template', '')
        final_template = self._load_prompt_with_language_fallback(
            saved_template, get_default_template, lang_code
        )
        self.template_edit.setPlainText(final_template)
        
        # 加载 Random Questions 提示词
        saved_random = prefs.get('random_questions', '')
        final_random = self._load_prompt_with_language_fallback(
            saved_random, get_suggestion_template, lang_code
        )
        self.random_questions_edit.setPlainText(final_random)
        
        # 加载 Multi-Book 提示词
        saved_multi = prefs.get('multi_book_template', '')
        final_multi = self._load_prompt_with_language_fallback(
            saved_multi, get_multi_book_template, lang_code
        )
        self.multi_book_template_edit.setPlainText(final_multi)
        
        # 加载语言偏好设置（默认为False）
        use_interface_lang = prefs.get('use_interface_language', False)
        self.use_interface_language_checkbox.setChecked(use_interface_lang)
        self.update_language_instruction_display()
        
        # 加载 Persona 设置
        use_persona = prefs.get('use_persona', True)
        self.use_persona_checkbox.setChecked(use_persona)
        
        # 定义获取 persona 默认值的函数
        def get_persona_default(lang):
            from .i18n import get_translation
            lang_i18n = get_translation(lang)
            return lang_i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
        
        saved_persona = prefs.get('persona', '')
        final_persona = self._load_prompt_with_language_fallback(
            saved_persona, get_persona_default, lang_code
        )
        self.persona_edit.setText(final_persona)
        self.persona_edit.setEnabled(use_persona)
        self._load_reader_prompt_checks(prefs)
        self._load_reader_prompt_fields(prefs, lang_code)
        self._refresh_reader_preview()
        
        # 保存初始值用于变更检测（隐藏提示词系统：直接保存文本框内容）
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': use_interface_lang,
            'use_persona': use_persona,
            'persona': self.persona_edit.text().strip(),
            'reader_prompt': self._reader_prompt_values(),
        }
        
    def _reader_prompt_values(self):
        values = {
            key: box.isChecked()
            for key, box in getattr(self, 'reader_prompt_checks', {}).items()
        }
        if hasattr(self, 'reader_intro_field'):
            values['reader_prompt_intro'] = self.reader_intro_field.value()
        if hasattr(self, 'reader_note_field'):
            values['reader_prompt_default_question'] = self.reader_note_field.value()
        if hasattr(self, 'reader_chars_field'):
            values['reader_context_chars'] = self.reader_chars_field.value()
        return values

    def _load_reader_prompt_checks(self, prefs):
        for key, box in getattr(self, 'reader_prompt_checks', {}).items():
            box.blockSignals(True)
            box.setChecked(bool(prefs.get(key, True)))
            box.blockSignals(False)

    def _reader_text_default(self, key, fallback):
        return self.i18n.get(key, fallback)

    def _reader_text_getter(self, key, fallback):
        def getter(lang):
            from .i18n import get_translation
            return get_translation(lang).get(key, fallback)
        return getter

    def _load_reader_prompt_fields(self, prefs, lang_code):
        if not hasattr(self, 'reader_intro_field'):
            return
        intro_fallback = READER_PROMPT_INTRO_FALLBACK
        note_fallback = 'Explain this passage using the chapter context.'
        self.reader_intro_field.set_value(self._load_prompt_with_language_fallback(
            stored_reader_intro(prefs.get('reader_prompt_intro', '')),
            self._reader_text_getter('reader_prompt_intro', intro_fallback),
            lang_code,
        ))
        self.reader_note_field.set_value(self._load_prompt_with_language_fallback(
            prefs.get('reader_prompt_default_question', ''),
            self._reader_text_getter('reader_prompt_default_question', note_fallback),
            lang_code,
        ))
        try:
            from .epub_reader import reader_context_chars
        except ImportError:
            from epub_reader import reader_context_chars
        self.reader_chars_field.set_value(reader_context_chars(prefs))

    def _stored_reader_text(self, value, key, fallback, current_lang):
        default = self._reader_text_getter(key, fallback)(current_lang)
        if value.strip() == default.strip():
            return ''
        return value.strip()

    def _normalize_reader_texts(self):
        intro_fallback = READER_PROMPT_INTRO_FALLBACK
        note_fallback = 'Explain this passage using the chapter context.'
        if hasattr(self, 'reader_intro_field') and not str(self.reader_intro_field.value()).strip():
            self.reader_intro_field.set_value(self._reader_text_default('reader_prompt_intro', intro_fallback))
        if hasattr(self, 'reader_note_field') and not str(self.reader_note_field.value()).strip():
            self.reader_note_field.set_value(self._reader_text_default(
                'reader_prompt_default_question', note_fallback,
            ))

    def _reader_preview_prefs(self):
        prefs = {
            key: box.isChecked()
            for key, box in getattr(self, 'reader_prompt_checks', {}).items()
        }
        prefs['reader_prompt_intro'] = self.reader_intro_field.value()
        prefs['reader_prompt_default_question'] = self.reader_note_field.value()
        prefs['reader_context_chars'] = self.reader_chars_field.value()
        prefs['use_persona'] = False
        prefs['use_interface_language'] = False
        return prefs

    def _refresh_reader_preview(self):
        if not hasattr(self, 'reader_preview'):
            return
        try:
            from .epub_reader import build_reader_preview
        except ImportError:
            from epub_reader import build_reader_preview
        self.reader_preview.setPlainText(build_reader_preview(
            self._reader_preview_prefs(),
            self.i18n,
        ))

    def _on_reader_section_toggled(self):
        self._refresh_reader_preview()
        self.on_config_changed()

    def _on_reader_field_committed(self):
        self._normalize_reader_texts()
        self._refresh_reader_preview()
        self.on_config_changed()

    def _apply_reader_action_labels(self):
        labels = (
            self.i18n.get('reader_prompt_edit', 'Edit'),
            self.i18n.get('reader_prompt_done', 'Done'),
            self.i18n.get('reader_prompt_cancel', 'Cancel'),
        )
        for field in (
            getattr(self, 'reader_intro_field', None),
            getattr(self, 'reader_chars_field', None),
            getattr(self, 'reader_note_field', None),
        ):
            if field is not None:
                field.set_action_labels(*labels)

    def _commit_reader_fields(self):
        for field in (
            getattr(self, 'reader_intro_field', None),
            getattr(self, 'reader_chars_field', None),
            getattr(self, 'reader_note_field', None),
        ):
            if field is not None:
                field.commit_if_editing()

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
        
        # 保存 Random Questions 提示词
        current_random = self.random_questions_edit.toPlainText()
        default_random = get_suggestion_template(current_lang)
        
        if current_random.strip() == default_random.strip():
            prefs['random_questions'] = ''
        else:
            prefs['random_questions'] = current_random
        
        # 保存 Persona 设置
        prefs['use_persona'] = self.use_persona_checkbox.isChecked()
        current_persona = self.persona_edit.text().strip()
        
        # 定义获取 persona 默认值的函数
        def get_persona_default(lang):
            from .i18n import get_translation
            lang_i18n = get_translation(lang)
            return lang_i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
        
        default_persona = get_persona_default(current_lang)
        
        if current_persona == default_persona:
            prefs['persona'] = ''
        else:
            prefs['persona'] = current_persona

        self._commit_reader_fields()
        self._normalize_reader_texts()
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        reader_values = self._reader_prompt_values()
        intro_fallback = READER_PROMPT_INTRO_FALLBACK
        note_fallback = 'Explain this passage using the chapter context.'
        for key, checked in reader_values.items():
            if key == 'reader_prompt_intro':
                prefs[key] = self._stored_reader_text(checked, key, intro_fallback, current_lang)
            elif key == 'reader_prompt_default_question':
                prefs[key] = self._stored_reader_text(checked, key, note_fallback, current_lang)
            else:
                prefs[key] = checked
        
        prefs.commit()
        
        # 更新初始值（隐藏提示词系统：直接保存文本框内容）
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': self.use_interface_language_checkbox.isChecked(),
            'use_persona': self.use_persona_checkbox.isChecked(),
            'persona': self.persona_edit.text().strip(),
            'reader_prompt': self._reader_prompt_values(),
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
        reader_changed = self._reader_prompt_values() != self.initial_values.get('reader_prompt', {})
        
        return template_changed or random_changed or multi_changed or lang_pref_changed or persona_checkbox_changed or persona_text_changed or reader_changed
        
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
            'title_reader_prompt': ('reader_prompt_section_title', 'Reading mode'),
            'subtitle_reader_prompt': ('reader_prompt_section_subtitle',
                'Choose what is sent when you ask from the reader. The selected passage, its chapter, and the surrounding text can each be included.'),
            'label_reader_intro': ('reader_prompt_intro_label', 'Reading task'),
            'label_reader_context_chars': ('reader_prompt_context_chars', 'Characters before and after the selection'),
            'label_reader_default_note': ('reader_prompt_default_note_label', 'Default note'),
            'label_reader_preview_title': ('reader_prompt_preview_title', 'Example preview'),
            'label_reader_preview_hint': ('reader_prompt_preview_hint',
                'This preview uses a passage from Frankenstein by Mary Shelley. Checking a box adds or removes that part.'),
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
        reader_labels = {
            'reader_include_book': ('reader_include_book', 'Book information'),
            'reader_include_chapter': ('reader_include_chapter', 'Current chapter'),
            'reader_include_context': ('reader_include_context', 'Text around the selection'),
            'reader_include_selection': ('reader_include_selection', 'Selected text'),
            'reader_include_note': ('reader_include_note', 'Your note'),
        }
        for key, box in getattr(self, 'reader_prompt_checks', {}).items():
            label_key, fallback = reader_labels[key]
            box.setText(self.i18n.get(label_key, fallback))
        self._apply_reader_action_labels()
        if hasattr(self, 'persona_edit'):
            self.persona_edit.setPlaceholderText(
                self.i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
            )
        
        # 更新语言指令显示
        self.update_language_instruction_display()
        
        # 获取当前语言
        current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
        from .config import get_prefs
        prefs = get_prefs()
        
        # 重新加载提示词模板（保留用户自定义内容）
        # 如果当前内容是默认模板，则切换到新语言的默认模板
        # 如果是用户自定义内容，则保留
        
        # Ask 提示词
        current_template = self.template_edit.toPlainText()
        if self._is_default_value_from_any_language(current_template, get_default_template):
            self.template_edit.setPlainText(get_default_template(current_lang))
        
        # Random Questions 提示词
        current_random = self.random_questions_edit.toPlainText()
        if self._is_default_value_from_any_language(current_random, get_suggestion_template):
            self.random_questions_edit.setPlainText(get_suggestion_template(current_lang))
        
        # Multi-Book 提示词
        current_multi = self.multi_book_template_edit.toPlainText()
        if self._is_default_value_from_any_language(current_multi, get_multi_book_template):
            self.multi_book_template_edit.setPlainText(get_multi_book_template(current_lang))
        
        # Persona
        def get_persona_default(lang):
            from .i18n import get_translation
            lang_i18n = get_translation(lang)
            return lang_i18n.get('persona_placeholder', 'As a researcher, I want to research through book data.')
        
        current_persona = self.persona_edit.text().strip()
        if self._is_default_value_from_any_language(current_persona, get_persona_default):
            self.persona_edit.setText(get_persona_default(current_lang))
        
        # 更新 placeholder
        self.persona_edit.setPlaceholderText(get_persona_default(current_lang))

        intro_fallback = READER_PROMPT_INTRO_FALLBACK
        note_fallback = 'Explain this passage using the chapter context.'
        if hasattr(self, 'reader_intro_field'):
            self.reader_intro_field.cancel_edit()
            if self._is_default_value_from_any_language(
                self.reader_intro_field.value(),
                self._reader_text_getter('reader_prompt_intro', intro_fallback),
            ):
                self.reader_intro_field.set_value(
                    self._reader_text_getter('reader_prompt_intro', intro_fallback)(current_lang)
                )
        if hasattr(self, 'reader_note_field'):
            self.reader_note_field.cancel_edit()
            if self._is_default_value_from_any_language(
                self.reader_note_field.value(),
                self._reader_text_getter('reader_prompt_default_question', note_fallback),
            ):
                self.reader_note_field.set_value(
                    self._reader_text_getter('reader_prompt_default_question', note_fallback)(current_lang)
                )
        self._refresh_reader_preview()
        
        # 更新初始值，避免误判为有变更
        # 因为切换语言后加载了新语言的默认模板，需要更新 initial_values
        self.initial_values = {
            'template': self.template_edit.toPlainText(),
            'random_questions': self.random_questions_edit.toPlainText(),
            'multi_book_template': self.multi_book_template_edit.toPlainText(),
            'use_interface_language': self.use_interface_language_checkbox.isChecked(),
            'use_persona': self.use_persona_checkbox.isChecked(),
            'persona': self.persona_edit.text().strip(),
            'reader_prompt': self._reader_prompt_values(),
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


def resolve_request_template(prefs, kind='ask'):
    """Built-in ask/multi/random prompts follow the plugin language at send time."""
    from .i18n import (
        get_all_languages,
        get_default_template,
        get_multi_book_template,
        get_suggestion_template,
    )
    from .utils import resolve_prompt_template

    lang_code = prefs.get('language', 'en') or 'en'
    if kind == 'multi':
        getter = get_multi_book_template
        key = 'multi_book_template'
        placeholders = ('{books_metadata}', '{query}')
    elif kind == 'random':
        getter = get_suggestion_template
        key = 'random_questions'
        placeholders = ('{title}', '{author}')
    else:
        getter = get_default_template
        key = 'template'
        placeholders = ('{title}', '{author}', '{query}')
    localized = getter(lang_code)
    known = [getter(code) for code in get_all_languages()]
    return resolve_prompt_template(
        prefs.get(key, ''), localized, known, placeholders
    )


def _persona_for_request(prefs):
    """Default persona follows the plugin language; a custom sentence is kept."""
    from .i18n import get_all_languages, get_translation
    from .utils import resolve_persona_text

    lang_code = prefs.get('language', 'en') or 'en'
    localized = get_translation(lang_code).get(
        'persona_placeholder',
        'As a researcher, I want to research through book data.',
    )
    known = [
        get_translation(code).get('persona_placeholder', '')
        for code in get_all_languages()
    ]
    known.append('As a researcher, I want to research through book data.')
    return resolve_persona_text(prefs.get('persona', ''), localized, known)


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
    
    # 在开头添加 persona（如果启用）。未自定义时跟随插件语言，避免英文默认句贴在中文/德文模板前。
    use_persona = prefs.get('use_persona', True)
    if use_persona:
        persona_text = _persona_for_request(prefs)
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
