#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import urllib3
from typing import Optional, Dict, Any, Tuple, Union
import logging
from .i18n import get_translation
from .models import AIModelFactory, BaseAIModel
from .models.base import AIProvider, DEFAULT_MODELS, DEFAULT_PROVIDER
from .utils import mask_api_key, mask_api_key_in_text, safe_log_config

# 添加一个 logger
logger = logging.getLogger(__name__)

# 禁用不安全的请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AIAPIError(Exception):
    """自定义 API 错误异常类，适用于所有 AI 模型"""
    def __init__(self, message: str, status_code: Optional[int] = None, error_type: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type
        self.message = message

    def __str__(self) -> str:
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message

# 为了向后兼容，保留原有的错误类名
GrokAPIError = AIAPIError

class APIClient:
    """AI 模型 API 客户端，支持多种 AI 模型"""
    
    # 字符串模型名称到AIProvider枚举的映射
    _MODEL_TO_PROVIDER = {
        'grok': AIProvider.AI_GROK,
        'gemini': AIProvider.AI_GEMINI,
        'deepseek': AIProvider.AI_DEEPSEEK
    }
    
    def __init__(self, i18n: Dict[str, str] = None, 
                 max_retries: int = 3, timeout: float = 30.0):
        """初始化 AI 模型 API 客户端
        
        Args:
            i18n: 国际化文本字典
            max_retries: 最大重试次数
            timeout: 请求超时时间（秒）
        """
        self._timeout = timeout
        self._ai_model = None  # 当前使用的 AI 模型实例
        self._model_name = None  # 当前使用的模型名称
        
        # 初始化连接池
        self._session = self._create_session(max_retries, timeout)
        
        # 初始化 i18n
        self.i18n = i18n or get_translation('en')
        
        # 加载当前选择的模型
        self._load_current_model()
        
    def _create_session(self, max_retries: int, timeout: float) -> requests.Session:
        """创建带有连接池的 Session 对象"""
        session = requests.Session()
        
        # 配置连接池
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,      # 连接池数量
            pool_maxsize=10,         # 最大连接数
            max_retries=max_retries, # 最大重试次数
            pool_block=False         # 非阻塞模式
        )
        
        # 为 http 和 https 都添加适配器
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session
        
    def __del__(self):
        """析构函数，确保会话被正确关闭"""
        if hasattr(self, '_session'):
            try:
                self._session.close()
            except:
                pass
    
    def _prepare_request(self, prompt: str) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """准备 API 请求的共同部分
        
        Args:
            prompt: 问题文本
            
        Returns:
            tuple: (headers, data) 请求头和请求数据
        """
        # 检查模型是否已加载
        if not self._ai_model:
            self._load_current_model()
            
        if not self._ai_model:
            error_msg = self.i18n.get('no_model_configured', 'No AI model configured. Please configure an AI model in settings.')
            raise AIAPIError(error_msg, error_type="config_error")
        
        try:
            # 验证 token
            self._ai_model.validate_token()
            
            # 获取请求头和请求数据
            headers = self._ai_model.prepare_headers()
            data = self._ai_model.prepare_request_data(prompt, system_message=self.i18n.get(
                'system_message',
                "You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis. Focus on the substance of the books, not just their titles."
            ))
            
            # 记录日志
            logger.debug(f"Prepared request for model: {self._model_name}")
            
            return headers, data
            
        except Exception as e:
            # 将异常转换为 AIAPIError
            error_msg = str(e)
            if "API Key not set" in error_msg or "token" in error_msg.lower():
                error_type = "auth_error"
            else:
                error_type = "config_error"
                
            raise AIAPIError(error_msg, error_type=error_type) from e
    
    def ask(self, prompt: str, lang_code: str = 'en', return_dict: bool = False, stream: bool = False, stream_callback=None) -> str:
        """向 AI 模型发送问题并获取回答，支持流式请求
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            return_dict: 是否返回完整的响应字典，默认为 False，只返回文本
            stream: 是否使用流式请求，默认为 False
            stream_callback: 流式响应回调函数，用于处理流式响应的每个片段
            
        Returns:
            str 或 dict: 如果 return_dict 为 False，返回回答文本；否则返回完整的响应字典
            
        Raises:
            AIAPIError: 当 API 请求失败时抛出
        """
        # 更新 i18n 以确保使用正确的语言
        self.i18n = get_translation(lang_code)
        
        # 检查模型是否已加载
        if not self._ai_model:
            # 尝试重新加载模型
            self._load_current_model()
            
            if not self._ai_model:
                error_msg = self.i18n.get('no_model_configured', 'No AI model configured. Please configure an AI model in settings.')
                raise AIAPIError(error_msg, error_type="config_error")
        
        try:
            # 准备请求参数
            kwargs = {
                'temperature': 0.7,
                'max_tokens': 2000
            }
            
            # 检查模型是否支持流式传输以及是否在配置中启用了流式传输
            model_supports_streaming = hasattr(self._ai_model, 'supports_streaming') and self._ai_model.supports_streaming()
            streaming_enabled = self._ai_model.config.get('enable_streaming', True)  # 默认启用
            
            # 如果请求流式响应，模型支持流式传输，并且配置中启用了流式传输
            if stream and model_supports_streaming and streaming_enabled:
                kwargs['stream'] = True
                
                # 如果提供了回调函数，使用流式请求
                if stream_callback:
                    # 创建一个内部回调处理器，将其传递给模型的ask方法
                    def handle_stream_response(chunk):
                        if chunk and stream_callback:
                            stream_callback(chunk)
                    
                    # 将回调处理器传递给模型
                    kwargs['stream_callback'] = handle_stream_response
                    
                    # 记录日志
                    logger.debug(f"使用流式传输请求 {self._model_name} 模型")
            
            # 使用模型实例发送请求
            response = self._ai_model.ask(prompt, **kwargs)
            
            # 如果响应为空，抛出错误
            if not response.strip():
                error_msg = self.i18n.get('empty_answer', 'API returned an empty answer')
                raise AIAPIError(error_msg, error_type="api_error")
            
            # 根据 return_dict 参数决定返回值
            if return_dict:
                # 为了向后兼容，构造一个类似 Grok API 的响应格式
                return {
                    "choices": [
                        {
                            "message": {
                                "content": response
                            }
                        }
                    ],
                    "model": self._model_name
                }
            else:
                return response
                
        except AIAPIError:
            # 直接重新抛出 AIAPIError
            raise
        except Exception as e:
            # 处理其他未知错误
            error_msg = f"{self.i18n.get('unknown_error', 'Unknown error')}: {str(e)}"
            raise AIAPIError(error_msg, error_type="unknown_error") from e
    
    def _get_provider_from_model_name(self, model_name: str) -> AIProvider:
        """根据模型名称获取对应的AIProvider枚举值
        
        Args:
            model_name: 模型名称字符串
            
        Returns:
            AIProvider: 对应的AIProvider枚举值
        """
        return self._MODEL_TO_PROVIDER.get(model_name, DEFAULT_PROVIDER)
    
    def _load_current_model(self):
        """加载当前选择的模型"""
        from calibre.utils.config import JSONConfig
        try:
            # 获取当前配置
            prefs = JSONConfig('plugins/ask_grok')
            selected_model = prefs.get('selected_model', 'grok')  # 仍然使用字符串作为配置键
            models_config = prefs.get('models', {})
            
            # 添加调试日志
            logger.debug(f"当前选中的模型: {selected_model}")
            # 安全记录所有模型配置，隐藏API Key
            safe_models_config = safe_log_config(models_config)
            logger.debug(f"所有模型配置: {safe_models_config}")
            
            # 获取选中模型的配置
            model_config = models_config.get(selected_model, {})
            
            # 添加调试日志
            # 安全记录选中模型的配置，隐藏API Key
            safe_model_config = safe_log_config(model_config)
            logger.debug(f"选中模型的配置: {safe_model_config}")
            
            # 获取对应的AIProvider枚举值
            provider = self._get_provider_from_model_name(selected_model)
            
            # 如果模型配置不存在，尝试使用 grok 作为后备
            if not model_config:
                if selected_model != 'grok' and 'grok' in models_config:
                    selected_model = 'grok'
                    model_config = models_config.get('grok', {})
                    provider = AIProvider.AI_GROK
                    # 安全记录后备模型的配置，隐藏API Key
                    safe_model_config = safe_log_config(model_config)
                    logger.debug(f"使用后备模型 grok，配置: {safe_model_config}")
            
            # 创建模型实例
            if model_config:
                self._model_name = selected_model
                self._ai_model = AIModelFactory.create_model(selected_model, model_config)
                # 安全记录模型配置，隐藏API Key
                safe_model_config = safe_log_config(model_config)
                logger.info(f"已加载 AI 模型: {selected_model} ({provider.name}), 配置: {safe_model_config}")
            else:
                logger.warning("未找到有效的 AI 模型配置，将无法发送请求")
                self._model_name = None
                self._ai_model = None
                
        except Exception as e:
            logger.error(f"加载 AI 模型时出错: {str(e)}")
            self._model_name = None
            self._ai_model = None
    
    def get_random_question_prompt(self, lang_code: str = 'en') -> str:
        """获取随机问题提示词
        
        Args:
            lang_code: 语言代码，用于获取相应语言的随机问题提示词
            
        Returns:
            str: 随机选择的一个问题提示词，如果没有配置则返回空字符串
        """
        from calibre.utils.config import JSONConfig
        import random
        
        # 获取当前配置
        prefs = JSONConfig('plugins/ask_grok')
        random_questions = prefs.get('random_questions', {})
        
        # 获取当前语言的随机问题提示词
        questions = random_questions.get(lang_code, '')
        if not questions:
            return ''
        
        # 按行分割并过滤空行
        question_list = [q.strip() for q in questions.split('\n') if q.strip()]
        if not question_list:
            return ''
        
        # 随机选择一个问题提示词
        return random.choice(question_list)
    
    def random_question(self, prompt: str, lang_code: str = 'en') -> str:
        """生成随机问题
        
        使用当前配置的 AI 模型生成随机问题
        
        Args:
            prompt: 包含书籍信息的提示词
            lang_code: 语言代码，用于获取相应的翻译文本
            
        Returns:
            str: 生成的随机问题
            
        Raises:
            AIAPIError: 当 API 请求失败时抛出
        """
        # 更新 i18n 以确保使用正确的语言
        self.i18n = get_translation(lang_code)
        
        # 获取当前使用的模型名称，用于日志记录
        model_name = self._ai_model.__class__.__name__
        logger.debug(f"使用 {model_name} 生成随机问题，提示词: {prompt[:50]}...")
        
        try:
            # 明确指定 stream=False，禁用流式传输
            logger.debug(f"{model_name}: 开始请求随机问题，禁用流式传输")
            response = self._ai_model.ask(prompt, stream=False)
            
            logger.debug(f"{model_name}: 成功获取响应，长度: {len(response) if response else 0}")
            
            # 清理响应，去除多余的空白字符和引号
            response = response.strip()
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1].strip()
                
            return response
                
        except AIAPIError as api_error:
            # 记录详细的 API 错误信息
            logger.error(f"{model_name} API 错误: {str(api_error)}")
            # 直接重新抛出 AIAPIError
            raise
        except Exception as e:
            # 记录详细的异常信息
            logger.error(f"{model_name} 随机问题生成异常: {str(e)}", exc_info=True)
            # 处理其他未知错误
            error_msg = f"{self.i18n.get('random_question_error', 'Error generating random question')}: {str(e)}"
            raise AIAPIError(error_msg, error_type="random_question_error") from e
    
    def reload_model(self):
        """重新加载当前选择的模型"""
        self._load_current_model()
        return self._model_name is not None and self._ai_model is not None
    
    @property
    def model_name(self):
        """获取当前使用的模型名称"""
        if not self._model_name:
            self._load_current_model()
        return self._model_name or 'unknown'
    
    @property
    def model_display_name(self):
        """获取当前使用的模型显示名称"""
        if not self._model_name:
            self._load_current_model()
        
        if not self._model_name:
            return 'Unknown Model'
        
        # 获取对应的AIProvider枚举值
        provider = self._get_provider_from_model_name(self._model_name)
        
        # 从默认模型配置中获取显示名称
        model_config = DEFAULT_MODELS.get(provider)
        if model_config:
            return model_config.display_name
        
        # 如果没有找到对应的配置，使用默认名称
        return self._model_name.capitalize()
            
    @property
    def auth_token(self):
        """获取当前模型的认证令牌"""
        if not self._ai_model:
            self._load_current_model()
            
        if not self._ai_model:
            return ''
            
        # 获取对应的AIProvider枚举值
        provider = self._get_provider_from_model_name(self._model_name)
        
        # 从模型配置中获取认证令牌
        if hasattr(self._ai_model, 'config'):
            # 根据不同的模型类型获取正确的API密钥字段
            if provider == AIProvider.AI_GROK:
                return self._ai_model.config.get('auth_token', '')
            else:
                # 其他模型默认使用api_key字段
                return self._ai_model.config.get('api_key', '')
        return ''
    
    @property
    def api_base(self):
        """获取当前模型的 API 基础 URL"""
        if not self._ai_model:
            self._load_current_model()
            
        if not self._ai_model:
            # 使用默认模型配置中的API基础URL
            return DEFAULT_MODELS[AIProvider.AI_GROK].default_api_base_url
            
        # 获取对应的AIProvider枚举值
        provider = self._get_provider_from_model_name(self._model_name)
        
        # 从模型配置中获取 API 基础 URL
        if hasattr(self._ai_model, 'config'):
            # 获取对应模型的默认API基础URL
            default_api_base_url = DEFAULT_MODELS[provider].default_api_base_url
            return self._ai_model.config.get('api_base_url', default_api_base_url)
            
        # 如果没有配置，使用默认值
        return DEFAULT_MODELS[provider].default_api_base_url
    
    @property
    def model(self):
        """获取当前模型的模型名称"""
        if not self._ai_model:
            self._load_current_model()
            
        if not self._ai_model:
            # 使用默认模型配置中的模型名称
            return DEFAULT_MODELS[AIProvider.AI_GROK].default_model_name
            
        # 获取对应的AIProvider枚举值
        provider = self._get_provider_from_model_name(self._model_name)
        
        # 从模型配置中获取模型名称
        if hasattr(self._ai_model, 'config'):
            # 获取对应模型的默认模型名称
            default_model_name = DEFAULT_MODELS[provider].default_model_name
            return self._ai_model.config.get('model', default_model_name)
            
        # 如果没有配置，使用默认值
        return DEFAULT_MODELS[provider].default_model_name


# 创建 APIClient 的全局实例，供其他模块导入使用
api = APIClient()