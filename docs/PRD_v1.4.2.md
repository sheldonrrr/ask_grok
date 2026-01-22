# Chat with Library - 图书馆对话功能

## Overview / 概述

When user didn't select any books and continue to click Ask dialog, or user trigger via Search menu, the plugin will use current library's books metadata into query data, use this method to support user could chat with library.

当用户未选择任何书籍时继续点击Ask弹窗时，或者用户通过菜单中的Search触发，插件将使用当前图书馆的书籍元数据作为查询数据，通过此方法支持用户与图书馆进行对话。

**核心价值**：让拥有 50-100 本书的用户通过自然语义对话实现书籍搜索、打开和跳转，无需记忆精确书名。

## Core Requirements / 核心需求

### 1. Natural Semantic Search / 自然语义搜索
- 用户可以用自然语言描述需求，如"找一本关于机器学习的书"、"上周添加的科幻小说"
- AI 理解语义并返回匹配的书籍列表
- 支持模糊匹配、主题搜索、作者搜索等多维度查询

### 2. Book Navigation / 书籍导航
- AI 返回结果中包含可点击的书籍链接
- 界面上以书籍列表作为展示，上下方向键选择后，Enter键会打开对应书籍阅读

### 3. Context Awareness / 上下文感知
- AI通过定期Update的图书馆元数据构成的上下文数据了解用户的图书馆内容
- 支持多轮对话,记住上下文
- 目前仅先支持Nvidia的多轮对话,后续支持其他AI的多轮对话,以节省Context Tokens

## Implementation Strategy / 实现策略

### Phase 1: Minimal Viable Product (最小可行产品)

#### 1.1 Metadata Extraction / 元数据提取

**最小成本方案**：
- 默认仅提取核心字段：`title`, `authors`（用户可选择添加：`tags`, `series`, `publisher`, `pubdate`, `language`）
- 每本书压缩为单行 JSON，格式：
  ```json
  {"id":123,"title":"Book Title","authors":"Author Name"}
  ```
- 所有书籍元数据拼接为一行字符串存储，包含基础版本信息
- 预估：每本书约 80-120 字符，100 本书约 8-12KB

**Token 优化**：
- 对于 50 本书：~5KB ≈ 1,250 tokens
- 对于 100 本书：~10KB ≈ 2,500 tokens
- 主流模型（如 GPT-4, Claude, Gemini）上下文窗口 128K+，完全可容纳
- 默认最大书籍数限制为100本，防止Tokens超出AI限制

#### 1.2 UI Configuration / 界面配置

**新增 "Library" Tab**：
┌─ Library Settings ─────────────────────────┐
│ ☑ Enable Library Chat                      │
│                                             │
│ Metadata Fields to Include:                │
│ ☑ Title        ☑ Author(s)                 │
│ ☐ Series       ☐ Publisher                 │
│ ☐ Published    ☐ Language                  │
│                                             │
│ Book Filter:                                │
│ ☑ All books in library                     │
│                                             │
│ Max Book Numbers:                           │
│ [100]                                       │
│                                             │
│ [Update Library Data] [Preview Data]       │
│                                             │
│ AI Search Prompt:                           │
│ ┌─────────────────────────────────────────┐ │
│ │ Based on the user's library...          │ │
│ │ (Multi-line text editor)                │ │
│ └─────────────────────────────────────────┘ │
│ Available variables: {metadata}, {query}    │
│                                             │
│ Status:                                     │
│ 87 books, ~4,200 tokens,                    │
│ last update:                                │
│ 2026-01-01 12:00:00                         │
└─────────────────────────────────────────────┘

**实现细节**：
- 复用现有 `config.py` 的 Tab 架构
- 添加配置项：
  ```python
  prefs.defaults['library_chat_enabled'] = False
  prefs.defaults['library_metadata_fields'] = ['title', 'authors']  # 默认只选中书名和作者
  prefs.defaults['library_book_filter'] = 'all'  # 默认选择所有书籍
  prefs.defaults['library_max_books'] = 100  # 默认最大100本
  prefs.defaults['library_cached_metadata'] = ''  # 单行JSON字符串，包含版本信息
  prefs.defaults['library_last_update'] = None
  prefs.defaults['quick_search_shortcut'] = 'Ctrl+Shift+L'  # 快捷搜索快捷键
  prefs.defaults['library_ai_search_prompt'] = '''Based on the user's library metadata below, find the most relevant books that match the query.

Library: {metadata}
Query: {query}

Return ONLY the book titles, one per line, without any numbering, explanations, or additional text. Maximum 5 results.'''  # AI搜索默认提示词
  ```

**按钮功能**：
- **Update Library Data**：提取元数据并保存为单行JSON格式到本地，包含版本信息。成功后显示提示并更新Status状态（书籍数量、Token预估、更新时间）
- **Preview Data**：显示纯文本书籍名称列表，按照书库中的书籍顺序从上到下排列，方便用户确认包含哪些书籍

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
默认搜索本地的关键词，如果有命中，则返回书籍结果列表，最大结果5个
    ↓
如果输入`/ `开头，则输入完文字后，直接提交总的Metadata数据和用户的请求文字给AI，AI的输出结果中，给出书籍名称列表
    ↓
拿到AI输出的数据后，本地需要对拿到的结果进行过滤和处理，重新匹配本地的书籍列表，并在搜索框的下方显示书籍名称列表
    ↓
用户选择操作：
  - Enter: 打开选中的书籍
  - Ctrl+Enter: 进入完整对话模式（仍旧是调用原Ask弹窗，只是顶部的Metadata信息是当前书库总的Metadata信息即选择）
  - Esc: 关闭搜索框
```

**UI 设计**：
```
┌─────────────────────────────────────────────┐
│  Search your library...                     │
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

2. **双模式搜索**：
   - **默认模式**：直接搜索本地关键词（书名、作者），如有命中返回最多5个结果
   - **AI模式**：用户输入`/ `开头触发，提交Metadata和查询给AI，AI返回书籍名称列表后需要进行结果过滤和处理
   - **结果过滤**：考虑到不同AI可能返回不同格式（如带序号、带介绍语、带标点等），需要对AI返回结果进行清洗，提取纯书名后再与本地书籍列表进行模糊匹配
   - 或用户输入文字后，通过快捷键（Ctrl+Enter）或下方向键选中底部选项触发AI搜索

3. **键盘导航**：
   - ↑/↓ 键选择结果
   - Enter 打开书籍
   - Ctrl+Enter 进入完整对话（带上当前查询和结果）
   - Esc 关闭窗口

4. **操作模式**：
   - **快速打开**（Enter）：直接打开选中的书籍
   - **完整对话**（Ctrl+Enter）：进入完整对话模式，调用原Ask弹窗，使用当前书库总的Metadata信息
   - **AI搜索触发**：输入`/ `开头，或使用快捷键/下方向键选中底部选项

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
        # 判断搜索模式
        if query.startswith('/ '):
            # AI模式：提交给AI
            actual_query = query[2:]  # 移除'/ '前缀
            # 使用用户配置的AI搜索提示词
            prompt_template = prefs.get('library_ai_search_prompt', '')
            prompt = prompt_template.format(
                metadata=cached_metadata,
                query=actual_query
            )
            
            ai_response = self.api.search_library(prompt)
            
            # 过滤和处理AI返回结果
            filtered_results = self.filter_ai_response(ai_response)
            
            # 与本地书籍列表进行模糊匹配
            matched_books = self.match_local_books(filtered_results)
            self.display_results(matched_books)
        else:
            # 默认模式：本地关键词搜索
            results = self.search_local_keywords(query)
            self.display_results(results[:5])  # 最多5个结果
        
    def on_item_activated(self, item):
        # Enter 键：打开书籍
        book_id = item.data(Qt.UserRole)
        self.gui.iactions['View'].view_book(book_id)
        self.close()
        
    def filter_ai_response(self, ai_response):
        """
        过滤AI返回结果，提取纯书名
        处理各种可能的格式：
        - 带序号：1. Book Title, 1) Book Title, 1、Book Title
        - 带标点：- Book Title, * Book Title, • Book Title
        - 带介绍：Book Title - Description, Book Title (Author)
        - 带引号："Book Title", 'Book Title'
        """
        import re
        
        lines = ai_response.strip().split('\n')
        book_titles = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 移除常见的序号格式
            line = re.sub(r'^[\d]+[.、)）]\s*', '', line)
            # 移除列表标记
            line = re.sub(r'^[-*•]\s*', '', line)
            # 移除引号
            line = re.sub(r'^["\'](.+)["\']$', r'\1', line)
            # 移除括号内容（如作者、年份）
            line = re.sub(r'\s*[\(（].*?[\)）]\s*$', '', line)
            # 移除破折号后的描述
            line = re.sub(r'\s*[-–—]\s*.*$', '', line)
            
            line = line.strip()
            if line:
                book_titles.append(line)
        
        return book_titles[:5]  # 最多返回5个结果
    
    def match_local_books(self, book_titles):
        """
        将过滤后的书名与本地书籍列表进行模糊匹配
        使用Levenshtein距离或简单的子串匹配
        """
        from difflib import get_close_matches
        
        db = self.gui.current_db
        all_books = [(book_id, db.get_metadata(book_id).title) 
                     for book_id in db.all_book_ids()]
        
        matched_books = []
        all_titles = [title for _, title in all_books]
        
        for search_title in book_titles:
            # 使用difflib进行模糊匹配
            matches = get_close_matches(search_title, all_titles, n=1, cutoff=0.6)
            
            if matches:
                # 找到匹配的书籍ID
                for book_id, title in all_books:
                    if title == matches[0]:
                        matched_books.append((book_id, title))
                        break
        
        return matched_books
    
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
- ⚡ **快速**：默认本地搜索，无需等待AI响应
- 🎯 **精准**：`/ `触发AI语义搜索，智能理解用户意图
- 🔄 **灵活**：既能快速打开书，也能进入完整对话模式
- ⌨️ **高效**：全键盘操作，符合 Power User 习惯
- 💡 **明确**：通过`/ `前缀清晰区分本地搜索和AI搜索

#### 1.3 Data Update Mechanism / 数据更新机制

**按需更新**：
- 用户点击 "Update Library Data" 按钮时更新
- 首次使用时自动提示更新
- 显示更新时间和书籍数量

**代码实现**（伪代码）：
```python
def update_library_metadata():
    db = self.gui.current_db
    book_ids = db.all_book_ids()[:prefs.get('library_max_books', 100)]  # 限制最大数量
    
    selected_fields = prefs.get('library_metadata_fields', ['title', 'authors'])
    metadata_list = []
    
    for book_id in book_ids:
        mi = db.get_metadata(book_id)
        book_data = {'id': book_id}
        
        if 'title' in selected_fields:
            book_data['title'] = mi.title
        if 'authors' in selected_fields:
            book_data['authors'] = ', '.join(mi.authors or [])
        if 'series' in selected_fields:
            book_data['series'] = mi.series or ''
        if 'publisher' in selected_fields:
            book_data['publisher'] = mi.publisher or ''
        if 'pubdate' in selected_fields:
            book_data['published'] = str(mi.pubdate) if mi.pubdate else ''
        if 'language' in selected_fields:
            book_data['language'] = mi.language or ''
            
        metadata_list.append(book_data)
    
    # 压缩为单行JSON，包含版本信息
    import json
    from calibre_plugins.ask_grok.version import VERSION_STRING
    
    cached_data = {
        'version': VERSION_STRING,
        'books': metadata_list
    }
    
    # 保存为单行字符串
    prefs['library_cached_metadata'] = json.dumps(cached_data, ensure_ascii=False, separators=(',', ':'))
    prefs['library_last_update'] = datetime.now().isoformat()
    
    # 显示成功提示
    info_dialog(self.gui, 'Success', f'Successfully updated {len(metadata_list)} books', show=True)
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
| 50 books     | ~1,250           | All modern LLMs   |
| 100 books    | ~2,500           | All modern LLMs   |
| 500 books    | ~12,500          | GPT-4, Claude 3+  |
| 1000+ books  | ~25,000+         | Requires filtering|

### Performance / 性能
- 元数据提取：~0.1s per book → 100 books in ~10s
- JSON 序列化为单行：<1s for 100 books
- 首次加载后缓存，后续查询无需重新提取
- 本地关键词搜索：<50ms，无需等待AI响应
- AI语义搜索：取决于AI响应速度（1-3秒）

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

