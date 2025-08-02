#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Internationalization package for Ask Grok plugin.
This package provides translations for the plugin interface.
"""

# 从models.base导入AI提供商和模型配置类
from ..models.base import (
    AIProvider,
    ModelConfig,
    DEFAULT_MODELS,
    DEFAULT_PROVIDER,
    get_translation,
    get_default_template,
    get_suggestion_template,
    get_all_languages,
    get_model_specific_translation,
    get_current_model_config,
    set_default_provider
)

# Import all language modules to register them
from . import en
from . import fr
from . import de
from . import es
from . import pt
from . import nl
from . import da
from . import fi
from . import no
from . import sv
from . import ru
from . import ja
from . import zh
from . import zht
from . import yue

__all__ = [
    # Base classes and types
    'AIProvider',
    'ModelConfig',
    'DEFAULT_MODELS',
    'DEFAULT_PROVIDER',
    
    # Core functions
    'get_translation',
    'get_default_template',
    'get_suggestion_template',
    'get_all_languages',
    'get_model_specific_translation',
    'get_current_model_config',
    'set_default_provider'
]
