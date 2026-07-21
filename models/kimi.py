"""
Kimi (Moonshot) AI Model Implementation

Kimi API is OpenAI Chat Completions compatible.
Base URL (global): https://api.moonshot.ai/v1
Base URL (China):  https://api.moonshot.cn/v1

API keys are region-bound: a China-platform key only works with .cn,
and a global-platform key only works with .ai.
"""
import json
import time
import logging
from typing import Dict, Any, List, Optional

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation


class KimiModel(BaseAIModel):
    """
    Kimi (Moonshot) AI Model Implementation Class
    """
    # Default model name
    DEFAULT_MODEL = "kimi-k3"
    # Default API base URL (global; China keys may use https://api.moonshot.cn/v1)
    DEFAULT_API_BASE_URL = "https://api.moonshot.ai/v1"
    GLOBAL_API_BASE_URL = "https://api.moonshot.ai/v1"
    CHINA_API_BASE_URL = "https://api.moonshot.cn/v1"
    REGION_GLOBAL = "global"
    REGION_CHINA = "china"

    @classmethod
    def base_url_for_region(cls, region: str) -> str:
        """Map region id to Moonshot API base URL."""
        if region == cls.REGION_CHINA:
            return cls.CHINA_API_BASE_URL
        return cls.GLOBAL_API_BASE_URL

    @classmethod
    def region_from_base_url(cls, api_base_url: str) -> str:
        """Infer region id from API base URL (defaults to global)."""
        current = (api_base_url or "").rstrip("/").lower()
        china = cls.CHINA_API_BASE_URL.rstrip("/").lower()
        if current == china or current == "https://api.moonshot.cn":
            return cls.REGION_CHINA
        return cls.REGION_GLOBAL

    @classmethod
    def peer_base_url(cls, api_base_url: str) -> Optional[str]:
        """Return the other regional Moonshot endpoint, if applicable."""
        current = (api_base_url or "").rstrip("/")
        global_url = cls.GLOBAL_API_BASE_URL.rstrip("/")
        china_url = cls.CHINA_API_BASE_URL.rstrip("/")
        if current == global_url:
            return cls.CHINA_API_BASE_URL
        if current == china_url:
            return cls.GLOBAL_API_BASE_URL
        # Tolerate missing /v1 suffix
        if current in ("https://api.moonshot.ai",):
            return cls.CHINA_API_BASE_URL
        if current in ("https://api.moonshot.cn",):
            return cls.GLOBAL_API_BASE_URL
        return None

    def _switch_to_peer_base_url(self) -> Optional[str]:
        current = self.config.get("api_base_url", self.DEFAULT_API_BASE_URL)
        peer = self.peer_base_url(current)
        if not peer:
            return None
        logger = logging.getLogger(self.get_logger_name())
        logger.warning(
            "Kimi auth failed for %s; retrying with regional peer %s",
            current,
            peer,
        )
        self.config["api_base_url"] = peer
        self.config["kimi_region"] = self.region_from_base_url(peer)
        return peer

    @staticmethod
    def _is_auth_failure(error: Exception) -> bool:
        text = str(error).lower()
        if "401" in text or "invalid authentication" in text or "invalid_authentication" in text:
            return True
        response = getattr(error, "response", None)
        return bool(response is not None and getattr(response, "status_code", None) == 401)

    def fetch_available_models(self, skip_verification: bool = False) -> List[str]:
        """Fetch models, auto-falling back between .ai and .cn on 401."""
        try:
            return super().fetch_available_models(skip_verification=skip_verification)
        except Exception as e:
            if not self._is_auth_failure(e) or not self._switch_to_peer_base_url():
                raise
            return super().fetch_available_models(skip_verification=skip_verification)

    def verify_api_key_with_test_request(self) -> None:
        """Verify API key, auto-falling back between .ai and .cn on 401."""
        try:
            super().verify_api_key_with_test_request()
        except Exception as e:
            if not self._is_auth_failure(e) or not self._switch_to_peer_base_url():
                raise
            super().verify_api_key_with_test_request()

    def _validate_config(self):
        """
        Validate Kimi model configuration

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
        Get Kimi API Key

        :return: API Key string
        """
        return self.config.get('api_key', '')

    def validate_token(self) -> bool:
        """
        Validate if Kimi API Key is present

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
        Prepare Kimi API request headers

        :return: Request headers dictionary
        """
        token = self.get_token()

        if not token.startswith('Bearer '):
            token = f'Bearer {token}'

        return {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    @classmethod
    def _model_requires_fixed_temperature(cls, model_name: str) -> bool:
        """
        Newer Kimi thinking models (kimi-k*) reject temperature values other than 1.
        Classic moonshot-v1-* models still accept the usual 0-1 range.
        """
        name = (model_name or "").strip().lower()
        return name.startswith("kimi-k")

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Prepare Kimi API request data

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

        model_name = self.config.get('model', self.DEFAULT_MODEL)
        data = {
            "model": model_name,
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
            "max_tokens": kwargs.get('max_tokens', 4096),
        }

        # kimi-k3 / kimi-k2.5+ only allow temperature=1 (or omit). Sending 0.7 -> HTTP 400.
        if self._model_requires_fixed_temperature(model_name):
            if kwargs.get('temperature') is not None:
                data['temperature'] = 1.0
        else:
            data['temperature'] = kwargs.get('temperature', 0.7)

        if kwargs.get('stream', False):
            data['stream'] = True

        return data

    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send prompt to Kimi API and get response

        :param prompt: Prompt text
        :param kwargs: Other parameters like temperature, stream, stream_callback, etc.
        :return: AI model response text
        :raises Exception: When request fails
        """
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.kimi')

        def _raise_request_failed(err: Exception) -> None:
            detail = str(err)
            response = getattr(err, "response", None)
            if response is not None:
                try:
                    body = (response.text or "").strip()
                    if body:
                        detail = f"{detail} | {body[:500]}"
                        logger.error("Kimi API error body: %s", body[:500])
                except Exception:
                    pass
            logger.error(f"Kimi API request error: {detail}")
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'api_request_failed',
                    'API request failed: {error}',
                ).format(error=detail)
            )

        def _do_stream_request() -> str:
            full_content = ""
            chunk_count = 0
            last_chunk_time = time.time()
            api_url = f"{self.config['api_base_url']}/chat/completions"
            # Refresh headers/data in case base URL or model config changed
            req_headers = self.prepare_headers()
            req_data = self.prepare_request_data(prompt, **kwargs)

            with requests.post(
                api_url,
                headers=req_headers,
                json=req_data,
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

        def _do_non_stream_request() -> str:
            api_url = f"{self.config['api_base_url']}/chat/completions"
            req_headers = self.prepare_headers()
            req_data = self.prepare_request_data(prompt, **kwargs)
            response = requests.post(
                api_url,
                headers=req_headers,
                json=req_data,
                timeout=kwargs.get('timeout', 60),
            )
            response.raise_for_status()

            result = response.json()
            if 'choices' in result and result['choices']:
                message = result['choices'][0].get('message') or {}
                content = message.get('content')
                if content:
                    return content
                # Thinking models may briefly return empty content with reasoning_content
                reasoning = message.get('reasoning_content')
                if reasoning:
                    logger.warning(
                        "Kimi returned empty content with reasoning_content "
                        "(len=%s); returning empty string",
                        len(reasoning),
                    )
                    return ""
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'invalid_response',
                    'Invalid API response format',
                )
            )

        try:
            if use_stream and stream_callback:
                try:
                    return _do_stream_request()
                except requests.exceptions.HTTPError as e:
                    if self._is_auth_failure(e) and self._switch_to_peer_base_url():
                        return _do_stream_request()
                    _raise_request_failed(e)
                except requests.exceptions.RequestException as e:
                    _raise_request_failed(e)
            else:
                try:
                    return _do_non_stream_request()
                except requests.exceptions.HTTPError as e:
                    if self._is_auth_failure(e) and self._switch_to_peer_base_url():
                        return _do_non_stream_request()
                    _raise_request_failed(e)

        except requests.exceptions.RequestException as e:
            _raise_request_failed(e)

    def send_message(self, prompt: str, callback: callable) -> None:
        """
        Send message and stream response via callback

        :param prompt: Prompt text
        :param callback: Callback function to receive streaming text
        """
        try:
            self.ask(prompt, stream=True, stream_callback=callback)
        except Exception as e:
            logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.kimi')
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
        return "Kimi"

    def supports_streaming(self) -> bool:
        """
        Check if model supports streaming

        :return: True if streaming is supported
        """
        return True

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get Kimi model default configuration

        :return: Default configuration dictionary
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }
