"""
OpenAI AI Model Implementation
"""
import json
import requests
import time
import logging
from typing import Dict, Any, Optional

from .base import BaseAIModel
from ..i18n import get_translation


class OpenAIModel(BaseAIModel):
    """
    OpenAI AI Model Implementation Class
    Supports GPT-4, GPT-3.5, and other OpenAI models
    """
    # Default model name
    DEFAULT_MODEL = "gpt-4o-mini"
    # Default API base URL
    DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
    
    def _validate_config(self):
        """
        Validate OpenAI model configuration
        
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
        Get OpenAI model API Key/Token
        
        :return: API Key/Token string
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        Validate if OpenAI model token is valid
        
        :return: True if token is valid
        :raises ValueError: When token is invalid
        """
        # First call base class basic validation
        super().validate_token()
        
        token = self.get_token()
        
        # OpenAI API Key format validation: basic length check
        if len(token) < 20:
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_too_short', 'API Key is too short. Please check and enter the complete key.'))
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        Prepare OpenAI API request headers
        
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
        Prepare OpenAI API request data
        
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
        
        # Add streaming support
        if kwargs.get('stream', self.config.get('enable_streaming', True)):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to OpenAI API and get response
        
        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, stream_callback, etc.
        :return: AI model response text
        :raises Exception: When request fails
        """
        # Prepare request headers and data
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # Check if using streaming
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        
        try:
            # If using streaming
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                logger = logging.getLogger('calibre_plugins.ask_grok.models.openai')
                
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
                    logger.error(f"OpenAI API request error: {str(e)}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(translations.get('api_request_error', f'API request failed: {str(e)}'))
            
            # Non-streaming mode
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
            logger = logging.getLogger('calibre_plugins.ask_grok.models.openai')
            logger.error(f"OpenAI API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(translations.get('api_request_error', f'API request failed: {str(e)}'))
    
    def send_message(self, prompt: str, callback: callable) -> None:
        """
        Send message and stream response via callback
        
        :param prompt: Prompt text
        :param callback: Callback function to receive streaming text
        """
        try:
            self.ask(prompt, stream=True, stream_callback=callback)
        except Exception as e:
            logger = logging.getLogger('calibre_plugins.ask_grok.models.openai')
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
        return "OpenAI"
    
    # OpenAI 使用基类的默认实现，无需重写 fetch_available_models
    # 基类已经提供了完整的 OpenAI 兼容实现
