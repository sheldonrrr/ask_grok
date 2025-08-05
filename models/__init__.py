"""
AI 模型模块初始化文件

此包包含所有 AI 模型的实现，包括基础模型抽象类和具体模型实现。
"""

from .base import BaseAIModel, AIModelFactory
from .grok import GrokModel
from .gemini import GeminiModel
from .deepseek import DeepseekModel
from .custom import CustomModel

# 注册模型到工厂类
AIModelFactory.register_model('grok', GrokModel)
AIModelFactory.register_model('gemini', GeminiModel)
AIModelFactory.register_model('deepseek', DeepseekModel)
AIModelFactory.register_model('custom', CustomModel)

# 导出公共接口
__all__ = ['BaseAIModel', 'AIModelFactory', 'GrokModel', 'GeminiModel', 'DeepseekModel', 'CustomModel']
