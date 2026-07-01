"""
Perplexity (Sonar) AI Model Implementation

Perplexity Sonar API is largely OpenAI Chat Completions compatible.
Base URL: https://api.perplexity.ai
Endpoints:
- POST /chat/completions
- GET  /models
"""

import json
import time
import logging
from typing import Dict, Any

from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests

from .base import BaseAIModel
from ..i18n import get_translation


logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.perplexity')


def merge_snapshot(full_text: str, snapshot_text: str):
    """Merge final snapshot into streamed content without duplicating body."""
    full_text = full_text or ""
    snapshot_text = snapshot_text or ""
    if not snapshot_text:
        return full_text, "", "no_snapshot"
    if not full_text:
        return snapshot_text, snapshot_text, "init_from_snapshot"
    if snapshot_text.startswith(full_text):
        delta = snapshot_text[len(full_text):]
        return snapshot_text, delta, "snapshot_extends_full"
    if full_text.startswith(snapshot_text):
        return full_text, "", "snapshot_shorter_ignore"
    if snapshot_text in full_text:
        return full_text, "", "snapshot_inside_full"
    # Conservative fallback: keep stream content to avoid duplicate body.
    return full_text, "", "conflict_keep_full"


class PerplexityModel(BaseAIModel):
    """Perplexity Sonar model."""

    DEFAULT_MODEL = "sonar-pro"
    DEFAULT_API_BASE_URL = "https://api.perplexity.ai"

    def _validate_config(self):
        required_keys = ['api_key', 'api_base_url']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(
                    translations.get('missing_required_config', 'Missing required configuration: {key}').format(
                        key=key
                    )
                )

        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL

    def get_token(self) -> str:
        return self.config.get('api_key', '')

    def validate_token(self) -> bool:
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
        token = self.get_token()
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token,
        }

    def supports_streaming(self) -> bool:
        return True

    def get_model_name(self) -> str:
        return self.config.get('model', self.DEFAULT_MODEL)

    def get_provider_name(self) -> str:
        return "Perplexity"

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,
        }

    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get(
            'system_message',
            translations.get(
                'default_system_message',
                'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.',
            ),
        )

        data: Dict[str, Any] = {
            "model": self.config.get('model', self.DEFAULT_MODEL),
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4096),
        }

        # Add streaming support (only add if explicitly set to True)
        if kwargs.get('stream', False):
            data['stream'] = True

        # Perplexity-specific (optional) parameters can be passed-through via kwargs
        passthrough_keys = [
            'search_domain_filter',
            'search_recency_filter',
            'return_images',
            'return_related_questions',
            'search_mode',
        ]
        for k in passthrough_keys:
            if k in kwargs and kwargs[k] is not None:
                data[k] = kwargs[k]

        return data

    def ask(self, prompt: str, **kwargs) -> str:
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)

        # Random Question (suggestion) mode: do not append citations/search_results
        is_random_question = bool(kwargs.get('is_random_question', False))

        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)

        api_url = f"{self.config['api_base_url'].rstrip('/')}/chat/completions"
        try:
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                citations = []
                search_results = []
                latest_snapshot = ""

                try:
                    with requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),
                        stream=True,
                    ) as response:
                        response.raise_for_status()
                        pending_event_lines = []

                        def append_delta(new_text: str):
                            """仅处理增量文本。"""
                            nonlocal chunk_count, full_content, last_chunk_time
                            if not new_text:
                                return
                            full_content += new_text
                            stream_callback(new_text)
                            chunk_count += 1
                            last_chunk_time = time.time()

                        def process_event_payload(payload_text: str) -> bool:
                            nonlocal citations, search_results, latest_snapshot
                            if not payload_text:
                                return False
                            payload_text = payload_text.strip()
                            if not payload_text:
                                return False
                            if payload_text == '[DONE]':
                                return True
                            try:
                                chunk = json.loads(payload_text)
                            except json.JSONDecodeError:
                                return False

                            if not isinstance(chunk, dict):
                                return True

                            if isinstance(chunk.get('citations'), list):
                                citations = chunk.get('citations') or citations
                            if isinstance(chunk.get('search_results'), list):
                                search_results = chunk.get('search_results') or search_results

                            event_name = chunk.get('event')
                            choices = chunk.get('choices', [{}])[0]
                            if not isinstance(choices, dict):
                                choices = {}

                            delta = choices.get('delta', {})
                            content = delta.get('content') if isinstance(delta, dict) else None

                            message = choices.get('message', {})
                            message_content = (
                                message.get('content') if isinstance(message, dict) else None
                            )

                            if content:
                                append_delta(content)
                            if message_content:
                                latest_snapshot = message_content

                            return True

                        def flush_pending_event():
                            nonlocal pending_event_lines
                            if not pending_event_lines:
                                return
                            payload_text = '\n'.join(pending_event_lines)
                            if not process_event_payload(payload_text):
                                logger.warning("Skipped unparsable SSE payload from Perplexity stream")
                            pending_event_lines = []

                        for raw_line in response.iter_lines(decode_unicode=False):
                            if isinstance(raw_line, bytes):
                                line_text = raw_line.decode('utf-8', errors='replace')
                            else:
                                line_text = raw_line if isinstance(raw_line, str) else str(raw_line)
                            if not line_text:
                                flush_pending_event()
                                continue

                            if line_text.startswith('event:'):
                                flush_pending_event()
                                continue

                            if line_text.startswith('data:'):
                                chunk_data = line_text[len('data:'):].lstrip()
                                if chunk_data == '[DONE]':
                                    flush_pending_event()
                                    break
                                # 大多数服务端每个 data 行就是独立 JSON 事件；先尝试直接解析。
                                if process_event_payload(chunk_data):
                                    continue
                                pending_event_lines.append(chunk_data)
                                continue

                            if pending_event_lines:
                                # 容错：部分服务端会把同一event拆成首行data + 后续续行
                                pending_event_lines.append(line_text)
                                payload_text = '\n'.join(pending_event_lines)
                                if process_event_payload(payload_text):
                                    pending_event_lines = []
                                continue

                            # Warn if no new data for 15 seconds
                            current_time = time.time()
                            if current_time - last_chunk_time > 15:
                                logger.warning(
                                    f"No new data received for {current_time - last_chunk_time:.1f} seconds"
                                )

                        flush_pending_event()

                        merged_content, merged_delta, _ = merge_snapshot(
                            full_content,
                            latest_snapshot,
                        )
                        if merged_delta:
                            stream_callback(merged_delta)
                            chunk_count += 1
                        full_content = merged_content

                        logger.info(
                            f"Streaming completed, received {chunk_count} chunks, total length: {len(full_content)}"
                        )

                        if not full_content:
                            translations = get_translation(self.config.get('language', 'en'))
                            raise Exception(translations.get('empty_response', 'Received empty response from API'))

                        if is_random_question:
                            return full_content

                        appendix = self._format_references(citations=citations, search_results=search_results)
                        # Some UIs only consume stream_callback chunks; ensure appendix is visible by emitting once at the end
                        if appendix and stream_callback:
                            try:
                                stream_callback(appendix)
                            except Exception:
                                pass
                        return full_content + appendix

                except requests.exceptions.RequestException as e:
                    translations = get_translation(self.config.get('language', 'en'))
                    raise Exception(
                        translations.get('api_request_failed', 'API request failed: {error}').format(
                            error=str(e)
                        )
                    )

            # Non-streaming mode
            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 60),
            )
            response.raise_for_status()

            result = response.json()
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content']
                if is_random_question:
                    return content
                appendix = self._format_references(
                    citations=result.get('citations'),
                    search_results=result.get('search_results'),
                )
                return content + appendix

            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(translations.get('invalid_response', 'Invalid API response format'))

        except requests.exceptions.RequestException as e:
            translations = get_translation(self.config.get('language', 'en'))
            raise Exception(
                translations.get('api_request_failed', 'API request failed: {error}').format(
                    error=str(e)
                )
            ) from e

    def _format_references(self, citations=None, search_results=None) -> str:
        """Format Perplexity citations/search_results as plain text for easy copy/paste."""

        citations_list = citations if isinstance(citations, list) else []
        search_results_list = search_results if isinstance(search_results, list) else []

        lines = []

        if citations_list:
            lines.append("\n\n---\nCitations:")
            for idx, url in enumerate(citations_list, start=1):
                if not url:
                    continue
                lines.append(f"[{idx}] {url}")

        if search_results_list:
            lines.append("\n\n---\nSearch Results:")
            for idx, item in enumerate(search_results_list, start=1):
                if not isinstance(item, dict):
                    continue
                title = (item.get('title') or '').strip()
                url = (item.get('url') or '').strip()
                date = (item.get('date') or '').strip()
                last_updated = (item.get('last_updated') or '').strip()

                header_parts = []
                if title:
                    header_parts.append(title)
                if date:
                    header_parts.append(date)
                if last_updated:
                    header_parts.append(f"updated: {last_updated}")

                header = " - ".join(header_parts).strip()
                if header:
                    lines.append(f"[{idx}] {header}")
                if url:
                    lines.append(f"    {url}")

        return "\n".join(lines) if lines else ""
