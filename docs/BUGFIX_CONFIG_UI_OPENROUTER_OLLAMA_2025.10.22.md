# 配置界面 OpenRouter 和 Ollama 支持修复
**修复日期**: 2025-10-22  
**问题**: 配置界面中没有显示 OpenRouter 和 Ollama 的切换选项

---

## 问题描述

虽然已经实现了 OpenRouter 和 Ollama 两个新的 AI 模型，但在配置界面的下拉菜单中无法选择这两个选项。

---

## 根本原因

配置界面 (`config.py`) 中有多个地方使用了硬编码的模型映射字典 `model_mapping`，这些字典没有包含新添加的 OpenRouter 和 Ollama。

---

## 修复内容

### 1. 更新模型下拉菜单映射（2处）

#### 位置 1: `create_model_selection()` 方法（约第 781 行）
```python
model_mapping = {
    AIProvider.AI_GROK: 'grok',
    AIProvider.AI_GEMINI: 'gemini',
    AIProvider.AI_DEEPSEEK: 'deepseek',
    AIProvider.AI_CUSTOM: 'custom',
    AIProvider.AI_OPENAI: 'openai',
    AIProvider.AI_ANTHROPIC: 'anthropic',
    AIProvider.AI_NVIDIA: 'nvidia',
    AIProvider.AI_OPENROUTER: 'openrouter',  # ✅ 新增
    AIProvider.AI_OLLAMA: 'ollama'           # ✅ 新增
}
```

#### 位置 2: `update_model_combo()` 方法（约第 1041 行）
```python
model_mapping = {
    AIProvider.AI_GROK: 'grok',
    AIProvider.AI_GEMINI: 'gemini',
    AIProvider.AI_DEEPSEEK: 'deepseek',
    AIProvider.AI_CUSTOM: 'custom',
    AIProvider.AI_OPENAI: 'openai',
    AIProvider.AI_ANTHROPIC: 'anthropic',
    AIProvider.AI_NVIDIA: 'nvidia',
    AIProvider.AI_OPENROUTER: 'openrouter',  # ✅ 新增
    AIProvider.AI_OLLAMA: 'ollama'           # ✅ 新增
}
```

### 2. 更新 `load_config()` 方法中的 provider 映射（约第 236 行）

```python
elif self.model_id == 'openrouter':
    provider = AIProvider.AI_OPENROUTER
    model_config = get_current_model_config(provider)
elif self.model_id == 'ollama':
    provider = AIProvider.AI_OLLAMA
    model_config = get_current_model_config(provider)
```

### 3. 更新 `save_config()` 方法中的配置保存逻辑（约第 386 行）

```python
elif self.model_id == 'openrouter':
    provider = AIProvider.AI_OPENROUTER
    config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
    config['display_name'] = 'OpenRouter'
    # OpenRouter 特殊字段
    if hasattr(self, 'http_referer_edit'):
        config['http_referer'] = self.http_referer_edit.text().strip()
    if hasattr(self, 'x_title_edit'):
        config['x_title'] = self.x_title_edit.text().strip()
elif self.model_id == 'ollama':
    provider = AIProvider.AI_OLLAMA
    config['api_key'] = self.api_key_edit.toPlainText().strip() if hasattr(self, 'api_key_edit') else ''
    config['display_name'] = 'Ollama (Local)'
```

### 4. 更新 `update_api_base_placeholder()` 方法中的模型导入（约第 664 行）

```python
elif self.model_id == 'openrouter':
    from .models import OpenRouterModel
    model_config = OpenRouterModel
elif self.model_id == 'ollama':
    from .models import OllamaModel
    model_config = OllamaModel
```

### 5. 更新 `reset_model_params()` 方法中的 provider 映射（约第 697 行）

```python
elif self.model_id == 'openrouter':
    provider = AIProvider.AI_OPENROUTER
elif self.model_id == 'ollama':
    provider = AIProvider.AI_OLLAMA
```

### 6. 更新 `__init__()` 方法中的模型工厂注册（约第 751 行）

```python
AIModelFactory.register_model('openrouter', OpenRouterModel)
AIModelFactory.register_model('ollama', OllamaModel)
```

---

## 修改文件

- `config.py` - 6 处修改

---

## 修改总结

| 方法/位置 | 修改内容 | 说明 |
|----------|---------|------|
| `create_model_selection()` | 添加到 `model_mapping` | 下拉菜单显示 |
| `update_model_combo()` | 添加到 `model_mapping` | 语言切换时更新 |
| `load_config()` | 添加 provider 映射 | 加载配置时识别 |
| `save_config()` | 添加保存逻辑 | 保存配置时处理 |
| `update_api_base_placeholder()` | 添加模型导入 | API Base URL 占位符 |
| `reset_model_params()` | 添加 provider 映射 | 重置参数功能 |
| `__init__()` | 注册到工厂 | 模型工厂注册 |

---

## 验证步骤

1. **打开配置界面**
   - 在 Calibre 中打开 Ask Grok 插件配置
   - 切换到 "AI" 标签页

2. **检查下拉菜单**
   - 应该能看到 "OpenRouter" 选项
   - 应该能看到 "Ollama (Local)" 选项

3. **选择 OpenRouter**
   - 应该显示 API Key 输入框
   - 应该显示 API Base URL 输入框（默认：`https://openrouter.ai/api/v1`）
   - 应该显示模型选择/输入框
   - 应该显示 "Load Models" 按钮
   - 应该显示流式传输开关

4. **选择 Ollama**
   - 应该显示 API Key 输入框（标签：API Key (Optional)）
   - 应该显示 API Base URL 输入框（默认：`http://localhost:11434`）
   - 应该显示模型选择/输入框
   - 应该显示 "Load Models" 按钮
   - 应该显示流式传输开关

5. **测试配置保存**
   - 配置 OpenRouter 或 Ollama
   - 保存配置
   - 重新打开配置界面
   - 验证配置已保存

---

## 特殊注意事项

### OpenRouter 特殊字段
OpenRouter 支持两个可选的请求头字段：
- `http_referer`: 用于在 OpenRouter 上进行排名
- `x_title`: 应用名称标识

这些字段在配置中已经定义，但 UI 中可能需要额外添加输入框（可选功能）。

### Ollama 特殊说明
- API Key 是可选的（本地服务通常不需要）
- 默认 Base URL 是 `http://localhost:11434`
- 模型列表通过 `/api/tags` 端点获取（不是标准的 `/v1/models`）

---

## 相关文档

- `docs/DEV_PLAN_OPENROUTER_OLLAMA_2025.10.22.md` - 开发计划
- `docs/IMPLEMENTATION_COMPLETE_OPENROUTER_OLLAMA_2025.10.22.md` - 实施完成报告
- `models/openrouter.py` - OpenRouter 模型实现
- `models/ollama.py` - Ollama 模型实现

---

**修复状态**: ✅ 已完成  
**测试状态**: ⏳ 待测试  
**文档版本**: 1.0  
**最后更新**: 2025-10-22
