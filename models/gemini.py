"""
Google Gemini 模型实现

使用最新 Gemini REST API 格式：
- Auth: x-goog-api-key header
- Endpoint: /v1beta/models/{model}:generateContent
- System prompt: systemInstruction
- Streaming: :streamGenerateContent?alt=sse
"""
import json
import re
import time
from typing import Dict, Any
import logging

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation

# 获取日志记录器
logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.gemini')


class GeminiModel(BaseAIModel):
    """
    Google Gemini 模型实现类
    """
    # 默认模型名称（Google AI Studio / generativelanguage API 格式，不含 google/ 前缀）
    DEFAULT_MODEL = "gemini-3.5-flash"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def _validate_config(self):
        """
        验证 Gemini 模型配置

        :raises ValueError: 当配置无效时抛出异常
        """
        required_keys = ['api_key']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(
                    translations.get(
                        'missing_required_config',
                        'Missing required configuration: {key}',
                    ).format(key=key)
                )

        if 'api_base_url' not in self.config or not self.config.get('api_base_url'):
            self.config['api_base_url'] = self.DEFAULT_API_BASE_URL

        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL

    def get_token(self) -> str:
        """
        获取 Gemini 模型的 API Key/Token

        :return: API Key/Token 字符串
        """
        return self.config.get('api_key', '')

    def validate_token(self) -> bool:
        """
        验证 Gemini 模型的 token 是否有效

        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
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
        准备 Gemini API 请求头（最新推荐：x-goog-api-key）

        :return: 请求头字典
        """
        headers = {
            "Content-Type": "application/json",
        }

        api_key = self.get_token()
        if api_key:
            headers["x-goog-api-key"] = api_key

        return headers

    @staticmethod
    def normalize_model_name(model_name: str, default: str = None) -> str:
        """
        规范化模型名，兼容历史配置中的 models/ 与 google/ 前缀。

        :param model_name: 原始模型名
        :param default: 为空时的默认值
        :return: 可用于 URL 的模型名，如 gemini-3.5-flash
        """
        name = (model_name or '').strip()
        if not name:
            return default or GeminiModel.DEFAULT_MODEL

        if name.startswith('models/'):
            name = name[len('models/'):]

        # OpenRouter 风格前缀，不能用于 generativelanguage.googleapis.com
        if name.startswith('google/'):
            name = name[len('google/'):]

        return name

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Gemini API 请求数据（使用 systemInstruction + contents）

        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature 等
        :return: 请求数据字典
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
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ],
                }
            ]
        }

        # 最新格式：系统提示使用 systemInstruction，而不是伪装成 user 消息
        if system_message and system_message.strip():
            data["systemInstruction"] = {
                "parts": [
                    {"text": system_message}
                ]
            }

        generation_config: Dict[str, Any] = {}

        temperature = kwargs.get('temperature', 0.7)
        if temperature is not None:
            generation_config["temperature"] = temperature

        if 'max_tokens' in kwargs and kwargs.get('max_tokens') is not None:
            generation_config["maxOutputTokens"] = kwargs.get('max_tokens')

        if 'top_p' in kwargs and kwargs.get('top_p') is not None:
            generation_config["topP"] = kwargs.get('top_p')

        if 'top_k' in kwargs and kwargs.get('top_k') is not None:
            generation_config["topK"] = kwargs.get('top_k')

        if generation_config:
            data['generationConfig'] = generation_config

        return data

    def mask_api_key(self, text: str) -> str:
        """
        隐藏文本中的 API Key

        :param text: 原始文本
        :return: 隐藏 API Key 后的文本
        """
        text = re.sub(r'key=[A-Za-z0-9_-]+', 'key=********', text)
        text = re.sub(r'"api_key"\s*:\s*"[^"]+"', '"api_key":"********"', text)
        text = re.sub(
            r'(?i)(x-goog-api-key["\']?\s*[:=]\s*["\']?)[^"\'\s,]+',
            r'\1********',
            text,
        )
        return text

    def _build_generate_url(self, model_name: str, api_base_url: str, use_stream: bool) -> str:
        """构建 generateContent / streamGenerateContent URL。"""
        base = (api_base_url or self.DEFAULT_API_BASE_URL).rstrip('/')
        model = self.normalize_model_name(model_name, self.DEFAULT_MODEL)
        action = "streamGenerateContent" if use_stream else "generateContent"
        return f"{base}/models/{model}:{action}"

    def _extract_text_from_candidate(self, candidate: Dict[str, Any]) -> str:
        """从 candidate.content.parts 提取文本。"""
        content = candidate.get('content') or {}
        parts = content.get('parts') or []
        texts = []
        for part in parts:
            text = part.get('text')
            if text:
                texts.append(text)
        return ''.join(texts)

    def ask(self, prompt: str, **kwargs) -> str:
        """向 Gemini API 发送请求并获取回复

        Args:
            prompt: 用户提问
            **kwargs: 其他参数，包括：
                system_message: 系统消息
                temperature: 温度
                max_tokens: 最大令牌数
                top_p: Top-p 采样
                top_k: Top-k 采样
                stream: 是否使用流式传输
                stream_callback: 流式回调函数

        Returns:
            模型回复的文本
        """
        model_name = kwargs.get('model') or self.config.get('model', self.DEFAULT_MODEL)
        api_base_url = kwargs.get('api_base_url') or self.config.get(
            'api_base_url', self.DEFAULT_API_BASE_URL
        )

        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)

        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)

        params = {}
        url = self._build_generate_url(model_name, api_base_url, use_stream and bool(stream_callback))
        if use_stream and stream_callback:
            params["alt"] = "sse"

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                if use_stream and stream_callback:
                    full_content = ""
                    chunk_count = 0
                    last_chunk_time = time.time()

                    with requests.post(
                        url,
                        headers=headers,
                        json=data,
                        params=params,
                        timeout=kwargs.get('timeout', 300),
                        stream=True,
                    ) as response:
                        response.raise_for_status()

                        try:
                            for line in response.iter_lines():
                                if line:
                                    line = line.decode('utf-8')

                                    if line.startswith('data: '):
                                        line = line[6:]

                                        if line.strip() == "[DONE]":
                                            break

                                        try:
                                            chunk_data = json.loads(line)

                                            if 'candidates' in chunk_data and chunk_data['candidates']:
                                                candidate = chunk_data['candidates'][0]
                                                chunk_text = self._extract_text_from_candidate(candidate)
                                                if chunk_text:
                                                    full_content += chunk_text
                                                    stream_callback(chunk_text)
                                                    chunk_count += 1
                                                    last_chunk_time = time.time()
                                        except json.JSONDecodeError as je:
                                            logger.error(
                                                f"JSON解析错误: {str(je)}, 行内容: {line[:50]}..."
                                            )
                                            continue

                                current_time = time.time()
                                if current_time - last_chunk_time > 15:
                                    logger.warning(
                                        f"已经 {current_time - last_chunk_time:.1f} 秒没有收到新数据"
                                    )

                                if current_time - last_chunk_time > 60 and full_content:
                                    logger.warning("超过60秒无响应，主动触发恢复机制")
                                    raise requests.exceptions.ReadTimeout(
                                        "流式传输超过60秒没有新内容，可能是连接问题"
                                    )
                        except Exception as e:
                            logger.error(f"流式处理异常: {str(e)}")
                            logger.warning(
                                f"异常发生时状态: 已接收 {chunk_count} 块, 总长度: {len(full_content)}"
                            )

                            if full_content:
                                try:
                                    recovery_data = self.prepare_request_data(prompt, **kwargs)
                                    translations = get_translation(
                                        self.config.get('language', 'en')
                                    )
                                    recovery_prompt = translations.get(
                                        'stream_continue_prompt',
                                        'Please continue your previous answer without repeating content already provided.',
                                    )

                                    unclosed_code_blocks = full_content.count('```') % 2
                                    if unclosed_code_blocks:
                                        recovery_prompt += translations.get(
                                            'stream_continue_code_blocks',
                                            ' Your previous answer had unclosed code blocks. Please continue and complete these code blocks.',
                                        )

                                    recovery_data['contents'].append(
                                        {
                                            "role": "model",
                                            "parts": [{"text": full_content}],
                                        }
                                    )
                                    recovery_data['contents'].append(
                                        {
                                            "role": "user",
                                            "parts": [{"text": recovery_prompt}],
                                        }
                                    )

                                    recovery_timeout = kwargs.get('timeout', 300) + 60

                                    with requests.post(
                                        url,
                                        headers=headers,
                                        json=recovery_data,
                                        params=params,
                                        timeout=recovery_timeout,
                                        stream=True,
                                    ) as recovery_response:
                                        recovery_response.raise_for_status()

                                        for line in recovery_response.iter_lines():
                                            if line:
                                                line = line.decode('utf-8')

                                                if line.startswith('data: '):
                                                    line = line[6:]

                                                    if line.strip() == "[DONE]":
                                                        break

                                                    try:
                                                        chunk_data = json.loads(line)

                                                        if (
                                                            'candidates' in chunk_data
                                                            and chunk_data['candidates']
                                                        ):
                                                            candidate = chunk_data['candidates'][0]
                                                            chunk_text = self._extract_text_from_candidate(
                                                                candidate
                                                            )
                                                            if chunk_text:
                                                                full_content += chunk_text
                                                                stream_callback(chunk_text)
                                                                chunk_count += 1
                                                                last_chunk_time = time.time()
                                                    except json.JSONDecodeError as je:
                                                        logger.error(
                                                            f"恢复请求JSON解析错误: {str(je)}"
                                                        )
                                                        continue

                                except Exception as recovery_e:
                                    logger.error(f"恢复连接失败: {str(recovery_e)}")
                                    logger.warning(
                                        f"将返回已接收的 {len(full_content)} 字符内容"
                                    )
                            else:
                                raise

                    return full_content
                else:
                    response = requests.post(
                        url,
                        headers=headers,
                        json=data,
                        params=params,
                        timeout=kwargs.get('timeout', 300),
                    )
                    response.raise_for_status()

                    result = response.json()

                    if 'candidates' in result and result['candidates']:
                        candidate = result['candidates'][0]
                        content = self._extract_text_from_candidate(candidate)
                        if content:
                            return content

                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get(
                        'api_invalid_response',
                        'Unable to get valid API response',
                    )
                    if 'error' in result:
                        error_msg = (
                            f"{error_msg}: "
                            f"{result['error'].get('message', translations.get('unknown_error', 'Unknown error'))}"
                        )
                    logger.error(f"Gemini API 响应解析失败: {error_msg}")
                    raise Exception(error_msg)

            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")

                if attempt < max_retries - 1:
                    retry_wait = retry_delay * (2 ** attempt)
                    time.sleep(retry_wait)
                    continue

                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get(
                    'api_request_failed',
                    'API request failed: {error}',
                ).format(error=str(e))

                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()

                        if e.response.status_code == 404:
                            error_msg = translations.get(
                                'api_version_model_error',
                                'API version or model name error: {message}\n\n'
                                'Please update API Base URL to "{base_url}" and model to "{model}" '
                                'or other available model in settings.',
                            ).format(
                                message=error_detail.get('error', {}).get('message', ''),
                                base_url=self.DEFAULT_API_BASE_URL,
                                model=self.DEFAULT_MODEL,
                            )
                        elif e.response.status_code == 400:
                            message = error_detail.get('error', {}).get('message', '')
                            if 'location is not supported' in message.lower():
                                error_msg = translations.get(
                                    'gemini_geo_restriction',
                                    'Gemini API is not available in your region.',
                                )
                            else:
                                error_msg = translations.get(
                                    'api_format_error',
                                    'API request format error: {message}',
                                ).format(message=message)
                        elif e.response.status_code == 401:
                            error_msg = translations.get(
                                'api_key_invalid',
                                'API Key invalid or unauthorized: {message}\n\n'
                                'Please check your API Key and ensure API access is enabled.',
                            ).format(
                                message=error_detail.get('error', {}).get('message', '')
                            )
                        elif e.response.status_code == 429:
                            error_msg = translations.get(
                                'api_rate_limit',
                                'Request rate limit exceeded, please try again later\n\n'
                                'You may have exceeded the free usage quota. This could be due to:\n'
                                '1. Too many requests per minute\n'
                                '2. Too many requests per day\n'
                                '3. Too many input tokens per minute',
                            )
                    except Exception:
                        error_msg += (
                            f" | 响应内容: "
                            f"{e.response.text[:200] if hasattr(e.response, 'text') else '无法解析响应'}"
                        )

                raise Exception(error_msg) from e

    def get_model_name(self) -> str:
        """
        获取当前模型名称

        :return: 模型名称字符串
        """
        return self.normalize_model_name(
            self.config.get('model', self.DEFAULT_MODEL),
            self.DEFAULT_MODEL,
        )

    def get_provider_name(self) -> str:
        """
        获取提供商名称

        :return: 提供商名称字符串
        """
        return "Google Gemini"

    def supports_streaming(self) -> bool:
        """
        检查 Gemini 模型是否支持流式传输

        :return: 始终返回 True，因为 Gemini API 支持流式传输
        """
        return True

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Gemini 模型的默认配置

        :return: 默认配置字典
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    def prepare_models_request_headers(self) -> Dict[str, str]:
        """
        准备获取模型列表的请求头
        最新推荐使用 x-goog-api-key，GET 请求不需要 Content-Type

        :return: 请求头字典
        """
        headers = {}
        api_key = self.get_token()
        if api_key:
            headers["x-goog-api-key"] = api_key
        return headers

    def prepare_models_request_url(self, base_url: str, endpoint: str) -> str:
        """
        准备获取模型列表的完整 URL（不再把 API key 放进查询参数）

        :param base_url: API 基础 URL
        :param endpoint: API 端点路径
        :return: 完整的请求 URL
        """
        return self.build_api_url(base_url, endpoint)

    def parse_models_response(self, data: Dict[str, Any]) -> list:
        """
        解析 Gemini API 的模型列表响应
        移除 models/ 前缀，并优先保留支持 generateContent 的模型

        :param data: API 响应的 JSON 数据
        :return: 模型名称列表
        """
        models = []
        for model in data.get('models', []):
            methods = model.get('supportedGenerationMethods') or model.get('supportedActions') or []
            if methods and 'generateContent' not in methods:
                continue

            model_name = model.get('name', '')
            if model_name.startswith('models/'):
                model_name = model_name.replace('models/', '', 1)
            if model_name:
                models.append(model_name)
        return models

    def verify_api_key_with_test_request(self) -> None:
        """
        使用最新 header 认证方式验证 API Key
        """
        from ..i18n import get_translation

        provider_name = self.get_provider_name()
        timeout_seconds = 15

        try:
            api_base_url = self.config.get('api_base_url', self.DEFAULT_API_BASE_URL)
            model_name = self.normalize_model_name(
                self.config.get('model', self.DEFAULT_MODEL),
                self.DEFAULT_MODEL,
            )
            url = self._build_generate_url(model_name, api_base_url, use_stream=False)

            test_data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": "hi"}],
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 1,
                },
            }

            headers = self.prepare_headers()

            response = requests.post(
                url,
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

            if response.status_code in (200, 400):
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
