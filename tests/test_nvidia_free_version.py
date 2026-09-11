#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Nvidia Free health/chat headers must report the current plugin version."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import version


class TestNvidiaFreeVersionHeaders(unittest.TestCase):
    def test_plugin_version_is_not_hardcoded_100(self):
        self.assertNotEqual(version.VERSION_STRING, '1.0.0')
        self.assertRegex(version.VERSION_STRING, r'^\d+\.\d+\.\d+$')

    def test_nvidia_free_docs_use_current_plugin_version(self):
        text = (ROOT / 'aiprovider' / 'nvidia_free.md').read_text(encoding='utf-8')
        self.assertNotIn('X-Plugin-Version: 1.0.0', text)
        self.assertIn('X-Plugin-Version: {}'.format(version.VERSION_STRING), text)
        self.assertRegex(
            text,
            r'"version":\s*"' + re.escape(version.VERSION_STRING) + r'"',
        )
        self.assertIn('GET /api/health', text)
        self.assertNotIn('Reply with the single word pong', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
