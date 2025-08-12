#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import logging
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, 
                            QPushButton, QHBoxLayout, QFormLayout, QGroupBox, QScrollArea, QSizePolicy,
                            QFrame, QCheckBox)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFontMetrics
from .models.grok import GrokModel
from .models.gemini import GeminiModel
from .models.deepseek import DeepseekModel
from .models.custom import CustomModel
from calibre.utils.config import JSONConfig

from .i18n import get_default_template, get_translation, get_suggestion_template, get_all_languages
from .models.base import AIProvider, ModelConfig, DEFAULT_MODELS, AIModelFactory, BaseAIModel
from .utils import mask_api_key, mask_api_key_in_text, safe_log_config

# 初始化日志
logger = logging.getLogger(__name__)

# 创建配置对象
prefs = JSONConfig('plugins/ask_grok')

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
    }
}
prefs.defaults['template'] = get_default_template('en')
prefs.defaults['language'] = 'en'
prefs.defaults['ask_dialog_width'] = 600
prefs.defaults['ask_dialog_height'] = 400
prefs.defaults['random_questions'] = {}

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
        self.setup_ui()
    
    def setup_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建表单布局
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)
        main_layout.addLayout(layout)
        
        # 计算基础宽度
        font_metrics = QFontMetrics(self.font())
        base_width = font_metrics.width('X' * 40)  # 基于40个字符的宽度
        
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
        
        if model_config:
            # API Key/Token 输入框
            self.api_key_edit = QTextEdit(self)
            self.api_key_edit.setPlainText(self.config.get(api_key_field_name, ''))
            self.api_key_edit.textChanged.connect(self.on_config_changed)
            self.api_key_edit.setMaximumHeight(62)
            self.api_key_edit.setMinimumWidth(base_width)  # 基于字体大小设置宽度
            layout.addRow(self.i18n.get('api_key_label', 'API Key:'), self.api_key_edit)
            
            # 添加分隔线
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Plain)
            separator.setStyleSheet("border-top: 1px dashed #aaaaaa; margin-top: 15px; margin-bottom: 15px; background: none;")
            separator.setMinimumHeight(10)
            main_layout.addWidget(separator)
            
            # 创建一个新的表单布局用于模型参数
            model_layout = QFormLayout()
            model_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
            model_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
            model_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
            model_layout.setHorizontalSpacing(15)
            model_layout.setVerticalSpacing(10)
            main_layout.addLayout(model_layout)
            
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
            
            # 模型名称输入框
            self.model_edit = QLineEdit(self)
            self.model_edit.setText(self.config.get('model', model_config.default_model_name))
            self.model_edit.textChanged.connect(self.on_config_changed)
            self.model_edit.setMinimumHeight(25)  # 设置最小高度
            self.model_edit.setMinimumWidth(base_width)  # 设置最小宽度
            model_layout.addRow(self.i18n.get('model_label', 'Model:'), self.model_edit)

            # 流式传输选项
            self.enable_streaming_checkbox = QCheckBox(self.i18n.get('model_enable_streaming', 'Enable Streaming'))
            self.enable_streaming_checkbox.setChecked(self.config.get('enable_streaming', True))
            self.enable_streaming_checkbox.stateChanged.connect(self.on_config_changed)
            model_layout.addRow("", self.enable_streaming_checkbox)
            
            # Custom模型特有选项
            if self.model_id == 'custom':
                # 禁用SSL验证选项
                self.disable_ssl_verify_checkbox = QCheckBox(self.i18n.get('model_disable_ssl_verify', 'Disable SSL Verify'))
                self.disable_ssl_verify_checkbox.setChecked(self.config.get('disable_ssl_verify', False))
                self.disable_ssl_verify_checkbox.stateChanged.connect(self.on_config_changed)

                model_layout.addRow("", self.disable_ssl_verify_checkbox)
            
            # 添加重置按钮
            reset_button = QPushButton(self.i18n.get('reset_button', 'Reset to Default'))
            reset_button.setObjectName(f"reset_button_{self.model_id}")  # 设置明确的objectName
            reset_button.setProperty('isResetButton', True)  # 添加属性标记
            reset_button.clicked.connect(self.reset_model_params)
            
            # 使用QDialogButtonBox来保持与关闭按钮一致的样式
            button_box = QHBoxLayout()
            button_box.addWidget(reset_button)
            button_box.addStretch()  # 添加弹性空间，使按钮靠左
            main_layout.addLayout(button_box)
    
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
        
        # 通用配置项
        config['api_base_url'] = self.api_base_edit.text().strip() if hasattr(self, 'api_base_edit') else ''
        config['model'] = self.model_edit.text().strip() if hasattr(self, 'model_edit') else ''
        
        # 流式传输选项（如果存在）
        if hasattr(self, 'enable_streaming_checkbox'):
            config['enable_streaming'] = self.enable_streaming_checkbox.isChecked()
        else:
            config['enable_streaming'] = True  # 默认启用
            
        # Custom模型特有选项
        if self.model_id == 'custom':
            if hasattr(self, 'disable_ssl_verify_checkbox'):
                config['disable_ssl_verify'] = self.disable_ssl_verify_checkbox.isChecked()
            else:
                config['disable_ssl_verify'] = False  # 默认启用SSL验证
        
        # 安全记录日志，不显示敏感信息
        safe_config = safe_log_config(config)
        logger.debug(f"{self.model_id.capitalize()}模型配置保存: {safe_config}")
        
        return config
    
    def on_config_changed(self):
        """配置变更时发出信号"""
        self.config_changed.emit()
    
    def retranslate_ui(self):
        """更新模型配置控件的文本"""
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"更新模型{self.model_id}的配置控件文本")

        # 定义已知标签的翻译
        known_labels = {
            'api_key': self.i18n.get('api_key_label', 'API Key:'),
            'base_url': self.i18n.get('base_url_label', 'Base URL:'),
            'model': self.i18n.get('model_label', 'Model:')
        }
        
        # 更新复选框文本
        if hasattr(self, 'enable_streaming_checkbox'):
            self.enable_streaming_checkbox.setText(self.i18n.get('model_enable_streaming', 'Enable Streaming'))
            logger.debug("更新了流式传输复选框文本")
            
        if hasattr(self, 'disable_ssl_verify_checkbox'):
            self.disable_ssl_verify_checkbox.setText(self.i18n.get('model_disable_ssl_verify', 'Disable SSL Verify'))
            logger.debug("更新了SSL验证复选框文本")
            
        for label in self.findChildren(QLabel):
            # 先检查objectName
            if hasattr(label, 'objectName') and label.objectName():
                obj_name = label.objectName().lower()
                for key, value in known_labels.items():
                    if key in obj_name:
                        label.setText(value)
                        logger.debug(f"基于objectName更新了{key}标签为: {value}")
                        break
            
            # 如果没有匹配到objectName，则尝试匹配当前文本
            current_text = label.text()
            if current_text in known_labels.values():
                continue  # 已经是最新的翻译，无需更新
            
            # 检查关键字匹配
            current_text_lower = current_text.lower()
            if ('api' in current_text_lower and ('key' in current_text_lower or 'token' in current_text_lower)) or '密钥' in current_text_lower or 'clé' in current_text_lower:
                label.setText(known_labels['api_key'])
                logger.debug(f"基于关键字更新了API Key标签为: {known_labels['api_key']}")
            elif ('base' in current_text_lower and 'url' in current_text_lower) or '基础' in current_text_lower or 'base' in current_text_lower:
                label.setText(known_labels['base_url'])
                logger.debug(f"基于关键字更新了Base URL标签为: {known_labels['base_url']}")
            elif 'model' in current_text_lower or '模型' in current_text_lower or 'modèle' in current_text_lower:
                label.setText(known_labels['model'])
                logger.debug(f"基于关键字更新了Model标签为: {known_labels['model']}")
        
        reset_text = self.i18n.get('reset_button', 'Reset to Default')
        reset_tooltip = self.i18n.get('reset_tooltip', 'Reset to default value')
        
        for button in self.findChildren(QPushButton):
            if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于objectName更新了Reset按钮文本为: {reset_text}")
            elif button.property('isResetButton'):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于属性更新了Reset按钮文本为: {reset_text}")
            elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于工具提示更新了Reset按钮文本为: {reset_text}")
            elif button.text() in ['Reset to Default', '重置', 'Réinitialiser', 'リセット']:
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于当前文本更新了Reset按钮文本为: {reset_text}")
        
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
                
            if model_config:
                default_api_base_url = getattr(model_config, 'DEFAULT_API_BASE_URL', '')
                self.api_base_edit.setPlaceholderText(self.i18n.get('base_url_placeholder', 'Default: {default_api_base_url}').format(
                    default_api_base_url=default_api_base_url
                ))
                logger.debug("更新了API Base URL占位符")
    
    def reset_model_params(self):
        """重置模型参数为默认值，保留 API Key"""
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
        else:
            # 未知模型，无法重置
            return
            
        # 获取模型配置
        model_config = get_current_model_config(provider)
        
        if model_config:
            # 更新 UI 元素，保留 API Key
            self.api_base_edit.setText(model_config.default_api_base_url)
            self.model_edit.setText(model_config.default_model_name)
            
            # 如果存在流式传输选项，则设置为默认值（通常为True）
            if hasattr(self, 'enable_streaming_checkbox'):
                self.enable_streaming_checkbox.setChecked(True)
                
            # 重置Custom模型的特殊配置
            if self.model_id == 'custom' and hasattr(self, 'disable_ssl_verify_checkbox'):
                self.disable_ssl_verify_checkbox.setChecked(False)  # 默认启用SSL验证
        
        # 触发配置变更信号
        self.on_config_changed()


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
        
        # 初始化模型工厂
        AIModelFactory.register_model('grok', GrokModel)
        AIModelFactory.register_model('gemini', GeminiModel)
        AIModelFactory.register_model('deepseek', DeepseekModel)
        AIModelFactory.register_model('custom', CustomModel)
        
        self.setup_ui()
        self.load_initial_values()
        
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
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # 创建主布局
        main_layout = QVBoxLayout()
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
        
        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)
        
        # 1. 顶部：语言选择
        lang_group = QGroupBox(self.i18n.get('display', 'Display'))
        lang_group.setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 15px; margin-top: 5px; margin-bottom: 5px; } QGroupBox::title { font-weight: bold; color: #666666; padding: 0 5px; subcontrol-origin: margin; subcontrol-position: top left; left: 10px; }")
        lang_layout = QVBoxLayout()
        
        self.lang_combo = QComboBox(self)
        for code, name in SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(name, code)
        current_index = self.lang_combo.findData(get_prefs()['language'])
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        lang_layout.addWidget(QLabel(self.i18n.get('language_label', 'Language:')))
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)

        # 2. 中部：AI模型选择和配置
        model_group = QGroupBox(self.i18n.get('ai_models', 'AI'))
        model_group.setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 15px; margin-top: 5px; margin-bottom: 5px; } QGroupBox::title { font-weight: bold; color: #666666; padding: 0 5px; subcontrol-origin: margin; subcontrol-position: top left; left: 10px; }")
        model_layout = QVBoxLayout()

        # 添加模型选择下拉框
        model_select_layout = QHBoxLayout()
        model_select_layout.addWidget(QLabel(self.i18n.get('current_ai', 'Current AI:')))

        self.model_combo = QComboBox()
        # 使用DEFAULT_MODELS字典来动态添加模型
        model_mapping = {
            AIProvider.AI_GROK: 'grok',
            AIProvider.AI_GEMINI: 'gemini',
            AIProvider.AI_DEEPSEEK: 'deepseek',
            AIProvider.AI_CUSTOM: 'custom'
        }
        # 按照默认模型顺序添加到下拉框
        for provider, model_id in model_mapping.items():
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
        # 设置合适的边距和间距
        self.models_layout.setContentsMargins(10, 10, 10, 10)
        self.models_layout.setSpacing(10)
        
        # 添加模型配置控件
        self.setup_model_widgets()
        
        # 直接将布局添加到模型组布局中
        model_layout.addLayout(self.models_layout)
        model_group.setLayout(model_layout)
        
        # 添加间距
        spacer2 = QWidget()
        spacer2.setFixedHeight(15)
        content_layout.addWidget(spacer2)
        
        # 3. 底部：提示词模板配置
        template_group = QGroupBox(self.i18n.get('prompt_template', 'Prompts'))
        template_group.setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 15px; margin-top: 5px; margin-bottom: 5px; } QGroupBox::title { font-weight: bold; color: #666666; padding: 0 5px; subcontrol-origin: margin; subcontrol-position: top left; left: 10px; }")
        template_layout = QVBoxLayout()
        
        # 主提示词模板
        main_template_layout = QVBoxLayout()
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
        
        # 将布局设置应用到模板组
        template_group.setLayout(template_layout)
        
        # 添加所有组件到内容布局
        content_layout.addWidget(lang_group)
        content_layout.addWidget(model_group)
        content_layout.addWidget(template_group)
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
                    logger.debug(f"保存当前模型 {model_id} 的配置: {safe_log_config(current_configs[model_id])}")
                except Exception as e:
                    logger.error(f"获取模型 {model_id} 配置时出错: {str(e)}")
                    # 如果控件已被删除，使用初始值或默认值
                    if hasattr(self, 'initial_values') and 'models' in self.initial_values and model_id in self.initial_values['models']:
                        current_configs[model_id] = self.initial_values['models'][model_id]
                        logger.debug(f"使用初始值作为模型 {model_id} 的配置: {safe_log_config(current_configs[model_id])}")
        
        # 清除当前布局中的所有元素
        self.clear_layout(self.models_layout)
        self.model_widgets = {}
        
        # 获取当前选中的模型
        model_id = self.model_combo.currentData()
        logger.debug(f"当前选中的模型: {model_id}")
        
        # 获取模型配置的优先级：
        # 1. 当前会话中用户修改过的配置（存储在current_configs中）
        # 2. 当前会话的初始值（存储在self.initial_values中）
        # 3. 已保存的配置（存储在prefs中）
        model_config = {}
        
        # 1. 首先检查当前会话中用户修改过的配置
        if model_id in current_configs:
            model_config = current_configs[model_id]
            logger.debug(f"使用当前会话中的模型配置: {safe_log_config(model_config)}")
        # 2. 如果没有，检查初始值
        elif hasattr(self, 'initial_values') and 'models' in self.initial_values and model_id in self.initial_values['models']:
            model_config = self.initial_values['models'].get(model_id, {})
            logger.debug(f"使用初始值中的模型配置: {safe_log_config(model_config)}")
        # 3. 如果还是没有，从已保存的配置中获取
        if not model_config:
            prefs = get_prefs()
            model_config = prefs.get('models', {}).get(model_id, {})
            logger.debug(f"使用已保存的模型配置: {safe_log_config(model_config)}")
        
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
        logger.debug(f"切换到模型: {model_id}")
        
        # 设置模型组件 - 这里会保存当前模型的配置并加载新选中模型的配置
        self.setup_model_widgets()
        
        # 模型切换时仅需要更新内容，不需要重新添加布局
        # setup_model_widgets 已经处理了布局初始化和清除工作
        
        self.update_model_name_display()
        
        # 切换模型不会自动触发保存按钮的启用，需要用户实际修改配置
        # 调用on_config_changed检查是否有变更
        self.on_config_changed()
    
    def update_model_name_display(self):
        """更新模型下拉框中的模型名称显示，使用当前语言的翻译"""
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("更新模型名称显示")
        
        # 保存当前选中的模型ID
        current_model_id = self.model_combo.currentData()
        
        # 暂时阻断信号，防止触发on_model_changed
        self.model_combo.blockSignals(True)
        
        # 清空下拉框
        self.model_combo.clear()
        
        # 使用DEFAULT_MODELS字典来动态添加模型
        model_mapping = {
            AIProvider.AI_GROK: 'grok',
            AIProvider.AI_GEMINI: 'gemini',
            AIProvider.AI_DEEPSEEK: 'deepseek',
            AIProvider.AI_CUSTOM: 'custom'
        }
        
        # 按照默认模型顺序添加到下拉框，使用翻译后的名称
        for provider, model_id in model_mapping.items():
            if provider in DEFAULT_MODELS:
                # 获取翻译后的模型名称
                display_name_key = f"model_display_name_{model_id}"
                translated_name = self.i18n.get(display_name_key, DEFAULT_MODELS[provider].display_name)
                logger.debug(f"模型 {model_id} 的翻译名称: {translated_name}")
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
            'selected_model': prefs.get('selected_model', 'grok'),
            'models': copy.deepcopy(prefs.get('models', {})),
            'random_questions': copy.deepcopy(prefs.get('random_questions', {}))
        }
        
        # 调试日志
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"加载初始值: {safe_log_config(self.initial_values['models'])}")
        logger.debug(f"当前选中模型: {self.initial_values['selected_model']}")
        if self.initial_values['selected_model'] in self.initial_values['models']:
            logger.debug(f"当前模型配置: {safe_log_config(self.initial_values['models'][self.initial_values['selected_model']])}")
        else:
            logger.debug(f"当前模型配置不存在")
        
        
        # 设置当前语言
        current_index = self.lang_combo.findData(self.initial_values['language'])
        if current_index >= 0:
            self.lang_combo.setCurrentIndex(current_index)
        
        # 更新模型名称显示
        self.update_model_name_display()
        
        # 设置模板
        self.template_edit.setPlainText(self.initial_values['template'])
        
        # 设置随机问题提示词
        random_questions = self.initial_values['random_questions']
        
        # 调试信息
        print(f"DEBUG: initial_values['random_questions'] = {random_questions}")
        print(f"DEBUG: current_lang = {current_lang}")
        print(f"DEBUG: random_questions.get(current_lang) = {random_questions.get(current_lang)}")
        print(f"DEBUG: get_suggestion_template(current_lang) = {repr(get_suggestion_template(current_lang)[:100])}...")
        
        # 获取随机问题提示词，如果不存在或为空则使用默认模板
        saved_questions = random_questions.get(current_lang)
        if saved_questions and saved_questions.strip():
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(current_lang)
        
        print(f"DEBUG: default_value = {repr(default_value)[:100]}...")
        
        self.random_questions_edit.setPlainText(default_value)
        
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
        logger.debug(f"语言切换为: {lang_code}, 开始更新界面")
        
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
                logger.debug(f"更新了Reset按钮文本为: {button.text()}")
            # 如果按钮没有objectName，则尝试使用其他方式识别
            elif button.property('isResetButton') or (
                  hasattr(button, 'toolTip') and 
                  ('reset' in button.toolTip().lower() or 
                   'default' in button.toolTip().lower())):
                button.setText(self.i18n.get('reset_button', 'Reset to Default'))
                logger.debug(f"更新了Reset按钮文本为: {button.text()}")
        
        # 更新模型配置控件中的文本和Reset按钮
        if hasattr(self, 'model_widgets'):
            for model_id, widget in self.model_widgets.items():
                if hasattr(widget, 'i18n'):
                    widget.i18n = self.i18n  # 更新i18n字典
                    # 调用模型配置控件的retranslate_ui方法更新所有文本
                    if hasattr(widget, 'retranslate_ui') and callable(widget.retranslate_ui):
                        widget.retranslate_ui()
                        logger.debug(f"调用了模型 {model_id} 的retranslate_ui方法更新文本")
                    
                    # 对所有按钮进行额外检查，确保重置按钮文本被正确更新
                    reset_text = self.i18n.get('reset_button', 'Reset to Default')
                    reset_tooltip = self.i18n.get('reset_tooltip', 'Reset to default value')
                    
                    for button in widget.findChildren(QPushButton):
                        # 检查按钮的objectName
                        if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                            logger.debug(f"基于objectName更新了模型 {model_id} 的Reset按钮文本为: {reset_text}")
                        # 检查按钮的isResetButton属性
                        elif button.property('isResetButton'):
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                            logger.debug(f"基于属性更新了模型 {model_id} 的Reset按钮文本为: {reset_text}")
                        # 检查按钮的工具提示
                        elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                            logger.debug(f"基于工具提示更新了模型 {model_id} 的Reset按钮文本为: {reset_text}")
                        # 检查按钮的当前文本
                        elif button.text() in ['Reset to Default', 'Reset', '重置', 'Réinitialiser', 'リセット', 'Nollaa', 'Tilbakestill', 'Nulstil', 'Återställ']:
                            button.setText(reset_text)
                            button.setToolTip(reset_tooltip)
                            logger.debug(f"基于当前文本更新了模型 {model_id} 的Reset按钮文本为: {reset_text}")
        
        # 更新模板内容
        self.template_edit.setPlainText(get_default_template(lang_code))
        self.template_edit.setPlaceholderText(self.i18n.get('template_placeholder', 'Enter your prompt template here...'))
        logger.debug(f"更新了模板内容为语言 {lang_code} 的默认模板")
        
        # 更新随机问题提示词
        random_questions = get_prefs().get('random_questions', {})
        saved_questions = random_questions.get(lang_code)
        if saved_questions and saved_questions.strip():
            default_value = saved_questions
        else:
            default_value = get_suggestion_template(lang_code)
        self.random_questions_edit.setPlainText(default_value)
        self.random_questions_edit.setPlaceholderText(self.i18n.get('random_questions_placeholder', 'Enter your random questions prompts here...'))
        logger.debug(f"更新了随机问题提示词为语言 {lang_code} 的默认值")
        
        # 确保所有标签都被更新，使用更全面的方法
        # 首先更新所有标签页和标签文本
        self.setWindowTitle(self.i18n.get('config_title', 'Ask Grok Configuration'))
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, self.i18n.get('general_tab', 'General'))
            self.tab_widget.setTabText(1, self.i18n.get('ai_models', 'AI'))
            logger.debug(f"更新了标签页文本")
        
        # 更新GroupBox标题
        for group_box in self.findChildren(QGroupBox):
            if 'display' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('display', 'Display'))
                logger.debug(f"更新了Display GroupBox标题")
            elif 'ai' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('ai_models', 'AI'))
                logger.debug(f"更新了AI GroupBox标题")
            elif 'prompt' in group_box.title().lower():
                group_box.setTitle(self.i18n.get('prompt_template', 'Prompts'))
                logger.debug(f"更新了Prompts GroupBox标题")
        
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
                        logger.debug(f"基于objectName更新了{key}标签为: {value}")
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
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'current_ai' and ('current' in current_text_lower or 'ai' in current_text_lower or '当前' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'api_key' and ('api' in current_text_lower or 'key' in current_text_lower or '密钥' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'base_url' and ('url' in current_text_lower or 'base' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'model' and ('model' in current_text_lower or '模型' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'ask_prompts' and (('ask' in current_text_lower and 'prompt' in current_text_lower) or '提问提示' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'random_questions' and (('random' in current_text_lower and 'question' in current_text_lower) or '随机问题' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    break
                elif key == 'prompt_template' and (('prompt' in current_text_lower and 'template' in current_text_lower) or '提示模板' in current_text_lower or '提示词模板' in current_text_lower):
                    label.setText(value)
                    logger.debug(f"基于关键字更新了{key}标签为: {value}")
                    
        # 发出语言改变信号，通知其他组件更新界面
        logger.debug(f"发送语言变更信号: {lang_code}")
        self.language_changed.emit(lang_code)
        
        # 标记配置已更改
        self.on_config_changed()
    
    def retranslate_ui(self):
        """更新界面文字"""
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("开始更新界面文字")
        
        # 更新标题和按钮文本
        self.setWindowTitle(self.i18n.get('config_title', 'Ask Grok Configuration'))
        #self.save_button.setText(self.i18n.get('save_button', 'Save'))
        
        # 更新成功提示文字
        if hasattr(self, 'save_success_label') and not self.save_success_label.isHidden():
            self.save_success_label.setText(self.i18n.get('save_success', 'Settings saved successfully!'))
        
        # 更新各个标签页标题
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, self.i18n.get('general_tab', 'General'))
            self.tab_widget.setTabText(1, self.i18n.get('ai_models', 'AI'))
        
        # 更新GroupBox标题
        for group_box in self.findChildren(QGroupBox):
            if group_box.title() == self.i18n.get('display', 'Display') or group_box.title() == 'Display':
                group_box.setTitle(self.i18n.get('display', 'Display'))
                logger.debug("更新了Display GroupBox标题")
            elif group_box.title() == self.i18n.get('ai_models', 'AI') or group_box.title() == 'AI':
                group_box.setTitle(self.i18n.get('ai_models', 'AI'))
                logger.debug("更新了AI GroupBox标题")
        
        # 更新所有标签文本
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
        for child in self.findChildren(QLabel):
            # 先检查objectName
            if hasattr(child, 'objectName') and child.objectName():
                obj_name = child.objectName().lower()
                for key, value in known_labels.items():
                    if key in obj_name:
                        child.setText(value)
                        logger.debug(f"基于objectName更新了{key}标签为: {value}")
                        break
            
            # 如果没有匹配到objectName，则尝试匹配当前文本
            current_text = child.text()
            if current_text in known_labels.values():
                continue  # 已经是最新的翻译，无需更新
            
            # 检查关键字匹配
            current_text_lower = current_text.lower()
            if ('language' in current_text_lower or '语言' in current_text or '言語' in current_text_lower):
                child.setText(known_labels['language'])
                logger.debug(f"基于关键字更新了语言标签为: {known_labels['language']}")
            elif ('current' in current_text_lower and 'ai' in current_text_lower) or '当前' in current_text:
                child.setText(known_labels['current_ai'])
                logger.debug(f"基于关键字更新了当前AI标签为: {known_labels['current_ai']}")
            elif ('api' in current_text_lower or ('key' in current_text_lower or 'token' in current_text_lower)) or '密钥' in current_text_lower or 'clé' in current_text_lower:
                child.setText(known_labels['api_key'])
                logger.debug(f"基于关键字更新了API Key标签为: {known_labels['api_key']}")
            elif ('base' in current_text_lower and 'url' in current_text_lower) or '基础' in current_text or 'base' in current_text_lower:
                child.setText(known_labels['base_url'])
                logger.debug(f"基于关键字更新了Base URL标签为: {known_labels['base_url']}")
            elif 'model' in current_text_lower or '模型' in current_text or 'modèle' in current_text_lower:
                child.setText(known_labels['model'])
                logger.debug(f"基于关键字更新了Model标签为: {known_labels['model']}")
            elif ('ask' in current_text_lower and 'prompt' in current_text_lower) or '提问提示' in current_text:
                child.setText(known_labels['ask_prompts'])
                logger.debug(f"基于关键字更新了Ask Prompts标签为: {known_labels['ask_prompts']}")
            elif ('random' in current_text_lower and ('question' in current_text_lower or 'prompt' in current_text_lower)) or '随机问题' in current_text:
                child.setText(known_labels['random_questions'])
                logger.debug(f"基于关键字更新了Random Questions Prompts标签为: {known_labels['random_questions']}")
            elif ('prompt' in current_text_lower and 'template' in current_text_lower) or '提示模板' in current_text or '提示词模板' in current_text:
                child.setText(known_labels['prompt_template'])
                logger.debug(f"基于关键字更新了Prompt Template标签为: {known_labels['prompt_template']}")
        
        # 更新所有按钮文本
        reset_text = self.i18n.get('reset_button', 'Reset to Default')
        reset_tooltip = self.i18n.get('reset_tooltip', 'Reset to default value')
        #save_text = self.i18n.get('save_button', 'Save')
        
        for button in self.findChildren(QPushButton):
            # 通过objectName或属性识别Reset按钮
            if hasattr(button, 'objectName') and 'reset' in button.objectName().lower():
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于objectName更新了Reset按钮文本为: {reset_text}")
            # 通过属性识别
            elif button.property('isResetButton'):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于属性更新了Reset按钮文本为: {reset_text}")
            # 通过工具提示识别
            elif hasattr(button, 'toolTip') and ('reset' in button.toolTip().lower() or 'default' in button.toolTip().lower()):
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于工具提示更新了Reset按钮文本为: {reset_text}")
            # 通过当前文本识别
            elif button.text() in ['Reset to Default', '重置', 'Réinitialiser', 'リセット']:
                button.setText(reset_text)
                button.setToolTip(reset_tooltip)
                logger.debug(f"基于当前文本更新了Reset按钮文本为: {reset_text}")
            # 更新Save按钮
            #elif button.text() in ['Save', '保存', 'Sauvegarder', '保存する']:
            #    button.setText(save_text)
            #    logger.debug(f"更新了Save按钮文本为: {save_text}")
        
        # 更新模型配置控件
        if hasattr(self, 'model_widgets'):
            for model_id, widget in self.model_widgets.items():
                if hasattr(widget, 'i18n'):
                    widget.i18n = self.i18n
                    logger.debug(f"更新了模型{model_id}的配置控件")
        
        # 更新模型下拉框中的显示名称
        self.update_model_name_display()
        logger.debug("更新了模型下拉框中的显示名称")
    
    def save_settings(self):
        """保存设置"""
        import logging
        logger = logging.getLogger(__name__)
        
        prefs = get_prefs()
        
        # 保存语言设置
        prefs['language'] = self.lang_combo.currentData()
        
        # 保存模板
        prefs['template'] = self.template_edit.toPlainText().strip()
        
        # 保存随机问题提示词
        current_lang = prefs['language']
        if 'random_questions' not in prefs:
            prefs['random_questions'] = {}
        prefs['random_questions'][current_lang] = self.random_questions_edit.toPlainText().strip()
        
        # 保存选中的模型
        prefs['selected_model'] = self.model_combo.currentData()
        
        # 保存所有模型的配置
        models_config = prefs.get('models', {})
        
        # 保存所有模型的配置，而不仅仅是当前选中的模型
        for model_id, widget in self.model_widgets.items():
            model_config = widget.get_config()
            models_config[model_id] = model_config
            logger.debug(f"保存模型 {model_id} 的配置: {safe_log_config(model_config)}")
        
        prefs['models'] = models_config
        logger.debug(f"保存到prefs的所有模型配置: {safe_log_config(models_config)}")
        
        # 更新按钮状态
        #self.save_button.setEnabled(False)
        
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
            logger.debug(f"强制刷新prefs配置后的模型配置: {refreshed_models.get('grok', {}).get('model', '未找到')}")
        
        # 重新获取最新的prefs值，确保我们使用的是已保存的值
        prefs = get_prefs(force_reload=True)  # 添加force_reload参数
        # 安全地记录重新获取的prefs
        reloaded_models = safe_log_config(prefs.get('models', {}))
        logger.debug(f"重新获取prefs后的模型配置: {reloaded_models.get('grok', {}).get('model', '未找到')}")
        current_lang = prefs.get('language', 'en')
        
        # 更新初始值，但不重新加载界面元素
        # 只更新初始值字典，不重新设置界面元素
        # 保存初始值
        self.initial_values = {
            'language': current_lang,
            'template': prefs.get('template', get_default_template(current_lang)),
            'selected_model': prefs.get('selected_model', 'grok'),
            'models': copy.deepcopy(prefs.get('models', {})),
            'random_questions': copy.deepcopy(prefs.get('random_questions', {}))
        }
        # 安全地记录更新后的初始值
        updated_models = safe_log_config(self.initial_values['models'])
        logger.debug(f"保存设置后更新初始值中的模型配置: {updated_models.get('grok', {}).get('model', '未找到')}")
        
        logger.debug(f"保存设置后更新初始值: {safe_log_config(self.initial_values['models'])}")
        
        # 确保设置已经写入到磁盘
        from calibre.utils.config import JSONConfig
        if isinstance(prefs, JSONConfig):
            prefs.commit()
    
    def check_for_changes(self):
        """检查是否有配置变更
        
        :return: 如果有变更返回 True，否则返回 False
        """
        # 获取当前语言
        current_lang = self.lang_combo.currentData()
        
        # 确保 initial_values 存在并包含必要的键
        if not hasattr(self, 'initial_values') or not isinstance(self.initial_values, dict):
            self.initial_values = {}
        
        # 确保必要的键存在
        for key in ['language', 'template', 'selected_model', 'models', 'random_questions']:
            if key not in self.initial_values:
                if key == 'language':
                    self.initial_values[key] = 'en'
                elif key == 'template':
                    self.initial_values[key] = ''
                elif key == 'selected_model':
                    self.initial_values[key] = 'grok'
                elif key == 'models' or key == 'random_questions':
                    self.initial_values[key] = {}
        
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
        
        # 检查模板是否更改
        if hasattr(self, 'template_edit'):
            template_text = self.template_edit.toPlainText().strip()
            if template_text != self.initial_values['template']:
                general_changed = True
                logger.debug("模板已更改")
        
        # 检查随机问题提示词是否更改
        random_questions_changed = False
        initial_random_questions = self.initial_values['random_questions'].get(current_lang, '')
        
        current_random_questions = ''
        if hasattr(self, 'random_questions_edit'):
            current_random_questions = self.random_questions_edit.toPlainText().strip()
            if current_random_questions != initial_random_questions:
                random_questions_changed = True
                logger.debug("随机问题提示词已更改")
        
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
                                logger.debug(f"模型 {model_id} 配置已更改")
                                break
                        except Exception as e:
                            logger.error(f"获取模型 {model_id} 配置时出错: {str(e)}")
            except Exception as e:
                logger.error(f"检查模型配置时出错: {str(e)}")
        
        # 返回是否有变更
        return general_changed or models_changed or random_questions_changed
    
    def on_config_changed(self):
        """当任何配置发生改变时检查是否需要启用保存按钮"""
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
