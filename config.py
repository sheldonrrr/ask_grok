#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import logging
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, 
                            QPushButton, QHBoxLayout, QFormLayout, QGroupBox, QScrollArea, QSizePolicy,
                            QFrame, QCheckBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QEvent
from PyQt5.QtGui import QFontMetrics
from .models.grok import GrokModel
from .models.gemini import GeminiModel
from .models.deepseek import DeepseekModel
from .models.custom import CustomModel
from .models.openai import OpenAIModel
from .models.anthropic import AnthropicModel
from .models.nvidia import NvidiaModel
from .models.openrouter import OpenRouterModel
from .models.ollama import OllamaModel
from calibre.utils.config import JSONConfig

from .i18n import get_default_template, get_translation, get_suggestion_template, get_multi_book_template, get_all_languages
from .models.base import AIProvider, ModelConfig, DEFAULT_MODELS, AIModelFactory, BaseAIModel
from .utils import mask_api_key, mask_api_key_in_text, safe_log_config
from .widgets import NoScrollComboBox, apply_button_style
from .ui_constants import (
    SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
    MARGIN_MEDIUM, PADDING_MEDIUM,
    get_groupbox_style, get_separator_style
)

# 初始化日志
logger = logging.getLogger(__name__)


# 创建配置对象
prefs = JSONConfig('plugins/ask_ai_plugin')

# 从i18n模块获取支持的语言列表
# 将字典转换为列表格式 [(code, name), ...]
_languages_dict = get_all_languages()
SUPPORTED_LANGUAGES = [(code, name) for code, name in _languages_dict.items()]
# 确保英语作为默认语言排在第一位
SUPPORTED_LANGUAGES.sort(key=lambda x: 0 if x[0] == 'en' else 1)

# 获取AI服务商配置的函数
def get_current_model_config(provider: AIProvider) -> ModelConfig:
    """获取指定AI服务商的模型配置"""
    return DEFAULT_MODELS.get(provider)

# 获取AI服务商配置
GROK_CONFIG = get_current_model_config(AIProvider.AI_GROK)
GEMINI_CONFIG = get_current_model_config(AIProvider.AI_GEMINI)
DEEPSEEK_CONFIG = get_current_model_config(AIProvider.AI_DEEPSEEK)
CUSTOM_CONFIG = get_current_model_config(AIProvider.AI_CUSTOM)
OPENAI_CONFIG = get_current_model_config(AIProvider.AI_OPENAI)
ANTHROPIC_CONFIG = get_current_model_config(AIProvider.AI_ANTHROPIC)
NVIDIA_CONFIG = get_current_model_config(AIProvider.AI_NVIDIA)
OPENROUTER_CONFIG = get_current_model_config(AIProvider.AI_OPENROUTER)
OLLAMA_CONFIG = get_current_model_config(AIProvider.AI_OLLAMA)

# 默认配置
prefs.defaults['selected_model'] = 'grok'  # 当前选中的模型
prefs.defaults['models'] = {
    'grok': {
        'auth_token': '',
        'api_base_url': GROK_CONFIG.default_api_base_url,
        'model': GROK_CONFIG.default_model_name,
        'display_name': GROK_CONFIG.display_name,
        'enabled': True
    },
    'gemini': {
        'api_key': '',
        'api_base_url': GEMINI_CONFIG.default_api_base_url,
        'model': GEMINI_CONFIG.default_model_name,
        'display_name': GEMINI_CONFIG.display_name,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'deepseek': {
        'api_key': '',
        'api_base_url': DEEPSEEK_CONFIG.default_api_base_url,
        'model': DEEPSEEK_CONFIG.default_model_name,
        'display_name': DEEPSEEK_CONFIG.display_name,        
        'enabled': False  # 默认不启用，需要用户配置
    },
    'custom': {
        'api_key': '',
        'api_base_url': CUSTOM_CONFIG.default_api_base_url,
        'model': CUSTOM_CONFIG.default_model_name,
        'display_name': CUSTOM_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'openai': {
        'api_key': '',
        'api_base_url': OPENAI_CONFIG.default_api_base_url,
        'model': OPENAI_CONFIG.default_model_name,
        'display_name': OPENAI_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'anthropic': {
        'api_key': '',
        'api_base_url': ANTHROPIC_CONFIG.default_api_base_url,
        'model': ANTHROPIC_CONFIG.default_model_name,
        'display_name': ANTHROPIC_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'nvidia': {
        'api_key': '',
        'api_base_url': NVIDIA_CONFIG.default_api_base_url,
        'model': NVIDIA_CONFIG.default_model_name,
        'display_name': NVIDIA_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'openrouter': {
        'api_key': '',
        'api_base_url': OPENROUTER_CONFIG.default_api_base_url,
        'model': OPENROUTER_CONFIG.default_model_name,
        'display_name': OPENROUTER_CONFIG.display_name,
        'enable_streaming': True,
        'http_referer': '',  # Optional: for ranking on OpenRouter
        'x_title': 'Ask AI Plugin',  # Optional: app name
        'enabled': False  # 默认不启用，需要用户配置
    },
    'ollama': {
        'api_key': '',  # Optional for Ollama (local service)
        'api_base_url': OLLAMA_CONFIG.default_api_base_url,
        'model': OLLAMA_CONFIG.default_model_name,
        'display_name': OLLAMA_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    }
}
prefs.defaults['template'] = get_default_template('en')
prefs.defaults['multi_book_template'] = """以下是关于多本书籍的信息：

{books_metadata}

用户问题：{query}

请基于以上书籍信息回答问题。"""
prefs.defaults['language'] = 'en'
prefs.defaults['ask_dialog_width'] = 800
prefs.defaults['ask_dialog_height'] = 600
prefs.defaults['random_questions'] = {}
prefs.defaults['request_timeout'] = 60  # Default timeout in seconds
prefs.defaults['parallel_ai_count'] = 1  # Number of parallel AI requests (1-4)
prefs.defaults['cached_models'] = {}  # Cached model lists for each AI provider

# Export settings
prefs.defaults['enable_default_export_folder'] = False  # Whether to export to default folder
prefs.defaults['default_export_folder'] = ''  # Default export folder path
prefs.defaults['copy_mode'] = 'response'  # Copy mode: 'response' or 'qa'
prefs.defaults['export_mode'] = 'current'  # Export mode: 'current' or 'history'

def get_prefs(force_reload=False):
    """获取配置
    
    Args:
        force_reload: 是否强制重新加载配置文件
    """
    # 如果需要强制重新加载
    if force_reload and isinstance(prefs, JSONConfig):
        prefs.refresh()
    
    # 确保模板不为空，如果为空则使用当前语言的默认模板
    if not prefs['template']:
        prefs['template'] = get_default_template(prefs.get('language', 'en'))
    
    # 确保语言键存在，如果不存在则使用默认值 'en'
    if 'language' not in prefs:
        prefs['language'] = 'en'
    
    # 确保 models 键存在
    if 'models' not in prefs:
        prefs['models'] = {}
    
    # 确保 selected_model 键存在
    if 'selected_model' not in prefs:
        prefs['selected_model'] = 'grok'
    
    # 确保 request_timeout 键存在
    if 'request_timeout' not in prefs:
        prefs['request_timeout'] = 60
    
    # 确保 parallel_ai_count 键存在
    if 'parallel_ai_count' not in prefs:
        prefs['parallel_ai_count'] = 1
    
    # 确保默认模型配置存在
    if 'grok' not in prefs['models']:
        prefs['models']['grok'] = {
            'auth_token': '',
            'api_base_url': GROK_CONFIG.default_api_base_url,
            'model': GROK_CONFIG.default_model_name,
            'display_name': GROK_CONFIG.display_name  # 设置固定的显示名称
        }
    
    # 不再强制更新模型名称，保留用户的自定义设置
    # 只有当模型名称不存在时，才使用默认值
    
    # 自动判断并设置 is_configured 字段（用于已有配置的兼容性）
    for model_id, model_config in prefs['models'].items():
        if 'is_configured' not in model_config:
            # 判断是否已配置
            if model_id == 'ollama':
                # Ollama 不需要 API Key
                has_auth = True
            else:
                # 其他模型需要 API Key
                api_key_field = 'auth_token' if model_id == 'grok' else 'api_key'
                has_auth = bool(model_config.get(api_key_field, '').strip())
            
            # 检查是否有模型名称
            has_model = bool(model_config.get('model', '').strip())
            
            # 设置 is_configured 标志
            model_config['is_configured'] = has_auth and has_model
    
    return prefs


class ModelConfigWidget(QWidget):
    """单个模型配置控件"""
    config_changed = pyqtSignal()
    
    def __init__(self, model_id, config, i18n, parent=None):
        super().__init__(parent)
        self.model_id = model_id
        self.config = config
        self.i18n = i18n
        self.initial_values = {}
        
        # 加载动画实例（在 setup_ui 后初始化）
        self.load_models_animation = None
        
        # 按钮状态标志：是否已加载模型列表
        self._models_loaded = False
        
        # 初始化标志，用于避免初始化时触发变化检测
        self._is_initializing = True
        self.setup_ui()
        self._is_initializing = False
    
    def setup_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建表单布局
        model_layout = QFormLayout()
        model_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        model_layout.setHorizontalSpacing(SPACING_MEDIUM)  # 标签和字段间距
        model_layout.setVerticalSpacing(SPACING_SMALL)     # 行间距
        model_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 标签右对齐
        model_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addLayout(model_layout)
        
        # 计算基础宽度（减少字符数，避免超出窗口宽度）
        font_metrics = QFontMetrics(self.font())
        base_width = font_metrics.width('X' * 35)  # 基于35个字符的宽度，避免水平滚动条
        
        # 获取模型配置
        model_config = None
        api_key_field_name = 'api_key'
        
        # 根据模型ID获取对应的AIProvider和ModelConfig
        if self.model_id == 'grok':
            provider = AIProvider.AI_GROK
            model_config = get_current_model_config(provider)
            api_key_field_name = 'auth_token'
        elif self.model_id == 'gemini':
            provider = AIProvider.AI_GEMINI
            model_config = get_current_model_config(provider)
        elif self.model_id == 'deepseek':
            provider = AIProvider.AI_DEEPSEEK
            model_config = get_current_model_config(provider)
        elif self.model_id == 'custom':
            provider = AIProvider.AI_CUSTOM
            model_config = get_current_model_config(provider)
        elif self.model_id == 'openai':
            provider = AIProvider.AI_OPENAI
            model_config = get_current_model_config(provider)
        elif self.model_id == 'anthropic':
            provider = AIProvider.AI_ANTHROPIC
            model_config = get_current_model_config(provider)
        elif self.model_id == 'nvidia':
            provider = AIProvider.AI_NVIDIA
            model_config = get_current_model_config(provider)
        elif self.model_id == 'openrouter':
            provider = AIProvider.AI_OPENROUTER
            model_config = get_current_model_config(provider)
        elif self.model_id == 'ollama':
            provider = AIProvider.AI_OLLAMA
            model_config = get_current_model_config(provider)
        
        if model_config:
            # Nvidia 特殊提示：免费 API Key 信息
            if self.model_id == 'nvidia':
                info_label = QLabel(self.i18n.get('nvidia_free_info', 
                    'New users get 6 months free API access - No credit card required'))
                info_label.setStyleSheet("color: palette(mid); padding: 5px 0;")
                info_label.setWordWrap(True)
                main_layout.addWidget(info_label)
            
            # API Key/Token 输入框（Ollama 不需要）
            if self.model_id != 'ollama':
                self.api_key_edit = QTextEdit(self)
                self.api_key_edit.setPlainText(self.config.get(api_key_field_name, ''))
                self.api_key_edit.textChanged.connect(self.on_api_key_changed)
                self.api_key_edit.setMaximumHeight(62)
                self.api_key_edit.setMinimumWidth(base_width)  # 基于字体大小设置宽度
                model_layout.addRow(self.i18n.get('api_key_label', 'API Key:'), self.api_key_edit)
            else:
                # Ollama 不需要 API Key，创建一个空的占位符以保持代码兼容性
                self.api_key_edit = None
            
            # 添加分隔线
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Plain)
            separator.setStyleSheet("border-top: 1px dashed palette(mid); margin-top: 15px; margin-bottom: 15px; background: none;")
            separator.setMinimumHeight(10)
            main_layout.addWidget(separator)
            
            # API Base URL 输入框
            self.api_base_edit = QLineEdit(self)
            self.api_base_edit.setText(self.config.get('api_base_url', model_config.default_api_base_url))
            self.api_base_edit.textChanged.connect(self.on_config_changed)
            self.api_base_edit.setPlaceholderText(self.i18n.get('base_url_placeholder', 'Default: {default_api_base_url}').format(
                default_api_base_url=model_config.default_api_base_url
            ))
            self.api_base_edit.setMinimumHeight(25)  # 设置最小高度
            self.api_base_edit.setMinimumWidth(base_width)  # 设置最小宽度
            model_layout.addRow(self.i18n.get('base_url_label', 'Base URL:'), self.api_base_edit)
            
            # 模型选择区域：下拉框 + 加载按钮
            model_select_layout = QHBoxLayout()
            
            # 模型下拉框
            self.model_combo = NoScrollComboBox(self)
            self.model_combo.setMinimumWidth(int(base_width * 0.7))
            self.model_combo.setEditable(False)
            self.model_combo.currentTextChanged.connect(self.on_model_combo_changed)
            model_select_layout.addWidget(self.model_combo)
            
            # 添加占位符选项
            placeholder_text = self.i18n.get('select_model', '-- No Model --')
            self.model_combo.addItem(placeholder_text)
            
            # 从缓存加载模型列表
            prefs = get_prefs()
            cached_models = prefs.get('cached_models', {})
            if self.model_id in cached_models and cached_models[self.model_id]:
                self.model_combo.addItems(cached_models[self.model_id])
            else:
                # 没有缓存时，添加提示项
                hint_text = self.i18n.get('request_model_list', 'Please request model list')
                self.model_combo.addItem(hint_text)
                # 禁用提示项
                model = self.model_combo.model()
                item = model.item(1)  # 第二项是提示项
                if item:
                    item.setEnabled(False)
            
            # 添加按钮之间的间距
            model_select_layout.addSpacing(8)
            
            # 加载模型按钮
            self.load_models_button = QPushButton(self.i18n.get('load_models_list', 'Load Model List'), self)
            self.load_models_button.clicked.connect(self.on_load_models_clicked)
            # 增加按钮宽度以适应不同字体大小（16px、14px等）
            apply_button_style(self.load_models_button, min_width=200)
            model_select_layout.addWidget(self.load_models_button)
            
            # 初始化加载动画
            from .ui_constants import ButtonLoadingAnimation
            self.load_models_animation = ButtonLoadingAnimation(
                button=self.load_models_button,
                loading_text=self.i18n.get('loading_models_text', 'Loading'),
                original_text=self.i18n.get('load_models_list', 'Load Model List')
            )
            
            # 初始化按钮状态
            self.update_load_models_button_state()
            
            model_layout.addRow(self.i18n.get('model_label', 'Model:'), model_select_layout)
            
            # 使用自定义模型名称选项
            self.use_custom_model_checkbox = QCheckBox(self.i18n.get('use_custom_model', 'Use custom model name'))
            self.use_custom_model_checkbox.stateChanged.connect(self.on_custom_model_toggled)
            model_layout.addRow("", self.use_custom_model_checkbox)
            
            # 自定义模型名称输入框（始终显示，初始禁用）
            self.custom_model_input = QLineEdit(self)
            self.custom_model_input.setMinimumWidth(base_width)
            self.custom_model_input.setMinimumHeight(25)  # 设置最小高度
            self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))
            self.custom_model_input.textChanged.connect(self.on_config_changed)
            self.custom_model_input.setEnabled(False)  # 初始禁用（灰色）
            # 保存这一行的索引
            self.custom_model_row = model_layout.rowCount()
            model_layout.addRow("", self.custom_model_input)
            
            # 加载模型配置（填充下拉框或自定义输入）
            self.load_model_config()

            # 流式传输选项
            self.enable_streaming_checkbox = QCheckBox(self.i18n.get('model_enable_streaming', 'Enable Streaming'))
            self.enable_streaming_checkbox.setChecked(self.config.get('enable_streaming', True))
            self.enable_streaming_checkbox.stateChanged.connect(self.on_config_changed)
            model_layout.addRow("", self.enable_streaming_checkbox)
            
            # 添加重置按钮（红色警告样式）
            reset_button = QPushButton(self.i18n.get('reset_current_ai', 'Reset Current AI to Default'))
            reset_button.setObjectName(f"reset_button_{self.model_id}")  # 设置明确的objectName
            reset_button.setProperty('isResetButton', True)  # 添加属性标记
            reset_button.clicked.connect(self.reset_model_params)
            reset_button.setToolTip(self.i18n.get('reset_tooltip', 'Reset current AI to default values'))
            
            # 应用红色警告样式（与 Reset All Data 保持一致）
            reset_button.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            model_layout.addRow("", reset_button)
    
    def get_config(self):
        """获取当前配置"""
        import logging
        logger = logging.getLogger(__name__)
        
        config = {}
        config['enabled'] = True  # 默认启用所选模型
        
        # 获取对应的AIProvider和ModelConfig
        provider = None
        model_config = None
        
        if self.model_id == 'grok':
            provider = AIProvider.AI_GROK
            # API Key字段名称为auth_token
            config['auth_token'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'x.AI (Grok)'  # 设置固定的显示名称
        elif self.model_id == 'gemini':
            provider = AIProvider.AI_GEMINI
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'Google Gemini'  # 设置固定的显示名称
        elif self.model_id == 'deepseek':
            provider = AIProvider.AI_DEEPSEEK
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'Deepseek'  # 设置固定的显示名称
        elif self.model_id == 'custom':
            provider = AIProvider.AI_CUSTOM
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'Custom'  # 设置固定的显示名称
        elif self.model_id == 'openai':
            provider = AIProvider.AI_OPENAI
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'OpenAI'  # 设置固定的显示名称
        elif self.model_id == 'anthropic':
            provider = AIProvider.AI_ANTHROPIC
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'Anthropic (Claude)'  # 设置固定的显示名称
        elif self.model_id == 'nvidia':
            provider = AIProvider.AI_NVIDIA
            # 获取 API Key 并记录详细日志
            if hasattr(self, 'api_key_edit'):
                api_key_value = self.api_key_edit.toPlainText().strip()
                config['api_key'] = api_key_value
            else:
                config['api_key'] = ''
                logger.warning(f"[Nvidia get_config] api_key_edit 控件不存在！")
            config['display_name'] = 'Nvidia AI'  # 设置固定的显示名称
        elif self.model_id == 'openrouter':
            provider = AIProvider.AI_OPENROUTER
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'OpenRouter'  # 设置固定的显示名称
            # OpenRouter 特殊字段
            if hasattr(self, 'http_referer_edit'):
                config['http_referer'] = self.http_referer_edit.text().strip()
            if hasattr(self, 'x_title_edit'):
                config['x_title'] = self.x_title_edit.text().strip()
        elif self.model_id == 'ollama':
            provider = AIProvider.AI_OLLAMA
            # Ollama 不需要 API Key
            config['api_key'] = self.api_key_edit.toPlainText().strip() if (hasattr(self, 'api_key_edit') and self.api_key_edit) else ''
            config['display_name'] = 'Ollama (Local)'  # 设置固定的显示名称
        
        # 通用配置项
        config['api_base_url'] = self.api_base_edit.text().strip() if hasattr(self, 'api_base_edit') else ''
        
        # 模型名称配置（新逻辑：支持下拉框或自定义输入）
        if hasattr(self, 'use_custom_model_checkbox') and self.use_custom_model_checkbox.isChecked():
            # 使用自定义模型名称
            config['use_custom_model_name'] = True
            config['model'] = self.custom_model_input.text().strip() if hasattr(self, 'custom_model_input') else ''
        else:
            # 使用下拉框选中的模型
            config['use_custom_model_name'] = False
            if hasattr(self, 'model_combo'):
                current_text = self.model_combo.currentText().strip()
                # 过滤掉占位符文本，避免保存无效的模型名称
                if self._is_placeholder_text(current_text):
                    config['model'] = ''  # 占位符不保存
                else:
                    config['model'] = current_text
            else:
                config['model'] = ''
        
        # 流式传输选项（如果存在）
        if hasattr(self, 'enable_streaming_checkbox'):
            config['enable_streaming'] = self.enable_streaming_checkbox.isChecked()
        else:
            config['enable_streaming'] = True  # 默认启用
        
        # 判断是否已配置完成
        config['is_configured'] = self._is_model_configured(config)
        
        return config
    
    def _is_model_configured(self, config: dict) -> bool:
        """检查当前模型配置是否完整
        
        判断标准：
        1. 有 API Key（Ollama 除外）
        2. 有模型名称
        """
        # 检查 API Key（Ollama 不需要）
        if self.model_id == 'ollama':
            has_auth = True
        else:
            api_key_field = 'auth_token' if self.model_id == 'grok' else 'api_key'
            has_auth = bool(config.get(api_key_field, '').strip())
        
        # 检查模型名称
        has_model = bool(config.get('model', '').strip())
        
        return has_auth and has_model
    
    def on_api_key_changed(self):
        """API Key 变化时的处理"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 清除当前 AI 的模型缓存
        from .config import get_prefs
        prefs = get_prefs()
        cached_models = prefs.get('cached_models', {})
        if self.model_id in cached_models:
            del cached_models[self.model_id]
            prefs['cached_models'] = cached_models
        
        # 更新 Load Models 按钮状态
        self.update_load_models_button_state()
        
        # 触发配置变更信号
        self.on_config_changed()
    
    def on_config_changed(self):
        """配置变更处理"""
        # 如果正在初始化，不发送信号
        if hasattr(self, '_is_initializing') and self._is_initializing:
            return
        self.config_changed.emit()
    
    def update_load_models_button_state(self):
        """更新 Load Models 按钮的启用/禁用状态"""
        if not hasattr(self, 'load_models_button'):
            return
        
        # Ollama 不需要 API Key，始终可用
        if self.model_id == 'ollama':
            self.load_models_button.setEnabled(True)
            return
        
        # 其他 AI 需要检查 API Key
        api_key = self.get_api_key()
        self.load_models_button.setEnabled(bool(api_key))
    
    def _is_placeholder_text(self, text):
        """检查文本是否是占位符（基于 i18n key）
        
        Args:
            text: 要检查的文本
            
        Returns:
            bool: 如果是占位符返回 True，否则返回 False
        """
        if not text:
            return True
        
        # 获取所有可能的占位符文本（基于 i18n key）
        placeholder_keys = ['select_model', 'request_model_list']
        
        for key in placeholder_keys:
            placeholder_value = self.i18n.get(key, '')
            if text == placeholder_value:
                return True
        
        return False
    
    def _find_best_default_model(self, models):
        """智能匹配最佳默认模型
        
        Args:
            models: 模型列表
            
        Returns:
            int: 最佳匹配的模型索引（1-based，0是占位符）
        """
        import logging
        logger = logging.getLogger(__name__)
        
        if not models or len(models) == 0:
            return 0  # 返回占位符
        
        # 获取当前AI的默认模型名称
        from .models.base import AIProvider, get_current_model_config
        
        default_model_name = None
        if self.model_id == 'grok':
            provider = AIProvider.AI_GROK
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'gemini':
            provider = AIProvider.AI_GEMINI
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'deepseek':
            provider = AIProvider.AI_DEEPSEEK
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'openai':
            provider = AIProvider.AI_OPENAI
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'anthropic':
            provider = AIProvider.AI_ANTHROPIC
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'nvidia':
            provider = AIProvider.AI_NVIDIA
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'openrouter':
            provider = AIProvider.AI_OPENROUTER
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        elif self.model_id == 'ollama':
            provider = AIProvider.AI_OLLAMA
            model_config = get_current_model_config(provider)
            default_model_name = model_config.default_model_name if model_config else None
        
        if not default_model_name:
            return 1  # 返回第一个实际模型
        
        
        # 1. 精确匹配
        for i, model in enumerate(models):
            if model == default_model_name:
                return i + 1  # +1 因为索引0是占位符
        
        # 2. 部分匹配（包含关系）
        for i, model in enumerate(models):
            if default_model_name in model or model in default_model_name:
                return i + 1
        
        # 3. 模糊匹配（最长公共子串）
        best_match_index = 0
        best_match_score = 0
        
        for i, model in enumerate(models):
            # 计算相似度（简单的字符重叠）
            model_lower = model.lower()
            default_lower = default_model_name.lower()
            
            # 计算公共字符数
            common_chars = sum(1 for c in default_lower if c in model_lower)
            score = common_chars / max(len(default_lower), 1)
            
            if score > best_match_score:
                best_match_score = score
                best_match_index = i + 1
        
        if best_match_score > 0.3:  # 至少30%的相似度
            return best_match_index
        
        # 4. 没有找到匹配，返回第一个模型
        return 1
    
    def on_load_models_clicked(self):
        """点击加载模型按钮 - 根据状态执行加载或测试"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 如果已加载模型，则执行测试
        if self._models_loaded:
            self._test_current_model()
            return
        
        # 否则执行加载模型列表
        # 1. 验证 API Key（Ollama 不需要）
        if self.model_id != 'ollama':
            api_key = self.get_api_key()
            if not api_key:
                QMessageBox.warning(
                    self,
                    self.i18n.get('warning', 'Warning'),
                    self.i18n.get('api_key_required', 'Please enter API Key first')
                )
                return
        
        # 2. 清除缓存，强制使用当前输入框的 API Key 重新加载
        prefs = get_prefs()
        cached_models = prefs.get('cached_models', {})
        if self.model_id in cached_models:
            del cached_models[self.model_id]
            prefs['cached_models'] = cached_models
        
        # 3. 启动加载动画
        self.load_models_animation.start()
        
        # 4. 获取当前配置（从输入框实时获取）
        config = self.get_config()
        api_key_value = config.get('api_key') or config.get('auth_token')
        
        # 4. 创建 API 客户端并获取模型列表
        from .api import APIClient
        api_client = APIClient(i18n=self.i18n)
        
        # 使用 QTimer 异步执行，避免阻塞 UI
        def fetch_models():
            # 第一步：加载模型列表（跳过验证）
            success, result = api_client.fetch_available_models(self.model_id, config, skip_verification=True)
            
            # 停止加载动画
            self.load_models_animation.stop()
            
            if success:
                # 成功：填充下拉框
                models = result
                
                self.model_combo.clear()
                # 先添加占位符
                placeholder_text = self.i18n.get('select_model', '-- No Model --')
                self.model_combo.addItem(placeholder_text)
                # 再添加模型列表
                self.model_combo.addItems(models)
                
                # 保存到缓存
                prefs = get_prefs()
                cached_models = prefs.get('cached_models', {})
                cached_models[self.model_id] = models
                prefs['cached_models'] = cached_models
                
                # 如果有保存的模型名称，尝试选中
                saved_model = config.get('model', '').strip()
                selected_index = 0  # 默认占位符
                
                if saved_model and saved_model != placeholder_text:
                    # 有有效的保存模型（不是空字符串，也不是占位符文本）
                    index = self.model_combo.findText(saved_model)
                    if index >= 0 and index > 0:  # 确保不是占位符
                        selected_index = index
                    else:
                        # 模型不在列表中，尝试智能匹配默认模型
                        selected_index = self._find_best_default_model(models)
                else:
                    # 没有保存的模型或保存的是占位符，尝试智能匹配默认模型
                    selected_index = self._find_best_default_model(models)
                
                # 设置选中的索引
                self.model_combo.setCurrentIndex(selected_index)
                
                # 确保取消勾选"使用自定义模型名称"，使用下拉框中的模型
                if hasattr(self, 'use_custom_model_checkbox'):
                    self.use_custom_model_checkbox.setChecked(False)
                
                # 标记模型已加载，更新按钮状态
                self._models_loaded = True
                self.update_load_models_button_state()
                
                # 显示加载成功消息
                selected_model = self.model_combo.currentText()
                placeholder_text = self.i18n.get('select_model', '-- No Model --')
                
                # 直接保存配置
                self._save_config_after_load()
                
                # 显示成功消息（只有一个"关闭"按钮）
                if selected_model and selected_model != placeholder_text:
                    # 有选中的模型，显示模型名称
                    QMessageBox.information(
                        self,
                        self.i18n.get('success', 'Success'),
                        self.i18n.get('models_loaded_with_selection', 
                            'Successfully loaded {count} models.\nSelected model: {model}').format(
                                count=len(models),
                                model=selected_model
                            )
                    )
                else:
                    # 没有选中有效模型，只显示数量
                    QMessageBox.information(
                        self,
                        self.i18n.get('success', 'Success'),
                        self.i18n.get('models_loaded', 'Successfully loaded {count} models').format(count=len(models))
                    )
            else:
                # 失败：显示错误（错误信息已经格式化好：用户友好描述 + 技术细节）
                error_msg = result
                logger.error(f"Failed to load models: {error_msg}")
                
                QMessageBox.critical(
                    self,
                    self.i18n.get('error', 'Error'),
                    error_msg
                )
        
        # 使用 QTimer 延迟执行，避免阻塞
        QTimer.singleShot(100, fetch_models)
    
    def update_load_models_button_state(self):
        """更新加载模型按钮的状态和文本"""
        if self._models_loaded:
            # 已加载模型，显示"测试当前模型"
            self.load_models_button.setText(self.i18n.get('test_current_model', 'Test Current Model'))
            # 更新动画的原始文本
            self.load_models_animation.original_text = self.i18n.get('test_current_model', 'Test Current Model')
        else:
            # 未加载模型，显示"加载模型列表"
            self.load_models_button.setText(self.i18n.get('load_models_list', 'Load Model List'))
            # 更新动画的原始文本
            self.load_models_animation.original_text = self.i18n.get('load_models_list', 'Load Model List')
    
    def _test_current_model(self):
        """测试当前选中的模型"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取当前选中的模型
        selected_model = self.model_combo.currentText()
        placeholder_text = self.i18n.get('select_model', '-- No Model --')
        
        if not selected_model or selected_model == placeholder_text:
            QMessageBox.warning(
                self,
                self.i18n.get('warning', 'Warning'),
                self.i18n.get('model_placeholder', 'Please load models first')
            )
            return
        
        # 获取当前配置
        config = self.get_config()
        config['model'] = selected_model
        
        
        # 启动加载动画
        self.load_models_animation.start()
        
        # 使用 QTimer 异步执行，避免阻塞 UI
        def test_model():
            # 创建 API 客户端
            from .api import APIClient
            api_client = APIClient(i18n=self.i18n)
            
            # 测试模型
            success, message = api_client.test_model(self.model_id, config, test_model_name=selected_model)
            
            # 停止加载动画
            self.load_models_animation.stop()
            
            if success:
                # 测试成功，保存配置
                self._save_config_after_load()
                QMessageBox.information(
                    self,
                    self.i18n.get('success', 'Success'),
                    self.i18n.get('model_test_success', 'Model test successful! Configuration saved.')
                )
            else:
                # 测试失败，显示错误
                logger.error(f"[{self.model_id}] 模型测试失败: {message}")
                QMessageBox.critical(
                    self,
                    self.i18n.get('error', 'Error'),
                    message
                )
        
        # 使用 QTimer 延迟执行，避免阻塞 UI
        # 延迟 100ms 让动画有时间启动
        QTimer.singleShot(100, test_model)
    
    
    def _save_config_after_load(self):
        """加载模型后保存配置"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 查找父级 ConfigDialog
        parent = self.parent()
        config_dialog = None
        while parent:
            if isinstance(parent, ConfigDialog):
                config_dialog = parent
                break
            parent = parent.parent()
        
        if config_dialog:
            config_dialog.save_settings()
    
    def on_model_combo_changed(self, text):
        """模型下拉框变化时自动保存"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 过滤掉占位符文本，避免保存无效选择
        if self._is_placeholder_text(text):
            return
        
        logger.info(f"模型下拉框变化: {text}，触发自动保存")
        
        # 查找父对话框并自动保存（不标记为输入框变化）
        parent = self.parent()
        config_dialog = None
        while parent:
            if isinstance(parent, ConfigDialog):
                config_dialog = parent
                break
            parent = parent.parent()
        
        if config_dialog:
            logger.info(f"模型切换后自动保存配置")
            config_dialog.save_settings()
            logger.info(f"配置已自动保存")
        else:
            # 如果找不到父对话框，至少触发配置变更信号
            self.on_config_changed()
    
    def on_custom_model_toggled(self, state):
        """切换自定义模型名称"""
        use_custom = (state == 2)  # Qt.Checked = 2
        
        logger.info(f"[on_custom_model_toggled] 触发切换 - state={state}, use_custom={use_custom}")
        logger.info(f"[on_custom_model_toggled] 切换前 - model_combo.isEnabled()={self.model_combo.isEnabled()}, custom_model_input.isEnabled()={self.custom_model_input.isEnabled()}")
        
        # 切换控件启用/禁用状态
        self.model_combo.setEnabled(not use_custom)
        self.custom_model_input.setEnabled(use_custom)
        
        logger.info(f"[on_custom_model_toggled] 切换后 - model_combo.isEnabled()={self.model_combo.isEnabled()}, custom_model_input.isEnabled()={self.custom_model_input.isEnabled()}")
        
        # 如果切换到自定义，复制当前选中的模型名称（排除占位符）
        if use_custom:
            current_text = self.model_combo.currentText()
            
            # 使用 _is_placeholder_text 方法检查是否是占位符
            if not self._is_placeholder_text(current_text):
                logger.info(f"[on_custom_model_toggled] 复制模型名称: {current_text}")
                self.custom_model_input.setText(current_text)
            else:
                logger.info(f"[on_custom_model_toggled] 当前是占位符，不复制: {current_text}")
            # 设置焦点到输入框
            self.custom_model_input.setFocus()
        
        # 自动保存配置
        parent = self.parent()
        config_dialog = None
        while parent:
            if isinstance(parent, ConfigDialog):
                config_dialog = parent
                break
            parent = parent.parent()
        
        if config_dialog:
            logger.info(f"切换自定义模型模式后自动保存配置")
            config_dialog.save_settings()
            logger.info(f"配置已自动保存")
        else:
            # 如果找不到父对话框，至少触发配置变更信号
            self.on_config_changed()
    
    def load_model_config(self):
        """加载模型配置"""
        use_custom = self.config.get('use_custom_model_name', False)
        model_name = self.config.get('model', '')
        
        logger.info(f"[load_model_config] 开始加载 - use_custom={use_custom}, model_name={model_name}")
        logger.info(f"[load_model_config] 初始状态 - checkbox.isChecked()={self.use_custom_model_checkbox.isChecked()}, custom_input.isEnabled()={self.custom_model_input.isEnabled()}")
        
        if use_custom:
            # 使用自定义模式
            logger.info(f"[load_model_config] 设置为自定义模式")
            self.use_custom_model_checkbox.setChecked(True)
            self.custom_model_input.setText(model_name)
        else:
            # 尝试在下拉框中选中（如果列表已加载）
            logger.info(f"[load_model_config] 使用下拉框模式 - combo.count()={self.model_combo.count()}")
            if self.model_combo.count() > 1:  # 大于1表示有占位符+实际模型
                index = self.model_combo.findText(model_name)
                logger.info(f"[load_model_config] 查找模型 '{model_name}' - index={index}")
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)
                else:
                    # 模型不在列表中，重置为占位符，并在自定义输入框显示
                    logger.info(f"[load_model_config] 模型不在列表中，重置为占位符")
                    self.model_combo.setCurrentIndex(0)
                    if model_name:
                        self.custom_model_input.setText(model_name)
            else:
                # 只有占位符（没有实际模型），重置为占位符
                logger.info(f"[load_model_config] 只有占位符，重置为占位符")
                self.model_combo.setCurrentIndex(0)
                if model_name:
                    self.custom_model_input.setText(model_name)
        
        logger.info(f"[load_model_config] 加载完成 - checkbox.isChecked()={self.use_custom_model_checkbox.isChecked()}, custom_input.isEnabled()={self.custom_model_input.isEnabled()}")
    
    def get_api_key(self) -> str:
        """获取 API Key"""
        if hasattr(self, 'api_key_edit') and self.api_key_edit:
            return self.api_key_edit.toPlainText().strip()
        return ''
    
    def retranslate_ui(self):
        """更新模型配置控件的文本"""
        import logging
        logger = logging.getLogger(__name__)
        # 更新模型配置控件文本

        # 定义已知标签的翻译
        known_labels = {
            'api_key': self.i18n.get('api_key_label', 'API Key:'),
            'base_url': self.i18n.get('base_url_label', 'Base URL:'),
            'model': self.i18n.get('model_label', 'Model:')
        }
        
        # 更新复选框文本
        if hasattr(self, 'enable_streaming_checkbox'):
            self.enable_streaming_checkbox.setText(self.i18n.get('model_enable_streaming', 'Enable Streaming'))
        
        # 更新"使用自定义模型名称"复选框
        if hasattr(self, 'use_custom_model_checkbox'):
            self.use_custom_model_checkbox.setText(self.i18n.get('use_custom_model', 'Use custom model name'))
        
        # 更新"加载模型"按钮
        if hasattr(self, 'load_models_button'):
            self.load_models_button.setText(self.i18n.get('load_models', 'Load Models'))
        
        # 更新自定义模型输入框的placeholder
        if hasattr(self, 'custom_model_input'):
            self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))
            
        for label in self.findChildren(QLabel):
            # 先检查objectName
            if hasattr(label, 'objectName') and label.objectName():
                obj_name = label.objectName().lower()
                for key, value in known_labels.items():
                    if key in obj_name:
                        label.setText(value)
                        break
            
            # 如果没有匹配到objectName，则尝试匹配当前文本
            current_text = label.text()
            if current_text in known_labels.values():
                continue  # 已经是最新的翻译，无需更新
            
            # 检查关键字匹配
            current_text_lower = current_text.lower()
            if ('api' in current_text_lower and ('key' in current_text_lower or 'token' in current_text_lower)) or '密钥' in current_text_lower or 'clé' in current_text_lower:
                label.setText(known_labels['api_key'])
            elif ('base' in current_text_lower and 'url' in current_text_lower) or '基础' in current_text_lower or 'base' in current_text_lower:
                label.setText(known_labels['base_url'])
            elif 'model' in current_text_lower or '模型' in current_text_lower or 'modèle' in current_text_lower:
                label.setText(known_labels['model'])
        
        reset_text = self.i18n.get('reset_current_ai', 'Reset Current AI to Default')
        reset_tooltip = self.i18n.get('reset_tooltip', 'Reset current AI to default values')
        
        for button in self.findChildren(QPushButton):
            if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            elif button.property('isResetButton'):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            elif button.text() in ['Reset to Default', 'Reset Current AI to Default', '重置', '重置当前AI为默认值', 'Réinitialiser', 'リセット']:
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
        
        if hasattr(self, 'api_base_edit'):
            model_config = None
            if self.model_id == 'grok':
                from .models import GrokModel
                model_config = GrokModel
            elif self.model_id == 'gemini':
                from .models import GeminiModel
                model_config = GeminiModel
            elif self.model_id == 'deepseek':
                from .models import DeepseekModel
                model_config = DeepseekModel
            elif self.model_id == 'custom':
                from .models import CustomModel
                model_config = CustomModel
            elif self.model_id == 'openai':
                from .models import OpenAIModel
                model_config = OpenAIModel
            elif self.model_id == 'anthropic':
                from .models import AnthropicModel
                model_config = AnthropicModel
            elif self.model_id == 'nvidia':
                from .models import NvidiaModel
                model_config = NvidiaModel
            elif self.model_id == 'openrouter':
                from .models import OpenRouterModel
                model_config = OpenRouterModel
            elif self.model_id == 'ollama':
                from .models import OllamaModel
                model_config = OllamaModel
                
            if model_config:
                default_api_base_url = getattr(model_config, 'DEFAULT_API_BASE_URL', '')
                self.api_base_edit.setPlaceholderText(self.i18n.get('base_url_placeholder', 'Default: {default_api_base_url}').format(
                    default_api_base_url=default_api_base_url
                ))
    
    def _get_ai_display_name(self):
        """获取AI的显示名称（翻译后的）"""
        display_name_key = f"model_display_name_{self.model_id}"
        from .models.base import AIProvider, DEFAULT_MODELS
        
        # 尝试从 DEFAULT_MODELS 获取
        provider_map = {
            'grok': AIProvider.AI_GROK,
            'gemini': AIProvider.AI_GEMINI,
            'deepseek': AIProvider.AI_DEEPSEEK,
            'custom': AIProvider.AI_CUSTOM,
            'openai': AIProvider.AI_OPENAI,
            'anthropic': AIProvider.AI_ANTHROPIC,
            'nvidia': AIProvider.AI_NVIDIA,
            'openrouter': AIProvider.AI_OPENROUTER,
            'ollama': AIProvider.AI_OLLAMA,
        }
        
        provider = provider_map.get(self.model_id)
        if provider and provider in DEFAULT_MODELS:
            default_name = DEFAULT_MODELS[provider].display_name
            return self.i18n.get(display_name_key, default_name)
        
        # 回退到 model_id
        return self.model_id.capitalize()
    
    def reset_model_params(self):
        """重置模型参数为默认值，清除所有配置"""
        import logging
        from PyQt5.QtWidgets import QMessageBox
        logger = logging.getLogger(__name__)
        
        # 获取AI的显示名称
        ai_display_name = self._get_ai_display_name()
        
        # 显示确认对话框
        confirm_title = self.i18n.get('reset_ai_confirm_title', 'Confirm Reset')
        confirm_message = self.i18n.get('reset_ai_confirm_message', 
            'About to reset {ai_name} to default state.\n\n'
            'This will clear:\n'
            '• API Key\n'
            '• Custom model name\n'
            '• Other configured parameters\n\n'
            'Continue?').format(ai_name=ai_display_name)
        
        reply = QMessageBox.question(
            self,
            confirm_title,
            confirm_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # 默认选择 No
        )
        
        if reply != QMessageBox.Yes:
            logger.info(f"用户取消了重置 {self.model_id} 的操作")
            return
        
        logger.info(f"用户确认重置 {self.model_id}")
        
        # 获取对应的AIProvider和ModelConfig
        model_config = None
        
        if self.model_id == 'grok':
            provider = AIProvider.AI_GROK
        elif self.model_id == 'gemini':
            provider = AIProvider.AI_GEMINI
        elif self.model_id == 'deepseek':
            provider = AIProvider.AI_DEEPSEEK
        elif self.model_id == 'custom':
            provider = AIProvider.AI_CUSTOM
        elif self.model_id == 'openai':
            provider = AIProvider.AI_OPENAI
        elif self.model_id == 'anthropic':
            provider = AIProvider.AI_ANTHROPIC
        elif self.model_id == 'nvidia':
            provider = AIProvider.AI_NVIDIA
        elif self.model_id == 'openrouter':
            provider = AIProvider.AI_OPENROUTER
        elif self.model_id == 'ollama':
            provider = AIProvider.AI_OLLAMA
        else:
            # 未知模型，无法重置
            logger.warning(f"未知模型 ID: {self.model_id}，无法重置")
            return
            
        # 获取模型配置
        model_config = get_current_model_config(provider)
        
        if model_config:
            logger.info(f"开始重置模型 {self.model_id} 的参数")
            
            # 1. 清除 API Key / Auth Token（Ollama 除外）
            if self.model_id != 'ollama':
                if hasattr(self, 'api_key_edit') and self.api_key_edit:
                    self.api_key_edit.clear()
                    logger.info(f"已清除 {self.model_id} 的 API Key")
            
            # 2. 重置 API Base URL
            self.api_base_edit.setText(model_config.default_api_base_url)
            logger.info(f"已重置 API Base URL 为: {model_config.default_api_base_url}")
            
            # 3. 重置模型名称：清空下拉框，添加占位符，清空自定义输入框
            self.model_combo.clear()
            placeholder_text = self.i18n.get('select_model', '-- Select Model --')
            self.model_combo.addItem(placeholder_text)
            hint_text = self.i18n.get('request_model_list', 'Please request model list')
            self.model_combo.addItem(hint_text)
            # 禁用提示项
            model = self.model_combo.model()
            item = model.item(1)
            if item:
                item.setEnabled(False)
            self.model_combo.setCurrentIndex(0)  # 选中占位符
            
            # 取消自定义模式，清空自定义输入框
            self.use_custom_model_checkbox.setChecked(False)
            self.custom_model_input.clear()
            logger.info("已重置模型选择为占位符状态")
            
            # 4. 重置流式传输选项
            if hasattr(self, 'enable_streaming_checkbox'):
                self.enable_streaming_checkbox.setChecked(True)
                logger.info("已重置流式传输选项为启用")
                
            # 5. 重置 Custom 模型的特殊配置
            if self.model_id == 'custom':
                if hasattr(self, 'disable_ssl_verify_checkbox'):
                    self.disable_ssl_verify_checkbox.setChecked(False)  # 默认启用SSL验证
                    logger.info("已重置 SSL 验证选项为启用")
                if hasattr(self, 'http_referer_edit'):
                    self.http_referer_edit.clear()
                    logger.info("已清除 HTTP Referer")
            
            # 6. 重置 OpenRouter 的特殊配置
            if self.model_id == 'openrouter' and hasattr(self, 'http_referer_edit'):
                self.http_referer_edit.clear()
                logger.info("已清除 OpenRouter HTTP Referer")
            
            # 7. 清除模型缓存
            prefs = get_prefs()
            cached_models = prefs.get('cached_models', {})
            if self.model_id in cached_models:
                del cached_models[self.model_id]
                prefs['cached_models'] = cached_models
                logger.info(f"已清除 {self.model_id} 的模型缓存")
            
            # 8. 更新配置文件中的 is_configured 状态
            if 'models' in prefs and self.model_id in prefs['models']:
                prefs['models'][self.model_id]['is_configured'] = False
                logger.info(f"已将 {self.model_id} 标记为未配置状态")
            
            # 9. 更新 Load Models 按钮状态
            self.update_load_models_button_state()
            
            # 10. 通知父对话框更新模型列表的对钩标记
            # 通过发射信号让 ConfigDialog 更新模型名称显示
            config_dialog = None
            parent = self.parent()
            while parent:
                if isinstance(parent, ConfigDialog):
                    config_dialog = parent
                    config_dialog.update_model_names()
                    logger.info("已通知父对话框更新模型列表显示")
                    break
                parent = parent.parent()
            
            # 9. 自动保存配置（重置已经有二次确认，无需再次手动保存）
            if config_dialog:
                logger.info(f"开始自动保存重置后的配置")
                config_dialog.save_settings()
                logger.info(f"模型 {self.model_id} 重置完成并已自动保存")
            else:
                # 如果找不到父对话框，至少触发配置变更信号
                self.on_config_changed()
                logger.warning(f"未找到父对话框，无法自动保存配置")
                logger.info(f"模型 {self.model_id} 重置完成")


class ConfigDialog(QWidget):
    # 添加信号
    settings_saved = pyqtSignal()  # 设置保存信号
    language_changed = pyqtSignal(str)  # 语言改变信号
    config_changed = pyqtSignal()  # 配置变更信号
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        # 获取当前语言的翻译
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 保存初始值
        self.initial_values = {}
        self.model_widgets = {}
        
        # 跟踪是否有未保存的输入框变化
        self.has_unsaved_input_changes = False
        
        # 初始化标志，用于避免初始化时触发变化检测
        self._is_initializing = True
        
        # 初始化模型工厂（注意：这些模型已经在 models/__init__.py 中注册过了）
        AIModelFactory.register_model('grok', GrokModel)
        AIModelFactory.register_model('gemini', GeminiModel)
        AIModelFactory.register_model('deepseek', DeepseekModel)
        AIModelFactory.register_model('custom', CustomModel)
        AIModelFactory.register_model('openai', OpenAIModel)
        AIModelFactory.register_model('anthropic', AnthropicModel)
        AIModelFactory.register_model('nvidia', NvidiaModel)
        AIModelFactory.register_model('openrouter', OpenRouterModel)
        AIModelFactory.register_model('ollama', OllamaModel)
        
        self.setup_ui()
        self.load_initial_values()
        
        # 初始化完成，开始跟踪变化
        self._is_initializing = False
        self.has_unsaved_input_changes = False  # 重置标志
        
    def get_auth_token_without_bearer(self, token):
        """从 token 中移除 'Bearer ' 前缀"""
        if not token:
            return ''
        if token.startswith('Bearer '):
            return token[7:].strip()
        return token.strip()
        
    def get_auth_token_with_bearer(self, token):
        """确保 token 有 'Bearer ' 前缀"""
        if not token:
            return ''
        token = token.strip()
        if not token.startswith('Bearer '):
            return f'Bearer {token}'
        return token
        
    def setup_ui(self):
        # 设置窗口属性
        self.setMinimumWidth(700)  # 增加最小宽度，避免水平滚动条
        self.setMinimumHeight(500)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # 去除主布局的边距
        self.setLayout(main_layout)
        
        # 设置通用设置（包含所有配置）
        self.setup_general_tab(main_layout)
        
        # 注意：按钮布局现在在ui.py中统一管理，这里不再添加按钮布局
    
    def setup_general_tab(self, main_layout):
        """设置通用设置（包含所有配置项）"""
        
        # 创建一个主滚动区域来包含所有内容，防止窗口缩放时元素重叠
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QScrollArea.NoFrame)
        main_scroll.setObjectName("config_scroll")
        # 去除滚动区域的内边距和边框，让内容填满整个区域
        # 使用 ID 选择器确保只影响这个特定的 QScrollArea
        style = """
            QScrollArea#config_scroll {
                padding: 0px;
                margin: 0px;
                border: none;
            }
            QScrollArea#config_scroll > QWidget {
                background: transparent;
            }
            QScrollArea#config_scroll QWidget#qt_scrollarea_viewport {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """
        main_scroll.setStyleSheet(style)
        # 直接设置 viewport 的边距
        if main_scroll.viewport():
            main_scroll.viewport().setContentsMargins(0, 0, 0, 0)
        
        # 创建内容容器
        content_widget = QWidget()
        # 只为这个特定的 widget 设置样式，不影响子控件
        content_widget.setStyleSheet("QWidget#content_container { background: transparent; border: none; }")
        content_widget.setObjectName("content_container")
        content_layout = QVBoxLayout()
        # 使用紧凑间距，因为GroupBox已经有虚线框区分了
        from .ui_constants import SPACING_ASK_COMPACT
        content_layout.setSpacing(SPACING_ASK_COMPACT)  # 区域之间使用紧凑间距（4px）
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_widget.setLayout(content_layout)
        
        # 1. 顶部：语言选择
        lang_group = QGroupBox(self.i18n.get('display', 'Display'))
        lang_group.setObjectName('groupbox_display')  # 设置ObjectName用于语言切换
        lang_group.setStyleSheet(get_groupbox_style())
        lang_layout = QVBoxLayout()
        lang_layout.setSpacing(SPACING_SMALL)
        
        self.lang_combo = NoScrollComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(get_prefs()['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        language_label = QLabel(self.i18n.get('language_label', 'Language:'))
        language_label.setObjectName('label_language')
        lang_layout.addWidget(language_label)
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)

        # 2. 中部：AI模型选择和配置
        model_group = QGroupBox(self.i18n.get('ai_models', 'AI'))
        model_group.setObjectName('groupbox_ai_models')  # 设置ObjectName用于语言切换
        model_group.setStyleSheet(get_groupbox_style())
        model_layout = QVBoxLayout()
        model_layout.setSpacing(SPACING_MEDIUM)

        # 添加模型选择下拉框
        model_select_layout = QHBoxLayout()
        model_select_layout.setSpacing(SPACING_SMALL)
        current_ai_label = QLabel(self.i18n.get('current_ai', 'Current AI:'))
        current_ai_label.setObjectName('label_current_ai')
        model_select_layout.addWidget(current_ai_label)

        self.model_combo = NoScrollComboBox()
        # 使用有序列表来定义模型显示顺序（按使用频率和影响力排序）
        # OpenAI 第一，Custom 最后
        model_mapping = [
            (AIProvider.AI_OPENAI, 'openai'),
            (AIProvider.AI_ANTHROPIC, 'anthropic'),
            (AIProvider.AI_GEMINI, 'gemini'),
            (AIProvider.AI_GROK, 'grok'),
            (AIProvider.AI_DEEPSEEK, 'deepseek'),
            (AIProvider.AI_NVIDIA, 'nvidia'),
            (AIProvider.AI_OPENROUTER, 'openrouter'),
            (AIProvider.AI_OLLAMA, 'ollama'),
            (AIProvider.AI_CUSTOM, 'custom'),
        ]
        # 按照定义的顺序添加到下拉框
        for provider, model_id in model_mapping:
            if provider in DEFAULT_MODELS:
                model_config = DEFAULT_MODELS[provider]
                self.model_combo.addItem(model_config.display_name, model_id)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        model_select_layout.addWidget(self.model_combo)
        
        # 不再需要额外的模型名称标签，因为下拉框已经显示了模型名称
        
        model_layout.addLayout(model_select_layout)
        
        # 默认选择当前选中的模型
        current_model = get_prefs().get('selected_model', 'grok')
        index = self.model_combo.findData(current_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # 直接使用布局，不使用滚动区域或容器
        # 这样可以确保全部内容都能正确显示，不会出现二级滚动条
        
        # 创建模型配置布局
        self.models_layout = QVBoxLayout()
        # 使用统一的间距规范
        self.models_layout.setContentsMargins(0, 0, 0, 0)
        self.models_layout.setSpacing(SPACING_MEDIUM)
        
        # 添加模型配置控件
        self.setup_model_widgets()
        
        # 直接将布局添加到模型组布局中
        model_layout.addLayout(self.models_layout)
        
        # 添加分隔线（在重置按钮和超时设置之间）
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        separator.setStyleSheet(get_separator_style())
        model_layout.addWidget(separator)
        
        # 添加请求超时时间设置
        timeout_layout = QHBoxLayout()
        timeout_layout.setSpacing(SPACING_SMALL)
        timeout_label = QLabel(self.i18n.get('request_timeout_label', 'Request Timeout:'))
        timeout_label.setObjectName('label_request_timeout')
        timeout_layout.addWidget(timeout_label)
        
        self.timeout_input = QLineEdit(self)
        self.timeout_input.setText(str(get_prefs().get('request_timeout', 60)))
        self.timeout_input.setPlaceholderText(self.i18n.get('timeout_placeholder', '60'))
        self.timeout_input.setMaximumWidth(100)
        # 只允许输入数字
        from PyQt5.QtGui import QIntValidator
        self.timeout_input.setValidator(QIntValidator(1, 3600, self))  # 1-3600秒
        self.timeout_input.textChanged.connect(self.on_config_changed)
        timeout_layout.addWidget(self.timeout_input)
        
        timeout_unit_label = QLabel(self.i18n.get('seconds', 'seconds'))
        timeout_layout.addWidget(timeout_unit_label)
        timeout_layout.addStretch()
        
        model_layout.addLayout(timeout_layout)
        
        # 添加并行AI数量设置
        parallel_layout = QHBoxLayout()
        parallel_layout.setSpacing(SPACING_SMALL)
        parallel_label = QLabel(self.i18n.get('parallel_ai_count_label', 'Parallel AI Count:'))
        parallel_label.setObjectName('label_parallel_ai_count')
        parallel_label.setToolTip(self.i18n.get('parallel_ai_count_tooltip', 
            'Number of AIs to query simultaneously (1-4). Only applies to question requests, not random questions.'))
        parallel_layout.addWidget(parallel_label)
        
        self.parallel_ai_combo = NoScrollComboBox(self)
        # 添加选项1-4，但3-4置灰（保留入口，吸引高级用户）
        for i in range(1, 5):
            display_text = str(i)
            if i > 2:
                display_text += f" ({self.i18n.get('coming_soon', 'Coming Soon')})"
            self.parallel_ai_combo.addItem(display_text, i)
            # 将3和4选项设置为不可用
            if i > 2:
                model = self.parallel_ai_combo.model()
                item = model.item(i - 1)
                item.setEnabled(False)
                item.setToolTip(self.i18n.get('advanced_feature_tooltip', 
                    'This feature is under development. Stay tuned for updates!'))
        
        current_parallel = get_prefs().get('parallel_ai_count', 1)
        # 如果当前配置是3或4，自动降级到2
        if current_parallel > 2:
            current_parallel = 2
            get_prefs()['parallel_ai_count'] = 2
        index = self.parallel_ai_combo.findData(current_parallel)
        if index >= 0:
            self.parallel_ai_combo.setCurrentIndex(index)
        self.parallel_ai_combo.currentIndexChanged.connect(self.on_parallel_count_changed)
        self.parallel_ai_combo.setMaximumWidth(150)
        parallel_layout.addWidget(self.parallel_ai_combo)
        parallel_layout.addStretch()
        
        model_layout.addLayout(parallel_layout)
        
        # 并行AI选择器容器（动态显示）
        self.panel_ai_selectors_layout = QVBoxLayout()
        self.panel_ai_selectors = []  # 保存AI选择器的引用
        model_layout.addLayout(self.panel_ai_selectors_layout)
        
        # 初始化AI选择器
        self._update_panel_ai_selectors()
        
        # 添加并行AI提示信息
        from .ui_constants import TEXT_COLOR_SECONDARY
        parallel_notice = QLabel(self.i18n.get('parallel_ai_notice', 
            'Each response window will have its own AI selector. Make sure you have configured enough AI providers.'))
        parallel_notice.setWordWrap(True)
        parallel_notice.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; padding: 5px 0; font-style: italic;")
        model_layout.addWidget(parallel_notice)
        
        model_group.setLayout(model_layout)
        
        # 3. 底部：提示词模板配置
        template_group = QGroupBox(self.i18n.get('prompt_template', 'Prompts'))
        template_group.setObjectName('groupbox_prompt_template')  # 设置ObjectName用于语言切换
        template_group.setStyleSheet(get_groupbox_style())
        template_layout = QVBoxLayout()
        template_layout.setSpacing(SPACING_MEDIUM)
        
        # 主提示词模板
        main_template_layout = QVBoxLayout()
        main_template_layout.setSpacing(SPACING_SMALL)
        main_template_layout.addWidget(QLabel(self.i18n.get('ask_prompts', 'Ask Prompts:')))
        
        self.template_edit = QPlainTextEdit(self)
        self.template_edit.setPlainText(get_prefs()['template'])
        self.template_edit.textChanged.connect(self.on_config_changed)

        # 设置初始高度为大约5行文字的高度
        font_metrics = QFontMetrics(self.template_edit.font())
        line_height = font_metrics.lineSpacing()
        padding = 10  # 上下内边距
        five_lines_height = line_height * 5 + padding
        ten_lines_height = line_height * 10 + padding
        
        # 设置初始高度和最小/最大高度限制
        self.template_edit.setMinimumHeight(five_lines_height)  # 最小5行高度
        self.template_edit.setMaximumHeight(ten_lines_height)  # 最大10行高度
        
        # 设置大小策略以允许垂直扩展和调整大小
        self.template_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 确保滚动条在需要时出现
        self.template_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.template_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_template_layout.addWidget(self.template_edit)
        
        # 将主提示词模板添加到模板布局
        template_layout.addLayout(main_template_layout)
        
        # 随机问题提示词
        random_questions_layout = QVBoxLayout()
        random_questions_layout.setSpacing(SPACING_SMALL)
        random_questions_layout.addWidget(QLabel(self.i18n.get('random_questions_prompts', 'Random Questions Prompts:')))
        
        self.random_questions_edit = QPlainTextEdit(self)
        
        # 从配置中加载随机问题提示词，如果不存在则使用默认值
        random_questions = get_prefs().get('random_questions', {})
        current_lang = self.lang_combo.currentData()
        
        # 获取随机问题提示词，如果不存在或为空则使用默认模板
        saved_questions = random_questions.get(current_lang)
        if saved_questions and saved_questions.strip():
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(current_lang)
        
        self.random_questions_edit.setPlainText(default_value)

        self.random_questions_edit.textChanged.connect(self.on_config_changed)

        # 设置初始高度为大约5行文字的高度
        font_metrics = QFontMetrics(self.random_questions_edit.font())
        line_height = font_metrics.lineSpacing()
        padding = 10  # 上下内边距
        five_lines_height = line_height * 5 + padding
        ten_lines_height = line_height * 10 + padding
        
        # 设置初始高度和最小/最大高度限制
        self.random_questions_edit.setMinimumHeight(five_lines_height)  # 最小5行高度
        self.random_questions_edit.setMaximumHeight(ten_lines_height)  # 最大10行高度
        
        # 设置大小策略以允许垂直扩展和调整大小
        self.random_questions_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 确保滚动条在需要时出现
        self.random_questions_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.random_questions_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        random_questions_layout.addWidget(self.random_questions_edit)
        
        # 将随机问题提示词添加到模板布局
        template_layout.addLayout(random_questions_layout)
        
        # 多书提示词模板
        multi_book_template_layout = QVBoxLayout()
        multi_book_template_layout.setSpacing(SPACING_SMALL)
        multi_book_template_layout.addWidget(QLabel(self.i18n.get('multi_book_template_label', 'Multi-Book Prompt Template:')))
        
        self.multi_book_template_edit = QPlainTextEdit(self)
        self.multi_book_template_edit.setPlainText(get_prefs().get('multi_book_template', ''))
        self.multi_book_template_edit.textChanged.connect(self.on_config_changed)
        
        # 设置初始高度为大约5行文字的高度
        font_metrics = QFontMetrics(self.multi_book_template_edit.font())
        line_height = font_metrics.lineSpacing()
        padding = 10  # 上下内边距
        five_lines_height = line_height * 5 + padding
        ten_lines_height = line_height * 10 + padding
        
        # 设置初始高度和最小/最大高度限制
        self.multi_book_template_edit.setMinimumHeight(five_lines_height)  # 最小5行高度
        self.multi_book_template_edit.setMaximumHeight(ten_lines_height)  # 最大10行高度
        
        # 设置大小策略以允许垂直扩展和调整大小
        self.multi_book_template_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 确保滚动条在需要时出现
        self.multi_book_template_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.multi_book_template_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        multi_book_template_layout.addWidget(self.multi_book_template_edit)
        
        # 添加占位符说明
        placeholder_hint = QLabel(self.i18n.get('multi_book_placeholder_hint', 'Use {books_metadata} for book information, {query} for user question'))
        placeholder_hint.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-style: italic; padding: 5px 0;")
        placeholder_hint.setWordWrap(True)
        multi_book_template_layout.addWidget(placeholder_hint)
        
        # 将多书提示词模板添加到模板布局
        template_layout.addLayout(multi_book_template_layout)
        
        # 将布局设置应用到模板组
        template_group.setLayout(template_layout)
        
        # 4. Export Settings
        export_group = QGroupBox(self.i18n.get('export_settings', 'Export Settings'))
        export_group.setObjectName('groupbox_export_settings')
        export_group.setStyleSheet(get_groupbox_style())
        export_layout = QVBoxLayout()
        export_layout.setSpacing(SPACING_SMALL)
        
        # 复选框：导出到默认文件夹
        self.enable_default_folder_checkbox = QCheckBox(
            self.i18n.get('enable_default_export_folder', 'Export to default folder')
        )
        self.enable_default_folder_checkbox.setObjectName('checkbox_enable_default_folder')
        self.enable_default_folder_checkbox.setChecked(
            self.initial_values.get('enable_default_export_folder', False)
        )
        self.enable_default_folder_checkbox.stateChanged.connect(self._on_export_config_changed)
        export_layout.addWidget(self.enable_default_folder_checkbox)
        
        # 文件夹选择区域
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(SPACING_SMALL)
        
        # 文件夹路径标签（显示当前选择的路径）
        self.export_folder_label = QLabel(
            self.initial_values.get('default_export_folder', '') or 
            self.i18n.get('no_folder_selected', 'No folder selected')
        )
        self.export_folder_label.setObjectName('label_export_folder')
        self.export_folder_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                border: 1px solid palette(mid);
                border-radius: 4px;
                background: palette(base);
            }
        """)
        self.export_folder_label.setWordWrap(True)
        folder_layout.addWidget(self.export_folder_label, 1)
        
        # 浏览按钮
        self.browse_folder_button = QPushButton(self.i18n.get('browse', 'Browse...'))
        self.browse_folder_button.setObjectName('button_browse_folder')
        apply_button_style(self.browse_folder_button, min_width=100)
        self.browse_folder_button.clicked.connect(self._on_browse_export_folder)
        self.browse_folder_button.setEnabled(
            self.initial_values.get('enable_default_export_folder', False)
        )
        folder_layout.addWidget(self.browse_folder_button)
        
        export_layout.addLayout(folder_layout)
        
        export_group.setLayout(export_layout)
        
        # 5. 危险区域：重置所有数据
        reset_group = QGroupBox(self.i18n.get('reset_all_data', 'Reset All Data'))
        reset_group.setObjectName('groupbox_reset_data')
        reset_group.setStyleSheet(get_groupbox_style() + "QGroupBox { border-color: #dc3545; }")  # 红色边框表示危险操作
        reset_layout = QVBoxLayout()
        reset_layout.setSpacing(SPACING_SMALL)
        
        # 警告文字
        warning_label = QLabel(self.i18n.get('reset_all_data_warning', 
            'This will delete all API Keys, prompt templates, and local history records. Please proceed with caution.'))
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #dc3545; font-weight: bold; padding: 5px 0;")
        reset_layout.addWidget(warning_label)
        
        # 重置按钮
        self.reset_button = QPushButton(self.i18n.get('reset_all_data', 'Reset All Data'))
        self.reset_button.setObjectName('button_reset_all_data')
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.reset_button.clicked.connect(self.on_reset_all_data)
        reset_layout.addWidget(self.reset_button)
        
        reset_group.setLayout(reset_layout)
        
        # 添加所有组件到内容布局
        content_layout.addSpacing(SPACING_ASK_COMPACT)  # 顶部添加小间距
        content_layout.addWidget(lang_group)
        content_layout.addWidget(model_group)
        content_layout.addWidget(template_group)
        content_layout.addWidget(export_group)
        content_layout.addWidget(reset_group)
        content_layout.addStretch()
        
        # 将内容容器设置到主滚动区域
        main_scroll.setWidget(content_widget)
        
        # 添加主滚动区域到主布局
        main_layout.addWidget(main_scroll)

    def setup_model_widgets(self):
        """初始化所有模型配置控件"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 确保 models_layout 已经初始化
        if not hasattr(self, 'models_layout') or self.models_layout is None:
            # 创建模型配置布局
            self.models_layout = QVBoxLayout()
            # 设置合适的边距和间距
            self.models_layout.setContentsMargins(10, 10, 10, 10)
            self.models_layout.setSpacing(10)
        
        # 在清空控件前，保存所有当前模型的配置
        current_configs = {}
        if hasattr(self, 'model_widgets'):
            for model_id, widget in self.model_widgets.items():
                try:
                    current_configs[model_id] = widget.get_config()
                    pass  # 配置已保存
                except Exception as e:
                    logger.error(f"获取模型 {model_id} 配置时出错: {str(e)}")
                    # 如果控件已被删除，使用初始值或默认值
                    if hasattr(self, 'initial_values') and 'models' in self.initial_values and model_id in self.initial_values['models']:
                        current_configs[model_id] = self.initial_values['models'][model_id]
                        pass  # 使用初始值
        
        # 清除当前布局中的所有元素
        self.clear_layout(self.models_layout)
        self.model_widgets = {}
        
        # 获取当前选中的模型
        model_id = self.model_combo.currentData()
        
        # 获取模型配置的优先级：
        # 1. 当前会话中用户修改过的配置（存储在current_configs中）
        # 2. 已保存的配置（存储在prefs中）
        # 3. 当前会话的初始值（存储在self.initial_values中）
        model_config = None
        
        # 1. 首先检查当前会话中用户修改过的配置
        if model_id in current_configs:
            model_config = current_configs[model_id]
        # 2. 如果没有，从已保存的配置中获取
        elif get_prefs().get('models', {}).get(model_id):
            model_config = get_prefs().get('models', {}).get(model_id, {})
        # 3. 如果还是没有，检查初始值
        elif hasattr(self, 'initial_values') and 'models' in self.initial_values and model_id in self.initial_values['models']:
            model_config = self.initial_values['models'].get(model_id, {})
        # 4. 如果都没有，使用空字典
        else:
            model_config = {}
        
        # 创建模型配置控件
        widget = ModelConfigWidget(model_id, model_config, self.i18n)
        widget.config_changed.connect(self.on_config_changed)
        # 不设置最小高度，让控件根据内容自动调整大小
        
        # 保存控件引用
        self.model_widgets[model_id] = widget
        
        # 添加到布局
        self.models_layout.addWidget(widget)
        # 移除addStretch，防止Reset按钮被推到不可见区域
    
    def clear_layout(self, layout):
        """清除布局中的所有元素"""
        if layout is None:
            return
            
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
                item.layout().deleteLater()
    
    def on_model_changed(self, index):
        """当选择的模型改变时"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取当前选中的模型
        model_id = self.model_combo.currentData()
        
        # 设置模型组件 - 这里会保存当前模型的配置并加载新选中模型的配置
        self.setup_model_widgets()
        
        # 模型切换时仅需要更新内容，不需要重新添加布局
        # setup_model_widgets 已经处理了布局初始化和清除工作
        
        self.update_model_name_display()
        
        # 重置当前模型的加载状态（切换AI服务商时重置按钮）
        if model_id in self.model_widgets:
            widget = self.model_widgets[model_id]
            if hasattr(widget, '_models_loaded'):
                widget._models_loaded = False
                widget.update_load_models_button_state()
        
        # 切换模型不会自动触发保存按钮的启用，需要用户实际修改配置
        # 调用on_config_changed检查是否有变更
        self.on_config_changed()
    
    def update_model_names(self):
        """更新模型列表显示（包括对钩标记）- 别名方法"""
        self.update_model_name_display()
    
    def update_model_name_display(self):
        """更新模型下拉框中的模型名称显示，使用当前语言的翻译"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 保存当前选中的模型ID
        current_model_id = self.model_combo.currentData()
        
        # 暂时阻断信号，防止触发on_model_changed
        self.model_combo.blockSignals(True)
        
        # 清空下拉框
        self.model_combo.clear()
        
        # 使用有序列表来定义模型显示顺序（按使用频率和影响力排序）
        # OpenAI 第一，Custom 最后
        model_mapping = [
            (AIProvider.AI_OPENAI, 'openai'),
            (AIProvider.AI_ANTHROPIC, 'anthropic'),
            (AIProvider.AI_GEMINI, 'gemini'),
            (AIProvider.AI_GROK, 'grok'),
            (AIProvider.AI_DEEPSEEK, 'deepseek'),
            (AIProvider.AI_NVIDIA, 'nvidia'),
            (AIProvider.AI_OPENROUTER, 'openrouter'),
            (AIProvider.AI_OLLAMA, 'ollama'),
            (AIProvider.AI_CUSTOM, 'custom'),
        ]
        
        # 获取当前所有模型的配置状态
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        
        # 按照定义的顺序添加到下拉框，使用翻译后的名称
        for provider, model_id in model_mapping:
            if provider in DEFAULT_MODELS:
                # 获取翻译后的模型名称
                display_name_key = f"model_display_name_{model_id}"
                translated_name = self.i18n.get(display_name_key, DEFAULT_MODELS[provider].display_name)
                
                # 检查是否已配置，添加对钩标记
                model_config = models_config.get(model_id, {})
                if model_config.get('is_configured', False):
                    translated_name = f"✓ {translated_name}"
                
                self.model_combo.addItem(translated_name, model_id)
        
        # 恢复之前选中的模型
        index = self.model_combo.findData(current_model_id)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # 恢复信号连接
        self.model_combo.blockSignals(False)
    
    def load_initial_values(self):
        """加载初始值"""
        prefs = get_prefs()
        current_lang = prefs.get('language', 'en')
        
        # 保存初始值
        self.initial_values = {
            'language': current_lang,
            'template': prefs.get('template', get_default_template(current_lang)),
            'multi_book_template': prefs.get('multi_book_template', ''),
            'selected_model': prefs.get('selected_model', 'grok'),
            'models': copy.deepcopy(prefs.get('models', {})),
            'random_questions': copy.deepcopy(prefs.get('random_questions', {})),
            'request_timeout': prefs.get('request_timeout', 60),
            'parallel_ai_count': prefs.get('parallel_ai_count', 1),
            'enable_default_export_folder': prefs.get('enable_default_export_folder', False),
            'default_export_folder': prefs.get('default_export_folder', '')
        }
        
        # 调试日志
        import logging
        logger = logging.getLogger(__name__)
        # 初始值已加载
        
        
        # 设置当前语言
        current_index = self.lang_combo.findData(self.initial_values['language'])
        if current_index >= 0:
            self.lang_combo.setCurrentIndex(current_index)
        
        # 更新模型名称显示
        self.update_model_name_display()
        
        # 设置模板
        self.template_edit.setPlainText(self.initial_values['template'])
        # 保存原始文本用于变更检测
        self.initial_values['template_raw'] = self.template_edit.toPlainText()
        
        # 设置多书提示词模板
        if hasattr(self, 'multi_book_template_edit'):
            self.multi_book_template_edit.setPlainText(self.initial_values.get('multi_book_template', ''))
            # 保存原始文本用于变更检测
            self.initial_values['multi_book_template_raw'] = self.multi_book_template_edit.toPlainText()
        
        # 设置随机问题提示词
        random_questions = self.initial_values['random_questions']
        
        # 获取随机问题提示词，如果不存在或为空则使用默认模板
        saved_questions = random_questions.get(current_lang)
        if saved_questions and saved_questions.strip():
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(current_lang)
        
        self.random_questions_edit.setPlainText(default_value)
        # 保存原始文本用于变更检测
        if 'random_questions_raw' not in self.initial_values:
            self.initial_values['random_questions_raw'] = {}
        self.initial_values['random_questions_raw'][current_lang] = self.random_questions_edit.toPlainText()
        
        # 设置当前模型
        model_index = self.model_combo.findData(self.initial_values['selected_model'])
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
            
    def on_language_changed(self, index):
        """语言改变时的处理函数"""
        lang_code = self.lang_combo.currentData()
        
        # 记录日志
        import logging
        logger = logging.getLogger(__name__)
        
        # 立即保存语言设置到全局配置
        prefs['language'] = lang_code
        prefs.commit()  # 立即提交更改
        
        # 更新界面语言
        self.i18n = get_translation(lang_code)
        
        # 更新界面文字
        self.retranslate_ui()
        
        # 更新模型下拉框中的显示名称
        self.update_model_name_display()
        
        # 手动更新所有Reset按钮的文本和工具提示
        # 通过对象名称或属性识别Reset按钮，而不是通过文本匹配
        for button in self.findChildren(QPushButton):
            # 检查按钮的objectName或其他属性来识别Reset按钮
            if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                button.setText(self.i18n.get('reset_button', 'Reset to Default'))
            # 如果按钮没有objectName，则尝试使用其他方式识别
            elif button.property('isResetButton') or (
                  hasattr(button, 'toolTip') and 
                  ('reset' in button.toolTip().lower() or 
                   'default' in button.toolTip().lower())):
                button.setText(self.i18n.get('reset_button', 'Reset to Default'))
        
        # 更新模型配置控件中的文本和Reset按钮
        if hasattr(self, 'model_widgets'):
            for model_id, widget in self.model_widgets.items():
                if hasattr(widget, 'i18n'):
                    widget.i18n = self.i18n  # 更新i18n字典
                    # 调用模型配置控件的retranslate_ui方法更新所有文本
                    if hasattr(widget, 'retranslate_ui') and callable(widget.retranslate_ui):
                        widget.retranslate_ui()
                    
                    # 对所有按钮进行额外检查，确保重置按钮文本被正确更新
                    reset_text = self.i18n.get('reset_button', 'Reset to Default')
                    reset_tooltip = self.i18n.get('reset_tooltip', 'Reset to default value')
                    
                    for button in widget.findChildren(QPushButton):
                        # 检查按钮的objectName
                        if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                        # 检查按钮的isResetButton属性
                        elif button.property('isResetButton'):
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                        # 检查按钮的工具提示
                        elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                        # 检查按钮的当前文本
                        elif button.text() in ['Reset to Default', 'Reset', '重置', 'Réinitialiser', 'リセット', 'Nollaa', 'Tilbakestill', 'Nulstil', 'Återställ']:
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
        
        # 更新模板内容
        self.template_edit.setPlainText(get_default_template(lang_code))
        self.template_edit.setPlaceholderText(self.i18n.get('template_placeholder', 'Enter your prompt template here...'))
        
        # 更新多书模板内容
        self.multi_book_template_edit.setPlainText(get_multi_book_template(lang_code))
        self.multi_book_template_edit.setPlaceholderText(self.i18n.get('multi_book_template_placeholder', 'Enter your multi-book prompt template here...'))
        
        # 更新随机问题提示词
        random_questions = get_prefs().get('random_questions', {})
        saved_questions = random_questions.get(lang_code)
        if saved_questions and saved_questions.strip():
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(lang_code)
        self.random_questions_edit.setPlainText(default_value)
        self.random_questions_edit.setPlaceholderText(self.i18n.get('random_questions_placeholder', 'Enter your random questions prompts here...'))
        
        # 确保所有标签都被更新，使用更全面的方法
        # 首先更新所有标签页和标签文本
        self.setWindowTitle(self.i18n.get('config_title', 'Ask AI Plugin Configuration'))
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, self.i18n.get('general_tab', 'General'))
            self.tab_widget.setTabText(1, self.i18n.get('ai_models', 'AI'))
        
        # 更新GroupBox标题
        for group_box in self.findChildren(QGroupBox):
            if 'display' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('display', 'Display'))
            elif 'ai' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('ai_models', 'AI'))
            elif 'prompt' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('prompt_template', 'Prompts'))
        
        # 更新所有标签
        known_labels = {
            'language': self.i18n.get('language_label', 'Language:'),
            'current_ai': self.i18n.get('current_ai', 'Current AI:'),
            'api_key': self.i18n.get('api_key_label', 'API Key:'),
            'base_url': self.i18n.get('base_url_label', 'Base URL:'),
            'model': self.i18n.get('model_label', 'Model:'),
            'ask_prompts': self.i18n.get('ask_prompts', 'Ask Prompts:'),
            'random_questions': self.i18n.get('random_questions_prompts', 'Random Questions Prompts:'),
            'prompt_template': self.i18n.get('prompt_template', 'Prompt Template:')
        }
        
        # 对每个标签进行处理
        for label in self.findChildren(QLabel):
            # 先检查objectName
            if hasattr(label, 'objectName') and label.objectName():
                obj_name = label.objectName().lower()
                for key, value in known_labels.items():
                    if key in obj_name:
                        label.setText(value)
                        break
            
            # 如果没有匹配到objectName，则尝试匹配当前文本
            current_text = label.text()
            if current_text in known_labels.values():
                continue  # 已经是最新的翻译，无需更新
            
            # 检查关键字匹配
            current_text_lower = current_text.lower()
            for key, value in known_labels.items():
                # 关键字匹配逻辑
                if key == 'language' and ('language' in current_text_lower or '语言' in current_text_lower or '言語' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'current_ai' and ('current' in current_text_lower or 'ai' in current_text_lower or '当前' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'api_key' and ('api' in current_text_lower or 'key' in current_text_lower or '密钥' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'base_url' and ('url' in current_text_lower or 'base' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'model' and ('model' in current_text_lower or '模型' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'ask_prompts' and (('ask' in current_text_lower and 'prompt' in current_text_lower) or '提问提示' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'random_questions' and (('random' in current_text_lower and 'question' in current_text_lower) or '随机问题' in current_text_lower):
                    label.setText(value)
                    break
                elif key == 'prompt_template' and (('prompt' in current_text_lower and 'template' in current_text_lower) or '提示模板' in current_text_lower or '提示词模板' in current_text_lower):
                    label.setText(value)
                    
        # 更新initial_values中的语言，避免重复触发语言变更检测
        self.initial_values['language'] = lang_code
        
        # 发出语言改变信号，通知其他组件更新界面
        self.language_changed.emit(lang_code)
        
        # 语言切换后自动保存配置
        logger.info(f"语言切换后自动保存配置")
        self.save_settings()
        logger.info(f"配置已自动保存")
    
    def retranslate_ui(self):
        """更新界面文字"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 更新标题和按钮文本
        self.setWindowTitle(self.i18n.get('config_title', 'Ask AI Plugin Configuration'))
        #self.save_button.setText(self.i18n.get('save_button', 'Save'))
        
        # 更新成功提示文字
        if hasattr(self, 'save_success_label') and not self.save_success_label.isHidden():
            self.save_success_label.setText(self.i18n.get('save_success', 'Settings saved successfully!'))
        
        # 更新各个标签页标题
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, self.i18n.get('general_tab', 'General'))
            self.tab_widget.setTabText(1, self.i18n.get('ai_models', 'AI'))
        
        # 更新GroupBox标题（使用ObjectName，语言无关）
        groupbox_map = {
            'groupbox_display': ('display', 'Display'),
            'groupbox_ai_models': ('ai_models', 'AI'),
            'groupbox_prompt_template': ('prompt_template', 'Prompts')
        }
        
        for group_box in self.findChildren(QGroupBox):
            obj_name = group_box.objectName()
            if obj_name in groupbox_map:
                i18n_key, fallback = groupbox_map[obj_name]
                new_title = self.i18n.get(i18n_key, fallback)
                old_title = group_box.title()
                group_box.setTitle(new_title)
        
        # 更新所有标签文本（使用ObjectName，语言无关）
        label_map = {
            'label_language': ('language_label', 'Language:'),
            'label_current_ai': ('current_ai', 'Current AI:'),
            'label_request_timeout': ('request_timeout_label', 'Request Timeout:'),
            'label_parallel_ai_count': ('parallel_ai_count_label', 'Parallel AI Count:'),
        }
        
        # 对每个标签进行处理
        for label in self.findChildren(QLabel):
            obj_name = label.objectName()
            if obj_name in label_map:
                i18n_key, fallback = label_map[obj_name]
                new_text = self.i18n.get(i18n_key, fallback)
                old_text = label.text()
                label.setText(new_text)
                logger.debug(f"更新了标签 [{obj_name}]: {old_text} -> {new_text}")
        
        # 更新所有按钮文本
        reset_text = self.i18n.get('reset_current_ai', 'Reset Current AI to Default')
        reset_tooltip = self.i18n.get('reset_tooltip', 'Reset current AI to default values')
        #save_text = self.i18n.get('save_button', 'Save')
        
        for button in self.findChildren(QPushButton):
            # 通过objectName或属性识别Reset按钮
            if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            # 通过属性识别
            elif button.property('isResetButton'):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            # 通过工具提示识别
            elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            # 通过当前文本识别
            elif button.text() in ['Reset to Default', 'Reset Current AI to Default', '重置', '重置当前AI为默认值', 'Réinitialiser', 'リセット']:
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            # 更新Save按钮
            #elif button.text() in ['Save', '保存', 'Sauvegarder', '保存する']:
            #    button.setText(save_text)
            #    logger.debug(f"更新了Save按钮文本为: {save_text}")
        
        # 更新模型配置控件
        if hasattr(self, 'model_widgets'):
            for model_id, widget in self.model_widgets.items():
                if hasattr(widget, 'i18n'):
                    widget.i18n = self.i18n
                    pass  # 配置控件已更新
        
        # 更新模型下拉框中的显示名称
        self.update_model_name_display()
        logger.debug("更新了模型下拉框中的显示名称")
        
        # 更新占位符提示文本（多书提示词模板说明）
        for label in self.findChildren(QLabel):
            text = label.text()
            # 检查是否是占位符提示（包含 {books_metadata} 或 {query}）
            if '{books_metadata}' in text or '{query}' in text or 'book information' in text.lower() or '书籍信息' in text or 'информац' in text.lower():
                label.setText(self.i18n.get('multi_book_placeholder_hint', 'Use {books_metadata} for book information, {query} for user question'))
                logger.debug("更新了多书提示词占位符提示文本")
                break
        
        # 更新"秒"标签
        for label in self.findChildren(QLabel):
            text = label.text()
            if text in ['seconds', '秒', 'секунд', 'secondes', 'Sekunden', 'sekuntia']:
                label.setText(self.i18n.get('seconds', 'seconds'))
                logger.debug("更新了秒标签文本")
                break
        
        # 更新超时输入框的placeholder
        if hasattr(self, 'timeout_input'):
            self.timeout_input.setPlaceholderText(self.i18n.get('timeout_placeholder', '60'))
            logger.debug("更新了超时输入框placeholder")
        
        # 更新多书提示词模板的默认内容（如果当前内容为空或为默认值）
        if hasattr(self, 'multi_book_template_edit'):
            current_text = self.multi_book_template_edit.toPlainText().strip()
            # 获取当前语言代码
            current_lang = self.lang_combo.currentData() if hasattr(self, 'lang_combo') else 'en'
            # 获取该语言的默认多书模板
            default_multi_book_template = get_multi_book_template(current_lang)
            # 如果当前内容为空，则填充默认模板
            if not current_text:
                self.multi_book_template_edit.setPlainText(default_multi_book_template)
                logger.debug(f"更新了多书模板为语言 {current_lang} 的默认值")
            # 如果当前内容是其他语言的默认模板，也更新为当前语言的默认模板
            else:
                # 检查是否是任何语言的默认模板
                all_langs = get_all_languages()
                is_default_template = False
                for lang_code in all_langs.keys():
                    try:
                        lang_default = get_multi_book_template(lang_code)
                        # 移除空格和换行符进行比较
                        if current_text.replace(' ', '').replace('\n', '') == lang_default.replace(' ', '').replace('\n', ''):
                            is_default_template = True
                            break
                    except:
                        pass
                
                if is_default_template:
                    self.multi_book_template_edit.setPlainText(default_multi_book_template)
                    logger.debug(f"检测到默认模板，更新为语言 {current_lang} 的默认值")
    
    def on_parallel_count_changed(self):
        """并行AI数量变更处理"""
        import logging
        logger = logging.getLogger(__name__)
        
        self._update_panel_ai_selectors()
        
        # 并行AI数量切换后自动保存配置
        logger.info(f"并行AI数量切换后自动保存配置")
        self.save_settings()
        logger.info(f"配置已自动保存")
    
    def _update_panel_ai_selectors(self):
        """更新并行AI选择器"""
        # 清除旧的选择器
        for widget in self.panel_ai_selectors:
            widget.deleteLater()
        self.panel_ai_selectors.clear()
        
        # 获取当前并行数量
        parallel_count = self.parallel_ai_combo.currentData()
        if not parallel_count or parallel_count <= 1:
            return
        
        # 获取已配置的AI列表（细节1：显示"AI服务 + 模型名称"）
        prefs = get_prefs()
        models_config = prefs.get('models', {})
        configured_ais = []
        for model_id, config in models_config.items():
            if config.get('enabled', False):
                # 检查是否有API Key（Ollama不需要）
                has_key = False
                if model_id == 'ollama':
                    has_key = True
                elif model_id == 'grok':
                    has_key = bool(config.get('auth_token', '').strip())
                else:
                    has_key = bool(config.get('api_key', '').strip())
                
                if has_key:
                    # 构建显示文本：AI服务名 + 模型名
                    display_name = config.get('display_name', model_id)
                    model_name = config.get('model', '')
                    if model_name:
                        display_text = f"{display_name} ({model_name})"
                    else:
                        display_text = display_name
                    configured_ais.append((model_id, display_text))
        
        # 读取当前的AI选择
        saved_selections = prefs.get('panel_ai_selections', {})
        
        # 获取当前选中的主要AI
        current_ai = prefs.get('selected_model', 'grok')
        
        # 为每个面板创建选择器
        for i in range(parallel_count):
            panel_layout = QHBoxLayout()
            
            panel_label = QLabel(f"{self.i18n.get('ai_panel_label', 'AI {index}:').format(index=i+1)}")
            panel_label.setMinimumWidth(60)  # 固定标签宽度，保持对齐
            panel_layout.addWidget(panel_label)
            
            # 细节3：始终显示下拉框（即使没有配置AI）
            panel_combo = NoScrollComboBox()
            # 细节2：下拉框充满右侧空间
            panel_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            # 添加AI选项
            # 对于AI 1：显示所有已配置的AI
            # 对于AI 2及以上：只有当配置的AI数量 > 面板索引时才显示
            should_show_ais = (i == 0) or (len(configured_ais) > i)
            
            # 先添加占位符选项（与询问弹窗保持一致）
            placeholder_text = self.i18n.get('select_ai', '-- Select AI --')
            panel_combo.addItem(placeholder_text, None)
            
            if should_show_ais and configured_ais:
                # 有足够的AI时，添加AI列表
                for ai_id, display_text in configured_ais:
                    panel_combo.addItem(display_text, ai_id)
            else:
                # 没有足够的AI时，添加提示项
                hint_text = self.i18n.get('add_more_ai_providers', 'Please add more AI providers in settings')
                panel_combo.addItem(hint_text, None)
                # 禁用提示项，使其无法被选中
                model = panel_combo.model()
                item = model.item(1)  # 第二项是提示项
                if item:
                    item.setEnabled(False)
            
            # 智能选择默认AI
            default_ai = None
            if should_show_ais and configured_ais:
                if i == 0:
                    # AI 1：默认选择当前主要AI
                    default_ai = current_ai
                elif i == 1 and len(configured_ais) >= 2:
                    # AI 2：选择下一个不同的AI
                    for ai_id, _ in configured_ais:
                        if ai_id != current_ai:
                            default_ai = ai_id
                            break
            
            # 设置当前选中的AI：优先使用保存的选择，其次使用智能选择
            saved_ai = saved_selections.get(f'panel_{i}')
            if saved_ai and should_show_ais and configured_ais:
                index = panel_combo.findData(saved_ai)
                if index >= 0:
                    panel_combo.setCurrentIndex(index)
                else:
                    # 保存的AI不存在，重置为占位符
                    panel_combo.setCurrentIndex(0)
            elif default_ai and should_show_ais and configured_ais:
                index = panel_combo.findData(default_ai)
                if index >= 0:
                    panel_combo.setCurrentIndex(index)
                    # 保存默认选择
                    if 'panel_ai_selections' not in prefs:
                        prefs['panel_ai_selections'] = {}
                    prefs['panel_ai_selections'][f'panel_{i}'] = default_ai
                else:
                    # 默认AI不存在，重置为占位符
                    panel_combo.setCurrentIndex(0)
            else:
                # 没有保存的选择且没有默认AI，显示占位符
                panel_combo.setCurrentIndex(0)
            
            # 连接信号触发保存按钮
            panel_combo.currentIndexChanged.connect(lambda idx, panel_idx=i: self._on_panel_ai_selector_changed(panel_idx))
            
            panel_layout.addWidget(panel_combo)
            
            # 添加到布局
            container = QWidget()
            container.setLayout(panel_layout)
            self.panel_ai_selectors_layout.addWidget(container)
            self.panel_ai_selectors.append(container)
    
    def _on_panel_ai_selector_changed(self, panel_index):
        """面板AI选择器变更处理"""
        # 保存选择
        prefs = get_prefs()
        selections = prefs.get('panel_ai_selections', {})
        
        # 获取当前选中的AI
        if panel_index < len(self.panel_ai_selectors):
            container = self.panel_ai_selectors[panel_index]
            combo = container.findChild(QComboBox)
            if combo:
                ai_id = combo.currentData()
                if ai_id:
                    selections[f'panel_{panel_index}'] = ai_id
                    logger.info(f"配置页面：保存面板 {panel_index} 的AI选择: {ai_id}")
        
        prefs['panel_ai_selections'] = selections
        self.on_config_changed()
    
    def save_settings(self):
        """保存设置"""
        import logging
        logger = logging.getLogger(__name__)
        
        prefs = get_prefs()
        
        # 保存语言设置
        prefs['language'] = self.lang_combo.currentData()
        
        # 保存模板
        prefs['template'] = self.template_edit.toPlainText().strip()
        
        # 保存多书提示词模板
        prefs['multi_book_template'] = self.multi_book_template_edit.toPlainText().strip()
        
        # 保存随机问题提示词
        current_lang = prefs['language']
        if 'random_questions' not in prefs:
            prefs['random_questions'] = {}
        prefs['random_questions'][current_lang] = self.random_questions_edit.toPlainText().strip()
        
        # 保存请求超时时间
        if hasattr(self, 'timeout_input'):
            timeout_value = self.timeout_input.text().strip()
            if timeout_value:
                prefs['request_timeout'] = int(timeout_value)
            else:
                prefs['request_timeout'] = 60  # 默认值
        
        # 保存并行AI数量
        if hasattr(self, 'parallel_ai_combo'):
            prefs['parallel_ai_count'] = self.parallel_ai_combo.currentData()
        
        # 保存Export配置
        if hasattr(self, 'enable_default_folder_checkbox'):
            prefs['enable_default_export_folder'] = self.enable_default_folder_checkbox.isChecked()
        if hasattr(self, 'export_folder_label'):
            folder_text = self.export_folder_label.text()
            if folder_text != self.i18n.get('no_folder_selected', 'No folder selected'):
                prefs['default_export_folder'] = folder_text
            else:
                prefs['default_export_folder'] = ''
        
        # 保存选中的模型
        prefs['selected_model'] = self.model_combo.currentData()
        
        # 保存所有模型的配置
        models_config = prefs.get('models', {})
        
        # 保存所有模型的配置，而不仅仅是当前选中的模型
        for model_id, widget in self.model_widgets.items():
            model_config = widget.get_config()
            models_config[model_id] = model_config
            pass  # 模型配置已保存
        
        prefs['models'] = models_config
        # 所有模型配置已保存
        
        # 更新按钮状态
        #self.save_button.setEnabled(False)
        
        # 重置未保存的输入框变化标志
        self.has_unsaved_input_changes = False
        
        # 显示保存成功提示
        if hasattr(self, 'save_success_label'):
            self.save_success_label.setText(self.i18n.get('save_success', 'Settings saved successfully!'))
            self.save_success_label.show()
            QTimer.singleShot(2000, self.save_success_label.hide)
        
        # 发出保存成功信号
        self.settings_saved.emit()
        
        # 确保设置已经写入到磁盘
        from calibre.utils.config import JSONConfig
        if isinstance(prefs, JSONConfig):
            prefs.commit()
            # 强制JSONConfig重新加载配置文件
            prefs.refresh()
            # 获取刷新后的配置并安全地记录日志
            refreshed_models = safe_log_config(prefs.get('models', {}))
            pass  # 配置已刷新
        
        # 重新获取最新的prefs值，确保我们使用的是已保存的值
        prefs = get_prefs(force_reload=True)  # 添加force_reload参数
        # 安全地记录重新获取的prefs
        reloaded_models = safe_log_config(prefs.get('models', {}))
        # 配置已重新加载
        current_lang = prefs.get('language', 'en')
        
        # 更新初始值，但不重新加载界面元素
        # 只更新初始值字典，不重新设置界面元素
        # 保存初始值
        self.initial_values = {
            'language': current_lang,
            'template': prefs.get('template', get_default_template(current_lang)),
            'multi_book_template': prefs.get('multi_book_template', ''),
            'selected_model': prefs.get('selected_model', 'grok'),
            'models': copy.deepcopy(prefs.get('models', {})),
            'random_questions': copy.deepcopy(prefs.get('random_questions', {})),
            'request_timeout': prefs.get('request_timeout', 60),
            'parallel_ai_count': prefs.get('parallel_ai_count', 1),
            'enable_default_export_folder': prefs.get('enable_default_export_folder', False),
            'default_export_folder': prefs.get('default_export_folder', '')
        }
        
        # 更新原始文本值（用于变更检测）
        if hasattr(self, 'template_edit'):
            self.initial_values['template_raw'] = self.template_edit.toPlainText()
        if hasattr(self, 'multi_book_template_edit'):
            self.initial_values['multi_book_template_raw'] = self.multi_book_template_edit.toPlainText()
        if hasattr(self, 'random_questions_edit'):
            if 'random_questions_raw' not in self.initial_values:
                self.initial_values['random_questions_raw'] = {}
            self.initial_values['random_questions_raw'][current_lang] = self.random_questions_edit.toPlainText()
        
        # 安全地记录更新后的初始值
        updated_models = safe_log_config(self.initial_values['models'])
        # 初始值已更新
        
        # 确保设置已经写入到磁盘
        from calibre.utils.config import JSONConfig
        if isinstance(prefs, JSONConfig):
            prefs.commit()
    
    def check_for_changes(self):
        """检查是否有配置变更
        
        :return: 如果有变更返回 True，否则返回 False
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取当前语言
        current_lang = self.lang_combo.currentData()
        
        # 确保 initial_values 存在并包含必要的键
        if not hasattr(self, 'initial_values') or not isinstance(self.initial_values, dict):
            self.initial_values = {}
        
        # 确保必要的键存在
        for key in ['language', 'template', 'multi_book_template', 'selected_model', 'models', 'random_questions', 'request_timeout', 'parallel_ai_count']:
            if key not in self.initial_values:
                if key == 'language':
                    self.initial_values[key] = 'en'
                elif key == 'template' or key == 'multi_book_template':
                    self.initial_values[key] = ''
                elif key == 'selected_model':
                    self.initial_values[key] = 'grok'
                elif key == 'models' or key == 'random_questions':
                    self.initial_values[key] = {}
                elif key == 'request_timeout':
                    self.initial_values[key] = 60
                elif key == 'parallel_ai_count':
                    self.initial_values[key] = 1
        
        # 检查通用设置是否更改
        general_changed = False
        
        # 检查语言设置是否更改
        if current_lang != self.initial_values['language']:
            general_changed = True
            logger.debug(f"语言设置已更改: {current_lang} != {self.initial_values['language']}")
        
        # 检查模型选择是否更改
        if hasattr(self, 'model_combo') and self.model_combo.currentData() != self.initial_values['selected_model']:
            general_changed = True
            logger.debug(f"模型选择已更改: {self.model_combo.currentData()} != {self.initial_values['selected_model']}")
        
        # 检查模板是否更改（使用原始文本，不 strip，以便检测空格变化）
        if hasattr(self, 'template_edit'):
            template_text = self.template_edit.toPlainText()
            # 保存时会 strip，所以这里也需要比较 strip 后的值
            # 但为了让用户看到即时反馈，我们比较原始文本
            if template_text != self.initial_values.get('template_raw', self.initial_values['template']):
                general_changed = True
                logger.debug("模板已更改")
        
        # 检查多书提示词模板是否更改（使用原始文本）
        if hasattr(self, 'multi_book_template_edit'):
            multi_book_template_text = self.multi_book_template_edit.toPlainText()
            if multi_book_template_text != self.initial_values.get('multi_book_template_raw', self.initial_values.get('multi_book_template', '')):
                general_changed = True
                logger.debug("多书提示词模板已更改")
        
        # 检查随机问题提示词是否更改（使用原始文本）
        random_questions_changed = False
        initial_random_questions = self.initial_values['random_questions'].get(current_lang, '')
        
        current_random_questions = ''
        if hasattr(self, 'random_questions_edit'):
            current_random_questions = self.random_questions_edit.toPlainText()
            # 同样使用原始文本比较
            initial_raw = self.initial_values.get('random_questions_raw', {}).get(current_lang, initial_random_questions)
            if current_random_questions != initial_raw:
                random_questions_changed = True
                logger.debug("随机问题提示词已更改")
        
        # 检查请求超时时间是否更改
        timeout_changed = False
        if hasattr(self, 'timeout_input'):
            current_timeout = self.timeout_input.text().strip()
            if current_timeout:
                try:
                    if int(current_timeout) != self.initial_values['request_timeout']:
                        timeout_changed = True
                        logger.debug("请求超时时间已更改")
                except ValueError:
                    pass
        
        # 检查并行AI数量是否更改
        parallel_ai_changed = False
        if hasattr(self, 'parallel_ai_combo'):
            current_parallel = self.parallel_ai_combo.currentData()
            if current_parallel != self.initial_values.get('parallel_ai_count', 1):
                parallel_ai_changed = True
                logger.debug(f"并行AI数量已更改: {current_parallel} != {self.initial_values.get('parallel_ai_count', 1)}")
        
        # 检查模型配置是否更改
        models_changed = False
        if hasattr(self, 'model_widgets'):
            try:
                for model_id, widget in self.model_widgets.items():
                    if model_id in self.initial_values['models']:
                        try:
                            current_config = widget.get_config()
                            if current_config != self.initial_values['models'][model_id]:
                                models_changed = True
                                pass  # 配置已更改
                                break
                        except Exception as e:
                            logger.error(f"获取模型 {model_id} 配置时出错: {str(e)}")
            except Exception as e:
                logger.error(f"检查模型配置时出错: {str(e)}")
        
        # 返回是否有变更
        return general_changed or models_changed or random_questions_changed or timeout_changed or parallel_ai_changed
    
    def on_config_changed(self):
        """当任何配置发生改变时检查是否需要启用保存按钮"""
        # 如果正在初始化，不标记为有变化
        if self._is_initializing:
            return
        
        # 标记有未保存的输入框变化
        self.has_unsaved_input_changes = True
        
        # 检查是否有配置变更
        has_changes = self.check_for_changes()
        
        # 发送配置变更信号
        self.config_changed.emit()
    
    def reset_to_initial_values(self):
        """重置到初始值"""
        # 重置语言
        lang_index = self.lang_combo.findData(self.initial_values['language'])
        if lang_index >= 0:
            self.lang_combo.setCurrentIndex(lang_index)
        
        # 重置模板
        self.template_edit.setPlainText(self.initial_values['template'])
        
        # 重置随机问题提示词
        current_lang = self.initial_values['language']
        random_questions = self.initial_values['random_questions']
        saved_questions = random_questions.get(current_lang)
        if saved_questions:
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(current_lang)
        self.random_questions_edit.setPlainText(default_value)
        
        # 重置选中的模型
        model_index = self.model_combo.findData(self.initial_values['selected_model'])
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        
        # 更新模型名称显示
        self.update_model_name_display()
        
        # 重置模型配置
        self.setup_model_widgets()
        
        # 重置按钮状态
        #self.save_button.setEnabled(False)
        #self.save_success_label.setText('')
        #self.save_success_label.hide()
    
    def _on_export_config_changed(self):
        """Export配置改变时的回调"""
        # 启用/禁用浏览按钮
        is_enabled = self.enable_default_folder_checkbox.isChecked()
        self.browse_folder_button.setEnabled(is_enabled)
        
        # 标记配置已修改
        self.on_config_changed()
    
    def _on_browse_export_folder(self):
        """浏览并选择导出文件夹"""
        from PyQt5.QtWidgets import QFileDialog
        import os
        
        # 获取当前路径（如果有）
        current_folder = self.export_folder_label.text()
        if current_folder == self.i18n.get('no_folder_selected', 'No folder selected'):
            current_folder = os.path.expanduser('~')  # 默认用户主目录
        
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(
            self,
            self.i18n.get('select_export_folder', 'Select Export Folder'),
            current_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            # 更新标签显示
            self.export_folder_label.setText(folder)
            
            # 标记配置已修改
            self.on_config_changed()
    
    def on_reset_all_data(self):
        """重置所有插件数据"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 显示确认对话框
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.i18n.get('reset_all_data_confirm_title', 'Confirm Reset'))
        msg_box.setText(self.i18n.get('reset_all_data_confirm_message',
            'Are you sure you want to reset the plugin to its initial state?\n\n'
            'This will permanently delete:\n'
            '• All API Keys\n'
            '• All custom prompt templates\n'
            '• All conversation history\n'
            '• All plugin settings\n\n'
            'This action cannot be undone!'))
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # 自定义按钮文本
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)
        yes_button.setText(self.i18n.get('yes', 'Yes'))
        no_button.setText(self.i18n.get('no', 'No'))
        
        result = msg_box.exec_()
        
        if result == QMessageBox.Yes:
            try:
                logger.info("开始重置所有插件数据...")
                
                # 保存当前的语言设置（重置时不删除语言选择）
                current_language = get_prefs().get('language', 'en')
                logger.info(f"保存当前语言设置: {current_language}")
                
                # 1. 删除配置文件
                from calibre.utils.config import JSONConfig
                import os
                
                # 获取配置文件路径
                config_dir = os.path.join(os.path.expanduser('~'), '.config', 'calibre', 'plugins')
                config_file = os.path.join(config_dir, 'ask_ai_plugin.json')
                
                if os.path.exists(config_file):
                    os.remove(config_file)
                    logger.info(f"已删除配置文件: {config_file}")
                
                # 2. 删除历史记录文件
                # 删除v2版本的历史记录JSON文件
                history_v2_path = os.path.join(config_dir, 'ask_ai_plugin_history_v2.json')
                if os.path.exists(history_v2_path):
                    os.remove(history_v2_path)
                    logger.info(f"已删除历史记录文件(v2): {history_v2_path}")
                
                # 删除旧版本的历史记录数据库（如果存在）
                history_db_path = os.path.join(config_dir, 'ask_ai_plugin_history.db')
                if os.path.exists(history_db_path):
                    os.remove(history_db_path)
                    logger.info(f"已删除历史记录数据库(旧版): {history_db_path}")
                
                # 3. 删除日志文件（可选）
                log_dir = os.path.join(os.path.expanduser('~'), '.config', 'calibre', 'ask_grok_logs')
                if os.path.exists(log_dir):
                    import shutil
                    shutil.rmtree(log_dir)
                    logger.info(f"已删除日志目录: {log_dir}")
                
                # 4. 强制重新加载配置（这会触发默认值的重新初始化）
                get_prefs(force_reload=True)
                logger.info("已强制重新加载配置，使用默认值")
                
                # 5. 恢复语言设置（保留用户的语言选择）
                prefs = get_prefs()
                prefs['language'] = current_language
                # 根据恢复的语言设置，重新加载对应语言的默认模板
                prefs['template'] = get_default_template(current_language)
                prefs['multi_book_template'] = get_multi_book_template(current_language)
                # 随机问题提示词
                if 'random_questions' not in prefs:
                    prefs['random_questions'] = {}
                prefs['random_questions'][current_language] = get_suggestion_template(current_language)
                prefs.commit()
                logger.info(f"已恢复语言设置并加载对应语言的默认模板: {current_language}")
                
                # 显示成功消息
                QMessageBox.information(
                    self,
                    self.i18n.get('success', 'Success'),
                    self.i18n.get('reset_all_data_success', 
                        'All plugin data has been reset successfully. Please restart calibre for changes to take effect.')
                )
                
                logger.info("所有插件数据已成功重置")
                
            except Exception as e:
                logger.error(f"重置插件数据失败: {str(e)}", exc_info=True)
                QMessageBox.critical(
                    self,
                    self.i18n.get('error', 'Error'),
                    self.i18n.get('reset_all_data_failed', 'Failed to reset plugin data: {error}').format(error=str(e))
                )
