# Ask Grok

一个简单的 Calibre 插件，允许用户使用Grok询问关于书籍的问题。

## 功能

- 直接在Calibre选中书籍后中调用Grok问询关于书籍的问题
- 自动包含当前书籍的源数据信息，无需复制粘贴或手动输入
- 单次的输入输出对话界面
- 可配置更改API密钥
- 可配置提交的提示词模板
- 可预览的界面快捷键
- 可预览的插件版本信息

## 安装

### 安装方法（1/2）：通过calibre官方的插件市场进行安装

1. 打开calibre的`首选项`
2. 打开`插件`
3. 打开`获取新的插件`
4. 在`按名称筛选`中输入`Ask Grok`
5. 选中插件进行安装
6. 重启calibre

### 安装方法（2/2）：通过GitHub下载zip插件文件进行安装

1. 下载[Ask Grok zip file]()

导入文件到calibre的自定义插件：

1. 在calibre中选择"首选项" -> "插件" -> "从文件加载插件"
2. 选择下载的插件文件进行安装
3. 安装完成后，重启Calibre

## 获取Grok API Key

  - 进入Grok后台配置地址：https://console.x.ai/
  - 如果没有团队，创建团队
  - 选择并进入页面：API Keys
  - 点击按钮：Create API Keys
  - 输入API Key的命名，建议是：Calibre_Ask_Grok
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
- [全局]询问： Command + L；
- [全局]配置： Command + Shift + L
- [仅询问弹窗] 建议： Command + Shift + S
- [仅询问弹窗] 发送： Command + Enter

## 依赖要求

- Calibre 7.25 或更高版本
- Python module：Requests

## Grok API Key 说明

- API 调用次数依赖于隶属帐号的权限

## 隐私处理

- 发送请求给Grok时，插件会调用书籍的Metadate信息，其中包含：书名、作者、出版社，但不会包含可能含有用户自定义信息的 Tags、Comments等
- Grok API Key在输入后会保存一份Json文件到本地，不会传输到服务器
- 使用Python中的requests module，不会经过第三方服务器
- 本插件的隐私处理会依赖于Grok自身的隐私处理政策，由于仍然还没支持Private Chat：是的，Grok会使用你提交的数据进行模型训练
- 插件支持从本地的环境变量中获取API Key，在本地的环境变量中设置`XAI_AUTH_TOKEN`即可
  
Grok Private Chat is private and won't appear in user's history or be used to train models. Grok may securely retain it for up to 30 days for safety purposes.
