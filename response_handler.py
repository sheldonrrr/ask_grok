#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication
import logging
import os
import sys
import time
from datetime import datetime
from threading import Thread

# 从 vendor 命名空间导入第三方库
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import markdown2
from calibre_plugins.ask_ai_plugin.lib.ask_ai_plugin_vendor import bleach

# 使用 Calibre 配置目录存储日志
from calibre.utils.config import config_dir

# 导入历史记录管理器
from .history_manager import HistoryManager

# 导入UI常量
from .ui_constants import FONT_SIZE_MEDIUM

# 配置日志目录
log_dir = os.path.join(config_dir, 'plugins', 'ask_ai_plugin_logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ask_ai_plugin_response.log')

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
    
    def _process_think_tags(self, text):
        """处理推理模型的 think 标签，将其转换为特殊样式的 HTML
        
        使用占位符策略避免 markdown2 转义 HTML 标签
        """
        import re
        import html
        
        # 存储 think 内容的列表
        think_blocks = []
        
        # 查找所有 <think>...</think> 标签
        def extract_think(match):
            think_content = match.group(1)
            # 转义 HTML 特殊字符
            escaped_content = html.escape(think_content)
            think_blocks.append(escaped_content)
            # 返回占位符（使用 HTML 注释格式）
            return f'<!--THINK_BLOCK_{len(think_blocks)-1}-->'
        
        # 替换所有 <think>...</think> 标签为占位符
        processed_text = re.sub(r'<think>(.*?)</think>', extract_think, text, flags=re.DOTALL)
        
        return processed_text, think_blocks

    def run(self):
        if self._is_cancelled:
            return
        try:
            # 处理推理模型的 think 标签，获取占位符文本和 think 块列表
            text_to_convert, think_blocks = self._process_think_tags(self.text)
            
            # 使用markdown2转换markdown为HTML
            html = markdown2.markdown(
                text_to_convert,
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
            
            # 将占位符替换回 think 块的 HTML
            for i, think_content in enumerate(think_blocks):
                think_html = f'<div class="reasoning-process" style="background-color: #f0f8ff; border-left: 4px solid #4a90e2; padding: 12px; margin: 10px 0; border-radius: 4px; font-size: 0.9em; color: #555;"><div style="font-weight: bold; color: #4a90e2; margin-bottom: 8px;">[推理过程]</div><div style="white-space: pre-wrap; font-family: monospace;">{think_content}</div></div>'
                html = html.replace(f'<!--THINK_BLOCK_{i}-->', think_html)
            
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
        
        # 智能滚动控制变量
        self._user_is_scrolling = False  # 用户是否正在主动滚动
        self._last_scroll_value = 0  # 上次滚动位置
        self._scroll_resume_timer = None  # 恢复自动滚动的定时器
        self._last_html_update_time = 0  # 上次HTML更新时间
    
    def _process_think_tags_for_stream(self, text):
        """处理流式响应中的 think 标签
        
        使用占位符策略：
        1. 先将 <think> 标签替换为占位符
        2. Markdown 转换
        3. 将占位符替换回 HTML
        """
        import re
        import html
        
        # 存储 think 内容的列表
        think_blocks = []
        
        # 查找所有完整的 <think>...</think> 标签
        def extract_think(match):
            think_content = match.group(1)
            # 不转义内容，保留原始 Markdown 格式
            think_blocks.append(think_content)
            # 返回占位符（使用 HTML 注释格式，markdown2 不会处理）
            return f'<!--THINK_BLOCK_{len(think_blocks)-1}-->'
        
        # 替换所有完整的 <think>...</think> 标签为占位符
        processed_text = re.sub(r'<think>(.*?)</think>', extract_think, text, flags=re.DOTALL)
        
        # 只在有新的 think 块时记录日志
        if think_blocks and not hasattr(self, '_last_think_count'):
            self._last_think_count = 0
        
        if think_blocks and len(think_blocks) != self._last_think_count:
            logger.info(f"[Process Think Tags] 提取 {len(think_blocks)} 个 think 块，总长度: {sum(len(b) for b in think_blocks)} 字符")
            self._last_think_count = len(think_blocks)
        
        # 处理未完成的 <think> 标签（流式传输中可能出现）
        if '<think>' in processed_text and '</think>' not in processed_text[processed_text.rfind('<think>'):]:
            # 找到最后一个未闭合的 <think>
            last_think_pos = processed_text.rfind('<think>')
            before_think = processed_text[:last_think_pos]
            think_content = processed_text[last_think_pos + 7:]  # 7 = len('<think>')
            
            # 保存未完成的 think 内容（不转义，保留 Markdown 格式）
            think_blocks.append(think_content)
            processed_text = before_think + f'<!--THINK_BLOCK_INCOMPLETE_{len(think_blocks)-1}-->'
        
        # 返回处理后的文本和 think 块列表
        return processed_text, think_blocks

    def setup(self, response_area, send_button, i18n, api, input_area=None, stop_button=None):
        """设置处理器需要的UI组件和国际化文本
        
        Args:
            response_area: 显示响应的文本区域
            send_button: 发送按钮
            i18n: 国际化对象
            api: API 客户端
            input_area: 输入问题的文本区域
            stop_button: 停止按钮
        """
        self.response_area = response_area
        self.send_button = send_button
        self.stop_button = stop_button
        self.i18n = i18n
        self.api = api
        self.input_area = input_area  # 保存输入区域的引用
        
        # 连接滚动条信号以检测用户滚动
        scrollbar = self.response_area.verticalScrollBar()
        if scrollbar:
            scrollbar.valueChanged.connect(self._on_scroll_value_changed)

    def update_i18n(self, i18n):
        """更新国际化文本对象"""
        self.i18n = i18n
        # 更新按钮文本
        if self.send_button.isEnabled():
            self.send_button.setText(self.i18n.get('send', 'Send'))
    
    def cancel_request(self):
        """取消当前请求"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("[Cancel Request] 用户请求取消当前请求")
        
        # 设置取消标志
        self._request_cancelled = True
        
        # 停止加载动画
        self._stop_loading_timer()
        
        # 如果有正在运行的请求线程，等待它结束
        if hasattr(self, '_request_thread') and self._request_thread and self._request_thread.is_alive():
            logger.info("[Cancel Request] 等待请求线程结束...")
            # 不要调用 join()，让线程自然结束
        
        # 清理资源
        self._cleanup_request()
        
        logger.info("[Cancel Request] 请求已取消")

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

    def start_async_request(self, prompt, model_id=None):
        """开始异步请求 API，可以处理普通请求和流式请求
        
        Args:
            prompt: 提示词
            model_id: 可选，指定使用的模型ID。如果为None，使用当前选中的模型
        """
        self._request_start_time = time.time()
        logger.info(f"[Request Start] 开始处理请求, 时间: {time.strftime('%H:%M:%S')}, model_id: {model_id}")
        
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
                
                # 如果指定了model_id，需要临时切换模型来检测流式支持
                original_model = None
                original_model_name = None
                if model_id and model_id != self.api._model_name:
                    logger.info(f"[流式检测] 临时切换模型以检测流式支持: {self.api._model_name} -> {model_id}")
                    original_model = self.api._ai_model
                    original_model_name = self.api._model_name
                    self.api._switch_to_model(model_id)
                
                # 检查当前模型是否支持流式传输
                # 首先检查模型是否已加载
                if not self.api._ai_model:
                    raise Exception("AI model not loaded. Please check your configuration.")
                
                model_supports_streaming = hasattr(self.api._ai_model, 'supports_streaming') and self.api._ai_model.supports_streaming()
                streaming_enabled = self.api._ai_model.config.get('enable_streaming', True)  # 默认启用
                
                logger.info(f"[模型检测] 当前模型: {self.api.model_name}, 支持流式传输: {model_supports_streaming}, 启用流式传输: {streaming_enabled}")
                
                # 恢复原始模型（如果切换了的话）
                if original_model is not None:
                    logger.info(f"[流式检测] 恢复原始模型: {model_id} -> {original_model_name}")
                    self.api._ai_model = original_model
                    self.api._model_name = original_model_name
                
                if model_supports_streaming and streaming_enabled:
                    # 使用流式请求
                    logger.info(f"[流式请求] 开始使用流式请求处理 {self.api.model_name} 模型")
                    
                    # 初始化流式日志计数器
                    if not hasattr(self, '_stream_log_counter'):
                        self._stream_log_counter = 0
                        self._stream_log_total_chars = 0
                    
                    def stream_callback(chunk):
                        if not self._request_cancelled:
                            # 只在每1000个字符时记录一次日志
                            self._stream_log_total_chars += len(chunk)
                            self._stream_log_counter += 1
                            if self._stream_log_total_chars % 1000 < len(chunk):
                                logger.info(f"[流式回调] 已接收 {self._stream_log_counter} 个片段，累计 {self._stream_log_total_chars} 字符")
                            self._current_signals.stream_update.emit(chunk)
                    
                    # 调用API时传入回调函数和model_id
                    response = self.api.ask(prompt, stream=True, stream_callback=stream_callback, model_id=model_id)
                    logger.info(f"[流式请求完成] 收到完整响应, 长度: {len(response)} 字符")
                    
                    # 在流式请求完成后，发送完整响应
                    if not self._request_cancelled:
                        logger.info(f"[流式请求完成] 发送最终累积响应到UI, 长度: {len(self._stream_response)} 字符")
                        self._current_signals.update_ui.emit(self._stream_response, True)
                else:
                    # 使用普通请求
                    logger.info(f"[普通请求] 使用普通请求处理 {self.api.model_name} 模型")
                    response = self.api.ask(prompt, stream=False, model_id=model_id)  # 明确指定不使用流式，并传递model_id
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
        self._stream_response = ""  # 累积的完整响应
        self._stream_buffer = ""    # 待处理的缓冲区
        self._last_update_time = 0
        self._update_interval = 0.1  # 100ms更新间隔
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_stream_buffer)
        self._last_processed_length = 0  # 上次处理的响应长度
    
    def _handle_stream_update(self, chunk):
        """处理流式响应更新
        
        :param chunk: 流式响应片段
        """
        if not chunk or self._request_cancelled:
            return
        
        # 初始化流式响应变量（如果还没有初始化）
        if not hasattr(self, '_update_timer'):
            self._init_stream_variables()
            
        # 累积响应内容
        self._stream_response += chunk
        self._stream_buffer += chunk
        
        # 检测推理标签（用于调试）
        if '<' in chunk and any(tag in chunk for tag in ['think', 'reasoning', 'ds-think', 'thinking']):
            logger.warning(f"[Response Handler Debug] 检测到可能的推理标签，chunk内容: {repr(chunk[:200])}")
        
        # 只在每1000个字符时记录一次日志
        if len(self._stream_response) % 1000 < len(chunk):
            logger.info(f"[Stream Update] 累积响应长度: {len(self._stream_response)} 字符 (~{len(self._stream_response)//4} tokens)")
            # 输出累积内容的前500字符用于调试
            logger.debug(f"[Response Handler Debug] 累积内容（前500字符）: {repr(self._stream_response[:500])}")
        
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
        
        # 检查是否有新内容需要处理
        current_length = len(self._stream_response)
        if not hasattr(self, '_last_processed_length'):
            self._last_processed_length = 0
        
        if current_length == self._last_processed_length:
            # 没有新内容，跳过处理
            self._stream_buffer = ""
            return
            
        # 只在缓冲区较大时记录日志
        if len(self._stream_buffer) > 100:
            logger.debug(f"[Stream Process] 处理缓冲区: {len(self._stream_buffer)} 字符，新增: {current_length - self._last_processed_length} 字符")
        
        self._stream_buffer = ""  # 清空缓冲区
        self._last_update_time = time.time()
        self._last_processed_length = current_length  # 更新已处理长度
        
        try:
            # 处理推理模型的 think 标签，获取占位符文本和 think 块列表
            text_to_convert, think_blocks = self._process_think_tags_for_stream(self._stream_response)
            
            # 使用markdown2转换完整的累积响应为HTML
            html = markdown2.markdown(
                text_to_convert,
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
            
            # 将占位符替换回 think 块的 HTML
            import re
            for i, think_content in enumerate(think_blocks):
                # 将推理内容转换为 Markdown HTML
                think_html_content = markdown2.markdown(
                    think_content,
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
                
                # 完整的 think 块 - 添加结束标识
                think_html = f'''<div class="reasoning-process" style="background-color: #f0f8ff; border-left: 4px solid #4a90e2; padding: 12px; margin: 10px 0; border-radius: 4px; font-size: 0.9em; color: #555;">
                    <div style="font-weight: bold; color: #4a90e2; margin-bottom: 8px; display: flex; align-items: center;">
                        <span>[推理过程]</span>
                    </div>
                    <div style="line-height: 1.6;">{think_html_content}</div>
                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #d0e8ff; font-size: 0.85em; color: #888; text-align: right;">
                        [推理完成]
                    </div>
                </div>'''
                html = html.replace(f'<!--THINK_BLOCK_{i}-->', think_html)
                
                # 未完成的 think 块
                incomplete_html = f'''<div class="reasoning-process" style="background-color: #fff9e6; border-left: 4px solid #ffa500; padding: 12px; margin: 10px 0; border-radius: 4px; font-size: 0.9em; color: #555;">
                    <div style="font-weight: bold; color: #ffa500; margin-bottom: 8px; display: flex; align-items: center;">
                        <span>[正在思考...]</span>
                    </div>
                    <div style="line-height: 1.6;">{think_html_content}</div>
                </div>'''
                html = html.replace(f'<!--THINK_BLOCK_INCOMPLETE_{i}-->', incomplete_html)
            
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
        
        # 重置流式响应相关变量
        self._last_processed_length = 0
        self._last_think_count = 0
        self._stream_response = ""
        self._stream_buffer = ""
            
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
                        font-size: {FONT_SIZE_MEDIUM}pt;
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
        base_style = f"""
            color: palette(text);
            font-size: {FONT_SIZE_MEDIUM}pt;
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

    def _on_scroll_value_changed(self, value):
        """滚动条值变化时的回调，用于检测用户主动滚动"""
        scrollbar = self.response_area.verticalScrollBar()
        if not scrollbar:
            return
        
        # 检测是否是用户主动滚动（而非程序自动滚动）
        # 如果滚动位置发生变化，且不在底部，说明用户在主动滚动
        if value != self._last_scroll_value:
            is_at_bottom = value >= scrollbar.maximum() - 5
            
            # 如果用户离开底部，标记为正在滚动
            if not is_at_bottom and not self._user_is_scrolling:
                self._user_is_scrolling = True
                logger.info(f"[Smart Scroll] 用户开始滚动，暂停自动更新")
            
            # 如果用户滚动到底部，恢复自动滚动
            elif is_at_bottom and self._user_is_scrolling:
                self._user_is_scrolling = False
                logger.info(f"[Smart Scroll] 用户回到底部，恢复自动更新")
            
            # 更新上次滚动位置
            self._last_scroll_value = value
            
            # 重置恢复定时器：如果用户停止滚动2秒，自动恢复
            if self._user_is_scrolling:
                if self._scroll_resume_timer:
                    self._scroll_resume_timer.stop()
                self._scroll_resume_timer = QTimer()
                self._scroll_resume_timer.setSingleShot(True)
                self._scroll_resume_timer.timeout.connect(self._resume_auto_scroll)
                self._scroll_resume_timer.start(2000)  # 2秒后恢复
    
    def _resume_auto_scroll(self):
        """恢复自动滚动（用户停止滚动2秒后）"""
        scrollbar = self.response_area.verticalScrollBar()
        if scrollbar:
            # 检查是否在底部附近（100像素内）
            is_near_bottom = scrollbar.value() >= scrollbar.maximum() - 100
            if is_near_bottom:
                self._user_is_scrolling = False
                logger.info(f"[Smart Scroll] 用户停止滚动且接近底部，恢复自动更新")
    
    def _set_html_response(self, html):
        """设置HTML响应并确保正确的样式"""
        import time
        
        # 只在HTML长度较大时记录日志（每1000字符记录一次）
        if not hasattr(self, '_last_html_log_size'):
            self._last_html_log_size = 0
        
        if len(html) - self._last_html_log_size >= 1000:
            logger.debug(f"[Set HTML] 更新UI显示, HTML长度: {len(html)} 字符")
            self._last_html_log_size = len(html)
        
        try:
            scrollbar = self.response_area.verticalScrollBar()
            if not scrollbar:
                self.response_area.setHtml(html)
                self.response_area.setAlignment(Qt.AlignLeft)
                return
            
            # 如果用户正在滚动，降低更新频率（500ms一次）
            current_time = time.time()
            if self._user_is_scrolling:
                if current_time - self._last_html_update_time < 0.5:
                    return  # 跳过本次更新
            
            self._last_html_update_time = current_time
            
            # 保存当前滚动位置和状态
            old_value = scrollbar.value()
            old_maximum = scrollbar.maximum()
            was_at_bottom = old_value >= old_maximum - 5
            
            # 临时断开滚动条信号，避免setHtml触发valueChanged导致误判
            scrollbar.valueChanged.disconnect(self._on_scroll_value_changed)
            
            # 设置HTML内容
            self.response_area.setHtml(html)
            self.response_area.setAlignment(Qt.AlignLeft)
            
            # 决定滚动行为
            new_maximum = scrollbar.maximum()
            
            if self._user_is_scrolling:
                # 用户正在主动滚动，保持绝对位置（不计算相对位置，避免抖动）
                # 尽量保持用户看到的内容不变
                scrollbar.setValue(min(old_value, new_maximum))
                self._last_scroll_value = scrollbar.value()
            elif was_at_bottom:
                # 用户在底部且未主动滚动，自动滚动到最新内容
                scrollbar.setValue(new_maximum)
                self._last_scroll_value = new_maximum
            else:
                # 用户不在底部也未主动滚动（可能刚开始），保持原位置
                scrollbar.setValue(min(old_value, new_maximum))
                self._last_scroll_value = scrollbar.value()
            
            # 重新连接滚动条信号
            scrollbar.valueChanged.connect(self._on_scroll_value_changed)
            
        except Exception as e:
            logger.error(f"[Set HTML] 更新UI时出错: {str(e)}")
            # 确保信号重新连接
            try:
                scrollbar = self.response_area.verticalScrollBar()
                if scrollbar:
                    scrollbar.valueChanged.connect(self._on_scroll_value_changed)
            except:
                pass


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
            
            # 更新按钮状态（收到响应后启用相关按钮）
            parent_dialog = self.parent()
            if parent_dialog and hasattr(parent_dialog, 'response_panels'):
                for panel in parent_dialog.response_panels:
                    if hasattr(panel, 'response_handler') and panel.response_handler == self:
                        panel.update_button_states()
                        break
            
            # 如果不是从历史记录加载的，保存到历史记录
            if not is_history:
                try:
                    # 获取父对话框以访问多书相关属性
                    if parent_dialog and hasattr(parent_dialog, 'current_uid'):
                        question = self.input_area.toPlainText()
                        
                        # 确定模式
                        mode = 'multi' if parent_dialog.is_multi_book else 'single'
                        
                        # 使用新的保存方法，传递AI标识符和模型信息
                        ai_id = getattr(self, 'ai_id', None)  # 获取AI标识符
                        
                        # 获取模型信息 - 优先从面板的API对象获取（面板切换AI时会更新）
                        model_info = None
                        api_obj = None
                        
                        # 尝试从父对话框的面板获取API对象
                        if hasattr(parent_dialog, 'response_panels') and parent_dialog.response_panels:
                            # 找到当前ResponseHandler对应的面板
                            for panel in parent_dialog.response_panels:
                                if hasattr(panel, 'response_handler') and panel.response_handler == self:
                                    api_obj = panel.api
                                    break
                        
                        # 如果没有找到面板的API，回退到使用ResponseHandler的API
                        if not api_obj and hasattr(self, 'api'):
                            api_obj = self.api
                        
                        # 从API对象提取模型信息
                        if api_obj:
                            model_info = {
                                'provider_name': getattr(api_obj, 'provider_name', 'Unknown'),
                                'model': getattr(api_obj, 'model', 'Unknown'),
                                'api_base': getattr(api_obj, 'api_base', '')
                            }
                        
                        logger.info(f"[历史记录] 准备保存: UID={parent_dialog.current_uid}, AI={ai_id}, 模式={mode}, 响应长度={len(text)}")
                        self.history_manager.save_history(
                            parent_dialog.current_uid,
                            mode,
                            parent_dialog.books_metadata,
                            question,
                            text,
                            ai_id=ai_id,
                            model_info=model_info
                        )
                        logger.info(f"[历史记录] ✓ 保存成功: UID={parent_dialog.current_uid}, AI={ai_id}")
                        
                        # 刷新历史记录菜单
                        if hasattr(parent_dialog, '_load_related_histories'):
                            parent_dialog._load_related_histories()
                            logger.info(f"[历史记录] 已刷新历史记录菜单")
                        
                        # 更新导出全部历史记录按钮状态
                        if hasattr(parent_dialog, 'response_panels') and parent_dialog.response_panels:
                            for panel in parent_dialog.response_panels:
                                if hasattr(panel, 'update_export_all_button_state'):
                                    panel.update_export_all_button_state()
                    elif hasattr(self, 'current_metadata') and self.current_metadata:
                        # 向后兼容旧版本
                        question = self.input_area.toPlainText()
                        # 使用旧版本保存（会被转换为新格式）
                        logger.warning("使用旧版本历史记录保存方法")
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
        # 显示发送按钮，隐藏停止按钮
        self.send_button.setVisible(True)
        if hasattr(self, 'stop_button') and self.stop_button is not None:
            self.stop_button.setVisible(False)