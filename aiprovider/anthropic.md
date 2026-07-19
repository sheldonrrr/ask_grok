# Anthropic (Claude) 配置指南

## 核心配置

- **API Key**: 必需。在请求头中作为 `x-api-key` 发送。
- **Base URL**: 必需。例如 `https://api.anthropic.com/v1`。
- **API Version**: 必需请求头 `anthropic-version: 2023-06-01`。

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证与请求头**:
  ```http
  x-api-key: ${apiKey}
  anthropic-version: 2023-06-01
  ```
- **响应**: `{"data":[{"id":"claude-opus-4-8", ...}]}`

## 发送聊天请求

- **端点**: `${baseUrl}/messages`
- **方法**: `POST`
- **认证与请求头**:
  ```http
  Content-Type: application/json
  x-api-key: ${apiKey}
  anthropic-version: 2023-06-01
  ```
- **请求体 (Body)**:
  ```json
  {
    "model": "claude-opus-4-8",
    "max_tokens": 4096,
    "system": "<系统提示词>",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 实现要点

1. 系统提示使用顶层 `system`，不要放进 `messages` 的 `role: system`（除非你明确使用 mid-conversation system 能力）。
2. `max_tokens` 是必填字段。
3. **Claude Opus 4.7 / 4.8 及更新 Opus**：不要发送 `temperature` / `top_p` / `top_k`，否则会返回 400。
4. 流式响应监听 `content_block_delta`（`text_delta`）与 `message_stop`。
5. 非流式响应从 `content[]` 中拼接所有 `type: "text"` 块。

## 总结

Anthropic Messages API 的关键是：`x-api-key` + `anthropic-version`，以及按模型代际正确省略采样参数。
