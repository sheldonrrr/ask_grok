#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base module for internationalization (i18n) in Ask AI Plugin.
This module is a compatibility layer that re-exports classes and functions from models.base.
"""

# 从models.base导入所有需要的类和函数
from ..models.base import (
    AIProvider as ModelType,  # 为了向后兼容，将AIProvider重命名为ModelType
    ModelConfig,
    DEFAULT_MODELS,
    DEFAULT_PROVIDER as DEFAULT_MODEL_TYPE,  # 为了向后兼容，将DEFAULT_PROVIDER重命名为DEFAULT_MODEL_TYPE
    BaseTranslation,
    TranslationRegistry,
    get_translation,
    get_model_specific_translation,
    get_current_model_config,
    set_default_provider as set_default_model_type,  # 为了向后兼容，将set_default_provider重命名为set_default_model_type
    get_default_template,
    get_suggestion_template,
    get_all_languages
)

# 为了向后兼容，确保任何使用ModelType的代码仍然有效
# 创建从旧的ModelType枚举名称到新的AIProvider枚举值的映射
# 导入AIProvider以确保它在此模块中可用
from ..models.base import AIProvider

MODELTYPE_TO_AIPROVIDER = {
    'GROK': AIProvider.AI_GROK,
    'GEMINI': AIProvider.AI_GEMINI,
    'DEEPSEEK': AIProvider.AI_DEEPSEEK,
}

# 确保旧代码中使用的ModelType.GROK等仍然有效
for old_name, provider in MODELTYPE_TO_AIPROVIDER.items():
    setattr(ModelType, old_name, provider)
