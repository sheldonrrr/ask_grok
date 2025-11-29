# OpenAI 及其兼容提供商配置指南

此指南适用于 OpenAI 以及遵循其 API 格式的兼容提供商，包括 **DeepSeek, Qwen, OpenRouter, xAI, Nvidia, Custom**。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。这是 API 的根地址，例如 `https://api.openai.com/v1`。

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

这类提供商遵循了统一的 API 标准，配置相对简单。主要挑战在于处理像 Nvidia 这样的特例所带来的 CORS 问题。
