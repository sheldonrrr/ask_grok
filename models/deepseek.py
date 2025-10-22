"""
Deepseek AI 模型实现
"""
import json
import requests
import time
import logging
from typing import Dict, Any, Optional

from .base import BaseAIModel
from ..i18n import get_translation

# 获取日志记录器
logger = logging.getLogger('calibre_plugins.ask_grok.models.deepseek')


class DeepseekModel(BaseAIModel):
    """
    Deepseek AI 模型实现类
    """
    # 默认模型名称，集中管理便于后续更新
    DEFAULT_MODEL = "deepseek-chat"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://api.deepseek.com"
    
    def _validate_config(self):
        """
        验证 Deepseek 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        # 基本必需字段（不包括 model，因为在获取模型列表时可能为空）
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
        获取 Deepseek 模型的 API Key/Token
        
        :return: API Key/Token 字符串
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        验证 Deepseek 模型的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 首先调用基类的基本验证
        super().validate_token()
        
        token = self.get_token()
        
        # 检查 token 是否为空
        if not token or token.strip() == '':
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_empty', 'API Key is empty. Please enter a valid API Key.'))
        
        # 不再检查 token 长度或格式，只要不为空即可
        # Deepseek 可能支持多种格式的 API Key
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 Deepseek API 请求头
        
        :return: 请求头字典
        """
        token = self.get_token()
        
        # 根据 Deepseek API 文档，正确的认证头格式是: Authorization: Bearer <DeepSeek API Key>
        # 确保添加 Bearer 前缀
            
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Deepseek API 请求数据
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature 等
        :return: 请求数据字典
        """
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
        
        data = {
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
            "model": self.config.get('model', self.DEFAULT_MODEL),
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 8192)
        }
        
        # 添加流式传输支持（只有明确指定 stream=True 才添加）
        if kwargs.get('stream', False):
            data['stream'] = True
        
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 Deepseek API 发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        # 准备请求头和数据
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # 添加流式处理选项，可以减少超时问题
        use_stream = kwargs.get('stream', True)
        if use_stream:
            data['stream'] = True
        
        # 重试设置
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                if use_stream:
                    # 使用流式处理
                    full_content = ""
                    stream_callback = kwargs.get('stream_callback')
                    logger.info(f"开始流式请求, 回调函数存在: {stream_callback is not None}")
                    
                    try:
                        with requests.post(
                            f"{self.config['api_base_url']}/chat/completions",
                            headers=headers,
                            json=data,
                            timeout=kwargs.get('timeout', 300),
                            verify=True,
                            stream=True
                        ) as response:
                            response.raise_for_status()
                            logger.info(f"流式响应状态码: {response.status_code}")
                            
                            for line in response.iter_lines():
                                if line:
                                    line = line.decode('utf-8')
                                    logger.debug(f"收到流式响应行: {line[:50]}...")
                                    
                                    if line.startswith('data: '):
                                        line = line[6:]
                                        if line.strip() == '[DONE]':
                                            logger.info("收到流式响应结束标记 [DONE]")
                                            break
                                        
                                        try:
                                            chunk = json.loads(line)
                                            content = chunk.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                            
                                            if content:
                                                full_content += content
                                                logger.info(f"解析出内容片段, 长度: {len(content)}字符, 累计: {len(full_content)}字符")
                                                
                                                # 如果提供了回调函数，则调用它
                                                if stream_callback and callable(stream_callback):
                                                    logger.info(f"调用流式回调函数, 传递内容长度: {len(content)}字符")
                                                    stream_callback(content)
                                        except json.JSONDecodeError as e:
                                            logger.error(f"JSON解析错误: {str(e)}, 行内容: {line[:50]}...")
                                            continue
                    except Exception as e:
                        logger.error(f"流式请求处理异常: {str(e)}")
                        raise
                        
                    logger.info(f"流式请求完成, 总内容长度: {len(full_content)}字符")
                    return full_content
                else:
                    # 使用普通请求
                    response = requests.post(
                        f"{self.config['api_base_url']}/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),
                        verify=True
                    )
                    response.raise_for_status()
                    
                    result = response.json()
                    return result['choices'][0]['message']['content']
            
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    # 如果不是最后一次尝试，则等待后重试
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                    continue
                
                # 最后一次尝试失败，抛出异常
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e))
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        error_msg += f" | {json.dumps(error_detail, ensure_ascii=False)}"
                    except:
                        error_msg += f" | {e.response.text}"
                raise Exception(error_msg) from e
    
    def supports_streaming(self) -> bool:
        """
        检查 Deepseek 模型是否支持流式传输
        
        :return: 始终返回 True，因为 Deepseek API 支持流式传输
        """
        return True
        
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Deepseek 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
    
    # Deepseek 使用基类的默认实现（OpenAI 兼容格式），无需重写 fetch_available_models
