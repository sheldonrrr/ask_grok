# LM Studio (Local) 配置指南

LM Studio 可在本地加载 GGUF 等模型，并提供 **OpenAI 兼容 API**。

## 核心配置

- **API Key**: 通常不需要（可选）
- **Base URL**: 默认 `http://localhost:1234/v1`
- **Model**: 在 LM Studio 中先 Load 模型，再在插件中刷新列表

## 使用步骤

1. 打开 LM Studio，加载一个模型
2. 启动 Local Server（Developer → Start Server）
3. 在 Ask AI Plugin 添加 **LM Studio (Local)**
4. 确认 Base URL，点击刷新模型并测试

## 请求形态

- **模型列表**: `GET ${baseUrl}/models`
- **聊天**: `POST ${baseUrl}/chat/completions`（`messages` + 可选 `stream`）

## 总结

与 Custom OpenAI 兼容端点相同协议；专用入口仅预填 LM Studio 默认端口与说明。
