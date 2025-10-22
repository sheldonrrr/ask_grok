# 自定义模型输入框 UI 改造计划

## 改造日期
2025-10-22

## 问题描述

### 当前实现
在配置页面中，当勾选 "Use custom model name" 复选框后：
- ✅ 模型下拉框会被禁用（`setEnabled(False)`）
- ❌ 自定义输入框会显示出来（`setVisible(True)`）

### 存在的问题
1. **界面不稳定**：输入框的显示/隐藏会导致界面元素跳动
2. **用户体验差**：用户看不到输入框的存在，不知道勾选后会发生什么
3. **极限情况支持不足**：
   - 模型列表加载失败时，用户可能不知道可以使用自定义输入
   - 私有模型场景下，用户需要先勾选才能看到输入框

## 改造方案

### 核心思想
**输入框始终可见，通过 `setEnabled()` 控制是否可编辑**

### UI 布局变化

#### 改造前
```
┌─────────────────────────────────────┐
│ Model: [下拉框 ▼] [Load Models]    │
│        □ Use custom model name      │
│        [自定义输入框] ← 初始隐藏    │  ← 勾选后才显示
└─────────────────────────────────────┘
```

#### 改造后
```
┌─────────────────────────────────────┐
│ Model: [下拉框 ▼] [Load Models]    │
│        □ Use custom model name      │
│        [自定义输入框] ← 始终显示    │  ← 未勾选时禁用（灰色）
└─────────────────────────────────────┘
```

### 交互逻辑

#### 未勾选状态（默认）
- 模型下拉框：**启用**（可选择）
- 自定义输入框：**禁用**（灰色，不可编辑）
- 保存配置时：使用下拉框选中的模型

#### 勾选状态
- 模型下拉框：**禁用**（灰色，不可选择）
- 自定义输入框：**启用**（可编辑）
- 保存配置时：使用自定义输入框的内容

### 优势

1. **界面稳定**
   - ✅ 输入框始终占据固定位置
   - ✅ 无显示/隐藏导致的界面跳动
   - ✅ 布局更加整洁统一

2. **用户体验提升**
   - ✅ 用户可以看到输入框的存在
   - ✅ 禁用状态（灰色）提示用户需要勾选才能使用
   - ✅ 视觉上更加清晰直观

3. **极限情况友好**
   - ✅ 模型列表加载失败时，用户能看到输入框作为备选方案
   - ✅ 私有模型场景下，用户知道如何输入自定义名称
   - ✅ 降低用户的认知负担

## 代码修改

### 文件：`config.py`

#### 1. 修改输入框初始化（第 275-284 行）

**修改前：**
```python
# 自定义模型名称输入框（初始隐藏）
self.custom_model_input = QLineEdit(self)
self.custom_model_input.setMinimumWidth(base_width)
self.custom_model_input.setMinimumHeight(25)
self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))
self.custom_model_input.textChanged.connect(self.on_config_changed)
self.custom_model_input.setVisible(False)  # ← 初始隐藏
self.custom_model_row = model_layout.rowCount()
model_layout.addRow("", self.custom_model_input)
```

**修改后：**
```python
# 自定义模型名称输入框（始终显示，初始禁用）
self.custom_model_input = QLineEdit(self)
self.custom_model_input.setMinimumWidth(base_width)
self.custom_model_input.setMinimumHeight(25)
self.custom_model_input.setPlaceholderText(self.i18n.get('custom_model_placeholder', 'Enter custom model name'))
self.custom_model_input.textChanged.connect(self.on_config_changed)
self.custom_model_input.setEnabled(False)  # ← 初始禁用（灰色）
self.custom_model_row = model_layout.rowCount()
model_layout.addRow("", self.custom_model_input)
```

**变更说明：**
- 删除：`self.custom_model_input.setVisible(False)`
- 新增：`self.custom_model_input.setEnabled(False)`
- 注释更新：从"初始隐藏"改为"始终显示，初始禁用"

#### 2. 修改切换逻辑（第 464-496 行）

**修改前：**
```python
def on_custom_model_toggled(self, state):
    """切换自定义模型名称"""
    use_custom = (state == Qt.Checked)
    
    logger.debug(f"切换自定义模型名称: use_custom={use_custom}")
    
    # 切换控件可见性
    self.model_combo.setEnabled(not use_custom)
    self.custom_model_input.setVisible(use_custom)  # ← 控制显示/隐藏
    
    # 如果切换到自定义，复制当前选中的模型名称
    if use_custom:
        if self.model_combo.currentText():
            self.custom_model_input.setText(self.model_combo.currentText())
        # 设置焦点到输入框
        self.custom_model_input.setFocus()
    
    # 强制更新父控件和布局
    parent = self.custom_model_input.parent()
    if parent:
        parent.updateGeometry()
    
    # 更新整个窗口的布局
    if hasattr(self, 'layout') and self.layout():
        self.layout().update()
        self.layout().activate()
    
    # 强制重绘
    self.custom_model_input.update()
    self.update()
    
    # 触发配置变更
    self.on_config_changed()
```

**修改后：**
```python
def on_custom_model_toggled(self, state):
    """切换自定义模型名称"""
    use_custom = (state == Qt.Checked)
    
    logger.debug(f"切换自定义模型名称: use_custom={use_custom}")
    
    # 切换控件启用/禁用状态
    self.model_combo.setEnabled(not use_custom)
    self.custom_model_input.setEnabled(use_custom)  # ← 控制启用/禁用
    
    # 如果切换到自定义，复制当前选中的模型名称
    if use_custom:
        if self.model_combo.currentText():
            self.custom_model_input.setText(self.model_combo.currentText())
        # 设置焦点到输入框
        self.custom_model_input.setFocus()
    
    # 触发配置变更
    self.on_config_changed()
```

**变更说明：**
- 修改：`setVisible(use_custom)` → `setEnabled(use_custom)`
- 删除：不再需要强制更新布局的代码（因为输入框始终可见，不会引起布局变化）
  - 删除 `parent.updateGeometry()`
  - 删除 `self.layout().update()` 和 `self.layout().activate()`
  - 删除 `self.custom_model_input.update()` 和 `self.update()`

#### 3. 配置加载逻辑（第 498-522 行）

**无需修改**，因为：
- `setChecked()` 会触发 `on_custom_model_toggled()`
- `on_custom_model_toggled()` 会自动处理 `setEnabled()` 状态

但需要确保在 `load_model_config()` 中正确设置复选框状态。

## 测试计划

### 1. 基本功能测试
- [ ] 页面初始加载时，自定义输入框显示且为禁用状态（灰色）
- [ ] 勾选 "Use custom model name" 后，输入框变为启用状态（可编辑）
- [ ] 取消勾选后，输入框恢复禁用状态（灰色）
- [ ] 勾选时，下拉框正确禁用
- [ ] 取消勾选时，下拉框正确启用

### 2. 数据同步测试
- [ ] 勾选时，下拉框的当前值正确复制到输入框
- [ ] 保存配置时，使用正确的模型名称（下拉框或输入框）
- [ ] `use_custom_model_name` 字段正确保存

### 3. 配置加载测试
- [ ] 加载使用下拉框的配置：输入框禁用，下拉框选中正确项
- [ ] 加载使用自定义的配置：输入框启用，显示正确内容
- [ ] 旧配置兼容性：无 `use_custom_model_name` 字段时正确处理

### 4. 界面稳定性测试
- [ ] 切换复选框时，界面无跳动
- [ ] 输入框位置固定，不会因为状态变化而移动
- [ ] 布局整洁，视觉上协调

### 5. 极限情况测试
- [ ] 模型列表为空时，输入框可见且可通过勾选使用
- [ ] 模型列表加载失败时，输入框作为备选方案可用
- [ ] 输入框禁用时，用户无法编辑（符合预期）

### 6. 多语言测试
- [ ] 输入框的 placeholder 文本正确显示各语言版本
- [ ] 复选框文本正确显示各语言版本

## 实施步骤

1. **备份当前代码**
   ```bash
   git add config.py
   git commit -m "backup: before custom model input refactor"
   ```

2. **修改代码**
   - 修改输入框初始化（第 275-284 行）
   - 修改切换逻辑（第 464-496 行）

3. **测试验证**
   - 运行测试计划中的所有测试项
   - 确保所有功能正常工作

4. **提交代码**
   ```bash
   git add config.py
   git commit -m "refactor: custom model input always visible, controlled by setEnabled"
   ```

## 预期效果

### 用户视角
- 界面更加稳定，无跳动感
- 输入框始终可见，降低认知负担
- 禁用状态（灰色）提供清晰的视觉反馈

### 开发者视角
- 代码更简洁（删除了布局强制更新代码）
- 逻辑更清晰（启用/禁用 vs 显示/隐藏）
- 维护更容易（减少了布局相关的边界情况）

## 风险评估

### 低风险
- 修改范围小，仅涉及两处代码
- 逻辑简单，从 `setVisible()` 改为 `setEnabled()`
- 不影响数据保存和加载逻辑

### 潜在问题
- Qt 的 `setEnabled(False)` 可能在不同主题下显示效果不同
  - **解决方案**：在多个主题下测试，确保禁用状态清晰可见

## 总结

这次改造通过将自定义输入框从"显示/隐藏"改为"启用/禁用"，实现了：

1. ✅ **界面稳定性提升**：无跳动，布局固定
2. ✅ **用户体验改善**：输入框始终可见，降低认知负担
3. ✅ **代码简化**：删除了强制更新布局的代码
4. ✅ **极限情况友好**：模型列表加载失败时，用户能看到备选方案

**这是一个小而美的改进，符合"最小化修改，最大化效果"的原则。**
