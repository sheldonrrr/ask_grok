#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = 'GPL v3'
__copyright__ = '2024'
__docformat__ = 'restructuredtext en'

from calibre.customize import InterfaceActionBase

class AskGPTPlugin(InterfaceActionBase):
    name                = 'Ask GPT'
    description         = '使用 ChatGPT 询问关于当前书籍的问题'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Sheldon'
    version = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin = 'calibre_plugins.ask_gpt.ui:AskGPTPluginUI'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.ask_gpt.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()

        # Apply the changes
        ac= self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
