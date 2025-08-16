#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication
import markdown2
import bleach
import logging
import os
import sys
import time
from datetime import datetime
from threading import Thread

# 使用 Calibre 配置目录存储日志
from calibre.utils.config import config_dir

# 导入历史记录管理器
from .history_manager import HistoryManager

# 配置日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_grok_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_grok_response.log')

# 使用已配置的日志系统，不再重复配置根日志记录器
# 只创建当前模块的日志记录器

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
    # 新增流式响应的信号
    stream_update = pyqtSignal(str)

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
        self.history_manager = HistoryManager()
        self.current_metadata = None  # 存储当前书籍的元数据

    def setup(self, response_area, send_button, i18n, api, input_area=None):
        """
        设置处理器需要的UI组件和国际化文本
        
        Args:
            response_area: 显示响应的文本区域
            send_button: 发送按钮
            i18n: 国际化对象
            api: API 客户端
            input_area: 输入问题的文本区域
        """
        self.response_area = response_area
        self.send_button = send_button
        self.i18n = i18n
        self.api = api
        self.input_area = input_area  # 保存输入区域的引用

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
        """开始异步请求 API㕼可以处理普通请求和流式请求"""
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
        # 连接流式响应信号
        self._current_signals.stream_update.connect(self._handle_stream_update)
        logger.info(f"[Signal Connect] 信号连接完成, 耗时: {(time.time() - connect_start)*1000:.2f}ms")
        
        # 初始化流式响应相关变量
        self._init_stream_variables()
        
        def run_request():
            try:
                # 记录当前使用的 AI 模型
                try:
                    model_name = self.api.model_display_name
                    logger.info(f"[API Model] 当前使用的 AI 模型: {model_name}")
                except Exception as e:
                    logger.warning(f"[API Model] 获取模型信息失败: {str(e)}")
                
                logger.info(f"[API Request] 开始API请求, 时间: {time.strftime('%H:%M:%S')}")
                api_start = time.time()
                
                # 检查当前模型是否支持流式传输
                model_supports_streaming = hasattr(self.api._ai_model, 'supports_streaming') and self.api._ai_model.supports_streaming()
                streaming_enabled = self.api._ai_model.config.get('enable_streaming', True)  # 默认启用
                
                logger.info(f"[模型检测] 当前模型: {self.api.model_name}, 支持流式传输: {model_supports_streaming}, 启用流式传输: {streaming_enabled}")
                
                if model_supports_streaming and streaming_enabled:
                    # 使用流式请求
                    logger.info(f"[流式请求] 开始使用流式请求处理 {self.api.model_name} 模型")
                    
                    def stream_callback(chunk):
                        if not self._request_cancelled:
                            logger.info(f"[流式回调] 收到流式片段, 长度: {len(chunk)} 字符")
                            self._current_signals.stream_update.emit(chunk)
                    
                    # 调用API时传入回调函数
                    response = self.api.ask(prompt, stream=True, stream_callback=stream_callback)
                    logger.info(f"[流式请求完成] 收到完整响应, 长度: {len(response)} 字符")
                    
                    # 在流式请求完成后，发送完整响应
                    if not self._request_cancelled:
                        logger.info(f"[流式请求完成] 发送最终累积响应到UI, 长度: {len(self._stream_response)} 字符")
                        self._current_signals.update_ui.emit(self._stream_response, True)
                else:
                    # 使用普通请求
                    logger.info(f"[普通请求] 使用普通请求处理 {self.api.model_name} 模型")
                    response = self.api.ask(prompt)
                    if not self._request_cancelled:
                        self._current_signals.update_ui.emit(response, True)
                
                api_time = (time.time() - api_start) * 1000
                logger.info(f"[API Response] 收到API响应, 耗时: {api_time:.2f}ms")
                
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
        self._timeout_timer = QTimer()
        self._timeout_timer.setSingleShot(True)
        self._timeout_timer.timeout.connect(self._check_request_timeout)
        self._timeout_timer.start(360000)  # 增加超时时间到60秒
        logger.info(f"[Request Setup] 请求设置完成, 总耗时: {(time.time() - self._request_start_time)*1000:.2f}ms")
    
    # 初始化流式响应相关变量
    def _init_stream_variables(self):
        """初始化流式响应相关变量"""
        self._stream_response = ""
        self._stream_buffer = ""
        self._last_update_time = 0
        self._update_interval = 0.1  # 100ms更新间隔
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_stream_buffer)
    
    def _handle_stream_update(self, chunk):
        """处理流式响应更新
        
        :param chunk: 流式响应片段
        """
        logger.info(f"[Stream Update] 收到流式响应片段: {len(chunk)} 字符")
        
        if not chunk or self._request_cancelled:
            logger.warning("[Stream Update] 片段为空或请求已取消，忽略此片段")
            return
        
        # 初始化流式响应变量（如果还没有初始化）
        if not hasattr(self, '_update_timer'):
            self._init_stream_variables()
            
        # 累积响应内容
        self._stream_response += chunk
        self._stream_buffer += chunk
        logger.info(f"[Stream Update] 当前累积响应长度: {len(self._stream_response)} 字符")
        
        # 停止加载动画，因为我们已经开始收到响应
        self._stop_loading_timer()
        
        # 控制更新频率，避免闪烁
        current_time = time.time()
        if current_time - self._last_update_time >= self._update_interval:
            # 如果超过更新间隔，立即处理
            self._process_stream_buffer()
        else:
            # 否则设置定时器延迟处理
            if not self._update_timer.isActive():
                remaining_time = int((self._last_update_time + self._update_interval - current_time) * 1000)
                self._update_timer.start(max(10, remaining_time))  # 至少10ms
    
    def _process_stream_buffer(self):
        """处理累积的流式响应缓冲区"""
        if not self._stream_buffer or self._request_cancelled:
            return
            
        logger.info(f"[Stream Process] 处理缓冲区内容, 长度: {len(self._stream_buffer)} 字符")
        self._stream_buffer = ""  # 清空缓冲区
        self._last_update_time = time.time()
        
        try:
            # 使用markdown2转换完整的累积响应为HTML
            html = markdown2.markdown(
                self._stream_response,
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
            
            # 更新UI
            self._set_html_response(safe_html)
            
            # 停止加载动画，因为我们已经开始收到响应
            self._stop_loading_timer()
            
        except Exception as e:
            logger.error(f"[Stream Update] 处理流式响应时出错: {str(e)}")
    
    def _check_request_timeout(self):
        """检查请求是否超时"""
        if hasattr(self, '_request_start_time') and self._request_start_time and not self._request_cancelled:
            elapsed = time.time() - self._request_start_time
            if elapsed > 360:  # 60秒超时
                self.handle_error("Request took too long, automatically terminated", "timeout")
    
    def _cleanup_request(self):
        """清理请求资源"""
        # 取消超时检查定时器
        if hasattr(self, '_timeout_timer') and self._timeout_timer is not None:
            self._timeout_timer.stop()
            self._timeout_timer = None
            
        # 断开信号连接
        if hasattr(self, '_current_signals'):
            try:
                self._current_signals.update_ui.disconnect()
                self._current_signals.error_occurred.disconnect()
                self._current_signals.request_finished.disconnect()
                # 断开流式响应信号
                self._current_signals.stream_update.disconnect()
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
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed'))

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
        request_failed = self.i18n.get('request_failed', 'Request failed')
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
        logger.info(f"[Set HTML] 更新UI显示, HTML长度: {len(html)} 字符")
        try:
            # 设置HTML内容
            self.response_area.setHtml(html)
            self.response_area.setAlignment(Qt.AlignLeft)
            
            # 滚动到文档底部，显示最新内容
            scrollbar = self.response_area.verticalScrollBar()
            if scrollbar:
                scrollbar.setValue(scrollbar.maximum())
            
            # 强制更新UI
            QApplication.processEvents()
            logger.info("[Set HTML] UI更新成功，已滚动到最新内容")
        except Exception as e:
            logger.error(f"[Set HTML] 更新UI时出错: {str(e)}")


    def _update_ui_from_signal(self, text, is_response, is_history=False):
        """通过信号更新UI，确保在主线程中执行
        
        :param text: 要显示的文本
        :param is_response: 是否为最终响应
        :param is_history: 是否来自历史记录
        """
        import time
        update_start = time.time()
        logger.info(f"[UI Update] 开始更新UI, 时间: {time.strftime('%H:%M:%S')}")
        
        if is_response:
            # 如果是最终响应，设置Markdown响应
            md_start = time.time()
            self.set_markdown_response(text)
            logger.info(f"[Markdown Process] Markdown处理完成, 耗时: {(time.time() - md_start)*1000:.2f}ms")
            
            # 如果不是从历史记录加载的，保存到历史记录
            if not is_history and hasattr(self, 'current_metadata') and self.current_metadata:
                try:
                    question = self.input_area.toPlainText()
                    self.history_manager.save_history(
                        self.current_metadata,
                        question,
                        text
                    )
                    logger.info("成功保存问询历史")
                except Exception as e:
                    logger.error(f"保存问询历史失败: {str(e)}")
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