"""
OpenAI (ChatGPT) AI Model Implementation

Uses the current Responses API (recommended over Chat Completions):
- POST /v1/responses
- Auth: Authorization: Bearer <api_key>
- System guidance: top-level `instructions`
- User prompt: top-level `input`
- Streaming events: response.output_text.delta
"""
import json
import time
import logging
from typing import Dict, Any, List

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.openai')


class OpenAIModel(BaseAIModel):
    """
    OpenAI (ChatGPT) AI Model Implementation Class

    Note: This provider uses the Responses API. Other OpenAI-compatible
    providers in this plugin continue to use /chat/completions.
    """
    # Default model name
    DEFAULT_MODEL = "gpt-5.4"
    # Default API base URL
    DEFAULT_API_BASE_URL = "https://api.openai.com/v1"

    def _validate_config(self):
        """
        Validate OpenAI model configuration

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
        super().validate_token()

        token = self.get_token()
        if len(token) < 20:
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
        Prepare OpenAI API request headers

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
        Prepare OpenAI Responses API request data

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

        data: Dict[str, Any] = {
            "model": kwargs.get('model') or self.config.get('model', self.DEFAULT_MODEL),
            "input": prompt,
            # Do not persist book Q&A on OpenAI servers by default
            "store": False,
        }

        if system_message and str(system_message).strip():
            data["instructions"] = system_message

        temperature = kwargs.get('temperature', 0.7)
        if temperature is not None:
            data["temperature"] = temperature

        max_tokens = kwargs.get('max_tokens')
        if max_tokens is not None:
            data["max_output_tokens"] = max_tokens

        if kwargs.get('stream', False):
            data['stream'] = True

        return data

    @staticmethod
    def extract_text_from_response(result: Dict[str, Any]) -> str:
        """
        Extract assistant text from a Responses API payload.

        :param result: Parsed JSON response
        :return: Output text
        """
        if not isinstance(result, dict):
            return ''

        output_text = result.get('output_text')
        if isinstance(output_text, str) and output_text:
            return output_text

        texts: List[str] = []
        for item in result.get('output') or []:
            if not isinstance(item, dict):
                continue
            if item.get('type') != 'message':
                continue
            for part in item.get('content') or []:
                if not isinstance(part, dict):
                    continue
                if part.get('type') in ('output_text', 'text') and part.get('text'):
                    texts.append(part['text'])
        return ''.join(texts)

    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to OpenAI Responses API and get response

        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, stream_callback, etc.
        :return: AI model response text
        :raises Exception: When request fails
        """
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)

        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)

        api_base_url = kwargs.get('api_base_url') or self.config.get(
            'api_base_url', self.DEFAULT_API_BASE_URL
        )
        api_url = self.build_api_url(api_base_url, '/responses')

        try:
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()

                with requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=kwargs.get('timeout', 300),
                    stream=True,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        line_str = line.decode('utf-8')
                        if not line_str.startswith('data: '):
                            continue

                        payload = line_str[6:].strip()
                        if payload == '[DONE]':
                            break

                        try:
                            event = json.loads(payload)
                        except json.JSONDecodeError as je:
                            logger.error(
                                f"JSON parse error: {str(je)}, line content: {line_str[:50]}..."
                            )
                            continue

                        event_type = event.get('type')
                        if event_type == 'response.output_text.delta':
                            chunk_text = event.get('delta') or ''
                            if chunk_text:
                                full_content += chunk_text
                                stream_callback(chunk_text)
                                chunk_count += 1
                                last_chunk_time = time.time()
                        elif event_type == 'response.completed':
                            # Prefer final assembled text when provided
                            completed = event.get('response') or {}
                            final_text = self.extract_text_from_response(completed)
                            if final_text and not full_content:
                                full_content = final_text
                                stream_callback(final_text)
                            break
                        elif event_type == 'error':
                            message = (event.get('error') or {}).get(
                                'message', 'Unknown streaming error'
                            )
                            raise Exception(message)

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

            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 60),
            )
            response.raise_for_status()

            result = response.json()
            content = self.extract_text_from_response(result)
            if content:
                return content

            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get('invalid_response', 'Invalid API response format')
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'api_request_failed',
                'API request failed: {error}',
            ).format(error=str(e))
            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.json()
                    message = (detail.get('error') or {}).get('message')
                    if message:
                        error_msg = f"{error_msg} | {message}"
                except Exception:
                    pass
            raise Exception(error_msg) from e

    def send_message(self, prompt: str, callback: callable) -> None:
        """
        Send message and stream response via callback

        :param prompt: Prompt text
        :param callback: Callback function to receive streaming text
        """
        try:
            self.ask(prompt, stream=True, stream_callback=callback)
        except Exception as e:
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

    def supports_streaming(self) -> bool:
        """
        Check if model supports streaming

        :return: True if streaming is supported
        """
        return True

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get OpenAI model default configuration

        :return: Default configuration dictionary
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    def verify_api_key_with_test_request(self) -> None:
        """
        Verify API key against Responses API (not Chat Completions).
        """
        provider_name = self.get_provider_name()
        timeout_seconds = 15

        try:
            headers = self.prepare_headers()
            api_base_url = self.config.get('api_base_url', self.DEFAULT_API_BASE_URL)
            test_url = self.build_api_url(api_base_url, '/responses')
            test_data = self.prepare_request_data("hi", max_tokens=16, stream=False)

            logger.info(f"[{provider_name}] 发送测试请求验证 API Key: {test_url}")

            response = requests.post(
                test_url,
                headers=headers,
                json=test_data,
                timeout=timeout_seconds,
            )

            logger.info(f"[{provider_name}] 测试请求响应状态码: {response.status_code}")
            logger.debug(f"[{provider_name}] 测试请求响应内容: {response.text[:200]}")

            if response.status_code == 401:
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get(
                    'error_401',
                    'API Key authentication failed. Please check: API Key is correct, '
                    'account has sufficient balance, API Key has not expired.',
                )
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(
                    f"{error_msg}\n\n{tech_details}: HTTP 401 - Invalid API Key"
                )

            if response.status_code == 404:
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get(
                    'error_404',
                    'API endpoint not found. Please check if the API Base URL configuration is correct.',
                )
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(
                    f"{error_msg}\n\n{tech_details}: HTTP 404 - This may indicate an invalid API Key or insufficient permissions."
                )

            if response.status_code in [200, 400, 422]:
                logger.info(
                    f"[{provider_name}] API Key 验证成功 - 状态码: {response.status_code}"
                )
            else:
                logger.warning(
                    f"[{provider_name}] 收到未预期的状态码: {response.status_code}"
                )

        except requests.exceptions.Timeout as e:
            logger.error(f"[{provider_name}] API Key 验证请求超时: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'error_network',
                'Network connection failed. Please check network connection, '
                'proxy settings, or firewall configuration.',
            )
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(
                f"{error_msg}\n\n{tech_details}: Timeout after {timeout_seconds} seconds"
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"[{provider_name}] API Key 验证请求失败: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code in [401, 403]:
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get(
                        'error_401',
                        'API Key authentication failed. Please check: API Key is correct, '
                        'account has sufficient balance, API Key has not expired.',
                    )
                    tech_details = translations.get('technical_details', 'Technical Details')
                    raise Exception(f"{error_msg}\n\n{tech_details}: {str(e)}")
            logger.info(f"[{provider_name}] API Key 验证通过（收到非401/403响应）")

    # Models list still uses GET /v1/models (OpenAI-compatible, covered by BaseAIModel)
