# KoboldCpp (Local) 配置指南

KoboldCpp 在默认端口提供 **OpenAI 兼容 API**（`/v1`）。

## 核心配置

- **API Key**: 通常不需要（可选）
- **Base URL**: 默认 `http://localhost:5001/v1`
- **Model**: 启动并加载模型后，在插件中刷新列表

## 使用步骤

1. 启动 KoboldCpp 并加载模型（默认端口 `5001`）
2. 确认 OpenAI 兼容路由可用：`http://localhost:5001/v1`
3. 在 Ask AI Plugin 添加 **KoboldCpp (Local)**
4. 刷新模型列表并测试对话

> 若本机 `localhost` 解析到 IPv6 出问题，可将 Base URL 改为 `http://127.0.0.1:5001/v1`。

## 请求形态

- **模型列表**: `GET ${baseUrl}/models`
- **聊天**: `POST ${baseUrl}/chat/completions`（`messages` + 可选 `stream`）

## 总结

专用入口预填 KoboldCpp 默认地址；协议与其他 OpenAI 兼容本地服务一致。
