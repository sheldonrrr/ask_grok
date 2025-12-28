# Ask AI Plugin - 数据结构文档（开发版本）

本文档记录了 Ask AI Plugin 插件**开发版本**存储的所有数据结构，用于版本兼容性维护和数据迁移。

## 文档版本
- **插件版本**: v1.3.9 (开发版本)
- **文档创建日期**: 2024-12-28
- **最后更新**: 2024-12-28
- **对比版本**: v1.3.8 (稳定版本)

---

## 一、存储文件位置

插件使用 Calibre 的配置目录存储数据，路径为：`{calibre_config_dir}/plugins/`

### 1.1 配置文件
- **文件名**: `ask_ai_plugin.json`
- **完整路径**: `{calibre_config_dir}/plugins/ask_ai_plugin.json`
- **存储方式**: Calibre JSONConfig
- **用途**: 存储所有插件配置，包括 AI 配置、界面设置、模板等

### 1.2 历史记录文件
- **文件名（当前版本）**: `ask_ai_plugin_history_v2.json`
- **文件名（旧版本）**: `ask_ai_plugin_latest_history.json`
- **完整路径**: `{calibre_config_dir}/plugins/ask_ai_plugin_history_v2.json`
- **存储方式**: 标准 JSON 文件
- **用途**: 存储用户的问询历史记录

### 1.3 日志文件
- **目录**: `{calibre_config_dir}/plugins/ask_ai_plugin_logs/`
- **文件名**: `ask_ai_plugin_debug.log`
- **用途**: 调试日志（仅在启用调试模式时）

---

## 二、配置文件数据结构 (ask_ai_plugin.json)

### 2.1 顶层配置结构

```json
{
  "selected_model": "grok",
  "models": { /* AI 模型配置，见 2.2 */ },
  "template": "单书提示词模板文本",
  "multi_book_template": "多书提示词模板文本",
  "language": "en",
  "language_user_set": false,
  "ask_dialog_width": 800,
  "ask_dialog_height": 600,
  "random_questions": "随机问题提示词模板",
  "request_timeout": 60,
  "parallel_ai_count": 1,
  "cached_models": { /* 缓存的模型列表，见 2.4 */ },
  "enable_default_export_folder": false,
  "default_export_folder": "",
  "copy_mode": "response",
  "export_mode": "current",
  "use_persona": true,
  "persona": "As a researcher, I want to research through book data.",
  "use_interface_language": false,
  "enable_debug_logging": false
}
```

### 2.2 AI 模型配置结构 (models)

每个 AI 提供商都有独立的配置对象，键名为提供商 ID。

#### 2.2.1 通用字段（所有 AI 提供商共有）

```json
{
  "api_key": "API密钥字符串",
  "api_base_url": "API基础URL",
  "model": "模型名称",
  "display_name": "显示名称",
  "enabled": true,
  "is_configured": true,
  "use_custom_model_name": false
}
```

#### 2.2.2 Grok 配置

```json
{
  "auth_token": "xai-xxx",
  "api_base_url": "https://api.x.ai/v1",
  "model": "grok-beta",
  "display_name": "Grok",
  "enabled": true,
  "is_configured": true,
  "use_custom_model_name": false
}
```

#### 2.2.3 Gemini 配置

```json
{
  "api_key": "",
  "api_base_url": "https://generativelanguage.googleapis.com/v1beta",
  "model": "gemini-2.0-flash-exp",
  "display_name": "Gemini",
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.4 DeepSeek 配置

```json
{
  "api_key": "",
  "api_base_url": "https://api.deepseek.com",
  "model": "deepseek-chat",
  "display_name": "DeepSeek",
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.5 Custom (自定义) 配置

```json
{
  "api_key": "",
  "api_base_url": "https://api.example.com/v1",
  "model": "custom-model",
  "display_name": "Custom",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.6 OpenAI 配置

```json
{
  "api_key": "",
  "api_base_url": "https://api.openai.com/v1",
  "model": "gpt-4o",
  "display_name": "OpenAI",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.7 Anthropic 配置

```json
{
  "api_key": "",
  "api_base_url": "https://api.anthropic.com",
  "model": "claude-3-5-sonnet-20241022",
  "display_name": "Anthropic",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.8 Nvidia 配置

```json
{
  "api_key": "",
  "api_base_url": "https://integrate.api.nvidia.com/v1",
  "model": "nvidia/llama-3.1-nemotron-70b-instruct",
  "display_name": "Nvidia",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.9 OpenRouter 配置

```json
{
  "api_key": "",
  "api_base_url": "https://openrouter.ai/api/v1",
  "model": "openai/gpt-4o",
  "display_name": "OpenRouter",
  "enable_streaming": true,
  "http_referer": "",
  "x_title": "Ask AI Plugin",
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.10 Perplexity 配置

```json
{
  "api_key": "",
  "api_base_url": "https://api.perplexity.ai",
  "model": "sonar",
  "display_name": "Perplexity",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

#### 2.2.11 Ollama 配置

```json
{
  "api_key": "",
  "api_base_url": "http://localhost:11434",
  "model": "llama3",
  "display_name": "Ollama",
  "enable_streaming": true,
  "enabled": false,
  "is_configured": false,
  "use_custom_model_name": false
}
```

### 2.3 随机问题配置 (random_questions)

**⚠️ 重要变更**: 在 v1.3.9 中，`random_questions` 从对象改为字符串类型。

#### v1.3.9（开发版本）- 字符串类型

```json
{
  "random_questions": "Generate 5 random questions about this book:\n\nTitle: {title}\nAuthor: {author}\n..."
}
```

`random_questions` 现在是一个提示词模板字符串，而不是语言-问题列表的对象。

#### v1.3.8（旧版本）- 对象类型

```json
{
  "random_questions": {
    "en": [
      "What is the main theme of this book?",
      "Who are the main characters?"
    ],
    "zh": [
      "这本书的主题是什么？",
      "主要人物有哪些？"
    ]
  }
}
```

### 2.4 缓存的模型列表 (cached_models)

```json
{
  "provider_id": [
    "model-name-1",
    "model-name-2",
    "model-name-3"
  ]
}
```

示例：
```json
{
  "openai": [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo"
  ],
  "anthropic": [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022"
  ]
}
```

### 2.5 配置字段说明

| 字段名 | 类型 | 默认值 | 说明 | 版本变更 |
|--------|------|--------|------|---------|
| `selected_model` | string | "grok" | 当前选中的 AI 提供商 ID | - |
| `models` | object | {} | 所有 AI 提供商的配置对象 | - |
| `template` | string | 默认模板 | 单书提示词模板 | - |
| `multi_book_template` | string | 默认模板 | 多书提示词模板 | - |
| `language` | string | "en" | 界面语言代码 | - |
| `language_user_set` | boolean | false | 用户是否手动设置过语言 | - |
| `ask_dialog_width` | integer | 800 | 对话框宽度（像素） | - |
| `ask_dialog_height` | integer | 600 | 对话框高度（像素） | - |
| `random_questions` | **string** | 默认模板 | 随机问题提示词模板 | **v1.3.9 改为字符串** |
| `request_timeout` | integer | 60 | API 请求超时时间（秒） | - |
| `parallel_ai_count` | integer | 1 | 并行 AI 请求数量（1-4） | - |
| `cached_models` | object | {} | 缓存的模型列表 | - |
| `enable_default_export_folder` | boolean | false | 是否启用默认导出文件夹 | - |
| `default_export_folder` | string | "" | 默认导出文件夹路径 | - |
| `copy_mode` | string | "response" | 复制模式：'response' 或 'qa' | - |
| `export_mode` | string | "current" | 导出模式：'current' 或 'history' | - |
| `use_persona` | boolean | true | 是否在提示词中使用角色设定 | - |
| `persona` | string | 默认角色 | 用户角色设定文本 | - |
| `use_interface_language` | boolean | false | 是否要求 AI 使用界面语言回复 | **v1.3.9 新增** |
| `enable_debug_logging` | boolean | false | 是否启用调试日志 | - |

### 2.6 AI 模型配置字段说明

| 字段名 | 类型 | 说明 | 适用提供商 |
|--------|------|------|-----------|
| `auth_token` | string | 认证令牌（Grok 专用） | Grok |
| `api_key` | string | API 密钥 | 除 Grok 外的所有提供商 |
| `api_base_url` | string | API 基础 URL | 所有提供商 |
| `model` | string | 模型名称 | 所有提供商 |
| `display_name` | string | 显示名称 | 所有提供商 |
| `enabled` | boolean | 是否启用该提供商 | 所有提供商 |
| `is_configured` | boolean | 是否已配置（有 API Key 和模型） | 所有提供商 |
| `use_custom_model_name` | boolean | 是否使用自定义模型名称 | 所有提供商 |
| `enable_streaming` | boolean | 是否启用流式传输 | Custom, OpenAI, Anthropic, Nvidia, OpenRouter, Perplexity, Ollama |
| `http_referer` | string | HTTP Referer 头（可选） | OpenRouter |
| `x_title` | string | 应用名称（可选） | OpenRouter |

---

## 三、历史记录文件数据结构 (ask_ai_plugin_history_v2.json)

### 3.1 文件结构

历史记录文件是一个 JSON 对象，键为 UID，值为历史记录对象。

```json
{
  "20241228120000_a1b2c3d4e5f6": {
    "uid": "20241228120000_a1b2c3d4e5f6",
    "timestamp": "2024-12-28 12:00:00",
    "mode": "single",
    "books": [ /* 书籍元数据列表，见 3.2 */ ],
    "question": "用户提出的问题",
    "answers": { /* AI 响应字典，见 3.3 */ }
  }
}
```

### 3.2 书籍元数据结构 (books)

```json
[
  {
    "id": 123,
    "title": "书名",
    "authors": ["作者1", "作者2"],
    "publisher": "出版社",
    "pubdate": "2024-01-01",
    "tags": ["标签1", "标签2"],
    "series": "系列名",
    "series_index": 1.0,
    "rating": 5.0,
    "comments": "书籍简介或评论",
    "languages": ["eng"],
    "identifiers": {
      "isbn": "1234567890"
    }
  }
]
```

### 3.3 AI 响应结构 (answers)

#### 3.3.1 当前版本（v2）- 多 AI 支持

```json
{
  "ai_provider_id": {
    "answer": "AI 的回答内容",
    "timestamp": "2024-12-28 12:00:00",
    "model_info": {
      "provider_name": "OpenAI",
      "model": "gpt-4o",
      "api_base": "https://api.openai.com/v1"
    }
  },
  "default": {
    "answer": "默认 AI 的回答内容",
    "timestamp": "2024-12-28 12:00:00",
    "model_info": {
      "provider_name": "Grok",
      "model": "grok-beta",
      "api_base": "https://api.x.ai/v1"
    }
  }
}
```

#### 3.3.2 旧版本（v1）- 单 AI 支持（已废弃但需兼容）

```json
{
  "answer": "AI 的回答内容"
}
```

**注意**: 旧版本使用 `answer` 字段直接存储字符串，新版本会自动迁移为：
```json
{
  "default": {
    "answer": "AI 的回答内容",
    "timestamp": "历史记录的时间戳"
  }
}
```

### 3.4 历史记录字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `uid` | string | 唯一标识符，格式：`{timestamp}_{book_ids_hash}` |
| `timestamp` | string | 记录创建/更新时间，格式：`YYYY-MM-DD HH:MM:SS` |
| `mode` | string | 模式：'single'（单书）或 'multi'（多书） |
| `books` | array | 书籍元数据列表 |
| `question` | string | 用户提出的问题 |
| `answers` | object | AI 响应字典，键为 AI ID，值为响应对象 |

### 3.5 UID 生成规则

UID 格式：`{timestamp}_{book_ids_hash}`

- `timestamp`: 格式为 `YYYYMMDDHHmmss`（14位数字）
- `book_ids_hash`: 书籍 ID 列表的 MD5 哈希值前 12 位

示例：
- 书籍 ID: [123, 456]
- 时间戳: 2024-12-28 12:00:00
- UID: `20241228120000_a1b2c3d4e5f6`

---

## 四、版本变更详情（v1.3.8 → v1.3.9）

### 4.1 新增字段

| 字段名 | 类型 | 默认值 | 说明 | 代码位置 |
|--------|------|--------|------|---------|
| `use_interface_language` | boolean | false | 是否要求 AI 使用当前界面语言回复 | `prompts_widget.py` |

### 4.2 字段类型变更

| 字段名 | v1.3.8 类型 | v1.3.9 类型 | 说明 |
|--------|------------|------------|------|
| `random_questions` | object (语言-问题列表字典) | string (提示词模板) | 从预定义问题列表改为可自定义的提示词模板 |

#### 4.2.1 random_questions 变更详情

**旧版本 (v1.3.8)**:
```json
{
  "random_questions": {
    "en": ["Question 1", "Question 2"],
    "zh": ["问题1", "问题2"]
  }
}
```

**新版本 (v1.3.9)**:
```json
{
  "random_questions": "Generate 5 random questions about this book:\n\nTitle: {title}\nAuthor: {author}\n..."
}
```

### 4.3 功能变更

#### 4.3.1 语言偏好设置

**新增功能**: 用户可以选择是否要求 AI 始终使用当前插件界面语言进行回复。

- **配置字段**: `use_interface_language`
- **默认值**: `false`（不强制）
- **实现位置**: `prompts_widget.py` 第 76-126 行
- **工作原理**: 
  - 当启用时，会在提示词末尾自动添加语言指令
  - 例如：`"\n\nPlease respond in English."`
  - 语言指令根据当前界面语言动态生成

**代码示例**:
```python
# prompts_widget.py 第 365-378 行
def get_language_instruction_text(self):
    """获取语言指令文本"""
    if not self.use_interface_language_checkbox.isChecked():
        return ""
    
    # 获取当前语言名称
    current_lang = self.parent_dialog.config_widget.config_dialog.lang_combo.currentData()
    from .i18n import get_all_languages
    all_languages = get_all_languages()
    language_name = all_languages.get(current_lang, 'English')
    
    # 返回语言指令
    return f"\n\nPlease respond in {language_name}."
```

#### 4.3.2 随机问题生成方式变更

**旧版本**: 从预定义的问题列表中随机选择
**新版本**: 使用提示词模板让 AI 生成随机问题

这个变更使得随机问题功能更加灵活和可定制。

### 4.4 兼容性影响

#### 4.4.1 向后兼容性

✅ **完全兼容**: 从 v1.3.8 升级到 v1.3.9 不会丢失数据

- `use_interface_language` 字段缺失时，默认为 `false`
- `random_questions` 字段会自动处理：
  - 如果是对象类型（旧版本），会被忽略或转换为默认模板
  - 如果是字符串类型（新版本），直接使用

#### 4.4.2 向前兼容性

⚠️ **部分不兼容**: 从 v1.3.9 降级到 v1.3.8 可能出现问题

- `use_interface_language` 字段会被忽略（不影响功能）
- `random_questions` 如果是字符串，旧版本可能无法正确处理

---

## 五、数据迁移和兼容性

### 5.1 历史记录迁移（v1 → v2）

**旧版本文件**: `ask_ai_plugin_latest_history.json`
**新版本文件**: `ask_ai_plugin_history_v2.json`

#### 5.1.1 旧版本数据结构

```json
{
  "uid": {
    "uid": "uid_string",
    "timestamp": "2024-12-28 12:00:00",
    "mode": "single",
    "books": [...],
    "question": "问题",
    "answer": "单个回答字符串"
  }
}
```

#### 5.1.2 迁移逻辑

代码位置：`history_manager.py` 第 97-109 行

```python
# 确保answers键存在（兼容旧格式）
if 'answers' not in self.histories[uid]:
    # 旧格式转换：如果有answer字段，迁移到answers['default']
    if 'answer' in self.histories[uid]:
        old_answer = self.histories[uid].pop('answer')
        self.histories[uid]['answers'] = {
            'default': {
                'answer': old_answer,
                'timestamp': self.histories[uid]['timestamp']
            }
        }
    else:
        self.histories[uid]['answers'] = {}
```

### 5.2 配置迁移注意事项

#### 5.2.1 新增字段的默认值

新版本添加字段时，需要在代码中添加兼容性检查：

```python
# 示例：处理 use_interface_language 字段
use_interface_lang = prefs.get('use_interface_language', False)
```

#### 5.2.2 random_questions 字段处理

代码位置：`prompts_widget.py` 第 649-656 行

```python
# 保存 Random Questions 提示词
current_random = self.random_questions_edit.toPlainText()
default_random = get_suggestion_template(current_lang)

if current_random.strip() == default_random.strip():
    prefs['random_questions'] = ''
else:
    prefs['random_questions'] = current_random
```

**注意**: 
- 如果 `random_questions` 为空字符串，会使用默认模板
- 旧版本的对象类型数据会被新版本忽略，使用默认模板替代

#### 5.2.3 模型配置的 is_configured 字段

代码位置：`config.py` 第 298-319 行

旧版本没有 `is_configured` 字段，新版本会自动判断并添加：

```python
for model_id, model_config in prefs['models'].items():
    if 'is_configured' not in model_config:
        # 判断是否已配置
        if model_id == 'ollama':
            has_auth = True  # Ollama 不需要 API Key
        else:
            api_key_field = 'auth_token' if model_id == 'grok' else 'api_key'
            has_auth = bool(model_config.get(api_key_field, '').strip())
        
        has_model = bool(model_config.get('model', '').strip())
        model_config['is_configured'] = has_auth and has_model
```

---

## 六、数据备份和恢复

### 6.1 配置备份

配置文件位置：`{calibre_config_dir}/plugins/ask_ai_plugin.json`

备份方法：
1. 直接复制 JSON 文件
2. 使用 Calibre 的配置导出功能

### 6.2 历史记录备份

历史记录文件位置：`{calibre_config_dir}/plugins/ask_ai_plugin_history_v2.json`

备份方法：
1. 直接复制 JSON 文件
2. 插件内置的导出功能（导出为 Markdown 或 JSON）

### 6.3 数据清除

代码位置：`config.py` 第 3145-3159 行

清除所有数据的操作：
1. 删除配置文件：`ask_ai_plugin.json`
2. 删除历史记录文件：`ask_ai_plugin_history_v2.json`
3. 删除旧版历史记录文件：`ask_ai_plugin_latest_history.json`（如果存在）

---

## 七、版本兼容性矩阵

| 数据结构 | v1.3.7 及之前 | v1.3.8 | v1.3.9 (开发版) | 兼容性 |
|---------|--------------|--------|----------------|--------|
| 配置文件 | ask_ai_plugin.json | ask_ai_plugin.json | ask_ai_plugin.json | ✅ 完全兼容 |
| 历史记录 | ask_ai_plugin_latest_history.json | ask_ai_plugin_history_v2.json | ask_ai_plugin_history_v2.json | ✅ 自动迁移 |
| `answers` 字段 | 单个字符串 `answer` | 字典 `answers` | 字典 `answers` | ✅ 自动迁移 |
| `is_configured` 字段 | 不存在 | 存在 | 存在 | ✅ 自动添加 |
| `use_custom_model_name` | 不存在 | 存在 | 存在 | ✅ 默认 false |
| `model_info` 字段 | 不存在 | 存在于 answers 中 | 存在于 answers 中 | ✅ 可选字段 |
| `random_questions` | 对象 | 对象 | **字符串** | ⚠️ 类型变更 |
| `use_interface_language` | 不存在 | 不存在 | **存在** | ✅ 新增字段 |

---

## 八、开发者注意事项

### 8.1 添加新配置字段

1. 在 `config.py` 的 `prefs.defaults` 中添加默认值
2. 在代码中使用 `prefs.get('field_name', default_value)` 确保兼容性
3. 更新本文档

### 8.2 修改数据结构

1. 保持向后兼容，不要删除旧字段
2. 添加迁移逻辑处理旧数据
3. 更新版本号
4. 更新本文档
5. 在版本变更章节中详细记录变更

### 8.3 测试兼容性

1. 使用旧版本创建测试数据
2. 升级到新版本
3. 验证数据是否正确迁移
4. 验证功能是否正常
5. 测试降级场景（如果需要支持）

### 8.4 v1.3.9 特别注意事项

#### 8.4.1 random_questions 字段处理

在读取 `random_questions` 时，需要处理两种类型：

```python
# 获取 random_questions
random_questions = prefs.get('random_questions', '')

# 检查类型
if isinstance(random_questions, dict):
    # 旧版本：对象类型，使用默认模板
    random_questions = get_suggestion_template(current_lang)
elif isinstance(random_questions, str):
    # 新版本：字符串类型
    if not random_questions.strip():
        # 空字符串，使用默认模板
        random_questions = get_suggestion_template(current_lang)
```

#### 8.4.2 use_interface_language 功能集成

在构建提示词时，需要检查并添加语言指令：

```python
# prompts_widget.py 第 854-862 行
use_interface_language = prefs.get('use_interface_language', False)
if use_interface_language:
    lang_code = prefs.get('language', 'en')
    all_languages = get_all_languages()
    language_name = all_languages.get(lang_code, 'English')
    language_instruction = f"\n\nPlease respond in {language_name}."
    result = result + language_instruction
```

---

## 九、常见问题

### 9.1 历史记录丢失

**原因**: 
- 历史记录文件被删除
- 文件损坏
- 权限问题

**解决方案**:
1. 检查备份文件（`.bak` 后缀）
2. 检查文件权限
3. 查看日志文件了解错误详情

### 9.2 配置重置

**原因**:
- 配置文件被删除
- 配置文件损坏
- 手动执行了"Reset All Data"

**解决方案**:
1. 从备份恢复配置文件
2. 重新配置 AI 提供商

### 9.3 模型列表为空

**原因**:
- 缓存未加载
- API Key 无效
- 网络问题

**解决方案**:
1. 点击"Refresh Model List"按钮
2. 检查 API Key 是否正确
3. 检查网络连接

### 9.4 升级后随机问题功能异常

**原因**: v1.3.9 改变了 `random_questions` 的数据类型

**解决方案**:
1. 在 Prompts 配置页面重新设置随机问题模板
2. 或者使用默认模板（留空即可）

### 9.5 语言指令不生效

**原因**: `use_interface_language` 未启用或配置错误

**解决方案**:
1. 在 Prompts 配置页面启用"Use Interface Language"选项
2. 确认当前界面语言设置正确
3. 检查提示词预览中是否包含语言指令

---

## 十、附录

### 10.1 支持的语言代码

| 代码 | 语言 |
|------|------|
| en | English |
| zh | 简体中文 |
| zht | 繁體中文 |
| ja | 日本語 |
| es | Español |
| fr | Français |
| de | Deutsch |
| ru | Русский |
| pt | Português |
| nl | Nederlands |
| sv | Svenska |
| no | Norsk |
| da | Dansk |
| fi | Suomi |
| yue | 粵語 |

### 10.2 支持的 AI 提供商

| ID | 名称 | 默认 API Base URL |
|----|------|-------------------|
| grok | Grok | https://api.x.ai/v1 |
| gemini | Gemini | https://generativelanguage.googleapis.com/v1beta |
| deepseek | DeepSeek | https://api.deepseek.com |
| custom | Custom | https://api.example.com/v1 |
| openai | OpenAI | https://api.openai.com/v1 |
| anthropic | Anthropic | https://api.anthropic.com |
| nvidia | Nvidia | https://integrate.api.nvidia.com/v1 |
| openrouter | OpenRouter | https://openrouter.ai/api/v1 |
| perplexity | Perplexity | https://api.perplexity.ai |
| ollama | Ollama | http://localhost:11434 |

### 10.3 文件路径示例

**Windows**:
- 配置: `C:\Users\{username}\AppData\Roaming\calibre\plugins\ask_ai_plugin.json`
- 历史: `C:\Users\{username}\AppData\Roaming\calibre\plugins\ask_ai_plugin_history_v2.json`

**macOS**:
- 配置: `~/Library/Preferences/calibre/plugins/ask_ai_plugin.json`
- 历史: `~/Library/Preferences/calibre/plugins/ask_ai_plugin_history_v2.json`

**Linux**:
- 配置: `~/.config/calibre/plugins/ask_ai_plugin.json`
- 历史: `~/.config/calibre/plugins/ask_ai_plugin_history_v2.json`

### 10.4 提示词模板动态字段

在提示词模板中可以使用以下动态字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `{title}` | 书籍标题 | "The Great Gatsby" |
| `{author}` | 作者 | "F. Scott Fitzgerald" |
| `{publisher}` | 出版社 | "Scribner" |
| `{pubdate}` | 出版日期 | "1925-04-10" |
| `{tags}` | 标签列表 | "Classic, Fiction" |
| `{series}` | 系列名 | "Modern Library" |
| `{rating}` | 评分 | "5.0" |
| `{comments}` | 简介/评论 | "A novel about..." |
| `{query}` | 用户问题 | "What is the theme?" |

---

## 十一、更新日志

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.3.9 | 2024-12-28 | 开发版本文档创建，记录新增 `use_interface_language` 字段和 `random_questions` 类型变更 |
| v1.3.8 | 2024-12-28 | 稳定版本基准 |

---

## 十二、迁移指南（v1.3.8 → v1.3.9）

### 12.1 用户迁移步骤

1. **备份数据**（强烈推荐）
   - 备份 `ask_ai_plugin.json`
   - 备份 `ask_ai_plugin_history_v2.json`

2. **升级插件**
   - 安装 v1.3.9 版本
   - 重启 Calibre

3. **验证配置**
   - 打开插件配置
   - 检查所有 AI 配置是否正常
   - 检查历史记录是否完整

4. **配置新功能**（可选）
   - 在 Prompts 页面配置"Use Interface Language"选项
   - 自定义随机问题提示词模板

### 12.2 开发者迁移步骤

1. **更新代码**
   - 处理 `use_interface_language` 字段
   - 处理 `random_questions` 类型变更

2. **测试兼容性**
   - 测试从 v1.3.8 升级场景
   - 测试全新安装场景
   - 测试数据迁移逻辑

3. **更新文档**
   - 更新用户手册
   - 更新 CHANGELOG
   - 更新本数据结构文档

---

**文档结束**
