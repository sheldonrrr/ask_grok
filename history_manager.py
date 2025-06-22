#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
from datetime import datetime
from calibre.utils.config import config_dir

logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self):
        self.history_file = os.path.join(config_dir, 'plugins', 'ask_grok_latest_history.json')
        self.history_data = self._load_history()
    
    def _load_history(self):
        """加载历史记录文件"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
            # 如果解析失败，尝试备份并创建新文件
            try:
                if os.path.exists(self.history_file):
                    import shutil
                    backup_file = f"{self.history_file}.bak"
                    shutil.copy2(self.history_file, backup_file)
                    logger.warning(f"历史记录文件已损坏，已备份到: {backup_file}")
            except Exception as backup_error:
                logger.error(f"备份历史记录文件失败: {str(backup_error)}")
        
        # 如果文件不存在或解析失败，返回默认结构
        return {"books": {}}
    
    def _save_history(self):
        """保存历史记录到文件"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            # 创建一个可序列化的数据副本
            serializable_data = json.loads(json.dumps(
                self.history_data,
                default=lambda o: o.isoformat() if hasattr(o, 'isoformat') else str(o),
                ensure_ascii=False,
                indent=2
            ))
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存历史记录失败: {str(e)}")
            return False
    
    def generate_book_key(self, metadata):
        """
        生成书籍的唯一键
        
        Args:
            metadata: 包含书籍元数据的字典，需要包含 title, authors, publisher, pubdate, languages
            
        Returns:
            str: 唯一键
        """
        try:
            # 确保作者列表是有序的
            authors = tuple(sorted(metadata.get('authors', [])))
            languages = tuple(sorted(metadata.get('languages', [])))
            
            # 构建键值元组
            key_data = (
                metadata.get('title', '').lower().strip(),
                authors,
                metadata.get('publisher', '').lower().strip(),
                metadata.get('pubdate') or '',
                languages
            )
            # 使用元组的字符串表示作为键
            return str(key_data)
        except Exception as e:
            logger.error(f"生成书籍键失败: {str(e)}")
            return None
    
    def save_history(self, metadata, question, answer):
        """
        保存问询历史
        
        Args:
            metadata: 书籍元数据
            question: 用户问题
            answer: AI回答
            
        Returns:
            bool: 是否保存成功
        """
        try:
            book_key = self.generate_book_key(metadata)
            if not book_key:
                return False
                
            # 准备要保存的数据
            history_entry = {
                "metadata": {
                    "title": metadata.get('title', ''),
                    "authors": metadata.get('authors', []),
                    "publisher": metadata.get('publisher', ''),
                    "pubdate": metadata.get('pubdate', ''),
                    "languages": metadata.get('languages', [])
                },
                "history": {
                    "timestamp": datetime.now().isoformat(),
                    "question": question,
                    "answer": answer
                }
            }
            
            # 更新历史记录
            self.history_data["books"][book_key] = history_entry
            
            # 保存到文件
            return self._save_history()
            
        except Exception as e:
            logger.error(f"保存问询历史失败: {str(e)}")
            return False
    
    def get_history(self, metadata):
        """
        获取指定书籍的历史记录
        
        Args:
            metadata: 书籍元数据
            
        Returns:
            dict: 历史记录，如果没有则返回None
        """
        try:
            book_key = self.generate_book_key(metadata)
            if book_key and book_key in self.history_data.get("books", {}):
                return self.history_data["books"][book_key]["history"]
            return None
        except Exception as e:
            logger.error(f"获取历史记录失败: {str(e)}")
            return None
    
    def clear_history(self):
        """清空所有历史记录"""
        try:
            self.history_data = {"books": {}}
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            return True
        except Exception as e:
            logger.error(f"清空历史记录失败: {str(e)}")
            return False
