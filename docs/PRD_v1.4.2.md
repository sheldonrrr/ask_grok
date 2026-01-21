# Chat with Library - 图书馆对话功能

## Overview / 概述

When user didn't select any books, the plugin will use current library's books metadata into query data, use this method to support user could chat with library.

当用户未选择任何书籍时，插件将使用当前图书馆的书籍元数据作为查询数据，通过此方法支持用户与图书馆进行对话。

**核心价值**：让拥有 50-100 本书的用户通过自然语义对话实现书籍搜索、打开和跳转，无需记忆精确书名。

## Core Requirements / 核心需求

### 1. Natural Semantic Search / 自然语义搜索
- 用户可以用自然语言描述需求，如"找一本关于机器学习的书"、"上周添加的科幻小说"
- AI 理解语义并返回匹配的书籍列表
- 支持模糊匹配、主题搜索、作者搜索等多维度查询

### 2. Book Navigation / 书籍导航
- AI 返回结果中包含可点击的书籍链接
- 点击后直接在 Calibre 中打开对应书籍
- 支持批量操作（如"打开所有推荐的书"）

### 3. Context Awareness / 上下文感知
- AI 了解用户的图书馆内容
- 可以进行对比、推荐、分类等智能操作
- 支持多轮对话，记住上下文

## Implementation Strategy / 实现策略

### Phase 1: Minimal Viable Product (最小可行产品)

#### 1.1 Metadata Extraction / 元数据提取

**最小成本方案**：
- 仅提取核心字段：`title`, `authors`, `tags`, `series`, `publisher`, `pubdate`, `comments`
- 每本书压缩为单行 JSON，格式：
  ```json
  {"id":123,"title":"Book Title","authors":"Author Name","tags":"tag1,tag2","series":"Series Name"}
  ```
- 预估：每本书约 150-200 字符，100 本书约 15-20KB

**Token 优化**：
- 对于 50 本书：~10KB ≈ 2,500 tokens
- 对于 100 本书：~20KB ≈ 5,000 tokens
- 主流模型（如 GPT-4, Claude, Gemini）上下文窗口 128K+，完全可容纳

#### 1.2 UI Configuration / 界面配置

**新增 "Library" Tab**：
```
┌─ Library Settings ─────────────────────────┐
│ ☑ Enable Library Chat                      │
│                                             │
│ Metadata Fields to Include:                │
│ ☑ Title        ☑ Authors      ☑ Tags       │
│ ☑ Series       ☑ Publisher    ☐ ISBN       │
│ ☑ Comments     ☐ Custom Field 1            │
│                                             │
│ Book Filter:                                │
│ ○ All books in library                     │
│ ○ Books with specific tags: [_________]    │
│ ○ Custom book list (Advanced)              │
│                                             │
│ [Update Library Data] [Preview Data]       │
│                                             │
│ Status: 87 books, ~4,200 tokens            │
└─────────────────────────────────────────────┘
```

**实现细节**：
- 复用现有 `config.py` 的 Tab 架构
- 添加配置项：
  ```python
  prefs.defaults['library_chat_enabled'] = False
  prefs.defaults['library_metadata_fields'] = ['title', 'authors', 'tags', 'series']
  prefs.defaults['library_book_filter'] = 'all'  # 'all', 'tags', 'custom'
  prefs.defaults['library_cached_metadata'] = ''  # JSON string
  prefs.defaults['library_last_update'] = None
  prefs.defaults['quick_search_shortcut'] = 'Ctrl+Shift+L'  # 快捷搜索快捷键
  ```

#### 1.2.5 Quick Search Entry (Raycast-style) / 快捷搜索入口

**产品形态**：类似 Raycast 的快速搜索界面

**交互流程**：
```
用户按快捷键 (Ctrl+Shift+L)
    ↓
弹出轻量级搜索框（居中悬浮）
    ↓
用户输入查询 "python 编程"
    ↓
实时显示列表式结果
    ↓
用户选择操作：
  - Enter: 打开选中的书籍
  - Ctrl+Enter: 进入完整对话模式
  - Esc: 关闭搜索框
```

**UI 设计**：
```
┌─────────────────────────────────────────────┐
│  🔍 Search your library...                  │
│─────────────────────────────────────────────│
│  📚 Python Crash Course                     │
│     Eric Matthes · Programming · 2019       │
│     ⏎ Open  |  ⌘⏎ Chat                     │
│─────────────────────────────────────────────│
│  📚 Fluent Python                           │
│     Luciano Ramalho · Advanced · 2022       │
│     ⏎ Open  |  ⌘⏎ Chat                     │
│─────────────────────────────────────────────│
│  📚 Effective Python                        │
│     Brett Slatkin · Best Practices · 2019   │
│     ⏎ Open  |  ⌘⏎ Chat                     │
│─────────────────────────────────────────────│
│  💬 Ask AI about these results...           │
│     ⌘⏎ Start conversation                   │
└─────────────────────────────────────────────┘
```

**实现要点**：

1. **轻量级窗口**：
   - 使用 `QDialog` 创建无边框、半透明背景的悬浮窗
   - 尺寸：600x400px，屏幕居中
   - 支持 Esc 快速关闭

2. **实时搜索**：
   - 用户输入时，通过 AI 实时匹配书籍（debounce 300ms）
   - 显示前 5-10 个最相关结果
   - 使用简化的 prompt（仅返回书籍列表，无需详细解释）

3. **键盘导航**：
   - ↑/↓ 键选择结果
   - Enter 打开书籍
   - Ctrl+Enter 进入完整对话（带上当前查询和结果）
   - Esc 关闭窗口

4. **双模式切换**：
   - **快速模式**（默认）：列表式结果，快速打开书籍
   - **对话模式**：点击底部"Ask AI"或按 Ctrl+Enter，切换到完整对话界面

**代码实现**（伪代码）：
```python
class QuickSearchDialog(QDialog):
    def __init__(self, parent, api):
        super().__init__(parent)
        self.api = api
        self.setup_ui()
        
    def setup_ui(self):
        # 无边框、半透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search your library...")
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # 结果列表
        self.results_list = QListWidget()
        self.results_list.itemActivated.connect(self.on_item_activated)
        
        # 底部操作栏
        self.chat_button = QPushButton("💬 Ask AI about these results...")
        self.chat_button.clicked.connect(self.open_full_chat)
        
    def on_search_changed(self, text):
        # Debounce 300ms
        QTimer.singleShot(300, lambda: self.perform_search(text))
        
    def perform_search(self, query):
        # 调用 AI 搜索（简化 prompt）
        prompt = f"""
        User's library: {cached_metadata}
        Query: {query}
        
        Return top 5 matching books in JSON format:
        [{{"id": 123, "title": "...", "authors": "...", "relevance": "..."}}]
        """
        
        results = self.api.search_library(prompt)
        self.display_results(results)
        
    def on_item_activated(self, item):
        # Enter 键：打开书籍
        book_id = item.data(Qt.UserRole)
        self.gui.iactions['View'].view_book(book_id)
        self.close()
        
    def open_full_chat(self):
        # Ctrl+Enter：进入完整对话
        query = self.search_input.text()
        results = self.get_current_results()
        
        # 关闭快捷搜索，打开完整对话
        self.close()
        
        # 打开 AskDialog，预填充查询和结果
        d = AskDialog(self.gui, None, self.api)
        d.prefill_query(query, results)
        d.exec_()
```

**快捷键注册**（在 `ui.py` 中）：
```python
# 注册快捷搜索快捷键
self.quick_search_action = self.create_menu_action(
    self.menu,
    unique_name='quick_search',
    text='Quick Search Library',
    shortcut='Ctrl+Shift+L',
    description='Open quick search dialog',
    triggered=self.show_quick_search,
    shortcut_name='Ask AI: Quick Search',
    persist_shortcut=True,
)

def show_quick_search(self):
    """显示快捷搜索对话框"""
    if not self.api:
        self.initialize_api()
    
    d = QuickSearchDialog(self.gui, self.api)
    d.exec_()
```

**优势**：
- ⚡ **快速**：无需选择书籍，直接搜索整个图书馆
- 🎯 **精准**：AI 语义理解，比传统搜索更智能
- 🔄 **灵活**：既能快速打开书，也能深入对话
- ⌨️ **高效**：全键盘操作，符合 Power User 习惯

#### 1.3 Data Update Mechanism / 数据更新机制

**按需更新**：
- 用户点击 "Update Library Data" 按钮时更新
- 首次使用时自动提示更新
- 显示更新时间和书籍数量

**代码实现**（伪代码）：
```python
def update_library_metadata():
    db = self.gui.current_db
    book_ids = db.all_book_ids()
    
    metadata_list = []
    for book_id in book_ids:
        mi = db.get_metadata(book_id)
        metadata_list.append({
            'id': book_id,
            'title': mi.title,
            'authors': ', '.join(mi.authors or []),
            'tags': ', '.join(mi.tags or []),
            'series': mi.series or '',
        })
    
    # 压缩为 JSON
    import json
    cached_data = json.dumps(metadata_list, ensure_ascii=False)
    prefs['library_cached_metadata'] = cached_data
    prefs['library_last_update'] = datetime.now().isoformat()
```

#### 1.4 Query Integration / 查询集成

**修改 `api.py` 的提示词构建**：
```python
def build_library_context():
    if not prefs.get('library_chat_enabled'):
        return ''
    
    cached_metadata = prefs.get('library_cached_metadata', '')
    if not cached_metadata:
        return ''
    
    return f"""
You have access to the user's Calibre library metadata:
{cached_metadata}

When user asks about books, search within this library and provide:
1. Matching book titles with IDs
2. Brief explanation why they match
3. Format response as: "Found: [Book Title] (ID: 123)"

User can click book IDs to open them in Calibre.
"""
```

#### 1.5 Book Link Handling / 书籍链接处理

**在响应中识别书籍 ID**：
- AI 返回格式：`(ID: 123)` 或 `[Book ID: 123]`
- 前端解析并转换为可点击链接
- 点击后调用 `self.gui.iactions['View'].view_book(book_id)`

**实现**（在 `response_panel.py` 中）：
```python
import re

def make_book_links_clickable(html_content):
    # 匹配 (ID: 123) 格式
    pattern = r'\(ID:\s*(\d+)\)'
    
    def replace_with_link(match):
        book_id = match.group(1)
        return f'<a href="calibre://book/{book_id}" style="color: #0066cc; text-decoration: underline;">Open Book {book_id}</a>'
    
    return re.sub(pattern, replace_with_link, html_content)
```

### Phase 2: Enhanced Features (增强功能 - 可选)

#### 2.1 Smart Book List Management / 智能书单管理
- 允许用户手动排除某些书籍
- 支持按标签、系列、评分过滤
- 提供"最近添加"、"未读"等快捷过滤

#### 2.2 Token Usage Monitoring / Token 使用监控
- 实时显示当前元数据占用的 token 数
- 警告超过模型限制（如 >100K tokens）
- 建议用户启用过滤器

#### 2.3 Incremental Updates / 增量更新
- 检测图书馆变化（新增/删除书籍）
- 仅更新变化部分，减少处理时间

## User Flow / 用户流程

### First-Time Setup / 首次设置
1. 用户打开插件配置 → Library Tab
2. 勾选 "Enable Library Chat"
3. 点击 "Update Library Data"
4. 系统提取元数据并显示：`✓ 87 books loaded, ~4,200 tokens`
5. 用户保存配置

### Daily Usage / 日常使用
1. 用户打开 Ask AI 对话框（未选择任何书籍）
2. 输入自然语言查询：`"找一本关于 Python 编程的书"`
3. AI 响应：
   ```
   Found 3 books about Python programming:
   
   1. **Python Crash Course** (ID: 45) - Beginner-friendly introduction
   2. **Fluent Python** (ID: 78) - Advanced Python techniques  
   3. **Effective Python** (ID: 92) - Best practices guide
   
   Click any book ID to open it in Calibre.
   ```
4. 用户点击 `(ID: 78)` → Calibre 打开《Fluent Python》

## Technical Considerations / 技术考量

### Token Limits / Token 限制
| Library Size | Estimated Tokens | Compatible Models |
|--------------|------------------|-------------------|
| 50 books     | ~2,500           | All modern LLMs   |
| 100 books    | ~5,000           | All modern LLMs   |
| 500 books    | ~25,000          | GPT-4, Claude 3+  |
| 1000+ books  | ~50,000+         | Requires filtering|

### Performance / 性能
- 元数据提取：~0.1s per book → 100 books in ~10s
- JSON 序列化：<1s for 100 books
- 首次加载后缓存，后续查询无需重新提取

### Data Privacy / 数据隐私
- 元数据仅在用户主动查询时发送给 AI
- 不包含书籍内容，仅元数据
- 用户可随时禁用此功能

## Success Metrics / 成功指标

1. **功能性**：用户能通过自然语言找到并打开书籍
2. **性能**：100 本书的元数据更新 <15 秒
3. **准确性**：AI 搜索结果准确率 >80%
4. **易用性**：零配置即可使用（默认包含所有书籍）

## Future Enhancements / 未来增强

- **向量搜索**：使用 embeddings 进行语义相似度搜索
- **个性化推荐**：基于阅读历史推荐书籍
- **批量操作**：支持"将所有科幻小说添加到设备"等批量命令
- **多语言优化**：针对中文书籍优化元数据提取

