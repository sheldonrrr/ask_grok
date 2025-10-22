# Critical Rules for AI Code Editing

## ⚠️ RED LINES - DO NOT MODIFY

These are critical components required by Calibre plugin architecture. **Modifying these incorrectly will cause the plugin to crash or fail to load.**

---

## 1. Plugin Import Name File

**File:** `plugin-import-name-ask_grok.txt`

**Content:** 
```
ask_grok
```

**Rules:**
- ❌ **NEVER** modify this file
- ❌ **NEVER** change the import name `ask_grok`
- ❌ **NEVER** delete this file
- ✅ This file defines the plugin's import namespace in Calibre
- ✅ Calibre uses this to load the plugin as `calibre_plugins.ask_grok`

**Why it matters:** Calibre's plugin system requires this exact import name to load the plugin correctly. Changing it will break all imports and make the plugin unloadable.

---

## 2. Plugin Class Definition

**File:** `__init__.py` (Lines 81-98)

**Critical Code Block:**
```python
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
```

**Rules:**
- ❌ **NEVER** change the class name `AskGrokPlugin`
- ❌ **NEVER** remove the inheritance from `InterfaceActionBase`
- ⚠️ **CAREFULLY** update `version` tuple when making releases (must be 3-integer tuple)
- ⚠️ **CAREFULLY** update `minimum_calibre_version` only if you add features requiring newer Calibre
- ❌ **NEVER** change `actual_plugin` path unless you rename/move the UI class
- ⚠️ **CAREFULLY** modify `supported_platforms` only if platform support changes
- ✅ Can safely update: `description`, `author` (if needed)
- ✅ Can safely update: `icon` path (if icon file is renamed/moved)

**Why it matters:** This is the entry point for Calibre's plugin system. The class attributes are read by Calibre to register and load the plugin.

---

## 3. Plugin Entry Point Methods

**File:** `__init__.py` (Lines 99-124)

**Critical Methods:**
```python
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
```

**Rules:**
- ❌ **NEVER** delete these methods
- ❌ **NEVER** change method signatures (names, parameters)
- ⚠️ **CAREFULLY** modify method bodies only if you understand Calibre's plugin loading mechanism
- ✅ These methods are required by Calibre's `InterfaceActionBase` interface

**Why it matters:** Calibre calls these methods to load and configure the plugin. Breaking them will prevent the plugin from loading or being configurable.

---

## 4. Import Structure

**File:** `__init__.py` (Lines 1-21)

**Critical Import Block:**
```python
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
```

**Rules:**
- ❌ **NEVER** remove the `InterfaceActionBase` import
- ❌ **NEVER** remove the `lib` directory path setup (lines 14-21)
- ⚠️ **CAREFULLY** add new imports only after the lib path is set up
- ✅ The lib directory setup must happen before importing third-party libraries

**Why it matters:** Calibre plugins must bundle their dependencies in a `lib` folder. This code ensures those dependencies are found before any imports that need them.

---

## 5. UI Plugin Class

**File:** `ui.py` (Lines 46-50)

**Critical Code:**
```python
class AskGrokPluginUI(InterfaceAction):
    name = 'Ask Grok'
    # 根据操作系统设置不同的快捷键
    action_spec = ('Ask Grok', 'images/ask_grok.png', 'Ask Grok about this book', 
                  'Ctrl+L')
```

**Rules:**
- ❌ **NEVER** change the class name `AskGrokPluginUI`
- ❌ **NEVER** remove the inheritance from `InterfaceAction`
- ⚠️ **CAREFULLY** modify `action_spec` tuple (must be 4-element tuple: name, icon, tooltip, shortcut)
- ✅ Can safely update: shortcut key, tooltip text, icon path

**Why it matters:** This is the actual UI implementation that `__init__.py` loads. The class name must match the `actual_plugin` path.

---

## 6. Version Management

**File:** `__init__.py` (Lines 23-30)

**Critical Code:**
```python
# 版本信息 - 硬编码以确保跨平台兼容性
VERSION = (1, 2, 3) # 版本号推送触发
VERSION_STRING = '.'.join(map(str, VERSION))
PLUGIN_NAME = 'Ask Grok'
PLUGIN_DESCRIPTION = 'Ask questions about a book using AI'
AUTHOR = 'Sheldon'
AUTHOR_EMAIL = 'sheldonrrr@gmail.com'
KEYWORDS = 'bookAI readingAI x.AI GrokAI GeminiAI'
```

**Rules:**
- ⚠️ **CAREFULLY** update `VERSION` tuple - must match the version in `AskGrokPlugin.version`
- ⚠️ **CAREFULLY** keep `VERSION` and `AskGrokPlugin.version` synchronized
- ✅ Can safely update: `PLUGIN_DESCRIPTION`, `KEYWORDS`
- ✅ Update `AUTHOR_EMAIL` only if ownership changes

**Why it matters:** Version inconsistencies can cause update issues in Calibre's plugin manager.

---

## 7. Configuration System

**File:** `config.py` (Lines 26-27)

**Critical Code:**
```python
# 创建配置对象
prefs = JSONConfig('plugins/ask_grok')
```

**Rules:**
- ❌ **NEVER** change the config path `'plugins/ask_grok'`
- ❌ **NEVER** rename the `prefs` variable without updating all references
- ⚠️ **CAREFULLY** add new config defaults using `prefs.defaults['key'] = value`
- ✅ Can safely add new configuration options

**Why it matters:** Changing the config path will lose all user settings. The path must match the plugin import name.

---

## 8. Logging System

**File:** `__init__.py` (Lines 32-77)

**Critical Code:**
```python
# 创建插件日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_grok_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_grok_debug.log')
```

**Rules:**
- ⚠️ **CAREFULLY** modify logging configuration
- ❌ **NEVER** remove the log directory creation
- ✅ Can safely adjust log levels and formats
- ✅ Can safely add new loggers

**Why it matters:** Logging is critical for debugging user issues. Breaking it makes troubleshooting impossible.

---

## 9. Third-Party Dependencies

**File:** `lib/` directory

**Rules:**
- ❌ **NEVER** delete the `lib` directory
- ⚠️ **CAREFULLY** update dependencies - test thoroughly on all platforms
- ⚠️ **CAREFULLY** ensure dependencies are compatible with Calibre's Python version
- ✅ Can safely add new dependencies to `lib/`
- ✅ Must update `requirements.txt` when adding dependencies

**Current Dependencies:**
- `requests` - HTTP requests to AI APIs
- `bleach` - HTML sanitization
- `markdown2` - Markdown rendering

**Why it matters:** Calibre plugins must bundle all dependencies. Missing or incompatible dependencies will crash the plugin.

---

## 10. Icon Resources

**File:** `images/` directory

**Critical Icons:**
- `images/ask_grok.png` - Main plugin icon (referenced in `__init__.py` line 88)

**Rules:**
- ❌ **NEVER** delete `images/ask_grok.png` without updating the reference
- ⚠️ **CAREFULLY** ensure icon files are in supported formats (PNG, JPG)
- ✅ Can safely add new icon files
- ✅ Must update references if renaming icon files

**Why it matters:** Missing icons will cause the plugin to fail loading or display incorrectly in Calibre's UI.

---

## General Development Rules

### DO NOT:
1. ❌ Change the plugin import name (`ask_grok`)
2. ❌ Modify the plugin class structure without understanding Calibre's API
3. ❌ Remove required Calibre imports (`InterfaceActionBase`, `InterfaceAction`)
4. ❌ Break the lib directory path setup
5. ❌ Change config storage path
6. ❌ Remove or rename critical methods required by Calibre
7. ❌ Modify version numbers without synchronizing all references
8. ❌ Delete bundled dependencies without ensuring they're not needed

### DO:
1. ✅ Test on all supported platforms (Windows, macOS, Linux) after changes
2. ✅ Keep version numbers synchronized across files
3. ✅ Update `requirements.txt` when adding dependencies
4. ✅ Add logging for new features to aid debugging
5. ✅ Follow existing code style and patterns
6. ✅ Update documentation when adding features
7. ✅ Test with minimum Calibre version (7.0.0) if possible
8. ✅ Validate that the plugin loads in Calibre after changes

### CAREFULLY MODIFY:
1. ⚠️ Plugin metadata (name, description, version)
2. ⚠️ Configuration defaults and structure
3. ⚠️ UI layout and widgets
4. ⚠️ API client implementations
5. ⚠️ Internationalization (i18n) files
6. ⚠️ Model configurations

---

## Testing Checklist

Before committing changes, verify:

- [ ] Plugin loads in Calibre without errors
- [ ] Configuration dialog opens and saves settings
- [ ] Main UI dialog opens and functions correctly
- [ ] API calls work with configured providers
- [ ] No Python import errors in Calibre's debug log
- [ ] Version numbers are synchronized
- [ ] All required files are present
- [ ] Icons display correctly
- [ ] Keyboard shortcuts work
- [ ] Plugin can be uninstalled and reinstalled

---

## Emergency Recovery

If the plugin breaks after modifications:

1. Check Calibre's debug log: `Preferences` → `Advanced` → `Miscellaneous` → `View Calibre Debug Log`
2. Check plugin log: `~/.config/calibre/plugins/ask_grok_logs/ask_grok_debug.log`
3. Restore critical files from version control
4. Verify `plugin-import-name-ask_grok.txt` is intact
5. Verify `__init__.py` class definition is intact
6. Verify `lib` directory path setup is intact
7. Reinstall the plugin in Calibre

---

## Contact

For questions about these rules or Calibre plugin development:
- Calibre Plugin Development Guide: https://manual.calibre-ebook.com/creating_plugins.html
- Plugin Author: sheldonrrr@gmail.com
