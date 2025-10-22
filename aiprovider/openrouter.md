# OpenRouter 配置指南

OpenRouter 是一个模型聚合器，它也遵循 OpenAI 的 API 格式，但支持一些额外的可选请求头。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。官方地址为 `https://openrouter.ai/api/v1`。

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
- **认证与请求头**:
  ```json
  {
    "Authorization": "Bearer ${apiKey}",
    "HTTP-Referer": "<你的网站URL>", // 可选，用于在 OpenRouter 上进行排名
    "X-Title": "<你的网站名称>" // 可选，用于在 OpenRouter 上进行排名
  }
  ```
- **请求体 (Body)**:
  ```json
  {
    "model": "openai/gpt-4o", // 模型名称通常带有前缀，如 openai/
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

OpenRouter 的配置是标准的 OpenAI 兼容模式，但它允许通过 `HTTP-Referer` 和 `X-Title` 这两个可选的请求头来标识你的应用。

## 官方指引：

curl https://openrouter.ai/api/v1/models

## 官方指引中的 retrieved 返回示例

{
  "data": [
    {
      "id": "string",
      "name": "string",
      "created": 1741818122,
      "description": "string",
      "architecture": {
        "input_modalities": [
          "text",
          "image"
        ],
        "output_modalities": [
          "text"
        ],
        "tokenizer": "GPT",
        "instruct_type": "string"
      },
      "top_provider": {
        "is_moderated": true,
        "context_length": 128000,
        "max_completion_tokens": 16384
      },
      "pricing": {
        "prompt": "0.0000007",
        "completion": "0.0000007",
        "image": "0",
        "request": "0",
        "web_search": "0",
        "internal_reasoning": "0",
        "input_cache_read": "0",
        "input_cache_write": "0"
      },
      "canonical_slug": "string",
      "context_length": 128000,
      "hugging_face_id": "string",
      "per_request_limits": {},
      "supported_parameters": [
        "string"
      ],
      "default_parameters": {
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0
      }
    }
  ]
}