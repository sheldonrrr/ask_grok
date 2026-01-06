# Environment Configuration Guide

## 概述

`env_config.py` 文件用于管理 Nvidia Free 模型的测试和生产环境配置。

## 配置说明

### 切换环境

编辑 `env_config.py` 文件中的 `CURRENT_ENV` 变量：

```python
# 开发环境（本地测试）
CURRENT_ENV = 'development'

# 生产环境（云端部署）
CURRENT_ENV = 'production'
```

### 环境配置

#### Development（开发环境）
- **Proxy URL**: `http://localhost:8787`
- **用途**: 本地测试后端
- **测试命令**:
  ```bash
  # 健康检查
  curl http://localhost:8787/api/health

  # 测试聊天接口
  curl -X POST http://localhost:8787/api/chat \
    -H "Content-Type: application/json" \
    -d '{
      "model": "meta/llama-3.3-70b-instruct",
      "messages": [{"role": "user", "content": "hello"}]
    }'
  ```

#### Production（生产环境）
- **Proxy URL**: `https://nvidia-proxy.boy-liushaopeng.workers.dev`
- **用途**: Cloudflare Worker 生产服务器
- **注意**: 部署到云端后需要更新此 URL

## 使用方式

### 1. 本地开发测试

1. 启动本地后端服务器（端口 8787）
2. 设置 `CURRENT_ENV = 'development'`
3. 在 Calibre 中使用 Nvidia Free 模型

### 2. 生产环境部署

1. 将后端部署到 Cloudflare Workers
2. 更新 `production.proxy_url` 为实际的云端 URL
3. 设置 `CURRENT_ENV = 'production'`
4. 重新打包插件

## 添加新环境

如需添加新环境（如 staging），可在 `NVIDIA_FREE_CONFIG` 中添加：

```python
NVIDIA_FREE_CONFIG = {
    'development': {
        'proxy_url': 'http://localhost:8787',
        'description': 'Local development server',
    },
    'staging': {
        'proxy_url': 'https://nvidia-proxy-staging.workers.dev',
        'description': 'Staging server',
    },
    'production': {
        'proxy_url': 'https://nvidia-proxy.your-subdomain.workers.dev',
        'description': 'Cloudflare Worker production server',
    }
}
```

## 注意事项

1. 修改环境配置后需要重新加载插件
2. 确保本地服务器在测试前已启动
3. 生产环境 URL 需要在部署后更新
4. 环境切换不影响其他 AI 模型的配置
