# Stream 参数处理 Bug 修复

## 修复日期
2025-10-22

## 问题描述

### 错误现象
OpenAI 模型发送请求时出现错误：
```
API request failed: Expecting value: line 1 column 1 (char 0)
```

HTTP 响应状态码为 200，但无法解析响应体。

### 根本原因

**问题 1：response_handler.py 未指定 stream 参数**

在 `response_handler.py` 第 252 行，普通请求调用时：
```python
response = self.api.ask(prompt)  # ❌ 未指定 stream 参数
```

**问题 2：prepare_request_data() 使用配置默认值**

所有 OpenAI 兼容模型（OpenAI、Grok、Nvidia、Custom、Deepseek）的 `prepare_request_data()` 方法中：
```python
# 错误的实现
if kwargs.get('stream', self.config.get('enable_streaming', True)):
    data['stream'] = True
```

### 问题链路

```
用户配置: enable_streaming = True
    ↓
response_handler 判断: 不支持流式 → 使用普通请求
    ↓
调用: api.ask(prompt)  # 未传 stream 参数
    ↓
prepare_request_data(): kwargs.get('stream', 配置默认值)
    ↓
读取配置: enable_streaming = True
    ↓
请求数据: {"stream": true, ...}  # ❌ 错误！
    ↓
API 返回: 流式响应（SSE 格式）
    ↓
代码尝试: response.json()  # ❌ 无法解析流式数据
    ↓
错误: Expecting value: line 1 column 1 (char 0)
```

## 修复方案

### 修复 1：response_handler.py

**文件：** `response_handler.py` 第 252 行

**修改前：**
```python
response = self.api.ask(prompt)
```

**修改后：**
```python
response = self.api.ask(prompt, stream=False)  # 明确指定不使用流式
```

### 修复 2：所有 OpenAI 兼容模型

**受影响的文件：**
- `models/openai.py`
- `models/grok.py`
- `models/nvidia.py`
- `models/custom.py`
- `models/deepseek.py`
- `models/anthropic.py`
- `models/gemini.py`

**修改前：**
```python
# 添加流式传输支持
if kwargs.get('stream', self.config.get('enable_streaming', True)):
    data['stream'] = True
```

**修改后：**
```python
# 添加流式传输支持（只有明确指定 stream=True 才添加）
if kwargs.get('stream', False):
    data['stream'] = True
```

### 关键变化

| 场景 | 修改前 | 修改后 |
|------|--------|--------|
| `ask(prompt)` | 使用配置默认值 | `stream=False` |
| `ask(prompt, stream=True)` | `stream=True` | `stream=True` |
| `ask(prompt, stream=False)` | `stream=False` | `stream=False` |

## 修复后的正确流程

### 流式请求流程
```
response_handler 判断: 支持流式 + 启用流式
    ↓
调用: api.ask(prompt, stream=True, stream_callback=callback)
    ↓
prepare_request_data(): kwargs.get('stream', False) = True
    ↓
请求数据: {"stream": true, ...}  # ✅ 正确
    ↓
API 返回: 流式响应（SSE 格式）
    ↓
代码处理: response.iter_lines()  # ✅ 正确处理流式数据
```

### 普通请求流程
```
response_handler 判断: 不支持流式 或 未启用流式
    ↓
调用: api.ask(prompt, stream=False)
    ↓
prepare_request_data(): kwargs.get('stream', False) = False
    ↓
请求数据: {...}  # ✅ 不包含 stream 字段
    ↓
API 返回: 完整 JSON 响应
    ↓
代码处理: response.json()  # ✅ 正确解析 JSON
```

## 影响范围

### 受影响的模型
- ✅ OpenAI
- ✅ Grok
- ✅ Nvidia
- ✅ Custom
- ✅ Deepseek
- ✅ Anthropic
- ✅ Gemini

**所有 7 个 AI 模型都受影响！**

## 测试验证

### 测试用例 1：普通请求（OpenAI）
```
配置: enable_streaming = True
调用: response_handler → 普通请求
预期: stream=False 传递给 API
结果: ✅ 请求成功，返回完整 JSON
```

### 测试用例 2：流式请求（OpenAI）
```
配置: enable_streaming = True
调用: response_handler → 流式请求
预期: stream=True 传递给 API
结果: ✅ 流式数据正确处理
```

### 测试用例 3：其他模型
```
模型: Grok, Nvidia, Custom, Deepseek
场景: 普通请求 + 流式请求
结果: ✅ 所有场景正常工作
```

## 经验教训

### 1. 显式优于隐式
**问题：** 依赖配置默认值导致行为不可预测
**教训：** 关键参数应该显式传递，不要依赖默认值

### 2. 参数传递要明确
**问题：** `kwargs.get('stream', 配置默认值)` 混淆了调用意图
**教训：** 使用 `kwargs.get('stream', False)` 明确"未指定=False"的语义

### 3. 日志的重要性
**问题：** 初期难以定位问题
**教训：** 添加详细日志帮助快速定位了问题根源

## 代码审查清单

在类似场景中，检查以下几点：

- [ ] API 参数是否显式传递？
- [ ] 默认值是否合理？
- [ ] 配置值和运行时参数的优先级是否清晰？
- [ ] 是否有充分的日志记录参数传递？
- [ ] 错误处理是否能提供有用的诊断信息？

## 相关文档

- `docs/REFACTOR_CUSTOM_MODEL_INPUT_2025.10.22.md` - 自定义模型输入框改造
- `docs/CUSTOM_MODEL_NAME_DATA_FLOW_2025.10.22.md` - 数据流分析
- `docs/REFACTOR_FETCH_MODELS_2025.10.22.md` - 模型列表重构

## 总结

这次 bug 修复涉及：
- ✅ 1 个 response_handler 文件
- ✅ 7 个模型文件（OpenAI、Grok、Nvidia、Custom、Deepseek、Anthropic、Gemini）
- ✅ 核心问题：参数默认值处理不当
- ✅ 修复方式：显式传递参数，避免依赖配置默认值

**注意：** Gemini 的实现略有不同，它根据 `use_stream` 参数选择不同的 API 端点（`generateContent` vs `streamGenerateContent`），而不是在请求数据中添加 `stream` 字段。但问题的根源相同：都是依赖配置默认值导致的。

**关键原则：在 API 调用中，显式传递关键参数，不要依赖隐式默认值。**
