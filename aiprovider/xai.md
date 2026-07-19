# SpaceXAI (Grok) 配置指南

SpaceXAI（原 xAI 品牌）提供 Grok 模型。官方文档现以 SpaceXAI 命名，API 主机仍为 `api.x.ai`。

Ask AI Plugin 的 **Grok** 提供商使用推荐的 **Responses API**。

## 核心配置

- **API Key**: 必需。`Authorization: Bearer ${apiKey}`（插件配置字段仍为 `auth_token`，兼容旧配置）
- **Base URL**: 必需。`https://api.x.ai/v1`
- **Model**: 默认 `grok-4.3`

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
    "model": "grok-4.3",
    "instructions": "<系统提示词>",
    "input": "<用户提示词>",
    "store": false
  }
  ```

### 可选字段

| 字段 | 说明 |
| --- | --- |
| `prompt_cache_key` | 会话粘性缓存路由（推荐长对话设置） |
| `max_output_tokens` | 最大输出 token |
| `temperature` | 采样温度 |
| `stream` | 是否流式返回 |

### 流式事件

- `response.output_text.delta`（字段 `delta`）
- `response.completed`
- `error`

## 兼容说明

- Chat Completions（`/v1/chat/completions`）仍可用，但新接入推荐 Responses API。
- 新模型如 `grok-4.5` 可手动填写；插件默认保持更稳妥的 `grok-4.3`。

## 总结

协议主机未变（`https://api.x.ai/v1`），品牌展示更新为 SpaceXAI，请求改为 Responses API，默认模型为 `grok-4.3`。
