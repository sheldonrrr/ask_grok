#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import hashlib
from datetime import datetime
from calibre.utils.config import config_dir

logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self):
        # 使用新的历史记录文件（v2版本）
        self.history_file = os.path.join(config_dir, 'plugins', 'ask_ai_plugin_history_v2.json')
        self.histories = self._load_histories()
        
        # 保留旧版本文件路径用于迁移
        self.old_history_file = os.path.join(config_dir, 'plugins', 'ask_ai_plugin_latest_history.json')
    
    def _load_histories(self):
        """加载历史记录文件（新版本格式）"""
        if not os.path.exists(self.history_file):
            return {}
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
            # 备份损坏的文件
            try:
                import shutil
                backup_file = f"{self.history_file}.bak"
                shutil.copy2(self.history_file, backup_file)
                logger.warning(f"历史记录文件已损坏，已备份到: {backup_file}")
            except Exception as backup_error:
                logger.error(f"备份历史记录文件失败: {str(backup_error)}")
            return {}
    
    def _save_histories(self):
        """保存历史记录到文件"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.histories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存历史记录失败: {str(e)}")
    
    def generate_uid(self, book_ids):
        """
        生成唯一 UID
        
        Args:
            book_ids: 书籍ID列表
            
        Returns:
            str: UID格式 {timestamp}_{book_ids_hash}
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        book_ids_sorted = sorted([str(bid) for bid in book_ids])
        book_ids_str = ','.join(book_ids_sorted)
        hash_suffix = hashlib.md5(book_ids_str.encode()).hexdigest()[:12]
        
        return f"{timestamp}_{hash_suffix}"
    
    def save_history(self, uid, mode, books_metadata, question, answer):
        """
        保存历史记录
        
        Args:
            uid: 唯一标识符
            mode: 'single' 或 'multi'
            books_metadata: 书籍元数据列表
            question: 用户问题
            answer: AI回答
        """
        history_entry = {
            'uid': uid,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mode': mode,
            'books': books_metadata,
            'question': question,
            'answer': answer
        }
        
        # 添加或更新历史记录
        self.histories[uid] = history_entry
        self._save_histories()
        
        logger.info(f"历史记录已保存: UID={uid}, 模式={mode}, 书籍数={len(books_metadata)}")
    
    def get_related_histories(self, book_ids):
        """
        获取包含指定书籍的所有历史记录
        
        Args:
            book_ids: 书籍ID列表
            
        Returns:
            历史记录列表，按时间倒序
        """
        related = []
        
        for uid, history in self.histories.items():
            # 检查是否包含任意一本书
            history_book_ids = [book['id'] for book in history['books']]
            if any(book_id in history_book_ids for book_id in book_ids):
                related.append(history)
        
        # 按时间倒序排序
        related.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return related
    
    def get_history_by_uid(self, uid):
        """根据 UID 获取历史记录"""
        return self.histories.get(uid)
    
    def clear_history(self):
        """清空所有历史记录"""
        try:
            self.histories = {}
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            logger.info("所有历史记录已清空")
            return True
        except Exception as e:
            logger.error(f"清空历史记录失败: {str(e)}")
            return False
    
    # 保留旧版本兼容方法
    def get_history(self, metadata):
        """
        获取指定书籍的历史记录（旧版本兼容）
        
        Args:
            metadata: 书籍元数据字典
            
        Returns:
            dict: 历史记录，如果没有则返回None
        """
        # 尝试通过书籍ID查找
        book_id = metadata.get('id')
        if book_id:
            histories = self.get_related_histories([book_id])
            if histories:
                # 返回最新的一条记录
                return histories[0]
        return None
