# 开发计划：多书选择与元数据对话功能

**创建日期**: 2025-01-24  
**最后更新**: 2025-01-24  
**功能描述**: 支持选择多本书籍，提取并聚合元数据信息，让AI基于多本书的前置信息进行对话

---

## 一、核心需求

### 1.1 窗口标题
- **单书模式**：`提问 - 书名`
- **多书模式**：`提问 - 3本书`（仅显示数量，不显示书名）

### 1.2 元数据展示（可折叠列表）
- **可折叠列表**：每本书的元数据可独立展开/收起
- **默认状态**：
  - 单书模式：元数据展开
  - 多书模式：所有书籍元数据收起
  - 单书模式和多书模式均展示书名
- **元数据内容**：保持现有字段（标题、作者、出版社、出版日期、语言、系列等）
- **已删除书籍处理**：元数据区域置灰显示，保留书籍信息但标注为"已删除"

### 1.3 提示词系统
- **独立多书提示词**：在 Config 的"提示设置"中新增独立配置项
- **用户可编辑**：支持自定义多书提示词模板
- **简单拼接逻辑**：不使用复杂模板变量，直接拼接所有书籍的元数据
  - 示例：`书籍1: 标题、作者、出版日期、系列、出版社、语言\n书籍2: 标题、作者、出版日期、系列、出版社、语言\n用户问题: {query}`

### 1.4 历史记录系统（核心变更）

#### 历史记录切换器
- 在对话窗口标题添加历史记录切换下拉菜单
- 显示当前书籍关联的所有历史记录（单书或多书）
- 格式示例：
  - `单书: 1本书 - 2025-01-24 12:30`
  - `多书: 3本书 - 2025-01-24 14:15`

#### 跨模式切换
- 从单书历史切换到多书历史时：
  - 自动切换到多书模式
  - 窗口标题更新为 `提问 - 3本书`
  - 元数据区域显示多本书（默认收起）
  - 加载对应的问答内容
  - calibre中选择多本书调起对话窗口时，自动切换到多书模式
  - calibre切换到多书历史时，同时自动选择该集合下的多本书（如果技术可行的话就做）

#### UID 机制
- 每个提问对象（单书或多书组合）分配唯一 UID
- UID 格式：`{timestamp}_{book_ids_hash}`
  - 示例：`20250124123045_abc123def456`
- 用于关联历史记录和书籍组合

#### 数据库扩容
新增字段到历史记录 JSON 结构：

```json
{
  "uid": "20250124123045_abc123def456",
  "timestamp": "2025-01-24 12:30:45",
  "mode": "multi",
  "books": [
    {
      "id": 123,
      "title": "书名1",
      "authors": ["作者1"],
      "publisher": "出版社1",
      "pubdate": "2023-01-01",
      "language": "zh",
      "series": "系列1",
      "deleted": false
    },
    {
      "id": 456,
      "title": "书名2",
      "deleted": true
    }
  ],
  "question": "用户问题",
  "answer": "AI回答"
}
```

---

## 二、技术实现方案

### 2.1 数据结构设计

#### 修改 `AskDialog.__init__`

```python
def __init__(self, gui, books_info, api, history_uid=None):
    """
    Args:
        books_info: 单个 Metadata 对象或 Metadata 列表
        history_uid: 可选，用于加载特定历史记录
    """
    super().__init__(gui)
    self.gui = gui
    self.api = api
    
    # 统一处理为列表
    if isinstance(books_info, list):
        self.books_info = books_info
        self.is_multi_book = len(books_info) > 1
    else:
        self.books_info = [books_info]
        self.is_multi_book = False
    
    # 向后兼容
    self.book_info = self.books_info[0]
    
    # 生成或加载 UID
    if history_uid:
        self.current_uid = history_uid
    else:
        self.current_uid = self._generate_uid()
    
    # 准备书籍元数据列表
    self.books_metadata = [self._extract_metadata(book) for book in self.books_info]
    self.book_metadata = self.books_metadata[0]
```

#### UID 生成方法

```python
def _generate_uid(self):
    """生成唯一 UID"""
    import hashlib
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    book_ids = sorted([str(book.id) for book in self.books_info])
    book_ids_str = ','.join(book_ids)
    hash_suffix = hashlib.md5(book_ids_str.encode()).hexdigest()[:12]
    
    return f"{timestamp}_{hash_suffix}"
```

#### 元数据提取方法

```python
def _extract_metadata(self, book_info):
    """提取单本书的元数据"""
    pubdate = book_info.get('pubdate', '')
    if hasattr(pubdate, 'strftime'):
        pubdate = pubdate.strftime('%Y-%m-%d')
    elif isinstance(pubdate, str) and 'T' in pubdate:
        pubdate = pubdate.split('T')[0]
    
    # 检查书籍是否仍存在
    try:
        db = self.gui.current_db
        db.get_metadata(book_info.id, index_is_id=True)
        deleted = False
    except:
        deleted = True
    
    return {
        'id': book_info.id,
        'title': book_info.get('title', ''),
        'authors': book_info.get('authors', []),
        'publisher': book_info.get('publisher', ''),
        'pubdate': pubdate,
        'languages': book_info.get('languages', []),
        'series': book_info.get('series', ''),
        'deleted': deleted
    }
```

### 2.2 UI 实现

#### 窗口标题更新

```python
def _update_window_title(self):
    """更新窗口标题"""
    if self.is_multi_book:
        book_count = len(self.books_info)
        title = f"{self.i18n['menu_title']} - {book_count}{self.i18n['books_unit']}"
    else:
        title = f"{self.i18n['menu_title']} - {self.book_info.title}"
    
    self.setWindowTitle(title)
```

#### 可折叠元数据列表

```python
def _create_metadata_widget(self):
    """创建可折叠的元数据展示组件"""
    from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
    from PyQt5.QtGui import QColor
    
    self.metadata_tree = QTreeWidget()
    self.metadata_tree.setHeaderHidden(True)
    self.metadata_tree.setMaximumHeight(300)
    
    for idx, book_meta in enumerate(self.books_metadata):
        # 创建书籍节点
        book_item = QTreeWidgetItem(self.metadata_tree)
        
        # 设置书籍标题
        title_text = f"{idx + 1}. {book_meta['title']}"
        if book_meta['deleted']:
            title_text += f" ({self.i18n['deleted']})"
            book_item.setForeground(0, QColor(128, 128, 128))
        
        book_item.setText(0, title_text)
        
        # 添加元数据子节点
        if book_meta['authors']:
            author_item = QTreeWidgetItem(book_item)
            author_item.setText(0, f"{self.i18n['metadata_authors']}: {', '.join(book_meta['authors'])}")
        
        if book_meta['publisher']:
            pub_item = QTreeWidgetItem(book_item)
            pub_item.setText(0, f"{self.i18n['metadata_publisher']}: {book_meta['publisher']}")
        
        if book_meta['pubdate']:
            date_item = QTreeWidgetItem(book_item)
            date_item.setText(0, f"{self.i18n['metadata_pubyear']}: {book_meta['pubdate']}")
        
        if book_meta['languages']:
            lang_item = QTreeWidgetItem(book_item)
            lang_name = self.get_language_name(book_meta['languages'][0])
            lang_item.setText(0, f"{self.i18n['metadata_language']}: {lang_name}")
        
        if book_meta['series']:
            series_item = QTreeWidgetItem(book_item)
            series_item.setText(0, f"{self.i18n['metadata_series']}: {book_meta['series']}")
        
        # 设置默认展开/收起状态
        # 单书模式：展开；多书模式：收起
        # 但两种模式都显示书名（作为树节点的根节点文本）
        book_item.setExpanded(not self.is_multi_book)
    
    return self.metadata_tree
```

#### 历史记录切换按钮

```python
def _create_history_switcher(self):
    """创建历史记录切换按钮和菜单"""
    from PyQt5.QtWidgets import QToolButton, QMenu
    
    self.history_button = QToolButton()
    self.history_button.setText(self.i18n['history'])
    self.history_button.setPopupMode(QToolButton.InstantPopup)
    
    self.history_menu = QMenu()
    self.history_button.setMenu(self.history_menu)
    
    self._load_related_histories()
    
    return self.history_button

def _load_related_histories(self):
    """加载当前书籍关联的所有历史记录"""
    if not hasattr(self.response_handler, 'history_manager'):
        return
    
    current_book_ids = [book.id for book in self.books_info]
    all_histories = self.response_handler.history_manager.get_related_histories(current_book_ids)
    
    self.history_menu.clear()
    
    # 新对话选项
    new_action = self.history_menu.addAction(self.i18n['new_conversation'])
    new_action.triggered.connect(lambda: self._on_history_switched(None))
    
    if all_histories:
        self.history_menu.addSeparator()
    
    # 历史记录列表（统一显示格式）
    for history in all_histories:
        book_count = len(history['books'])
        display_text = f"{book_count}{self.i18n['books_unit']} - {history['timestamp']}"
        
        action = self.history_menu.addAction(display_text)
        action.triggered.connect(lambda checked, uid=history['uid']: self._on_history_switched(uid))

def _on_history_switched(self, uid):
    """历史记录切换事件"""
    if uid is None:
        # 新对话
        self.input_area.clear()
        self.response_area.clear()
        return
    
    history = self.response_handler.history_manager.get_history_by_uid(uid)
    if not history:
        return
    
    # 重建书籍列表
    books_info = []
    book_ids_to_select = []  # 用于反向选择
    
    for book_meta in history['books']:
        book_ids_to_select.append(book_meta['id'])
        if not book_meta['deleted']:
            try:
                db = self.gui.current_db
                mi = db.get_metadata(book_meta['id'], index_is_id=True)
                books_info.append(mi)
            except:
                pass
    
    # 更新当前状态
    self.books_info = books_info if books_info else self.books_info
    self.is_multi_book = len(history['books']) > 1
    self.current_uid = uid
    
    # 反向选择：在 Calibre 中选中这些书籍（如果技术可行）
    self._select_books_in_calibre(book_ids_to_select)
    
    # 更新 UI
    self._update_window_title()
    self._rebuild_metadata_widget()
    
    # 加载问答内容
    self.input_area.setPlainText(history['question'])
    self.response_handler._update_ui_from_signal(
        history['answer'], 
        is_response=True,
        is_history=True
    )

def _select_books_in_calibre(self, book_ids):
    """在 Calibre 主界面中选中指定书籍"""
    try:
        from PyQt5.QtCore import QItemSelectionModel
        
        # 清除当前选择
        self.gui.library_view.selectionModel().clear()
        
        # 选中指定书籍
        model = self.gui.library_view.model()
        for book_id in book_ids:
            try:
                # 查找书籍在视图中的行号
                row = model.id_to_row(book_id)
                if row is not None:
                    index = model.index(row, 0)
                    self.gui.library_view.selectionModel().select(
                        index, 
                        QItemSelectionModel.Select | QItemSelectionModel.Rows
                    )
            except:
                # 书籍可能已被删除或不在当前视图中
                pass
    except Exception as e:
        logger.warning(f"无法在 Calibre 中选中书籍: {str(e)}")
```

### 2.3 提示词系统

#### Config 配置新增

```python
# 默认多书提示词模板
DEFAULT_MULTI_BOOK_TEMPLATE = """以下是关于多本书籍的信息：

{books_metadata}

用户问题：{query}

请基于以上书籍信息回答问题。"""

# 在 prefs 初始化中添加
prefs.defaults['multi_book_template'] = DEFAULT_MULTI_BOOK_TEMPLATE
```

#### 提示词拼接逻辑

```python
def _build_multi_book_prompt(self, question):
    """构建多书提示词"""
    from calibre_plugins.ask_ai_plugin.config import get_prefs
    prefs = get_prefs()
    
    template = prefs.get('multi_book_template', DEFAULT_MULTI_BOOK_TEMPLATE)
    
    # 拼接所有书籍元数据（包含所有字段：标题、作者、出版日期、系列、出版社、语言）
    books_metadata_text = []
    for idx, book in enumerate(self.books_info, 1):
        book_text = f"书籍 {idx}:\n"
        book_text += f"  标题: {book.title}\n"
        
        if book.authors:
            book_text += f"  作者: {', '.join(book.authors)}\n"
        
        if hasattr(book, 'pubdate') and book.pubdate:
            year = str(book.pubdate.year) if hasattr(book.pubdate, 'year') else str(book.pubdate)
            book_text += f"  出版日期: {year}\n"
        
        if hasattr(book, 'series') and book.series:
            book_text += f"  系列: {book.series}\n"
        
        if book.publisher:
            book_text += f"  出版社: {book.publisher}\n"
        
        if book.language:
            lang_name = self.get_language_name(book.language)
            book_text += f"  语言: {lang_name}\n"
        
        books_metadata_text.append(book_text)
    
    prompt = template.format(
        books_metadata='\n'.join(books_metadata_text),
        query=question
    )
    
    return prompt
```

### 2.4 历史记录管理器扩展

```python
class HistoryManager:
    def __init__(self):
        self.history_file = os.path.join(
            config_dir, 'plugins', 'ask_ai_plugin_history_v2.json'
        )
        self.histories = self._load_histories()
    
    def save_history(self, uid, mode, books_metadata, question, answer):
        """保存历史记录"""
        from datetime import datetime
        
        history_entry = {
            'uid': uid,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mode': mode,
            'books': books_metadata,
            'question': question,
            'answer': answer
        }
        
        self.histories[uid] = history_entry
        self._save_histories()
    
    def get_related_histories(self, book_ids):
        """获取包含指定书籍的所有历史记录"""
        related = []
        
        for uid, history in self.histories.items():
            history_book_ids = [book['id'] for book in history['books']]
            if any(book_id in history_book_ids for book_id in book_ids):
                related.append(history)
        
        related.sort(key=lambda x: x['timestamp'], reverse=True)
        return related
    
    def get_history_by_uid(self, uid):
        """根据 UID 获取历史记录"""
        return self.histories.get(uid)
```

### 2.5 修改 `show_dialog` 方法

```python
def show_dialog(self):
    self.initialize_api()
    
    rows = self.gui.library_view.selectionModel().selectedRows()
    if not rows or len(rows) == 0:
        return
    
    db = self.gui.current_db
    
    if len(rows) == 1:
        book_id = self.gui.library_view.model().id(rows[0])
        mi = db.get_metadata(book_id, index_is_id=True)
        books_info = mi
    else:
        books_info = []
        for row in rows:
            book_id = self.gui.library_view.model().id(row)
            mi = db.get_metadata(book_id, index_is_id=True)
            books_info.append(mi)
    
    d = AskDialog(self.gui, books_info, self.api)
    self.ask_dialog = d
    d.finished.connect(lambda result: setattr(self, 'ask_dialog', None))
    d.exec_()
```

---

## 三、i18n 翻译

### 3.1 中文 (zh.py)

```python
'books_unit': '本书',
'new_conversation': '新对话',
'single_book': '单书',
'multi_book': '多书',
'deleted': '已删除',
'history': '历史记录',
'multi_book_template_label': '多书提示词模板:',
```

### 3.2 繁体中文 (zht.py)

```python
'books_unit': '本書',
'new_conversation': '新對話',
'single_book': '單書',
'multi_book': '多書',
'deleted': '已刪除',
'history': '歷史記錄',
'multi_book_template_label': '多書提示詞模板:',
```

### 3.3 英文 (en.py)

```python
'books_unit': ' books',
'new_conversation': 'New Conversation',
'single_book': 'Single Book',
'multi_book': 'Multi-Book',
'deleted': 'Deleted',
'history': 'History',
'multi_book_template_label': 'Multi-Book Prompt Template:',
```

---

## 四、实施阶段

### Phase 1: 数据结构与历史记录系统
- 修改 `HistoryManager` 类
- 实现 UID 生成机制
- 实现新的历史记录方法

### Phase 2: AskDialog 核心重构
- 修改 `__init__` 支持单书/多书模式
- 实现元数据提取方法
- 修改 `show_dialog` 支持多书选择

### Phase 3: UI 组件实现
- 实现可折叠元数据树形组件
- 实现历史记录切换器
- 修改窗口标题更新逻辑

### Phase 4: 提示词系统
- 在 `config.py` 添加多书提示词配置
- 在 Config UI 添加编辑器
- 实现多书提示词构建方法

### Phase 5: 历史记录切换逻辑
- 实现历史记录加载方法
- 实现切换事件处理
- 实现跨模式切换逻辑

### Phase 6: i18n 翻译
- 添加中文、繁体中文、英文翻译

### Phase 7: 集成与调试
- 整合所有组件
- 向后兼容性测试
- 边界情况处理

---

**文档版本**: 2.0  
**最后更新**: 2025-01-24  
**状态**: 待实施
