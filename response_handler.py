#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
import markdown2
import bleach
import logging
import os
import sys
from threading import Thread
from PyQt5.QtCore import pyqtSignal, QObject
import time

# 使用 Calibre 配置目录存储日志
from calibre.utils.config import config_dir

# 配置日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_grok_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_grok_response.log')

# 获取根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# 检查是否已经添加过处理器，避免重复添加
if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file for h in root_logger.handlers):
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到根日志记录器
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info('=' * 80)
logger.info('Response Handler 初始化完成')

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
            # 使用markdown2转换markdown为HTML
            html = markdown2.markdown(
                self.text,
                extras=[
                    'fenced-code-blocks',
                    'tables',
                    'break-on-newline',
                    'header-ids',
                    'strike',
                    'task_list',
                    'markdown-in-html'
                ]
            )
            
            if self._is_cancelled:
                return
                
            # 清理HTML，允许表格相关标签
            allowed_tags = [
                'p', 'br', 'strong', 'em', 'b', 'i', 'u', 's',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'pre', 'code', 'blockquote',
                'table', 'thead', 'tbody', 'tr', 'th', 'td',
                'ul', 'ol', 'li',
                'a', 'img', 'div', 'span'
            ]
            
            allowed_attrs = {
                'a': ['href', 'title', 'target'],
                'img': ['src', 'alt', 'title'],
                'th': ['align'],
                'td': ['align'],
                '*': ['class', 'id', 'style']
            }
            
            # 清理HTML
            safe_html = bleach.clean(
                html,
                tags=allowed_tags,
                attributes=allowed_attrs,
                strip=True
            )
            
            if not self._is_cancelled:
                self.result.emit(safe_html)
                
        except Exception as e:
            logger.error(f"Markdown渲染错误: {str(e)}")
            if not self._is_cancelled:
                self.result.emit(f'<div class="error">渲染Markdown时出错: {str(e)}</div>')

    def cancel(self):
        """标记取消状态，让线程自然结束"""
        self._is_cancelled = True

# 在类外部或类级别定义信号类
class ResponseSignals(QObject):
    update_ui = pyqtSignal(str, bool)
    error_occurred = pyqtSignal(str, str)
    request_finished = pyqtSignal()

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
        self.signal = ResponseSignals()

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
            # 直接传递异常对象，而不是字符串
            self.signal.error_occurred.emit(e)
        finally:
            # 恢复按钮状态 - 通过信号在主线程中更新
            self.signal.request_finished.emit()

    def start_async_request(self, prompt):
        """开始异步请求 API"""
        self._request_start_time = time.time()
        logger.info(f"[Request Start] 开始处理请求, 时间: {time.strftime('%H:%M:%S')}")
        
        # 清理之前的请求状态
        start_cleanup = time.time()
        self.cleanup()
        logger.info(f"[Cleanup] 清理完成, 耗时: {(time.time() - start_cleanup)*1000:.2f}ms")
        
        # 创建新的信号对象，避免信号重复连接
        self._current_signals = ResponseSignals()
        
        # 连接信号
        connect_start = time.time()
        self._current_signals.update_ui.connect(self._update_ui_from_signal)
        self._current_signals.error_occurred.connect(self.handle_error)
        self._current_signals.request_finished.connect(self._cleanup_request)
        logger.info(f"[Signal Connect] 信号连接完成, 耗时: {(time.time() - connect_start)*1000:.2f}ms")
        
        def run_request():
            try:
                logger.info(f"[API Request] 开始API请求, 时间: {time.strftime('%H:%M:%S')}")
                api_start = time.time()
                response = self.api.ask(prompt)
                api_time = (time.time() - api_start) * 1000
                logger.info(f"[API Response] 收到API响应, 耗时: {api_time:.2f}ms")
                
                if not self._request_cancelled:
                    emit_start = time.time()
                    self._current_signals.update_ui.emit(response, True)
                    logger.info(f"[Emit UI Update] 发送UI更新信号, 耗时: {(time.time() - emit_start)*1000:.2f}ms")
            except Exception as e:
                error_time = time.strftime('%H:%M:%S')
                logger.error(f"[API Error] 请求出错, 时间: {error_time}, 错误: {str(e)}")
                if not self._request_cancelled:
                    error_type = getattr(e, 'error_type', 'unknown')
                    error_msg = str(e) or str(type(e).__name__)
                    self._current_signals.error_occurred.emit(error_msg, error_type)
            finally:
                if not self._request_cancelled:
                    self._current_signals.request_finished.emit()
                logger.info(f"[Request Finished] 请求处理完成, 总耗时: {(time.time() - self._request_start_time)*1000:.2f}ms")
        
        # 启动请求线程
        thread_start = time.time()
        self._request_thread = Thread(target=run_request)
        self._request_thread.daemon = True
        self._request_cancelled = False
        self._request_thread.start()
        logger.info(f"[Thread Start] 启动请求线程, 耗时: {(time.time() - thread_start)*1000:.2f}ms")
        
        # 设置加载动画
        self._setup_loading_animation()
        
        # 设置超时检查
        QTimer.singleShot(30000, self._check_request_timeout)
        logger.info(f"[Request Setup] 请求设置完成, 总耗时: {(time.time() - self._request_start_time)*1000:.2f}ms")
    
    def _check_request_timeout(self):
        """检查请求是否超时"""
        if hasattr(self, '_request_thread') and self._request_thread.is_alive():
            self._request_cancelled = True
            self.handle_error(self.i18n.get('request_timeout', 'Request timeout, please try again later'))
    
    def _cleanup_request(self):
        """清理请求资源"""
        # 断开信号连接
        if hasattr(self, '_current_signals'):
            try:
                self._current_signals.update_ui.disconnect()
                self._current_signals.error_occurred.disconnect()
                self._current_signals.request_finished.disconnect()
            except:
                pass
            self._current_signals = None
        
        # 恢复按钮状态
        self._restore_button_state()
        
        # 停止加载动画
        self._stop_loading_timer()

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
                        font-size: 13px;
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
        self._loading_timer.start(300)  # 每300毫秒更新一次
        
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
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed, please try again later'))

    def _format_error_html(self, title, message, error_type='default'):
        """格式化错误信息为HTML
        
        Args:
            title: 错误标题
            message: 错误详细信息
            error_type: 错误类型，可选值：'default', 'auth', 'api'
            
        Returns:
            str: 格式化后的HTML字符串
        """
        # 基础样式
        base_style = """
            color: palette(text);
            font-size: 13px;
            margin: 15px 0;
            padding: 10px;
            font-family: -apple-system, 'Segoe UI', 'Ubuntu', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        """
        
        # 根据错误类型添加特定样式
        if error_type == 'auth':
            style = base_style + """
                background-color: #ffebee;
                border-radius: 4px;
                border-left: 4px solid #d32f2f;
            """
        else:  # default and other types
            style = base_style + """
                text-align: left;
            """
        
        # 构建HTML
        error_html = f"""
            <div style="{style}">
                {title}<br><br>
                {message}
            </div>
        """
        
        # 如果是认证错误，添加额外提示
        if error_type == 'auth':
            auth_tip = self.i18n.get('invalid_token', 'Please check your API token validable in the plugin settings.') \
                     if hasattr(self.i18n, 'get') else 'Please check your API token validable in the plugin settings.'
            error_html += f"""
                <div style="margin-top: 15px; color: #666; font-size: 12px;">
                    {auth_tip}
                </div>
            """
            
        return error_html

    def handle_error(self, error_msg, error_type='unknown'):
        """处理错误信息
        
        Args:
            error_msg: 错误信息，可以是字符串或异常对象
            error_type: 错误类型，如 'auth_error', 'api_error' 等
        """
        self._stop_loading_timer()
        
        # 获取本地化错误信息
        error_prefix = self.i18n.get('error', 'Error: ')
        request_failed = self.i18n.get('request_failed', 'Request failed, please try again later')
        invalid_token = self.i18n.get('invalid_token', 'Invalid token. Please check your API token validable in settings.')
        
        # 处理错误信息
        error_str = str(error_msg)
        
        # 根据错误类型设置标题和错误类型
        if error_type == 'auth_error' or (hasattr(error_msg, 'error_type') and error_msg.error_type == 'auth_error'):
            title = self.i18n.get('auth_error_title', 'Authentication Error')
            error_type = 'auth'
            message = error_str if error_str else invalid_token
        elif 'template_error' in error_str:
            title = error_str
            message = ""
            error_type = 'default'
        else:
            title = f"{error_prefix}{request_failed}"
            message = error_str if error_str != title else ""
            error_type = 'api' if error_type == 'unknown' else error_type
        
        # 生成错误HTML
        error_html = self._format_error_html(
            title=title,
            message=message,
            error_type=error_type
        )
        
        # 更新UI
        if self.response_area:
            self.response_area.setHtml(error_html)
        
        # 恢复按钮状态
        self.send_button.setEnabled(True)
        if hasattr(self, 'i18n') and self.i18n is not None:
            self.send_button.setText(self.i18n.get('send_button', 'Send'))
        else:
            self.send_button.setText('Send')

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
        import time
        update_start = time.time()
        logger.info(f"[UI Update] 开始更新UI, 时间: {time.strftime('%H:%M:%S')}")
        
        if is_response:
            # 如果是最终响应，设置Markdown响应
            md_start = time.time()
            self.set_markdown_response(text)
            logger.info(f"[Markdown Process] Markdown处理完成, 耗时: {(time.time() - md_start)*1000:.2f}ms")
            return
            
        # 处理非响应状态（如加载中）
        self.send_button.setText(text)
        self.send_button.setStyleSheet("""
            QPushButton {
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                min-width: 80px;
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
                color: palette(text);
                padding: 2px 12px;
                min-height: 1.2em;
                max-height: 1.2em;
                min-width: 80px;
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