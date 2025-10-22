# 配置保存信号未触发修复
**修复日期**: 2025-10-22  
**问题**: 保存配置后，主对话框的模型显示没有更新

---

## 问题描述

用户在配置界面切换模型（如从 x.AI 切换到 Ollama）并点击 Save 后，主对话框右上角的模型显示仍然显示旧的模型名称（x.AI），没有更新为新的模型（Ollama）。

---

## 根本原因

`AskGrokConfigWidget` 没有转发 `ConfigDialog` 的 `settings_saved` 信号，导致 `TabDialog.on_settings_saved()` 方法从未被调用。

### 信号传递链路

**预期的信号链路**:
```
ConfigDialog.save_settings()
  → emit settings_saved
    → AskGrokConfigWidget (应该转发)
      → TabDialog.on_settings_saved()
        → 更新 UI
```

**实际的信号链路（修复前）**:
```
ConfigDialog.save_settings()
  → emit settings_saved
    → ❌ AskGrokConfigWidget (没有转发)
      → ❌ TabDialog.on_settings_saved() (从未被调用)
```

---

## 修复内容

### 1. 添加 settings_saved 信号到 AskGrokConfigWidget

**位置**: `ui.py` 第 253-257 行

**修改前**:
```python
class AskGrokConfigWidget(QWidget):
    """配置页面组件"""
    # 定义一个与 ConfigDialog 相同的语言变更信号
    language_changed = pyqtSignal(str)
```

**修改后**:
```python
class AskGrokConfigWidget(QWidget):
    """配置页面组件"""
    # 定义与 ConfigDialog 相同的信号
    language_changed = pyqtSignal(str)
    settings_saved = pyqtSignal()  # 添加设置保存信号
```

### 2. 转发 ConfigDialog 的 settings_saved 信号

**位置**: `ui.py` 第 274-276 行

**修改前**:
```python
# 连接 ConfigDialog 的语言变更信号，并转发出去
self.config_dialog.language_changed.connect(self.on_language_changed)
```

**修改后**:
```python
# 连接 ConfigDialog 的信号，并转发出去
self.config_dialog.language_changed.connect(self.on_language_changed)
self.config_dialog.settings_saved.connect(self.settings_saved.emit)  # 转发设置保存信号
```

### 3. 简化 TabDialog 中的信号连接

**位置**: `ui.py` 第 434-438 行

**修改前**:
```python
self.setLayout(layout)

# 连接配置对话框的信号
self.config_widget.config_dialog.settings_saved.connect(self.on_settings_saved)

# 连接语言切换信号
self.config_widget.language_changed.connect(self.on_language_changed)
```

**修改后**:
```python
self.setLayout(layout)

# 连接配置组件的信号
self.config_widget.settings_saved.connect(self.on_settings_saved)
self.config_widget.language_changed.connect(self.on_language_changed)
```

---

## 修复后的信号链路

**修复后的完整信号链路**:
```
ConfigDialog.save_settings()
  → emit settings_saved (第 1532 行)
    → AskGrokConfigWidget.settings_saved (转发)
      → TabDialog.on_settings_saved() (第 499 行)
        → api.reload_model()
        → ask_dialog.api.reload_model()
        → ask_dialog.update_model_info()
          → 更新状态栏标签
          → 更新窗口标题
```

---

## 验证步骤

1. **打开主对话框**
   - 选择一本书
   - 点击 "Ask Grok" 打开对话框
   - 观察右上角显示 "Model: x.AI (Grok)"

2. **切换模型**
   - 打开配置界面
   - 切换到 "AI" 标签页
   - 选择 "Ollama (Local)"
   - 配置 Base URL
   - 点击 "Save"

3. **检查日志**
   - 应该看到 "=== on_settings_saved 被调用 ==="
   - 应该看到 "已重新加载全局 API 实例"
   - 应该看到 "正在更新已打开的AskDialog实例的模型信息"
   - 应该看到 "已更新AskDialog实例的模型信息"

4. **验证 UI 更新**
   - 返回主对话框
   - 右上角应该显示 "Model: Ollama (Local)"
   - 窗口标题应该包含 "[Ollama (Local)]"

---

## 相关代码位置

### 信号定义
- `config.py:733` - `ConfigDialog.settings_saved` 信号定义
- `ui.py:257` - `AskGrokConfigWidget.settings_saved` 信号定义

### 信号发出
- `config.py:1532` - `ConfigDialog.save_settings()` 发出信号

### 信号转发
- `ui.py:276` - `AskGrokConfigWidget` 转发信号

### 信号连接
- `ui.py:417` - `TabDialog` 连接 `config_dialog.settings_saved`（旧的，已移除）
- `ui.py:437` - `TabDialog` 连接 `config_widget.settings_saved`（新的）

### 信号处理
- `ui.py:499` - `TabDialog.on_settings_saved()` 处理信号

---

## 为什么之前没有发现这个问题？

1. **语言切换正常工作**: 因为 `language_changed` 信号已经被正确转发
2. **配置保存成功**: 配置确实被保存到磁盘，只是 UI 没有更新
3. **重启后正常**: 重启 Calibre 后，新配置会被加载，显示正确

---

## 修改文件

- `ui.py` - 3 处修改
  - `AskGrokConfigWidget` 类 - 添加 `settings_saved` 信号
  - `AskGrokConfigWidget.__init__()` - 转发 `settings_saved` 信号
  - `TabDialog.__init__()` - 简化信号连接

---

## 相关文档

- `docs/BUGFIX_MODEL_DISPLAY_UPDATE_2025.10.22.md` - 模型显示更新修复（之前的尝试）
- `docs/BUGFIX_OLLAMA_NO_API_KEY_2025.10.22.md` - Ollama API Key 修复

---

**修复状态**: ✅ 已完成  
**测试状态**: ⏳ 待测试  
**文档版本**: 1.0  
**最后更新**: 2025-10-22
