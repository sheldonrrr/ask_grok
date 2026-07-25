"""
Mistral AI Model Implementation

Mistral API is OpenAI Chat Completions compatible.
Base URL: https://api.mistral.ai/v1
"""
import json
import time
import logging
from typing import Dict, Any

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation


class MistralModel(BaseAIModel):
    """
    Mistral AI Model Implementation Class
    """
    # Default model name
    DEFAULT_MODEL = "mistral-large-latest"
    # Default API base URL
    DEFAULT_API_BASE_URL = "https://api.mistral.ai/v1"

    def _validate_config(self):
        """
        Validate Mistral model configuration

        :raises ValueError: When configuration is invalid
        """
        required_keys = ['api_key', 'api_base_url']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(
                    translations.get(
                        'missing_required_config',
                        'Missing required configuration: {key}',
                    ).format(key=key)
                )

        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL

    def get_token(self) -> str:
        """
        Get Mistral API Key

        :return: API Key string
        """
        return self.config.get('api_key', '')

    def validate_token(self) -> bool:
        """
        Validate if Mistral API Key is present

        :return: True if token is valid
        :raises ValueError: When token is invalid
        """
        super().validate_token()

        token = self.get_token()
        if not token or token.strip() == '':
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(
                translations.get(
                    'api_key_empty',
                    'API Key is empty. Please enter a valid API Key.',
                )
            )

        if len(token.strip()) < 10:
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(
                translations.get(
                    'api_key_too_short',
                    'API Key is too short. Please check and enter the complete key.',
                )
            )

        return True

    def prepare_headers(self) -> Dict[str, str]:
        """
        Prepare Mistral API request headers

        :return: Request headers dictionary
        """
        token = self.get_token()

        if not token.startswith('Bearer '):
            token = f'Bearer {token}'

        return {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Prepare Mistral API request data

        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, etc.
        :return: Request data dictionary
        """
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get(
            'system_message',
            translations.get(
                'default_system_message',
                'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.',
            ),
        )

        data = {
            "model": self.config.get('model', self.DEFAULT_MODEL),
            "messages": [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4096),
        }

        if kwargs.get('stream', False):
            data['stream'] = True

        return data

    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Mistral API and get response

        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, stream_callback, etc.
        :return: AI model response text
        :raises Exception: When request fails
        """
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)

        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.mistral')

        try:
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
                                        logger.error(
                                            f"JSON parse error: {str(je)}, line content: {line_str[:50]}..."
                                        )
                                        continue

                                current_time = time.time()
                                if current_time - last_chunk_time > 15:
                                    logger.warning(
                                        f"No new data received for {current_time - last_chunk_time:.1f} seconds"
                                    )

                                if current_time - last_chunk_time > 60 and full_content:
                                    logger.warning(
                                        "No response for over 60 seconds, triggering recovery mechanism"
                                    )
                                    translations = get_translation(
                                        self.config.get('language', 'en')
                                    )
                                    raise requests.exceptions.ReadTimeout(
                                        translations.get(
                                            'stream_timeout_error',
                                            "Streaming timeout after 60 seconds with no new content, possible connection issue",
                                        )
                                    )

                        logger.info(
                            f"Streaming completed, received {chunk_count} chunks, total length: {len(full_content)}"
                        )
                        return full_content

                except requests.exceptions.RequestException as e:
                    logger.error(f"Mistral API request error: {str(e)}")
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(
                        translations.get(
                            'api_request_failed',
                            'API request failed: {error}',
                        ).format(error=str(e))
                    )

            else:
                api_url = f"{self.config['api_base_url']}/chat/completions"
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 60),
                )
                response.raise_for_status()

                result = response.json()
                if 'choices' in result and result['choices']:
                    return result['choices'][0]['message']['content']
                else:
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(
                        translations.get(
                            'invalid_response',
                            'Invalid API response format',
                        )
                    )

        except requests.exceptions.RequestException as e:
            logger.error(f"Mistral API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'api_request_failed',
                    'API request failed: {error}',
                ).format(error=str(e))
            )

    def send_message(self, prompt: str, callback: callable) -> None:
        """
        Send message and stream response via callback

        :param prompt: Prompt text
        :param callback: Callback function to receive streaming text
        """
        try:
            self.ask(prompt, stream=True, stream_callback=callback)
        except Exception as e:
            logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.mistral')
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
        return "Mistral"

    def supports_streaming(self) -> bool:
        """
        Check if model supports streaming

        :return: True if streaming is supported
        """
        return True

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get Mistral model default configuration

        :return: Default configuration dictionary
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    # Mistral 使用基类的默认实现，无需重写 fetch_available_models
