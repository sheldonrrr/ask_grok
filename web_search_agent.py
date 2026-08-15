#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AI-driven web search loop: search again or summarize the current Ask result."""

from __future__ import annotations

import re
import logging

try:
    from .web_search import (
        WebSearchError,
        format_search_results_markdown,
        search_web,
    )
except ImportError:
    from web_search import (
        WebSearchError,
        format_search_results_markdown,
        search_web,
    )

logger = logging.getLogger(__name__)

MAX_SEARCH_ROUNDS = 3
MAX_QUERIES_PER_ROUND = 3

_SEARCH_RE = re.compile(r'<search>(.*?)</search>', re.DOTALL | re.IGNORECASE)
_ANSWER_RE = re.compile(r'<answer>(.*?)</answer>', re.DOTALL | re.IGNORECASE)


def parse_agent_decision(text):
    """Parse an AI reply into ('search', queries) or ('answer', markdown)."""
    raw = (text or '').strip()
    if not raw:
        return 'answer', ''

    search_match = _SEARCH_RE.search(raw)
    if search_match:
        queries = []
        for line in search_match.group(1).splitlines():
            query = line.strip().lstrip('-*').strip()
            if query:
                queries.append(query)
            if len(queries) >= MAX_QUERIES_PER_ROUND:
                break
        if queries:
            return 'search', queries

    answer_match = _ANSWER_RE.search(raw)
    if answer_match:
        return 'answer', answer_match.group(1).strip()
    return 'answer', raw


def _normalize_query(query):
    return re.sub(r'\s+', ' ', (query or '').strip().lower())


def build_planner_prompt(user_prompt, search_transcript, i18n=None, force_answer=False):
    """Build the planner / final-answer prompt around the original Ask prompt."""
    i18n = i18n or {}
    transcript = (search_transcript or '').strip() or i18n.get(
        'web_search_no_previous_results', '(none yet)'
    )
    template_key = 'web_search_force_answer_prompt' if force_answer else 'web_search_planner_prompt'
    default = (
        'Using only the information below, write the final markdown answer. Do not output <search> tags.\n\n'
        'User question and context:\n{user_prompt}\n\nWeb search results:\n{search_transcript}'
        if force_answer else
        'You may request live web searches when you need current facts.\n\n'
        'User question and context:\n{user_prompt}\n\nPrevious web search results:\n{search_transcript}\n\n'
        'Respond with <search> queries (one per line) or the final markdown answer.'
    )
    template = i18n.get(template_key, default)
    return template.format(user_prompt=user_prompt, search_transcript=transcript)


class WebSearchAgent:
    """Run Brave searches requested by the current AI, then return one transcript."""

    def __init__(
        self,
        ask_fn,
        i18n=None,
        api_key='',
        max_rounds=MAX_SEARCH_ROUNDS,
        cancelled_fn=None,
        on_update=None,
        search_fn=None,
    ):
        self.ask_fn = ask_fn
        self.i18n = i18n or {}
        self.api_key = (api_key or '').strip()
        self.max_rounds = max(1, int(max_rounds or MAX_SEARCH_ROUNDS))
        self.cancelled_fn = cancelled_fn or (lambda: False)
        self.on_update = on_update
        self.search_fn = search_fn or self._default_search

    def _default_search(self, query):
        return search_web(query, self.api_key, i18n=self.i18n)

    def _emit(self, chunk):
        if chunk and self.on_update and not self.cancelled_fn():
            self.on_update(chunk)

    def _cancelled(self):
        return bool(self.cancelled_fn())

    def run(self, user_prompt):
        """Return the full markdown (search schedule + final answer)."""
        transcript_parts = []
        used_queries = set()
        fatal_auth_error = None

        for round_index in range(self.max_rounds):
            if self._cancelled():
                break
            can_search = (
                fatal_auth_error is None and round_index < self.max_rounds
            )
            planner_prompt = build_planner_prompt(
                user_prompt,
                '\n\n'.join(transcript_parts),
                self.i18n,
                force_answer=not can_search,
            )
            response = self.ask_fn(planner_prompt) or ''
            if self._cancelled():
                break

            action, payload = parse_agent_decision(response)
            if action != 'search' or not can_search:
                answer = payload if action == 'answer' else (response or '').strip()
                return self._join_final(transcript_parts, answer)

            new_queries = []
            for query in payload:
                key = _normalize_query(query)
                if not key or key in used_queries:
                    continue
                used_queries.add(key)
                new_queries.append(query)

            if not new_queries:
                return self._join_final(transcript_parts, response)

            for query in new_queries:
                if self._cancelled():
                    break
                searching = self.i18n.get(
                    'web_search_searching', 'Searching the web: {query}'
                ).format(query=query)
                prefix = '\n\n' if transcript_parts else ''
                self._emit('{0}{1}\n\n'.format(prefix, searching))
                try:
                    results = self.search_fn(query)
                    block = format_search_results_markdown(query, results, self.i18n)
                except WebSearchError as exc:
                    logger.warning('Brave search failed for %r: %s', query, exc)
                    block = format_search_results_markdown(
                        query, [], self.i18n, error_message=str(exc),
                    )
                    if exc.error_type in ('missing_key', 'invalid_key'):
                        fatal_auth_error = exc
                transcript_parts.append(block)
                self._emit(block if block.endswith('\n') else block + '\n')
                if fatal_auth_error is not None:
                    break

        if self._cancelled():
            return '\n\n'.join(transcript_parts).strip()

        planner_prompt = build_planner_prompt(
            user_prompt, '\n\n'.join(transcript_parts), self.i18n, force_answer=True,
        )
        answer = self.ask_fn(planner_prompt) or ''
        action, payload = parse_agent_decision(answer)
        if action == 'answer':
            answer = payload
        return self._join_final(transcript_parts, answer)

    @staticmethod
    def _join_final(transcript_parts, answer):
        parts = [part for part in transcript_parts if part]
        final = (answer or '').strip()
        if final:
            parts.append(final)
        return '\n\n'.join(parts).strip()
