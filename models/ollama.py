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
        # 获取 i18n 翻译（在 try 块之前，确保异常处理中可用）
        language = self.config.get('language', 'en')
        logger.debug(f"Ollama fetching models with language: {language}")
        translations = get_translation(language)
        logger.debug(f"Ollama translation for error_401: {translations.get('error_401', 'NOT FOUND')[:50]}...")
        
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
            user_msg = translations.get('error_unknown', 'Unknown error.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: Invalid response format"
            logger.error(f"Invalid Ollama response format, response: {json.dumps(result, ensure_ascii=False)[:200]}...")
            raise Exception(error_msg)
            
        except requests.exceptions.HTTPError as e:
            # HTTP 错误 - 根据状态码提供友好提示
            status_code = e.response.status_code if e.response is not None else None
            
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
            
            # 格式化完整错误信息
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Ollama HTTP error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error details: {json.dumps(error_detail, ensure_ascii=False)}")
                except:
                    logger.error(f"Response content: {e.response.text[:500]}")
            raise Exception(error_msg)
            
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误
            user_msg = translations.get('error_network', 
                'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Ollama connection error: {str(e)}")
            raise Exception(error_msg)
            
        except requests.exceptions.Timeout as e:
            # 超时错误
            user_msg = translations.get('error_network', 
                'Network connection failed. Please check network connection, proxy settings, or firewall configuration.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: Connection timeout"
            
            logger.error(f"Ollama request timeout: {str(e)}")
            raise Exception(error_msg)
            
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            user_msg = translations.get('error_unknown', 'Unknown error.')
            technical_label = translations.get('technical_details', 'Technical Details')
            error_msg = f"{user_msg}\n\n{technical_label}: {str(e)}"
            
            logger.error(f"Ollama request error: {str(e)}")
            raise Exception(error_msg)
    
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
    
    def verify_api_key_with_test_request(self) -> None:
        """
        验证 Ollama 服务是否可用
        虽然 Ollama 是本地服务不需要 API Key，但需要验证服务是否正在运行
        """
        import logging
        from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
        from ..i18n import get_translation
        
        logger.info("[Ollama] 验证本地服务是否可用...")
        provider_name = self.get_provider_name()
        
        try:
            # 发送一个测试请求到 /api/generate 端点
            api_base_url = self.config.get('api_base_url', self.DEFAULT_API_BASE_URL)
            test_url = f"{api_base_url}/api/generate"
            
            # 使用默认模型发送最小的测试请求
            test_data = {
                "model": self.DEFAULT_MODEL,
                "prompt": "hi",
                "stream": False
            }
            
            logger.info(f"[{provider_name}] 发送测试请求验证服务: {test_url}")
            
            response = requests.post(
                test_url,
                json=test_data,
                timeout=10,
                verify=False
            )
            
            logger.info(f"[{provider_name}] 测试请求响应状态码: {response.status_code}")
            logger.debug(f"[{provider_name}] 测试请求响应内容: {response.text[:200]}")
            
            # 检查响应状态码
            if response.status_code == 404:
                # 404 可能是模型不存在，但服务是运行的
                # 检查响应内容来确定
                if "model" in response.text.lower() and "not found" in response.text.lower():
                    logger.info(f"[{provider_name}] 服务运行正常，但默认模型不存在（这是正常的）")
                    return
                else:
                    logger.error(f"[{provider_name}] 服务端点不存在")
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get('ollama_service_not_running', 
                        'Ollama service is not running. Please start Ollama service first.')
                    tech_details = translations.get('technical_details', 'Technical Details')
                    raise Exception(f"{error_msg}\n\n{tech_details}: HTTP 404 - Service not found at {api_base_url}")
            
            elif response.status_code == 200:
                logger.info(f"[{provider_name}] 服务验证成功")
            
            elif 400 <= response.status_code < 500:
                # 4xx 错误说明服务在运行，只是请求有问题（这是可以接受的）
                logger.info(f"[{provider_name}] 服务运行正常 - 状态码: {response.status_code}")
            
            else:
                logger.warning(f"[{provider_name}] 收到未预期的状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError as e:
            # 连接错误 - 服务未运行
            logger.error(f"[{provider_name}] 无法连接到 Ollama 服务: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('ollama_service_not_running', 
                'Ollama service is not running. Please start Ollama service first.')
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(f"{error_msg}\n\n{tech_details}: Connection refused - {api_base_url}")
        
        except requests.exceptions.Timeout as e:
            # 超时错误
            logger.error(f"[{provider_name}] 连接超时: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('ollama_service_timeout', 
                'Ollama service connection timeout. Please check if the service is running properly.')
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(f"{error_msg}\n\n{tech_details}: Timeout")
        
        except requests.exceptions.RequestException as e:
            # 其他请求错误
            logger.error(f"[{provider_name}] 服务验证请求失败: {str(e)}")
            if not isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
                # 如果不是连接或超时错误，可能服务是运行的
                logger.info(f"[{provider_name}] 服务可能运行正常（收到非连接错误）")
