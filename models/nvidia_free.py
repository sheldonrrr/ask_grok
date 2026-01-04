"""
Nvidia Free Proxy Model Implementation
使用免费代理服务器访问 Nvidia API
"""
import json
import time
import logging
from typing import Dict, Any, Optional

from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
from .nvidia import NvidiaModel
from .base import format_http_error
from ..i18n import get_translation
from ..device_fingerprint import DeviceFingerprint


class NvidiaFreeModel(NvidiaModel):
    """
    Nvidia 免费代理模型实现
    通过 Cloudflare Worker 代理访问 Nvidia API
    """
    DEFAULT_PROXY_URL = "https://nvidia-proxy.your-subdomain.workers.dev"
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化 Nvidia 免费代理模型
        
        :param config: 模型配置字典
        """
        self.logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.nvidia_free')
        
        if 'proxy_url' in config and config['proxy_url']:
            config['api_base_url'] = config['proxy_url']
        else:
            config['api_base_url'] = self.DEFAULT_PROXY_URL
        
        config['api_key'] = 'free-tier'
        
        if not config.get('model'):
            config['model'] = self.DEFAULT_MODEL
        
        super(NvidiaModel, self).__init__(config)
        
        self.logger.info("使用 Nvidia 免费代理模式")
    
    def _validate_config(self):
        """
        验证免费代理模式配置
        免费模式不需要 API Key
        """
        if not self.config.get('api_base_url'):
            self.config['api_base_url'] = self.DEFAULT_PROXY_URL
        
        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL
    
    def get_token(self) -> str:
        """
        免费模式不需要真实的 API Key
        
        :return: 固定返回 'free-tier'
        """
        return 'free-tier'
    
    def validate_token(self) -> bool:
        """
        免费代理模式不需要验证 token
        
        :return: 始终返回 True
        """
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备代理请求头
        不需要 Authorization，但需要添加客户端元数据
        
        :return: 请求头字典
        """
        metadata = DeviceFingerprint.get_client_metadata()
        
        headers = {
            "Content-Type": "application/json",
            "X-User-UUID": metadata['user_uuid'],
            "X-Device-Fingerprint": metadata['device_fingerprint'],
            "X-Client-Locale": metadata['device_info'].get('locale', 'en_US'),
            "X-Client-System": metadata['device_info'].get('system', 'unknown'),
            "X-Plugin-Version": metadata.get('plugin_version', 'unknown')
        }
        
        return headers
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        通过代理服务器发送请求
        
        :param prompt: 提示词
        :param kwargs: 其他参数
        :return: AI 响应文本
        """
        if 'stream' not in kwargs:
            kwargs['stream'] = self.config.get('enable_streaming', True)
        
        use_stream = kwargs['stream']
        stream_callback = kwargs.get('stream_callback', None)
        
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        try:
            api_url = f"{self.config['api_base_url']}/api/chat"
            
            self.logger.debug(f"发送请求到免费代理: {api_url}")
            
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                
                try:
                    with requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),
                        stream=True,
                        verify=True
                    ) as response:
                        response.raise_for_status()
                        
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    try:
                                        if line_str == 'data: [DONE]':
                                            break
                                        line_data = json.loads(line_str[6:])
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
                                        self.logger.error(f"JSON 解析错误: {str(je)}")
                                        continue
                                
                                current_time = time.time()
                                if current_time - last_chunk_time > 60 and full_content:
                                    self.logger.warning("超过 60 秒无响应，触发恢复机制")
                                    translations = get_translation(self.config.get('language', 'en'))
                                    raise requests.exceptions.ReadTimeout(
                                        translations.get('stream_timeout_error', 
                                            "流式传输超时，可能连接出现问题"))
                        
                        return full_content
                        
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"免费代理请求错误: {str(e)}")
                    error_msg = self._format_proxy_error(e)
                    raise Exception(error_msg)
            
            else:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),
                    verify=True
                )
                
                response.raise_for_status()
                
                try:
                    result = response.json()
                    
                    if 'choices' in result and result['choices']:
                        content = result['choices'][0]['message']['content']
                        return content
                    else:
                        translations = get_translation(self.config.get('language', 'en'))
                        raise Exception(translations.get('invalid_response', 
                            '无效的 API 响应格式'))
                except json.JSONDecodeError as je:
                    self.logger.error(f"JSON 解析失败: {str(je)}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('json_parse_error', 
                        f'无法解析 API 响应: {str(je)}'))
                    
        except requests.exceptions.RequestException as e:
            self.logger.error(f"代理请求失败: {str(e)}")
            error_msg = self._format_proxy_error(e)
            raise Exception(error_msg)
    
    def _format_proxy_error(self, error: Exception) -> str:
        """
        格式化代理错误信息
        
        :param error: 异常对象
        :return: 格式化后的错误信息
        """
        translations = get_translation(self.config.get('language', 'en'))
        
        if hasattr(error, 'response') and error.response is not None:
            status_code = error.response.status_code
            
            if status_code == 429:
                return translations.get('free_tier_rate_limit', 
                    '免费通道请求频率超限。请稍后再试或配置自己的 Nvidia API Key。')
            elif status_code == 503:
                return translations.get('free_tier_unavailable', 
                    '免费通道暂时不可用。请稍后再试或配置自己的 Nvidia API Key。')
            elif status_code >= 500:
                return translations.get('free_tier_server_error', 
                    '免费通道服务器错误。请稍后再试。')
            else:
                try:
                    error_data = error.response.json()
                    if 'error' in error_data:
                        return f"{translations.get('free_tier_error', '免费通道错误')}: {error_data['error']}"
                except:
                    pass
        
        return format_http_error(error, self.config.get('language', 'en'))
    
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        return "Nvidia AI（免费）"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "proxy_url": cls.DEFAULT_PROXY_URL,
            "api_key": "free-tier",
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }
    
    def fetch_available_models(self, skip_verification=False):
        """
        免费通道不支持获取模型列表
        返回预定义的模型列表
        """
        return [
            "meta/llama-3.3-70b-instruct",
            "meta/llama-3.1-405b-instruct",
            "nvidia/llama-3.1-nemotron-70b-instruct",
        ]
    
    def verify_api_key_with_test_request(self):
        """
        免费通道不需要验证 API Key
        但可以测试代理服务器是否可用
        """
        try:
            api_url = f"{self.config['api_base_url']}/api/health"
            response = requests.get(api_url, timeout=10, verify=True)
            
            if response.status_code == 200:
                self.logger.info("免费代理服务器连接正常")
                return True
            else:
                translations = get_translation(self.config.get('language', 'en'))
                raise Exception(translations.get('free_tier_unavailable', 
                    '免费通道暂时不可用'))
        except Exception as e:
            self.logger.error(f"免费代理服务器连接失败: {str(e)}")
            raise
