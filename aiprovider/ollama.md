# Ollama (本地大模型) 配置指南

Ollama 用于在本地运行大语言模型，其配置方式与其他云服务提供商有显著不同。

## 核心配置

- **API Key**: 不需要。
- **Base URL**: 必需。通常是本地服务的地址，例如 `http://localhost:11434`。

## 获取模型列表

- **端点**: `${baseUrl}/api/tags`
- **方法**: `GET`
- **认证**: 无。

## 发送聊天请求

- **端点**: `${baseUrl}/api/chat`
- **方法**: `POST`
- **认证**: 无。
- **请求体 (Body)**:
  ```json
  {
    "model": "<模型名称>",
    "messages": [
      {
        "role": 'user',
        "content": "<用户提示词>"
      }
    ],
    "stream": false // 在本项目中，我们使用非流式响应
  }
  ```

## 总结

Ollama 的配置非常简单，因为它在本地运行，无需 API Key 进行认证。所有操作都通过访问本地的 Base URL 完成。
