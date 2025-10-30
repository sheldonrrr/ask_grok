"""
基础 AI 模型抽象类和工厂类

定义了所有 AI 模型需要实现的接口和基础功能。
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union
from enum import Enum, auto


class AIProvider(Enum):
    """AI 服务提供商枚举类型"""
    AI_GROK = auto()      # x.AI (Grok)
    AI_GEMINI = auto()    # Google Gemini
    AI_DEEPSEEK = auto()  # Deepseek
    AI_CUSTOM = auto()    # Custom (Local or Remote API)
    AI_OPENAI = auto()    # OpenAI (GPT models)
    AI_ANTHROPIC = auto() # Anthropic (Claude models)
    AI_NVIDIA = auto()    # Nvidia AI (Free tier available)
    AI_OPENROUTER = auto() # OpenRouter (Model aggregator)
    AI_OLLAMA = auto()    # Ollama (Local models)


class ModelConfig:
    """特定 AI 模型的配置类"""
    
    def __init__(self, 
                 provider: AIProvider,
                 display_name: str,
                 api_key_label: str,
                 default_api_base_url: str,
                 default_model_name: str):
        """
        初始化模型配置
        
        :param provider: AI 服务提供商类型
        :param display_name: 显示名称
        :param api_key_label: API 密钥标签
        :param default_api_base_url: 默认 API 基础 URL
        :param default_model_name: 默认模型名称
        """
        self.provider = provider
        self.display_name = display_name
        self.api_key_label = api_key_label
        self.default_api_base_url = default_api_base_url
        self.default_model_name = default_model_name


# 默认模型配置
DEFAULT_MODELS = {
    AIProvider.AI_GROK: ModelConfig(
        provider=AIProvider.AI_GROK,
        display_name="x.AI (Grok)",
        api_key_label="X.AI API Key:",
        default_api_base_url="https://api.x.ai/v1",
        default_model_name="grok-4-latest"
    ),
    AIProvider.AI_GEMINI: ModelConfig(
        provider=AIProvider.AI_GEMINI,
        display_name="Google Gemini",
        api_key_label="API Key:",
        default_api_base_url="https://generativelanguage.googleapis.com/v1beta",
        default_model_name="gemini-2.5-pro"
    ),
    AIProvider.AI_DEEPSEEK: ModelConfig(
        provider=AIProvider.AI_DEEPSEEK,
        display_name="Deepseek",
        api_key_label="API Key:",
        default_api_base_url="https://api.deepseek.com",
        default_model_name="deepseek-chat"
    ),
    AIProvider.AI_CUSTOM: ModelConfig(
        provider=AIProvider.AI_CUSTOM,
        display_name="Custom",
        api_key_label="API Key:",
        default_api_base_url="",
        default_model_name=""
    ),
    AIProvider.AI_OPENAI: ModelConfig(
        provider=AIProvider.AI_OPENAI,
        display_name="OpenAI",
        api_key_label="OpenAI API Key:",
        default_api_base_url="https://api.openai.com/v1",
        default_model_name="gpt-4o-mini"
    ),
    AIProvider.AI_ANTHROPIC: ModelConfig(
        provider=AIProvider.AI_ANTHROPIC,
        display_name="Anthropic (Claude)",
        api_key_label="Anthropic API Key:",
        default_api_base_url="https://api.anthropic.com/v1",
        default_model_name="claude-3-5-sonnet-20241022"
    ),
    AIProvider.AI_NVIDIA: ModelConfig(
        provider=AIProvider.AI_NVIDIA,
        display_name="Nvidia AI",
        api_key_label="Nvidia API Key:",
        default_api_base_url="https://integrate.api.nvidia.com/v1",
        default_model_name="meta/llama-3.3-70b-instruct"
    ),
    AIProvider.AI_OPENROUTER: ModelConfig(
        provider=AIProvider.AI_OPENROUTER,
        display_name="OpenRouter",
        api_key_label="OpenRouter API Key:",
        default_api_base_url="https://openrouter.ai/api/v1",
        default_model_name="openai/gpt-4o-mini"
    ),
    AIProvider.AI_OLLAMA: ModelConfig(
        provider=AIProvider.AI_OLLAMA,
        display_name="Ollama (Local)",
        api_key_label="API Key (Optional):",
        default_api_base_url="http://localhost:11434",
        default_model_name="llama3"
    )
}

# 默认 AI 提供商
DEFAULT_PROVIDER = AIProvider.AI_GROK

class BaseTranslation:
    """所有语言翻译的基类"""
    
    @property
    def code(self) -> str:
        """返回语言代码"""
        raise NotImplementedError("子类必须实现语言代码属性")
    
    @property
    def name(self) -> str:
        """返回语言名称"""
        raise NotImplementedError("子类必须实现语言名称属性")
    
    @property
    def default_template(self) -> str:
        """返回该语言的默认模板"""
        raise NotImplementedError("子类必须实现默认模板属性")
    
    @property
    def suggestion_template(self) -> str:
        """返回该语言的建议模板"""
        raise NotImplementedError("子类必须实现建议模板属性")
    
    @property
    def translations(self) -> Dict[str, str]:
        """返回该语言的所有翻译"""
        raise NotImplementedError("子类必须实现翻译字典属性")
        
    def get_model_specific_translation(self, key: str, provider: AIProvider = DEFAULT_PROVIDER) -> str:
        """
        获取特定 AI 提供商的翻译
        
        :param key: 翻译键
        :param provider: AI 提供商类型
        :return: 翻译文本
        """
        translations = self.translations
        model_key = f"{key}_{provider.name.lower()}"
        
        # 首先尝试获取特定 AI 提供商的翻译
        if model_key in translations:
            return translations[model_key]
        
        # 回退到通用翻译
        return translations.get(key, key)


class TranslationRegistry:
    """所有可用翻译的注册表"""
    
    _translations: Dict[str, BaseTranslation] = {}
    _default_language = "en"
    
    @classmethod
    def register(cls, translation_class):
        """注册翻译类"""
        instance = translation_class()
        cls._translations[instance.code] = instance
        return translation_class
    
    @classmethod
    def get_translation(cls, lang_code: str) -> BaseTranslation:
        """根据语言代码获取翻译"""
        return cls._translations.get(lang_code, cls._translations.get(cls._default_language))
    
    @classmethod
    def get_all_languages(cls) -> Dict[str, str]:
        """获取所有可用语言，格式为 {代码: 名称}"""
        return {code: trans.name for code, trans in cls._translations.items()}
    
    @classmethod
    def set_default_language(cls, lang_code: str) -> None:
        """设置默认语言"""
        if lang_code in cls._translations:
            cls._default_language = lang_code


def get_translation(lang_code: str) -> Dict[str, str]:
    """获取指定语言代码的翻译"""
    translation = TranslationRegistry.get_translation(lang_code)
    return translation.translations


def get_model_specific_translation(key: str, lang_code: str, provider: AIProvider = DEFAULT_PROVIDER) -> str:
    """获取指定语言代码的特定 AI 提供商翻译"""
    translation = TranslationRegistry.get_translation(lang_code)
    return translation.get_model_specific_translation(key, provider)


def get_current_model_config(provider: AIProvider = DEFAULT_PROVIDER) -> ModelConfig:
    """获取指定 AI 提供商的配置"""
    return DEFAULT_MODELS.get(provider, DEFAULT_MODELS[DEFAULT_PROVIDER])


def set_default_provider(provider: AIProvider) -> None:
    """设置默认 AI 提供商"""
    global DEFAULT_PROVIDER
    DEFAULT_PROVIDER = provider


def get_default_template(lang_code: str) -> str:
    """获取指定语言代码的默认模板"""
    translation = TranslationRegistry.get_translation(lang_code)
    return translation.default_template


def get_suggestion_template(lang_code: str) -> str:
    """获取指定语言代码的建议模板"""
    translation = TranslationRegistry.get_translation(lang_code)
    return translation.suggestion_template


def get_multi_book_template(lang_code: str) -> str:
    """获取指定语言代码的多书默认模板"""
    translation = TranslationRegistry.get_translation(lang_code)
    return translation.multi_book_default_template


def get_all_languages() -> Dict[str, str]:
    """获取所有可用语言"""
    return TranslationRegistry.get_all_languages()


class BaseAIModel(ABC):
    """
    AI 模型抽象基类，定义所有 AI 模型需要实现的接口
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 AI 模型
        
        :param config: 模型配置字典，包含 API key 等必要参数
        """
        self.config = config
        self._validate_config()
    
    @abstractmethod
    def _validate_config(self) -> None:
        """
        验证配置是否有效
        
        :raises ValueError: 当配置无效时抛出异常
        """
        pass
    
    def validate_token(self) -> bool:
        """
        验证模型配置中的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 基本验证：检查 token 是否存在
        token = self.get_token()
        if not token or not token.strip():
            raise ValueError("API Key not set or empty")
        return True
    
    def get_token(self) -> str:
        """
        获取模型的 API Key/Token
        子类可以重写此方法以支持不同的 token 字段名
        
        :return: API Key/Token 字符串
        """
        # 尝试常见的 token 字段名
        for key in ['auth_token', 'api_key', 'token']:
            if key in self.config and self.config[key]:
                return self.config[key]
        return ""
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 API 请求头
        子类可以重写此方法以支持不同的请求头格式
        
        :return: 请求头字典
        """
        return {
            "Content-Type": "application/json"
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 API 请求数据
        子类必须重写此方法以支持不同的请求数据格式
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature 等
        :return: 请求数据字典
        """
        raise NotImplementedError("子类必须实现 prepare_request_data 方法")
    
    @abstractmethod
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 AI 模型发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        pass
        
    def supports_streaming(self) -> bool:
        """
        检查模型是否支持流式传输
        
        :return: 如果支持流式传输则返回 True，默认为 False
        """
        return False
    
    def get_models_endpoint(self) -> str:
        """
        获取模型列表的 API 端点
        子类可以重写此方法以自定义端点
        
        :return: API 端点路径，默认为 "/models"
        """
        return "/models"
    
    def prepare_models_request_headers(self) -> Dict[str, str]:
        """
        准备获取模型列表的请求头
        子类可以重写此方法以自定义请求头
        默认使用 prepare_headers() 方法
        
        :return: 请求头字典
        """
        return self.prepare_headers()
    
    def build_api_url(self, base_url: str, endpoint: str) -> str:
        """
        智能构建 API URL，避免路径重复
        
        这是一个通用方法，处理常见的 URL 拼接问题：
        1. 避免重复的路径段（如 /v1/v1/...）
        2. 正确处理尾部斜杠
        3. 支持完整路径的 base_url
        
        :param base_url: API 基础 URL
        :param endpoint: API 端点路径
        :return: 完整的请求 URL
        
        示例:
            base_url="https://api.example.com/v1", endpoint="/v1/chat/completions"
            -> "https://api.example.com/v1/chat/completions"
            
            base_url="https://api.example.com", endpoint="/v1/chat/completions"
            -> "https://api.example.com/v1/chat/completions"
        """
        base_url = base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        
        # 如果 base_url 已经包含了 endpoint 的开始部分，避免重复
        # 例如: base_url 以 /v1 结尾，endpoint 以 v1/ 开始
        if base_url.endswith('/v1') and endpoint.startswith('v1/'):
            # 移除 endpoint 中重复的 v1
            endpoint = endpoint[3:]  # 移除 "v1/"
        
        return f"{base_url}/{endpoint}"
    
    def prepare_models_request_url(self, base_url: str, endpoint: str) -> str:
        """
        准备获取模型列表的完整 URL
        子类可以重写此方法以自定义 URL 格式（如 Gemini 需要在 URL 中添加 API key）
        
        :param base_url: API 基础 URL
        :param endpoint: API 端点路径
        :return: 完整的请求 URL
        """
        return self.build_api_url(base_url, endpoint)
    
    def parse_models_response(self, data: Dict[str, Any]) -> list:
        """
        解析模型列表 API 响应
        子类可以重写此方法以处理不同的响应格式
        默认处理 OpenAI 兼容格式: {"data": [{"id": "model-name"}, ...]}
        
        :param data: API 响应的 JSON 数据
        :return: 模型名称列表
        """
        return [model['id'] for model in data.get('data', [])]
    
    def get_logger_name(self) -> str:
        """
        获取 logger 名称
        
        :return: logger 名称字符串
        """
        class_name = self.__class__.__name__.lower().replace('model', '')
        return f'calibre_plugins.ask_ai_plugin.models.{class_name}'
    
    def fetch_available_models(self) -> list:
        """
        通用的获取模型列表实现
        
        此方法提供了一个标准的实现流程：
        1. 准备 URL 和请求头
        2. 发送 GET 请求
        3. 解析响应
        4. 返回排序后的模型列表
        
        子类通常不需要重写此方法，只需重写以下辅助方法来定制行为：
        - get_models_endpoint(): 自定义 API 端点
        - prepare_models_request_headers(): 自定义请求头
        - prepare_models_request_url(): 自定义 URL 格式
        - parse_models_response(): 自定义响应解析
        
        如果提供商完全不支持模型列表 API，子类应该抛出 NotImplementedError
        
        :return: 模型名称列表
        :raises NotImplementedError: 如果提供商不支持模型列表 API
        :raises Exception: 当 API 请求失败时抛出异常
        """
        import logging
        import requests
        
        logger = logging.getLogger(self.get_logger_name())
        
        try:
            # 获取配置
            api_base_url = self.config.get('api_base_url', getattr(self, 'DEFAULT_API_BASE_URL', ''))
            
            # 准备请求
            endpoint = self.get_models_endpoint()
            url = self.prepare_models_request_url(api_base_url, endpoint)
            headers = self.prepare_models_request_headers()
            
            # 获取 i18n 翻译
            from ..i18n import get_translation
            translations = get_translation(self.config.get('language', 'en'))
            
            # 发送请求
            logger.info(translations.get('fetching_models_from', 'Fetching models from {url}').format(url=url))
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            models = self.parse_models_response(data)
            
            # 记录成功
            provider_name = self.get_provider_name()
            logger.info(translations.get('successfully_fetched_models', 
                                        'Successfully fetched {count} {provider} models').format(
                                            count=len(models), 
                                            provider=provider_name))
            return sorted(models)
            
        except requests.exceptions.RequestException as e:
            logger.error(translations.get('failed_to_fetch_models', 
                                         'Failed to fetch models: {error}').format(error=str(e)))
            raise Exception(translations.get('failed_to_fetch_models', 
                                           'Failed to fetch models: {error}').format(error=str(e)))


class AIModelFactory:
    """
    AI 模型工厂类，用于创建不同类型的 AI 模型实例
    """
    _model_classes = {}
    
    @classmethod
    def register_model(cls, model_name: str, model_class):
        """
        注册模型类
        
        :param model_name: 模型名称，如 'grok', 'gemini' 等
        :param model_class: 模型类，必须是 BaseAIModel 的子类
        """
        if not issubclass(model_class, BaseAIModel):
            raise TypeError(f"Model class must be a subclass of BaseAIModel, got {model_class.__name__}")
        cls._model_classes[model_name] = model_class
    
    @classmethod
    def create_model(cls, model_name: str, config: Dict[str, Any]) -> BaseAIModel:
        """
        创建指定类型的 AI 模型实例
        
        :param model_name: 模型名称，如 'grok', 'gemini' 等
        :param config: 模型配置
        :return: AI 模型实例
        :raises ValueError: 当指定的模型未注册时抛出异常
        """
        model_class = cls._model_classes.get(model_name)
        if model_class is None:
            raise ValueError(f"Unknown model: {model_name}. Available models: {list(cls._model_classes.keys())}")
        return model_class(config)
    
    @classmethod
    def get_available_models(cls) -> list:
        """
        获取所有已注册的模型名称
        
        :return: 已注册的模型名称列表
        """
        return list(cls._model_classes.keys())
    
    @classmethod
    def get_model_default_config(cls, model_name: str) -> Dict[str, Any]:
        """
        获取指定模型的默认配置
        
        :param model_name: 模型名称
        :return: 默认配置字典
        :raises ValueError: 当指定的模型未注册时抛出异常
        """
        model_class = cls._model_classes.get(model_name)
        if model_class is None:
            # 使用i18n翻译字符串
            from calibre_plugins.ask_ai_plugin.i18n import get_translation
            i18n = get_translation('en')  # 默认使用英文
            error_msg = i18n.get('unknown_model', 'Unknown model: {model_name}').format(model_name=model_name)
            raise ValueError(error_msg)
        return model_class.get_default_config()
