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
VERSION = (1, 6, 2) # 版本号推送触发
VERSION_STRING = '.'.join(map(str, VERSION))
PLUGIN_NAME = 'Ask AI Plugin'
PLUGIN_DESCRIPTION = 'Ask questions about books using multiple AI providers'
AUTHOR = 'Sheldon'
AUTHOR_EMAIL = 'sheldonrrr@gmail.com'
KEYWORDS = 'bookAI readingAI multiAI OpenAI Anthropic Gemini DeepSeek Kimi Moonshot Mistral Nvidia Ollama'

logger = logging.getLogger(__name__)

PLUGIN_ICON = 'images/icon.png'

class AskAIPlugin(InterfaceActionBase):
    name                = 'Ask AI Plugin'
    description         = 'Ask questions about books using multiple AI providers'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sheldon'
    version             = (1, 6, 2)
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
        Prefer calibre's plugin_path / load_resources; fall back to PLUGIN_DIR
        and zip path heuristics for older installs and development trees.
        '''
        import os
        import sys
        from zipfile import ZipFile
        
        logger = logging.getLogger(__name__)
        logger.info(f"[get_resources] 请求资源: {name}")
        logger.info(f"[get_resources] PLUGIN_DIR: {PLUGIN_DIR}")

        plugin_path_attr = getattr(self, 'plugin_path', None)
        direct_path = os.path.join(PLUGIN_DIR, name)
        possible_names = [
            name,
            f'calibre_plugins/ask_ai_plugin/{name}',
            f'ask_ai_plugin/{name}',
        ]

        def _read_from_zip(plugin_zip):
            with ZipFile(plugin_zip, 'r') as zf:
                names = zf.namelist()
                logger.info(f"[get_resources] zip文件列表: {names[:20]}")
                for possible_name in possible_names:
                    if possible_name in names:
                        logger.info(f"[get_resources] 在zip中找到: {possible_name}")
                        data = zf.read(possible_name)
                        logger.info(f"[get_resources] 成功读取 {len(data)} 字节")
                        return data
                logger.warning(f"[get_resources] 在zip中未找到资源: {name}")
            return None

        # Method 1: calibre official plugin_path (most reliable for installed zips)
        if plugin_path_attr and os.path.isfile(plugin_path_attr):
            try:
                resources = self.load_resources([name])
                data = resources.get(name)
                if data:
                    logger.info(f"[get_resources] load_resources 成功读取 {len(data)} 字节")
                    return data
            except Exception as e:
                logger.info(f"[get_resources] load_resources 未命中/失败: {e}")
            try:
                data = _read_from_zip(plugin_path_attr)
                if data:
                    return data
            except Exception as e:
                logger.error(f"[get_resources] 从 plugin_path zip 读取失败: {e}", exc_info=True)

        # Method 2: direct file access (development / extracted tree)
        logger.info(f"[get_resources] 尝试直接访问: {direct_path}")
        if os.path.exists(direct_path) and os.path.isfile(direct_path):
            logger.info(f"[get_resources] 找到文件，直接读取")
            with open(direct_path, 'rb') as f:
                data = f.read()
            logger.info(f"[get_resources] 成功读取 {len(data)} 字节")
            return data

        # Method 3: PLUGIN_DIR-as-zip or sys.path heuristics
        logger.info(f"[get_resources] 直接访问失败，尝试从zip读取")
        plugin_zip = None
        if PLUGIN_DIR.endswith('.zip') and os.path.isfile(PLUGIN_DIR):
            plugin_zip = PLUGIN_DIR
            logger.info(f"[get_resources] PLUGIN_DIR就是zip文件: {plugin_zip}")
        else:
            for path in sys.path:
                path_l = str(path).lower()
                if (
                    path_l.endswith('.zip')
                    and os.path.exists(path)
                    and ('ask ai plugin' in path_l or 'ask_ai_plugin' in path_l)
                ):
                    plugin_zip = path
                    logger.info(f"[get_resources] 在sys.path找到插件zip: {plugin_zip}")
                    break

        if plugin_zip and os.path.isfile(plugin_zip):
            try:
                data = _read_from_zip(plugin_zip)
                if data:
                    return data
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