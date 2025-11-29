"""
Custom AI 模型实现

支持用户自定义的本地或远程API模型，如Ollama等
"""
import json
from typing import Dict, Any, Optional

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation


class CustomModel(BaseAIModel):
    """
    Custom AI 模型实现类
    支持用户自定义的本地或远程API模型，如Ollama等
    """
    # 默认模型名称
    DEFAULT_MODEL = "llama3"
    # 默认 API 基础 URL (Ollama默认地址)
    DEFAULT_API_BASE_URL = "http://localhost:11434"
    
    def _validate_config(self):
        """
        验证 Custom 模型配置（实现抽象方法）
        验证必要的配置项
        
        :raises ValueError: 当配置无效时抛出异常
        """
        # 只验证 api_base_url，model 可以为空（在 Load Models 时）
        if not self.config.get('api_base_url'):
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('missing_required_config', 'Missing required configuration: {key}').format(key='api_base_url'))
        # model 在 Load Models 时可以为空，不做强制检查
    
    def validate_config(self):
        """
        验证 Custom 模型配置（公共方法）
        """
        self._validate_config()
    
    def validate_token(self) -> bool:
        """
        验证 Custom 模型的配置是否有效
        对于本地模型，可能不需要token，所以这里只验证基本配置
        
        :return: 如果配置有效则返回 True
        :raises ValueError: 当配置无效时抛出异常
        """
        # 不调用基类的validate_token方法，因为基类会检查API Key
        # 而对于Custom模型，API Key是可选的
        self._validate_config()
        
        # 验证API基础URL（必需）
        if not self.config.get('api_base_url'):
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_base_url_required', 'API Base URL is required'))
        
        # model 在 Load Models 时可以为空，只在实际对话时才需要
        # 所以这里不验证 model
        
        # 对于API Key，如果提供了就验证非空，但不强制要求提供
        # 这样本地模型就可以不需要API Key
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 API 请求头
        对于本地模型，API Key是可选的
        
        :return: 请求头字典
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # 如果有API Key，则添加到请求头中
        # 如果没有，则不添加Authorization头
        token = self.get_token()
        if token and token.strip():
            if not token.startswith('Bearer '):
                token = f'Bearer {token}'
            headers["Authorization"] = token
            
        return headers
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 API 请求数据
        
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
            "temperature": kwargs.get('temperature', 0.7)
        }
        
        # 添加流式传输支持（只有明确指定 stream=True 才添加）
        if kwargs.get('stream', False):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 API 发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        # 准备请求头和数据
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # 检查是否使用流式传输
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        
        try:
            # 构建API URL - 使用基类的智能 URL 构建方法
            base_url = self.config['api_base_url']
            
            # 如果 base_url 已经包含完整路径，直接使用
            if '/api/chat' in base_url or '/chat/completions' in base_url:
                api_url = base_url
            else:
                # 使用基类方法智能拼接 URL
                api_url = self.build_api_url(base_url, '/v1/chat/completions')
            
            # 如果使用流式传输
            if use_stream and stream_callback:
                full_content = ""
                
                # 发送流式请求
                # 对于本地请求，完全禁用代理
                # 创建新的会话对象，确保不使用任何代理
                session = requests.Session()
                session.trust_env = False  # 不使用环境变量中的代理设置
                
                # 使用session发送请求，而不是直接使用requests.post
                with session.post(
                    api_url,
                    headers=headers,
                    json=data,
                    stream=True,
                    timeout=kwargs.get('timeout', 60)
                ) as response:
                    response.raise_for_status()
                    
                    for line in response.iter_lines():
                        if not line:
                            continue
                        
                        # 解码行
                        line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                        
                        # OpenAI 格式使用 "data: " 前缀
                        if line_str.startswith('data: '):
                            line_str = line_str[6:]  # 移除 "data: " 前缀
                        
                        # 跳过 [DONE] 标记
                        if line_str.strip() == '[DONE]':
                            break
                            
                        try:
                            # 解析JSON响应
                            chunk = json.loads(line_str)
                            
                            # 尝试 OpenAI 格式：提取 choices[0].delta.content
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    full_content += content
                                    stream_callback(content)
                            # 兼容 Ollama 格式：提取 message.content
                            elif 'message' in chunk and 'content' in chunk['message']:
                                content = chunk['message']['content']
                                if content:
                                    full_content += content
                                    stream_callback(content)
                                # 检查是否完成
                                if chunk.get('done', False):
                                    break
                                
                        except json.JSONDecodeError:
                            continue
                
                return full_content
            else:
                # 非流式请求
                import logging
                logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.custom')
                
                logger.debug("开始Custom模型非流式请求")
                try:
                    # 记录请求详情，但隐藏敏感信息
                    logger.debug(f"请求URL: {api_url}")
                    
                    # 隐藏授权信息的请求头记录
                    safe_headers = {k: '***' if k.lower() == 'authorization' else v for k, v in headers.items()}
                    logger.debug(f"请求头: {json.dumps(safe_headers, ensure_ascii=False)}")
                    
                    # 记录请求数据
                    logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)[:500]}...")
                    
                    # 设置stream=False以获取完整响应
                    data['stream'] = False
                    
                    # 对于本地请求，完全禁用代理
                    # 创建新的会话对象，确保不使用任何代理
                    session = requests.Session()
                    session.trust_env = False  # 不使用环境变量中的代理设置
                    
                    # 使用session发送请求，而不是直接使用requests.post
                    response = session.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 60)
                    )
                    response.raise_for_status()
                    
                    logger.debug(f"响应状态: {response.status_code}, 响应长度: {len(response.text)}")
                    
                    result = response.json()
                    
                    # 尝试 OpenAI 格式
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        logger.debug(f"成功获取响应内容（OpenAI格式），长度: {len(content)}")
                        return content
                    
                    # 兼容 Ollama 格式
                    if 'message' in result and 'content' in result['message']:
                        content = result['message']['content']
                        logger.debug(f"成功获取响应内容（Ollama格式），长度: {len(content)}")
                        return content
                    
                    # 如果响应格式不符合预期
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get('api_content_extraction_failed', 'Unable to extract content from API response')
                    logger.error(f"{error_msg}, 响应: {json.dumps(result, ensure_ascii=False)[:200]}...")
                    raise Exception(error_msg)
                except requests.exceptions.RequestException as req_e:
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get('api_request_failed', 'API request failed: {error}').format(error=str(req_e))
                    logger.error(error_msg)
                    if hasattr(req_e, 'response') and req_e.response is not None:
                        try:
                            error_detail = req_e.response.json()
                            logger.error(f"错误详情: {json.dumps(error_detail, ensure_ascii=False)}")
                        except:
                            logger.error(f"响应内容: {req_e.response.text[:500]}")
                    raise Exception(error_msg) from req_e
            
        except requests.exceptions.RequestException as e:
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
        检查模型是否支持流式传输
        
        :return: 始终返回 True，因为我们假设API支持流式传输
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
        return "Custom"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "api_key": "",  # 完全可选，本地模型通常不需要，远程服务可能需要
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
    
    # Custom 模型使用基类的 build_api_url 方法，无需重写 prepare_models_request_url
