# Google Gemini 配置指南

## 核心配置

- **API Key**: 必需。请求头 `x-goog-api-key`（不再使用 URL `?key=`）
- **Base URL**: 必需。例如 `https://generativelanguage.googleapis.com/v1beta`
- **Model**: 默认 `gemini-3.5-flash`（原生 ID，不要带 `google/` 前缀）

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证**: `x-goog-api-key: ${apiKey}`
- 响应里的 `name` 可能带 `models/` 前缀，插件会自动去掉后再使用。

## 发送聊天请求

- **端点**:
  - 非流式：`${baseUrl}/models/${model}:generateContent`
  - 流式：`${baseUrl}/models/${model}:streamGenerateContent?alt=sse`
- **方法**: `POST`
- **认证**: `x-goog-api-key: ${apiKey}`
- **请求体**:
  ```json
  {
    "systemInstruction": {
      "parts": [{"text": "<系统提示词>"}]
    },
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "<用户提示词>"}]
      }
    ]
  }
  ```

## 总结

Ask AI Plugin 使用 Gemini 原生 REST：`systemInstruction` + `contents`，鉴权走请求头。若从 OpenRouter 复制模型名（如 `google/gemini-3.5-flash`），插件会自动去掉 `google/` 前缀。
