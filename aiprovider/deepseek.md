# DeepSeek 配置指南

DeepSeek 遵循 OpenAI 的 API 格式，配置相对直接。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。官方地址为 `https://api.deepseek.com`。

## 获取模型列表

- **端点**: `${baseUrl}/v1/models`
- **方法**: `GET`
- **认证**: 
  ```json
  {
    "Authorization": "Bearer ${apiKey}"
  }
  ```

## 发送聊天请求

- **端点**: `${baseUrl}/v1/chat/completions`
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
    "model": "deepseek-chat",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

DeepSeek 是一个标准的 OpenAI 兼容 API，无需特殊处理。
