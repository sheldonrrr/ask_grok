# Chat with Library - MVP 最小可行产品

## 核心目标

用户未选择书籍时点击Ask，插件自动提取书库中所有书籍的书名和作者名，通过AI搜索返回匹配的书籍列表。

**一句话描述**：让用户用自然语言问"有没有关于Python的书"，AI返回书名列表。

---

## MVP 功能范围

### ✅ 保留功能

1. **元数据提取**：仅提取书名(title)和作者名(authors)
2. **AI搜索**：用户输入查询，AI返回书名列表
3. **结果显示**：在对话框中显示AI返回的书籍列表
4. **打开书籍**：点击书籍可以打开

### ❌ 删除功能

- ~~双模式搜索（本地搜索 + AI搜索）~~ → 只要AI搜索
- ~~快捷搜索弹窗（Raycast风格）~~ → 复用现有Ask对话框
- ~~可配置字段选择~~ → 固定只提取书名和作者
- ~~Book Filter过滤器~~ → 固定提取所有书籍
- ~~Max Book Numbers限制~~ → 固定100本
- ~~Preview Data预览~~ → 不需要预览
- ~~AI Search Prompt编辑~~ → 使用固定提示词
- ~~复杂的结果过滤和模糊匹配~~ → AI直接返回书籍ID
- ~~快捷键注册~~ → 复用现有菜单

---

## 实现方案

### 1. 配置界面（极简）

在现有配置中添加一个简单的开关：

```
┌─ Library Settings ─────────────┐
│ ☑ Enable Library Chat          │
│                                 │
│ [Update Library Data]           │
│                                 │
│ Status: 87 books, last update:  │
│ 2026-01-01 12:00:00             │
└─────────────────────────────────┘
```

**配置项**：
```python
prefs.defaults['library_chat_enabled'] = False
prefs.defaults['library_cached_metadata'] = ''  # JSON字符串
prefs.defaults['library_last_update'] = None
```

### 2. 元数据提取（最简单）

点击"Update Library Data"按钮时：

```python
def update_library_metadata():
    db = self.gui.current_db
    book_ids = db.all_book_ids()[:100]  # 固定最多100本
    
    books = []
    for book_id in book_ids:
        mi = db.get_metadata(book_id)
        books.append({
            'id': book_id,
            'title': mi.title,
            'authors': ', '.join(mi.authors or [])
        })
    
    # 保存为JSON
    import json
    prefs['library_cached_metadata'] = json.dumps(books, ensure_ascii=False)
    prefs['library_last_update'] = datetime.now().isoformat()
```

### 3. AI搜索（固定提示词）

用户在Ask对话框输入查询时，如果未选择书籍且启用了Library Chat：

```python
def build_prompt(user_query):
    cached_metadata = prefs.get('library_cached_metadata', '')
    if not cached_metadata:
        return user_query  # 未更新元数据，正常查询
    
    prompt = f"""You have access to the user's book library. Here are all the books:

{cached_metadata}

User query: {user_query}

Please find matching books and return them in this format:
- Book Title 1 (ID: 123)
- Book Title 2 (ID: 456)

Only return books that match the query. Maximum 5 results."""
    
    return prompt
```

### 4. 结果显示（复用现有界面）

AI返回的内容直接显示在现有的Ask对话框中，用户可以：
- 看到书籍列表
- 点击书籍ID链接打开书籍（复用现有的书籍链接处理逻辑）

---

## 用户流程

### 首次设置
1. 打开插件配置 → Library Tab
2. 勾选"Enable Library Chat"
3. 点击"Update Library Data"
4. 完成

### 日常使用
1. 不选择任何书籍，点击Ask按钮
2. 输入："有没有关于Python的书"
3. AI返回：
   ```
   Found 3 books about Python:
   - Python Crash Course (ID: 45)
   - Fluent Python (ID: 78)
   - Effective Python (ID: 92)
   ```
4. 点击书籍ID打开书籍

---

## 技术实现清单

### 需要修改的文件

1. **config.py**
   - 添加Library Tab
   - 添加Enable开关
   - 添加Update按钮
   - 显示Status状态

2. **ui.py**
   - 检测是否选择了书籍
   - 如果未选择且启用Library Chat，调用library搜索模式

3. **api.py**
   - 添加`build_library_prompt()`方法
   - 在发送请求前检查是否需要注入library元数据

4. **utils.py**（新建）
   - `update_library_metadata()` - 提取元数据
   - `get_library_metadata()` - 获取缓存的元数据

### 代码量估算
- config.py: +50行
- ui.py: +20行
- api.py: +30行
- utils.py: +40行
- **总计：约140行代码**

---

## 成功标准

1. ✅ 用户能提取书库元数据（100本书 <5秒）
2. ✅ 用户能用自然语言搜索书籍
3. ✅ AI能返回相关书籍列表
4. ✅ 用户能点击打开书籍

---

## 未来迭代（v1.5+）

等MVP跑通后再考虑：
- 可配置字段
- 本地搜索模式
- 快捷搜索弹窗
- 结果过滤优化
- 更多配置选项

---

## 关键决策

**为什么删除这些功能？**

1. **双模式搜索** → AI搜索已经够用，本地搜索是优化项
2. **快捷搜索弹窗** → 现有对话框已经能用，新UI是锦上添花
3. **可配置字段** → 书名+作者已经足够识别书籍
4. **复杂过滤** → 让AI直接返回正确格式，而不是事后修正
5. **各种限制和配置** → 固定参数，减少选择困难

**第一性原理**：
- 用户想要什么？→ 用自然语言找到书
- 最简单的实现？→ 把书名列表给AI，让AI找
- 最小的改动？→ 复用现有对话框和链接处理

---

## 开发顺序

1. **Day 1**: 实现元数据提取和配置界面（utils.py + config.py）
2. **Day 2**: 实现AI搜索集成（api.py + ui.py）
3. **Day 3**: 测试和修复bug
4. **Day 4**: 发布MVP

**目标：4天内上线可用版本**
