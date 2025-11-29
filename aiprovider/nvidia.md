# Nvidia API 配置指南

Nvidia 的 API 遵循 OpenAI 的格式，但存在一个主要的 **CORS 跨域问题**，需要特殊处理。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。官方地址为 `https://integrate.api.nvidia.com/v1`。

## 获取模型列表

- **端点**: `${baseUrl}/models`
- **方法**: `GET`
- **认证**: 
  ```json
  {
    "Authorization": "Bearer ${apiKey}"
  }
  ```
- **CORS 问题**: 直接从浏览器请求此端点会失败。必须通过一个后端代理来转发请求。
  - **解决方案**: 前端请求本地服务器的 `/proxy?url=https://integrate.api.nvidia.com/v1/models`，由本地服务器代为请求，并将结果返回给前端。

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
    "model": "meta/llama-4-maverick-17b-128e-instruct",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```
- **CORS 问题**: 与获取模型列表类似，发送聊天请求也可能需要通过代理，具体取决于目标服务器的策略。

## 总结

配置 Nvidia API 的最大挑战是处理 CORS 跨域问题。在前端应用中，必须设置一个后端代理来安全地转发所有对 Nvidia API 的请求。
