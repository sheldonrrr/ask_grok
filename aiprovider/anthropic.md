# Anthropic (Claude) 配置指南

## 核心配置

- **API Key**: 必需。在请求头中作为 `x-api-key` 发送。
- **Base URL**: 必需。这是 API 的根地址，例如 `https://api.anthropic.com/v1`。

## 获取模型列表

- **端点**: Anthropic 不提供公开的、用于自动获取模型列表的 API 端点。
- **方法**: N/A
- **解决方案**: 模型名称需要用户手动输入或在前端硬编码。

## 发送聊天请求

- **端点**: `${baseUrl}/messages`
- **方法**: `POST`
- **认证与请求头**:
  ```json
  {
    "Content-Type": "application/json",
    "x-api-key": "${apiKey}",
    "anthropic-version": "2023-06-01" // 版本号是必需的
  }
  ```
- **请求体 (Body)**:
  ```json
  {
    "model": "<模型名称>",
    "max_tokens": 4096, // 建议设置一个最大输出长度
    "messages": [
      {
        "role": "user",
        "content": "<用户提示词>"
      }
    ]
  }
  ```

## 总结

Anthropic 的 API 有两个关键点：
1.  支持自动获取模型列表

curl https://api.anthropic.com/v1/models \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01"

2.  请求头中除了 API Key (`x-api-key`)，还必须包含一个明确的 API 版本号 (`anthropic-version`)。
