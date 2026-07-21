# Kimi (Moonshot) 配置指南

Kimi 遵循 OpenAI 的 API 格式，配置相对直接。

## 核心配置

- **API Key**: 必需。在请求头中作为 Bearer Token 发送。
- **平台**: 添加/编辑 Kimi 时选择 **国际版** 或 **中国大陆版**（决定 Base URL）：
  - **国际版**: `https://api.moonshot.ai/v1`
  - **中国大陆版**: `https://api.moonshot.cn/v1`
- Base URL 由平台选项决定（只读显示），Key 与平台不可混用。

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

### 参数注意

- `kimi-k*`（如 `kimi-k3`、`kimi-k2.5`）**temperature 只能为 1**（或不传）。传 `0.7` 会返回 `400 invalid temperature`。
- 经典 `moonshot-v1-*` 模型仍可使用常规 temperature。

## 常见失败原因

若 Key 来自中国站（platform.moonshot.cn）却选择了国际版，加载模型会返回 `401 Invalid Authentication`。在添加弹窗中切换到 **中国大陆版** 即可。

界面语言为中文时，默认选中中国大陆版；否则默认国际版。加载/测试时若鉴权失败，仍会自动尝试另一区域一次并回写平台选项。

## 总结

Kimi 是一个标准的 OpenAI 兼容 API。注意国际与中国大陆平台的 API Key 与 Base URL 不可混用。
