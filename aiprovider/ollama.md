# Ollama (Local) 配置指南

Ollama 在本地运行大语言模型。Ask AI Plugin 通过其 **OpenAI 兼容接口** 接入。

## 核心配置

- **API Key**: 通常不需要（可选）
- **Base URL**: 默认 `http://localhost:11434/v1`
- **Model**: 点击刷新从本地拉取；也可手动填写已 `ollama pull` 的模型名

## 获取模型列表

- **端点**: `${baseUrl}/models`（即 `http://localhost:11434/v1/models`）
- **方法**: `GET`
- **认证**: 无（除非自建反向代理要求）

## 发送聊天请求

- **端点**: `${baseUrl}/chat/completions`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "model": "<模型名称>",
    "messages": [
      {"role": "system", "content": "<系统提示词>"},
      {"role": "user", "content": "<用户提示词>"}
    ],
    "stream": true
  }
  ```

## 总结

请先启动 Ollama 服务，再在插件中刷新模型列表。旧版原生 `/api/chat` 路径已不再使用；请使用带 `/v1` 的 OpenAI 兼容 Base URL。
