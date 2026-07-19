# OpenAI 兼容提供商配置指南

此指南适用于遵循 **Chat Completions** 格式的兼容提供商，包括 **DeepSeek, Qwen, OpenRouter, xAI, Nvidia, Custom, Mistral, Kimi** 等。

> 插件内置的 **OpenAI (ChatGPT)** 提供商已改用 Responses API，请看 [openai.md](./openai.md)。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。这是 API 的根地址，例如 `https://api.deepseek.com`。

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证**: 
  ```json
  {
    "Authorization": "Bearer ${apiKey}"
  }
  ```
- **注意事项**:
  - **Nvidia**: 直接从浏览器请求此端点会遇到 CORS 跨域问题。需要通过本地服务器代理该请求。

## 发送聊天请求

- **端点**: `${baseUrl}/chat/completions`
- **方法**: `POST`
- **认证**: 
  ```json
  {
    "Authorization": "Bearer ${apiKey}"
  }
  ```
- **请求体 (Body)**:
  ```json
  {
    "model": "<模型名称>",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

这类提供商遵循 Chat Completions API 标准，配置相对简单。真正的 OpenAI/ChatGPT 官方接口请改用 Responses API。
