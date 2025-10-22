# 模型显示更新修复
**修复日期**: 2025-10-22  
**问题**: 配置界面切换模型后，主对话框右上角的模型显示没有更新

---

## 问题描述

用户在配置界面切换到 OpenRouter 并保存后，主对话框右上角的 AI 提示仍然显示之前的模型（如 "x.AI (Grok)"），没有更新为 "OpenRouter"。

---

## 根本原因

在 `on_settings_saved()` 方法中，虽然重新加载了全局的 API 实例，但没有重新加载 `AskDialog` 实例中的 API 实例。

### 代码架构说明

1. **全局 API 实例**: `calibre_plugins.ask_grok.api.api`
   - 在 `api.py` 中创建的全局单例

2. **插件 API 实例**: `InterfacePlugin.api`
   - 在插件主类中创建的实例

3. **对话框 API 实例**: `AskDialog.api`
   - 通过构造函数传递给 `AskDialog` 的实例

这三个可能是不同的对象实例，因此需要分别重新加载。

---

## 修复内容

### 修改 `on_settings_saved()` 方法

**位置**: `ui.py` 第 497 行

**修改前**:
```python
def on_settings_saved(self):
    """当设置保存时的处理函数"""
    import logging
    logger = logging.getLogger(__name__)
    
    # 重新加载模型，确保使用最新选择的模型
    from calibre_plugins.ask_grok.api import api
    api.reload_model()
    logger.debug("已重新加载模型")
    
    # 更新已打开的AskDialog实例的模型信息
    try:
        if (hasattr(ask_grok_plugin, 'plugin_instance') and 
            ask_grok_plugin.plugin_instance and 
            hasattr(ask_grok_plugin.plugin_instance, 'ask_dialog') and 
            ask_grok_plugin.plugin_instance.ask_dialog):
            
            logger.debug("正在更新已打开的AskDialog实例的模型信息")
            ask_grok_plugin.plugin_instance.ask_dialog.update_model_info()
            logger.debug("已更新AskDialog实例的模型信息")
    except Exception as e:
        logger.error(f"更新AskDialog实例的模型信息时出错: {str(e)}")
```

**修改后**:
```python
def on_settings_saved(self):
    """当设置保存时的处理函数"""
    import logging
    logger = logging.getLogger(__name__)
    
    # 重新加载全局 API 实例
    from calibre_plugins.ask_grok.api import api
    api.reload_model()
    logger.debug("已重新加载全局 API 实例")
    
    # 更新已打开的AskDialog实例的模型信息
    try:
        if (hasattr(ask_grok_plugin, 'plugin_instance') and 
            ask_grok_plugin.plugin_instance and 
            hasattr(ask_grok_plugin.plugin_instance, 'ask_dialog') and 
            ask_grok_plugin.plugin_instance.ask_dialog):
            
            logger.debug("正在更新已打开的AskDialog实例的模型信息")
            # ✅ 确保 AskDialog 的 API 实例也被重新加载
            if hasattr(ask_grok_plugin.plugin_instance.ask_dialog, 'api'):
                ask_grok_plugin.plugin_instance.ask_dialog.api.reload_model()
                logger.debug("已重新加载 AskDialog 的 API 实例")
            # 然后更新 UI 显示
            ask_grok_plugin.plugin_instance.ask_dialog.update_model_info()
            logger.debug("已更新AskDialog实例的模型信息")
    except Exception as e:
        logger.error(f"更新AskDialog实例的模型信息时出错: {str(e)}")
```

---

## 修复逻辑

### 更新流程

1. **保存配置** → `ConfigDialog.save_settings()`
2. **发出信号** → `settings_saved.emit()`
3. **处理信号** → `TabDialog.on_settings_saved()`
4. **重新加载 API**:
   - ✅ 重新加载全局 API 实例
   - ✅ 重新加载 AskDialog 的 API 实例（**新增**）
5. **更新 UI** → `AskDialog.update_model_info()`
   - 更新状态栏的模型信息标签
   - 更新窗口标题

### update_model_info() 方法

该方法负责更新 UI 显示：

```python
def update_model_info(self):
    """更新模型信息显示"""
    try:
        # 确保模型已经重新加载
        self.api.reload_model()
        
        # 获取最新的模型显示名称
        model_display_name = self.api.model_display_name
        
        # 更新状态栏中的模型信息标签
        if hasattr(self, 'model_info_label') and self.model_info_label:
            self.model_info_label.setText(f"{self.i18n.get('using_model', 'Model')}: {model_display_name}")
        
        # 更新窗口标题
        if hasattr(self, 'book_info') and self.book_info:
            self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
            
    except Exception as e:
        logger.error(f"更新模型信息时出错: {str(e)}")
```

---

## 修改文件

- `ui.py` - 修改 `on_settings_saved()` 方法

---

## 验证步骤

1. **打开主对话框**
   - 选择一本书
   - 点击 "Ask Grok" 打开对话框
   - 观察右上角的模型显示（如 "Model: x.AI (Grok)"）

2. **切换模型**
   - 打开配置界面
   - 切换到 "AI" 标签页
   - 从下拉菜单选择 "OpenRouter"
   - 配置 API Key
   - 点击 "Save" 保存

3. **验证更新**
   - 返回主对话框
   - 右上角的模型显示应该立即更新为 "Model: OpenRouter"
   - 窗口标题也应该更新为包含 "[OpenRouter]"

4. **测试其他模型**
   - 重复步骤 2-3，测试切换到其他模型（Ollama, Nvidia, Anthropic 等）
   - 每次保存后，主对话框的显示都应该立即更新

---

## 相关代码位置

### UI 更新相关
- `ui.py:497` - `on_settings_saved()` 方法
- `ui.py:842` - `update_model_info()` 方法
- `ui.py:856` - 更新状态栏标签
- `ui.py:864` - 更新窗口标题

### API 重新加载
- `api.py:533` - 全局 API 实例
- `api.py:XXX` - `reload_model()` 方法

### 配置保存
- `config.py:1482` - `save_settings()` 方法
- `config.py:1526` - 发出 `settings_saved` 信号

---

## 技术细节

### API 实例的生命周期

1. **全局实例**: 在模块加载时创建，整个应用程序共享
2. **插件实例**: 在插件初始化时创建
3. **对话框实例**: 在对话框打开时传递

### 为什么需要分别重新加载？

因为每个实例都有自己的状态（如当前模型、配置等），如果只重新加载全局实例，对话框实例的状态不会改变，导致显示不更新。

### reload_model() 方法的作用

```python
def reload_model(self):
    """重新加载模型配置"""
    # 从配置中读取最新的 selected_model
    # 创建新的模型实例
    # 更新 self._ai_model
    # 更新 self.model_name 和 self.model_display_name
```

---

## 相关文档

- `docs/BUGFIX_CONFIG_UI_OPENROUTER_OLLAMA_2025.10.22.md` - 配置界面修复
- `docs/BUGFIX_OPENROUTER_ABSTRACT_METHOD_2025.10.22.md` - OpenRouter 抽象方法修复
- `docs/IMPLEMENTATION_COMPLETE_OPENROUTER_OLLAMA_2025.10.22.md` - OpenRouter/Ollama 实施报告

---

**修复状态**: ✅ 已完成  
**测试状态**: ⏳ 待测试  
**文档版本**: 1.0  
**最后更新**: 2025-10-22
