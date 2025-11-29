# Google Gemini 配置指南

## 核心配置

- **API Key**: 必需。作为 URL 查询参数发送。
- **Base URL**: 必需。这是 API 的根地址，例如 `https://generativelanguage.googleapis.com/v1beta`。

## 获取模型列表

### REST API 方式
- **完整 URL**: `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`
- **端点**: `/v1beta/models`
- **方法**: `GET`
- **认证**: API Key 作为 URL 查询参数 `key` 传递
- **响应格式**:
  ```json
  {
    "models": [
      {
        "name": "models/gemini-2.5-flash",
        "displayName": "Gemini 2.5 Flash",
        "supportedActions": ["generateContent", "embedContent"]
      }
    ]
  }
  ```
- **注意事项**:
  1. 响应中的模型名称包含 `models/` 前缀，需要移除后使用
  2. 可以通过 `supportedActions` 字段过滤支持特定功能的模型
  3. 只返回支持 `generateContent` 的模型用于对话

### Python SDK 方式（参考）
```python
from google import genai

client = genai.Client()

# 列出支持 generateContent 的模型
print("List of models that support generateContent:\n")
for m in client.models.list():
    for action in m.supported_actions:
        if action == "generateContent":
            print(m.name)

# 列出支持 embedContent 的模型
print("List of models that support embedContent:\n")
for m in client.models.list():
    for action in m.supported_actions:
        if action == "embedContent":
            print(m.name)
```

## 发送聊天请求

- **端点**: `${baseUrl}/${model_name}:generateContent?key=${apiKey}`
- **方法**: `POST`
- **认证**: API Key 同样附加在 URL 的查询参数中。
- **请求体 (Body)**:
  ```json
  {
    "contents": [
      {
        "parts": [
          {
            "text": "<用户提示词>"
          }
        ]
      }
    ]
  }
  ```

## 实现要点

### 获取模型列表的特殊处理
1. **认证方式**: API Key 必须作为 URL 查询参数 `key` 传递，不能放在请求头中
2. **请求头**: GET 请求不应包含 `Content-Type` 头，否则可能导致 400 错误
3. **响应处理**: 模型名称包含 `models/` 前缀（如 `models/gemini-2.5-flash`），使用时需要移除前缀
4. **模型过滤**: 建议只返回 `supportedActions` 包含 `generateContent` 的模型

### 常见问题

#### 400 Bad Request 错误
**原因**: 
- GET 请求包含了不必要的 `Content-Type: application/json` 头
- API Key 格式错误或包含特殊字符未正确编码

**解决方案**:
- 移除 GET 请求的 Content-Type 头
- 确保 API Key 正确 URL 编码

#### 400 Bad Request - 地理位置限制
**错误信息**: `User location is not supported for the API use.`

**原因**: Gemini API 在某些地区不可用（如中国大陆）

**解决方案**:
1. **使用 VPN**: 连接到支持的地区（如美国、欧洲等）
2. **切换提供商**: 使用其他 AI 提供商
   - OpenAI (GPT-4)
   - Anthropic (Claude)
   - DeepSeek
   - Nvidia AI
   - Ollama (本地运行)
3. **查看可用性**: 访问 [Google AI Studio](https://aistudio.google.com/) 查看您所在地区的可用性

#### 401 Unauthorized 错误
**原因**: API Key 无效或已过期

**解决方案**:
- 在 Google AI Studio 重新生成 API Key
- 确认 API Key 已启用 Gemini API 访问权限

## 总结

Gemini 的 API 设计比较独特：
1. **认证方式**: API Key 通过 URL 参数传递，而非请求头
2. **端点格式**: 聊天请求需要动态拼接模型名称，格式为 `${model_name}:generateContent`
3. **模型名称**: 响应中的模型名称包含 `models/` 前缀，需要移除
4. **请求头**: GET 请求（如获取模型列表）不需要 Content-Type 头
