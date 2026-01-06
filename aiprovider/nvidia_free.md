# Nvidia Free API 请求示例

Worker URL: `https://nvidia-proxy.boy-liushaopeng.workers.dev`

## 1. 健康检查

### 请求
```bash
GET /api/health
```

```bash
curl https://nvidia-proxy.boy-liushaopeng.workers.dev/api/health
```

### 成功响应 (200)
```json
{
  "status": "ok",
  "timestamp": "2026-01-06T01:37:35.940Z",
  "service": "nvidia-proxy",
  "version": "1.0.0"
}
```

---

## 2. 获取模型列表

### 请求
```bash
GET /api/models
```

```bash
curl https://nvidia-proxy.boy-liushaopeng.workers.dev/api/models
```

### 成功响应 (200)
```json
{
  "object": "list",
  "data": [
    {
      "id": "meta/llama-3.3-70b-instruct",
      "object": "model",
      "created": 1234567890,
      "owned_by": "nvidia"
    }
  ]
}
```

### 错误响应 (500)
```json
{
  "error": "Failed to fetch models",
  "status": 500
}
```

---

## 3. 聊天接口（非流式）

### 请求
```bash
POST /api/chat
Content-Type: application/json
```

#### 请求头（可选）
```
X-User-UUID: 429e1288-3d7c-4733-8da9-7279c6bf29d7
X-Device-Fingerprint: dcb2173ba53ca489fe47c23e45175bb7
X-Client-Locale: zh_CN
X-Client-System: Darwin
X-Plugin-Version: 1.0.0
```

#### 请求体
```json
{
  "model": "meta/llama-3.3-70b-instruct",
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2000,
  "stream": false
}
```

#### cURL 示例
```bash
curl -X POST https://nvidia-proxy.boy-liushaopeng.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -H "X-User-UUID: 429e1288-3d7c-4733-8da9-7279c6bf29d7" \
  -H "X-Device-Fingerprint: dcb2173ba53ca489fe47c23e45175bb7" \
  -H "X-Client-Locale: zh_CN" \
  -d '{
    "model": "meta/llama-3.3-70b-instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 2000,
    "stream": false
  }'
```

### 成功响应 (200)
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "meta/llama-3.3-70b-instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm doing well, thank you for asking. How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

---

## 4. 聊天接口（流式）

### 请求
```bash
POST /api/chat
Content-Type: application/json
```

#### 请求体
```json
{
  "model": "meta/llama-3.3-70b-instruct",
  "messages": [
    {
      "role": "user",
      "content": "Tell me a short story"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2000,
  "stream": true
}
```

#### cURL 示例
```bash
curl -X POST https://nvidia-proxy.boy-liushaopeng.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -H "X-User-UUID: 429e1288-3d7c-4733-8da9-7279c6bf29d7" \
  -d '{
    "model": "meta/llama-3.3-70b-instruct",
    "messages": [
      {"role": "user", "content": "Tell me a short story"}
    ],
    "stream": true
  }'
```

### 成功响应 (200)
流式响应，每行一个 JSON 对象：

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"meta/llama-3.3-70b-instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"Once"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"meta/llama-3.3-70b-instruct","choices":[{"index":0,"delta":{"content":" upon"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"meta/llama-3.3-70b-instruct","choices":[{"index":0,"delta":{"content":" a"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"meta/llama-3.3-70b-instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## 错误响应示例

### 1. 速率限制 (429)
```json
{
  "error": "Rate limit exceeded",
  "message": "Rate limit exceeded: 10 requests per minute",
  "retryAfter": 60
}
```

### 2. 请求参数错误 (400)
```json
{
  "error": "Invalid request",
  "message": "messages field is required and must be an array"
}
```

### 3. Nvidia API 错误 (502/503)
```json
{
  "error": "Nvidia API error",
  "message": "API returned status 503",
  "details": "Service temporarily unavailable"
}
```

### 4. 方法不允许 (405)
```json
{
  "error": "Method Not Allowed"
}
```

### 5. 内部服务器错误 (500)
```json
{
  "error": "Internal Server Error",
  "message": "Unexpected error occurred"
}
```

---

## 请求参数说明

### messages 字段
- **必填**，数组类型
- 每个消息对象包含：
  - `role`: "user" | "assistant" | "system"
  - `content`: 消息内容（字符串）

### model 字段
- 可选，默认: `meta/llama-3.3-70b-instruct`
- 支持的模型请通过 `/api/models` 查询

### temperature 字段
- 可选，默认: `0.7`
- 范围: 0.0 - 2.0
- 控制输出随机性

### max_tokens 字段
- 可选，默认: `2000`
- 最大值: `4096`（受速率限制配置约束）
- 控制最大输出长度

### stream 字段
- 可选，默认: `false`
- `true`: 流式响应
- `false`: 一次性返回完整响应

---

## 速率限制

- **每分钟请求数**: 10 次/用户
- **每天请求数**: 100 次/用户或IP
- **每天 tokens**: 50000 tokens/用户
- **单次最大 tokens**: 4096 tokens

超过限制会返回 429 状态码，响应中包含 `retryAfter` 字段（秒）。

---

## 注意事项

1. 所有请求必须使用 HTTPS
2. Content-Type 必须为 `application/json`
3. 建议添加 `X-User-UUID` 和 `X-Device-Fingerprint` 请求头以获得更好的速率限制体验
4. 流式响应使用 Server-Sent Events (SSE) 格式
5. 本地开发时速率限制可能被禁用（KV 未配置）
