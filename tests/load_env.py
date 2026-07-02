#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Load variables from a local .env file into os.environ (minimal, no dependencies)."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(env_path: Path | None = None) -> bool:
    """
    Parse KEY=VALUE lines from .env into os.environ (setdefault, no override).

    :return: True if the file was found and read.
    """
    if env_path is None:
        env_path = Path(__file__).resolve().parents[1] / '.env'

    if not env_path.is_file():
        return False

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        os.environ.setdefault(key, value)

    return True
