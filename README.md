# Ask Grok

一个简单的 Calibre 插件，允许用户使用Grok询问关于书籍的问题。

## 功能

- 直接在 Calibre 中调用 ChatGPT
- 自动包含当前书籍的相关信息
- 简单的对话界面
- 可配置的 API 密钥和提示词模板

## 安装方法

1. 下载插件文件
2. 压缩根目录为zip格式
3. 在 Calibre 中选择"首选项" -> "插件" -> "从文件加载插件"
4. 选择下载的插件文件进行安装
5. 安装完成后，重启 Calibre

## 配置说明

1. 安装插件后，在配置页面中设置你的 Grok API Key
2. 点击保存按钮后即可使用插件

## 使用方法

1. 在 Calibre 书库中选择一本书
2. 点击工具栏中的 "Ask Grok" 按钮
3. 在弹出的对话框中输入你的问题
4. 点击"发送"获取Grok的回答
5. 点击"建议？"，请求AI生成问题

## 快捷键
- [全局]询问： Command + L；
- [全局]配置： Command + Shift + L
- [仅询问弹窗] 建议： Command + Shift + S
- [仅询问弹窗] 发送： Command + Enter

## 开发说明

这是一个最小可行版本，包含以下核心功能：

- 配置Grok请求参数；
- 查看插件快捷键；
- 请求默认支持流式结果返回；

## 依赖要求

- Calibre 7.25 或更高版本
- OpenAI Python 包
- PyQt5

## 注意事项

- 需要有效的 Grok API Key，获取路径：https://console.x.ai/api
- API 调用次数依赖于隶属帐号的权限

## 隐私处理

- 发送请求给Grok时，会调用书籍的Metadate，其中包含：书名、作者、出版社等；
- Grok API Key在输入后会保存一份Json文件到本地，并不会传输到任何服务器端；
- 请求使用Python中的requests，并不会经过第三方服务器；
