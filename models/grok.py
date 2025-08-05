"""
Grok AI 模型实现
"""
import json
import requests
from typing import Dict, Any, Optional

from .base import BaseAIModel


class GrokModel(BaseAIModel):
    """
    Grok AI 模型实现类
    """
    # 默认模型名称，集中管理便于后续更新
    DEFAULT_MODEL = "grok-4-latest"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://api.x.ai/v1"
    
    def _validate_config(self):
        """
        验证 Grok 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        required_keys = ['auth_token', 'api_base_url', 'model']
        for key in required_keys:
            if not self.config.get(key):
                raise ValueError(f"Missing required config key: {key}")
    
    def get_token(self) -> str:
        """
        获取 Grok 模型的 API Key/Token
        
        :return: API Key/Token 字符串
        """
        return self.config.get('auth_token', '')
    
    def validate_token(self) -> bool:
        """
        验证 Grok 模型的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 首先调用基类的基本验证
        super().validate_token()
        
        token = self.get_token()
        
        # Grok API Key 格式验证（可选）
        # 注意：这里我们不再强制要求 xai- 前缀，因为 API 可能会变化
        if len(token) < 10:  # 只要求基本长度
            raise ValueError("API Key is too short. Please check and enter the complete key.")
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 Grok API 请求头
        
        :return: 请求头字典
        """
        token = self.get_token()
        
        # 确保 token 有 Bearer 前缀
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
            
        return {
            "Content-Type": "application/json",
            "Authorization": token
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Grok API 请求数据
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream 等
        :return: 请求数据字典
        """
        system_message = kwargs.get('system_message', "You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.")
        
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
            "max_tokens": kwargs.get('max_tokens', 2000)
        }
        
        # 添加流式传输支持
        if kwargs.get('stream', self.config.get('enable_streaming', True)):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 Grok API 发送提示并获取响应
        
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
            # 如果使用流式传输
            if use_stream and stream_callback:
                full_content = ""
                with requests.post(
                    f"{self.config['api_base_url']}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),  # 流式传输需要更长的超时时间
                    stream=True,
                    verify=False  # 注意：生产环境应该验证 SSL 证书
                ) as response:
                    response.raise_for_status()
                    
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                # 处理数据行
                                try:
                                    line_data = json.loads(line_str[6:])  # 去除 'data: ' 前缀
                                    if 'choices' in line_data and line_data['choices']:
                                        choice = line_data['choices'][0]
                                        if 'delta' in choice and 'content' in choice['delta']:
                                            chunk_text = choice['delta']['content']
                                            if chunk_text:
                                                full_content += chunk_text
                                                stream_callback(chunk_text)
                                except json.JSONDecodeError:
                                    # 忽略无效的 JSON
                                    pass
                
                return full_content
            else:
                # 非流式请求
                import logging
                logger = logging.getLogger('calibre_plugins.ask_grok.models.grok')
                
                logger.debug("开始Grok非流式请求")
                try:
                    # 记录请求详情，但隐藏敏感信息
                    api_url = f"{self.config['api_base_url']}/chat/completions"
                    logger.debug(f"请求URL: {api_url}")
                    
                    # 隐藏授权信息的请求头记录
                    safe_headers = {k: '***' if k.lower() == 'authorization' else v for k, v in headers.items()}
                    logger.debug(f"请求头: {json.dumps(safe_headers, ensure_ascii=False)}")
                    
                    # 记录请求数据
                    logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)[:500]}...")
                    
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 60),  # 增加超时时间
                        verify=False  # 注意：生产环境应该验证 SSL 证书
                    )
                    response.raise_for_status()
                    
                    logger.debug(f"Grok响应状态: {response.status_code}, 响应长度: {len(response.text)}")
                    
                    result = response.json()
                    
                    if 'choices' in result and result['choices'] and len(result['choices']) > 0:
                        if 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
                            content = result['choices'][0]['message']['content']
                            logger.debug(f"成功获取Grok响应内容，长度: {len(content)}")
                            return content
                    
                    # 如果响应格式不符合预期
                    error_msg = "无法从Grok API响应中提取内容"
                    logger.error(f"{error_msg}, 响应: {json.dumps(result, ensure_ascii=False)[:200]}...")
                    raise Exception(error_msg)
                except requests.exceptions.RequestException as req_e:
                    error_msg = f"Grok API请求失败: {str(req_e)}"
                    logger.error(error_msg)
                    if hasattr(req_e, 'response') and req_e.response is not None:
                        try:
                            error_detail = req_e.response.json()
                            logger.error(f"错误详情: {json.dumps(error_detail, ensure_ascii=False)}")
                        except:
                            logger.error(f"响应内容: {req_e.response.text[:500]}")
                    raise Exception(error_msg) from req_e
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f" | {json.dumps(error_detail, ensure_ascii=False)}"
                except:
                    error_msg += f" | {e.response.text}"
            raise Exception(error_msg) from e
    
    def supports_streaming(self) -> bool:
        """
        检查 Grok 模型是否支持流式传输
        
        :return: 始终返回 True，因为 Grok API 支持流式传输
        """
        return True
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Grok 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "auth_token": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
