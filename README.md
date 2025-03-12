# Calibre Ask Grok 插件

一个简单的 Calibre 插件，允许用户使用 ChatGPT 询问关于当前阅读书籍的问题。

## 功能特点

- 直接在 Calibre 中调用 ChatGPT
- 自动包含当前书籍的相关信息
- 简单的对话界面
- 可配置的 API 密钥和提示词模板

## 安装方法

1. 下载插件文件
2. 在 Calibre 中选择"首选项" -> "插件" -> "从文件加载插件"
3. 选择下载的插件文件进行安装
4. 安装完成后，重启 Calibre

## 配置说明

1. 安装插件后，在插件配置页面中设置你的 OpenAI API Key
2. 可以自定义提示词模板（可选）

## 使用方法

1. 在 Calibre 库中选择一本书
2. 点击工具栏中的 "Ask GPT" 按钮
3. 在弹出的对话框中输入你的问题
4. 点击"发送"获取 ChatGPT 的回答

## 开发说明

这是一个最小可行版本，包含以下核心文件：

- `__init__.py`: 插件入口
- `ui.py`: 用户界面实现
- `api.py`: ChatGPT API 调用
- `config.py`: 配置管理

## 依赖要求

- Calibre 7.25 或更高版本
- OpenAI Python 包
- PyQt5

## 注意事项

- 需要有效的 OpenAI API Key
- 请遵守 OpenAI 的使用条款
- API 调用可能产生费用
