#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import logging
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, 
                            QPushButton, QHBoxLayout, QFormLayout, QGroupBox, QScrollArea, QSizePolicy,
                            QFrame, QCheckBox, QMessageBox, QApplication)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QEvent
from PyQt5.QtGui import QFontMetrics
from .models.grok import GrokModel
from .models.gemini import GeminiModel
from .models.deepseek import DeepseekModel
from .models.custom import CustomModel
from .models.openai import OpenAIModel
from .models.anthropic import AnthropicModel
from .models.nvidia import NvidiaModel
from .models.nvidia_free import NvidiaFreeModel
from .models.openrouter import OpenRouterModel
from .models.perplexity import PerplexityModel
from .models.ollama import OllamaModel
from calibre.utils.config import JSONConfig
from .env_config import EnvironmentConfig

from .i18n import get_default_template, get_translation, get_suggestion_template, get_multi_book_template, get_all_languages
from .models.base import AIProvider, ModelConfig, DEFAULT_MODELS, AIModelFactory, BaseAIModel
from .utils import mask_api_key, mask_api_key_in_text, safe_log_config
from .widgets import NoScrollComboBox, apply_button_style
from .ui_constants import (
    SPACING_TINY, SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
    MARGIN_MEDIUM, PADDING_MEDIUM,
    TEXT_COLOR_PRIMARY, TEXT_COLOR_SECONDARY, TEXT_COLOR_SECONDARY_STRONG, BG_COLOR_ALTERNATE,
    get_groupbox_style, get_separator_style, get_subtitle_style, get_section_title_style,
    get_list_widget_style
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
NVIDIA_FREE_CONFIG = get_current_model_config(AIProvider.AI_NVIDIA_FREE)
OPENROUTER_CONFIG = get_current_model_config(AIProvider.AI_OPENROUTER)
PERPLEXITY_CONFIG = get_current_model_config(AIProvider.AI_PERPLEXITY)
OLLAMA_CONFIG = get_current_model_config(AIProvider.AI_OLLAMA)

# 默认配置
prefs.defaults['selected_model'] = 'nvidia_free'  # 当前选中的模型（默认使用免费通道）
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
    'perplexity': {
        'api_key': '',
        'api_base_url': PERPLEXITY_CONFIG.default_api_base_url,
        'model': PERPLEXITY_CONFIG.default_model_name,
        'display_name': PERPLEXITY_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'ollama': {
        'api_key': '',  # Optional for Ollama (local service)
        'api_base_url': OLLAMA_CONFIG.default_api_base_url,
        'model': OLLAMA_CONFIG.default_model_name,
        'display_name': OLLAMA_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': False  # 默认不启用，需要用户配置
    },
    'nvidia_free': {
        'api_key': 'free-tier',  # 免费通道不需要真实 API Key
        'proxy_url': EnvironmentConfig.get_nvidia_free_proxy_url(),
        'api_base_url': EnvironmentConfig.get_nvidia_free_proxy_url(),
        'model': NVIDIA_FREE_CONFIG.default_model_name,
        'display_name': NVIDIA_FREE_CONFIG.display_name,
        'enable_streaming': True,
        'enabled': True,  # 默认启用免费通道
        'provider_id': 'nvidia_free'
    }
}
prefs.defaults['template'] = get_default_template('en')
prefs.defaults['multi_book_template'] = get_multi_book_template('en')
prefs.defaults['language'] = 'en'
prefs.defaults['language_user_set'] = False
prefs.defaults['ask_dialog_width'] = 800
prefs.defaults['ask_dialog_height'] = 600
prefs.defaults['random_questions'] = ''  # v1.3.9: Changed from dict to string (prompt template)
prefs.defaults['request_timeout'] = 60  # Default timeout in seconds
prefs.defaults['parallel_ai_count'] = 1  # Number of parallel AI requests (1-4)
prefs.defaults['cached_models'] = {}  # Cached model lists for each AI provider
prefs.defaults['nvidia_free_first_use_shown'] = False  # Track if first use reminder has been shown

# Export settings
prefs.defaults['enable_default_export_folder'] = False  # Whether to export to default folder
prefs.defaults['default_export_folder'] = ''  # Default export folder path
prefs.defaults['copy_mode'] = 'response'  # Copy mode: 'response' or 'qa'
prefs.defaults['export_mode'] = 'current'  # Export mode: 'current' or 'history'

# Persona settings
prefs.defaults['use_persona'] = True  # Whether to use persona in prompts
prefs.defaults['persona'] = 'As a researcher, I want to research through book data.'  # User's persona text

# Language preference settings (v1.3.9)
prefs.defaults['use_interface_language'] = False  # Whether to ask AI to respond in interface language

# Library Chat settings (v1.4.2 MVP)
prefs.defaults['library_chat_enabled'] = False  # Enable library chat feature
prefs.defaults['library_cached_metadata'] = ''  # Cached library metadata (JSON string)
prefs.defaults['library_last_update'] = ''  # Last update timestamp (ISO format)
prefs.defaults['ai_search_first_time'] = True  # Show welcome dialog only on first use
prefs.defaults['ai_search_last_history_uid'] = None  # Last AI Search conversation UID for history persistence

def get_prefs(force_reload=False):
    """获取配置
    
    Args:
        force_reload: 是否强制重新加载配置文件
    """
    # 如果需要强制重新加载
    if force_reload and isinstance(prefs, JSONConfig):
        prefs.refresh()
    
    # 确保语言键存在，如果不存在则使用默认值 'en'
    if 'language' not in prefs:
        prefs['language'] = 'en'

    # 如果用户没有在插件内明确选择过语言，则默认跟随 calibre 的界面语言（若插件支持）
    # calibre 语言来自 Preferences -> Look & Feel -> Choose language
    try:
        if not prefs.get('language_user_set', False):
            from calibre.utils.localization import get_lang

            calibre_lang = (get_lang() or 'en').replace('-', '_')
            base = calibre_lang.split('_')[0].lower()

            # Map calibre language codes to plugin language codes
            # 支持的语言映射表
            lang_mapping = {
                'zh': 'zh',      # Chinese Simplified
                'en': 'en',      # English
                'ja': 'ja',      # Japanese
                'fr': 'fr',      # French
                'de': 'de',      # German
                'es': 'es',      # Spanish
                'ru': 'ru',      # Russian
                'pt': 'pt',      # Portuguese
                'nl': 'nl',      # Dutch
                'sv': 'sv',      # Swedish
                'no': 'no',      # Norwegian
                'fi': 'fi',      # Finnish
                'da': 'da',      # Danish
                'yue': 'yue',    # Cantonese
            }
            
            plugin_lang = lang_mapping.get(base)
            
            # Special handling for Chinese variants
            if base == 'zh':
                upper = calibre_lang.upper()
                if '_TW' in upper or '_HK' in upper or '_MO' in upper:
                    plugin_lang = 'zht'  # Traditional Chinese
                else:
                    plugin_lang = 'zh'   # Simplified Chinese

            supported = {code for code, _ in SUPPORTED_LANGUAGES}
            if plugin_lang and plugin_lang in supported and prefs.get('language', 'en') != plugin_lang:
                prefs['language'] = plugin_lang
                # 同时更新模板为对应语言的默认模板
                prefs['template'] = get_default_template(plugin_lang)
                prefs['multi_book_template'] = get_multi_book_template(plugin_lang)
                prefs.commit()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to inherit Calibre language: {e}")
    
    # 确保模板不为空，如果为空则使用当前语言的默认模板
    # 注意：这个检查必须在语言确定之后执行
    if not prefs['template']:
        prefs['template'] = get_default_template(prefs.get('language', 'en'))
    
    # 确保多书模板不为空
    if not prefs.get('multi_book_template'):
        prefs['multi_book_template'] = get_multi_book_template(prefs.get('language', 'en'))
    
    # 确保 models 键存在
    if 'models' not in prefs:
        prefs['models'] = {}
    
    # 确保 nvidia_free 配置存在（首次安装时的默认 AI）
    if 'nvidia_free' not in prefs['models']:
        prefs['models']['nvidia_free'] = {
            'api_key': 'free-tier',
            'proxy_url': EnvironmentConfig.get_nvidia_free_proxy_url(),
            'api_base_url': EnvironmentConfig.get_nvidia_free_proxy_url(),
            'model': NVIDIA_FREE_CONFIG.default_model_name,
            'display_name': NVIDIA_FREE_CONFIG.display_name,
            'enable_streaming': True,
            'enabled': True,
            'provider_id': 'nvidia_free',
            'is_configured': True  # Nvidia Free 默认已配置
        }
    
    # 确保 selected_model 键存在（默认使用 nvidia_free）
    if 'selected_model' not in prefs:
        prefs['selected_model'] = 'nvidia_free'
    
    # 确保 request_timeout 键存在
    if 'request_timeout' not in prefs:
        prefs['request_timeout'] = 60
    
    # 确保 parallel_ai_count 键存在
    if 'parallel_ai_count' not in prefs:
        prefs['parallel_ai_count'] = 1
    
    # 配置迁移：强制更新 nvidia_free 的 proxy_url 为当前环境配置
    # 这确保环境切换后配置能正确更新
    if 'nvidia_free' in prefs['models']:
        current_env_url = EnvironmentConfig.get_nvidia_free_proxy_url()
        if prefs['models']['nvidia_free'].get('proxy_url') != current_env_url:
            prefs['models']['nvidia_free']['proxy_url'] = current_env_url
            prefs['models']['nvidia_free']['api_base_url'] = current_env_url
            prefs.commit()
    
    # 配置迁移：删除已废弃的 openrouter_free 配置（旧版本遗留数据）
    # 同时删除任何包含 'openrouter' 且 model 为 ':free' 或包含 'free' 的旧配置
    models_to_remove = []
    for config_id, config in prefs['models'].items():
        if not isinstance(config, dict):
            continue
        # 检查是否是废弃的 openrouter free 配置
        if 'openrouter_free' in config_id:
            models_to_remove.append(config_id)
        elif config_id.startswith('openrouter') and config.get('model', '').lower().endswith(':free'):
            models_to_remove.append(config_id)
        elif config.get('provider_id') == 'openrouter_free':
            models_to_remove.append(config_id)
    
    for config_id in models_to_remove:
        del prefs['models'][config_id]
        # 如果当前选中的是被删除的模型，切换到 nvidia_free
        if prefs.get('selected_model') == config_id:
            prefs['selected_model'] = 'nvidia_free'
    
    if models_to_remove:
        prefs.commit()
    
    # 确保默认模型配置存在
    if 'grok' not in prefs['models']:
        prefs['models']['grok'] = {
            'auth_token': '',
            'api_base_url': GROK_CONFIG.default_api_base_url,
            'model': GROK_CONFIG.default_model_name,
            'display_name': GROK_CONFIG.display_name  # 设置固定的显示名称
        }

    # 清理历史配置中误保存的占位符模型名称（例如“-- 切换Model --”）
    # 目的：避免占位符被当作真实 model 写入配置，进而在 UI 中被复制到自定义模型输入框。
    try:
        # 收集所有语言下的 select_model / request_model_list 文本，用于识别占位符
        placeholder_texts = set()
        for code, _name in SUPPORTED_LANGUAGES:
            try:
                t = get_translation(code)
                placeholder_texts.add(t.get('select_model', ''))
                placeholder_texts.add(t.get('request_model_list', ''))
            except Exception:
                pass

        changed = False
        for _model_id, cfg in (prefs.get('models') or {}).items():
            if not isinstance(cfg, dict):
                continue

            # 默认情况下不启用“Use custom model name”
            if 'use_custom_model_name' not in cfg:
                cfg['use_custom_model_name'] = False
                changed = True

            model_val = (cfg.get('model') or '').strip()
            if model_val and model_val in placeholder_texts:
                logger.warning(
                    f"[prefs_sanitize] Detected placeholder model stored in prefs. model_id={_model_id}, model='{model_val}'. Clearing it and disabling use_custom_model_name."
                )
                cfg['model'] = ''
                cfg['use_custom_model_name'] = False
                changed = True
            elif not model_val and cfg.get('use_custom_model_name'):
                # 没有有效 model 时，确保不处于自定义模式
                logger.warning(
                    f"[prefs_sanitize] use_custom_model_name=True but model is empty. model_id={_model_id}. Forcing use_custom_model_name=False."
                )
                cfg['use_custom_model_name'] = False
                changed = True

        if changed:
            prefs.commit()
    except Exception:
        pass
    
    # 不再强制更新模型名称，保留用户的自定义设置
    # 只有当模型名称不存在时，才使用默认值
    
    # 自动判断并设置 is_configured 字段（用于已有配置的兼容性）
    for model_id, model_config in prefs['models'].items():
        if 'is_configured' not in model_config:
            # 获取 provider_id（用于判断模型类型）
            provider_id = model_config.get('provider_id')
            if not provider_id:
                provider_id = model_id.split('_')[0] if '_' in model_id else model_id
            
            # 判断是否已配置
            if provider_id in ['ollama', 'custom', 'nvidia_free']:
                # Ollama、Custom 和 Nvidia Free 不需要用户提供 API Key
                has_auth = True
            else:
                # 其他模型需要 API Key
                api_key_field = 'auth_token' if provider_id == 'grok' else 'api_key'
                has_auth = bool(model_config.get(api_key_field, '').strip())
            
            # 检查是否有模型名称
            has_model = bool(model_config.get('model', '').strip())
            
            # 设置 is_configured 标志
            model_config['is_configured'] = has_auth and has_model
    
    # ========== v1.3.9 兼容性迁移 ==========
    
    # 1. 迁移 random_questions (dict -> string)
    # v1.3.8 使用 dict 格式: {"en": [...], "zh": [...]}
    # v1.3.9 使用 string 格式: 提示词模板
    random_questions = prefs.get('random_questions', '')
    if isinstance(random_questions, dict):
        # 旧版本格式，重置为空字符串（将使用默认模板）
        prefs['random_questions'] = ''
        logger.info("[Migration v1.3.9] random_questions: dict -> string (reset to default template)")
        prefs.commit()
    
    # 2. 确保 use_interface_language 存在
    if 'use_interface_language' not in prefs:
        prefs['use_interface_language'] = False
        logger.info("[Migration v1.3.9] Added use_interface_language = False")
    
    # ========== 迁移结束 ==========
    
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
        # 创建主布局（直接使用 VBoxLayout，更灵活）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(SPACING_MEDIUM)
        
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
        elif self.model_id == 'perplexity':
            provider = AIProvider.AI_PERPLEXITY
            model_config = get_current_model_config(provider)
        elif self.model_id == 'openrouter':
            provider = AIProvider.AI_OPENROUTER
            model_config = get_current_model_config(provider)
        elif self.model_id == 'ollama':
            provider = AIProvider.AI_OLLAMA
            model_config = get_current_model_config(provider)
        elif self.model_id == 'nvidia_free':
            provider = AIProvider.AI_NVIDIA_FREE
            model_config = get_current_model_config(provider)
        
        if model_config:
            from .ui_constants import TEXT_COLOR_SECONDARY_STRONG
            
            # API Key/Token 输入框（Ollama 和 nvidia_free 不需要）
            if self.model_id == 'nvidia_free':
                # Nvidia 免费通道：显示纯文字提示
                api_key_label = QLabel(self.i18n.get('api_key_label', 'API Key'))
                api_key_label.setObjectName(f'label_api_key_{self.model_id}')
                main_layout.addWidget(api_key_label)
                
                # 纯文字提示（不可编辑）
                api_key_info = QLabel(self.i18n.get('nvidia_free_api_key_info', 'Will be obtained from server'))
                api_key_info.setObjectName(f'label_api_key_info_{self.model_id}')
                api_key_info.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 8px; background-color: #f5f5f5; border-radius: 4px;")
                api_key_info.setMinimumHeight(40)
                main_layout.addWidget(api_key_info)
                
                # 免费通道说明
                free_desc = QLabel(self.i18n.get('nvidia_free_desc', 'This service is maintained by the developer and kept free, but may be less stable. For more stable service, please configure your own Nvidia API Key.'))
                free_desc.setObjectName(f'label_free_desc_{self.model_id}')
                free_desc.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 2px 0;")
                free_desc.setWordWrap(True)
                main_layout.addWidget(free_desc)
                
                # 创建空的占位符以保持代码兼容性
                self.api_key_edit = None
            elif self.model_id != 'ollama':
                # API Key 标签
                api_key_label = QLabel(self.i18n.get('api_key_label', 'API Key'))
                api_key_label.setObjectName(f'label_api_key_{self.model_id}')
                main_layout.addWidget(api_key_label)
                
                # API Key 输入框
                self.api_key_edit = QTextEdit(self)
                self.api_key_edit.setPlainText(self.config.get(api_key_field_name, ''))
                self.api_key_edit.textChanged.connect(self.on_api_key_changed)
                self.api_key_edit.setMaximumHeight(62)
                self.api_key_edit.setMinimumWidth(base_width)
                main_layout.addWidget(self.api_key_edit)
                
                # API Key 说明
                api_key_desc = QLabel(self.i18n.get('api_key_desc', 'Your API key for authentication. Keep it secure and do not share.'))
                api_key_desc.setObjectName(f'label_api_key_desc_{self.model_id}')
                api_key_desc.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 2px 0;")
                api_key_desc.setWordWrap(True)
                main_layout.addWidget(api_key_desc)
            else:
                # Ollama 不需要 API Key，创建一个空的占位符以保持代码兼容性
                self.api_key_edit = None
            
            # API Base URL 标签
            base_url_label = QLabel(self.i18n.get('base_url_label', 'Base URL'))
            base_url_label.setObjectName(f'label_base_url_{self.model_id}')
            main_layout.addWidget(base_url_label)
            
            # API Base URL 输入框
            self.api_base_edit = QLineEdit(self)
            self.api_base_edit.setText(self.config.get('api_base_url', model_config.default_api_base_url))
            self.api_base_edit.textChanged.connect(self.on_config_changed)
            self.api_base_edit.setPlaceholderText(self.i18n.get('base_url_placeholder', 'Default: {default_api_base_url}').format(
                default_api_base_url=model_config.default_api_base_url
            ))
            self.api_base_edit.setMinimumHeight(25)
            self.api_base_edit.setMinimumWidth(base_width)
            main_layout.addWidget(self.api_base_edit)
            
            # Base URL 说明
            base_url_desc = QLabel(self.i18n.get('base_url_desc', 'The API endpoint URL. Use default unless you have a custom endpoint.'))
            base_url_desc.setObjectName(f'label_base_url_desc_{self.model_id}')
            base_url_desc.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 2px 0;")
            base_url_desc.setWordWrap(True)
            main_layout.addWidget(base_url_desc)
            
            # 模型下拉框
            self.model_combo = NoScrollComboBox(self)
            self.model_combo.setMinimumWidth(int(base_width * 0.7))
            self.model_combo.setEditable(False)
            self.model_combo.currentTextChanged.connect(self.on_model_combo_changed)
            
            # 添加占位符选项
            placeholder_text = self.i18n.get('select_model', '-- No Model --')
            self.model_combo.addItem(placeholder_text)
            # 标记占位符，便于语言切换时更新文本
            self.model_combo.setItemData(0, 'select_model')
            
            # 从缓存加载模型列表
            prefs = get_prefs()
            cached_models = prefs.get('cached_models', {})
            if self.model_id == 'perplexity':
                # Perplexity: hardcoded models (no reliable public model list endpoint)
                hardcoded_models = [
                    'sonar',
                    'sonar-pro',
                    'sonar-reasoning-pro',
                    'sonar-deep-research',
                ]
                self.model_combo.addItems(hardcoded_models)
                # Mark as loaded so the button becomes "Test Current Model"
                self._models_loaded = True
                # Default-select Sonar so user can test immediately (prefer saved model if valid)
                saved_model = (self.config.get('model') or '').strip()
                if saved_model and saved_model in hardcoded_models:
                    idx = self.model_combo.findText(saved_model)
                    self.model_combo.setCurrentIndex(idx if idx >= 1 else 1)
                else:
                    self.model_combo.setCurrentIndex(1)
            elif self.model_id in cached_models and cached_models[self.model_id]:
                self.model_combo.addItems(cached_models[self.model_id])
            else:
                # 没有缓存时，添加提示项
                hint_text = self.i18n.get('request_model_list', 'Please request model list')
                self.model_combo.addItem(hint_text)
                # 标记提示项，便于语言切换时更新文本
                self.model_combo.setItemData(1, 'request_model_list')
                # 禁用提示项
                model = self.model_combo.model()
                item = model.item(1)  # 第二项是提示项
                if item:
                    item.setEnabled(False)
            
            # 模型按钮区域（新行）
            model_buttons_layout = QHBoxLayout()
            model_buttons_layout.setSpacing(SPACING_SMALL)
            
            # 刷新模型列表按钮（Perplexity 不显示）
            self.refresh_models_button = QPushButton(self.i18n.get('refresh_model_list', 'Refresh Model List'), self)
            self.refresh_models_button.setObjectName(f'button_refresh_models_{self.model_id}')
            self.refresh_models_button.clicked.connect(self.on_refresh_models_clicked)
            apply_button_style(self.refresh_models_button, min_width=0)
            # Perplexity 模型列表是硬编码，不需要刷新按钮
            if self.model_id != 'perplexity':
                model_buttons_layout.addWidget(self.refresh_models_button, 1)  # 50% 宽度
            else:
                self.refresh_models_button.hide()
            
            # 测试当前模型按钮
            self.test_model_button = QPushButton(self.i18n.get('test_current_model', 'Test Current Model'), self)
            self.test_model_button.setObjectName(f'button_test_model_{self.model_id}')
            self.test_model_button.clicked.connect(self.on_test_model_clicked)
            apply_button_style(self.test_model_button, min_width=0)
            model_buttons_layout.addWidget(self.test_model_button, 1)  # 50% 宽度
            
            # 初始化加载动画（用于刷新按钮）
            from .ui_constants import ButtonLoadingAnimation
            self.refresh_models_animation = ButtonLoadingAnimation(
                button=self.refresh_models_button,
                loading_text=self.i18n.get('loading_models_text', 'Loading'),
                original_text=self.i18n.get('refresh_model_list', 'Refresh Model List')
            )
            
            # 测试按钮动画
            self.test_model_animation = ButtonLoadingAnimation(
                button=self.test_model_button,
                loading_text=self.i18n.get('testing_text', 'Testing'),
                original_text=self.i18n.get('test_current_model', 'Test Current Model')
            )
            
            # 兼容旧代码：保留 load_models_button 引用
            self.load_models_button = self.refresh_models_button
            self.load_models_animation = self.refresh_models_animation
            
            # 模型标签
            model_label = QLabel(self.i18n.get('model_label', 'Model'))
            model_label.setObjectName(f'label_model_{self.model_id}')
            main_layout.addWidget(model_label)
            
            # 模型下拉框
            main_layout.addWidget(self.model_combo)
            
            # 模型按钮区域
            main_layout.addLayout(model_buttons_layout)
            
            # 模型说明
            model_desc = QLabel(self.i18n.get('model_desc', 'Select a model from the list or use a custom model name.'))
            model_desc.setObjectName(f'label_model_desc_{self.model_id}')
            model_desc.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 2px 0;")
            model_desc.setWordWrap(True)
            main_layout.addWidget(model_desc)
            
            # 使用自定义模型名称选项
            self.use_custom_model_checkbox = QCheckBox(self.i18n.get('use_custom_model', 'Use custom model name'))
            self.use_custom_model_checkbox.setObjectName(f'checkbox_use_custom_model_{self.model_id}')
            self.use_custom_model_checkbox.stateChanged.connect(self.on_custom_model_toggled)
            main_layout.addWidget(self.use_custom_model_checkbox)
            
            # 自定义模型名称输入框（始终显示，初始禁用）
            self.custom_model_input = QLineEdit(self)
            self.custom_model_input.setMinimumWidth(base_width)
            self.custom_model_input.setMinimumHeight(25)
            self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))
            self.custom_model_input.textChanged.connect(self.on_config_changed)
            self.custom_model_input.setEnabled(False)
            main_layout.addWidget(self.custom_model_input)
            
            # 加载模型配置（填充下拉框或自定义输入）
            self.load_model_config()
            
            # 添加分隔线（高级区域）
            separator2 = QFrame()
            separator2.setFrameShape(QFrame.HLine)
            separator2.setFrameShadow(QFrame.Plain)
            separator2.setStyleSheet("border-top: 1px dashed palette(mid); margin-top: 15px; margin-bottom: 15px; background: none;")
            separator2.setMinimumHeight(10)
            main_layout.addWidget(separator2)
            
            # 高级区域标题
            advanced_label = QLabel(self.i18n.get('advanced_section', 'Advanced'))
            advanced_label.setObjectName(f'label_advanced_{self.model_id}')
            advanced_label.setStyleSheet("font-weight: bold;")
            main_layout.addWidget(advanced_label)
            
            # 流式传输选项
            self.enable_streaming_checkbox = QCheckBox(self.i18n.get('model_enable_streaming', 'Enable Streaming'))
            self.enable_streaming_checkbox.setObjectName(f'checkbox_enable_streaming_{self.model_id}')
            self.enable_streaming_checkbox.setChecked(self.config.get('enable_streaming', True))
            self.enable_streaming_checkbox.stateChanged.connect(self.on_config_changed)
            main_layout.addWidget(self.enable_streaming_checkbox)
            
            # 流式传输说明
            streaming_desc = QLabel(self.i18n.get('streaming_desc', 'Enable real-time response streaming for faster feedback.'))
            streaming_desc.setObjectName(f'label_streaming_desc_{self.model_id}')
            streaming_desc.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 2px 0;")
            streaming_desc.setWordWrap(True)
            main_layout.addWidget(streaming_desc)
            
            # 服务商特定提示（放在底部）
            if self.model_id == 'nvidia':
                notice_label = QLabel(self.i18n.get('nvidia_free_credits_notice', 
                    'Note: New users get free API credits - No credit card required.'))
                notice_label.setObjectName('label_nvidia_notice')
                notice_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 5px 0; font-style: italic;")
                notice_label.setWordWrap(True)
                main_layout.addWidget(notice_label)
            elif self.model_id == 'perplexity':
                notice_label = QLabel(self.i18n.get('perplexity_model_notice', 
                    'Note: Perplexity does not provide a public model list API, so models are hardcoded.'))
                notice_label.setObjectName('label_perplexity_notice')
                notice_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 5px 0; font-style: italic;")
                notice_label.setWordWrap(True)
                main_layout.addWidget(notice_label)
            elif self.model_id == 'ollama':
                notice_label = QLabel(self.i18n.get('ollama_no_api_key_notice', 
                    'Note: Ollama is a local model that does not require an API key.'))
                notice_label.setObjectName('label_ollama_notice')
                notice_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 5px 0; font-style: italic;")
                notice_label.setWordWrap(True)
                main_layout.addWidget(notice_label)
            
            # 设置按钮初始状态
            self.update_button_states()
            
            # 连接信号以更新按钮状态
            if self.api_key_edit is not None:
                self.api_key_edit.textChanged.connect(self.update_button_states)
            self.model_combo.currentTextChanged.connect(self.update_button_states)
    
    def update_button_states(self):
        """更新刷新和测试按钮的启用状态"""
        # 刷新按钮：需要 API Key（Ollama 和 nvidia_free 除外）
        if self.model_id in ['ollama', 'nvidia_free']:
            self.refresh_models_button.setEnabled(True)
        elif self.api_key_edit is not None:
            # QTextEdit 使用 toPlainText()，QLineEdit 使用 text()
            if hasattr(self.api_key_edit, 'toPlainText'):
                api_key = self.api_key_edit.toPlainText().strip()
            else:
                api_key = self.api_key_edit.text().strip()
            self.refresh_models_button.setEnabled(bool(api_key))
        else:
            self.refresh_models_button.setEnabled(False)
        
        # 测试按钮：需要选中有效模型
        current_model = self.model_combo.currentText()
        placeholder_text = self.i18n.get('select_model', '-- No Model --')
        hint_text = self.i18n.get('request_model_list', 'Please request model list')
        is_valid_model = bool(current_model and current_model not in [placeholder_text, hint_text])
        self.test_model_button.setEnabled(is_valid_model)
    
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
        elif self.model_id == 'perplexity':
            provider = AIProvider.AI_PERPLEXITY
            config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
            config['display_name'] = 'Perplexity'  # 设置固定的显示名称
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
        elif self.model_id == 'nvidia_free':
            provider = AIProvider.AI_NVIDIA_FREE
            # Nvidia 免费通道不需要用户提供 API Key
            config['api_key'] = 'free-tier'
            config['proxy_url'] = self.api_base_edit.text().strip() if hasattr(self, 'api_base_edit') else ''
            # 动态拼接翻译后的显示名称
            free_text = self.i18n.get('free', 'Free')
            config['display_name'] = f"Nvidia AI ({free_text})"
            config['provider_id'] = 'nvidia_free'
        
        # 通用配置项
        config['api_base_url'] = self.api_base_edit.text().strip() if hasattr(self, 'api_base_edit') else ''
        
        # 模型名称配置（新逻辑：支持下拉框或自定义输入）
        if hasattr(self, 'use_custom_model_checkbox') and self.use_custom_model_checkbox.isChecked():
            # 使用自定义模型名称
            config['use_custom_model_name'] = True
            config['model'] = self.custom_model_input.text().strip() if hasattr(self, 'custom_model_input') else ''
            logger.debug(
                f"[get_config] model_id={self.model_id} use_custom_model_name=True custom_model_input='{config['model']}'"
            )
        else:
            # 使用下拉框选中的模型
            config['use_custom_model_name'] = False
            if hasattr(self, 'model_combo'):
                current_text = self.model_combo.currentText().strip()
                # 过滤掉占位符文本，避免保存无效的模型名称
                if self._is_placeholder_text(current_text):
                    logger.debug(
                        f"[get_config] model_id={self.model_id} placeholder selected in combo, clearing model. combo_text='{current_text}'"
                    )
                    config['model'] = ''  # 占位符不保存
                else:
                    config['model'] = current_text
                logger.debug(
                    f"[get_config] model_id={self.model_id} use_custom_model_name=False saved_model='{config['model']}' combo_text='{current_text}'"
                )
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
        
        # 触发配置变更信号
        self.on_config_changed()
    
    def on_config_changed(self):
        """配置变更处理"""
        # 如果正在初始化，不发送信号
        if hasattr(self, '_is_initializing') and self._is_initializing:
            return
        self.config_changed.emit()
    
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
        elif self.model_id == 'perplexity':
            provider = AIProvider.AI_PERPLEXITY
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
    
    def on_refresh_models_clicked(self):
        """点击刷新模型列表按钮"""
        # 直接调用加载模型列表逻辑
        self._load_models_list()
    
    def on_test_model_clicked(self):
        """点击测试当前模型按钮"""
        self._test_current_model()
    
    def on_load_models_clicked(self):
        """点击加载模型按钮 - 根据状态执行加载或测试（兼容旧代码）"""
        import logging
        logger = logging.getLogger(__name__)

        # Perplexity: always test current model (no model list loading)
        if self.model_id == 'perplexity':
            self._test_current_model()
            return
        
        # 如果已加载模型，则执行测试
        if self._models_loaded:
            self._test_current_model()
            return
        
        # 否则执行加载模型列表
        self._load_models_list()
    
    def _load_models_list(self):
        """加载模型列表的内部方法"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 1. 验证 API Key（Ollama 和 nvidia_free 不需要）
        if self.model_id not in ['ollama', 'nvidia_free']:
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
        self.refresh_models_animation.start()
        
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
            self.refresh_models_animation.stop()
            
            if success:
                # 成功：填充下拉框
                models = result
                
                self.model_combo.clear()
                # 先添加占位符
                placeholder_text = self.i18n.get('select_model', '-- No Model --')
                self.model_combo.addItem(placeholder_text)
                self.model_combo.setItemData(0, 'select_model')
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
                
                # 标记模型已加载
                self._models_loaded = True
                
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
        
        # 启动测试动画
        self.test_model_animation.start()
        
        # 使用 QTimer 异步执行，避免阻塞 UI
        def test_model():
            # 创建 API 客户端
            from .api import APIClient
            api_client = APIClient(i18n=self.i18n)
            
            # 测试模型
            success, message = api_client.test_model(self.model_id, config, test_model_name=selected_model)
            
            # 停止测试动画
            self.test_model_animation.stop()
            
            if success:
                # 测试成功
                QMessageBox.information(
                    self,
                    self.i18n.get('success', 'Success'),
                    self.i18n.get('model_test_success', 'Model test successful!')
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
        
        # 检查是否是占位符
        is_placeholder = self._is_placeholder_text(text)
        
        if is_placeholder:
            logger.info(f"用户选择了占位符 '{text}'，清空模型选择并触发自动保存")
        else:
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
            before_text = ''
            try:
                before_text = self.custom_model_input.text()
            except Exception:
                before_text = ''
            current_text = self.model_combo.currentText()

            # 优先用 itemData 标记来判断是否占位符/提示项（避免语言切换后文本比对失败）
            try:
                current_index = self.model_combo.currentIndex()
                current_tag = self.model_combo.itemData(current_index)
            except Exception:
                current_index = -1
                current_tag = None

            is_placeholder = (current_tag in ('select_model', 'request_model_list'))
            if not is_placeholder:
                # 兼容旧数据：如果没有 tag，再回退到文本判断
                is_placeholder = self._is_placeholder_text(current_text)

            logger.warning(
                f"[on_custom_model_toggled] model_id={self.model_id} use_custom=True combo_index={current_index} combo_tag={current_tag} combo_text='{current_text}' is_placeholder={is_placeholder} custom_before='{before_text}'"
            )

            if is_placeholder:
                logger.info(f"[on_custom_model_toggled] 当前是占位符，不复制: {current_text}")
                # 关键：保持输入框为空，让 placeholder 生效
                if not self.custom_model_input.text().strip():
                    self.custom_model_input.clear()
            else:
                # 只有在用户还没输入自定义名称时，才自动带入当前选中的模型名
                if not self.custom_model_input.text().strip():
                    logger.info(f"[on_custom_model_toggled] 复制模型名称: {current_text}")
                    self.custom_model_input.setText(current_text)

            after_text = ''
            try:
                after_text = self.custom_model_input.text()
            except Exception:
                after_text = ''
            logger.warning(
                f"[on_custom_model_toggled] model_id={self.model_id} use_custom=True custom_after='{after_text}'"
            )
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
            # 避免把占位符文本当作真实模型名写入自定义输入框
            if model_name and not self._is_placeholder_text(model_name):
                self.custom_model_input.setText(model_name)
            else:
                self.custom_model_input.clear()
        else:
            # 尝试在下拉框中选中（如果列表已加载）
            logger.info(f"[load_model_config] 使用下拉框模式 - combo.count()={self.model_combo.count()}")
            if self.model_combo.count() > 1:  # 大于1表示有占位符+实际模型
                # Perplexity: if no saved model yet, default-select the first real model.
                # This avoids cross-platform signal timing differences where the earlier
                # setCurrentIndex(1) may be overwritten back to placeholder.
                if self.model_id == 'perplexity' and not (model_name or '').strip():
                    logger.info("[load_model_config] Perplexity 未保存模型，默认选中第一个模型")
                    self.model_combo.setCurrentIndex(1)
                    return

                index = self.model_combo.findText(model_name)
                logger.info(f"[load_model_config] 查找模型 '{model_name}' - index={index}")
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)
                else:
                    # 模型不在列表中，重置为占位符，并在自定义输入框显示
                    logger.info(f"[load_model_config] 模型不在列表中，重置为占位符")
                    self.model_combo.setCurrentIndex(0)
                    if model_name and not self._is_placeholder_text(model_name):
                        self.custom_model_input.setText(model_name)
                    else:
                        self.custom_model_input.clear()
            else:
                # 只有占位符（没有实际模型），重置为占位符
                logger.info(f"[load_model_config] 只有占位符，重置为占位符")
                self.model_combo.setCurrentIndex(0)
                if model_name and not self._is_placeholder_text(model_name):
                    self.custom_model_input.setText(model_name)
                else:
                    self.custom_model_input.clear()
        
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
        
        # 使用 objectName 映射更新 CheckBox
        checkbox_map = {
            f'checkbox_enable_streaming_{self.model_id}': ('model_enable_streaming', 'Enable Streaming'),
            f'checkbox_use_custom_model_{self.model_id}': ('use_custom_model', 'Use custom model name'),
        }
        
        for checkbox in self.findChildren(QCheckBox):
            obj_name = checkbox.objectName()
            if obj_name in checkbox_map:
                i18n_key, fallback = checkbox_map[obj_name]
                checkbox.setText(self.i18n.get(i18n_key, fallback))
        
        # 使用 objectName 映射更新 Button
        button_map = {
            f'button_load_models_{self.model_id}': ('load_models_list', 'Load Model List'),
        }
        
        for button in self.findChildren(QPushButton):
            obj_name = button.objectName()
            if obj_name in button_map:
                i18n_key, fallback = button_map[obj_name]
                button.setText(self.i18n.get(i18n_key, fallback))
        
        # 更新自定义模型输入框的placeholder
        if hasattr(self, 'custom_model_input'):
            self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))

        # 更新模型下拉框中的占位符/提示项文本（未配置/未加载模型时）
        # 通过 userData 标记来识别这些项，避免依赖旧语言的显示文本
        if hasattr(self, 'model_combo') and self.model_combo is not None:
            try:
                for idx in range(self.model_combo.count()):
                    tag = self.model_combo.itemData(idx)
                    if tag == 'select_model':
                        self.model_combo.setItemText(idx, self.i18n.get('select_model', '-- No Model --'))
                    elif tag == 'request_model_list':
                        self.model_combo.setItemText(idx, self.i18n.get('request_model_list', 'Please request model list'))
                        # 保持提示项不可选
                        model = self.model_combo.model()
                        item = model.item(idx)
                        if item:
                            item.setEnabled(False)
            except Exception:
                pass
        
        # 使用 objectName 映射更新 Label（完全移除硬编码文本检测）
        label_map = {
            'label_nvidia_free_info': ('nvidia_free_info', 'New users get 6 months free API access - No credit card required'),
            f'label_api_key_{self.model_id}': ('api_key_label', 'API Key'),
            f'label_base_url_{self.model_id}': ('base_url_label', 'Base URL'),
            f'label_model_{self.model_id}': ('model_label', 'Model'),
        }
        
        for label in self.findChildren(QLabel):
            obj_name = label.objectName()
            if obj_name in label_map:
                i18n_key, fallback = label_map[obj_name]
                label.setText(self.i18n.get(i18n_key, fallback))
        
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
            elif self.model_id == 'perplexity':
                from .models import PerplexityModel
                model_config = PerplexityModel
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
            'perplexity': AIProvider.AI_PERPLEXITY,
            'ollama': AIProvider.AI_OLLAMA,
            'nvidia_free': AIProvider.AI_NVIDIA_FREE,
        }
        
        provider = provider_map.get(self.model_id)
        if provider and provider in DEFAULT_MODELS:
            default_name = DEFAULT_MODELS[provider].display_name
            # 对于 nvidia_free，动态拼接翻译后的名称
            if self.model_id == 'nvidia_free':
                free_text = self.i18n.get('free', 'Free')
                return f"Nvidia AI ({free_text})"
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
        elif self.model_id == 'perplexity':
            provider = AIProvider.AI_PERPLEXITY
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
            self.model_combo.setItemData(0, 'select_model')
            hint_text = self.i18n.get('request_model_list', 'Please request model list')
            self.model_combo.addItem(hint_text)
            self.model_combo.setItemData(1, 'request_model_list')
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

            # 8.1 同步重置 prefs 中的模型配置为默认值（确保真正清空 API Key / 恢复默认 model）
            if 'models' in prefs:
                prefs_models = prefs.get('models', {}) or {}
                current = prefs_models.get(self.model_id, {}) or {}
                current['api_base_url'] = model_config.default_api_base_url
                current['model'] = model_config.default_model_name
                if self.model_id == 'grok':
                    current['auth_token'] = ''
                    if 'api_key' in current:
                        try:
                            del current['api_key']
                        except Exception:
                            pass
                elif self.model_id != 'ollama':
                    current['api_key'] = ''
                current['enable_streaming'] = True
                current['enabled'] = False

                # Reset provider-specific extra fields
                if self.model_id == 'openrouter':
                    current['http_referer'] = ''
                    current['x_title'] = 'Ask AI Plugin'
                if self.model_id == 'custom':
                    if 'disable_ssl_verify' in current:
                        current['disable_ssl_verify'] = False
                    if 'disable_ssl_verify_checkbox' in current:
                        current['disable_ssl_verify_checkbox'] = False
                prefs_models[self.model_id] = current
                prefs['models'] = prefs_models
                logger.info(f"已将 {self.model_id} 的 prefs 配置重置为默认值")

            # 8.2 Perplexity：恢复硬编码模型列表并默认选中 sonar
            if self.model_id == 'perplexity':
                try:
                    self.model_combo.clear()
                    self.model_combo.addItem(placeholder_text)
                    self.model_combo.setItemData(0, 'select_model')

                    for m in ['sonar', 'sonar-pro', 'sonar-reasoning-pro', 'sonar-deep-research']:
                        self.model_combo.addItem(m)
                        self.model_combo.setItemData(self.model_combo.count() - 1, m)

                    default_model = model_config.default_model_name
                    idx = self.model_combo.findText(default_model)
                    self.model_combo.setCurrentIndex(idx if idx >= 0 else 1)
                    logger.info(f"Perplexity 模型列表已恢复，默认选中: {default_model}")
                except Exception:
                    pass
            
            # 9. 通知父对话框更新模型列表的对钩标记
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
        AIModelFactory.register_model('perplexity', PerplexityModel)
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
        # 不设置最小宽度，让父窗口（TabDialog）控制整体尺寸
        self.setMinimumHeight(400)
        
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
        # 使用统一的Tab布局规范
        from .ui_constants import TAB_CONTENT_MARGIN, TAB_CONTENT_SPACING, get_tab_scroll_area_style
        content_layout.setSpacing(TAB_CONTENT_SPACING)
        content_layout.setContentsMargins(TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN)
        content_widget.setLayout(content_layout)
        
        # 1. 顶部：语言选择
        # Section Title（外部）- 第一个 section，顶部间距较小
        from .ui_constants import get_first_section_title_style
        lang_title = QLabel(self.i18n.get('language_settings', 'Language'))
        lang_title.setObjectName('title_language')
        lang_title.setStyleSheet(get_first_section_title_style())
        content_layout.addWidget(lang_title)
        
        # Subtitle（外部）
        lang_subtitle = QLabel(self.i18n.get('language_subtitle', 'Choose your preferred interface language'))
        lang_subtitle.setObjectName('subtitle_language')
        lang_subtitle.setWordWrap(True)
        lang_subtitle.setStyleSheet(get_subtitle_style())
        content_layout.addWidget(lang_subtitle)
        
        # GroupBox（无标题）
        lang_group = QGroupBox()
        lang_group.setObjectName('groupbox_display')
        lang_group.setStyleSheet(get_groupbox_style())
        lang_layout = QVBoxLayout()
        lang_layout.setSpacing(SPACING_SMALL)
        
        self.lang_combo = NoScrollComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(get_prefs()['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        language_label = QLabel(self.i18n.get('language_label', 'Language'))
        language_label.setObjectName('label_language')
        lang_layout.addWidget(language_label)
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        content_layout.addWidget(lang_group)

        # 2. 中部：AI模型选择和配置
        # Section Title（外部）
        ai_title = QLabel(self.i18n.get('ai_models', 'AI Providers'))
        ai_title.setObjectName('title_ai_providers')
        ai_title.setStyleSheet(get_section_title_style())
        content_layout.addWidget(ai_title)
        
        # Subtitle（外部）
        ai_subtitle = QLabel(self.i18n.get('ai_providers_subtitle', 'Configure AI providers and select your default AI'))
        ai_subtitle.setObjectName('subtitle_ai_providers')
        ai_subtitle.setWordWrap(True)
        ai_subtitle.setStyleSheet(get_subtitle_style())
        content_layout.addWidget(ai_subtitle)
        
        # GroupBox（无标题）
        model_group = QGroupBox()
        model_group.setObjectName('groupbox_ai_models')
        model_group.setStyleSheet(get_groupbox_style())
        model_layout = QVBoxLayout()
        model_layout.setSpacing(SPACING_MEDIUM)

        # ========== 新版 AI 区域：列表概览 + 管理入口 ==========
        
        # 空态提示（当没有已配置 AI 时显示）
        hint_text = self.i18n.get('no_configured_ai_hint', 
            'No AI configured. Plugin cannot work. Please click "Add AI" to add an AI provider.')
        self.no_ai_hint_label = QLabel(f"💡 {hint_text}")
        self.no_ai_hint_label.setObjectName('label_no_ai_hint')
        self.no_ai_hint_label.setWordWrap(True)
        self.no_ai_hint_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_COLOR_PRIMARY};
                padding: {PADDING_MEDIUM}px;
                background: {BG_COLOR_ALTERNATE};
                border-radius: {SPACING_TINY}px;
            }}
        """)
        self.no_ai_hint_label.setVisible(False)  # 默认隐藏，由 refresh_ai_list 控制
        model_layout.addWidget(self.no_ai_hint_label)
        
        # 默认 AI 选择行
        default_ai_layout = QHBoxLayout()
        default_ai_layout.setSpacing(SPACING_SMALL)
        
        default_ai_label = QLabel(self.i18n.get('default_ai_label', 'Default AI:'))
        default_ai_label.setObjectName('label_default_ai')
        default_ai_layout.addWidget(default_ai_label)
        
        # 默认 AI 下拉框（只显示已配置的 AI）
        self.model_combo = NoScrollComboBox()
        self.model_combo.setObjectName('combo_default_ai')
        self.model_combo.currentIndexChanged.connect(self.on_default_ai_changed)
        default_ai_layout.addWidget(self.model_combo)
        default_ai_layout.addStretch()
        
        model_layout.addLayout(default_ai_layout)
        
        # 已配置 AI 列表（简洁显示）
        from PyQt5.QtWidgets import QListWidget, QListWidgetItem
        from PyQt5.QtCore import QEvent
        self.configured_ai_list = QListWidget()
        self.configured_ai_list.setObjectName('list_configured_ai_summary')
        self.configured_ai_list.setMaximumHeight(120)
        self.configured_ai_list.setStyleSheet(get_list_widget_style())
        self.configured_ai_list.itemDoubleClicked.connect(self._on_ai_list_double_clicked)
        
        # 安装事件过滤器，实现鼠标滚动互斥
        self.configured_ai_list.viewport().installEventFilter(self)
        
        model_layout.addWidget(self.configured_ai_list)
        
        # AI 操作按钮区域
        ai_buttons_layout = QHBoxLayout()
        ai_buttons_layout.setSpacing(SPACING_SMALL)
        
        # 添加 AI 按钮（使用默认样式）
        self.add_ai_button = QPushButton(self.i18n.get('add_ai_button', 'Add AI'))
        self.add_ai_button.setObjectName('button_add_ai')
        self.add_ai_button.clicked.connect(self._on_add_ai_clicked)
        ai_buttons_layout.addWidget(self.add_ai_button)
        
        # 管理已配置 AI 按钮（使用默认样式）
        self.manage_ai_button = QPushButton(self.i18n.get('manage_configured_ai_button', 'Manage Configured AI'))
        self.manage_ai_button.setObjectName('button_manage_ai')
        self.manage_ai_button.clicked.connect(self._on_manage_ai_clicked)
        ai_buttons_layout.addWidget(self.manage_ai_button)
        
        ai_buttons_layout.addStretch()
        
        model_layout.addLayout(ai_buttons_layout)
        
        # 初始化 AI 列表显示
        self.refresh_ai_list()
        
        # 保留 model_widgets 字典用于兼容性（但不再在 General 中展开显示）
        self.model_widgets = {}
        self.models_layout = QVBoxLayout()  # 保留空布局用于兼容性
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Plain)
        separator.setStyleSheet(get_separator_style())
        model_layout.addWidget(separator)
        
        # 添加请求超时时间设置
        timeout_layout = QHBoxLayout()
        timeout_layout.setSpacing(SPACING_SMALL)
        timeout_label = QLabel(self.i18n.get('request_timeout_label', 'Request Timeout'))
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
        timeout_unit_label.setObjectName('label_timeout_unit')
        timeout_layout.addWidget(timeout_unit_label)
        timeout_layout.addStretch()
        
        model_layout.addLayout(timeout_layout)
        
        # 添加并行AI数量设置
        parallel_layout = QHBoxLayout()
        parallel_layout.setSpacing(SPACING_SMALL)
        parallel_label = QLabel(self.i18n.get('parallel_ai_count_label', 'Parallel AI Count'))
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
        from .ui_constants import TEXT_COLOR_SECONDARY_STRONG
        parallel_notice = QLabel(self.i18n.get('parallel_ai_notice', 
            'Each response window will have its own AI selector. Make sure you have configured enough AI providers.'))
        parallel_notice.setObjectName('label_parallel_ai_notice')
        parallel_notice.setWordWrap(True)
        parallel_notice.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: 5px 0; font-style: italic;")
        model_layout.addWidget(parallel_notice)
        
        model_group.setLayout(model_layout)
        content_layout.addWidget(model_group)
        
        # 3. Export Settings
        # Section Title（外部）
        export_title = QLabel(self.i18n.get('export_settings', 'Export Settings'))
        export_title.setObjectName('title_export_settings')
        export_title.setStyleSheet(get_section_title_style())
        content_layout.addWidget(export_title)
        
        # Subtitle（外部）
        export_subtitle = QLabel(self.i18n.get('export_settings_subtitle', 'Set default folder for exporting PDFs'))
        export_subtitle.setObjectName('subtitle_export_settings')
        export_subtitle.setWordWrap(True)
        export_subtitle.setStyleSheet(get_subtitle_style())
        content_layout.addWidget(export_subtitle)
        
        # GroupBox（无标题）
        export_group = QGroupBox()
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
        saved_folder = self.initial_values.get('default_export_folder', '').strip()
        self.export_folder_label = QLabel(
            saved_folder if saved_folder else self.i18n.get('no_folder_selected', 'No folder selected')
        )
        self.export_folder_label.setObjectName('label_export_folder')
        # 设置自定义属性标记是否显示的是占位符文本
        self.export_folder_label.setProperty('is_placeholder', not bool(saved_folder))
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
        content_layout.addWidget(export_group)
        
        # 5. Debug Logging Settings
        # Section Title（外部）
        debug_title = QLabel(self.i18n.get('debug_settings', 'Debug Settings'))
        debug_title.setObjectName('title_debug_settings')
        debug_title.setStyleSheet(get_section_title_style())
        content_layout.addWidget(debug_title)
        
        # Subtitle（外部）
        debug_subtitle = QLabel(self.i18n.get('debug_settings_subtitle', 'Enable debug logging for troubleshooting'))
        debug_subtitle.setObjectName('subtitle_debug_settings')
        debug_subtitle.setWordWrap(True)
        debug_subtitle.setStyleSheet(get_subtitle_style())
        content_layout.addWidget(debug_subtitle)
        
        # GroupBox（无标题）
        debug_group = QGroupBox()
        debug_group.setObjectName('groupbox_debug_settings')
        debug_group.setStyleSheet(get_groupbox_style())
        debug_layout = QVBoxLayout()
        debug_layout.setSpacing(SPACING_SMALL)
        
        # 复选框：启用调试日志
        self.enable_debug_logging_checkbox = QCheckBox(
            self.i18n.get('enable_debug_logging', 'Enable debug logging (ask_ai_plugin_debug.log)')
        )
        self.enable_debug_logging_checkbox.setObjectName('checkbox_enable_debug_logging')
        self.enable_debug_logging_checkbox.setChecked(
            self.initial_values.get('enable_debug_logging', False)
        )
        self.enable_debug_logging_checkbox.stateChanged.connect(self.on_config_changed)
        debug_layout.addWidget(self.enable_debug_logging_checkbox)
        
        # 说明文字
        debug_hint = QLabel(self.i18n.get('debug_logging_hint', 
            'When disabled, debug logs will not be written to file. This can prevent the log file from growing too large.'))
        debug_hint.setObjectName('label_debug_hint')
        debug_hint.setWordWrap(True)
        from .ui_constants import TEXT_COLOR_SECONDARY_STRONG
        debug_hint.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; font-style: italic; padding: 5px 0;")
        debug_layout.addWidget(debug_hint)
        
        debug_group.setLayout(debug_layout)
        content_layout.addWidget(debug_group)
        
        # 6. 危险区域：重置所有数据
        # Section Title（外部）
        reset_title = QLabel(self.i18n.get('reset_all_data', 'Reset All Data'))
        reset_title.setObjectName('title_reset_all_data')
        reset_title.setStyleSheet(get_section_title_style())
        content_layout.addWidget(reset_title)
        
        # Subtitle（外部，红色警告）
        reset_subtitle = QLabel(self.i18n.get('reset_all_data_subtitle', 
            'Warning: This will permanently delete all your settings and data'))
        reset_subtitle.setObjectName('subtitle_reset_all_data')
        reset_subtitle.setWordWrap(True)
        reset_subtitle.setStyleSheet("color: #dc3545; font-size: 1em; padding: 0; margin: 0 0 8px 0;")
        content_layout.addWidget(reset_subtitle)
        
        # GroupBox（无标题，无红色边框）
        reset_group = QGroupBox()
        reset_group.setObjectName('groupbox_reset_data')
        reset_group.setStyleSheet(get_groupbox_style())
        reset_layout = QVBoxLayout()
        reset_layout.setSpacing(SPACING_SMALL)
        
        # 重置按钮（使用默认样式）
        self.reset_button = QPushButton(self.i18n.get('reset_all_data', 'Reset All Data'))
        self.reset_button.setObjectName('button_reset_all_data')
        self.reset_button.clicked.connect(self.on_reset_all_data)
        reset_layout.addWidget(self.reset_button)
        
        reset_group.setLayout(reset_layout)
        content_layout.addWidget(reset_group)
        
        # 底部添加固定间距和弹性空间
        content_layout.addSpacing(SPACING_MEDIUM)
        content_layout.addStretch()
        
        # 将内容容器设置到主滚动区域
        main_scroll.setWidget(content_widget)
        
        # 添加主滚动区域到主布局
        main_layout.addWidget(main_scroll)

    def setup_model_widgets(self):
        """初始化所有模型配置控件（兼容性方法，现在为空操作）
        
        注意：模型配置控件现在在 AI Manager 弹窗中创建和管理，
        此方法保留用于兼容性，但不再执行任何操作。
        """
        # 确保 model_widgets 字典存在
        if not hasattr(self, 'model_widgets'):
            self.model_widgets = {}
    
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
    
    def refresh_ai_list(self):
        """刷新 AI 列表显示（已配置 AI 列表 + 默认 AI 下拉框）"""
        from PyQt5.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QLabel
        from PyQt5.QtCore import Qt
        
        prefs = get_prefs(force_reload=True)
        models_config = prefs.get('models', {})
        selected_model = prefs.get('selected_model', '')
        
        # AI Provider 显示顺序（用于排序）
        provider_order = ['openai', 'anthropic', 'gemini', 'grok', 'deepseek', 
                          'nvidia', 'perplexity', 'openrouter', 'ollama', 'custom']
        
        # 收集已配置的 AI（支持新的 config_id 格式：provider_uuid）
        configured_ais = []
        for config_id, config in models_config.items():
            if not config.get('is_configured', False):
                continue
            
            # 获取 provider_id（兼容旧数据）
            provider_id = config.get('provider_id', config_id.split('_')[0] if '_' in config_id else config_id)
            
            # 生成显示名称：Provider + Model
            # 对于 nvidia_free，动态生成翻译后的名称
            if provider_id == 'nvidia_free' or config_id == 'nvidia_free':
                free_text = self.i18n.get('free', 'Free')
                provider_name = f"Nvidia AI ({free_text})"
            else:
                provider_name = config.get('display_name', provider_id)
            
            model_name = config.get('model', '')
            if model_name:
                display_text = f"{provider_name} - {model_name}"
            else:
                display_text = provider_name
            
            # 排序键
            try:
                sort_key = provider_order.index(provider_id)
            except ValueError:
                sort_key = 999
            
            configured_ais.append((config_id, display_text, sort_key))
        
        # 按 provider 排序
        configured_ais.sort(key=lambda x: x[2])
        
        # 检查重复名称，添加序号
        name_counts = {}
        for i, (config_id, display_text, sort_key) in enumerate(configured_ais):
            if display_text in name_counts:
                name_counts[display_text] += 1
                new_display_text = f"{display_text} ({name_counts[display_text]})"
                configured_ais[i] = (config_id, new_display_text, sort_key)
            else:
                name_counts[display_text] = 1
        
        # 如果有重复，第一个也需要加序号
        for display_text, count in name_counts.items():
            if count > 1:
                for i, (config_id, text, sort_key) in enumerate(configured_ais):
                    if text == display_text:
                        configured_ais[i] = (config_id, f"{display_text} (1)", sort_key)
                        break
        
        # 更新空态提示
        has_configured = len(configured_ais) > 0
        self.no_ai_hint_label.setVisible(not has_configured)
        
        # 更新已配置 AI 列表（简洁显示，不使用自定义 widget）
        self.configured_ai_list.clear()
        for config_id, display_text, _ in configured_ais:
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, config_id)
            self.configured_ai_list.addItem(item)
        
        # 如果没有已配置 AI，显示提示
        if not has_configured:
            hint_item = QListWidgetItem(self.i18n.get('no_configured_ai', 'No AI configured yet'))
            hint_item.setData(Qt.UserRole, None)
            hint_item.setFlags(hint_item.flags() & ~Qt.ItemIsSelectable)
            hint_item.setForeground(Qt.gray)
            self.configured_ai_list.addItem(hint_item)
        
        # 更新管理按钮状态和文本
        self.manage_ai_button.setEnabled(has_configured)
        if not has_configured:
            self.manage_ai_button.setText(self.i18n.get('manage_configured_ai_button', 'Manage Configured AI'))
            self.manage_ai_button.setToolTip(self.i18n.get('manage_ai_disabled_tooltip', 'Please add an AI provider first.'))
        else:
            count = len(configured_ais)
            button_text = self.i18n.get('manage_configured_ai_button', 'Manage Configured AI') + f' ({count})'
            self.manage_ai_button.setText(button_text)
            self.manage_ai_button.setToolTip('')
        
        # 更新默认 AI 下拉框
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        
        if has_configured:
            for config_id, display_text, _ in configured_ais:
                self.model_combo.addItem(display_text, config_id)
            
            # 选中当前默认 AI
            index = self.model_combo.findData(selected_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
            elif self.model_combo.count() > 0:
                # 如果当前默认 AI 不在已配置列表中，选择第一个
                self.model_combo.setCurrentIndex(0)
        else:
            # 没有已配置 AI，添加占位符
            self.model_combo.addItem(self.i18n.get('no_configured_ai', 'No AI configured yet'), None)
        
        self.model_combo.blockSignals(False)
        self.model_combo.setEnabled(has_configured)
    
    def on_default_ai_changed(self, index):
        """当默认 AI 选择改变时"""
        if self._is_initializing:
            return
        
        model_id = self.model_combo.currentData()
        if model_id is None:
            return
        
        # 保存默认 AI 选择
        prefs = get_prefs()
        prefs['selected_model'] = model_id
        
        # 同步更新 panel_ai_selections 的第一个面板
        # 这样 Ask 对话框下次打开时会使用新的默认 AI
        panel_selections = prefs.get('panel_ai_selections', {}) or {}
        panel_selections['panel_0'] = model_id
        prefs['panel_ai_selections'] = panel_selections
        
        prefs.commit()
        
        # 更新 initial_values，避免 check_for_changes 仍然检测到变更
        if hasattr(self, 'initial_values'):
            self.initial_values['selected_model'] = model_id
        
        # 刷新列表以更新星标
        self.refresh_ai_list()
        
        logger.info(f"默认 AI 已自动保存: {model_id}")
    
    def eventFilter(self, obj, event):
        """事件过滤器：处理已配置AI列表的鼠标滚动事件"""
        from PyQt5.QtCore import QEvent
        
        # 只处理已配置AI列表的滚动事件
        if obj == self.configured_ai_list.viewport() and event.type() == QEvent.Wheel:
            # 获取列表的滚动条
            scrollbar = self.configured_ai_list.verticalScrollBar()
            
            # 检查是否需要滚动（内容超出可见区域）
            if scrollbar.maximum() > 0:
                # 获取滚动增量
                delta = event.angleDelta().y()
                
                # 检查是否到达边界
                at_top = scrollbar.value() == scrollbar.minimum()
                at_bottom = scrollbar.value() == scrollbar.maximum()
                
                # 如果在边界且继续向边界方向滚动，则传递给父控件
                if (at_top and delta > 0) or (at_bottom and delta < 0):
                    return False  # 不拦截，让父控件处理
                
                # 否则拦截事件，只在列表内滚动，不传递给父控件
                # 手动处理滚动
                scrollbar.setValue(scrollbar.value() - delta // 8)
                return True  # 拦截事件，不传递给父控件
            else:
                # 列表内容未超出，不需要滚动，让父控件处理
                return False
        
        # 其他事件正常传递
        return super(ConfigDialog, self).eventFilter(obj, event)
    
    def _on_ai_list_double_clicked(self, item):
        """双击 AI 列表项时打开管理弹窗"""
        model_id = item.data(Qt.UserRole)
        if model_id is None:
            return
        self._on_manage_ai_clicked()
    
    def _on_add_ai_clicked(self):
        """点击添加 AI 按钮时打开弹窗"""
        from .ai_manager_dialog import AddAIDialog
        
        dialog = AddAIDialog(self)
        dialog.config_changed.connect(self._on_ai_manager_config_changed)
        
        # 连接语言切换信号
        if hasattr(self, 'language_changed'):
            self.language_changed.connect(lambda lang: self._update_dialog_language(dialog, lang))
        
        dialog.exec_()
    
    def _on_manage_ai_clicked(self):
        """点击管理 AI 按钮时打开弹窗"""
        from .ai_manager_dialog import ManageAIDialog
        
        dialog = ManageAIDialog(self)
        dialog.config_changed.connect(self._on_ai_manager_config_changed)
        
        # 连接语言切换信号
        if hasattr(self, 'language_changed'):
            self.language_changed.connect(lambda lang: self._update_dialog_language(dialog, lang))
        
        dialog.exec_()
    
    def _update_dialog_language(self, dialog, lang_code):
        """更新弹窗的语言"""
        from .i18n import get_translation
        
        # 更新弹窗的 i18n
        dialog.i18n = get_translation(lang_code)
        
        # 调用弹窗的 retranslate_ui 方法
        if hasattr(dialog, 'retranslate_ui'):
            dialog.retranslate_ui()
    
    def _on_ai_manager_config_changed(self):
        """AI Manager 配置变更时的回调"""
        # 重新加载配置
        self.load_initial_values()
        
        # 更新 UI
        self.refresh_ai_list()
        self.update_model_name_display()
    
    def on_model_changed(self, index):
        """当选择的模型改变时（兼容性方法，现在直接调用 on_default_ai_changed）"""
        self.on_default_ai_changed(index)
    
    def update_model_names(self):
        """更新模型列表显示（包括对钩标记）- 别名方法"""
        self.update_model_name_display()
    
    def update_model_name_display(self):
        """更新模型下拉框中的模型名称显示（兼容性方法，现在调用 refresh_ai_list）"""
        self.refresh_ai_list()
    
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
            'request_timeout': prefs.get('request_timeout', 60),
            'parallel_ai_count': prefs.get('parallel_ai_count', 1),
            'enable_default_export_folder': prefs.get('enable_default_export_folder', False),
            'default_export_folder': prefs.get('default_export_folder', ''),
            'enable_debug_logging': prefs.get('enable_debug_logging', False)
        }
        
        # 调试日志
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[Export Config] 加载导出配置 - enable_default_export_folder: {self.initial_values.get('enable_default_export_folder')}, default_export_folder: {self.initial_values.get('default_export_folder')}")
        
        
        # 设置当前语言
        current_index = self.lang_combo.findData(self.initial_values['language'])
        if current_index >= 0:
            self.lang_combo.setCurrentIndex(current_index)
        
        # 更新模型名称显示
        self.update_model_name_display()
        
        # 设置当前模型
        model_index = self.model_combo.findData(self.initial_values['selected_model'])
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        
        # 设置导出配置
        if hasattr(self, 'enable_default_folder_checkbox'):
            enable_export = self.initial_values.get('enable_default_export_folder', False)
            self.enable_default_folder_checkbox.setChecked(enable_export)
            logger.info(f"[Export Config] 设置checkbox状态: {enable_export}")
        
        if hasattr(self, 'export_folder_label'):
            saved_folder = self.initial_values.get('default_export_folder', '').strip()
            if saved_folder:
                self.export_folder_label.setText(saved_folder)
                # 设置为非占位符
                self.export_folder_label.setProperty('is_placeholder', False)
                logger.info(f"[Export Config] 设置文件夹路径: {saved_folder}")
            else:
                no_folder_text = self.i18n.get('no_folder_selected', 'No folder selected')
                self.export_folder_label.setText(no_folder_text)
                # 设置为占位符
                self.export_folder_label.setProperty('is_placeholder', True)
                logger.info(f"[Export Config] 未设置文件夹，显示: {no_folder_text}")
        
        if hasattr(self, 'browse_folder_button'):
            button_enabled = self.initial_values.get('enable_default_export_folder', False)
            self.browse_folder_button.setEnabled(button_enabled)
            logger.info(f"[Export Config] 设置浏览按钮状态: {button_enabled}")
            
    def on_language_changed(self, index):
        """语言改变时的处理函数"""
        lang_code = self.lang_combo.currentData()
        
        # 记录日志
        import logging
        logger = logging.getLogger(__name__)
        
        # 立即保存语言设置到全局配置
        prefs['language'] = lang_code
        prefs['language_user_set'] = True
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
        
        # 更新 Export 配置区域的占位符文字（特殊处理）
        # 注意：checkbox 和 button 已在 retranslate_ui() 中通过 objectName 映射更新
        if hasattr(self, 'export_folder_label'):
            # 使用自定义属性检测是否显示的是占位符文本
            is_placeholder = self.export_folder_label.property('is_placeholder')
            if is_placeholder:
                # 如果是占位符，更新为新语言的占位符文本
                self.export_folder_label.setText(
                    self.i18n.get('no_folder_selected', 'No folder selected')
                )
                    
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
        
        # GroupBox 标题已移到外部作为独立的 QLabel，不再需要更新 GroupBox 的 title
        # 确保所有 GroupBox 的标题为空
        for group_box in self.findChildren(QGroupBox):
            if group_box.title():  # 如果有标题，清空它
                group_box.setTitle('')
        
        # 更新所有标签文本（使用ObjectName，语言无关）
        label_map = {
            # Section titles
            'title_language': ('language_settings', 'Language'),
            'title_ai_providers': ('ai_models', 'AI Providers'),
            'title_prompts': ('prompt_template', 'Prompts'),
            'title_export_settings': ('export_settings', 'Export Settings'),
            'title_debug_settings': ('debug_settings', 'Debug Settings'),
            'title_reset_all_data': ('reset_all_data', 'Reset All Data'),
            # Section subtitles
            'subtitle_language': ('language_subtitle', 'Choose your preferred interface language'),
            'subtitle_ai_providers': ('ai_providers_subtitle', 'Configure AI providers and select your default AI'),
            'subtitle_prompts': ('prompts_subtitle', 'Customize how questions are sent to AI'),
            'subtitle_export_settings': ('export_settings_subtitle', 'Set default folder for exporting PDFs'),
            'subtitle_debug_settings': ('debug_settings_subtitle', 'Enable debug logging for troubleshooting'),
            'subtitle_reset_all_data': ('reset_all_data_subtitle', 'Warning: This will permanently delete all your settings and data'),
            # Other labels
            'label_language': ('language_label', 'Language'),
            'label_current_ai': ('current_ai', 'Current AI'),
            'label_request_timeout': ('request_timeout_label', 'Request Timeout'),
            'label_timeout_unit': ('seconds', 'seconds'),
            'label_parallel_ai_count': ('parallel_ai_count_label', 'Parallel AI Count'),
            'label_parallel_ai_notice': ('parallel_ai_notice', 'Each response window will have its own AI selector. Make sure you have configured enough AI providers.'),
            'label_ask_prompts': ('ask_prompts', 'Ask Prompts'),
            'label_random_questions_prompts': ('random_questions_prompts', 'Random Questions Prompts'),
            'label_multi_book_template': ('multi_book_template_label', 'Multi-Book Prompt Template'),
            'label_multi_book_placeholder_hint': ('multi_book_placeholder_hint', 'Use {books_metadata} for book information, {query} for user question'),
            'label_debug_hint': ('debug_logging_hint', 'When disabled, debug logs will not be written to file. This can prevent the log file from growing too large.'),
            'label_nvidia_free_info': ('nvidia_free_info', 'New users get 6 months free API access - No credit card required'),
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
        
        # 更新 CheckBox 文本（使用 ObjectName 映射）
        checkbox_map = {
            'checkbox_enable_default_folder': ('enable_default_export_folder', 'Export to default folder'),
            'checkbox_enable_debug_logging': ('enable_debug_logging', 'Enable debug logging (ask_ai_plugin_debug.log)'),
        }
        
        for checkbox in self.findChildren(QCheckBox):
            obj_name = checkbox.objectName()
            if obj_name in checkbox_map:
                i18n_key, fallback = checkbox_map[obj_name]
                checkbox.setText(self.i18n.get(i18n_key, fallback))
                logger.debug(f"更新了复选框 [{obj_name}]: {checkbox.text()}")
        
        # 更新所有按钮文本（使用ObjectName映射，避免硬编码文本检测）
        button_map = {
            'button_browse_folder': ('browse_folder', 'Browse...'),
            'button_reset_all_data': ('reset_all_data', 'Reset All Data'),
            'button_add_ai': ('add_ai_button', 'Add AI'),
            'button_manage_ai': ('manage_configured_ai_button', 'Manage Configured AI'),
        }
        
        for button in self.findChildren(QPushButton):
            obj_name = button.objectName()
            
            # 优先使用 objectName 映射
            if obj_name in button_map:
                i18n_key, fallback = button_map[obj_name]
                button.setText(self.i18n.get(i18n_key, fallback))
                logger.debug(f"更新了按钮 [{obj_name}]: {button.text()}")
            # Reset AI 按钮的特殊处理
            elif obj_name and 'reset' in obj_name.lower() and 'all' not in obj_name.lower():
                reset_text = self.i18n.get('reset_current_ai', 'Reset Current AI to Default')
                reset_tooltip = self.i18n.get('reset_tooltip', 'Reset current AI to default values')
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
            # 通过属性识别 Reset 按钮
            elif button.property('isResetButton'):
                reset_text = self.i18n.get('reset_current_ai', 'Reset Current AI to Default')
                reset_tooltip = self.i18n.get('reset_tooltip', 'Reset current AI to default values')
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
        
        # 更新管理AI按钮的文本（需要包含数量）
        if hasattr(self, 'manage_ai_button'):
            # 获取已配置AI的数量
            prefs = get_prefs()
            models_config = prefs.get('models', {})
            configured_count = sum(1 for config in models_config.values() if config.get('is_configured', False))
            
            if configured_count > 0:
                button_text = self.i18n.get('manage_configured_ai_button', 'Manage Configured AI') + f' ({configured_count})'
                self.manage_ai_button.setText(button_text)
            else:
                self.manage_ai_button.setText(self.i18n.get('manage_configured_ai_button', 'Manage Configured AI'))
        
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
                # 获取 provider_id（用于判断模型类型）
                provider_id = config.get('provider_id')
                if not provider_id:
                    provider_id = model_id.split('_')[0] if '_' in model_id else model_id
                
                # 检查是否有API Key（Ollama和Custom不需要）
                has_key = False
                if provider_id in ['ollama', 'custom']:
                    has_key = True
                elif provider_id == 'grok':
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
        # 如果正在初始化，不处理
        if self._is_initializing:
            return
        
        import logging
        logger = logging.getLogger(__name__)
        
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
                    logger.info(f"[Parallel AI] 面板 {panel_index} 切换AI为: {ai_id}")
        
        prefs['panel_ai_selections'] = selections
        
        # 立即保存配置
        logger.info(f"[Parallel AI] 面板AI选择器变更，立即保存配置")
        self.save_settings()
        logger.info(f"[Parallel AI] 配置已自动保存")
    
    def save_settings(self):
        """保存设置"""
        import logging
        logger = logging.getLogger(__name__)
        
        prefs = get_prefs()
        
        # 保存语言设置
        prefs['language'] = self.lang_combo.currentData()
        
        # 注意：提示词模板现在在 Prompts Tab 中管理，不在 General Tab 中保存
        
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
            logger.info(f"[Export Config Save] checkbox状态: {self.enable_default_folder_checkbox.isChecked()}")
        if hasattr(self, 'export_folder_label'):
            # 使用 is_placeholder 属性判断，而不是比较文本
            # 这样可以避免在切换语言时因为占位符文本变化导致的判断错误
            is_placeholder = self.export_folder_label.property('is_placeholder')
            folder_text = self.export_folder_label.text()
            logger.info(f"[Export Config Save] is_placeholder={is_placeholder}, folder_text={folder_text}")
            if not is_placeholder:
                # 不是占位符，保存实际路径
                prefs['default_export_folder'] = folder_text
                logger.info(f"[Export Config Save] 保存实际路径: {folder_text}")
            else:
                # 是占位符，保存空字符串
                prefs['default_export_folder'] = ''
                logger.info(f"[Export Config Save] 保存空字符串（占位符）")
        
        # 保存Debug Logging配置
        if hasattr(self, 'enable_debug_logging_checkbox'):
            prefs['enable_debug_logging'] = self.enable_debug_logging_checkbox.isChecked()
            logger.info(f"[Debug Logging] 保存调试日志设置: {self.enable_debug_logging_checkbox.isChecked()}")
        
        # 保存选中的模型（只有当 model_combo 有有效数据时才保存）
        selected_model = self.model_combo.currentData()
        if selected_model is not None:
            prefs['selected_model'] = selected_model
        
        # 注意：模型配置现在在 AI Manager 弹窗中保存，不在这里处理
        # model_widgets 字典在新版中为空，保留此注释说明变更
        
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
            'request_timeout': prefs.get('request_timeout', 60),
            'parallel_ai_count': prefs.get('parallel_ai_count', 1),
            'enable_default_export_folder': prefs.get('enable_default_export_folder', False),
            'default_export_folder': prefs.get('default_export_folder', ''),
            'enable_debug_logging': prefs.get('enable_debug_logging', False)
        }
        
        # 注意：提示词模板的原始文本值现在在 Prompts Tab 中管理
        
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
        
        # 注意：提示词模板检查已移至 Prompts Tab
        
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
        return general_changed or models_changed or timeout_changed or parallel_ai_changed
    
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
        
        # 注意：提示词模板重置已移至 Prompts Tab
        
        # 重置选中的模型
        model_index = self.model_combo.findData(self.initial_values['selected_model'])
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        
        # 更新模型名称显示（会调用 refresh_ai_list）
        self.update_model_name_display()
        
        # 注意：模型配置现在在 AI Manager 弹窗中处理，不再调用 setup_model_widgets
        
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
        # 使用自定义属性检测是否为占位符
        is_placeholder = self.export_folder_label.property('is_placeholder')
        if is_placeholder:
            current_folder = ''  # 空路径，让对话框使用默认行为
        
        # 打开文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(
            self,
            self.i18n.get('select_export_folder', 'Select Export Folder'),
            current_folder,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if folder:
            # 更新标签显示
            self.export_folder_label.setText(folder)
            # 标记为非占位符（显示的是实际路径）
            self.export_folder_label.setProperty('is_placeholder', False)
            
            # 自动保存配置
            self.save_settings()
    
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
                from calibre.utils.config import JSONConfig, config_dir
                import os
                
                # 获取配置文件路径（使用Calibre的config_dir确保跨平台兼容）
                plugins_dir = os.path.join(config_dir, 'plugins')
                config_file = os.path.join(plugins_dir, 'ask_ai_plugin.json')
                
                if os.path.exists(config_file):
                    os.remove(config_file)
                    logger.info(f"已删除配置文件: {config_file}")
                
                # 2. 删除历史记录文件
                # 删除v2版本的历史记录JSON文件
                history_v2_path = os.path.join(plugins_dir, 'ask_ai_plugin_history_v2.json')
                if os.path.exists(history_v2_path):
                    os.remove(history_v2_path)
                    logger.info(f"已删除历史记录文件(v2): {history_v2_path}")
                
                # 删除旧版本的历史记录数据库（如果存在）
                history_db_path = os.path.join(plugins_dir, 'ask_ai_plugin_history.db')
                if os.path.exists(history_db_path):
                    os.remove(history_db_path)
                    logger.info(f"已删除历史记录数据库(旧版): {history_db_path}")
                
                # 3. 删除日志文件（需要先关闭所有日志处理器）
                log_dir = os.path.join(plugins_dir, 'ask_ai_plugin_logs')
                if os.path.exists(log_dir):
                    # 关闭所有日志处理器以释放文件句柄（Windows需要）
                    root_logger = logging.getLogger()
                    handlers_to_remove = []
                    for handler in root_logger.handlers[:]:  # 使用切片创建副本以避免迭代时修改
                        if isinstance(handler, logging.FileHandler):
                            # 检查是否是插件的日志文件
                            if 'ask_ai_plugin_logs' in handler.baseFilename:
                                handler.close()
                                handlers_to_remove.append(handler)
                    
                    # 移除已关闭的处理器
                    for handler in handlers_to_remove:
                        root_logger.removeHandler(handler)
                    
                    logger.info(f"已关闭 {len(handlers_to_remove)} 个日志处理器")
                    
                    # 现在可以安全删除日志目录
                    import shutil
                    import time
                    # 在Windows上，可能需要短暂延迟以确保文件句柄完全释放
                    time.sleep(0.1)
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
                
                # 6. 清除 Ask 弹窗的 AI 选择记忆和窗口尺寸记忆
                # 确保这些键被明确删除，而不是依赖配置文件删除
                keys_to_clear = ['panel_ai_selections', 'ask_dialog_width', 'ask_dialog_height']
                for key in keys_to_clear:
                    if key in prefs:
                        del prefs[key]
                        logger.info(f"已清除配置键: {key}")
                
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


class LibraryWidget(QWidget):
    """图书馆对话功能配置界面（MVP极简版）"""
    config_changed = pyqtSignal()
    
    def __init__(self, parent=None, gui=None):
        QWidget.__init__(self, parent)
        self.gui = gui
        self.prefs = get_prefs()
        
        # 获取当前语言的翻译
        language = self.prefs.get('language', 'en')
        self.i18n = get_translation(language)
        
        self.setup_ui()
        self.load_values()
    
    def setup_ui(self):
        """设置UI"""
        from .ui_constants import (setup_tab_widget_layout, TAB_CONTENT_MARGIN, 
                                   TAB_CONTENT_SPACING, get_first_section_title_style)
        
        # 使用统一的 Tab 布局
        main_layout = setup_tab_widget_layout(self)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # 内容容器
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, 
                                  TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN)
        layout.setSpacing(TAB_CONTENT_SPACING)
        
        # Privacy alert section - 使用统一的第一个 section 标题样式
        self.privacy_title = QLabel(self.i18n.get('ai_search_privacy_title', 'Privacy Notice'))
        self.privacy_title.setStyleSheet(get_first_section_title_style())
        layout.addWidget(self.privacy_title)
        
        self.privacy_alert = QLabel(self.i18n.get('ai_search_privacy_alert', 
            'AI Search uses book metadata (titles and authors) from your library. '
            'This information will be sent to the AI provider you have configured to process your search queries.'))
        self.privacy_alert.setWordWrap(True)
        self.privacy_alert.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: {PADDING_MEDIUM}px; background-color: palette(alternate-base); border-left: 3px solid palette(mid);")
        layout.addWidget(self.privacy_alert)
        
        layout.addSpacing(SPACING_MEDIUM)
        
        # AI搜索说明
        self.info_label = QLabel(self.i18n.get('library_info', 
            'AI Search is always enabled. When you don\'t select any books, '
            'you can search your entire library using natural language.'))
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: {PADDING_MEDIUM}px;")
        layout.addWidget(self.info_label)
        
        layout.addSpacing(SPACING_SMALL)
        
        # 更新按钮
        self.update_button = QPushButton(self.i18n.get('library_update', 'Update Library Data'))
        self.update_button.setToolTip(self.i18n.get('library_update_tooltip', 
            'Extract book titles and authors from your library'))
        self.update_button.clicked.connect(self.on_update_library)
        apply_button_style(self.update_button)
        layout.addWidget(self.update_button)
        
        layout.addSpacing(SPACING_SMALL)
        
        # 状态标签
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY_STRONG}; padding: {PADDING_MEDIUM}px;")
        layout.addWidget(self.status_label)
        
        # 添加弹性空间
        layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def load_values(self):
        """加载配置值"""
        # AI搜索现在始终启用，确保配置为True
        self.prefs['library_chat_enabled'] = True
        
        # 更新状态显示
        self.update_status_display()
    
    def retranslate_ui(self):
        """更新界面语言"""
        # 重新获取当前语言的翻译
        language = self.prefs.get('language', 'en')
        self.i18n = get_translation(language)
        
        # 更新所有文本 - 使用实例变量直接更新
        if hasattr(self, 'privacy_title'):
            self.privacy_title.setText(self.i18n.get('ai_search_privacy_title', 'Privacy Notice'))
        
        if hasattr(self, 'privacy_alert'):
            self.privacy_alert.setText(self.i18n.get('ai_search_privacy_alert', 
                'AI Search uses book metadata (titles and authors) from your library. '
                'This information will be sent to the AI provider you have configured to process your search queries.'))
        
        if hasattr(self, 'info_label'):
            self.info_label.setText(self.i18n.get('library_info', 
                'AI Search is always enabled. When you don\'t select any books, '
                'you can search your entire library using natural language.'))
        
        # 更新按钮文本
        if hasattr(self, 'update_button'):
            self.update_button.setText(self.i18n.get('library_update', 'Update Library Data'))
            self.update_button.setToolTip(self.i18n.get('library_update_tooltip', 
                'Extract book titles and authors from your library'))
        
        # 更新状态显示
        self.update_status_display()
    
    def update_status_display(self):
        """更新状态显示"""
        from .utils import get_library_metadata, get_library_last_update
        import json
        
        metadata = get_library_metadata(self.prefs)
        last_update = get_library_last_update(self.prefs)
        
        if metadata and last_update:
            try:
                books = json.loads(metadata)
                book_count = len(books)
                
                # 格式化时间显示
                from datetime import datetime
                update_time = datetime.fromisoformat(last_update)
                time_str = update_time.strftime('%Y-%m-%d %H:%M:%S')
                
                status_text = self.i18n.get('library_status', 
                    'Status: {count} books, last update: {time}').format(
                    count=book_count, time=time_str)
            except Exception as e:
                logger.error(f"Failed to parse library metadata: {e}")
                status_text = self.i18n.get('library_status_error', 'Status: Error loading data')
        else:
            status_text = self.i18n.get('library_status_empty', 
                'Status: No data. Click "Update Library Data" to start.')
        
        self.status_label.setText(status_text)
    
    def on_update_library(self):
        """更新图书馆数据"""
        if not self.gui:
            QMessageBox.warning(self, 
                self.i18n.get('error', 'Error'),
                self.i18n.get('library_no_gui', 'GUI not available'))
            return
        
        from .utils import update_library_metadata
        
        # 显示处理中提示
        self.update_button.setEnabled(False)
        self.update_button.setText(self.i18n.get('library_updating', 'Updating...'))
        QApplication.processEvents()
        
        try:
            # 提取元数据
            db = self.gui.current_db
            success, book_count, error_msg = update_library_metadata(db, self.prefs)
            
            if success:
                # 更新状态显示
                self.update_status_display()
                
                # 显示成功消息
                QMessageBox.information(self,
                    self.i18n.get('success', 'Success'),
                    self.i18n.get('library_update_success', 
                        'Successfully updated {count} books').format(count=book_count))
            else:
                QMessageBox.warning(self,
                    self.i18n.get('error', 'Error'),
                    error_msg or self.i18n.get('library_update_failed', 'Failed to update library data'))
        
        finally:
            # 恢复按钮状态
            self.update_button.setEnabled(True)
            self.update_button.setText(self.i18n.get('library_update', 'Update Library Data'))
    
    
    def save_settings(self):
        """保存设置"""
        # AI搜索始终启用
        self.prefs['library_chat_enabled'] = True
        logger.info("AI Search is always enabled")
    
    def has_changes(self):
        """检查是否有未保存的更改"""
        # AI搜索没有可配置项，始终返回False
        return False
