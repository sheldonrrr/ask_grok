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
    
    def save_history(self, uid, mode, books_metadata, question, answer, ai_id=None, model_info=None):
        """
        保存历史记录（支持多AI响应）
        
        Args:
            uid: 唯一标识符
            mode: 'single' 或 'multi'
            books_metadata: 书籍元数据列表
            question: 用户问题
            answer: AI回答（单个AI）或字典（多个AI）
            ai_id: AI标识符（可选，用于多AI场景）
            model_info: 模型信息字典（可选），包含provider_name, model, api_base等
        """
        # 如果历史记录不存在，创建新的
        if uid not in self.histories:
            self.histories[uid] = {
                'uid': uid,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'mode': mode,
                'books': books_metadata,
                'question': question,
                'answers': {}  # 改为字典，支持多个AI的响应
            }
        else:
            # 历史记录已存在，更新问题（以防用户修改了问题）
            self.histories[uid]['question'] = question
            # 更新时间戳为最新的响应时间
            self.histories[uid]['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 确保answers键存在（兼容旧格式）
        if 'answers' not in self.histories[uid]:
            # 旧格式转换：如果有answer字段，迁移到answers['default']
            if 'answer' in self.histories[uid]:
                old_answer = self.histories[uid].pop('answer')
                self.histories[uid]['answers'] = {
                    'default': {
                        'answer': old_answer,
                        'timestamp': self.histories[uid]['timestamp']
                    }
                }
            else:
                self.histories[uid]['answers'] = {}
        
        # 更新或添加AI的响应
        if ai_id:
            # 多AI场景：保存特定AI的响应
            answer_data = {
                'answer': answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 如果提供了模型信息，保存它
            if model_info:
                answer_data['model_info'] = model_info
            self.histories[uid]['answers'][ai_id] = answer_data
            logger.info(f"历史记录已保存: UID={uid}, AI={ai_id}, 模式={mode}, 问题长度={len(question)}, 答案长度={len(answer)}")
        else:
            # 单AI场景（向后兼容）：使用'default'作为key
            answer_data = {
                'answer': answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 如果提供了模型信息，保存它
            if model_info:
                answer_data['model_info'] = model_info
            self.histories[uid]['answers']['default'] = answer_data
            logger.info(f"历史记录已保存: UID={uid}, 模式={mode}, 书籍数={len(books_metadata)}, 问题长度={len(question)}, 答案长度={len(answer)}")
        
        self._save_histories()
    
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
    
    def delete_history(self, uid):
        """删除指定UID的历史记录
        
        Args:
            uid: 历史记录的唯一标识符
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            if uid in self.histories:
                del self.histories[uid]
                self._save_histories()
                logger.info(f"已删除历史记录: {uid}")
                return True
            else:
                logger.warning(f"历史记录不存在: {uid}")
                return False
        except Exception as e:
            logger.error(f"删除历史记录失败: {str(e)}")
            return False
    
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
