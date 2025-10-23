# Plugin Rename Checklist: Ask Grok → Ask AI Plugin

## 重要说明

⚠️ **关键约束**：根据 `CRITICAL_RULES.md`，以下内容**不能修改**：
- `plugin-import-name-ask_grok.txt` 文件
- Python 导入路径 `calibre_plugins.ask_grok`
- 类名 `AskGrokPlugin` 和 `AskGrokPluginUI`

这些是 Calibre 插件架构的核心要求，修改会导致插件无法加载。

---

## 修改清单

### 1. 插件元数据 (高优先级)

#### 1.1 `__init__.py`
- [ ] Line 26: `PLUGIN_NAME = 'Ask Grok'` → `'Ask AI Plugin'`
- [ ] Line 27: `PLUGIN_DESCRIPTION` 可选更新
- [ ] Line 30: `KEYWORDS` 更新为更通用的关键词
- [ ] Line 74: 日志消息 `'已配置Ask Grok日志系统'` → `'已配置Ask AI Plugin日志系统'`
- [ ] Line 77: 日志消息 `'Ask Grok 插件启动'` → `'Ask AI Plugin 插件启动'`
- [ ] Line 82: `name = 'Ask Grok'` → `'Ask AI Plugin'`
- [ ] Line 83: `description` 可选更新
- [ ] Line 88: `icon = 'images/ask_grok.png'` → `'images/ask_ai_plugin.png'` (需要重命名图标文件)

**注意**：
- ❌ 不要修改 Line 81: `class AskGrokPlugin` (必须保持)
- ❌ 不要修改 Line 94: `actual_plugin = 'calibre_plugins.ask_grok.ui:AskGrokPluginUI'` (必须保持)

---

### 2. 国际化文件 (高优先级)

需要在所有语言文件中更新 `plugin_name` 和 `about_plugin` 键：

#### 2.1 英文 (`i18n/en.py`)
- [ ] Line 35: `'plugin_name': 'Ask Grok'` → `'Ask AI Plugin'`
- [ ] Line 185: `'about_plugin': 'Why Ask Grok?'` → `'Why Ask AI Plugin?'`

#### 2.2 简体中文 (`i18n/zh.py`)
- [ ] Line 35: `'plugin_name': 'Ask Grok'` → `'Ask AI Plugin'`
- [ ] Line 187: `'about_plugin': '关于 Ask Grok'` → `'关于 Ask AI Plugin'`

#### 2.3 繁体中文 (`i18n/zht.py`)
- [ ] Line 35: `'plugin_name': 'Ask Grok'` → `'Ask AI Plugin'`
- [ ] Line 182: `'about_plugin': '為何使用 Ask Grok？'` → `'為何使用 Ask AI Plugin？'`

#### 2.4 其他语言文件
需要更新以下文件中的相同键：
- [ ] `i18n/fi.py` (Finnish)
- [ ] `i18n/nl.py` (Dutch)
- [ ] `i18n/es.py` (Spanish)
- [ ] `i18n/sv.py` (Swedish)
- [ ] `i18n/da.py` (Danish)
- [ ] `i18n/de.py` (German)
- [ ] `i18n/fr.py` (French)
- [ ] `i18n/it.py` (Italian)
- [ ] `i18n/ja.py` (Japanese)
- [ ] `i18n/ko.py` (Korean)
- [ ] `i18n/no.py` (Norwegian)
- [ ] `i18n/pt.py` (Portuguese)
- [ ] `i18n/ru.py` (Russian)
- [ ] `i18n/yue.py` (Cantonese)

---

### 3. 配置路径 (中优先级)

#### 3.1 配置存储路径
当前使用 `JSONConfig('plugins/ask_grok')`，这会影响配置文件位置。

**选项 A：保持不变** (推荐)
- 优点：用户配置不会丢失
- 缺点：配置路径与插件名不一致

**选项 B：迁移配置**
- 需要在 `__init__.py` 或首次加载时添加迁移逻辑
- 将 `~/.config/calibre/plugins/ask_grok.json` 迁移到 `ask_ai_plugin.json`

**涉及文件**：
- [ ] `api.py` Line 258: `JSONConfig('plugins/ask_grok')`
- [ ] `api.py` Line 319: `JSONConfig('plugins/ask_grok')`
- [ ] `config.py` 中所有 `get_prefs()` 调用 (已封装，无需修改)

---

### 4. 日志路径 (中优先级)

#### 4.1 日志目录名称
当前使用 `ask_grok_logs`，可以选择更新：

**涉及文件**：
- [ ] `__init__.py` Line 38: `'plugins', 'ask_grok_logs'` → `'plugins', 'ask_ai_plugin_logs'`
- [ ] `__init__.py` Line 40: `'ask_grok_debug.log'` → `'ask_ai_plugin_debug.log'`
- [ ] `response_handler.py` Line 22: `'plugins', 'ask_grok_logs'` → `'plugins', 'ask_ai_plugin_logs'`
- [ ] `response_handler.py` Line 24: `'ask_grok_response.log'` → `'ask_ai_plugin_response.log'`

---

### 5. 图标文件 (高优先级)

#### 5.1 重命名图标文件
- [ ] `images/ask_grok.png` → `images/ask_ai_plugin.png`
- [ ] 更新 `__init__.py` Line 88 中的引用

---

### 6. 文档文件 (低优先级)

#### 6.1 README 和文档
- [ ] `README.md` - 更新所有提到 "Ask Grok" 的地方
- [ ] `docs/CRITICAL_RULES.md` - 更新示例和说明
- [ ] `docs/PROJECT_STRUCTURE.md` - 更新项目描述
- [ ] `docs/FEATURE_*.md` - 更新功能文档中的插件名称

---

### 7. 注释和文档字符串 (低优先级)

需要搜索并更新所有 Python 文件中的：
- [ ] 文件头部的文档字符串 (如 `"""English language translations for Ask Grok plugin."""`)
- [ ] 注释中提到的插件名称

**涉及的主要文件**：
- 所有 `i18n/*.py` 文件的文档字符串
- `ui.py`, `config.py`, `api.py` 等核心文件的注释

---

## 不需要修改的内容

以下内容**不应该修改**，因为它们是 Calibre 插件系统的要求：

1. ❌ `plugin-import-name-ask_grok.txt` 文件内容
2. ❌ 类名 `AskGrokPlugin`
3. ❌ 类名 `AskGrokPluginUI`
4. ❌ 导入路径 `calibre_plugins.ask_grok`
5. ❌ `actual_plugin = 'calibre_plugins.ask_grok.ui:AskGrokPluginUI'`
6. ❌ 所有 Python 文件中的 `from calibre_plugins.ask_grok import ...` 导入语句
7. ❌ 项目目录名 `ask_grok` (可以保持，不影响显示名称)

---

## 实施建议

### 阶段 1：核心显示名称 (必须)
1. 更新 `__init__.py` 中的插件元数据
2. 更新所有 i18n 文件中的 `plugin_name` 和 `about_plugin`
3. 重命名并更新图标文件引用

### 阶段 2：配置和日志 (可选)
1. 决定是否迁移配置路径
2. 更新日志目录名称

### 阶段 3：文档和注释 (可选)
1. 更新 README 和文档
2. 更新代码注释和文档字符串

---

## 测试清单

完成修改后，需要测试：

- [ ] 插件能否正常加载
- [ ] 插件名称在 Calibre 界面中正确显示为 "Ask AI Plugin"
- [ ] 图标正确显示
- [ ] 配置对话框标题正确
- [ ] About 页面显示正确的插件名称
- [ ] 所有语言的翻译正确显示
- [ ] 现有用户配置不丢失（如果保持配置路径不变）
- [ ] 日志文件正常写入

---

## 风险评估

**低风险**：
- 更新显示名称和翻译
- 更新文档和注释

**中风险**：
- 更改配置路径（需要迁移逻辑）
- 更改日志路径（用户需要知道新位置）

**高风险**：
- 修改类名或导入路径（会导致插件崩溃）

---

## 总结

**必须修改**：
- 插件元数据 (name, description)
- 所有 i18n 文件中的显示名称
- 图标文件名

**建议保持不变**：
- 配置路径 `plugins/ask_grok`（避免用户配置丢失）
- 日志路径（或提供迁移说明）
- 所有内部类名和导入路径

**估计工作量**：
- 核心修改：30-60 分钟
- 完整修改（包括文档）：2-3 小时
- 测试：30-60 分钟
