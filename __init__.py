#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPL v3'
__copyright__ = '2024, Sheldon'
__docformat__ = 'restructuredtext en'

from calibre.customize import InterfaceActionBase
import os
import sys

# 添加 lib 目录到 Python 路径
lib_dir = os.path.join(os.path.dirname(__file__), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

class AskGPTPlugin(InterfaceActionBase):
    name                = 'Ask Grok'
    description         = '使用 X.AI Grok 询问关于当前书籍的问题'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)
    icon                = 'images/ask_gpt.png'

    actual_plugin = 'calibre_plugins.ask_gpt.ui:AskGPTPluginUI'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.ask_gpt.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        # 只保存配置，不尝试重新初始化 API
        config_widget.save_settings()
        # Apply the changes
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
        else:
            print("Warning: actual_plugin_ is None in save_settings")

# 添加阅读器插件
from calibre_plugins.ask_gpt.viewer_plugin import AskGPTViewerPlugin