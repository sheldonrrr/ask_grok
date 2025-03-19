#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = 'GPL v3'
__copyright__ = '2024'
__docformat__ = 'restructuredtext en'

from calibre.customize import InterfaceActionBase

class AskGPTPlugin(InterfaceActionBase):
    name                = 'Ask Grok'
    description         = '使用 X.AI Grok 询问关于当前书籍的问题'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)
    
    # 添加图标相关属性
    icon                = 'images/ask_gpt.png'
    priority            = 1
    can_be_disabled     = True
    default_state       = True

    actual_plugin = 'calibre_plugins.ask_gpt.ui:AskGPTPluginUI'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.ask_gpt.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        # 只保存配置，不尝试重新初始化 API
        config_widget.save_settings()
