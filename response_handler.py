#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor
import markdown2
import bleach

class MarkdownWorker(QThread):
    result = pyqtSignal(str)

    def __init__(self, text, parent=None):
        super().__init__(None)  # 不设置父对象，避免随父对象一起销毁
        self.text = text
        self._is_cancelled = False

    def run(self):
        if self._is_cancelled:
            return
        try:
            html = markdown2.markdown(self.text, extras=['fenced-code-blocks', 'tables', 'break-on-newline', 'header-ids', 'strike', 'task_list', 'markdown-in-html'])
            if not self._is_cancelled:
                safe_html = bleach.clean(html, tags=['p', 'strong', 'em', 'h1', 'h2', 'h3', 'pre', 'code', 'blockquote', 'table', 'tr', 'th', 'td', 'ul', 'ol', 'li'], attributes=['id'])
                self.result.emit(safe_html)
        except Exception:
            pass  # 忽略取消状态下的错误

    def cancel(self):
        """标记取消状态，让线程自然结束"""
        self._is_cancelled = True

class StreamWorker(QThread):
    chunk_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, api, prompt, parent=None):
        super().__init__(None)  # 不设置父对象，避免随父对象一起销毁
        self.api = api
        self.prompt = prompt
        self._is_cancelled = False

    def run(self):
        try:
            for chunk in self.api.ask_stream(self.prompt):
                if self._is_cancelled:
                    return  # 立即返回，不发送完成信号
                self.chunk_received.emit(chunk)
        except Exception as e:
            if not self._is_cancelled:
                self.error_occurred.emit(str(e))
        if not self._is_cancelled:  # 只在非取消状态下发送完成信号
            self.finished.emit()

    def cancel(self):
        """标记取消状态，让线程自然结束"""
        self._is_cancelled = True

class ResponseHandler(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.response_area = None
        self.send_button = None
        self.i18n = None
        self._response_text = ''
        self._new_chunks = []
        self._request_cancelled = False
        self._loading_timer = None
        self._update_timer = None
        self._stream_worker = None
        self.api = None
        self._markdown_worker = None

    def setup(self, response_area, send_button, i18n, api):
        """设置处理器需要的UI组件和国际化文本"""
        self.response_area = response_area
        self.send_button = send_button
        self.i18n = i18n
        self.api = api

    def start_request(self, prompt):
        """开始一个新的请求，初始化状态和定时器"""
        # 确保清理之前的请求
        self.cleanup()
        
        self.send_button.setEnabled(False)
        self._response_text = ''
        self._new_chunks = []
        self._request_cancelled = False

        # 设置加载动画
        self._setup_loading_animation()

        # 创建并启动流式响应工作线程
        self._stream_worker = StreamWorker(self.api, prompt)  # 不设置父对象
        self._stream_worker.chunk_received.connect(self._on_chunk_received)
        self._stream_worker.error_occurred.connect(self.handle_error)
        self._stream_worker.finished.connect(self._on_stream_finished)
        
        # 设置请求超时
        QTimer.singleShot(2000, self._check_response_timeout)
        
        # 启动工作线程
        self._stream_worker.start()

    def _check_response_timeout(self):
        """检查是否超时"""
        if not self._response_text and not self._request_cancelled:
            self._request_cancelled = True
            if self._stream_worker:
                self._stream_worker.cancel()
            # 直接显示请求失败状态，不需要显示超时错误
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))
            self.send_button.setEnabled(True)

    def _on_chunk_received(self, chunk):
        """处理接收到的数据块"""
        if self._request_cancelled:
            return
            
        # 如果是第一个数据块，停止加载动画并开始更新定时器
        first_chunk = not self._response_text and not self._new_chunks
        if first_chunk:
            self._stop_loading_timer()
            self._start_update_timer()
        
        # 将新chunk添加到缓冲区
        self._new_chunks.append(chunk)

    def _start_update_timer(self):
        """启动更新定时器"""
        if not self._update_timer:
            self._update_timer = QTimer(self)
            self._update_timer.timeout.connect(self._update_response_area)
            self._update_timer.start(100)

    def _stop_loading_timer(self):
        """停止加载动画定时器"""
        if self._loading_timer and self._loading_timer.isActive():
            self._loading_timer.stop()
            self._loading_timer.deleteLater()
            self._loading_timer = None

    def _stop_update_timer(self):
        """停止更新定时器"""
        if self._update_timer and self._update_timer.isActive():
            self._update_timer.stop()
            self._update_timer.deleteLater()
            self._update_timer = None

    def _stop_all_timers(self):
        """停止所有定时器"""
        self._stop_loading_timer()
        self._stop_update_timer()

    def _on_stream_finished(self):
        """流式响应完成处理"""
        if not self._request_cancelled:
            self._update_response_area()  # 确保最后的内容被更新
            if self._response_text:
                self.set_markdown_response(self._response_text)
        
        # 只清理定时器和状态，不清理线程
        self._stop_all_timers()
        self.send_button.setEnabled(True)

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

    def _update_response_area(self):
        """更新响应区域，只更新新到达的内容"""
        if not self._new_chunks:
            return
            
        try:
            # 获取文本光标
            cursor = self.response_area.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            
            # 只插入新的数据块
            new_text = ''.join(self._new_chunks)
            cursor.insertText(new_text)
            self.response_area.setTextCursor(cursor)
            self.response_area.ensureCursorVisible()
            self.response_area.setAlignment(Qt.AlignLeft)  # 确保文本左对齐
            
            # 更新总响应文本并清空新数据块缓冲区
            self._response_text += new_text
            self._new_chunks = []
            
            # 如果响应区域内容过长，可以考虑清理旧内容
            if len(self._response_text) > 50000:  # 如果超过50KB
                self._response_text = self._response_text[-50000:]
                self.response_area.setPlainText(self._response_text)
                self.response_area.setAlignment(Qt.AlignLeft)  # 重设对齐
        except Exception as e:
            self.handle_error(f"更新显示失败: {str(e)}")

    def prepare_close(self):
        """准备关闭，清理资源但不影响线程运行"""
        self._stop_all_timers()
        self._request_cancelled = True
        
        # 只标记取消，让线程自然结束
        if self._stream_worker:
            self._stream_worker.cancel()
            
        if self._markdown_worker:
            self._markdown_worker.cancel()

    def cleanup(self):
        """清理资源并重置状态"""
        self._stop_all_timers()
        self._request_cancelled = True
        
        # 标记线程取消并清理
        if self._stream_worker:
            self._stream_worker.cancel()
            self._stream_worker.deleteLater()
            self._stream_worker = None
            
        if self._markdown_worker:
            self._markdown_worker.cancel()
            self._markdown_worker.deleteLater()
            self._markdown_worker = None
            
        self.send_button.setEnabled(True)

    def _show_request_failed(self):
        """显示请求失败状态"""
        if self.response_area and not self._response_text:
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))

    def handle_error(self, error):
        """处理错误情况"""
        if not self._request_cancelled:
            self._request_cancelled = True
            self._stop_all_timers()
            
            # 先显示错误信息
            error_text = f"{self.i18n.get('error_prefix', 'Error: ')}{str(error)}"
            self.response_area.setText(error_text)
            
            # 延迟显示请求失败状态
            def delayed_show_failed():
                if not self._response_text:  # 确保在这个时间点还没有响应
                    self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))
            
            QTimer.singleShot(2000, delayed_show_failed)
            self.send_button.setEnabled(True)

    def set_response(self, text):
        """设置响应文本（兼容旧接口）"""
        if not text:
            self.response_area.setText(self.i18n.get('no_response', 'No response'))
            return
        self.response_area.setPlainText(text)
        self.response_area.setAlignment(Qt.AlignLeft)

    def set_markdown_response(self, text):
        """将Markdown文本异步转换为HTML并显示"""
        if not text:
            self.response_area.setText(self.i18n.get('no_response', 'No response'))
            return
            
        self._stop_all_timers()  # 停止加载动画
        
        # 只标记取消，让线程自然结束
        if self._markdown_worker:
            self._markdown_worker.cancel()
            
        self._markdown_worker = MarkdownWorker(text)  # 不设置父对象
        self._markdown_worker.result.connect(self._set_html_response)
        self._markdown_worker.finished.connect(self._on_markdown_finished)
        self._markdown_worker.start()

    def _on_markdown_finished(self):
        """Markdown 渲染完成的处理"""
        if self._markdown_worker:
            self._markdown_worker.deleteLater()
            self._markdown_worker = None

    def _set_html_response(self, html):
        """设置HTML响应并确保正确的样式"""
        self.response_area.setHtml(html)
        self.response_area.setAlignment(Qt.AlignLeft)