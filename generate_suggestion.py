#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from .config import get_prefs, ConfigDialog
from .i18n import SUGGESTION_TEMPLATES

class SuggestionWorker(QThread):
    """生成建议的工作线程"""
    result = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, api, book_info):
        super().__init__(None)  # 不设置父对象，避免随父对象一起销毁
        self.api = api
        self.book_info = book_info
        self._is_cancelled = False
        self._is_finished = False  # 新增：标记线程是否完成
        
    def run(self):
        try:
            # 准备提示词
            template = SUGGESTION_TEMPLATES.get(get_prefs()['language'], SUGGESTION_TEMPLATES['en'])
            prompt = template.format(
                title=self.book_info.title,
                author=', '.join(self.book_info.authors) if self.book_info.authors else 'Unknown'
            )
            
            # 调用 API 获取建议
            suggestion = self.api.ask_stream(prompt)
            
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
    """处理生成建议的逻辑"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.response_area = None
        self.input_area = None
        self.suggest_button = None
        self.i18n = None
        self._worker = None
        self._loading_timer = None
        self._request_cancelled = False
        self._original_input = ''
        self._original_button_text = ''
        self._response_text = ''
        self.api = None
        self._cleanup_timer = None  # 新增：用于定期检查线程状态

    def setup(self, response_area, input_area, suggest_button, i18n, api):
        """设置处理器需要的UI组件和国际化文本"""
        self.response_area = response_area
        self.input_area = input_area
        self.suggest_button = suggest_button
        self.i18n = i18n
        self.api = api
        
        # 初始化状态
        self._request_cancelled = False
        self._loading_timer = None
        self._worker = None
        self._original_input = ''
        self._original_button_text = ''
        self._response_text = ''
        self._cleanup_timer = None

    def _setup_loading_animation(self):
        """设置加载动画定时器"""
        loading_text = self.i18n.get('loading_text', 'Loading')
        dots = ['', '.', '..', '...']
        current_dot = [0]

        def update_loading():
            # 只在非取消状态且没有响应时显示加载动画
            if not self._response_text and not self._request_cancelled:
                self.response_area.setText(f"{loading_text}{dots[current_dot[0]]}")
                current_dot[0] = (current_dot[0] + 1) % len(dots)

        self._loading_timer = QTimer(self)
        self._loading_timer.timeout.connect(update_loading)
        self._loading_timer.start(250)

    def _stop_loading_timer(self):
        """停止加载动画定时器"""
        if self._loading_timer and self._loading_timer.isActive():
            self._loading_timer.stop()
            self._loading_timer.deleteLater()
            self._loading_timer = None

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
        self.suggest_button.setEnabled(True)
        self.suggest_button.setText(self._original_button_text)
        self.suggest_button.setStyleSheet("")
        
        # 是否恢复原始输入
        if restore_input and self._original_input:
            self.input_area.setPlainText(self._original_input)

    def _on_suggestion_received(self, suggestion):
        """处理接收到的建议"""
        if not self._request_cancelled:
            self._stop_loading_timer()
            self._request_cancelled = True
            self._response_text = suggestion
            
            # 清空输出区域的加载动画
            self.response_area.clear()
            
            # 更新输入框内容
            self.input_area.setPlainText(suggestion)
            
            # 恢复按钮状态
            self._restore_ui_state()

    def _on_error(self, error):
        """处理错误"""
        if not self._request_cancelled:
            self._request_cancelled = True
            self._stop_loading_timer()
            
            # 先显示错误信息
            error_text = f"{self.i18n.get('error_prefix', 'Error: ')}{str(error)}"
            self.response_area.setText(error_text)
            
            # 恢复 UI 状态并保留原始输入
            self._restore_ui_state(restore_input=True)
            
            # 延迟显示请求失败状态
            def delayed_show_failed():
                if not self._response_text:  # 确保在这个时间点还没有响应
                    self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))
            
            QTimer.singleShot(2000, delayed_show_failed)

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
        """生成建议"""
        if not self.api or not book_info:
            return
            
        # 检查 auth token
        if not self.suggest_button.window()._check_auth_token():
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
        self.suggest_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                color: #666;
                padding: 2px 8px;
            }
        """)
        
        # 确保UI更新
        QApplication.processEvents()
        
        # 设置加载动画
        self._setup_loading_animation()
        
        # 创建并启动工作线程
        if self._worker:
            self._cleanup_worker()
            
        self._worker = SuggestionWorker(self.api, book_info)
        self._worker.result.connect(self._on_suggestion_received)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()
        
        # 设置超时检查
        QTimer.singleShot(2000, self._check_response_timeout)

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
