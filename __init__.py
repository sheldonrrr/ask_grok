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

# 设置插件目录
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

# 注意：第三方库已移至 lib/ask_ai_plugin_vendor/ 命名空间
# 不再需要 sys.path.insert，所有导入使用完整的命名空间路径
# 这样可以避免与其他 calibre 插件的依赖冲突

# 版本信息 - 硬编码以确保跨平台兼容性
VERSION = (1, 3, 4) # 版本号推送触发
VERSION_STRING = '.'.join(map(str, VERSION))
PLUGIN_NAME = 'Ask AI Plugin'
PLUGIN_DESCRIPTION = 'Ask questions about books using multiple AI providers'
AUTHOR = 'Sheldon'
AUTHOR_EMAIL = 'sheldonrrr@gmail.com'
KEYWORDS = 'bookAI readingAI multiAI OpenAI Anthropic Gemini DeepSeek Nvidia Ollama'

# 配置日志
import tempfile
import os
from calibre.utils.config import config_dir

# 创建插件日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_ai_plugin_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_ai_plugin_debug.log')

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
    
    # 只在首次配置时输出一次日志信息
    logger = logging.getLogger(__name__)
    logger.info(f'Ask AI Plugin 日志系统已配置，日志文件: {log_file}')

PLUGIN_ICON = 'images/icon.png'

class AskAIPlugin(InterfaceActionBase):
    name                = 'Ask AI Plugin'
    description         = 'Ask questions about books using multiple AI providers'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 3, 4)
    minimum_calibre_version = (6, 0, 0)
    icon                = 'images/ask_ai_plugin.png'

    # Declare the main action associated with this plugin
    # The keyboard shortcut can be None if you dont want to use a keyboard
    # shortcut. Remember that currently calibre has no central management for
    # keyboard shortcuts, so try to use an unusual/unused shortcut.
    actual_plugin = 'calibre_plugins.ask_ai_plugin.ui:AskAIPluginUI'
    
    def is_customizable(self):
        return True
    
    def get_resources(self, name):
        '''
        Load resources files that are packaged with the plugin zip file.
        '''
        import os
        import sys
        from zipfile import ZipFile
        
        logger = logging.getLogger(__name__)
        logger.info(f"[get_resources] 请求资源: {name}")
        logger.info(f"[get_resources] PLUGIN_DIR: {PLUGIN_DIR}")
        
        # Method 1: Try direct file access (for development)
        path = os.path.join(PLUGIN_DIR, name)
        logger.info(f"[get_resources] 尝试直接访问: {path}")
        
        if os.path.exists(path) and os.path.isfile(path):
            logger.info(f"[get_resources] 找到文件，直接读取")
            with open(path, 'rb') as f:
                data = f.read()
            logger.info(f"[get_resources] 成功读取 {len(data)} 字节")
            return data
        
        # Method 2: Try to read from zip file (when installed as plugin)
        logger.info(f"[get_resources] 直接访问失败，尝试从zip读取")
        
        # PLUGIN_DIR itself might be the zip file
        plugin_zip = None
        
        # First check if PLUGIN_DIR is the zip file
        if PLUGIN_DIR.endswith('.zip') and os.path.isfile(PLUGIN_DIR):
            plugin_zip = PLUGIN_DIR
            logger.info(f"[get_resources] PLUGIN_DIR就是zip文件: {plugin_zip}")
        else:
            # Otherwise search in sys.path
            for path in sys.path:
                if 'Ask AI Plugin.zip' in path and os.path.exists(path):
                    plugin_zip = path
                    logger.info(f"[get_resources] 在sys.path找到插件zip: {plugin_zip}")
                    break
        
        if plugin_zip and os.path.isfile(plugin_zip):
            try:
                with ZipFile(plugin_zip, 'r') as zf:
                    logger.info(f"[get_resources] zip文件列表: {zf.namelist()[:20]}")
                    
                    # Try different path formats
                    possible_names = [
                        name,
                        f'calibre_plugins/ask_ai_plugin/{name}',
                        f'ask_ai_plugin/{name}'
                    ]
                    
                    for possible_name in possible_names:
                        if possible_name in zf.namelist():
                            logger.info(f"[get_resources] 在zip中找到: {possible_name}")
                            data = zf.read(possible_name)
                            logger.info(f"[get_resources] 成功读取 {len(data)} 字节")
                            return data
                    
                    logger.warning(f"[get_resources] 在zip中未找到资源: {name}")
            except Exception as e:
                logger.error(f"[get_resources] 从zip读取失败: {e}", exc_info=True)
        else:
            logger.warning(f"[get_resources] 未找到插件zip文件")
        
        logger.error(f"[get_resources] 所有方法都失败")
        return None

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