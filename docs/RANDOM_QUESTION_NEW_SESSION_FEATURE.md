# 随机问题新会话功能实现文档

## 功能概述

优化随机问题按钮的行为，使其更符合用户预期：
1. 当前有问答历史时，点击随机问题自动创建新会话
2. 随机问题获取成功后暂存，不立即保存历史记录
3. 只有用户点击发送并获得AI回答后，才保存新的历史记录

## 实现细节

### 1. 新增方法和变量

#### AskDialog 类新增：

**临时状态变量**（ui.py 第 831-833 行）：
```python
# 临时缓存：用于暂存随机问题（在用户点击发送前不保存历史）
self._pending_random_question = None
self._is_generating_random_question = False
```

**检查历史数据方法**（ui.py 第 2015-2042 行）：
```python
def _has_history_data(self):
    """检查当前UID是否有历史记录（有AI回答）
    
    Returns:
        bool: 如果有历史记录且包含AI回答返回True，否则返回False
    """
```

### 2. 修改的核心逻辑

#### generate_suggestion() 方法（ui.py 第 2044-2070 行）

**新增逻辑**：
1. 检查是否有历史数据
2. 如果有，调用 `_on_new_conversation()` 创建新会话
3. 设置 `_is_generating_random_question = True` 标记

```python
# 检查是否有历史数据
if self._has_history_data():
    logger.info("检测到当前有历史记录，点击随机问题将创建新会话")
    # 创建新会话
    self._on_new_conversation()

# 标记这是一个随机问题请求
self._is_generating_random_question = True
```

#### _on_suggestion_received() 方法（random_question.py 第 280-284 行）

**新增逻辑**：
将随机问题暂存到父对话框的临时变量中

```python
# 将随机问题暂存到父对话框的临时变量中
parent_dialog = self.suggest_button.window() if self.suggest_button else None
if parent_dialog and hasattr(parent_dialog, '_pending_random_question'):
    parent_dialog._pending_random_question = suggestion
    logger.info(f"随机问题已暂存到临时变量，等待用户点击发送: {suggestion[:50]}...")
```

#### send_question() 方法（ui.py 第 2122-2136 行）

**修改逻辑**：
1. 检查是否是随机问题请求
2. 如果是，跳过重复的新UID生成（因为已在 generate_suggestion 中创建）
3. 重置标记

```python
# 检查是否是随机问题请求
is_random_question = hasattr(self, '_is_generating_random_question') and self._is_generating_random_question

# 如果是随机问题，已经在generate_suggestion中创建了新会话，这里不需要再创建
# 如果不是随机问题，检查当前UID是否已有历史记录
if not is_random_question:
    if hasattr(self, 'response_handler') and hasattr(self.response_handler, 'history_manager'):
        if self.current_uid in self.response_handler.history_manager.histories:
            old_uid = self.current_uid
            self.current_uid = self._generate_uid()
            logger.info(f"检测到已有历史记录，生成新UID: {old_uid} -> {self.current_uid}")
else:
    logger.info("随机问题请求，使用已创建的新会话UID")
    # 重置标记
    self._is_generating_random_question = False
```

#### _update_button_focus() 方法（ui.py 第 1995-2004 行）

**新增逻辑**：
用户修改输入框内容时，清除随机问题相关的临时状态

```python
# 如果用户修改了输入框内容，清除随机问题相关的临时状态
if hasattr(self, '_pending_random_question'):
    current_text = self.input_area.toPlainText()
    if current_text != self._pending_random_question:
        # 用户修改了随机问题，清除临时缓存和标记
        if self._pending_random_question is not None:
            logger.debug("用户修改了输入框内容，清除随机问题临时状态")
            self._pending_random_question = None
            if hasattr(self, '_is_generating_random_question'):
                self._is_generating_random_question = False
```

## 用户场景流程

### 场景1：有历史记录时点击随机问题

1. 用户打开有历史记录的书籍对话框
2. 点击"随机问题"按钮
3. **系统自动创建新会话**（生成新UID，清空输入和响应区域）
4. 获取随机问题并显示在输入框
5. **随机问题暂存到 `_pending_random_question`，不保存历史**
6. 用户点击"发送"
7. 获得AI回答后，**保存新的历史记录**（包含问题和回答）

### 场景2：获取随机问题后不发送

1. 用户点击"随机问题"按钮
2. 获取随机问题并显示在输入框
3. 用户**没有点击发送**，而是关闭对话框或切换到其他书籍
4. **不保存历史记录**（因为没有AI回答）
5. 下次打开同一本书，不会看到这个随机问题

### 场景3：修改随机问题后发送

1. 用户点击"随机问题"按钮
2. 获取随机问题并显示在输入框
3. 用户**修改了问题内容**
4. **系统自动清除 `_pending_random_question` 和 `_is_generating_random_question` 标记**
5. 用户点击"发送"
6. 按照普通问题处理（如果有历史记录，会创建新会话）

## 历史记录数据结构

历史记录中：
- **AI回答（answers）是必填项**：只有有回答的记录才会被保存
- **用户问题（question）可以为空**：允许没有问题的场景
- **随机问题不会单独保存**：只有在用户发送并获得回答后才保存

```json
{
  "uid": "20251105193000_abc123def456",
  "timestamp": "2025-11-05 19:30:00",
  "mode": "single",
  "books": [...],
  "question": "Tell me about this book",
  "answers": {
    "gemini": {
      "answer": "This is the AI response...",
      "timestamp": "2025-11-05 19:30:15"
    }
  }
}
```

## 修改的文件

1. **ui.py**
   - 新增 `_has_history_data()` 方法
   - 修改 `generate_suggestion()` 方法
   - 修改 `send_question()` 方法
   - 修改 `_update_button_focus()` 方法
   - 修改 `_load_history()` 方法 - 添加待发送随机问题恢复逻辑
   - 修改 `closeEvent()` 方法 - 保存待发送随机问题到临时存储
   - 新增临时状态变量
   - 添加 `datetime` 导入

2. **random_question.py**
   - 修改 `_on_suggestion_received()` 方法

## 临时存储机制

### 数据结构

待发送的随机问题保存在配置文件的 `pending_random_questions` 字段中：

```python
{
  "pending_random_questions": {
    "(2,)": {  # 书籍ID元组的字符串表示
      "question": "随机问题内容...",
      "uid": "20251105194500_abc123def456",
      "timestamp": "2025-11-05 19:45:00"
    }
  }
}
```

### 工作流程

1. **保存时机**（`closeEvent`）：
   - 用户点击随机问题获取问题后
   - 没有点击发送就关闭对话框
   - 系统将问题、UID和时间戳保存到配置

2. **恢复时机**（`_load_history`）：
   - 重新打开同一本书的对话框
   - 优先检查是否有待发送的随机问题
   - 如果有，恢复问题、UID和状态，清空响应区域
   - 如果没有，正常加载历史记录

3. **清除时机**（`send_question`）：
   - 用户点击发送按钮
   - 系统从临时存储中删除该书籍的待发送问题
   - 正常发送请求并保存历史记录

## 测试要点

### 测试用例1：有历史记录时点击随机问题
- [ ] 打开有历史记录的书籍
- [ ] 点击随机问题按钮
- [ ] 验证：输入框和响应区域被清空
- [ ] 验证：生成新的UID（检查日志）
- [ ] 验证：随机问题显示在输入框
- [ ] 验证：不立即保存历史记录
- [ ] 点击发送并获得回答
- [ ] 验证：新历史记录被保存

### 测试用例2：获取随机问题后不发送，再次打开恢复
- [ ] 点击随机问题按钮
- [ ] 获取随机问题
- [ ] 不点击发送，直接关闭对话框
- [ ] 重新打开同一本书
- [ ] **验证：显示刚才的随机问题（从临时存储恢复）**
- [ ] **验证：响应区域为空（没有AI回答）**
- [ ] **验证：UID与之前相同（检查日志）**

### 测试用例3：修改随机问题后发送
- [ ] 点击随机问题按钮
- [ ] 获取随机问题
- [ ] 修改问题内容
- [ ] 验证：临时状态被清除（检查日志）
- [ ] 点击发送
- [ ] 验证：按照普通问题处理

### 测试用例4：无历史记录时点击随机问题
- [ ] 打开新书籍（无历史记录）
- [ ] 点击随机问题按钮
- [ ] 验证：不创建新会话
- [ ] 验证：随机问题显示在输入框
- [ ] 点击发送并获得回答
- [ ] 验证：历史记录被保存

### 测试用例5：恢复随机问题后发送
- [ ] 点击随机问题按钮
- [ ] 获取随机问题
- [ ] 不点击发送，关闭对话框
- [ ] 重新打开同一本书
- [ ] 验证：随机问题被恢复
- [ ] 点击发送并获得回答
- [ ] 验证：历史记录被保存
- [ ] 验证：临时存储被清除（检查日志）
- [ ] 再次打开同一本书
- [ ] 验证：显示刚才保存的历史记录

## 日志关键字

在测试时可以搜索以下日志关键字：

- `检测到当前有历史记录，点击随机问题将创建新会话`
- `随机问题已暂存到临时变量，等待用户点击发送`
- `保存待发送的随机问题到临时存储`
- `发现待发送的随机问题`
- `已恢复待发送的随机问题状态，等待用户点击发送`
- `已清除临时存储中的待发送随机问题`
- `随机问题请求，使用已创建的新会话UID`
- `用户修改了输入框内容，清除随机问题临时状态`
- `检测到已有历史记录，生成新UID`

## 开发时间

- 第一阶段（基础功能）：
  - 分析需求：10分钟
  - 实现代码：30分钟
  - 文档编写：15分钟
- 第二阶段（临时存储机制）：
  - 分析问题：5分钟
  - 实现临时存储：25分钟
  - 更新文档：10分钟
- **总计：约95分钟**

## 状态

✅ 开发完成，待测试

## 更新日志

### v1 - 基础功能（2025-11-05 19:48）
- 有历史时点击随机问题创建新会话
- 随机问题暂存到内存变量
- 只有发送后才保存历史

### v2 - 临时存储机制（2025-11-05 19:52）
- 添加配置文件临时存储
- 关闭对话框时保存待发送的随机问题
- 重新打开时恢复待发送的随机问题
- 发送后清除临时存储
- **解决了用户反馈的问题：关闭后重新打开，现在会显示待发送的随机问题而不是旧的历史记录**
