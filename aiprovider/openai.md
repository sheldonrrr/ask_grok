# OpenAI (ChatGPT) 配置指南

Ask AI Plugin 的 **OpenAI** 提供商使用最新推荐的 **Responses API**（不再使用 Chat Completions）。

> 其他 OpenAI 兼容提供商（DeepSeek、OpenRouter、Custom 等）仍使用 `/chat/completions`，见 [openai_compatible.md](./openai_compatible.md)。

## 核心配置

- **API Key**: 必需。`Authorization: Bearer ${apiKey}`
- **Base URL**: 必需。例如 `https://api.openai.com/v1`
- **Model**: 例如 `gpt-5.4`

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证**:
  ```http
  Authorization: Bearer ${apiKey}
  ```

## 发送聊天请求（Responses API）

- **端点**: `${baseUrl}/responses`
- **方法**: `POST`
- **认证**:
  ```http
  Authorization: Bearer ${apiKey}
  Content-Type: application/json
  ```
- **请求体 (Body)**:
  ```json
  {
    "model": "gpt-5.4",
    "instructions": "<系统提示词>",
    "input": "<用户提示词>",
    "store": false,
    "temperature": 0.7
  }
  ```

### 字段说明

| Chat Completions（旧） | Responses（现用） |
| --- | --- |
| `messages[]` | `instructions` + `input` |
| `max_tokens` | `max_output_tokens` |
| `choices[0].message.content` | `output_text` 或 `output[].content[].text` |
| 默认可能存储 | 插件默认 `store: false` |

## 流式传输

- 请求体增加 `"stream": true`
- 关注 SSE 事件：
  - `response.output_text.delta`（字段 `delta`）
  - `response.completed`
  - `error`

## 总结

OpenAI/ChatGPT 提供商现已对齐官方推荐的 Responses 协议：`/v1/responses` + `instructions`/`input` + `store: false`。
