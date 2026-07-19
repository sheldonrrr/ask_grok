"""
Anthropic (Claude) AI Model Implementation

Uses the Messages API:
- POST /v1/messages
- Headers: x-api-key + anthropic-version: 2023-06-01
- System prompt via top-level `system`
- Opus 4.7+ reject temperature/top_p/top_k
"""
import json
import re
import time
import logging
from typing import Dict, Any, List

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.anthropic')


class AnthropicModel(BaseAIModel):
    """
    Anthropic (Claude) AI Model Implementation Class
    """
    # Default model name
    DEFAULT_MODEL = "claude-opus-4-8"
    # Default API base URL
    DEFAULT_API_BASE_URL = "https://api.anthropic.com/v1"
    # Required Anthropic API version (still current)
    ANTHROPIC_VERSION = "2023-06-01"

    def _validate_config(self):
        """
        Validate Anthropic model configuration

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
        Get Anthropic model API Key/Token

        :return: API Key/Token string
        """
        return self.config.get('api_key', '')

    def validate_token(self) -> bool:
        """
        Validate if Anthropic model token is valid

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
        Prepare Anthropic API request headers

        :return: Request headers dictionary
        """
        return {
            "Content-Type": "application/json",
            "x-api-key": self.get_token(),
            "anthropic-version": self.ANTHROPIC_VERSION,
        }

    @staticmethod
    def supports_sampling_params(model_name: str) -> bool:
        """
        Claude Opus 4.7+ reject temperature/top_p/top_k (400 if set).

        :param model_name: Model id
        :return: True if sampling params are allowed
        """
        name = (model_name or '').lower()
        match = re.search(r'claude-opus-4(?:\.|-)(\d+)', name)
        if match and int(match.group(1)) >= 7:
            return False
        # Also cover aliases like claude-opus-4-7 / claude-opus-4-8 without regex miss
        if 'opus-4-7' in name or 'opus-4-8' in name or 'opus-4.7' in name or 'opus-4.8' in name:
            return False
        return True

    @staticmethod
    def extract_text_from_content(content_blocks: Any) -> str:
        """
        Extract assistant text from Messages API content blocks.

        :param content_blocks: Response content array or string
        :return: Concatenated text
        """
        if isinstance(content_blocks, str):
            return content_blocks

        if not isinstance(content_blocks, list):
            return ''

        texts: List[str] = []
        for block in content_blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get('type')
            if block_type == 'text' and block.get('text'):
                texts.append(block['text'])
            elif block_type == 'thinking' and block.get('thinking'):
                # Keep thinking visible for book-analysis debugging when returned
                texts.append(f"<think>{block['thinking']}</think>\n\n")
        return ''.join(texts)

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Prepare Anthropic Messages API request data

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

        model_name = kwargs.get('model') or self.config.get('model', self.DEFAULT_MODEL)

        data: Dict[str, Any] = {
            "model": model_name,
            "max_tokens": kwargs.get('max_tokens', 4096),
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        if system_message and str(system_message).strip():
            data['system'] = system_message

        # Only include sampling params on models that still accept them
        if self.supports_sampling_params(model_name):
            data['temperature'] = kwargs.get('temperature', 0.7)
            if kwargs.get('top_p') is not None:
                data['top_p'] = kwargs.get('top_p')
            if kwargs.get('top_k') is not None:
                data['top_k'] = kwargs.get('top_k')

        if kwargs.get('stream', False):
            data['stream'] = True

        return data

    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Anthropic Messages API and get response

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
        api_url = self.build_api_url(api_base_url, '/messages')

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

                        try:
                            line_data = json.loads(line_str[6:])
                            event_type = line_data.get('type')

                            if event_type == 'content_block_delta':
                                delta = line_data.get('delta') or {}
                                delta_type = delta.get('type')
                                chunk_text = ''
                                if delta_type == 'text_delta':
                                    chunk_text = delta.get('text', '')
                                elif delta_type == 'thinking_delta':
                                    chunk_text = delta.get('thinking', '')
                                if chunk_text:
                                    full_content += chunk_text
                                    stream_callback(chunk_text)
                                    chunk_count += 1
                                    last_chunk_time = time.time()
                            elif event_type == 'message_stop':
                                break
                            elif event_type == 'error':
                                error_msg = (line_data.get('error') or {}).get(
                                    'message', 'Unknown streaming error'
                                )
                                raise Exception(error_msg)
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

            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 60),
            )
            response.raise_for_status()

            result = response.json()
            content = self.extract_text_from_content(result.get('content'))
            if content:
                return content

            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get('invalid_response', 'Invalid API response format')
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Anthropic API request error: {str(e)}")
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'api_request_failed',
                'API request failed: {error}',
            ).format(error=str(e))
            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.json()
                    message = (detail.get('error') or {}).get('message') or detail.get(
                        'message'
                    )
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
        return "Anthropic (Claude)"

    def supports_streaming(self) -> bool:
        """
        Check if model supports streaming

        :return: True if streaming is supported
        """
        return True

    def prepare_models_request_headers(self) -> Dict[str, str]:
        """
        Prepare headers for GET /v1/models (no Content-Type on GET)

        :return: Request headers dictionary
        """
        return {
            'x-api-key': self.config.get('api_key', ''),
            'anthropic-version': self.ANTHROPIC_VERSION,
        }

    def parse_models_response(self, data: Dict[str, Any]) -> list:
        """
        Parse Anthropic /v1/models response ({"data":[{"id": "..."}]})

        :param data: API response JSON
        :return: Model id list
        """
        models = []
        for model in data.get('data', []):
            model_id = model.get('id')
            if model_id:
                models.append(model_id)
        return models

    def verify_api_key_with_test_request(self) -> None:
        """
        Verify API key with a minimal Messages request
        """
        provider_name = self.get_provider_name()
        timeout_seconds = 15

        try:
            headers = self.prepare_headers()
            api_base_url = self.config.get('api_base_url', self.DEFAULT_API_BASE_URL)
            test_url = self.build_api_url(api_base_url, '/messages')
            model_name = self.config.get('model', self.DEFAULT_MODEL)

            test_data = {
                "model": model_name,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 1,
            }

            logger.info(f"[{provider_name}] 发送测试请求验证 API Key: {test_url}")

            response = requests.post(
                test_url,
                headers=headers,
                json=test_data,
                timeout=timeout_seconds,
            )

            logger.info(f"[{provider_name}] 测试请求响应状态码: {response.status_code}")
            logger.debug(f"[{provider_name}] 测试请求响应内容: {response.text[:200]}")

            if response.status_code in (401, 403):
                logger.error(f"[{provider_name}] API Key 无效 - {response.status_code}")
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get(
                    'error_401',
                    'API Key authentication failed. Please check: API Key is correct, '
                    'account has sufficient balance, API Key has not expired.',
                )
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(
                    f"{error_msg}\n\n{tech_details}: HTTP {response.status_code} - Invalid API Key"
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
