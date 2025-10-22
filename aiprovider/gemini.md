# Google Gemini 配置指南

## 核心配置

- **API Key**: 必需。作为 URL 查询参数发送。
- **Base URL**: 必需。这是 API 的根地址，例如 `https://generativelanguage.googleapis.com/v1beta`。

## 获取模型列表

- **端点**: `${baseUrl}/models?key=${apiKey}`
- **方法**: `GET`
- **认证**: API Key 直接附加在 URL 的查询参数中。

## 发送聊天请求

- **端点**: `${baseUrl}/${model_name}:generateContent?key=${apiKey}`
- **方法**: `POST`
- **认证**: API Key 同样附加在 URL 的查询参数中。
- **请求体 (Body)**:
  ```json
  {
    "contents": [
      {
        "parts": [
          {
            "text": "<用户提示词>"
          }
        ]
      }
    ]
  }
  ```

## 总结

Gemini 的 API 设计比较独特：
1.  认证信息（API Key）通过 URL 参数传递，而非请求头。
2.  聊天请求的端点需要动态地将模型名称拼接进去，格式为 `${model_name}:generateContent`。
