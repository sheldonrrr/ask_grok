# Custom (Fully Customizable) 配置指南

适用于使用非标准格式的自定义 AI 服务，支持完全自定义的认证和端点。

## 核心配置

- **API Key**: 可选。如果不使用自定义 Headers，将作为 Bearer Token 发送。
- **Base URL**: 必需。您的 API 基础地址（例如：`https://api.example.com`）

## 高级配置

### 自定义 Headers

在"Custom Headers"输入框中，输入 JSON 格式的键值对。

**示例 1：单个自定义 Header**
```json
{"X-API-Key": "your-api-key-here"}
```

**示例 2：多个自定义 Headers**
```json
{
  "X-API-Key": "your-api-key-here",
  "X-Custom-Header": "custom-value",
  "X-Request-ID": "12345"
}
```

**注意**：
- 如果填写了 Custom Headers，将使用自定义的认证方式
- 如果未填写 Custom Headers 但填写了 API Key，将使用标准的 `Authorization: Bearer ${apiKey}`
- Custom Headers 必须是有效的 JSON 格式

### 自定义端点

#### Models Endpoint（模型列表端点）
- **默认值**: `/models`
- **示例**: `/api/models`, `/v1/list`, `/api/v2/models`

#### Chat Endpoint（聊天端点）
- **默认值**: `/chat/completions`
- **示例**: `/api/chat`, `/v2/completions`, `/api/v1/chat`

**注意**：
- 端点路径会自动拼接到 Base URL 后面
- 端点路径应该以 `/` 开头
- 如果留空，将使用默认值

## 配置示例

### 示例 1：使用 X-API-Key 认证

**配置**:
- **Base URL**: `https://api.example.com`
- **API Key**: 留空
- **Model**: `custom-model`
- **Custom Headers**: `{"X-API-Key": "sk-1234567890"}`
- **Models Endpoint**: `/api/models`
- **Chat Endpoint**: `/api/chat`

**请求头**:
```json
{
  "Content-Type": "application/json",
  "X-API-Key": "sk-1234567890"
}
```

**请求 URL**:
- 聊天: `https://api.example.com/api/chat`
- 模型列表: `https://api.example.com/api/models`

### 示例 2：使用多个自定义 Headers

**配置**:
- **Base URL**: `https://api.example.com`
- **API Key**: 留空
- **Model**: `gpt-4`
- **Custom Headers**: `{"Api-Key": "key123", "X-Tenant-ID": "tenant456"}`
- **Models Endpoint**: `/v2/models`
- **Chat Endpoint**: `/v2/chat/completions`

**请求头**:
```json
{
  "Content-Type": "application/json",
  "Api-Key": "key123",
  "X-Tenant-ID": "tenant456"
}
```

**请求 URL**:
- 聊天: `https://api.example.com/v2/chat/completions`
- 模型列表: `https://api.example.com/v2/models`

### 示例 3：使用标准 Bearer Token（不填写 Custom Headers）

**配置**:
- **Base URL**: `https://api.example.com`
- **API Key**: `sk-1234567890`
- **Model**: `custom-model`
- **Custom Headers**: 留空
- **Models Endpoint**: `/models`
- **Chat Endpoint**: `/chat/completions`

**请求头**:
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer sk-1234567890"
}
```

## 发送聊天请求

- **端点**: `${baseUrl}${chatEndpoint}`（用户自定义）
- **方法**: `POST`
- **认证**: 根据配置决定
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

## 测试连接

1. 配置完成后，点击"加载模型"按钮
2. 系统将使用您配置的 Models Endpoint 获取模型列表
3. 如果连接成功，将显示可用的模型列表
4. 选择一个模型并保存配置
5. 在 AI Chat 中测试对话功能（使用 Chat Endpoint）

## 常见问题

### Q: Custom Headers 的格式是什么？
A: 必须是有效的 JSON 格式，键和值都用双引号包裹。例如：`{"X-API-Key": "value"}`

### Q: 如果我的服务不需要认证怎么办？
A: 将 API Key 和 Custom Headers 都留空即可。

### Q: 端点路径需要包含 Base URL 吗？
A: 不需要。端点路径会自动拼接到 Base URL 后面。例如 Base URL 是 `https://api.example.com`，Chat Endpoint 是 `/api/chat`，最终 URL 是 `https://api.example.com/api/chat`。

### Q: 我可以使用标准的 Bearer Token 吗？
A: 可以。如果不填写 Custom Headers，但填写了 API Key，系统会自动使用 `Authorization: Bearer ${apiKey}`。

### Q: Custom Headers 格式错误会怎样？
A: 系统会显示错误提示，并阻止保存无效配置。请确保输入的是有效的 JSON 格式。

## 注意事项

- Custom Headers 必须是有效的 JSON 格式
- 端点路径应该以 `/` 开头
- 如果使用本地服务（localhost, 127.0.0.1, 192.168.*），不会触发离线模式提示
- 所有请求都会通过后端代理，避免 CORS 问题

## 总结

Custom (Fully Customizable) 提供了最大的灵活性，可以连接几乎任何自定义 AI 服务。适合使用非标准认证方式或非标准端点的服务。
