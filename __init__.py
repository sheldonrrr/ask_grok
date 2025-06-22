#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPL v3'
__copyright__ = '2024, Sheldon'
__docformat__ = 'restructuredtext en'

from calibre.customize import InterfaceActionBase
import os
import sys
import json
import logging
from calibre_plugins.ask_grok import i18n

# 配置日志
import tempfile
import os
from calibre.utils.config import config_dir

# 创建插件日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_grok_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_grok_debug.log')

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info(f'Ask Grok 插件启动，日志文件位置: {log_file}')

PLUGIN_ICON = 'images/icon.png'
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

# 添加 lib 目录到 Python 路径
lib_dir = os.path.join(PLUGIN_DIR, 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

class AskGrokPlugin(InterfaceActionBase):
    name                = 'Ask Grok'
    description         = 'Ask Grok about this book'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 1, 19)
    minimum_calibre_version = (0, 7, 53)
    icon                = 'images/ask_grok.png'

    # Declare the main action associated with this plugin
    # The keyboard shortcut can be None if you dont want to use a keyboard
    # shortcut. Remember that currently calibre has no central management for
    # keyboard shortcuts, so try to use an unusual/unused shortcut.
    actual_plugin = 'calibre_plugins.ask_grok.ui:AskGrokPluginUI'
    
    def is_customizable(self):
        return True

    def load_actual_plugin(self, gui):
        '''
        This method must return the actual interface action plugin object.
        '''
        ac = getattr(self, 'actual_plugin_object', None)
        if ac is None:
            mod, cls = self.actual_plugin.split(':')
            from importlib import import_module
            ac = getattr(import_module(mod), cls)(gui, self.site_customization)
            self.actual_plugin_object = ac
        return ac

    def customization_help(self, gui=False):
        if getattr(self, 'actual_plugin_object', None) is not None:
            return self.actual_plugin_object.customization_help(gui)
        raise NotImplementedError()

    def config_widget(self):
        if getattr(self, 'actual_plugin_object', None) is not None:
            return self.actual_plugin_object.config_widget()
        raise NotImplementedError()

    def save_settings(self, config_widget):
        if getattr(self, 'actual_plugin_object', None) is not None:
            return self.actual_plugin_object.save_settings(config_widget)
        raise NotImplementedError()