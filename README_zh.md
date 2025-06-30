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
- 自动显示当前书籍的最近查询历史
- 支持复制回答，复制问题和回答

## 安装

在[发布页](https://github.com/sheldonrrr/ask_grok/releases)下载最新版本。

导入文件到calibre的自定义插件：

1.1. 在calibre中选择"首选项" -> "插件" -> "从文件加载插件"
1.2. 选择下载的插件文件进行安装
1.3. 安装完成后，重启calibre

## 获取Grok API Key

  - 进入Grok后台配置地址：https://console.x.ai/
  - 如果没有团队，创建团队
  - 选择并进入页面：API Keys
  - 点击按钮：Create API Keys
  - 输入API Key的命名
  - 点击按钮：Save
  - 创建成功后会得到一个Key值：`x-ai *****`
  - 复制该Key

## 配置API Key

  - 点击菜单栏Ask Grok下拉菜单，选择`配置`
  - 把 API Key 输入到`X.AI授权令牌`输入框中
  - 点击按钮`保存`
  - 会出现`保存成功`的文字提示

## 界面使用

1. 在 calibre 书库中选择一本书
2. 点击工具栏中的 "Ask Grok" 按钮
3. 在弹出的对话框中输入你的问题
4. 点击"发送"获取Grok的回答
5. 点击"随机问题"，请求AI生成问题

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

- calibre 7.25 或更高版本
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

- 您输入的Grok API Key会保存一份Json文件到本地文件夹，不会传输到任何第三方服务器上
- 发送请求给Grok时，插件会调用书籍的Metadata信息，用户在界面中看到的Metadata信息，就是插件会提交给Grok的Metadata信息
- 本插件的隐私处理会依赖于Grok自身的隐私处理政策，由于插件还没支持默认开启Private Chat，所以Grok会使用你提交的数据进行模型训练

# 故障排查

如果持续出现`请求失败`或其他无法使用情况，请彻底删除Ask Grok及相关的配置文件后重新安装最新版插件即可解决。

彻底删除Ask Grok的本地配置文件和插件文件夹：
- calibre 首选项
- 杂项
- 打开`calibre 配置`文件夹
- 打开`Plugins`文件夹
- 删除所有带有`ask_grok`前缀的文件或文件夹
- 重新安装最新版插件
- 重启calibre

Ask Grok的配置文件说明：
- Ask Grok.zip/Ask Grok 文件夹: 插件文件夹，删除后插件即会被删除
- ask_grok.json: 插件配置文件，删除后插件的配置信息即会被删除
- ask_grok.logs 文件夹: 插件日志文件夹，删除后插件的日志信息即会被删除
- ask_grok_latest_history.json: 插件最近查询历史文件，删除后插件的最近查询历史信息即会被删除

注意！
- 反馈时无需提供您的Grok API Key，请注意保密，一旦泄漏，您的Grok API Key将存在被滥用的风险