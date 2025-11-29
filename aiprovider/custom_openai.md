# Custom (OpenAI Format) 配置指南

适用于使用 OpenAI 格式的自定义服务，如 LocalAI、FastChat、vLLM 等。

## 核心配置

- **API Key**: 可选。在请求头中作为 Bearer Token 发送。
- **Base URL**: 必需。您的 API 基础地址（例如：`http://localhost:8000/v1`）

## 端点格式（固定）

- **聊天**: `${baseUrl}/chat/completions`
- **模型列表**: `${baseUrl}/models`

## 认证方式（固定）

标准 Bearer Token：
```json
{
  "Authorization": "Bearer ${apiKey}"
}
```

如果不需要认证，API Key 可以留空。

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
    "model": "your-model-name",
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ],
    "stream": true
  }
  ```

## 示例配置

### LocalAI
- **Base URL**: `http://localhost:8080/v1`
- **API Key**: 留空（LocalAI 默认不需要）
- **Model**: `gpt-3.5-turbo`

### FastChat
- **Base URL**: `http://localhost:8000/v1`
- **API Key**: 留空
- **Model**: `vicuna-7b`

### vLLM
- **Base URL**: `http://localhost:8000/v1`
- **API Key**: 留空
- **Model**: `meta-llama/Llama-2-7b-chat-hf`

### Text Generation WebUI (OpenAI 兼容模式)
- **Base URL**: `http://localhost:5000/v1`
- **API Key**: 留空
- **Model**: `your-model-name`

## 测试连接

1. 配置完成后，点击"加载模型"按钮
2. 如果连接成功，将显示可用的模型列表
3. 选择一个模型并保存配置
4. 在 AI Chat 中测试对话功能

## 注意事项

- 此模式使用固定的 OpenAI 端点格式，无法自定义端点路径
- 如果您的服务使用不同的端点路径，请使用 `Custom (Fully Customizable)` 模式
- 如果您的服务使用非标准认证方式（如 `X-API-Key`），请使用 `Custom (Fully Customizable)` 模式

## 总结

Custom (OpenAI Format) 是最简单的自定义模式，适合所有遵循 OpenAI API 格式的服务。配置简单，开箱即用。
