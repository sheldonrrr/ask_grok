#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Prompt length limits and validation for Ask AI Plugin."""

import json
import logging
import math

logger = logging.getLogger(__name__)

# Selection thresholds
LARGE_SELECTION_THRESHOLD = 50
COMPACT_METADATA_THRESHOLD = 30

# Default character limits (when custom limit is disabled)
#
# Derived from mainstream model context windows (2026, plugin default models):
#   OpenAI GPT-5.4:     400,000 tokens
#   DeepSeek V4-Flash: 1,000,000 tokens
#   Claude Opus 4.8:   1,000,000 tokens
#   (GPT-4o baseline still common: 128,000 tokens)
# Average of the three plugin defaults ≈ 800,000 tokens.
#
# Client limit uses ~25% of the 128K minimum tier for input prompt (~32K tokens),
# converted at ~3.5 characters/token → 112K chars, rounded to 128K for clarity.
# Multi-book keeps a 2× ratio for extra metadata. Output tokens and system
# overhead remain separate (see api.py max_tokens).
DEFAULT_SINGLE_LIMIT = 128_000
DEFAULT_MULTI_LIMIT = 256_000
DEFAULT_CUSTOM_LIMIT = 524_288
MIN_CUSTOM_LIMIT = 1000
MAX_CUSTOM_LIMIT = 2_000_000


def get_max_prompt_length(is_multi_book, prefs):
    """Return the effective max prompt length in characters."""
    if prefs.get('enable_custom_prompt_limit'):
        try:
            value = int(prefs.get('max_prompt_length', DEFAULT_CUSTOM_LIMIT))
        except (TypeError, ValueError):
            value = DEFAULT_CUSTOM_LIMIT
        return max(MIN_CUSTOM_LIMIT, min(value, MAX_CUSTOM_LIMIT))
    return DEFAULT_MULTI_LIMIT if is_multi_book else DEFAULT_SINGLE_LIMIT


def count_books_in_library_metadata(prefs):
    """Count books in cached library metadata JSON."""
    cached = prefs.get('library_cached_metadata', '')
    if not cached:
        return 0
    try:
        books = json.loads(cached)
        return len(books) if isinstance(books, list) else 0
    except (json.JSONDecodeError, TypeError):
        return 0


def _estimate_reduce_books(current, limit, book_count):
    """Estimate how many books to deselect to fit within the limit."""
    if book_count <= 0 or current <= limit:
        return 0
    over = current - limit
    avg_per_book = max(1, (current - 500) // book_count)
    return max(1, math.ceil(over / avg_per_book))


def format_prompt_too_long_error(i18n, current, limit, book_count, prefs, is_multi_book,
                                 is_library_search=False):
    """Build a detailed prompt-too-long error message with actionable guidance."""
    over = max(0, current - limit)
    reduce_count = _estimate_reduce_books(current, limit, book_count) if book_count > 1 else 0

    if is_library_search:
        detail = i18n.get(
            'question_too_long_detail_library',
            'Prompt is too long ({current} characters, limit {limit}, over by {over}). '
            'Your library index contains {book_count} book(s).'
        ).format(current=current, limit=limit, over=over, book_count=book_count)
    else:
        detail = i18n.get(
            'question_too_long_detail',
            'Prompt is too long ({current} characters, limit {limit}, over by {over}). '
            'You selected {book_count} book(s).'
        ).format(current=current, limit=limit, over=over, book_count=book_count)

    parts = [detail]

    if is_library_search:
        parts.append(i18n.get(
            'question_too_long_hint_library_search',
            'Your library index exceeds the current prompt limit. Enable Custom prompt length limit '
            'in Plugin Configuration → General (suggested: 524288 characters), or ask a more '
            'specific question.'
        ))
    elif book_count > 1:
        parts.append(i18n.get(
            'question_too_long_hint_ai_search',
            'For library-wide searches, use AI Search (ask without selecting books, '
            'or use the AI Search menu) instead of selecting many books.'
        ))

        if reduce_count > 0:
            parts.append(i18n.get(
                'question_too_long_reduce_books',
                'To compare a smaller set in depth, try deselecting about {count} book(s).'
            ).format(count=reduce_count))

    if not prefs.get('enable_custom_prompt_limit'):
        mode_label = i18n.get('multi_book', 'Multi-Book') if is_multi_book else i18n.get('single_book', 'Single Book')
        parts.append(i18n.get(
            'question_too_long_hint_default',
            'Current default limit: {limit} characters ({mode}). '
            'Advanced users can enable a custom limit in Plugin Configuration → General.'
        ).format(limit=limit, mode=mode_label))
    else:
        parts.append(i18n.get(
            'question_too_long_hint_custom',
            'You enabled a custom prompt limit. If requests time out, lower the limit in '
            'Plugin Configuration → General, or reduce selected books / use a more specific query.'
        ))

    return '\n\n'.join(parts)


def validate_prompt_length(prompt, is_multi_book, prefs, i18n, book_count=0,
                           is_library_search=False):
    """
    Validate prompt length against configured limits.

    :return: None if valid, otherwise an error message string.
    """
    if not prompt:
        return None

    limit = get_max_prompt_length(is_multi_book, prefs)
    current = len(prompt)

    if current <= limit:
        return None

    logger.warning(
        'Prompt too long: %s chars (limit %s, books %s, multi=%s)',
        current, limit, book_count, is_multi_book,
    )
    return format_prompt_too_long_error(
        i18n, current, limit, book_count, prefs, is_multi_book, is_library_search,
    )
