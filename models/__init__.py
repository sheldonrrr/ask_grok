"""
AI 模型模块初始化文件

此包包含所有 AI 模型的实现，包括基础模型抽象类和具体模型实现。
"""

from .base import BaseAIModel, AIModelFactory
from .grok import GrokModel
from .gemini import GeminiModel
from .deepseek import DeepseekModel
from .custom import CustomModel
from .openai import OpenAIModel
from .anthropic import AnthropicModel
from .nvidia import NvidiaModel

# 注册模型到工厂类
AIModelFactory.register_model('grok', GrokModel)
AIModelFactory.register_model('gemini', GeminiModel)
AIModelFactory.register_model('deepseek', DeepseekModel)
AIModelFactory.register_model('custom', CustomModel)
AIModelFactory.register_model('openai', OpenAIModel)
AIModelFactory.register_model('anthropic', AnthropicModel)
AIModelFactory.register_model('nvidia', NvidiaModel)

# 导出公共接口
__all__ = ['BaseAIModel', 'AIModelFactory', 'GrokModel', 'GeminiModel', 'DeepseekModel', 'CustomModel', 'OpenAIModel', 'AnthropicModel', 'NvidiaModel']
