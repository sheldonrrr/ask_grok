"""
OpenRouter AI 模型实现

OpenRouter 是一个模型聚合器，使用 OpenAI 兼容的 API 格式
"""
import logging
from typing import Dict, Any

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.openrouter')


class OpenRouterModel(BaseAIModel):
    """
    OpenRouter AI 模型实现类
    
    OpenRouter 使用 OpenAI 兼容的 API 格式，但支持额外的可选请求头
    """
    # 默认模型名称
    DEFAULT_MODEL = "openai/gpt-4o-mini"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://openrouter.ai/api/v1"
    
    def _validate_config(self):
        """
        验证 OpenRouter 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        # 基本必需字段
        required_keys = ['api_key', 'api_base_url']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(translations.get('missing_required_config', 'Missing required configuration: {key}').format(key=key))
        
        # 如果 model 为空，使用默认值
        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL
    
    def get_token(self) -> str:
        """
        获取 OpenRouter 模型的 API Key
        
        :return: API Key 字符串
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        验证 OpenRouter 模型的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 首先调用基类的基本验证
        super().validate_token()
        
        token = self.get_token()
        
        # OpenRouter API Key 格式验证：基本长度检查
        if len(token) < 10:
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_too_short', 'API Key is too short. Please check and enter the complete key.'))
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 OpenRouter API 请求头
        
        OpenRouter 支持额外的可选请求头用于排名和标识
        
        :return: 请求头字典
        """
        token = self.get_token()
        
        # 确保 token 有 Bearer 前缀
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        
        # 添加可选的请求头
        # HTTP-Referer: 用于在 OpenRouter 上进行排名
        if self.config.get('http_referer'):
            headers['HTTP-Referer'] = self.config['http_referer']
        
        # X-Title: 应用名称标识
        if self.config.get('x_title'):
            headers['X-Title'] = self.config['x_title']
        
        return headers
    
    def supports_streaming(self) -> bool:
        """
        检查 OpenRouter 模型是否支持流式传输
        
        :return: 始终返回 True，因为 OpenRouter API 支持流式传输
        """
        return True
    
    def get_model_name(self) -> str:
        """
        获取当前模型名称
        
        :return: 模型名称字符串
        """
        return self.config.get('model', self.DEFAULT_MODEL)
    
    def get_provider_name(self) -> str:
        """
        获取提供商名称
        
        :return: 提供商名称字符串
        """
        return "OpenRouter"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 OpenRouter 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
            "http_referer": "",  # 可选：用于在 OpenRouter 上进行排名
            "x_title": "Ask AI Plugin",  # 可选：应用名称标识
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 OpenRouter API 请求数据
        
        OpenRouter 使用 OpenAI 兼容格式
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream 等
        :return: 请求数据字典
        """
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
        
        data = {
            "model": self.config.get('model', self.DEFAULT_MODEL),
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4096)
        }
        
        # 添加流式传输支持（只有明确指定 stream=True 才添加）
        if kwargs.get('stream', False):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 OpenRouter API 发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        import json
        import requests
        import time
        
        # 检查是否使用流式传输 - 尊重显式传递的 stream 参数
        if 'stream' not in kwargs:
            kwargs['stream'] = self.config.get('enable_streaming', True)
        
        use_stream = kwargs['stream']
        stream_callback = kwargs.get('stream_callback', None)
        
        # 准备请求头和数据
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.openrouter')
        
        try:
            # 如果使用流式传输
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                
                api_url = f"{self.config['api_base_url']}/chat/completions"
                
                try:
                    with requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),
                        stream=True,
                        verify=False
                    ) as response:
                        response.raise_for_status()
                        
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    # 处理数据行
                                    try:
                                        if line_str == 'data: [DONE]':
                                            break
                                        line_data = json.loads(line_str[6:])  # 去除 'data: ' 前缀
                                        if 'choices' in line_data and line_data['choices']:
                                            choice = line_data['choices'][0]
                                            if 'delta' in choice and 'content' in choice['delta']:
                                                chunk_text = choice['delta']['content']
                                                if chunk_text:
                                                    full_content += chunk_text
                                                    stream_callback(chunk_text)
                                                    chunk_count += 1
                                                    last_chunk_time = time.time()
                                    except json.JSONDecodeError as je:
                                        logger.error(f"JSON parse error: {str(je)}, line content: {line_str[:50]}...")
                                        continue
                        
                        logger.info(f"Streaming completed, received {chunk_count} chunks, total length: {len(full_content)}")
                        return full_content
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"OpenRouter API request error: {str(e)}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e)))
            
            # 非流式模式
            else:
                api_url = f"{self.config['api_base_url']}/chat/completions"
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),
                    verify=False
                )
                response.raise_for_status()
                
                result = response.json()
                if 'choices' in result and result['choices']:
                    return result['choices'][0]['message']['content']
                else:
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('invalid_response', 'Invalid API response format'))
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e)))
    
    # OpenRouter 使用基类的默认实现获取模型列表
    # fetch_available_models() - GET /v1/models 端点
