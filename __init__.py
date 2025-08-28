#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__   = 'GPL v3'
__copyright__ = '2025, Sheldon'
__docformat__ = 'restructuredtext en'

from calibre.customize import InterfaceActionBase
import os
import sys
import json
import logging

# 首先设置插件目录和lib路径
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

# 添加 lib 目录到 Python 路径，确保在导入任何第三方库之前
lib_dir = os.path.join(PLUGIN_DIR, 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)
    print(f'已添加lib目录到Python路径: {lib_dir}')

# 版本信息 - 硬编码以确保跨平台兼容性
VERSION = (1, 2, 3) # 版本号推送触发
VERSION_STRING = '.'.join(map(str, VERSION))
PLUGIN_NAME = 'Ask Grok'
PLUGIN_DESCRIPTION = 'Ask questions about a book using AI'
AUTHOR = 'Sheldon'
AUTHOR_EMAIL = 'sheldonrrr@gmail.com'
KEYWORDS = 'bookAI readingAI x.AI GrokAI GeminiAI'

# 配置日志
import tempfile
import os
from calibre.utils.config import config_dir

# 创建插件日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_grok_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_grok_debug.log')

# 获取根日志记录器
root_logger = logging.getLogger()

# 检查是否已经添加过处理器，避免重复添加
handlers_exist = False
for handler in root_logger.handlers:
    if isinstance(handler, logging.FileHandler) and handler.baseFilename == log_file:
        handlers_exist = True
        break

# 只有在没有处理器时才添加，避免重复
if not handlers_exist:
    # 配置根日志记录器
    root_logger.setLevel(logging.DEBUG)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到根日志记录器
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    print(f'已配置Ask Grok日志系统，日志文件位置: {log_file}')

logger = logging.getLogger(__name__)
logger.info(f'Ask Grok 插件启动，日志文件位置: {log_file}')

PLUGIN_ICON = 'images/icon.png'

class AskGrokPlugin(InterfaceActionBase):
    name                = 'Ask Grok'
    description         = 'Ask questions about a book using AI'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 2, 3)
    minimum_calibre_version = (7, 0, 0)
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


# 添加图标加载函数
def get_icons(icon_name):
    """
    获取插件图标
    """
    from PyQt5.QtGui import QIcon
    import os
    
    # 使用绝对路径加载图标
    icon_path = os.path.join(PLUGIN_DIR, icon_name)
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    
    # 如果文件不存在，返回空图标
    return QIcon()