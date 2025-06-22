#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from .config import get_prefs, ConfigDialog
from .i18n import get_translation, SUGGESTION_TEMPLATES
import logging

logger = logging.getLogger(__name__)

class SuggestionWorker(QThread):
    """生成随机问题的工作线程"""
    result = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, api, book_info, i18n=None):
        super().__init__(None)  # 不设置父对象，避免随父对象一起销毁
        self.api = api
        self.i18n = i18n or {}
        
        # 验证 book_info 是否包含 title 属性
        if not hasattr(book_info, 'title'):
            error_msg = self.i18n.get("book_info_check", "book_info need to contain title attribute")
            raise ValueError(error_msg)
            
        self.book_info = book_info
        self._is_cancelled = False
        self._is_finished = False  # 标记线程是否完成

    def run(self):
        try:
            # 记录开始生成随机问题
            logger.info("开始生成随机问题...")
            
            # 准备书籍信息，使用 getattr 安全获取属性
            try:
                title = str(getattr(self.book_info, 'title', 'Unknown'))
                authors = getattr(self.book_info, 'authors', [])
                author_str = ', '.join(map(str, authors)) if authors and isinstance(authors, (list, tuple)) else 'Unknown'
                language = str(getattr(self.book_info, 'language', 'Unknown'))
            except Exception as e:
                error_msg = f"获取书籍信息时出错: {str(e)}"
                logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return
            
            # 记录书籍信息
            logger.info(f"书籍信息 - 标题: {title}, 作者: {author_str}, 语言: {language}")
            
            # 准备提示词
            template = SUGGESTION_TEMPLATES.get(get_prefs()['language'], SUGGESTION_TEMPLATES['en'])
            
            # 记录使用的模板
            logger.info(f"使用的问题随机问题模板: {template}")
            
            # 格式化提示词，包含完整的书籍信息
            prompt = template.format(
                title=title,
                author=author_str,
                language=language,
            )
            
            # 记录最终生成的提示词
            logger.info(f"生成的完整提示词: {prompt}")
            
            # 调用 API 获取随机问题，确保传递 lang_code 参数
            logger.info("正在调用 API 获取随机问题...")
            suggestion = self.api.random_question(prompt, lang_code=get_prefs()['language'])
            
            # 记录 API 返回的随机问题
            if suggestion:
                logger.info(f"成功获取到随机问题: {suggestion[:200]}...")  # 只记录前200个字符
            else:
                logger.warning("API 返回了空随机问题")
            
            if not self._is_cancelled and suggestion:
                self.result.emit(suggestion)
                
        except Exception as e:
            if not self._is_cancelled:
                self.error_occurred.emit(str(e))
        finally:
            if not self._is_cancelled:  # 只在非取消状态下发送完成信号
                self.finished.emit()
            self._is_finished = True  # 标记线程已完成
                
    def cancel(self):
        """标记取消状态，让线程自然结束"""
        self._is_cancelled = True
        
    def is_finished(self):
        """检查线程是否已完成"""
        return self._is_finished

class SuggestionHandler(QObject):
    """处理生成随机问题的逻辑"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.response_area = None
        self.input_area = None
        self.suggest_button = None
        self.i18n = {} # 初始化为空字典
        self._worker = None
        self._loading_timer = None
        self._request_cancelled = False
        self._original_input = ''
        self._original_button_text = ''
        self._response_text = ''
        self.api = None
        self._cleanup_timer = None

    def setup(self, response_area, input_area, suggest_button, api, i18n):
        """设置处理器需要的UI组件和国际化文本"""
        self.response_area = response_area
        self.input_area = input_area
        self.suggest_button = suggest_button
        self.api = api

        # 确保 i18n 是字典
        if not isinstance(i18n, dict):
            self.i18n = {}
        else:
            self.i18n = i18n
        
        # 初始化状态
        self._request_cancelled = False
        self._loading_timer = None
        self._worker = None
        self._original_input = ''
        self._original_button_text = ''
        self._response_text = ''
        self._cleanup_timer = None

    def update_i18n(self, i18n):
        """更新国际化文本对象"""
        self.i18n = i18n
        # 更新按钮文本
        if self.suggest_button.isEnabled():
            self.suggest_button.setText(self.i18n.get('suggest_button', 'Random Question'))

    def _setup_loading_animation(self):
        """设置加载动画定时器"""
        loading_text = self.i18n.get('loading_text', 'Loading')
        dots = ['', '.', '..', '...']
        current_dot = [0]

        def update_loading():
            # 只在非取消状态且没有响应时显示加载动画
            if not self._response_text and not self._request_cancelled:
                # 更新响应区域
                self.response_area.setText(f"{loading_text}{dots[current_dot[0]]}")
                # 更新按钮文本
                self.suggest_button.setText(f"{loading_text}{dots[current_dot[0]]}")
                current_dot[0] = (current_dot[0] + 1) % len(dots)

        self._loading_timer = QTimer(self)
        self._loading_timer.timeout.connect(update_loading)
        self._loading_timer.start(250)

    def _stop_loading_timer(self):
        """停止加载动画定时器"""
        try:
            if hasattr(self, '_loading_timer') and self._loading_timer is not None:
                if self._loading_timer.isActive():
                    self._loading_timer.stop()
                self._loading_timer.deleteLater()
                self._loading_timer = None
        except Exception as e:
            logger.error(f"停止加载定时器时出错: {str(e)}")

    def _check_response_timeout(self):
        """检查是否超时"""
        if not self._response_text and not self._request_cancelled:
            self._request_cancelled = True
            if self._worker:
                self._worker.cancel()
            # 直接显示请求失败状态
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))
            self._restore_ui_state()

    def _restore_ui_state(self, restore_input=False):
        """恢复UI状态"""
        if not self.suggest_button:
            return
            
        try:
            self.suggest_button.setEnabled(True)
            # 使用 i18n 获取按钮文本
            self.suggest_button.setText(self.i18n.get('suggest_button', 'Random Question') if hasattr(self, 'i18n') else 'Random Question')
            self.suggest_button.setStyleSheet("")
            
            # 是否恢复原始输入
            if restore_input and self._original_input and self.input_area:
                self.input_area.setPlainText(self._original_input)
        except Exception as e:
            logger.error(f"恢复UI状态时出错: {str(e)}")

    def _on_suggestion_received(self, suggestion):
        """处理接收到的随机问题"""
        try:
            if not self._request_cancelled:
                self._stop_loading_timer()
                self._request_cancelled = True
                
            if not suggestion:
                error_msg = self.i18n.get('empty_suggestion', 'Received empty suggestion')
                logger.warning(error_msg)
                if self.response_area:
                    self.response_area.setText(error_msg)
                return
                
            self._response_text = str(suggestion)
            
            # 更新UI
            if self.response_area:
                self.response_area.clear()
            
            if self.input_area:
                self.input_area.setPlainText(self._response_text)
                
        except Exception as e:
            error_msg = f"处理建议时出错: {str(e)}"
            logger.error(error_msg)
            if self.response_area:
                self.response_area.setText(self.i18n.get('process_suggestion_error', 'Error processing suggestion'))
        finally:
            # 确保UI状态总是能被恢复
            self._restore_ui_state()

    def _on_error(self, error):
        """处理错误"""
        if not self._request_cancelled:
            self._request_cancelled = True
            self._stop_loading_timer()
        
        if self.response_area and hasattr(self, 'i18n') and isinstance(self.i18n, dict):
            # 只显示一个错误提示
            error_text = self.i18n['suggestion_error']
            if error and str(error).strip():
                error_text = f"{error_text}: {str(error).strip()}"
            self.response_area.setText(error_text)
        
        self._restore_ui_state(restore_input=True)

    def _on_worker_finished(self):
        """工作线程完成的处理"""
        # 只清理状态，不立即删除线程
        self._stop_loading_timer()
        self.suggest_button.setEnabled(True)
        
        # 开始定期检查线程状态
        if self._worker:
            self._start_cleanup_timer()

    def _start_cleanup_timer(self):
        """开始定期检查线程状态"""
        if not self._cleanup_timer:
            self._cleanup_timer = QTimer(self)
            self._cleanup_timer.timeout.connect(self._check_worker_status)
            self._cleanup_timer.start(100)  # 每 100ms 检查一次

    def _stop_cleanup_timer(self):
        """停止清理定时器"""
        if self._cleanup_timer and self._cleanup_timer.isActive():
            self._cleanup_timer.stop()
            self._cleanup_timer.deleteLater()
            self._cleanup_timer = None

    def _check_worker_status(self):
        """检查工作线程状态"""
        if self._worker and self._worker.is_finished():
            self._stop_cleanup_timer()
            self._cleanup_worker()

    def _cleanup_worker(self):
        """安全清理工作线程"""
        if self._worker:
            try:
                if self._worker.is_finished():  # 只有在线程完成时才删除
                    self._worker.deleteLater()
            except RuntimeError:
                pass  # 忽略已经被删除的情况
            finally:
                self._worker = None

    def generate(self, book_info):
        """生成随机问题"""
        if not self.api:
            logger.error("API信息没有成功初始化，随机问题生成失败。")
            return
        if not book_info:
            logger.error("书籍信息未提供，随机问题生成失败。")
            return
        
        # 检查 auth token
        if not self.suggest_button.window()._check_auth_token():
            logger.error("Auth token检查失败，随机问题生成失败。")
            return

        # 保存原始状态
        self._original_button_text = self.suggest_button.text()
        self._original_input = self.input_area.toPlainText()
        
        # 重置状态
        self._request_cancelled = False
        self._response_text = ''
        
        # 更新UI状态
        self.suggest_button.setEnabled(False)
        self.suggest_button.setText(self.i18n.get('loading_text', 'Loading'))

        # 保持与默认状态一致的样式，特别是高度相关设置
        self.suggest_button.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                min-width: 80px;
            }
        """)
        
        # 确保UI更新
        QApplication.processEvents()
        
        # 设置加载动画
        self._setup_loading_animation()
        
        # 创建并启动工作线程
        if self._worker:
            self._cleanup_worker()
            
        self._worker = SuggestionWorker(self.api, book_info, i18n=self.i18n)
        self._worker.result.connect(self._on_suggestion_received)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()
        
        # 设置超时检查
        QTimer.singleShot(5000, self._check_response_timeout)

    def prepare_close(self):
        """准备关闭，清理资源但不影响线程运行"""
        self._stop_loading_timer()
        self._stop_cleanup_timer()
        self._request_cancelled = True
        
        # 只标记取消，让线程自然结束
        if self._worker:
            self._worker.cancel()
            self._start_cleanup_timer()  # 开始定期检查线程状态

    def cleanup(self):
        """清理资源"""
        self._stop_loading_timer()
        self._stop_cleanup_timer()
        self._request_cancelled = True
        self._cleanup_worker()
