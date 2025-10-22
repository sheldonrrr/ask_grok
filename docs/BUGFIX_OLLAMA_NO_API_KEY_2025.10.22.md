# Ollama 无需 API Key 修复
**修复日期**: 2025-10-22  
**问题**: Ollama 是本地服务，不需要 API Key，但配置界面仍然显示 API Key 输入框

---

## 问题描述

Ollama 是本地运行的大语言模型服务，通常运行在 `http://localhost:11434`，不需要 API Key 认证。但配置界面中仍然显示 API Key 输入框，这会让用户困惑。

---

## 修复内容

### 1. 修复 get_api_key() 方法

**位置**: `config.py` 第 570-574 行

**修改前**:
```python
def get_api_key(self) -> str:
    """获取 API Key"""
    if hasattr(self, 'api_key_edit'):
        return self.api_key_edit.toPlainText().strip()
    return ''
```

**修改后**:
```python
def get_api_key(self) -> str:
    """获取 API Key"""
    if hasattr(self, 'api_key_edit') and self.api_key_edit:
        return self.api_key_edit.toPlainText().strip()
    return ''
```

**说明**: 添加了 `and self.api_key_edit` 检查，避免在 Ollama 模型中调用 `toPlainText()` 时出现 `AttributeError`。

### 2. 隐藏 API Key 输入框

**位置**: `config.py` 第 243-254 行

**修改前**:
```python
if model_config:
    # API Key/Token 输入框
    self.api_key_edit = QTextEdit(self)
    self.api_key_edit.setPlainText(self.config.get(api_key_field_name, ''))
    self.api_key_edit.textChanged.connect(self.on_config_changed)
    self.api_key_edit.setMaximumHeight(62)
    self.api_key_edit.setMinimumWidth(base_width)
    layout.addRow(self.i18n.get('api_key_label', 'API Key:'), self.api_key_edit)
```

**修改后**:
```python
if model_config:
    # API Key/Token 输入框（Ollama 不需要）
    if self.model_id != 'ollama':
        self.api_key_edit = QTextEdit(self)
        self.api_key_edit.setPlainText(self.config.get(api_key_field_name, ''))
        self.api_key_edit.textChanged.connect(self.on_config_changed)
        self.api_key_edit.setMaximumHeight(62)
        self.api_key_edit.setMinimumWidth(base_width)
        layout.addRow(self.i18n.get('api_key_label', 'API Key:'), self.api_key_edit)
    else:
        # Ollama 不需要 API Key，创建一个空的占位符以保持代码兼容性
        self.api_key_edit = None
```

### 3. 跳过 API Key 验证

**位置**: `config.py` 第 448-457 行（`on_load_models_clicked` 方法）

**修改前**:
```python
# 1. 验证 API Key
api_key = self.get_api_key()
if not api_key:
    QMessageBox.warning(
        self,
        self.i18n.get('warning', 'Warning'),
        self.i18n.get('api_key_required', 'Please enter API Key first')
    )
    return
```

**修改后**:
```python
# 1. 验证 API Key（Ollama 不需要）
if self.model_id != 'ollama':
    api_key = self.get_api_key()
    if not api_key:
        QMessageBox.warning(
            self,
            self.i18n.get('warning', 'Warning'),
            self.i18n.get('api_key_required', 'Please enter API Key first')
        )
        return
```

**说明**: 在 Load Models 功能中，跳过 Ollama 的 API Key 验证，因为本地服务不需要认证。

### 4. 跳过 API 层的 API Key 验证

**位置**: `api.py` 第 495-502 行（`fetch_available_models` 方法）

**修改前**:
```python
# 2. 验证 API Key
api_key_field = 'auth_token' if model_name == 'grok' else 'api_key'
api_key = config.get(api_key_field, '').strip()
if not api_key:
    error_msg = self.i18n.get('api_key_required', 'API Key is required')
    logger.warning(f"fetch_available_models: {error_msg}")
    return False, error_msg
```

**修改后**:
```python
# 2. 验证 API Key（Ollama 不需要）
if model_name != 'ollama':
    api_key_field = 'auth_token' if model_name == 'grok' else 'api_key'
    api_key = config.get(api_key_field, '').strip()
    if not api_key:
        error_msg = self.i18n.get('api_key_required', 'API Key is required')
        logger.warning(f"fetch_available_models: {error_msg}")
        return False, error_msg
```

**说明**: 在 API 层的 `fetch_available_models` 方法中，也需要跳过 Ollama 的 API Key 验证。

### 5. 修复保存配置逻辑

**位置**: `config.py` 第 399-403 行

**修改前**:
```python
elif self.model_id == 'ollama':
    provider = AIProvider.AI_OLLAMA
    config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
    config['display_name'] = 'Ollama (Local)'
```

**修改后**:
```python
elif self.model_id == 'ollama':
    provider = AIProvider.AI_OLLAMA
    # Ollama 不需要 API Key
    config['api_key'] = self.api_key_edit.toPlainText().strip() if (hasattr(self, 'api_key_edit') and self.api_key_edit) else ''
    config['display_name'] = 'Ollama (Local)'
```

**说明**: 添加了 `and self.api_key_edit` 检查，因为现在 `api_key_edit` 可能为 `None`。

---

## 修复逻辑

### 条件判断
```python
if self.model_id != 'ollama':
    # 显示 API Key 输入框
else:
    # 不显示，设置为 None
```

### 保存时的处理
```python
# 检查 api_key_edit 是否存在且不为 None
if (hasattr(self, 'api_key_edit') and self.api_key_edit):
    config['api_key'] = self.api_key_edit.toPlainText().strip()
else:
    config['api_key'] = ''  # 空字符串
```

---

## 用户体验改进

### 修改前
- ❌ Ollama 配置界面显示 API Key 输入框
- ❌ 用户不知道是否需要填写
- ❌ 界面混乱，不够清晰

### 修改后
- ✅ Ollama 配置界面不显示 API Key 输入框
- ✅ 界面更简洁
- ✅ 用户体验更好

---

## Ollama 配置界面布局

选择 Ollama 后，配置界面应该显示：

```
┌─────────────────────────────────────┐
│ Ollama (Local)                      │
├─────────────────────────────────────┤
│ [不显示 API Key 输入框]              │
├─────────────────────────────────────┤
│ API Base URL:                       │
│ ┌─────────────────────────────────┐ │
│ │ http://localhost:11434          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Model:                              │
│ ┌─────────────────────────────────┐ │
│ │ llama3                          │ │
│ └─────────────────────────────────┘ │
│ [ ] Use custom model name           │
│                                     │
│ [Load Models]                       │
│                                     │
│ [ ] Enable Streaming                │
└─────────────────────────────────────┘
```

---

## 其他模型的 API Key 要求

| 模型 | API Key 要求 | 说明 |
|------|-------------|------|
| Grok | ✅ 必需 | x.AI API Token |
| Gemini | ✅ 必需 | Google API Key |
| Deepseek | ✅ 必需 | Deepseek API Key |
| OpenAI | ✅ 必需 | OpenAI API Key |
| Anthropic | ✅ 必需 | Anthropic API Key |
| Nvidia | ✅ 必需 | Nvidia API Key |
| OpenRouter | ✅ 必需 | OpenRouter API Key |
| **Ollama** | ❌ **不需要** | **本地服务** |
| Custom | ⚠️ 可选 | 取决于服务 |

---

## 代码兼容性

### 为什么设置为 None 而不是删除属性？

```python
self.api_key_edit = None
```

**原因**:
1. 保持代码兼容性
2. 其他地方可能会检查 `hasattr(self, 'api_key_edit')`
3. 避免 `AttributeError`

### 安全的访问方式

```python
# ✅ 安全的方式
if hasattr(self, 'api_key_edit') and self.api_key_edit:
    value = self.api_key_edit.toPlainText()

# ❌ 不安全的方式（会出错）
if hasattr(self, 'api_key_edit'):
    value = self.api_key_edit.toPlainText()  # 如果为 None 会报错
```

---

## 验证步骤

1. **打开配置界面**
   - 在 Calibre 中打开 Ask Grok 插件配置
   - 切换到 "AI" 标签页

2. **选择 Ollama**
   - 从下拉菜单选择 "Ollama (Local)"
   - 应该**不显示** API Key 输入框
   - 只显示 API Base URL 和 Model 配置

3. **选择其他模型**
   - 切换到其他模型（如 OpenRouter）
   - 应该**显示** API Key 输入框

4. **保存配置**
   - 配置 Ollama 的 Base URL（如 `http://localhost:11434`）
   - 点击 "Save" 保存
   - 不应该出现任何错误

5. **测试功能**
   - 使用 Ollama 发送问题
   - 应该正常工作（假设本地 Ollama 服务正在运行）

---

## 相关文档

- `docs/DEV_PLAN_OPENROUTER_OLLAMA_2025.10.22.md` - 开发计划
- `docs/IMPLEMENTATION_COMPLETE_OPENROUTER_OLLAMA_2025.10.22.md` - 实施完成报告
- `docs/BUGFIX_CONFIG_UI_OPENROUTER_OLLAMA_2025.10.22.md` - 配置界面修复
- `models/ollama.py` - Ollama 模型实现

---

## 修改文件

- `config.py` - 4 处修改
  - `get_api_key()` 方法 - 安全访问 api_key_edit（修复 Load Models 错误）
  - `load_config()` 方法 - 条件显示 API Key 输入框
  - `on_load_models_clicked()` 方法 - 跳过 Ollama 的 API Key 验证
  - `save_config()` 方法 - 安全访问 api_key_edit

- `api.py` - 1 处修改
  - `fetch_available_models()` 方法 - 跳过 Ollama 的 API Key 验证

---

**修复状态**: ✅ 已完成  
**测试状态**: ⏳ 待测试  
**文档版本**: 1.0  
**最后更新**: 2025-10-22
