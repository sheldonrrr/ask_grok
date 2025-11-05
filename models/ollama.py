"""
Ollama 本地大模型实现

Ollama 使用自定义 API 格式，与 OpenAI 不兼容
"""
import json
import time
import logging
from typing import Dict, Any, List, Optional

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.ollama')


class OllamaModel(BaseAIModel):
    """
    Ollama 本地大模型实现类
    
    Ollama 使用自定义 API 格式，主要用于本地运行大语言模型
    """
    # 默认模型名称
    DEFAULT_MODEL = "llama3"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "http://localhost:11434"
    
    def _validate_config(self):
        """
        验证 Ollama 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        # Ollama 只需要 api_base_url，API Key 是可选的
        if not self.config.get('api_base_url'):
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('missing_required_config', 'Missing required configuration: {key}').format(key='api_base_url'))
        
        # 如果 model 为空，使用默认值
        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL
    
    def get_token(self) -> str:
        """
        获取 Ollama 模型的 API Key
        
        Ollama 通常不需要 API Key（本地服务），返回空字符串
        
        :return: API Key 字符串（可能为空）
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        验证 Ollama 模型的 token
        
        Ollama 本地服务通常不需要认证，直接返回 True
        
        :return: 始终返回 True
        """
        # Ollama 本地服务不需要 token 验证
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 Ollama API 请求头
        
        Ollama 只需要 Content-Type，不需要认证头
        
        :return: 请求头字典
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # 如果配置了 API Key，添加到请求头（某些 Ollama 部署可能需要）
        api_key = self.get_token()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        return headers
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Ollama API 请求数据
        
        Ollama 使用自定义格式，与 OpenAI 不同
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream 等
        :return: 请求数据字典
        """
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
        
        # Ollama 格式
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
            ]
        }
        
        # 添加可选参数
        if 'temperature' in kwargs:
            data['temperature'] = kwargs['temperature']
        
        # 添加流式传输支持
        if kwargs.get('stream', False):
            data['stream'] = True
        else:
            data['stream'] = False
        
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 Ollama API 发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        # 检查是否使用流式传输 - 尊重显式传递的 stream 参数
        if 'stream' not in kwargs:
            kwargs['stream'] = self.config.get('enable_streaming', True)
        
        use_stream = kwargs['stream']
        stream_callback = kwargs.get('stream_callback', None)
        
        # 准备请求头和数据
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # Ollama 聊天端点
        api_url = f"{self.config['api_base_url']}/api/chat"
        
        try:
            # 如果使用流式传输
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                
                logger.debug(f"Ollama streaming request to: {api_url}")
                logger.debug(f"Request data: {json.dumps(data, ensure_ascii=False)[:200]}...")
                
                try:
                    with requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),
                        stream=True,
                        verify=False  # 本地服务通常不需要 SSL 验证
                    ) as response:
                        response.raise_for_status()
                        
                        # Ollama 流式响应：每行一个完整的 JSON 对象
                        for line in response.iter_lines():
                            if line:
                                try:
                                    line_str = line.decode('utf-8')
                                    line_data = json.loads(line_str)
                                    
                                    # Ollama 格式：{"message": {"role": "assistant", "content": "..."}, "done": false}
                                    if 'message' in line_data and 'content' in line_data['message']:
                                        chunk_text = line_data['message']['content']
                                        if chunk_text:
                                            full_content += chunk_text
                                            stream_callback(chunk_text)
                                            chunk_count += 1
                                    
                                    # 检查是否完成
                                    if line_data.get('done', False):
                                        logger.info(f"Ollama streaming completed, received {chunk_count} chunks, total length: {len(full_content)}")
                                        break
                                        
                                except json.JSONDecodeError as je:
                                    logger.error(f"JSON parsing error: {str(je)}, line: {line_str[:100]}...")
                                    continue
                    
                    return full_content
                    
                except Exception as e:
                    logger.error(f"Ollama streaming error: {str(e)}")
                    # 如果已经有部分内容，返回它
                    if full_content:
                        logger.warning(f"Returning partial content: {len(full_content)} characters")
                        return full_content
                    raise
            else:
                # 非流式请求
                logger.debug(f"Ollama non-streaming request to: {api_url}")
                logger.debug(f"Request data: {json.dumps(data, ensure_ascii=False)[:200]}...")
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),
                    verify=False  # 本地服务通常不需要 SSL 验证
                )
                response.raise_for_status()
                
                result = response.json()
                logger.debug(f"Ollama response status: {response.status_code}, response length: {len(response.text)}")
                
                # Ollama 非流式响应格式：{"message": {"role": "assistant", "content": "..."}}
                if 'message' in result and 'content' in result['message']:
                    content = result['message']['content']
                    logger.debug(f"Successfully got Ollama response, length: {len(content)}")
                    return content
                
                # 如果响应格式不符合预期
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('api_content_extraction_failed', 'Unable to extract content from Ollama API response')
                logger.error(f"{error_msg}, response: {json.dumps(result, ensure_ascii=False)[:200]}...")
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout as e:
            # 处理超时错误
            translations = get_translation(self.config.get('language', 'en'))
            timeout_value = kwargs.get('timeout', 60)
            error_msg = translations.get('request_timeout_error', 'Request timeout. Current timeout: {timeout} seconds').format(timeout=timeout_value)
            logger.error(f"Ollama API timeout error: {error_msg}")
            raise Exception(error_msg) from e
        except requests.exceptions.RequestException as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e))
            logger.error(f"Ollama API request error: {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error details: {json.dumps(error_detail, ensure_ascii=False)}")
                except:
                    logger.error(f"Response content: {e.response.text[:500]}")
            raise Exception(error_msg) from e
    
    def fetch_available_models(self) -> List[str]:
        """
        从 Ollama API 获取可用模型列表
        
        Ollama 使用特殊端点 /api/tags
        
        :return: 模型名称列表
        :raises Exception: 当请求失败时抛出异常
        """
        try:
            headers = self.prepare_headers()
            # Ollama 模型列表端点
            api_url = f"{self.config['api_base_url']}/api/tags"
            
            logger.debug(f"Fetching Ollama models from: {api_url}")
            
            response = requests.get(
                api_url,
                headers=headers,
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Ollama 响应格式：{"models": [{"name": "llama3", ...}, ...]}
            if 'models' in result and isinstance(result['models'], list):
                models = [model['name'] for model in result['models'] if 'name' in model]
                logger.info(f"Successfully fetched {len(models)} Ollama models")
                return models
            
            # 如果响应格式不符合预期
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('failed_to_fetch_models', 'Failed to fetch models: {error}').format(error='Invalid response format')
            logger.error(f"{error_msg}, response: {json.dumps(result, ensure_ascii=False)[:200]}...")
            raise Exception(error_msg)
            
        except requests.exceptions.RequestException as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('failed_to_fetch_models', 'Failed to fetch models: {error}').format(error=str(e))
            logger.error(f"Ollama fetch models error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error details: {json.dumps(error_detail, ensure_ascii=False)}")
                except:
                    logger.error(f"Response content: {e.response.text[:500]}")
            raise Exception(f"{error_msg}: {str(e)}") from e
    
    def supports_streaming(self) -> bool:
        """
        检查 Ollama 模型是否支持流式传输
        
        :return: 始终返回 True，因为 Ollama API 支持流式传输
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
        return "Ollama"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Ollama 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "api_key": "",  # 可选，本地服务通常不需要
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
