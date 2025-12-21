#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
版本信息模块

此模块集中管理插件的版本信息，确保所有引用版本号的地方保持一致。
"""

# 版本号元组，用于 Calibre 插件系统
VERSION = (1, 3, 7)

# 版本号字符串，用于显示
VERSION_STRING = '.'.join(map(str, VERSION))

# 完整版本号字符串（带 v 前缀），用于 UI 显示
VERSION_DISPLAY = f'v{VERSION_STRING}'

# 插件名称 - 与__init__.py中保持一致
PLUGIN_NAME = 'Ask AI Plugin'

# 插件描述 - 与__init__.py中保持一致
PLUGIN_DESCRIPTION = 'Ask questions about a book using AI'

# 作者信息
AUTHOR = 'Sheldon'
AUTHOR_EMAIL = 'sheldonrrr@gmail.com'

# 关键词
KEYWORDS = 'bookAI readingAI x.AI GrokAI GeminiAI'
