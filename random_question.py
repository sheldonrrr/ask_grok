#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QTextCursor
from .config import get_prefs, ConfigDialog
from .i18n import get_translation, get_suggestion_template
import logging

logger = logging.getLogger(__name__)

class SuggestionWorker(QThread):
    """生成随机问题的工作线程"""
    result = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, api, book_info, i18n=None, current_question=None):
        super().__init__(None)  # 不设置父对象，避免随父对象一起销毁
        self.api = api
        self.i18n = i18n or {}
        
        # 验证 book_info 是否包含 title 属性
        if not hasattr(book_info, 'title'):
            error_msg = self.i18n.get("book_info_check", "book_info need to contain title attribute")
            raise ValueError(error_msg)
            
        self.book_info = book_info
        self.current_question = current_question  # 保存当前问题
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
            
            # 准备提示词 - 从配置中获取用户自定义的随机问题提示词
            lang_code = get_prefs()['language']
            template = self.api.get_random_question_prompt(lang_code)
            
            # 如果用户没有配置，则使用默认模板
            if not template:
                template = get_suggestion_template(lang_code)
                logger.info("用户未配置随机问题提示词，使用默认模板")
            else:
                logger.info("使用用户配置的随机问题提示词")
            
            # 记录使用的模板
            logger.info(f"使用的问题随机问题模板: {template[:200]}...")
            
            # 格式化提示词，包含完整的书籍信息
            prompt = template.format(
                title=title,
                author=author_str,
                language=language,
            )
            
            # 如果存在当前问题，添加到提示词中以避免重复
            if self.current_question and self.current_question.strip():
                avoid_repeat = self.i18n.get("avoid_repeat_question", " Also, please make sure the new question is different from this one:").format(self.current_question.strip())
                prompt += avoid_repeat
            
            # 记录最终生成的提示词
            logger.info(f"生成的完整提示词: {prompt}")
            
            # 记录当前使用的 AI 模型
            try:
                model_name = self.api.model_display_name
                logger.info(f"当前使用的 AI 模型: {model_name}")
            except Exception as e:
                logger.warning(f"获取模型信息失败: {str(e)}")
                
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
        self._button_animation = None  # 使用统一的按钮加载动画
        self._request_cancelled = False
        self._original_input = ''
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
        
        # 初始化按钮加载动画
        from .ui_constants import ButtonLoadingAnimation
        self._button_animation = ButtonLoadingAnimation(
            button=self.suggest_button,
            loading_text=self.i18n.get('loading_text', 'Loading'),
            original_text=self.i18n.get('suggest_button', 'Random Question')
        )
        
        # 初始化状态
        self._request_cancelled = False
        self._worker = None
        self._original_input = ''
        self._response_text = ''
        self._cleanup_timer = None

    def update_i18n(self, i18n):
        """更新国际化文本对象"""
        self.i18n = i18n
        # 更新按钮文本
        if self.suggest_button.isEnabled():
            self.suggest_button.setText(self.i18n.get('suggest_button', 'Random Question'))

    def _setup_loading_animation(self):
        """设置加载动画（使用统一的按钮动画工具类）"""
        # 启动按钮加载动画
        if self._button_animation:
            self._button_animation.start()
        
        # 更新响应区域显示加载文本
        loading_text = self.i18n.get('loading_text', 'Loading')
        if self.response_area:
            self.response_area.setText(f"{loading_text}...")

    def _stop_loading_animation(self):
        """停止加载动画"""
        try:
            logger.debug("停止加载动画")
            if self._button_animation:
                self._button_animation.stop()
            logger.debug("加载动画已停止")
        except Exception as e:
            logger.error(f"停止加载动画时出错: {str(e)}")
            
    def _stop_timeout_timer(self):
        """停止超时检查定时器"""
        try:
            logger.debug("停止超时检查定时器")
            if hasattr(self, '_timeout_timer') and self._timeout_timer is not None:
                if self._timeout_timer.isActive():
                    self._timeout_timer.stop()
                self._timeout_timer.deleteLater()
                self._timeout_timer = None
                logger.debug("超时检查定时器已停止")
        except Exception as e:
            logger.error(f"停止超时检查定时器时出错: {str(e)}", exc_info=True)

    def _check_response_timeout(self):
        """检查是否超时"""
        # 如果已经有响应或请求已取消，则不执行超时处理
        if self._response_text or self._request_cancelled:
            logger.debug("超时检查：已有响应或请求已取消，跳过超时处理")
            return
            
        logger.debug("超时检查：触发超时处理")
        self._request_cancelled = True
        if self._worker:
            self._worker.cancel()
        # 直接显示请求失败状态
        if self.response_area:
            self.response_area.setText(self.i18n.get('request_failed', 'Request failed'))
        self._restore_ui_state()

    def _restore_ui_state(self, restore_input=False):
        """恢复UI状态"""
        logger.debug(f"_restore_ui_state called with restore_input={restore_input}")
        if not self.suggest_button:
            logger.debug("suggest_button不存在")
            return
            
        try:
            logger.debug("恢复按钮状态")
            self.suggest_button.setEnabled(True)
            # 使用 i18n 获取按钮文本
            button_text = self.i18n.get('suggest_button', 'Random Question') if hasattr(self, 'i18n') else 'Random Question'
            logger.debug(f"设置按钮文本为: {button_text}")
            self.suggest_button.setText(button_text)
            # 恢复按钮的原始样式（使用标准样式）
            from calibre_plugins.ask_ai_plugin.ui_constants import get_standard_button_style
            self.suggest_button.setStyleSheet(get_standard_button_style())
            
            # 是否恢复原始输入
            if restore_input and self._original_input and self.input_area:
                logger.debug(f"恢复原始输入: {self._original_input[:100]}")
                self.input_area.setPlainText(self._original_input)
            elif restore_input:
                logger.debug("无法恢复原始输入: 条件不满足")
        except Exception as e:
            logger.error(f"恢复UI状态时出错: {str(e)}", exc_info=True)

    def _on_suggestion_received(self, suggestion):
        """处理接收到的随机问题"""
        try:
            logger.debug(f"_on_suggestion_received called with suggestion: {suggestion[:100] if suggestion else 'None'}")
            
            # 停止加载动画和超时计时器
            if not self._request_cancelled:
                self._stop_loading_animation()
                self._stop_timeout_timer()
                self._request_cancelled = True
            
            # 首先设置响应文本，防止超时检查误判
            self._response_text = suggestion
            
            # 检查是否是空响应
            if not suggestion:
                error_msg = self.i18n.get('empty_suggestion', 'Received empty suggestion')
                if self.response_area:
                    self.response_area.setText(error_msg)
                self._response_text = None  # 重置响应文本，表示没有有效响应
            else:
                # 这是一个有效的建议
                logger.debug(f"收到有效随机问题，准备更新UI")
                
                # 将随机问题暂存到父对话框的临时变量中
                parent_dialog = self.suggest_button.window() if self.suggest_button else None
                if parent_dialog and hasattr(parent_dialog, '_pending_random_question'):
                    parent_dialog._pending_random_question = suggestion
                    logger.info(f"随机问题已暂存到临时变量，等待用户点击发送: {suggestion[:50]}...")
                
                # 更新输入框
                if self.input_area:
                    logger.debug("更新输入框文本")
                    self.input_area.setText(suggestion)
                    # 将光标移动到文本末尾
                    cursor = self.input_area.textCursor()
                    # 使用正确的QTextCursor常量
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.input_area.setTextCursor(cursor)
                    # 确保输入框获得焦点
                    self.input_area.setFocus()
                else:
                    logger.debug("input_area不存在")
                
                # 显示成功消息
                if self.response_area:
                    logger.debug("更新响应区域为成功消息")
                    self.response_area.setText(self.i18n.get('random_question_success', 'Random question generated successfully!'))
        except Exception as e:
            error_msg = f"处理建议时出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # 即使在异常情况下，如果我们有有效的响应文本，也不应该显示错误信息
            if self._response_text and self.input_area and self.input_area.toPlainText() == self._response_text:
                # 如果输入框已经有正确的文本，则显示成功信息
                if self.response_area:
                    self.response_area.setText(self.i18n.get('random_question_success', 'Random question generated successfully!'))
            else:
                # 否则显示错误信息
                if self.response_area:
                    self.response_area.setText(self.i18n.get('process_suggestion_error', 'Error processing suggestion'))
                self._response_text = None  # 确保错误情况下重置响应文本
        finally:
            # 确保UI状态总是能被恢复
            logger.debug("调用_restore_ui_state()")
            self._restore_ui_state(restore_input=False)  # 不恢复输入框，因为我们希望保留随机问题
            logger.debug("_restore_ui_state()调用完成")

    def _on_error(self, error):
        """处理错误"""
        if not self._request_cancelled:
            self._request_cancelled = True
            self._stop_loading_animation()
            self._stop_timeout_timer()  # 停止超时计时器
            
        if self.response_area:
            # 直接显示错误信息（已经格式化好：用户友好描述 + 技术细节）
            error_text = str(error).strip() if error else self.i18n.get('suggestion_error', 'Error generating suggestion')
            self.response_area.setText(error_text)
        
        # 重置响应文本，表示没有有效响应
        self._response_text = None
        
        # 开始定期检查线程状态
        self._start_cleanup_timer()

    def _stop_cleanup_timer(self):
        """停止清理定时器"""
        if self._cleanup_timer and self._cleanup_timer.isActive():
            self._cleanup_timer.stop()
            self._cleanup_timer.deleteLater()
            self._cleanup_timer = None

    def _start_cleanup_timer(self):
        """开始定期检查线程状态"""
        if not self._cleanup_timer:
            logger.debug("启动清理定时器")
            self._cleanup_timer = QTimer(self)
            self._cleanup_timer.timeout.connect(self._check_worker_status)
            self._cleanup_timer.start(100)  # 每 100ms 检查一次
            
    def _check_worker_status(self):
        """检查工作线程状态"""
        if self._worker and self._worker.is_finished():
            self._stop_cleanup_timer()
            self._cleanup_worker()

    def _cleanup_worker(self):
        """安全清理工作线程"""
        if not self._worker:
            return
            
        try:
            # 先取消工作线程
            self._worker.cancel()
            
            # 等待一小段时间让线程有机会自然结束
            if not self._worker.wait(100):  # 等待100ms
                # 如果线程还在运行，强制终止
                self._worker.terminate()
                self._worker.wait()  # 等待线程终止
                
            # 清理线程对象
            self._worker.deleteLater()
            
        except Exception as e:
            logger.warning(f"清理工作线程时出错: {str(e)}")
        finally:
            self._worker = None
            self._stop_loading_animation()
            self._stop_cleanup_timer()

    def generate(self, book_info):
        """生成随机问题"""
        if not self.api:
            logger.error("API信息没有成功初始化，随机问题生成失败。")
            return
        if not book_info:
            logger.error("书籍信息未提供，随机问题生成失败。")
            return
        
        # 检查是否已有请求在进行中
        if self._worker and not self._worker.is_finished():
            logger.warning("已有随机问题请求在进行中，忽略新请求")
            return
        
        # 检查当前选中的模型
        from calibre_plugins.ask_ai_plugin.config import get_prefs
        prefs = get_prefs()
        selected_model = prefs.get('selected_model', 'grok')
        
        # 如果是Custom模型，不需要检查API Key
        if selected_model == 'custom':
            logger.debug("Custom模型不强制要求API Key，跳过验证")
        else:
            # 对于其他模型，检查 auth token
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

        # 设置固定宽度，避免加载时文字变化导致按钮忽大忽小
        from calibre_plugins.ask_ai_plugin.ui_constants import get_standard_button_style
        self.suggest_button.setStyleSheet(get_standard_button_style())
        
        # 确保UI更新
        QApplication.processEvents()
        
        # 设置加载动画
        self._setup_loading_animation()
        
        # 获取当前问题
        current_question = self.input_area.toPlainText().strip()
        
        # 创建并启动工作线程
        if self._worker:
            self._cleanup_worker()
            
        # 总是传递当前问题，不进行与_original_input的比较
        # 这样即使第二次点击，也会将当前显示的问题传递给API
        self._worker = SuggestionWorker(
            self.api, 
            book_info, 
            i18n=self.i18n,
            current_question=current_question if current_question else None
        )
        self._worker.result.connect(self._on_suggestion_received)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()
        
        # 从配置中获取超时时间
        prefs = get_prefs()
        timeout_sec = prefs.get('request_timeout', 60)
        timeout_ms = timeout_sec * 1000
        
        logger.debug(f"使用配置的超时时间: {timeout_sec}秒")
        
        self._timeout_timer = QTimer(self)
        self._timeout_timer.setSingleShot(True)
        self._timeout_timer.timeout.connect(self._check_response_timeout)
        self._timeout_timer.start(timeout_ms)

    def prepare_close(self):
        """准备关闭，清理资源但不影响线程运行"""
        self._stop_loading_animation()
        self._stop_cleanup_timer()
        self._request_cancelled = True
        
        # 只标记取消，让线程自然结束
        if self._worker:
            self._worker.cancel()
            self._start_cleanup_timer()  # 开始定期检查线程状态

    def cleanup(self):
        """清理资源"""
        self._stop_loading_animation()
        self._stop_cleanup_timer()
        self._request_cancelled = True
        self._cleanup_worker()
        
    def _on_worker_finished(self):
        """工作线程完成时的处理"""
        logger.debug("工作线程完成")
        
        # 停止超时计时器，防止在响应返回后还触发超时
        self._stop_timeout_timer()
        
        # 如果界面显示"请求失败"但实际有响应文本，则更新界面
        if self._response_text and self.response_area and self.response_area.toPlainText() == self.i18n.get('request_failed', 'Request failed'):
            logger.debug("检测到超时后响应返回，更新界面")
            # 更新输入框
            if self.input_area:
                logger.debug(f"更新输入框文本为: {self._response_text[:50]}...")
                self.input_area.setText(self._response_text)
                # 将光标移动到文本末尾
                cursor = self.input_area.textCursor()
                # 使用正确的QTextCursor常量
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.input_area.setTextCursor(cursor)
                # 确保输入框获得焦点
                self.input_area.setFocus()
            
            # 显示成功消息
            if self.response_area:
                logger.debug("更新响应区域为成功消息")
                self.response_area.setText(self.i18n.get('random_question_success', 'Random question generated successfully!'))
                
            # 恢复按钮状态
            self._restore_ui_state(restore_input=False)
        
        # 清理工作线程
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
