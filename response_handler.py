#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor
import markdown2
import bleach
import logging

logger = logging.getLogger(__name__)

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
                html = html.replace('<br />', '')
                safe_html = bleach.clean(html, tags=['p', 'strong', 'em', 'h1', 'h2', 'h3', 'pre', 'code', 'blockquote', 'table', 'tr', 'th', 'td', 'ul', 'ol', 'li'], attributes=['id'])
                self.result.emit(safe_html)
        except Exception:
            pass  # 忽略取消状态下的错误

    def cancel(self):
        """标记取消状态，让线程自然结束"""
        self._is_cancelled = True



class ResponseHandler(QObject):
    stop_time_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        #连接信号到停止方法
        self.stop_time_signal.connect(self._stop_loading_timer)

        self.response_area = None
        self.send_button = None
        self.i18n = None
        self._response_text = ''
        self._request_cancelled = False
        self._loading_timer = None
        self.api = None
        self._markdown_worker = None
        self.signal = None

    def setup(self, response_area, send_button, i18n, api):
        """设置处理器需要的UI组件和国际化文本"""
        self.response_area = response_area
        self.send_button = send_button
        self.i18n = i18n
        self.api = api

    def update_i18n(self, i18n):
        """更新国际化文本对象"""
        self.i18n = i18n
        # 更新按钮文本
        if self.send_button.isEnabled():
            self.send_button.setText(self.i18n.get('send', 'Send'))

    def start_request(self, prompt):
        """开始一个新的请求，使用非流式 API"""
        # 确保清理之前的请求
        self.cleanup()
        
        # 保存原始状态
        self._original_button_text = self.i18n.get('send', 'Send')
        
        # 更新UI状态 - 通过信号在主线程中更新
        self.signal.update_ui.emit(self.i18n.get('sending', 'Sending...'), False)
        
        self._response_text = ''
        self._request_cancelled = False
        self._is_loading = True  # 开始加载
    
        try:
            # 发送请求
            response = self.api.ask(prompt)
            
            # 停止加载动画
            self._stop_loading_timer()
            self._is_loading = False  # 停止加载
            
            # 更新响应区域 - 通过信号在主线程中更新
            self._response_text = response
            self.signal.update_ui.emit(response, True)
            
        except Exception as e:
            self._stop_loading_timer()
            self._is_loading = False  # 停止加载
            self.signal.error_occurred.emit(str(e))
        finally:
            # 恢复按钮状态 - 通过信号在主线程中更新
            self.signal.request_finished.emit()

    def start_async_request(self, prompt):
        """开始异步请求 API"""
        from threading import Thread
        from PyQt5.QtCore import pyqtSignal, QObject
        
        # 定义一个信号类用于线程间通信
        class Signal(QObject):
            update_ui = pyqtSignal(str, bool)
            error_occurred = pyqtSignal(str)
            request_finished = pyqtSignal()
        
        self.signal = Signal()
        self.signal.update_ui.connect(self._update_ui_from_signal)
        self.signal.error_occurred.connect(self.handle_error)
        self.signal.request_finished.connect(self._restore_button_state)
        
        thread = Thread(target=self.start_request, args=(prompt,))
        thread.start()
        # 立即显示加载动画
        self._setup_loading_animation()

    def prepare_close(self):
        if self._markdown_worker:
            self._markdown_worker.cancel()

    def cleanup(self):
        """清理资源并重置状态"""
        self._stop_all_timers()
            
        if self._markdown_worker:
            self._markdown_worker.cancel()
            self._markdown_worker.deleteLater()
            self._markdown_worker = None
            
        self.send_button.setEnabled(True)

    def _stop_all_timers(self):
        """停止所有定时器"""
        # self._stop_loading_timer()
        self.stop_time_signal.emit()
        
    def _setup_loading_animation(self, mode='requesting'):
        """设置加载动画定时器
        
        :param mode: 动画模式，'requesting' 或 'formatting'
        """
        self._loading_texts = {
            'requesting': self.i18n.get('requesting', 'Requesting, please wait'),
            'formatting': self.i18n.get('formatting', 'Request successful, formatting')
        }
        self._animation_dots = ['', '.', '..', '...']
        self._animation_dot_index = 0
        self._animation_mode = mode

        def update_loading():
            if not self._request_cancelled:
                base_text = self._loading_texts[self._animation_mode]
                self.response_area.setHtml(f"""
                    <div style="
                        text-align: left;
                        color: palette(text);
                        font-size: 15px;
                        margin-top: 10px;
                        font-family: -apple-system, 'Segoe UI', 'Ubuntu', 'PingFang SC', 'Microsoft YaHei', sans-serif;
                    ">
                        {base_text}{self._animation_dots[self._animation_dot_index]}
                    </div>
                """)
                self._animation_dot_index = (self._animation_dot_index + 1) % len(self._animation_dots)

        # 停止之前的定时器
        self._stop_loading_timer()
        
        self._loading_timer = QTimer(self)
        self._loading_timer.timeout.connect(update_loading)
        self._loading_timer.start(250)
        # 立即更新一次
        update_loading()


    def _stop_loading_timer(self):
        """停止加载动画定时器"""
        if self._loading_timer:
            if self._loading_timer.isActive():
                self._loading_timer.stop()
            self._loading_timer.deleteLater()
            self._loading_timer = None
            
    def _show_request_failed(self):
        """显示请求失败状态"""
        if self.response_area and not self._response_text:
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please check your network'))

    def handle_error(self, error_msg):
        """处理错误信息"""
        self._stop_loading_timer()
        error_prefix = self.i18n.get('error_prefix', 'Error: ')
        request_failed = self.i18n.get('request_failed', 'Request failed, please check your network')
        
        # 显示错误信息
        self.response_area.setHtml(f"""
            <div style="
                color: #cc0000;
                font-size: 13px;
                margin-top: 10px;
                font-family: -apple-system, 'Segoe UI', 'Ubuntu', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            ">
                {error_prefix}{request_failed}<br>
                {error_msg}
            </div>
        """)
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

    def _update_ui_from_signal(self, text, is_response):
        """通过信号更新UI，确保在主线程中执行
        
        :param text: 要显示的文本
        :param is_response: 是否为最终响应
        """
        if is_response:
            # 如果是最终响应，设置Markdown响应
            self.set_markdown_response(text)
            return
            
        # 处理非响应状态（如加载中）
        self.send_button.setText(text)
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                color: palette(text);
                padding: 2px 8px;
                width: auto;
                height: auto;
            }
            QPushButton:hover:enabled {
                background-color: palette(midlight);
            }
            QPushButton:pressed {
                background-color: palette(midlight);
                color: white;
            }
        """)
        self.send_button.setEnabled(False)
        
        # 根据文本内容判断当前状态
        if text == self.i18n.get('sending', 'Sending...'):
            # 发送中的状态
            self._setup_loading_animation('requesting')
        elif not self._request_cancelled:
            # 其他非取消状态，如格式化中
            self._setup_loading_animation('formatting')
        else:
            # 请求已取消，停止加载动画
            self._stop_loading_timer()

    def _restore_button_state(self):
        """恢复按钮状态，确保在主线程中执行"""
        self.send_button.setEnabled(True)
        if hasattr(self, 'i18n') and self.i18n is not None:
            self.send_button.setText(self.i18n.get('send_button', 'Send'))
        else:
            self.send_button.setText('Send')
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                padding: 2px 8px;
            }
            QPushButton:disabled {
                color: #ccc;
            }
            QPushButton:hover:enabled {
                background-color: palette(midlight);
            }
            QPushButton:pressed {
                background-color: palette(midlight);
                color: white;
            }   
        """)