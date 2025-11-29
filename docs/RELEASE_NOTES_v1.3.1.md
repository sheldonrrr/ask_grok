# Release Notes - Ask AI Plugin v1.3.1

**发布日期：** 2025-11-05

---

## 🎉 主要更新

### 🔒 依赖隔离与冲突解决

**问题：** 用户反馈担心插件的第三方依赖可能与其他 calibre 插件产生冲突。

**解决方案：** 实施完整的命名空间隔离。

#### 技术改进

1. **移除重复依赖**
   - ✅ 删除 `webencodings`（calibre 已内置）
   - 💾 减少插件体积 ~10KB

2. **命名空间隔离**
   - ✅ 所有第三方库移至 `lib/ask_ai_plugin_vendor/`
   - ✅ 使用完整命名空间路径导入
   - ✅ 移除全局 `sys.path.insert`
   
3. **新的导入模式**
   ```python
   # 之前
   import requests
   import bleach
   import markdown2
   
   # 现在
   from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import requests
   from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import bleach
   from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import markdown2
   ```

#### 效果

- ✅ **零冲突**：不会与其他插件的依赖冲突
- ✅ **完全隔离**：每个插件使用自己的库版本
- ✅ **向后兼容**：用户无需任何操作
- ✅ **更稳定**：避免因其他插件导致的崩溃

---

### 🐛 Bug 修复

#### 修复 Enable/disable plugin 按钮报错

**问题：** Windows 用户点击插件管理器中的 "Enable/disable plugin" 按钮时报错：
```
AttributeError: 'AskAIPluginUI' object has no attribute 'config_widget'
```

**原因：** `AskAIPluginUI` 类缺少 calibre 插件 API 要求的 `config_widget()` 和 `save_settings()` 方法。

**修复：** 在 `ui.py` 中添加了这两个方法。

**测试：** ✅ 通过

---

### 📦 依赖更新

更新 `requirements.txt`，精确同步所有 vendor 库版本：

```
requests==2.32.3
urllib3==2.3.0
certifi==2025.1.31
charset-normalizer==3.4.1
idna==3.10
bleach==6.2.0
markdown2==2.5.3
```

---

### 📚 文档改进

新增文档：

1. **依赖冲突分析**
   - `docs/DEPENDENCY_CONFLICT_ANALYSIS.md`
   - 详细分析问题和解决方案

2. **Vendor 命名空间实施文档**
   - `docs/VENDOR_NAMESPACE_IMPLEMENTATION.md`
   - 完整的实施步骤和测试结果

3. **版本号更新指南**
   - `docs/VERSION_UPDATE_GUIDE.md`
   - 详细的版本号管理规则和检查清单

4. **版本号快速检查清单**
   - `docs/VERSION_UPDATE_CHECKLIST.md`
   - 一页纸的快速参考

5. **变更日志**
   - `CHANGELOG_VENDOR_NAMESPACE.md`
   - 本次更新的详细变更记录

---

## 🔧 技术细节

### 修改的文件（15 个）

**核心文件：**
- `__init__.py` - 移除 sys.path.insert，更新版本号
- `api.py` - 更新导入语句
- `ui.py` - 更新导入语句，添加 config_widget() 方法
- `response_handler.py` - 更新导入语句
- `version.py` - 更新版本号
- `requirements.txt` - 同步版本号

**模型文件（9 个）：**
- `models/base.py`
- `models/openai.py`
- `models/anthropic.py`
- `models/nvidia.py`
- `models/grok.py`
- `models/deepseek.py`
- `models/gemini.py`
- `models/ollama.py`
- `models/custom.py`
- `models/openrouter.py`

### 新增文件

- `lib/ask_ai_plugin_vendor/__init__.py` - Vendor 包初始化
- 5 个文档文件（见上文）

### 删除文件

- `lib/webencodings/` - 重复依赖
- `lib/webencodings-0.5.1.dist-info/`

---

## 📊 测试结果

### ✅ 所有测试通过

1. **Vendor 库导入测试**
   - ✅ 7 个库全部导入成功
   - ✅ 版本号正确

2. **命名空间隔离测试**
   - ✅ 63 个 vendor 模块加载
   - ✅ 全部在独立命名空间
   - ✅ requests 未污染全局命名空间

3. **AI 模型导入测试**
   - ✅ 9 个 AI 模型全部导入成功
   - ✅ API 客户端正常
   - ✅ ResponseHandler 正常

4. **插件功能测试**
   - ✅ calibre 正常启动
   - ✅ 插件正常加载
   - ✅ 版本号显示正确（v1.3.1）
   - ✅ Enable/disable 按钮正常

---

## 🚀 升级说明

### 用户无需任何操作

- ✅ 所有配置自动保留
- ✅ 所有功能正常工作
- ✅ 自动更新（如果启用）

### 手动更新

1. 下载最新版本插件
2. 在 calibre 中：`Preferences → Plugins → Load plugin from file`
3. 选择下载的 ZIP 文件
4. 重启 calibre

---

## 🙏 致谢

感谢用户反馈依赖冲突的担忧，这促使我们实施了更健壮的解决方案，让 Ask AI Plugin 与其他 calibre 插件更好地共存。

---

## 📝 下一步计划

### 可能的优化（未来版本）

1. **移除 bleach**
   - 使用 `html.escape()` 替代
   - 减少 ~50KB

2. **简化 markdown2**
   - 实现轻量级 Markdown 渲染器
   - 减少 ~160KB

3. **研究 calibre 原生 HTTP 库**
   - 如果支持流式响应，可移除 requests
   - 实现零依赖

---

## 🔗 相关链接

- **用户手册：** http://simp.ly/publish/FwMSSr
- **关于插件：** http://simp.ly/publish/xYW5Tr
- **GitHub：** [如果有的话]
- **问题反馈：** sheldonrrr@gmail.com

---

## 版本信息

- **版本号：** 1.3.1
- **发布日期：** 2025-11-05
- **支持的 calibre 版本：** 6.0.0+
- **支持的平台：** Windows, macOS, Linux

---

**Ask AI Plugin - 让 AI 帮你更好地阅读！** 📚✨
