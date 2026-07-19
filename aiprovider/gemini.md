# Google Gemini 配置指南

## 核心配置

- **API Key**: 必需。通过请求头 `x-goog-api-key` 发送（推荐；旧的 `?key=` 查询参数仍可用但不推荐）。
- **Base URL**: 必需。例如 `https://generativelanguage.googleapis.com/v1beta`。
- **Model**: 使用 Google AI 原生名称，例如 `gemini-3.5-flash`（不要使用 OpenRouter 风格的 `google/gemini-...`）。

## 获取模型列表

### REST API 方式
- **URL**: `https://generativelanguage.googleapis.com/v1beta/models`
- **方法**: `GET`
- **认证**:
  ```http
  x-goog-api-key: ${apiKey}
  ```
- **请求头**: GET 请求不要带 `Content-Type`
- **响应格式**:
  ```json
  {
    "models": [
      {
        "name": "models/gemini-3.5-flash",
        "displayName": "Gemini 3.5 Flash",
        "supportedGenerationMethods": ["generateContent", "countTokens"]
      }
    ]
  }
  ```
- **注意事项**:
  1. 响应中的模型名称包含 `models/` 前缀，使用前需要移除
  2. 建议只保留 `supportedGenerationMethods` 包含 `generateContent` 的模型

## 发送聊天请求

- **端点**: `${baseUrl}/models/${model_name}:generateContent`
- **流式端点**: `${baseUrl}/models/${model_name}:streamGenerateContent?alt=sse`
- **方法**: `POST`
- **认证**:
  ```http
  x-goog-api-key: ${apiKey}
  Content-Type: application/json
  ```
- **请求体 (Body)**:
  ```json
  {
    "systemInstruction": {
      "parts": [
        {
          "text": "<系统提示词>"
        }
      ]
    },
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "<用户提示词>"
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7
    }
  }
  ```

## 实现要点

1. **认证**: 优先使用 `x-goog-api-key` 请求头，不要把 Key 放进 URL
2. **系统提示**: 使用顶层字段 `systemInstruction`，不要再伪装成 `role: user` 的 contents
3. **模型名**: URL 中使用 `gemini-3.5-flash`，不要带 `models/`；也不要带 `google/`
4. **流式**: `streamGenerateContent` + `alt=sse`，按 `data: {...}` 解析 `candidates[0].content.parts[].text`

## 常见问题

### 404 Not Found
**原因**: 模型名错误（例如误用 `google/gemini-3.5-flash`）

**解决方案**:
- 改成 `gemini-3.5-flash`
- 或在设置里刷新模型列表后重新选择

### 400 Bad Request - 地理位置限制
**错误信息**: `User location is not supported for the API use.`

**解决方案**:
1. 使用 VPN 连接到支持地区
2. 切换到其他 AI 提供商
3. 在 [Google AI Studio](https://aistudio.google.com/) 查看地区可用性

### 401 / 403 Unauthorized
**原因**: API Key 无效或权限不足

**解决方案**:
- 在 Google AI Studio 重新生成 API Key
- 确认 Key 已启用 Gemini API 访问

## 总结

最新 Gemini REST 请求格式的关键点：
1. Header 认证：`x-goog-api-key`
2. 系统提示：`systemInstruction`
3. 对话内容：`contents[].role` + `parts[].text`
4. 模型名：原生 ID（如 `gemini-3.5-flash`）
