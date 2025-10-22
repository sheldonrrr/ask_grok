# Qwen配置指南

Qwen同样遵循 OpenAI 的 API 格式，但其 Base URL 根据服务区域有所不同。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。根据服务区域选择：
  - **北京**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
  - **新加坡**: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

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
    "model": "qwen-plus",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

配置 Qwen 的关键在于根据自己 API Key 的所属区域，正确填写 Base URL。
