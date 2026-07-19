# Kimi (Moonshot) 配置指南

Kimi 遵循 OpenAI 的 API 格式，配置相对直接。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。根据 API Key 所属区域选择：
  - **国际**: `https://api.moonshot.ai/v1`（插件默认）
  - **中国大陆**: `https://api.moonshot.cn/v1`

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证**:
  ```json
  {
    "Authorization": "Bearer ${apiKey}"
  }
  ```

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
    "model": "kimi-k3",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

Kimi 是一个标准的 OpenAI 兼容 API。注意国际与中国大陆平台的 API Key 与 Base URL 不可混用。
