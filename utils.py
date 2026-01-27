#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import copy

# 初始化日志
logger = logging.getLogger(__name__)

def mask_api_key(api_key, visible_chars=4, mask_chars=8):
    """
    隐藏API Key，只保留前几位字符，其余全部掩码
    
    :param api_key: 原始API Key
    :param visible_chars: 保留可见的前几位字符数（默认4）
    :param mask_chars: 显示的掩码字符数（默认8）
    :return: 隐藏后的API Key，格式如 "sk-o********"
    """
    if not api_key or len(api_key) <= visible_chars:
        return api_key
    
    # 保留前visible_chars位
    visible_part = api_key[:visible_chars]
    
    # 后面全部用固定数量的*号替代，不暴露任何额外信息
    mask_part = '*' * mask_chars
    
    return visible_part + mask_part

def mask_api_key_in_text(text):
    """
    隐藏文本中的API Key
    
    :param text: 包含API Key的文本
    :return: 隐藏API Key后的文本
    """
    if not text:
        return text
    
    # 隐藏URL参数中的API Key
    text = re.sub(r'(key=|api_key=|token=|auth_token=)([A-Za-z0-9_-]{4})([A-Za-z0-9_-]{8})([A-Za-z0-9_-]*)', 
                 r'\1\2********\4', text)
    
    # 隐藏JSON中的API Key
    text = re.sub(r'("api_key"|"key"|"token"|"auth_token")\s*:\s*"([A-Za-z0-9_-]{4})([A-Za-z0-9_-]{8})([A-Za-z0-9_-]*)"', 
                 r'\1:"\\2********\4"', text)
    
    return text

def safe_log_config(config, keys_to_mask=None):
    """
    安全地记录配置信息，隐藏敏感信息
    
    :param config: 配置字典
    :param keys_to_mask: 需要掩码的键列表，默认为['api_key', 'key', 'token', 'auth_token']
    :return: 处理后的配置字典副本
    """
    if config is None:
        return None
    
    if keys_to_mask is None:
        keys_to_mask = ['api_key', 'key', 'token', 'auth_token']
    
    # 创建配置的深拷贝，避免修改原始配置
    safe_config = copy.deepcopy(config)
    
    # 遍历配置，掩码敏感信息
    for key, value in safe_config.items():
        if key in keys_to_mask and isinstance(value, str) and value:
            safe_config[key] = mask_api_key(value)
        elif isinstance(value, dict):
            safe_config[key] = safe_log_config(value, keys_to_mask)
    
    return safe_config

def update_library_metadata(db, prefs):
    """
    提取图书馆元数据（仅书名和作者名）
    
    :param db: Calibre数据库对象
    :param prefs: 插件配置对象
    :return: (成功标志, 书籍数量, 错误信息)
    """
    try:
        import json
        from datetime import datetime
        
        # 获取所有书籍ID，最多100本
        # 使用new_api.all_book_ids()获取所有书籍ID
        try:
            book_ids = list(db.new_api.all_book_ids())[:100]
        except AttributeError:
            # 如果new_api不可用，尝试使用旧API
            book_ids = list(db.data.search_getting_ids('', db.FIELD_MAP['search']))[:100]
        
        books = []
        for book_id in book_ids:
            try:
                # 使用 index_is_id=True 确保正确获取元数据
                mi = db.get_metadata(book_id, index_is_id=True)
                if mi:
                    books.append({
                        'id': book_id,
                        'title': mi.title or 'Unknown',
                        'authors': ', '.join(mi.authors or ['Unknown'])
                    })
                else:
                    logger.warning(f"Book {book_id} metadata is None, skipping")
            except Exception as e:
                logger.warning(f"Failed to get metadata for book {book_id}: {e}")
                continue
        
        # 保存为JSON字符串
        prefs['library_cached_metadata'] = json.dumps(books, ensure_ascii=False)
        prefs['library_last_update'] = datetime.now().isoformat()
        
        # 更新统计页面的书籍数量
        try:
            from .statistics_widget import update_book_count
            update_book_count(prefs, len(books))
        except Exception as stat_error:
            logger.warning(f"Failed to update book count in statistics: {stat_error}")
        
        logger.info(f"Successfully updated library metadata: {len(books)} books")
        return True, len(books), None
        
    except Exception as e:
        error_msg = f"Failed to update library metadata: {str(e)}"
        logger.error(error_msg)
        return False, 0, error_msg

def get_library_metadata(prefs):
    """
    获取缓存的图书馆元数据
    
    :param prefs: 插件配置对象
    :return: 元数据JSON字符串，如果未缓存则返回None
    """
    return prefs.get('library_cached_metadata', None)

def get_library_last_update(prefs):
    """
    获取图书馆元数据最后更新时间
    
    :param prefs: 插件配置对象
    :return: ISO格式的时间字符串，如果未更新过则返回None
    """
    return prefs.get('library_last_update', None)

def is_library_chat_enabled(prefs):
    """
    检查是否启用了图书馆对话功能
    
    :param prefs: 插件配置对象
    :return: True/False
    """
    return prefs.get('library_chat_enabled', False)

def build_library_prompt(user_query, prefs):
    """
    构建包含图书馆元数据的AI提示词
    
    :param user_query: 用户查询
    :param prefs: 插件配置对象
    :return: 完整的提示词
    """
    cached_metadata = get_library_metadata(prefs)
    
    if not cached_metadata:
        return user_query
    
    # 获取当前语言设置
    language = prefs.get('language', 'en')
    
    # 根据语言选择提示词模板
    if language == 'zh':
        prompt = f"""您可以访问用户的图书馆。以下是所有书籍：

{cached_metadata}

用户查询：{user_query}

请找到匹配的书籍并以以下格式返回（**重要**：使用HTML链接格式，这样用户可以点击书名直接打开书籍）：

- <a href="calibre://book/书籍ID">书名</a> - 作者名

示例：
- <a href="calibre://book/123">Python编程</a> - Mark Lutz
- <a href="calibre://book/456">机器学习实战</a> - Peter Harrington

只返回匹配查询的书籍。最多5个结果。"""
    else:
        prompt = f"""You have access to the user's book library. Here are all the books:

{cached_metadata}

User query: {user_query}

Please find matching books and return them in this format (**IMPORTANT**: Use HTML link format so users can click book titles to open them directly):

- <a href="calibre://book/BOOK_ID">Book Title</a> - Author Name

Example:
- <a href="calibre://book/123">Learning Python</a> - Mark Lutz
- <a href="calibre://book/456">Machine Learning in Action</a> - Peter Harrington

Only return books that match the query. Maximum 5 results."""
    
    return prompt
