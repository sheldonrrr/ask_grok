"""
OpenAI-compatible Chat Completions helpers for local/remote providers.

Used by Ollama, LM Studio, KoboldCpp, and Custom.
Endpoint shape: POST {base}/chat/completions (or /v1/chat/completions).
"""
import json
import logging
from typing import Any, Dict, Optional

from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.openai_compat')


class OpenAICompatModel(BaseAIModel):
    """
    Shared OpenAI Chat Completions client.

    Subclasses set DEFAULT_MODEL, DEFAULT_API_BASE_URL, PROVIDER_DISPLAY_NAME.
    """

    DEFAULT_MODEL = ""
    DEFAULT_API_BASE_URL = "http://localhost:11434/v1"
    PROVIDER_DISPLAY_NAME = "OpenAI Compatible"
    # Appended when base URL has no chat path
    CHAT_COMPLETIONS_PATH = "/v1/chat/completions"

    def _validate_config(self):
        if not self.config.get('api_base_url'):
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(
                translations.get(
                    'missing_required_config',
                    'Missing required configuration: {key}',
                ).format(key='api_base_url')
            )
        if not self.config.get('model') and self.DEFAULT_MODEL:
            self.config['model'] = self.DEFAULT_MODEL

    def get_token(self) -> str:
        return self.config.get('api_key', '')

    def requires_auth_token(self) -> bool:
        return False

    def validate_token(self) -> bool:
        self._validate_config()
        if not self.config.get('api_base_url'):
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(
                translations.get('api_base_url_required', 'API Base URL is required')
            )
        return True

    def prepare_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        token = self.get_token()
        if token and token.strip():
            if not token.startswith('Bearer '):
                token = f'Bearer {token}'
            headers["Authorization"] = token
        return headers

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get(
            'system_message',
            translations.get(
                'default_system_message',
                'You are an expert in book analysis. Your task is to help users '
                'understand books better by providing insightful questions and analysis.',
            ),
        )

        data: Dict[str, Any] = {
            "model": kwargs.get('model') or self.config.get('model', self.DEFAULT_MODEL),
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            "temperature": kwargs.get('temperature', 0.7),
        }

        max_tokens = kwargs.get('max_tokens')
        if max_tokens is not None:
            data['max_tokens'] = max_tokens

        if kwargs.get('stream', False):
            data['stream'] = True

        return data

    def resolve_chat_url(self, base_url: Optional[str] = None) -> str:
        """Build chat completions URL from configured base URL."""
        base = (base_url or self.config.get('api_base_url') or self.DEFAULT_API_BASE_URL).rstrip('/')
        if '/api/chat' in base or '/chat/completions' in base:
            return base
        return self.build_api_url(base, self.CHAT_COMPLETIONS_PATH)

    def ask(self, prompt: str, **kwargs) -> str:
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        api_url = self.resolve_chat_url(kwargs.get('api_base_url'))

        try:
            session = requests.Session()
            session.trust_env = False  # local servers should not inherit proxies

            if use_stream and stream_callback:
                full_content = ""
                with session.post(
                    api_url,
                    headers=headers,
                    json=data,
                    stream=True,
                    timeout=kwargs.get('timeout', 120),
                ) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if not line:
                            continue
                        line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                        if line_str.startswith('data: '):
                            line_str = line_str[6:]
                        if line_str.strip() == '[DONE]':
                            break
                        try:
                            chunk = json.loads(line_str)
                        except json.JSONDecodeError:
                            continue

                        if 'choices' in chunk and chunk['choices']:
                            content = chunk['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                full_content += content
                                stream_callback(content)
                        elif 'message' in chunk and 'content' in chunk['message']:
                            # legacy Ollama native NDJSON fallback
                            content = chunk['message']['content']
                            if content:
                                full_content += content
                                stream_callback(content)
                            if chunk.get('done', False):
                                break
                return full_content

            data['stream'] = False
            response = session.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 120),
            )
            response.raise_for_status()
            result = response.json()

            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            if 'message' in result and 'content' in result['message']:
                return result['message']['content']

            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'api_content_extraction_failed',
                    'Unable to extract content from API response',
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
                    error_msg += f" | {json.dumps(error_detail, ensure_ascii=False)}"
                except Exception:
                    error_msg += f" | {getattr(e.response, 'text', '')}"
            raise Exception(error_msg) from e

    def supports_streaming(self) -> bool:
        return True

    def get_model_name(self) -> str:
        return self.config.get('model', self.DEFAULT_MODEL)

    def get_provider_name(self) -> str:
        return self.PROVIDER_DISPLAY_NAME

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    def verify_api_key_with_test_request(self, test_model: str = None) -> None:
        """
        Ping chat completions to confirm the local/remote server is reachable.

        :param test_model: Optional model override (kept for Ollama-style callers)
        """
        provider_name = self.get_provider_name()
        model_name = test_model or self.config.get('model') or self.DEFAULT_MODEL
        if not model_name:
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get(
                    'model_name_required',
                    'Please select or enter a model name before testing.',
                )
            )

        try:
            headers = self.prepare_headers()
            api_url = self.resolve_chat_url()
            test_data = self.prepare_request_data(
                "hi",
                model=model_name,
                max_tokens=16,
                stream=False,
            )
            logger.info(f"[{provider_name}] verify via {api_url} model={model_name}")

            session = requests.Session()
            session.trust_env = False
            response = session.post(
                api_url,
                headers=headers,
                json=test_data,
                timeout=30,
            )

            if response.status_code in (401, 403):
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get(
                    'error_401',
                    'API Key authentication failed. Please check: API Key is correct, '
                    'account has sufficient balance, API Key has not expired.',
                )
                tech_details = translations.get('technical_details', 'Technical Details')
                raise Exception(
                    f"{error_msg}\n\n{tech_details}: HTTP {response.status_code}"
                )

            if response.status_code >= 500:
                response.raise_for_status()

            logger.info(
                f"[{provider_name}] verify ok - status {response.status_code}"
            )

        except requests.exceptions.ConnectionError as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'local_service_not_running',
                'Cannot connect to the local AI service. Please confirm it is running '
                'and the Base URL is correct.',
            )
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(f"{error_msg}\n\n{tech_details}: {str(e)}") from e

        except requests.exceptions.Timeout as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get(
                'error_network',
                'Network connection failed. Please check network connection, '
                'proxy settings, or firewall configuration.',
            )
            tech_details = translations.get('technical_details', 'Technical Details')
            raise Exception(f"{error_msg}\n\n{tech_details}: {str(e)}") from e

        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code in (401, 403):
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get(
                        'error_401',
                        'API Key authentication failed.',
                    )
                    tech_details = translations.get('technical_details', 'Technical Details')
                    raise Exception(f"{error_msg}\n\n{tech_details}: {str(e)}") from e
            logger.info(f"[{provider_name}] verify passed with non-auth error: {e}")
