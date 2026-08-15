#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Brave Search parsing and the web-search agent loop."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import web_search
import web_search_agent


BRAVE_FIXTURE = {
    'type': 'search',
    'query': {'original': 'artificial intelligence'},
    'web': {
        'results': [
            {
                'title': 'Artificial Intelligence - Overview',
                'url': 'https://example.com/ai',
                'description': 'Learn about artificial intelligence...',
            },
            {
                'title': 'Second result',
                'url': 'https://example.com/two',
                'description': 'More detail',
            },
            {
                'title': 'Third',
                'url': 'https://example.com/three',
            },
        ]
    },
}


class TestParseBraveResults(unittest.TestCase):
    def test_parses_title_url_description(self):
        rows = web_search.parse_brave_web_results(BRAVE_FIXTURE, limit=5)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['title'], 'Artificial Intelligence - Overview')
        self.assertEqual(rows[0]['url'], 'https://example.com/ai')
        self.assertEqual(rows[0]['description'], 'Learn about artificial intelligence...')

    def test_respects_limit(self):
        rows = web_search.parse_brave_web_results(BRAVE_FIXTURE, limit=1)
        self.assertEqual(len(rows), 1)

    def test_empty_and_invalid_payloads(self):
        self.assertEqual(web_search.parse_brave_web_results(None), [])
        self.assertEqual(web_search.parse_brave_web_results({}), [])
        self.assertEqual(web_search.parse_brave_web_results({'web': {'results': 'nope'}}), [])


class TestSearchWeb(unittest.TestCase):
    def test_missing_key_does_not_call_http(self):
        session = MagicMock()
        with self.assertRaises(web_search.WebSearchError) as ctx:
            web_search.search_web('hello', '', session=session)
        self.assertEqual(ctx.exception.error_type, 'missing_key')
        session.get.assert_not_called()

    def test_sends_subscription_token_header(self):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = BRAVE_FIXTURE
        session = MagicMock()
        session.get.return_value = response

        rows = web_search.search_web('artificial intelligence', 'secret-token', session=session)
        self.assertEqual(len(rows), 3)
        _args, kwargs = session.get.call_args
        self.assertEqual(kwargs['headers']['X-Subscription-Token'], 'secret-token')
        self.assertEqual(kwargs['params']['q'], 'artificial intelligence')
        self.assertEqual(kwargs['headers']['Accept'], 'application/json')

    def test_invalid_key_status(self):
        response = MagicMock()
        response.status_code = 401
        session = MagicMock()
        session.get.return_value = response
        with self.assertRaises(web_search.WebSearchError) as ctx:
            web_search.search_web('q', 'bad-key', session=session)
        self.assertEqual(ctx.exception.error_type, 'invalid_key')
        self.assertEqual(ctx.exception.status_code, 401)

    def test_rate_limited_status(self):
        response = MagicMock()
        response.status_code = 429
        session = MagicMock()
        session.get.return_value = response
        with self.assertRaises(web_search.WebSearchError) as ctx:
            web_search.search_web('q', 'key', session=session)
        self.assertEqual(ctx.exception.error_type, 'rate_limited')


class TestAgentDecision(unittest.TestCase):
    def test_parses_search_queries(self):
        action, payload = web_search_agent.parse_agent_decision(
            'Sure.\n<search>\nlatest SpaceX launch\nStarship flight\n</search>'
        )
        self.assertEqual(action, 'search')
        self.assertEqual(payload, ['latest SpaceX launch', 'Starship flight'])

    def test_parses_answer_tag_and_plain_answer(self):
        action, payload = web_search_agent.parse_agent_decision('<answer>Final text</answer>')
        self.assertEqual(action, 'answer')
        self.assertEqual(payload, 'Final text')
        action, payload = web_search_agent.parse_agent_decision('Just the answer.')
        self.assertEqual(action, 'answer')
        self.assertEqual(payload, 'Just the answer.')

    def test_deduplicates_queries_across_rounds(self):
        asks = [
            '<search>\nSpaceX launch\nSpaceX launch\n</search>',
            'The launch happened last week.',
        ]

        def ask_fn(_prompt):
            return asks.pop(0)

        searches = []

        def search_fn(query):
            searches.append(query)
            return [{'title': 'T', 'url': 'https://ex.com', 'description': 'D'}]

        agent = web_search_agent.WebSearchAgent(
            ask_fn=ask_fn,
            api_key='k',
            search_fn=search_fn,
        )
        result = agent.run('What launched?')
        self.assertEqual(searches, ['SpaceX launch'])
        self.assertIn('The launch happened last week.', result)
        self.assertIn('https://ex.com', result)

    def test_answers_on_first_round_without_search(self):
        agent = web_search_agent.WebSearchAgent(
            ask_fn=lambda _p: 'Two plus two is four.',
            api_key='k',
            search_fn=lambda _q: self.fail('should not search'),
        )
        result = agent.run('What is 2+2?')
        self.assertEqual(result, 'Two plus two is four.')

    def test_caps_rounds_and_force_answers(self):
        searches = []

        def search_fn(query):
            searches.append(query)
            return [{'title': query, 'url': 'https://ex.com/' + query, 'description': ''}]

        ask_calls = {'n': 0}

        def counting_ask(prompt):
            ask_calls['n'] += 1
            if 'no further searches' in prompt or 'Do not output <search>' in prompt:
                return 'Summary from gathered results.'
            return '<search>\nquery-{0}\n</search>'.format(ask_calls['n'])

        agent = web_search_agent.WebSearchAgent(
            ask_fn=counting_ask,
            api_key='k',
            max_rounds=2,
            search_fn=search_fn,
        )
        result = agent.run('Latest news?')
        self.assertLessEqual(len(searches), 2)
        self.assertIn('Summary from gathered results.', result)

    def test_invalid_key_still_answers(self):
        def search_fn(_query):
            raise web_search.WebSearchError('bad key', error_type='invalid_key', status_code=401)

        replies = [
            '<search>\nbreaking news\n</search>',
            'I will answer without more search.',
        ]

        def ask_fn(_prompt):
            return replies.pop(0)

        agent = web_search_agent.WebSearchAgent(
            ask_fn=ask_fn,
            api_key='bad',
            search_fn=search_fn,
        )
        result = agent.run('What happened?')
        self.assertIn('bad key', result)
        self.assertIn('I will answer without more search.', result)


if __name__ == '__main__':
    unittest.main()
