"""
SpaceXAI (Grok) AI Model Implementation

SpaceXAI (formerly branded as xAI) keeps the same API host:
- Base URL: https://api.x.ai/v1
- Preferred: Responses API POST /v1/responses
- Auth: Authorization: Bearer <api_key>
- Config field remains `auth_token` for backward compatibility
"""
import json
import time
import logging
from typing import Dict, Any, List

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.grok')


class GrokModel(BaseAIModel):
    """
    SpaceXAI (Grok) AI Model Implementation Class
    """
    # Default model name (SpaceXAI flagship)
    DEFAULT_MODEL = "grok-4.5"
    # Default API base URL (unchanged host)
    DEFAULT_API_BASE_URL = "https://api.x.ai/v1"

    def _validate_config(self):
        """
        Validate Grok model configuration

        :raises ValueError: When configuration is invalid
        """
        required_keys = ['auth_token', 'api_base_url']
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
        Get SpaceXAI / Grok API Key/Token

        :return: API Key/Token string
        """
        return self.config.get('auth_token', '')

    def validate_token(self) -> bool:
        """
        Validate if Grok API token is valid

        :return: True if token is valid
        :raises ValueError: When token is invalid
        """
        super().validate_token()

        token = self.get_token()
        if len(token) < 10:
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
        Prepare SpaceXAI API request headers

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
        Prepare SpaceXAI Responses API request data

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
            # Prefer sticky prompt-cache routing for multi-turn sessions when available
            "store": False,
        }

        if system_message and str(system_message).strip():
            data["instructions"] = system_message

        # Optional cache key helps SpaceXAI sticky-route conversations
        prompt_cache_key = kwargs.get('prompt_cache_key') or self.config.get('prompt_cache_key')
        if prompt_cache_key:
            data['prompt_cache_key'] = prompt_cache_key

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
        Send prompt to SpaceXAI Responses API and get response

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
                                f"JSON解析错误: {str(je)}, 行内容: {line_str[:50]}..."
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
                                f"已经 {current_time - last_chunk_time:.1f} 秒没有收到新数据"
                            )

                        if current_time - last_chunk_time > 60 and full_content:
                            logger.warning("超过60秒无响应，主动触发恢复机制")
                            translations = get_translation(
                                self.config.get('language', 'en')
                            )
                            raise requests.exceptions.ReadTimeout(
                                translations.get(
                                    'stream_timeout_error',
                                    "流式传输超过60秒没有新内容，可能是连接问题",
                                )
                            )

                logger.info(
                    f"流式请求完成, 接收 {chunk_count} 块, 总长度: {len(full_content)}"
                )
                return full_content

            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 300),
            )
            response.raise_for_status()

            result = response.json()
            content = self.extract_text_from_response(result)
            if content:
                return content

            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'api_content_extraction_failed',
                    'Unable to extract content from Grok API response',
                )
            )

        except requests.exceptions.RequestException as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'api_request_failed',
                'API request failed: {error}',
            ).format(error=str(e))
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    message = (error_detail.get('error') or {}).get('message')
                    if message:
                        error_msg = f"{error_msg} | {message}"
                    else:
                        error_msg += f" | {json.dumps(error_detail, ensure_ascii=False)}"
                except Exception:
                    error_msg += f" | {getattr(e.response, 'text', '')}"
            raise Exception(error_msg) from e

    def supports_streaming(self) -> bool:
        """
        Check if Grok model supports streaming

        :return: Always True
        """
        return True

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
        return "SpaceXAI (Grok)"

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get Grok model default configuration

        :return: Default configuration dictionary
        """
        return {
            "auth_token": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    def prepare_models_request_headers(self) -> Dict[str, str]:
        """
        Models list uses Bearer auth via auth_token (not api_key).
        """
        return self.prepare_headers()

    def verify_api_key_with_test_request(self) -> None:
        """
        Verify API key against Responses API.
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

            if response.status_code in (401, 403):
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
