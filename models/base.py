"""
基础 AI 模型抽象类和工厂类

定义了所有 AI 模型需要实现的接口和基础功能。
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union, List
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
    AI_PERPLEXITY = auto() # Perplexity (Sonar)
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
    AIProvider.AI_PERPLEXITY: ModelConfig(
        provider=AIProvider.AI_PERPLEXITY,
        display_name="Perplexity",
        api_key_label="Perplexity API Key:",
        default_api_base_url="https://api.perplexity.ai",
        default_model_name="sonar"
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
    # Per-key fallback: use English as base and override with target language.
    # This guarantees missing keys never raise KeyError in UI code that uses
    # dict indexing, while still allowing partial translations.
    en_translation = TranslationRegistry.get_translation(TranslationRegistry._default_language)
    base = {}
    try:
        base = en_translation.translations.copy() if en_translation is not None else {}
    except Exception:
        base = {}
    try:
        if translation is not None and translation is not en_translation:
            base.update(translation.translations)
    except Exception:
        pass
    return base


def format_http_error(e: Exception, lang_code: str = 'en') -> str:
    """
    格式化 HTTP 错误信息为用户友好格式
    
    :param e: 异常对象（requests.exceptions.HTTPError 或其他）
    :param lang_code: 语言代码
    :return: 格式化的错误信息（用户友好描述 + 技术细节）
    """
    from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
    
    translations = get_translation(lang_code)
    
    # 检查是否是 HTTPError
    if isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code if e.response is not None else None
        
        # 根据状态码选择错误描述
        if status_code == 401:
            user_msg = translations.get('error_401', 
                'API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.')
        elif status_code == 403:
            user_msg = translations.get('error_403', 
                'Access denied. Please check: API Key has sufficient permissions, no regional access restrictions.')
        elif status_code == 404:
            user_msg = translations.get('error_404', 
                'API endpoint not found. Please check if the API Base URL configuration is correct.')
        elif status_code == 429:
            user_msg = translations.get('error_429', 
                'Too many requests, rate limit reached. Please try again later.')
        elif status_code and 500 <= status_code < 600:
            user_msg = translations.get('error_5xx', 
                'Server error. Please try again later or check the service provider status.')
        else:
            user_msg = translations.get('error_unknown', 'Unknown error.')
    elif isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
        # 网络连接错误或超时
        user_msg = translations.get('error_network', 
            'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
    else:
        # 其他错误
        user_msg = translations.get('error_unknown', 'Unknown error.')
    
    # 格式化完整错误信息
    technical_label = translations.get('technical_details', 'Technical Details')
    return f"{user_msg}\n\n{technical_label}: {str(e)}"


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
    
    def fetch_available_models(self, skip_verification: bool = False) -> List[str]:
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
        from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
        
        logger = logging.getLogger(self.get_logger_name())
        
        # 获取 i18n 翻译（在 try 块之前，确保异常处理中可用）
        from ..i18n import get_translation
        language = self.config.get('language', 'en')
        translations = get_translation(language)
        
        try:
            # 获取配置
            api_base_url = self.config.get('api_base_url', getattr(self, 'DEFAULT_API_BASE_URL', ''))
            api_key = self.config.get('api_key', '')
            
            # 准备请求
            endpoint = self.get_models_endpoint()
            url = self.prepare_models_request_url(api_base_url, endpoint)
            headers = self.prepare_models_request_headers()
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            models = self.parse_models_response(data)
            
            # 验证 API Key 是否有效（某些提供商的 /models 端点是公开的）
            # 可以通过 skip_verification 参数跳过验证，稍后手动验证
            if not skip_verification:
                try:
                    self.verify_api_key_with_test_request()
                except Exception as verify_error:
                    logger.error(f"[{self.get_provider_name()}] API Key 验证失败: {str(verify_error)}")
                    raise
            
            return sorted(models)
            
        except requests.exceptions.HTTPError as e:
            # HTTP 错误 - 根据状态码提供友好提示
            status_code = e.response.status_code if e.response is not None else None
            logger.error(f"[{self.get_provider_name()}] HTTP 错误 - 状态码: {status_code}")
            if e.response is not None:
                logger.error(f"[{self.get_provider_name()}] 响应内容: {e.response.text[:500]}")
            
            # 特殊处理：检查响应内容中的特定错误信息
            response_text = e.response.text if e.response is not None else ""
            
            # Gemini 地理位置限制错误
            if status_code == 400 and ('User location is not supported' in response_text or 'FAILED_PRECONDITION' in response_text):
                user_msg = translations.get('gemini_geo_restriction',
                    'Gemini API is not available in your region. Please try:\n'
                    '1. Use a VPN to connect from a supported region\n'
                    '2. Use other AI providers (OpenAI, Anthropic, DeepSeek, etc.)\n'
                    '3. Check Google AI Studio for region availability')
                technical_label = translations.get('technical_details', 'Technical Details')
                error_msg = f"{user_msg}\n\n{technical_label}: User location is not supported for the API use"
                logger.error(f"Failed to fetch models: {error_msg}")
                raise Exception(error_msg)
            
            # 选择对应的错误描述
            if status_code == 401:
                user_msg = translations.get('error_401', 
                    'API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.')
            elif status_code == 403:
                user_msg = translations.get('error_403', 
                    'Access denied. Please check: API Key has sufficient permissions, no regional access restrictions.')
            elif status_code == 404:
                user_msg = translations.get('error_404', 
                    'API endpoint not found. Please check if the API Base URL configuration is correct.')
            elif status_code == 429:
                user_msg = translations.get('error_429', 
                    'Too many requests, rate limit reached. Please try again later.')
            elif status_code and 500 <= status_code < 600:
                user_msg = translations.get('error_5xx', 
                    'Server error. Please try again later or check the service provider status.')
            else:
                user_msg = translations.get('error_unknown', 'Unknown error.')
            
            # 格式化完整错误信息：用户友好描述 + 技术细节
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Failed to fetch models: {str(e)}")
            raise Exception(error_msg)
            
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误
            user_msg = translations.get('error_network', 
                'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Network connection error: {str(e)}")
            raise Exception(error_msg)
            
        except requests.exceptions.Timeout as e:
            # 超时错误
            user_msg = translations.get('error_network', 
                'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: Connection timeout"
            
            logger.error(f"Request timeout: {str(e)}")
            raise Exception(error_msg)
            
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            user_msg = translations.get('error_unknown', 'Unknown error.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Request error: {str(e)}")
            raise Exception(error_msg)
    
    def verify_api_key_with_test_request(self) -> None:
        """
        通过发送测试请求来验证 API Key 是否有效
        
        某些 AI 提供商的 /models 端点是公开的，不需要认证，
        因此无法通过获取模型列表来验证 API Key 的有效性。
        这个方法会发送一个最小的测试请求到需要认证的端点来验证。
        
        默认实现：发送一个最小的 chat completion 请求
        子类可以重写此方法来自定义验证逻辑
        
        :raises Exception: 当 API Key 无效时抛出异常
        """
        import logging
        from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
        from ..i18n import get_translation
        
        logger = logging.getLogger(self.get_logger_name())
        provider_name = self.get_provider_name()
        
        try:
            # 准备测试请求
            headers = self.prepare_headers()
            api_base_url = self.config.get('api_base_url', getattr(self, 'DEFAULT_API_BASE_URL', ''))
            test_url = f"{api_base_url}/chat/completions"
            
            # 发送一个最小的测试请求
            test_data = self.prepare_request_data("hi", max_tokens=1, stream=False)
            
            logger.info(f"[{provider_name}] 发送测试请求验证 API Key: {test_url}")
            
            # 在线模型超时时间较长（15秒）
            timeout_seconds = 15
            response = requests.post(
                test_url,
                headers=headers,
                json=test_data,
                timeout=timeout_seconds,
                verify=False
            )
            
            logger.info(f"[{provider_name}] 测试请求响应状态码: {response.status_code}")
            logger.debug(f"[{provider_name}] 测试请求响应内容: {response.text[:200]}")
            
            # 401 = API Key 无效
            # 400/422 = API Key 有效，但请求参数无效（说明认证通过）
            # 200 = API Key 有效且请求成功
            # 404 = 端点不存在，可能是 API Key 无效或配置错误
            
            if response.status_code == 401:
                logger.error(f"[{provider_name}] API Key 无效 - 401 Unauthorized")
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('error_401', 
                    'API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.')
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(f"{error_msg}\n\n{tech_details}: HTTP 401 - Invalid API Key")
            
            elif response.status_code == 404:
                logger.error(f"[{provider_name}] 端点返回 404")
                logger.error(f"[{provider_name}] 响应内容: {response.text}")
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('error_404', 
                    'API endpoint not found. Please check if the API Base URL configuration is correct.')
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(f"{error_msg}\n\n{tech_details}: HTTP 404 - This may indicate an invalid API Key or insufficient permissions.")
            
            elif response.status_code in [200, 400, 422]:
                logger.info(f"[{provider_name}] API Key 验证成功 - 状态码: {response.status_code}")
            
            else:
                logger.warning(f"[{provider_name}] 收到未预期的状态码: {response.status_code}")
                
        except requests.exceptions.Timeout as e:
            # 超时错误 - 添加超时时间信息
            logger.error(f"[{provider_name}] API Key 验证请求超时: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('error_network', 
                'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(f"{error_msg}\n\n{tech_details}: Timeout after {timeout_seconds} seconds")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"[{provider_name}] API Key 验证请求失败: {str(e)}")
            # 如果是 401 错误，抛出友好的错误信息
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
                logger.error(f"[{provider_name}] 响应内容: {e.response.text[:200]}")
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('error_401', 
                    'API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.')
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(f"{error_msg}\n\n{tech_details}: {str(e)}")
            # 其他错误（400, 422等）说明 API Key 是有效的
            logger.info(f"[{provider_name}] API Key 验证通过（收到非401响应）")


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
