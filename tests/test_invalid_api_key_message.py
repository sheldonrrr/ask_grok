#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""SpaceXSI rejects a bad key with HTTP 400, not 401."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_base():
    spec = importlib.util.spec_from_file_location(
        'ask_ai_models_base_under_test',
        ROOT / 'models' / 'base.py',
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestInvalidApiKeyDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _load_base()

    def test_spacexsi_400_incorrect_api_key(self):
        body = (
            '{"code":"invalid-argument","error":'
            '"Incorrect API key provided. You can obtain an API key from https://console.x.ai."}'
        )
        self.assertTrue(self.base.response_indicates_invalid_api_key(400, body))

    def test_plain_401(self):
        self.assertTrue(self.base.response_indicates_invalid_api_key(401, ''))

    def test_parameter_400_is_not_an_auth_failure(self):
        body = '{"error":"max_output_tokens must be at least 1"}'
        self.assertFalse(self.base.response_indicates_invalid_api_key(400, body))


if __name__ == '__main__':
    unittest.main()
