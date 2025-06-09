# Ask Grok

一个简单的calibre插件，允许用户使用Grok询问关于书籍的问题。

## 预览

<img src="https://github.com/sheldonrrr/ask_grok/blob/main/ask_grok_gif_preview.gif" width="400">

## 功能

- 直接在calibre选中书籍后中调用Grok问询关于书籍的问题
- 自动包含当前书籍的源数据信息，无需复制粘贴或手动输入
- 单次的输入输出对话界面
- 可配置更改API密钥
- 可配置提交的提示词模板
- 可预览的界面快捷键
- 可预览的插件版本信息

## 安装

### 安装方法（1/2）：通过GitHub下载zip插件文件进行安装

1. 在[发布页](https://github.com/sheldonrrr/ask_grok/releases)下载最新版本。

导入文件到calibre的自定义插件：

1.1. 在calibre中选择"首选项" -> "插件" -> "从文件加载插件"
1.2. 选择下载的插件文件进行安装
1.3. 安装完成后，重启Calibre

### 安装方法（2/2）：通过calibre官方的插件市场进行安装

此方法需要该插件被添加到calibre插件索引之后才可以搜索到，如果可以搜索，我将在这里更新进入索引的日期

2.1. 打开calibre的`首选项`
2.2. 打开`插件`
2.3. 打开`获取新的插件`
2.4. 在`按名称筛选`中输入`Ask Grok`
2.5. 选中插件进行安装
2.6. 重启calibre

## 获取Grok API Key

  - 进入Grok后台配置地址：https://console.x.ai/
  - 如果没有团队，创建团队
  - 选择并进入页面：API Keys
  - 点击按钮：Create API Keys
  - 输入API Key的命名，建议是：calibre_Ask_Grok
  - 点击按钮：Save
  - 创建成功后会得到一个Key值：`Bearer x-ai *****`，或`x-ai *****`
  - 复制该Key

## 配置API Key

  - 点击菜单栏Ask Grok下拉菜单，选择`配置`
  - 把 API Key 输入到`X.AI授权令牌`输入框中
  - 点击按钮`保存`
  - 会出现`保存成功`的文字提示

## 界面使用

1. 在 Calibre 书库中选择一本书
2. 点击工具栏中的 "Ask Grok" 按钮
3. 在弹出的对话框中输入你的问题
4. 点击"发送"获取Grok的回答
5. 点击"建议？"，请求AI生成问题

## 快捷键
- [全局]询问： Command + L

## 语言支持
- 丹麦语 (Danish, da)
- 德语 (German, de)
- 英语 (English, en)
- 西班牙语 (Spanish, es)
- 芬兰语 (Finnish, fi)
- 法语 (French, fr)
- 日语 (Japanese, ja)
- 荷兰语 (Dutch, nl)
- 挪威语 (Norwegian, no)
- 葡萄牙语 (Portuguese, pt)
- 俄语 (Russian, ru)
- 瑞典语 (Swedish, sv)
- 简体中文 (Simplified Chinese, zh)
- 繁体中文 (Traditional Chinese, zht)
- 粤语 (Cantonese, yue)

## 依赖要求

- Calibre 7.25 或更高版本
- 外部 Python 模块：
  - requests
  - bleach
  - markdown2

### 使用的内置 Python 模块
- PyQt5（Qt 图形界面框架）
  - QtWidgets：QDialog、QVBoxLayout、QHBoxLayout、QLabel 等
  - QtCore：Qt、QTimer
  - Qt：QKeySequence、QAction、QMenu
- 标准库
  - os：文件和路径操作
  - sys：系统相关参数
  - json：JSON 数据处理
  - logging：调试和错误日志
  - datetime：时间操作
  - threading：线程管理

## Grok API Key 说明

- API 调用次数依赖于隶属帐号的权限

## 隐私处理

- 发送请求给Grok时，插件会调用书籍的Metadata信息，其中包含：书名、作者、出版社，但不会包含可能含有用户自定义信息的 Tags、Comments等
- Grok API Key在输入后会保存一份Json文件到本地，不会传输到服务器
- 使用Python中的requests module，不会经过第三方服务器
- 本插件的隐私处理会依赖于Grok自身的隐私处理政策，由于仍然还没支持Private Chat：是的，Grok会使用你提交的数据进行模型训练
- 插件支持从本地的环境变量中获取API Key，在本地的环境变量中设置`XAI_AUTH_TOKEN`即可

> **Grok官方声明**：Private Chat 是私密的，不会出现在用户历史记录中，也不会用于模型训练。出于安全目的，Grok 可能会安全地保留这些数据长达 30 天。
> 
> *原文：Grok Private Chat is private and won't appear in user's history or be used to train models. Grok may securely retain it for up to 30 days for safety purposes.*
