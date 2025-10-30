# UI界面优化指南

## 当前问题分析

### 1. **间距不统一**
- 有的地方用5px，有的用10px，有的用15px
- 缺乏系统性的间距规范
- 导致视觉上不够整齐

### 2. **对齐问题**
- 标签和输入框没有统一对齐
- 不同组件的左边距不一致
- GroupBox内的内容对齐混乱

### 3. **视觉层次不清晰**
- 缺少明确的视觉分组
- 分隔线使用不够一致
- 重要和次要信息没有明显区分

## 优化方案

### 一、建立8px间距系统

使用8px作为基准单位（符合Material Design和iOS设计规范）：

```
4px  - 极小间距（组件内部）
8px  - 小间距（相关元素）
16px - 中等间距（不同组之间）
24px - 大间距（主要区块）
32px - 超大间距（页面级分隔）
```

### 二、统一对齐规则

#### 1. **表单布局（QFormLayout）**
```python
# 标签宽度统一
form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
form_layout.setHorizontalSpacing(16)  # 标签和字段间距
form_layout.setVerticalSpacing(12)    # 行间距
```

#### 2. **水平布局（QHBoxLayout）**
```python
layout = QHBoxLayout()
layout.setSpacing(8)           # 元素间距
layout.setContentsMargins(0, 0, 0, 0)  # 边距
```

#### 3. **垂直布局（QVBoxLayout）**
```python
layout = QVBoxLayout()
layout.setSpacing(16)          # 组件间距
layout.setContentsMargins(16, 16, 16, 16)  # 边距
```

### 三、GroupBox优化

#### 当前问题：
```python
# 样式字符串太长，难以维护
setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 15px; ...")
```

#### 优化方案：
```python
from .ui_constants import get_groupbox_style

group_box.setStyleSheet(get_groupbox_style())
```

### 四、具体优化建议

#### 1. **General标签页布局**

**优化前：**
- 语言选择、AI选择、配置项混在一起
- 间距不统一
- 视觉层次不清

**优化后结构：**
```
┌─ Display ─────────────────────┐
│ Language:     [Dropdown ▼]    │  ← 16px padding
└───────────────────────────────┘
                                    ← 24px spacing
┌─ AI Configuration ────────────┐
│ Current AI:   [Dropdown ▼]    │  ← 16px padding
│                                │  ← 16px spacing
│ ┌─ Model Settings ──────────┐ │
│ │ API Key:    [__________]  │ │
│ │ Base URL:   [__________]  │ │
│ │ Model:      [Dropdown ▼]  │ │
│ │             [Load Models] │ │
│ └───────────────────────────┘ │
│                                │
│ ─────────────────────────────  │  ← separator
│                                │
│ Request Timeout: [60] seconds  │
│ Parallel AI:     [1 ▼]        │
└───────────────────────────────┘
                                    ← 24px spacing
┌─ Prompts ─────────────────────┐
│ Ask Prompts:                   │
│ [Text Area]                    │
│                                │
│ Random Questions:              │
│ [Text Area]                    │
└───────────────────────────────┘
```

#### 2. **对话弹窗优化**

**问题：**
- 响应区域和按钮间距不够
- AI切换器位置不够明显
- 按钮排列不够整齐

**优化建议：**
```
┌─ Ask AI Plugin ───────────────────────┐
│ [AI Selector ▼]              [× Close]│  ← 8px padding
│ ──────────────────────────────────────│  ← separator
│                                        │
│ Question: [________________] [Send]   │  ← 16px spacing
│                                        │
│ ┌─ Response ─────────────────────────┐│
│ │                                     ││
│ │  Response content here...           ││
│ │                                     ││
│ └─────────────────────────────────────┘│
│                                        │
│ [Copy] [Export] [Random Question]     │  ← 16px padding
└────────────────────────────────────────┘
```

### 五、实施步骤

#### 阶段1：建立设计系统（已完成）
- ✅ 创建 `ui_constants.py`
- ✅ 定义间距、尺寸、颜色规范

#### 阶段2：重构General标签页
1. 使用 `ui_constants` 中的间距常量
2. 统一GroupBox样式
3. 优化表单布局对齐
4. 添加合适的分隔线

#### 阶段3：优化对话弹窗
1. 调整整体布局间距
2. 优化按钮排列
3. 改进响应区域样式

#### 阶段4：统一其他界面
1. 快捷键页面
2. 关于页面
3. 模型配置页面

### 六、代码示例

#### 优化前：
```python
layout = QVBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)
```

#### 优化后：
```python
from .ui_constants import SPACING_MEDIUM, MARGIN_MEDIUM

layout = QVBoxLayout()
layout.setSpacing(SPACING_MEDIUM)
layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, 
                         MARGIN_MEDIUM, MARGIN_MEDIUM)
layout.addWidget(widget1)
layout.addWidget(widget2)
```

### 七、视觉设计原则

1. **对齐**：所有元素左对齐或右对齐，避免参差不齐
2. **间距**：使用8px倍数的间距系统
3. **分组**：相关元素用GroupBox或分隔线分组
4. **层次**：重要信息用粗体或更大字号
5. **一致性**：相同功能的元素使用相同样式

### 八、检查清单

在实施优化时，检查以下项目：

- [ ] 所有间距都是8的倍数
- [ ] GroupBox使用统一样式
- [ ] 表单标签右对齐
- [ ] 按钮使用统一的内边距
- [ ] 分隔线样式一致
- [ ] 输入框宽度合理
- [ ] 下拉框宽度足够
- [ ] 视觉层次清晰

## 参考资料

- Material Design Spacing: https://material.io/design/layout/spacing-methods.html
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Qt Layout Management: https://doc.qt.io/qt-5/layout.html
