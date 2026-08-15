#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Brave Search API client for optional web search in Ask."""

from __future__ import annotations

import logging
logger = logging.getLogger(__name__)

BRAVE_SEARCH_URL = 'https://api.search.brave.com/res/v1/web/search'
DEFAULT_RESULT_COUNT = 5
DEFAULT_TIMEOUT = 15
TEST_QUERY = 'brave search'


class WebSearchError(Exception):
    """Raised when a Brave Search request cannot be completed."""

    def __init__(self, message, error_type='search_error', status_code=None):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code

    def __str__(self):
        return self.message


def get_brave_api_key(prefs=None):
    """Return the user-bound Brave Search API key from plugin prefs."""
    if prefs is None:
        try:
            from .config import get_prefs
        except ImportError:
            from config import get_prefs
        prefs = get_prefs()
    return (prefs.get('brave_search_api_key') or '').strip()


def parse_brave_web_results(payload, limit=DEFAULT_RESULT_COUNT):
    """Extract title/url/description rows from a Brave Search JSON body."""
    if not isinstance(payload, dict):
        return []
    web = payload.get('web') or {}
    raw_results = web.get('results') or []
    if not isinstance(raw_results, list):
        return []

    results = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        title = (item.get('title') or '').strip()
        url = (item.get('url') or '').strip()
        description = (item.get('description') or item.get('snippet') or '').strip()
        if not title and not url:
            continue
        results.append({
            'title': title or url,
            'url': url,
            'description': description,
        })
        if len(results) >= max(1, int(limit or DEFAULT_RESULT_COUNT)):
            break
    return results


def format_search_results_markdown(query, results, i18n=None, error_message=None):
    """Render one search round as markdown for the current Ask response."""
    i18n = i18n or {}
    heading = i18n.get('web_search_heading', 'Web search: {query}').format(query=query)
    lines = ['### {0}'.format(heading)]

    if error_message:
        lines.append(error_message)
        return '\n'.join(lines)

    if not results:
        lines.append(i18n.get('web_search_no_results', 'No web results for: {query}').format(query=query))
        return '\n'.join(lines)

    for index, item in enumerate(results, start=1):
        title = item.get('title') or item.get('url') or ''
        url = item.get('url') or ''
        description = (item.get('description') or '').replace('\n', ' ').strip()
        if url:
            entry = '{0}. [{1}]({2})'.format(index, title, url)
        else:
            entry = '{0}. {1}'.format(index, title)
        if description:
            entry = '{0} — {1}'.format(entry, description)
        lines.append(entry)
    return '\n'.join(lines)


def _import_requests():
    try:
        from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
        return requests
    except ImportError:
        try:
            from lib.ask_ai_plugin_vendor import requests
            return requests
        except ImportError:
            import requests
            return requests


def search_web(
    query,
    api_key,
    count=DEFAULT_RESULT_COUNT,
    timeout=DEFAULT_TIMEOUT,
    session=None,
    requests_mod=None,
    i18n=None,
):
    """Call Brave Search and return parsed result dicts.

    Raises WebSearchError for missing/invalid keys and HTTP failures.
    """
    i18n = i18n or {}
    query = (query or '').strip()
    api_key = (api_key or '').strip()
    if not api_key:
        raise WebSearchError(
            i18n.get(
                'web_search_missing_key',
                'Web Search is on, but no Brave Search API key is configured. '
                'Open Configuration → Search and paste your Brave API key.',
            ),
            error_type='missing_key',
        )
    if not query:
        return []

    requests = requests_mod or _import_requests()
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': api_key,
    }
    params = {
        'q': query,
        'count': max(1, min(int(count or DEFAULT_RESULT_COUNT), 20)),
    }

    try:
        masked = api_key[:4] + '********' if len(api_key) > 4 else '********'
        logger.info('Brave Search request q=%r key=%s', query, masked)
        http = session or requests
        response = http.get(
            BRAVE_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=timeout,
        )
    except Exception as exc:
        raise WebSearchError(
            i18n.get(
                'web_search_request_failed',
                'Web search failed for "{query}": {error}',
            ).format(query=query, error=str(exc)),
            error_type='network_error',
        ) from exc

    status = getattr(response, 'status_code', None)
    if status in (401, 403):
        raise WebSearchError(
            i18n.get(
                'web_search_invalid_key',
                'Brave Search rejected the API key (HTTP {status}). '
                'Check the key and your Brave plan in Settings → Search.',
            ).format(status=status),
            error_type='invalid_key',
            status_code=status,
        )
    if status == 429:
        raise WebSearchError(
            i18n.get(
                'web_search_rate_limited',
                'Brave Search rate limit reached (HTTP 429). Try again later or check your plan quota.',
            ),
            error_type='rate_limited',
            status_code=status,
        )
    if status is not None and status >= 400:
        body = ''
        try:
            body = (response.text or '')[:200]
        except Exception:
            body = ''
        raise WebSearchError(
            i18n.get(
                'web_search_request_failed',
                'Web search failed for "{query}": {error}',
            ).format(query=query, error='HTTP {0} {1}'.format(status, body).strip()),
            error_type='http_error',
            status_code=status,
        )

    try:
        payload = response.json()
    except Exception as exc:
        raise WebSearchError(
            i18n.get(
                'web_search_request_failed',
                'Web search failed for "{query}": {error}',
            ).format(query=query, error=str(exc)),
            error_type='invalid_response',
            status_code=status,
        ) from exc

    return parse_brave_web_results(payload, limit=count)
