#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Nvidia Free docs stay public-safe; plugin version is not hardcoded 1.0.0."""

from __future__ import annotations

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

    def test_nvidia_free_docs_omit_internal_proxy_details(self):
        text = (ROOT / 'aiprovider' / 'nvidia_free.md').read_text(encoding='utf-8')
        self.assertNotIn('workers.dev', text)
        self.assertNotIn('X-Plugin-Version', text)
        self.assertNotIn('X-User-UUID', text)
        self.assertNotIn('X-Device-Fingerprint', text)
        self.assertNotIn('/api/health', text)
        self.assertNotIn('/api/chat', text)
        self.assertIn('nvidia_free', text)
        self.assertIn('Do not hack', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
