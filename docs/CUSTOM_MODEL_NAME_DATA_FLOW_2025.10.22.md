# 自定义模型名称数据流分析

## 文档日期
2025-10-22

## 概述
本文档详细说明自定义模型名称功能的完整数据流，包括保存、加载、冲突处理等逻辑。

## 数据结构

### 配置文件格式
```json
{
  "models": {
    "grok": {
      "enabled": true,
      "auth_token": "xai-xxx",
      "api_base_url": "https://api.x.ai/v1",
      "model": "grok-4-latest",
      "use_custom_model_name": false,  // ← 关键字段：标记是否使用自定义
      "enable_streaming": true
    },
    "openai": {
      "enabled": true,
      "api_key": "sk-xxx",
      "api_base_url": "https://api.openai.com/v1",
      "model": "my-private-model",
      "use_custom_model_name": true,  // ← 用户自定义模型
      "enable_streaming": true
    }
  }
}
```

### 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `use_custom_model_name` | boolean | `true`: 使用自定义输入框的值<br>`false`: 使用下拉框选中的值 |
| `model` | string | 模型名称（来源取决于 `use_custom_model_name`） |

## 完整数据流

### 1. 初始化阶段

```
用户打开配置页面
    ↓
setup_ui() 创建控件
    ↓
├─ model_combo (下拉框) - 初始为空
├─ use_custom_model_checkbox (复选框) - 初始未勾选
└─ custom_model_input (输入框) - 初始禁用 (setEnabled(False))
    ↓
load_model_config() 加载配置
    ↓
读取配置: use_custom_model_name, model
```

### 2. 加载配置阶段

#### 场景 A：使用下拉框模式 (`use_custom_model_name = false`)

```
load_model_config()
    ↓
use_custom = false
    ↓
检查下拉框是否有数据
    ↓
├─ 有数据 (count > 0)
│   ↓
│   查找模型名称
│   ↓
│   ├─ 找到 (index >= 0)
│   │   └─> 选中该项: model_combo.setCurrentIndex(index)
│   │
│   └─ 未找到 (index < 0)
│       └─> 自动切换到自定义模式
│           ├─ use_custom_model_checkbox.setChecked(True)
│           └─ custom_model_input.setText(model_name)
│
└─ 无数据 (count = 0)
    ↓
    如果有模型名称
    └─> 自动切换到自定义模式
        ├─ use_custom_model_checkbox.setChecked(True)
        └─ custom_model_input.setText(model_name)
```

#### 场景 B：使用自定义模式 (`use_custom_model_name = true`)

```
load_model_config()
    ↓
use_custom = true
    ↓
直接设置自定义模式
    ↓
├─ use_custom_model_checkbox.setChecked(True)
│   └─> 触发 on_custom_model_toggled(state=2)
│       └─> custom_model_input.setEnabled(True)
│
└─ custom_model_input.setText(model_name)
```

### 3. 用户交互阶段

#### 用户勾选 "Use custom model name"

```
用户勾选复选框
    ↓
stateChanged 信号触发
    ↓
on_custom_model_toggled(state=2)
    ↓
use_custom = (state == 2) = True
    ↓
├─ model_combo.setEnabled(False)      // 禁用下拉框
├─ custom_model_input.setEnabled(True) // 启用输入框
│
└─ 复制当前选中的模型名称
    └─ custom_model_input.setText(model_combo.currentText())
```

#### 用户取消勾选 "Use custom model name"

```
用户取消勾选
    ↓
stateChanged 信号触发
    ↓
on_custom_model_toggled(state=0)
    ↓
use_custom = (state == 2) = False
    ↓
├─ model_combo.setEnabled(True)        // 启用下拉框
└─ custom_model_input.setEnabled(False) // 禁用输入框
```

### 4. 保存配置阶段

```
用户点击保存
    ↓
get_config() 收集配置
    ↓
检查 use_custom_model_checkbox.isChecked()
    ↓
├─ 已勾选 (True)
│   ↓
│   config['use_custom_model_name'] = True
│   config['model'] = custom_model_input.text().strip()
│   └─> 保存用户输入的自定义模型名称
│
└─ 未勾选 (False)
    ↓
    config['use_custom_model_name'] = False
    config['model'] = model_combo.currentText().strip()
    └─> 保存下拉框选中的模型名称
```

## 冲突处理机制

### 问题：模型名称与列表冲突

**场景：**
1. 用户使用自定义模式，输入了 "gpt-4o-mini"
2. 保存配置：`use_custom_model_name = true, model = "gpt-4o-mini"`
3. 下次加载时，模型列表中也有 "gpt-4o-mini"

**当前处理逻辑：**

```python
# load_model_config() 中的逻辑
if use_custom:
    # 使用自定义模式
    self.use_custom_model_checkbox.setChecked(True)
    self.custom_model_input.setText(model_name)
    # ✅ 即使模型名称在列表中，也会使用自定义模式
```

**结论：**
- ✅ **不会冲突**
- `use_custom_model_name` 字段明确标记了数据来源
- 加载时严格按照 `use_custom_model_name` 的值来决定使用哪个控件
- 即使模型名称相同，也能区分是"用户自定义"还是"从列表选择"

### 问题：向后兼容性

**场景：旧配置没有 `use_custom_model_name` 字段**

```python
# 旧配置
{
  "model": "gpt-4o-mini"
  # 没有 use_custom_model_name 字段
}
```

**当前处理逻辑：**

```python
use_custom = self.config.get('use_custom_model_name', False)  # ← 默认 False
```

**处理流程：**
1. `use_custom_model_name` 不存在，默认为 `False`
2. 尝试在下拉框中查找模型名称
3. 如果找到：选中该项
4. 如果未找到：自动切换到自定义模式

**结论：**
- ✅ **完全兼容**
- 旧配置会被视为"下拉框模式"
- 如果模型在列表中，正常选中
- 如果模型不在列表中，自动切换到自定义模式并保留模型名称

## 边界情况处理

### 1. 模型列表加载失败

```
用户打开配置页面
    ↓
model_combo.count() = 0  // 列表为空
    ↓
load_model_config()
    ↓
if model_name:
    自动切换到自定义模式
    └─> 用户可以继续使用已保存的模型名称
```

**结论：** ✅ 即使列表加载失败，用户仍可使用自定义输入框

### 2. 用户清空自定义输入框

```
用户勾选自定义模式
    ↓
清空输入框
    ↓
保存配置
    ↓
config['model'] = ''  // 空字符串
```

**影响：**
- 模型名称为空，API 调用可能失败
- 建议：添加验证逻辑（见"改进建议"）

### 3. 用户在自定义模式下输入列表中存在的模型

```
用户勾选自定义模式
    ↓
输入 "gpt-4o-mini" (列表中也有这个模型)
    ↓
保存配置
    ↓
use_custom_model_name = true
model = "gpt-4o-mini"
```

**下次加载：**
```
use_custom = true
    ↓
直接使用自定义模式
    ↓
custom_model_input.setText("gpt-4o-mini")
```

**结论：** ✅ 不会冲突，`use_custom_model_name` 明确标记了来源

### 4. 模型列表更新后，之前选中的模型不在新列表中

```
旧列表: ["gpt-4", "gpt-3.5-turbo"]
用户选择: "gpt-4"
保存: use_custom_model_name = false, model = "gpt-4"
    ↓
API 更新，新列表: ["gpt-4o", "gpt-4o-mini"]
    ↓
下次加载配置
    ↓
use_custom = false
model_combo.findText("gpt-4") = -1  // 未找到
    ↓
自动切换到自定义模式
    ↓
use_custom_model_checkbox.setChecked(True)
custom_model_input.setText("gpt-4")
```

**结论：** ✅ 自动降级到自定义模式，保留用户的模型选择

## 数据一致性保证

### 保存时的数据来源

| 复选框状态 | `use_custom_model_name` | `model` 来源 |
|-----------|------------------------|-------------|
| 未勾选 | `false` | `model_combo.currentText()` |
| 已勾选 | `true` | `custom_model_input.text()` |

### 加载时的数据流向

| `use_custom_model_name` | 模型列表状态 | 处理逻辑 |
|------------------------|------------|---------|
| `true` | 任意 | 直接使用自定义模式 |
| `false` | 列表中有该模型 | 选中下拉框中的项 |
| `false` | 列表中无该模型 | 自动切换到自定义模式 |
| `false` | 列表为空 | 自动切换到自定义模式 |

## 改进建议

### 1. 添加输入验证

**问题：** 用户可能输入空模型名称

**建议：**
```python
def get_config(self):
    # ... 现有代码 ...
    
    if config['use_custom_model_name']:
        model_name = self.custom_model_input.text().strip()
        if not model_name:
            # 显示警告
            QMessageBox.warning(
                self,
                self.i18n.get('warning', 'Warning'),
                self.i18n.get('empty_model_name', 'Model name cannot be empty')
            )
            return None  # 阻止保存
        config['model'] = model_name
```

### 2. 添加模型名称格式验证

**建议：**
```python
def validate_model_name(self, name: str) -> bool:
    """验证模型名称格式"""
    # 只允许字母、数字、连字符、下划线、点
    import re
    pattern = r'^[a-zA-Z0-9\-_.]+$'
    return bool(re.match(pattern, name))
```

### 3. 添加重复检测提示

**场景：** 用户在自定义模式下输入了列表中已有的模型

**建议：**
```python
def on_custom_model_input_changed(self):
    """自定义输入框内容变化时检查"""
    if not self.use_custom_model_checkbox.isChecked():
        return
    
    text = self.custom_model_input.text().strip()
    if self.model_combo.findText(text) >= 0:
        # 显示提示：该模型在列表中已存在
        self.custom_model_input.setStyleSheet("border: 1px solid orange;")
        # 可选：显示工具提示
        self.custom_model_input.setToolTip(
            self.i18n.get('model_exists_in_list', 'This model exists in the list')
        )
    else:
        self.custom_model_input.setStyleSheet("")
        self.custom_model_input.setToolTip("")
```

### 4. 添加"切换到列表模式"快捷操作

**场景：** 用户在自定义模式下输入了列表中已有的模型

**建议：** 在输入框旁边显示一个按钮
```python
if self.model_combo.findText(text) >= 0:
    # 显示"使用列表中的模型"按钮
    self.switch_to_list_button.setVisible(True)
```

## 测试用例

### 测试 1：基本保存和加载
1. 勾选自定义模式
2. 输入 "my-custom-model"
3. 保存配置
4. 重新打开配置页面
5. ✅ 验证：复选框已勾选，输入框显示 "my-custom-model"

### 测试 2：下拉框模式保存和加载
1. 不勾选自定义模式
2. 从下拉框选择 "gpt-4o-mini"
3. 保存配置
4. 重新打开配置页面
5. ✅ 验证：复选框未勾选，下拉框选中 "gpt-4o-mini"

### 测试 3：模型不在列表中的自动降级
1. 手动编辑配置文件：`use_custom_model_name = false, model = "non-existent-model"`
2. 打开配置页面
3. ✅ 验证：自动切换到自定义模式，输入框显示 "non-existent-model"

### 测试 4：向后兼容性
1. 删除配置文件中的 `use_custom_model_name` 字段
2. 打开配置页面
3. ✅ 验证：按下拉框模式处理，如果模型在列表中则选中

### 测试 5：模式切换时的数据复制
1. 下拉框选择 "gpt-4o-mini"
2. 勾选自定义模式
3. ✅ 验证：输入框自动填入 "gpt-4o-mini"

## 总结

### 当前实现的优点

1. ✅ **数据来源明确**：`use_custom_model_name` 字段清晰标记
2. ✅ **不会冲突**：即使模型名称相同，也能区分来源
3. ✅ **向后兼容**：旧配置自动按下拉框模式处理
4. ✅ **自动降级**：模型不在列表时自动切换到自定义模式
5. ✅ **用户友好**：切换模式时自动复制数据

### 数据流完整性

```
保存：复选框状态 → use_custom_model_name → 选择数据来源 → 保存到配置
                                              ↓
加载：读取配置 → use_custom_model_name → 恢复控件状态 → 填充数据
```

**结论：整个数据流是完整、一致、可靠的。用户自定义的模型名称会被正确保存和加载，不会与模型列表冲突。**
