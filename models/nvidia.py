"""
Nvidia AI Model Implementation
"""
import json
import requests
import time
import logging
from typing import Dict, Any, Optional

from .base import BaseAIModel
from ..i18n import get_translation


class NvidiaModel(BaseAIModel):
    """
    Nvidia AI Model Implementation Class
    Supports Llama, DeepSeek-R1, Qwen, and other models available on Nvidia AI
    Note: Free tier available with 40 RPM rate limit
    """
    # Default model name
    DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"
    # Default API base URL
    DEFAULT_API_BASE_URL = "https://integrate.api.nvidia.com/v1"
    
    def _validate_config(self):
        """
        Validate Nvidia model configuration
        
        :raises ValueError: When configuration is invalid
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
        Get Nvidia model API Key/Token
        
        :return: API Key/Token string
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        Validate if Nvidia model token is valid
        
        :return: True if token is valid
        :raises ValueError: When token is invalid
        """
        # First call base class basic validation
        super().validate_token()
        
        token = self.get_token()
        
        # Nvidia API Key format validation: basic length check
        if len(token) < 10:
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_too_short', 'API Key is too short. Please check and enter the complete key.'))
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        Prepare Nvidia API request headers
        Note: Nvidia uses OpenAI-compatible format with Bearer token
        
        :return: Request headers dictionary
        """
        token = self.get_token()
        
        # Ensure token has Bearer prefix
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
            
        return {
            "Content-Type": "application/json",
            "Authorization": token
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Prepare Nvidia API request data
        Note: Nvidia uses OpenAI-compatible format
        
        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, etc.
        :return: Request data dictionary
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
        
        # Add streaming support if enabled
        # The stream parameter should already be set by ask() method
        if kwargs.get('stream', False):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Nvidia API and get response
        
        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, stream_callback, etc.
        :return: AI model response text
        :raises Exception: When request fails
        """
        # Check if using streaming - respect explicit stream parameter if provided
        # Only use config default if stream is not explicitly set
        if 'stream' not in kwargs:
            kwargs['stream'] = self.config.get('enable_streaming', True)
        
        use_stream = kwargs['stream']
        stream_callback = kwargs.get('stream_callback', None)
        
        # Prepare request headers and data
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        try:
            # If using streaming
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.nvidia')
                
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
                                    # Handle data line
                                    try:
                                        if line_str == 'data: [DONE]':
                                            break
                                        line_data = json.loads(line_str[6:])  # Remove 'data: ' prefix
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
                                    
                                # Check if no new data received for 15 seconds
                                current_time = time.time()
                                if current_time - last_chunk_time > 15:
                                    logger.warning(f"No new data received for {current_time - last_chunk_time:.1f} seconds")
                                
                                # If no new data for 60 seconds, try to recover connection
                                if current_time - last_chunk_time > 60 and full_content:
                                    logger.warning("No response for over 60 seconds, triggering recovery mechanism")
                                    translations = get_translation(self.config.get('language', 'en'))
                                    raise requests.exceptions.ReadTimeout(translations.get('stream_timeout_error', "Streaming timeout after 60 seconds with no new content, possible connection issue"))
                        
                        logger.info(f"Streaming completed, received {chunk_count} chunks, total length: {len(full_content)}")
                        return full_content
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Nvidia API request error: {str(e)}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e)))
            
            # Non-streaming mode
            else:
                logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.nvidia')
                api_url = f"{self.config['api_base_url']}/chat/completions"
                
                logger.debug(f"Non-streaming request to: {api_url}")
                logger.debug(f"Request data: {json.dumps({k: v for k, v in data.items() if k != 'messages'}, ensure_ascii=False)}")
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),
                    verify=False
                )
                response.raise_for_status()
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                
                try:
                    result = response.json()
                    logger.debug(f"Response JSON parsed successfully")
                    
                    if 'choices' in result and result['choices']:
                        content = result['choices'][0]['message']['content']
                        logger.debug(f"Response content length: {len(content)}")
                        return content
                    else:
                        translations = get_translation(self.config.get('language', 'en'))
                        logger.error(f"Invalid response format: {json.dumps(result, ensure_ascii=False)[:200]}")
                        raise Exception(translations.get('invalid_response', 'Invalid API response format'))
                except json.JSONDecodeError as je:
                    logger.error(f"Failed to parse JSON response: {str(je)}")
                    logger.error(f"Response text: {response.text[:500]}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('json_parse_error', f'Failed to parse API response: {str(je)}'))
                    
        except requests.exceptions.RequestException as e:
            logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.nvidia')
            logger.error(f"Nvidia API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e)))
    
    def send_message(self, prompt: str, callback: callable) -> None:
        """
        Send message and stream response via callback
        
        :param prompt: Prompt text
        :param callback: Callback function to receive streaming text
        """
        try:
            self.ask(prompt, stream=True, stream_callback=callback)
        except Exception as e:
            logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.nvidia')
            logger.error(f"send_message error: {str(e)}")
            raise
    
    def stop_stream(self) -> None:
        """
        Stop streaming response
        Note: Current implementation does not support mid-stream interruption
        """
        pass
    
    def get_model_name(self) -> str:
        """
        Get current model name
        
        :return: Model name string
        """
        return self.config.get('model', self.DEFAULT_MODEL)
    
    def get_provider_name(self) -> str:
        """
        Get provider name
        
        :return: Provider name string
        """
        return "Nvidia AI"
    
    def supports_streaming(self) -> bool:
        """
        Check if Nvidia model supports streaming
        
        :return: Always returns True, as Nvidia API supports streaming
        """
        return True
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get default configuration for Nvidia model
        
        :return: Default configuration dictionary
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # Enable streaming by default
        }
    
    # Nvidia 使用基类的默认实现（OpenAI 兼容格式），无需重写 fetch_available_models
