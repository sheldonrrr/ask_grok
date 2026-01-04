#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI Manager Dialogs - 独立弹窗用于管理 AI 服务商配置
包含两个弹窗：
1. AddAIDialog - 添加新的 AI 配置
2. ManageAIDialog - 管理已配置的 AI（编辑、删除、设为默认）
"""

import copy
import logging
import uuid
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QStackedWidget, QWidget,
    QMessageBox, QSplitter, QFrame, QSizePolicy, QScrollArea,
    QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .config import get_prefs, ModelConfigWidget, get_current_model_config
from .models.base import AIProvider, DEFAULT_MODELS
from .i18n import get_translation
from .widgets import apply_button_style
from .ui_constants import (
    SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE,
    BUTTON_MIN_WIDTH, BUTTON_HEIGHT,
    get_groupbox_style, get_section_title_style, get_subtitle_style,
    get_standard_button_style, get_list_widget_style, TEXT_COLOR_SECONDARY
)

logger = logging.getLogger(__name__)


# AI Provider 显示顺序（与 config.py 保持一致）
AI_PROVIDER_ORDER = [
    ('openai', AIProvider.AI_OPENAI),
    ('anthropic', AIProvider.AI_ANTHROPIC),
    ('gemini', AIProvider.AI_GEMINI),
    ('grok', AIProvider.AI_GROK),
    ('deepseek', AIProvider.AI_DEEPSEEK),
    ('nvidia', AIProvider.AI_NVIDIA),
    ('nvidia_free', AIProvider.AI_NVIDIA_FREE),  # 免费通道放在 Nvidia 后面
    ('perplexity', AIProvider.AI_PERPLEXITY),
    ('openrouter', AIProvider.AI_OPENROUTER),
    ('ollama', AIProvider.AI_OLLAMA),
    ('custom', AIProvider.AI_CUSTOM),
]


def generate_config_id():
    """生成唯一的配置 ID"""
    return str(uuid.uuid4())[:8]


def get_display_name_with_model(provider_name, model_name):
    """生成显示名称：Provider + Model"""
    if model_name:
        return f"{provider_name} - {model_name}"
    return provider_name


# ============================================================
# AddAIDialog - 添加新的 AI 配置
# ============================================================
class AddAIDialog(QDialog):
    """添加 AI 弹窗 - 选择 Provider 并配置"""
    
    config_changed = pyqtSignal()
    
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        
        if i18n is None:
            prefs = get_prefs()
            lang = prefs.get('language', 'en')
            self.i18n = get_translation(lang)
        else:
            self.i18n = i18n
        
        self.current_provider_id = None
        self.model_widget = None
        
        self.setup_ui()
        self.load_provider_list()
        
        # 默认选中第一项
        if self.provider_list.count() > 0:
            self.provider_list.setCurrentRow(0)
    
    def setup_ui(self):
        """设置 UI"""
        self.setWindowTitle(self.i18n.get('add_ai_title', 'Add AI Provider'))
        self.setMinimumSize(700, 600)
        self.resize(750, 680)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(SPACING_MEDIUM)
        main_layout.setContentsMargins(PADDING_LARGE, PADDING_LARGE, PADDING_LARGE, PADDING_LARGE)
        
        # 使用 QSplitter 分割左右
        splitter = QSplitter(Qt.Horizontal)
        
        # ========== 左侧：Provider 列表 ==========
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, SPACING_MEDIUM, 0)
        left_layout.setSpacing(SPACING_SMALL)
        
        # 标题
        provider_label = QLabel(self.i18n.get('select_provider', 'Select AI Provider'))
        provider_label.setStyleSheet("font-weight: bold; font-size: 1.1em;")
        left_layout.addWidget(provider_label)
        
        # Provider 列表
        self.provider_list = QListWidget()
        self.provider_list.setStyleSheet(get_list_widget_style())
        self.provider_list.currentItemChanged.connect(self.on_provider_selected)
        left_layout.addWidget(self.provider_list)
        
        splitter.addWidget(left_widget)
        
        # ========== 右侧：配置面板 ==========
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(SPACING_SMALL)
        
        # 配置面板标题
        self.config_title = QLabel(self.i18n.get('configuration', 'Configuration'))
        self.config_title.setStyleSheet("font-weight: bold; font-size: 1.1em;")
        right_layout.addWidget(self.config_title)
        
        # 配置面板容器
        self.config_container = QScrollArea()
        self.config_container.setWidgetResizable(True)
        self.config_container.setFrameShape(QFrame.NoFrame)
        
        # 空态提示
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_label = QLabel(self.i18n.get('select_provider_hint', 'Select a provider from the list'))
        empty_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 1em;")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_label)
        self.config_container.setWidget(self.empty_widget)
        
        right_layout.addWidget(self.config_container, 1)
        
        splitter.addWidget(right_widget)
        
        # 设置 splitter 比例
        splitter.setSizes([220, 480])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter, 1)
        
        # ========== 底部按钮 ==========
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SPACING_SMALL)
        button_layout.addStretch()
        
        # 取消按钮（使用默认样式）
        cancel_button = QPushButton(self.i18n.get('cancel', 'Cancel'))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # 添加按钮（使用默认样式）
        self.add_button = QPushButton(self.i18n.get('add_ai_button', 'Add'))
        self.add_button.clicked.connect(self.on_add_clicked)
        self.add_button.setEnabled(False)
        button_layout.addWidget(self.add_button)
        
        main_layout.addLayout(button_layout)
    
    def retranslate_ui(self):
        """更新界面文字（语言切换时调用）"""
        self.setWindowTitle(self.i18n.get('add_ai_title', 'Add AI Provider'))
        
        # 更新左侧标题
        for label in self.findChildren(QLabel):
            if label.styleSheet() and 'font-weight: bold' in label.styleSheet():
                # 这是标题标签
                if label.parent() == self.findChild(QWidget):  # 左侧标题
                    label.setText(self.i18n.get('select_provider', 'Select AI Provider'))
                    break
        
        # 更新配置面板标题
        if hasattr(self, 'config_title'):
            # 保持当前显示的 provider 名称
            current_text = self.config_title.text()
            if ' ' in current_text:
                provider_name = current_text.split(' ')[0]
                self.config_title.setText(f"{provider_name} {self.i18n.get('configuration', 'Configuration')}")
            else:
                self.config_title.setText(self.i18n.get('configuration', 'Configuration'))
        
        # 更新按钮文本
        if hasattr(self, 'add_button'):
            self.add_button.setText(self.i18n.get('add_ai_button', 'Add'))
        
        # 更新空态提示
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QWidget) and widget.layout():
                for i in range(widget.layout().count()):
                    item = widget.layout().itemAt(i)
                    if item and isinstance(item.widget(), QLabel):
                        label = item.widget()
                        if 'Select a provider' in label.text() or '从列表中选择' in label.text():
                            label.setText(self.i18n.get('select_provider_hint', 'Select a provider from the list'))
    
    def load_provider_list(self):
        """加载 Provider 列表"""
        self.provider_list.clear()
        
        for provider_id, provider_enum in AI_PROVIDER_ORDER:
            if provider_enum not in DEFAULT_MODELS:
                continue
            
            model_config = DEFAULT_MODELS[provider_enum]
            item = QListWidgetItem(model_config.display_name)
            item.setData(Qt.UserRole, provider_id)
            self.provider_list.addItem(item)
    
    def on_provider_selected(self, current, previous):
        """选中 Provider 时显示配置面板"""
        if current is None:
            return
        
        provider_id = current.data(Qt.UserRole)
        self.current_provider_id = provider_id
        
        # 获取默认配置
        provider_enum = None
        for pid, penum in AI_PROVIDER_ORDER:
            if pid == provider_id:
                provider_enum = penum
                break
        
        if provider_enum is None or provider_enum not in DEFAULT_MODELS:
            return
        
        default_config = DEFAULT_MODELS[provider_enum]
        
        # 创建空配置
        config = {
            'api_key': '',
            'api_base_url': default_config.default_api_base_url,
            'model': default_config.default_model_name,
            'display_name': default_config.display_name,
            'enabled': True,
            'is_configured': False,
            'enable_streaming': True
        }
        
        # 创建 ModelConfigWidget
        if self.model_widget:
            self.model_widget.deleteLater()
        
        self.model_widget = ModelConfigWidget(provider_id, config, self.i18n, parent=self)
        self.config_container.setWidget(self.model_widget)
        
        # 更新标题
        config_text = self.i18n.get('configuration', 'Configuration')
        self.config_title.setText(f"{default_config.display_name} {config_text}")
        
        # 启用添加按钮
        self.add_button.setEnabled(True)
    
    def on_add_clicked(self):
        """点击添加按钮"""
        if not self.current_provider_id or not self.model_widget:
            return
        
        # 获取配置
        config = self.model_widget.get_config()
        
        # 验证必填字段（Ollama 不需要 API Key）
        if self.current_provider_id != 'ollama':
            # Grok 使用 auth_token，其他使用 api_key
            key_field = 'auth_token' if self.current_provider_id == 'grok' else 'api_key'
            api_key = config.get(key_field, '').strip()
            if not api_key:
                QMessageBox.warning(
                    self,
                    self.i18n.get('warning', 'Warning'),
                    self.i18n.get('api_key_required', 'API Key is required.')
                )
                return
        
        # 生成配置 ID（使用模型名称）
        # 格式：provider_id 或 provider_id_model_name（如果有多个配置）
        model_name = config.get('model', '').strip()
        
        # 检查是否已有同一 provider 的配置
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        existing_provider_configs = [k for k in models_config.keys() if k.startswith(f"{self.current_provider_id}_") or k == self.current_provider_id]
        
        if existing_provider_configs:
            # 已有配置，使用 provider_model 格式
            # 清理模型名称中的特殊字符，只保留字母、数字、点、冒号和连字符
            safe_model_name = ''.join(c for c in model_name if c.isalnum() or c in '.:- ')
            safe_model_name = safe_model_name.replace(' ', '_')
            config_id = f"{self.current_provider_id}_{safe_model_name}"
        else:
            # 第一个配置，直接使用 provider_id
            config_id = self.current_provider_id
        
        # 标记为已配置
        config['is_configured'] = True
        config['provider_id'] = self.current_provider_id  # 记录原始 provider_id
        
        # 保存配置
        models_config[config_id] = config
        prefs['models'] = models_config
        
        # 如果是第一个配置，设为默认
        configured_count = sum(1 for c in models_config.values() if c.get('is_configured', False))
        if configured_count == 1:
            prefs['selected_model'] = config_id
        
        prefs.commit()
        
        logger.info(f"[AddAI] Added new config: {config_id}")
        
        # 发出信号
        self.config_changed.emit()
        
        # 关闭弹窗
        self.accept()


# ============================================================
# ManageAIDialog - 管理已配置的 AI
# ============================================================
class ManageAIDialog(QDialog):
    """管理 AI 弹窗 - 编辑、删除、设为默认"""
    
    config_changed = pyqtSignal()
    
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        
        if i18n is None:
            prefs = get_prefs()
            lang = prefs.get('language', 'en')
            self.i18n = get_translation(lang)
        else:
            self.i18n = i18n
        
        self.current_config_id = None
        self.model_widget = None
        
        self.setup_ui()
        self.load_configured_list()
        
        # 默认选中第一项
        if self.config_list.count() > 0:
            self.config_list.setCurrentRow(0)
    
    def setup_ui(self):
        """设置 UI"""
        self.setWindowTitle(self.i18n.get('manage_ai_title', 'Manage Configured AI'))
        self.setMinimumSize(750, 600)
        self.resize(800, 680)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(SPACING_MEDIUM)
        main_layout.setContentsMargins(PADDING_LARGE, PADDING_LARGE, PADDING_LARGE, PADDING_LARGE)
        
        # 使用 QSplitter 分割左右
        splitter = QSplitter(Qt.Horizontal)
        
        # ========== 左侧：已配置 AI 列表 ==========
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, SPACING_MEDIUM, 0)
        left_layout.setSpacing(SPACING_SMALL)
        
        # 标题
        list_label = QLabel(self.i18n.get('configured_ai_list', 'Configured AI'))
        list_label.setStyleSheet("font-weight: bold; font-size: 1.1em;")
        left_layout.addWidget(list_label)
        
        # 已配置 AI 列表
        self.config_list = QListWidget()
        self.config_list.setStyleSheet(get_list_widget_style(with_border_bottom=True))
        self.config_list.currentItemChanged.connect(self.on_config_selected)
        left_layout.addWidget(self.config_list)
        
        splitter.addWidget(left_widget)
        
        # ========== 右侧：配置面板 ==========
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(SPACING_SMALL)
        
        # 配置面板标题
        self.config_title = QLabel(self.i18n.get('configuration', 'Configuration'))
        self.config_title.setStyleSheet("font-weight: bold; font-size: 1.1em;")
        right_layout.addWidget(self.config_title)
        
        # 配置面板容器
        self.config_container = QScrollArea()
        self.config_container.setWidgetResizable(True)
        self.config_container.setFrameShape(QFrame.NoFrame)
        
        # 空态提示
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_label = QLabel(self.i18n.get('select_ai_to_edit', 'Select an AI from the list to edit'))
        empty_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 1em;")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_label)
        self.config_container.setWidget(self.empty_widget)
        
        right_layout.addWidget(self.config_container, 1)
        
        # 操作按钮（使用默认样式）
        action_layout = QHBoxLayout()
        action_layout.setSpacing(SPACING_SMALL)
        
        # 保存按钮
        self.save_button = QPushButton(self.i18n.get('save_ai_config', 'Save'))
        self.save_button.clicked.connect(self.on_save)
        self.save_button.setEnabled(False)
        action_layout.addWidget(self.save_button)
        
        # 删除按钮
        self.delete_button = QPushButton(self.i18n.get('delete_ai', 'Delete'))
        self.delete_button.clicked.connect(self.on_delete)
        self.delete_button.setEnabled(False)
        action_layout.addWidget(self.delete_button)
        
        action_layout.addStretch()
        right_layout.addLayout(action_layout)
        
        splitter.addWidget(right_widget)
        
        # 设置 splitter 比例
        splitter.setSizes([260, 490])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter, 1)
        
        # ========== 底部按钮 ==========
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_button = QPushButton(self.i18n.get('close_button', 'Close'))
        close_button.clicked.connect(self.accept)
        bottom_layout.addWidget(close_button)
        
        main_layout.addLayout(bottom_layout)
    
    def retranslate_ui(self):
        """更新界面文字（语言切换时调用）"""
        self.setWindowTitle(self.i18n.get('manage_ai_title', 'Manage Configured AI'))
        
        # 更新左侧标题
        for label in self.findChildren(QLabel):
            if label.styleSheet() and 'font-weight: bold' in label.styleSheet():
                # 这是标题标签
                if label.parent() == self.findChild(QWidget):  # 左侧标题
                    label.setText(self.i18n.get('configured_ai_list', 'Configured AI'))
                    break
        
        # 更新配置面板标题
        if hasattr(self, 'config_title'):
            # 保持当前显示的 provider 名称
            current_text = self.config_title.text()
            if ' ' in current_text:
                provider_name = current_text.split(' ')[0]
                self.config_title.setText(f"{provider_name} {self.i18n.get('configuration', 'Configuration')}")
            else:
                self.config_title.setText(self.i18n.get('configuration', 'Configuration'))
        
        # 更新按钮文本
        if hasattr(self, 'save_button'):
            self.save_button.setText(self.i18n.get('save_ai_config', 'Save'))
        if hasattr(self, 'delete_button'):
            self.delete_button.setText(self.i18n.get('delete_ai', 'Delete'))
        
        # 更新空态提示
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QWidget) and widget.layout():
                for i in range(widget.layout().count()):
                    item = widget.layout().itemAt(i)
                    if item and isinstance(item.widget(), QLabel):
                        label = item.widget()
                        if 'Select an AI' in label.text() or '从列表中选择' in label.text():
                            label.setText(self.i18n.get('select_ai_to_edit', 'Select an AI from the list to edit'))
    
    def load_configured_list(self):
        """加载已配置的 AI 列表"""
        self.config_list.clear()
        
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        selected_model = prefs.get('selected_model', '')
        
        # 收集已配置的 AI
        configured_items = []
        for config_id, config in models_config.items():
            if not config.get('is_configured', False):
                continue
            
            # 获取 provider_id（兼容旧数据）
            provider_id = config.get('provider_id', config_id.split('_')[0] if '_' in config_id else config_id)
            
            # 获取显示名称
            provider_name = config.get('display_name', provider_id)
            model_name = config.get('model', '')
            display_text = get_display_name_with_model(provider_name, model_name)
            
            configured_items.append((config_id, display_text, config_id == selected_model))
        
        # 按 provider 排序
        def sort_key(item):
            config_id = item[0]
            provider_id = config_id.split('_')[0] if '_' in config_id else config_id
            for i, (pid, _) in enumerate(AI_PROVIDER_ORDER):
                if pid == provider_id:
                    return i
            return 999
        
        configured_items.sort(key=sort_key)
        
        # 检查重复名称，添加序号
        name_counts = {}
        for i, (config_id, display_text, is_default) in enumerate(configured_items):
            if display_text in name_counts:
                name_counts[display_text] += 1
                new_display_text = f"{display_text} ({name_counts[display_text]})"
                configured_items[i] = (config_id, new_display_text, is_default)
            else:
                name_counts[display_text] = 1
        
        # 如果有重复，第一个也需要加序号
        for display_text, count in name_counts.items():
            if count > 1:
                for i, (config_id, text, is_default) in enumerate(configured_items):
                    if text == display_text:
                        configured_items[i] = (config_id, f"{display_text} (1)", is_default)
                        break
        
        # 添加到列表（使用自定义 widget 实现两行显示）
        for config_id, display_text, is_default in configured_items:
            # 分离服务商和模型名
            if ' - ' in display_text:
                parts = display_text.split(' - ', 1)
                provider_text = parts[0]
                model_text = parts[1]
            else:
                provider_text = display_text
                model_text = ''
            
            item = QListWidgetItem()
            item.setData(Qt.UserRole, config_id)
            
            # 创建自定义 widget
            from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
            from PyQt5.QtCore import QSize
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            # 使用 ui_constants 中的内边距，确保文本不被截断
            # 底部需要更多空间来显示小写字母的下降部分（如 y, g, p）
            item_layout.setContentsMargins(
                int(PADDING_SMALL * 0.8),  # 左
                PADDING_SMALL,              # 上
                int(PADDING_SMALL * 0.8),  # 右
                PADDING_SMALL + 8           # 下（额外增加8px确保下降字母不被截断）
            )
            item_layout.setSpacing(4)  # 增加服务商和模型之间的间距
            
            # 服务商名称（粗体，基准字体大小）
            provider_label = QLabel(provider_text)
            provider_label.setStyleSheet("font-weight: bold; font-size: 1em;")
            item_layout.addWidget(provider_label)
            
            # 模型名称（基准字体大小，支持换行）
            if model_text:
                model_label = QLabel(model_text)
                model_label.setWordWrap(True)
                model_label.setStyleSheet("font-size: 1em;")
                item_layout.addWidget(model_label)
            
            self.config_list.addItem(item)
            self.config_list.setItemWidget(item, item_widget)
            
            # 设置 item 的 sizeHint，确保高度足够显示所有内容
            item_widget.adjustSize()
            # 额外增加高度确保下降字母不被截断
            item.setSizeHint(QSize(item_widget.sizeHint().width(), item_widget.sizeHint().height() + 8))
        
        # 空态
        if self.config_list.count() == 0:
            hint_item = QListWidgetItem(self.i18n.get('no_configured_ai', 'No AI configured yet'))
            hint_item.setData(Qt.UserRole, None)
            hint_item.setFlags(hint_item.flags() & ~Qt.ItemIsSelectable)
            self.config_list.addItem(hint_item)
    
    def on_config_selected(self, current, previous):
        """选中配置时显示编辑面板"""
        if current is None:
            return
        
        config_id = current.data(Qt.UserRole)
        if config_id is None:
            self.config_container.setWidget(self.empty_widget)
            self.save_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            return
        
        self.current_config_id = config_id
        
        # 获取配置
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        config = models_config.get(config_id, {})
        selected_model = prefs.get('selected_model', '')
        
        # 获取 provider_id
        provider_id = config.get('provider_id', config_id.split('_')[0] if '_' in config_id else config_id)
        
        # 创建 ModelConfigWidget
        if self.model_widget:
            self.model_widget.deleteLater()
        
        self.model_widget = ModelConfigWidget(provider_id, config, self.i18n, parent=self)
        self.config_container.setWidget(self.model_widget)
        
        # 更新标题
        provider_name = config.get('display_name', provider_id)
        config_text = self.i18n.get('configuration', 'Configuration')
        self.config_title.setText(f"{provider_name} {config_text}")
        
        # 更新按钮状态
        self.save_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def on_save(self):
        """保存配置"""
        if not self.current_config_id or not self.model_widget:
            return
        
        config = self.model_widget.get_config()
        config['is_configured'] = True
        
        # 保留 provider_id
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        old_config = models_config.get(self.current_config_id, {})
        config['provider_id'] = old_config.get('provider_id', self.current_config_id.split('_')[0])
        
        models_config[self.current_config_id] = config
        prefs['models'] = models_config
        prefs.commit()
        
        # 刷新列表
        self.load_configured_list()
        self._select_config(self.current_config_id)
        
        self.config_changed.emit()
        
        display_name = config.get('display_name', self.current_config_id)
        QMessageBox.information(
            self,
            self.i18n.get('success', 'Success'),
            self.i18n.get('ai_config_saved_success', '{name} configuration saved successfully.').format(name=display_name)
        )
    
    def on_delete(self):
        """删除配置"""
        if not self.current_config_id:
            return
        
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        config = models_config.get(self.current_config_id, {})
        display_name = config.get('display_name', self.current_config_id)
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.i18n.get('confirm_delete_title', 'Confirm Delete'))
        msg_box.setText(self.i18n.get('confirm_delete_ai', 'Are you sure you want to delete {name}?').format(name=display_name))
        msg_box.setIcon(QMessageBox.Question)
        
        # 设置按钮文本为 i18n
        yes_button = msg_box.addButton(self.i18n.get('yes', 'Yes'), QMessageBox.YesRole)
        no_button = msg_box.addButton(self.i18n.get('no', 'No'), QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() != yes_button:
            return
        
        # 删除配置
        del models_config[self.current_config_id]
        
        # 如果删除的是默认 AI，选择另一个
        selected_model = prefs.get('selected_model', '')
        if self.current_config_id == selected_model:
            new_default = None
            for cid, cfg in models_config.items():
                if cfg.get('is_configured', False):
                    new_default = cid
                    break
            prefs['selected_model'] = new_default if new_default else ''
        
        prefs['models'] = models_config
        prefs.commit()
        
        logger.info(f"[ManageAI] Deleted config: {self.current_config_id}")
        
        # 清理
        if self.model_widget:
            self.model_widget.deleteLater()
            self.model_widget = None
        
        self.current_config_id = None
        
        # 重新创建 empty_widget（因为 QScrollArea.setWidget() 会接管所有权）
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_label = QLabel(self.i18n.get('select_ai_to_edit', 'Select an AI from the list to edit'))
        empty_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 1em;")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_label)
        
        self.config_container.setWidget(self.empty_widget)
        self.save_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        
        # 刷新列表
        self.load_configured_list()
        
        self.config_changed.emit()
    
    def _select_config(self, config_id):
        """选中指定配置"""
        for i in range(self.config_list.count()):
            item = self.config_list.item(i)
            if item.data(Qt.UserRole) == config_id:
                self.config_list.setCurrentItem(item)
                return


# ============================================================
# AIManagerDialog - 兼容性包装（保留旧接口）
# ============================================================
class AIManagerDialog(QDialog):
    """AI 管理弹窗 - 兼容性包装，现在直接打开 ManageAIDialog"""
    
    config_changed = pyqtSignal()
    
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        
        if i18n is None:
            prefs = get_prefs()
            lang = prefs.get('language', 'en')
            self.i18n = get_translation(lang)
        else:
            self.i18n = i18n
        
        # 直接使用 ManageAIDialog
        self.dialog = ManageAIDialog(parent=parent, i18n=i18n)
        self.dialog.config_changed.connect(self.config_changed.emit)
    
    def exec_(self):
        return self.dialog.exec_()
    
    def show(self):
        return self.dialog.show()
