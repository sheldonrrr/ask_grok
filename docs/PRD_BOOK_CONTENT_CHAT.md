# 书籍内容问询功能 - 技术规划文档

> **版本**: v1.5.0 规划  
> **创建日期**: 2025-02-04  
> **状态**: 规划中

## 1. 功能概述

### 1.1 目标
实现用户选中一本书后，能够：
1. **章节拆分**: 提取并拆分书籍的章节文字
2. **全书上传**: 将整本书的文字内容提交给 AI 进行问询
3. **智能对话**: 支持基于书籍内容的多轮对话

### 1.2 核心问题分析

**问题**: 书籍内容通常很长（几万到几十万字），而 AI 模型有上下文长度限制：
- GPT-4o: ~128K tokens
- Claude 3.5: ~200K tokens  
- Gemini 2.5 Pro: ~1M tokens
- DeepSeek: ~64K tokens

**解决思路**: 
1. 不一定需要多轮对话来"绕过"限制
2. 可以通过**智能分块**和**选择性上传**来优化
3. 多轮对话主要用于**上下文继承**，而非绕过限制

---

## 2. EPUB 文字提取方案

### 2.1 参考实现: karpathy/reader3

reader3 使用 `ebooklib` + `BeautifulSoup` 提取 EPUB 内容：

```python
# 核心依赖
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# 数据结构
@dataclass
class ChapterContent:
    id: str           # 内部ID
    href: str         # 文件名
    title: str        # 章节标题
    content: str      # 清理后的HTML
    text: str         # 纯文本（用于LLM）
    order: int        # 阅读顺序

# 提取纯文本
def extract_plain_text(soup: BeautifulSoup) -> str:
    text = soup.get_text(separator=' ')
    return ' '.join(text.split())  # 合并空白
```

### 2.2 推荐实现方案

#### 方案 A: 集成 ebooklib（推荐）

**优点**:
- 成熟稳定，广泛使用
- 支持 EPUB 2/3
- 可提取章节结构、目录、元数据

**实现步骤**:
1. 添加 `ebooklib` 到 `requirements.txt`
2. 创建 `epub_extractor.py` 模块
3. 实现章节提取和文本清理

```python
# epub_extractor.py 核心结构
class EPUBExtractor:
    def __init__(self, epub_path: str):
        self.book = epub.read_epub(epub_path)
    
    def get_chapters(self) -> List[Chapter]:
        """获取所有章节"""
        pass
    
    def get_chapter_text(self, chapter_id: str) -> str:
        """获取单个章节的纯文本"""
        pass
    
    def get_full_text(self) -> str:
        """获取全书纯文本"""
        pass
    
    def get_toc(self) -> List[TOCEntry]:
        """获取目录结构"""
        pass
```

#### 方案 B: 使用 Calibre 内置功能

Calibre 本身有强大的电子书处理能力，可以直接利用：

```python
from calibre.ebooks.conversion.plumber import Plumber
from calibre.ebooks.oeb.base import OEBBook
```

**优点**: 无需额外依赖，与 Calibre 深度集成  
**缺点**: API 文档较少，学习成本高

### 2.3 支持的格式扩展

| 格式 | 提取方案 | 优先级 |
|------|----------|--------|
| EPUB | ebooklib | P0 |
| PDF | pdfplumber / PyMuPDF | P1 |
| MOBI | Calibre 转换 | P2 |
| TXT | 直接读取 | P0 |

---

## 3. 上下文长度处理策略

### 3.1 Token 估算

```python
def estimate_tokens(text: str) -> int:
    """粗略估算 token 数量
    
    英文: ~4 字符/token
    中文: ~1.5 字符/token
    """
    # 简单估算
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.5 + other_chars / 4)
```

### 3.2 智能分块策略

#### 策略 1: 按章节分块（推荐）

```python
class ChapterChunker:
    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
    
    def chunk_book(self, chapters: List[Chapter]) -> List[Chunk]:
        """将书籍按章节分块，确保每块不超过限制"""
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for chapter in chapters:
            chapter_tokens = estimate_tokens(chapter.text)
            
            if current_tokens + chapter_tokens > self.max_tokens:
                # 保存当前块，开始新块
                chunks.append(Chunk(chapters=current_chunk))
                current_chunk = [chapter]
                current_tokens = chapter_tokens
            else:
                current_chunk.append(chapter)
                current_tokens += chapter_tokens
        
        if current_chunk:
            chunks.append(Chunk(chapters=current_chunk))
        
        return chunks
```

#### 策略 2: 滑动窗口分块

适用于需要保持上下文连续性的场景：

```python
def sliding_window_chunk(text: str, 
                         window_size: int = 80000,
                         overlap: int = 5000) -> List[str]:
    """滑动窗口分块，保持重叠以维持上下文"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + window_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
```

### 3.3 用户选择模式

提供三种上传模式供用户选择：

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **单章节** | 选择特定章节上传 | 精读、章节分析 |
| **多章节** | 选择多个章节上传 | 跨章节分析 |
| **全书** | 智能分块上传全书 | 全书总结、主题分析 |

---

## 4. 多轮对话与上下文继承

### 4.1 为什么需要多轮对话？

多轮对话的主要目的**不是**绕过上下文限制，而是：

1. **对话连续性**: 用户可以追问、深入探讨
2. **上下文积累**: AI 记住之前的讨论内容
3. **渐进式分析**: 先概览，再深入特定部分

### 4.2 对话历史管理

#### 方案 A: 完整历史（简单但受限）

```python
class ConversationManager:
    def __init__(self):
        self.messages = []  # 完整对话历史
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> List[dict]:
        return self.messages
```

**问题**: 历史越长，token 消耗越大

#### 方案 B: 滑动窗口历史（推荐）

```python
class SlidingWindowConversation:
    def __init__(self, max_history_tokens: int = 20000):
        self.messages = []
        self.max_tokens = max_history_tokens
        self.system_message = None  # 系统消息（含书籍内容）
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim_history()
    
    def _trim_history(self):
        """保留最近的对话，确保不超过限制"""
        while self._count_tokens() > self.max_tokens and len(self.messages) > 2:
            # 保留第一条和最后几条
            self.messages.pop(1)
    
    def get_messages_for_api(self) -> List[dict]:
        """获取发送给 API 的消息列表"""
        result = []
        if self.system_message:
            result.append({"role": "system", "content": self.system_message})
        result.extend(self.messages)
        return result
```

#### 方案 C: 摘要压缩（高级）

```python
class SummarizedConversation:
    def __init__(self):
        self.summary = ""  # 之前对话的摘要
        self.recent_messages = []  # 最近几轮对话
    
    async def compress_history(self, api_client):
        """让 AI 总结之前的对话"""
        if len(self.recent_messages) > 6:
            old_messages = self.recent_messages[:-4]
            summary_prompt = f"请简洁总结以下对话的要点：\n{old_messages}"
            new_summary = await api_client.ask(summary_prompt)
            self.summary = f"{self.summary}\n{new_summary}"
            self.recent_messages = self.recent_messages[-4:]
```

### 4.3 API 调用结构

```python
# 标准 OpenAI 兼容格式
messages = [
    {
        "role": "system",
        "content": """你是一个书籍分析助手。
        
以下是用户正在阅读的书籍内容：
---
{book_content}
---

请基于以上内容回答用户的问题。"""
    },
    {"role": "user", "content": "这本书的主题是什么？"},
    {"role": "assistant", "content": "这本书的主题是..."},
    {"role": "user", "content": "能详细说说第三章吗？"}
]
```

---

## 5. UI 设计方案

### 5.1 章节选择器

```
┌─────────────────────────────────────────┐
│ 📖 书籍内容                    [展开/收起] │
├─────────────────────────────────────────┤
│ ☑ 第一章 - 引言          (2,345 tokens) │
│ ☐ 第二章 - 背景          (5,678 tokens) │
│ ☑ 第三章 - 核心理论      (8,901 tokens) │
│ ☐ 第四章 - 案例分析      (6,543 tokens) │
│ ...                                      │
├─────────────────────────────────────────┤
│ 已选择: 2 章节 | 预估: 11,246 tokens     │
│ [全选] [取消全选] [智能选择]              │
└─────────────────────────────────────────┘
```

### 5.2 对话模式切换

```
┌─────────────────────────────────────────┐
│ 对话模式: ○ 单次问答  ● 连续对话         │
│                                          │
│ 连续对话设置:                            │
│   历史保留: [最近 5 轮 ▼]                │
│   [清除对话历史]                         │
└─────────────────────────────────────────┘
```

### 5.3 内容预览

```
┌─────────────────────────────────────────┐
│ 📄 内容预览                              │
├─────────────────────────────────────────┤
│ 第一章 - 引言                            │
│ ─────────────────────────────────────── │
│ 在这个信息爆炸的时代，我们每天都被海量   │
│ 的数据所包围。本书将探讨如何在这样的环   │
│ 境中保持清醒的思考...                    │
│                                          │
│ [查看完整内容] [复制到剪贴板]            │
└─────────────────────────────────────────┘
```

---

## 6. 技术实现路线图

### Phase 1: EPUB 文字提取（MVP）

**目标**: 实现基础的 EPUB 文字提取功能

**任务**:
- [ ] 添加 `ebooklib` 依赖
- [ ] 创建 `epub_extractor.py` 模块
- [ ] 实现章节列表获取
- [ ] 实现单章节文本提取
- [ ] 实现全书文本提取
- [ ] 添加 token 估算功能

**预计工时**: 2-3 天

### Phase 2: 章节选择 UI

**目标**: 提供用户友好的章节选择界面

**任务**:
- [ ] 创建章节选择对话框
- [ ] 实现章节列表展示（带 token 估算）
- [ ] 实现多选功能
- [ ] 实现内容预览
- [ ] 集成到主界面

**预计工时**: 3-4 天

### Phase 3: 多轮对话支持

**目标**: 实现基于书籍内容的连续对话

**任务**:
- [ ] 创建 `ConversationManager` 类
- [ ] 修改 API 调用支持多轮消息
- [ ] 实现对话历史管理
- [ ] 添加对话模式切换 UI
- [ ] 实现对话历史清除功能

**预计工时**: 3-4 天

### Phase 4: 智能分块与优化

**目标**: 处理超长内容，优化用户体验

**任务**:
- [ ] 实现智能分块算法
- [ ] 添加分块上传进度提示
- [ ] 实现对话摘要压缩（可选）
- [ ] 性能优化

**预计工时**: 2-3 天

---

## 7. 数据结构设计

### 7.1 书籍内容缓存

```python
@dataclass
class BookContent:
    """书籍内容缓存结构"""
    book_id: int                    # Calibre 书籍 ID
    title: str                      # 书名
    format: str                     # 格式 (epub, pdf, etc.)
    chapters: List[ChapterInfo]     # 章节列表
    extracted_at: datetime          # 提取时间
    total_tokens: int               # 总 token 数

@dataclass
class ChapterInfo:
    """章节信息"""
    id: str
    title: str
    order: int
    text: str
    token_count: int
    
@dataclass
class ConversationState:
    """对话状态"""
    book_id: int
    messages: List[Message]
    selected_chapters: List[str]
    created_at: datetime
    updated_at: datetime
```

### 7.2 配置项扩展

```python
# 新增配置项
BOOK_CONTENT_SETTINGS = {
    'enable_book_content_chat': True,      # 启用书籍内容对话
    'default_conversation_mode': 'single', # single / continuous
    'max_history_rounds': 5,               # 最大历史轮数
    'auto_chunk_threshold': 100000,        # 自动分块阈值 (tokens)
    'chunk_overlap': 500,                  # 分块重叠 (tokens)
    'cache_extracted_content': True,       # 缓存提取的内容
}
```

---

## 8. 风险与注意事项

### 8.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| EPUB 格式多样性 | 部分书籍提取失败 | 添加错误处理，支持回退方案 |
| Token 估算不准确 | 请求超限 | 预留 10% 余量，添加重试机制 |
| 大文件处理慢 | 用户体验差 | 异步处理，显示进度条 |

### 8.2 用户体验注意

1. **首次使用引导**: 提供简单的使用说明
2. **进度反馈**: 长时间操作需显示进度
3. **错误提示**: 清晰的错误信息和解决建议
4. **性能提示**: 当选择内容过多时给出警告

### 8.3 隐私考虑

- 书籍内容会发送到 AI 服务商
- 需在 UI 中明确提示用户
- 考虑添加"仅本地处理"选项（使用 Ollama）

---

## 9. 总结

### 核心结论

1. **不需要通过多轮对话绕过上下文限制**
   - 现代 LLM 上下文窗口已足够大（128K-1M tokens）
   - 一本普通书籍约 10-30 万字，约 5-15 万 tokens
   - 大多数情况可以一次性上传

2. **多轮对话的真正价值是上下文继承**
   - 让 AI 记住之前的讨论
   - 支持追问和深入探讨
   - 提供更自然的交互体验

3. **推荐的实现优先级**
   - P0: EPUB 文字提取 + 章节选择
   - P1: 多轮对话支持
   - P2: 智能分块 + 其他格式支持

### 下一步行动

1. 确认功能范围和优先级
2. 开始 Phase 1 开发
3. 设计详细的 UI 原型
