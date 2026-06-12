#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
响应面板组件 - 用于多AI并行请求功能
每个面板包含：AI选择器（多AI模式）、响应区域（右键复制/导出）
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from calibre_plugins.ask_ai_plugin.widgets import NoScrollComboBox
from calibre_plugins.ask_ai_plugin.ui_constants import (
    SPACING_SMALL, PADDING_MEDIUM, ASK_COMBO_MIN_WIDTH, ASK_RESPONSE_PANEL_MIN_HEIGHT,
    RESPONSE_FONT_FAMILY,
    get_response_area_qss,
    get_response_content_stylesheet,
)
from calibre_plugins.ask_ai_plugin.qa_actions import build_response_context_menu

logger = logging.getLogger(__name__)


class ResponsePanel(QWidget):
    """单个AI响应面板组件
    
    包含：
    - Header: AI切换器（多AI模式）
    - Response Area: 响应文本显示区域（右键复制/导出）
    """
    
    # 信号
    ai_changed = pyqtSignal(int, str)  # (panel_index, new_ai_id)
    request_started = pyqtSignal(int)  # panel_index
    request_finished = pyqtSignal(int)  # panel_index
    
    def __init__(self, panel_index, parent, api, i18n, show_ai_switcher=True):
        """初始化响应面板
        
        Args:
            panel_index: 面板索引（0-3）
            parent: 父窗口
            api: API客户端实例
            i18n: 国际化字典
            show_ai_switcher: 是否在面板内显示 AI 切换器（默认 True）
        """
        super().__init__(parent)
        self.panel_index = panel_index
        self.parent_dialog = parent
        self.api = api
        self.i18n = i18n
        self.response_handler = None  # 将在setup后初始化
        self.show_ai_switcher = show_ai_switcher
        
        # 标志：是否正在初始化（用于避免初始化时弹出确认对话框）
        self._is_initializing = True
        
        # 当前问题（用于按钮状态判断）
        self.current_question = ""
        
        # 存储原始Markdown文本（用于复制Markdown格式）
        self._original_markdown_text = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI布局"""
        # 主布局：垂直
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(SPACING_SMALL)
        
        # === Header 区域（横向） ===
        # 只有当 show_ai_switcher 为 True 时才显示 header
        if self.show_ai_switcher:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(SPACING_SMALL)
            
            # AI切换器（直接显示模型名称，不需要"AI 1:"标签）
            from calibre_plugins.ask_ai_plugin.ui_constants import style_ask_toolbar_widget
            self.ai_switcher = NoScrollComboBox()
            style_ask_toolbar_widget(self.ai_switcher)
            self.ai_switcher.currentIndexChanged.connect(self.on_ai_switched)
            header_layout.addWidget(self.ai_switcher)
            header_layout.addStretch()
            
            main_layout.addLayout(header_layout)
        else:
            # 不显示 header，但仍然创建 ai_switcher（将被添加到外部布局）
            from calibre_plugins.ask_ai_plugin.ui_constants import style_ask_toolbar_widget
            self.ai_switcher = NoScrollComboBox()
            style_ask_toolbar_widget(self.ai_switcher)
            self.ai_switcher.currentIndexChanged.connect(self.on_ai_switched)
        
        # === Response Area（占据主要空间） ===
        self.response_area = QTextBrowser()
        self.response_area.setOpenExternalLinks(False)  # 禁用外部链接，使用自定义处理
        self.response_area.setOpenLinks(False)  # 禁止QTextBrowser自动导航，防止内容被清除
        self.response_area.setMinimumHeight(200)
        self.response_area.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction | 
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        # 连接链接点击信号
        self.response_area.anchorClicked.connect(self._on_anchor_clicked)
        self.response_area.setStyleSheet(get_response_area_qss())
        self.response_area.setPlaceholderText(self.i18n.get('response_placeholder', 'Response soon...'))
        self.response_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.response_area.customContextMenuRequested.connect(self._show_context_menu)

        from PyQt5.QtGui import QFont
        response_font = QFont(self.response_area.font())
        font_families = [
            f.strip().strip("'\"")
            for f in RESPONSE_FONT_FAMILY.split(',')
            if f.strip().strip("'\"") not in ('-apple-system', 'sans-serif')
        ]
        if hasattr(response_font, 'setFamilies') and font_families:
            response_font.setFamilies(font_families)
        else:
            response_font.setStyleHint(QFont.SansSerif)
        self.response_area.setFont(response_font)

        doc = self.response_area.document()
        doc.setDocumentMargin(PADDING_MEDIUM)
        doc.setDefaultStyleSheet(get_response_content_stylesheet())
        
        main_layout.addWidget(self.response_area, stretch=1)

        self.setMinimumHeight(ASK_RESPONSE_PANEL_MIN_HEIGHT)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 添加边框样式
        # 使用 ResponsePanel 类名选择器，避免影响子控件（如 QComboBox 的下拉列表）
        self.setObjectName("ResponsePanel")
        self.setStyleSheet("""
            #ResponsePanel {
                border: 1px solid palette(mid);
                border-radius: 4px;
                background: palette(base);
            }
        """)
        
    def setup_response_handler(self, response_handler):
        """设置响应处理器
        
        Args:
            response_handler: ResponseHandler实例
        """
        self.response_handler = response_handler
        # 设置AI标识符，用于历史记录
        self.response_handler.ai_id = None  # 初始为None，在发送请求时更新
        
    def get_selected_ai(self):
        """获取当前选中的AI ID
        
        Returns:
            str: AI ID，如果没有选中则返回None
        """
        return self.ai_switcher.currentData()
    
    def populate_ai_switcher(self, configured_ais, used_ais=None):
        """填充AI切换器
        
        Args:
            configured_ais: 已配置的AI列表 [(ai_id, display_name), ...]
            used_ais: 已被其他面板使用的AI ID集合
        """
        if used_ais is None:
            used_ais = set()
        
        logger.info(f"[Panel {self.panel_index}] populate_ai_switcher - configured_ais数量: {len(configured_ais)}, used_ais: {used_ais}")
        
        # 阻止信号触发
        self.ai_switcher.blockSignals(True)
        
        current_ai = self.ai_switcher.currentData()
        logger.info(f"[Panel {self.panel_index}] 当前选中的AI: {current_ai}")
        self.ai_switcher.clear()
        
        # 添加一个空选项（用于留空）
        self.ai_switcher.addItem(
            self.i18n.get('select_ai', '-- Select AI --'),
            None
        )
        
        # 检查是否有可用的AI
        available_ais = [(ai_id, name) for ai_id, name in configured_ais if ai_id not in used_ais or ai_id == current_ai]
        logger.info(f"[Panel {self.panel_index}] 过滤后可用的AI数量: {len(available_ais)}, AI列表: {[ai_id for ai_id, _ in available_ais]}")
        
        if not available_ais:
            # 没有可用的AI，只显示提示
            self.ai_switcher.addItem(
                self.i18n.get('add_more_ai_providers', 'Please add more AI providers in settings'),
                None
            )
            self.ai_switcher.setEnabled(True)  # 保持启用，让用户看到提示
            self.response_area.setPlaceholderText(
                self.i18n.get('no_ai_available', 'No AI available for this panel')
            )
        else:
            # 有可用的AI
            for ai_id, display_name in available_ais:
                self.ai_switcher.addItem(display_name, ai_id)
            
            # 尝试恢复之前的选择
            if current_ai:
                index = self.ai_switcher.findData(current_ai)
                if index >= 0:
                    self.ai_switcher.setCurrentIndex(index)
                else:
                    # 如果之前的选择不可用，设置为空选项
                    self.ai_switcher.setCurrentIndex(0)
            
            self.ai_switcher.setEnabled(True)
        
        # 恢复信号
        self.ai_switcher.blockSignals(False)
    
    def on_ai_switched(self, index):
        """AI切换事件处理"""
        ai_id = self.ai_switcher.currentData()
        if ai_id:
            logger.info(f"面板 {self.panel_index} 切换到 AI: {ai_id}")
            
            # 检查是否需要询问用户是否设为默认AI
            # 如果用户取消切换，则不触发 ai_changed 信号
            if not self._check_and_prompt_default_ai(ai_id):
                return
            
            self.ai_changed.emit(self.panel_index, ai_id)
    
    def _check_and_prompt_default_ai(self, selected_ai_id):
        """检查并询问用户是否将选择的AI设为默认
        
        Args:
            selected_ai_id: 用户选择的AI ID
            
        Returns:
            bool: True表示继续切换AI，False表示用户取消切换
        """
        from PyQt5.QtWidgets import QMessageBox, QPushButton
        from calibre_plugins.ask_ai_plugin.config import prefs
        
        # 如果正在初始化，跳过提示（避免在恢复上次选择时弹出确认框）
        if self._is_initializing:
            return True
        
        # 只在单面板模式下提示
        if not hasattr(self.parent_dialog, 'response_panels'):
            return True
        
        panel_count = len(self.parent_dialog.response_panels)
        if panel_count != 1:
            return True
        
        # 获取config中当前的默认AI
        current_default_ai = prefs.get('selected_model', 'grok')
        
        # 如果选择的AI与默认AI相同，不提示
        if selected_ai_id == current_default_ai:
            return True
        
        # 获取AI的显示名称
        ai_display_name = self.ai_switcher.currentText()
        
        # 弹出确认对话框（使用自定义按钮文字以支持本地化）
        msg_title = self.i18n.get('set_default_ai_title', 'Set Default AI')
        msg_text = self.i18n.get(
            'set_default_ai_message',
            'You have switched to "{0}". Would you like to set it as the default AI for future queries?'
        ).format(ai_display_name)
        
        # 创建消息框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(msg_title)
        msg_box.setText(msg_text)
        msg_box.setIcon(QMessageBox.Question)
        
        # 添加本地化的按钮
        yes_text = self.i18n.get('yes', 'Yes')
        no_text = self.i18n.get('no', 'No')
        yes_button = msg_box.addButton(yes_text, QMessageBox.YesRole)
        no_button = msg_box.addButton(no_text, QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)  # 默认选择No，避免误操作
        
        msg_box.exec_()
        clicked_button = msg_box.clickedButton()
        
        if clicked_button == yes_button:
            # 用户选择Yes，更新config
            prefs.set('selected_model', selected_ai_id)
            logger.info(f"用户确认将 {selected_ai_id} 设为默认AI")
            
            # 显示成功提示
            success_msg = self.i18n.get(
                'set_default_ai_success',
                'Default AI has been set to "{0}".'
            ).format(ai_display_name)
            QMessageBox.information(self, self.i18n.get('info', 'Information'), success_msg)
            return True
        else:
            # 用户选择No，恢复到之前的AI选择
            
            # 阻止信号，避免递归调用
            self.ai_switcher.blockSignals(True)
            
            # 恢复到默认AI
            index = self.ai_switcher.findData(current_default_ai)
            if index >= 0:
                self.ai_switcher.setCurrentIndex(index)
            
            # 恢复信号
            self.ai_switcher.blockSignals(False)
            
            return False
    
    def send_request(self, prompt, model_id=None, use_library_chat=False):
        """发送请求到选中的AI
        
        Args:
            prompt: 提示词
            model_id: 可选，指定使用的模型ID。如果为None，使用当前选中的AI
            use_library_chat: 是否使用Library Chat功能
        """
        if not self.response_handler:
            logger.error(f"面板 {self.panel_index} 的 ResponseHandler 未初始化")
            return
        
        # 使用指定的model_id或当前选中的AI
        target_model_id = model_id if model_id else self.get_selected_ai()
        
        if not target_model_id:
            logger.warning(f"面板 {self.panel_index} 没有选中的AI")
            return
        
        logger.info(f"[面板 {self.panel_index}] 开始请求 AI: {target_model_id}, use_library_chat={use_library_chat}")
        self.request_started.emit(self.panel_index)
        
        # 更新响应处理器的AI标识符（用于历史记录）
        self.response_handler.ai_id = target_model_id
        logger.info(f"[面板 {self.panel_index}] 已设置 ai_id={target_model_id} 用于历史记录")
        
        # 调用响应处理器发送请求，传递model_id和use_library_chat参数
        self.response_handler.start_async_request(prompt, model_id=target_model_id, use_library_chat=use_library_chat)
        logger.info(f"[面板 {self.panel_index}] 异步请求已启动")
    
    def get_response_text(self):
        """获取响应文本
        
        Returns:
            str: 响应文本
        """
        return self.response_area.toPlainText()
    

    def _show_context_menu(self, pos):
        menu = build_response_context_menu(self)
        menu.exec_(self.response_area.mapToGlobal(pos))

    def clear_response(self):
        """清空响应区域"""
        self.response_area.clear()

    def update_button_states(self):
        """保留接口兼容（操作已移至右键菜单）。"""
        pass

    def update_export_all_button_state(self):
        """保留接口兼容。"""
        pass

    def set_current_question(self, question):
        """设置当前问题。"""
        self.current_question = question

    def _on_anchor_clicked(self, url):
        """处理链接点击事件
        
        支持的链接格式：
        - calibre://book/BOOK_ID - 在Calibre中打开书籍
        - http://... 或 https://... - 在浏览器中打开外部链接
        """
        from PyQt5.QtCore import QUrl
        from PyQt5.QtGui import QDesktopServices
        
        url_str = url.toString()
        
        # Windows compatibility: normalize backslashes to forward slashes
        # On Windows, QUrl might convert forward slashes to backslashes in some cases
        url_str = url_str.replace('\\', '/')
        
        logger.info("="*80)
        logger.info(f"[BOOK_LINK_CLICK] 链接被点击: {url_str}")
        logger.info(f"[BOOK_LINK_CLICK] 父对话框状态: visible={self.parent_dialog.isVisible()}, modal={self.parent_dialog.isModal()}")
        logger.info(f"[BOOK_LINK_CLICK] 响应区域内容长度: {len(self.response_area.toPlainText())}")
        
        try:
            # Windows compatibility: also check for backslash variants
            if url_str.startswith('calibre://book/') or url_str.startswith('calibre:/book/'):
                # 提取书籍ID - handle both double and single slash variants
                book_id_str = url_str.replace('calibre://book/', '').replace('calibre:/book/', '')
                book_id = int(book_id_str)
                logger.info(f"[BOOK_LINK_CLICK] 提取书籍 ID: {book_id}")
                
                # 使用Calibre的正确API打开书籍
                if hasattr(self.parent_dialog, 'gui') and self.parent_dialog.gui:
                    gui = self.parent_dialog.gui
                    logger.info(f"[BOOK_LINK_CLICK] GUI 实例可用")
                    logger.info(f"[BOOK_LINK_CLICK] 当前库视图选择: {gui.library_view.selectionModel().selectedRows()}")
                    
                    # 使用Calibre的View action打开书籍，不改变库视图选择
                    # 这样可以避免触发show_dialog()，保持AI Search对话框内容
                    try:
                        db = gui.current_db
                        fmt = db.formats(book_id, index_is_id=True)
                        logger.info(f"[BOOK_LINK_CLICK] 书籍格式: {fmt}")
                        
                        if fmt:
                            fmt = fmt.split(',')[0].lower()
                            path = db.format_abspath(book_id, fmt, index_is_id=True)
                            logger.info(f"[BOOK_LINK_CLICK] 书籍路径: {path}")
                            
                            if path:
                                print(f"[BOOK_LINK_CLICK] 准备打开书籍")
                                print(f"[BOOK_LINK_CLICK] 打开前对话框状态: visible={self.parent_dialog.isVisible()}")
                                logger.info(f"[BOOK_LINK_CLICK] 准备打开书籍")
                                logger.info(f"[BOOK_LINK_CLICK] 打开前对话框状态: visible={self.parent_dialog.isVisible()}")
                                
                                # 使用Calibre的View action来打开书籍，但通过直接调用view_book方法
                                # 这样可以避免改变库视图选择，同时避免EbookViewer直接实例化导致的崩溃
                                if 'View' in gui.iactions:
                                    view_action = gui.iactions['View']
                                    # 使用内部方法直接打开书籍，传入book_id
                                    try:
                                        # view_book方法需要book_id作为参数
                                        view_action._view_calibre_books([book_id])
                                        logger.info(f"[BOOK_LINK_CLICK] 使用View action打开书籍成功")
                                    except AttributeError:
                                        # 如果_view_calibre_books不存在，尝试其他方法
                                        # 临时选中书籍，打开后立即恢复选择
                                        old_selection = [gui.library_view.model().id(row) for row in gui.library_view.selectionModel().selectedRows()]
                                        gui.library_view.select_rows([book_id])
                                        view_action.qaction.trigger()
                                        # 恢复原来的选择（如果是AI Search模式，原来没有选择）
                                        if old_selection:
                                            gui.library_view.select_rows(old_selection)
                                        else:
                                            gui.library_view.selectionModel().clear()
                                        logger.info(f"[BOOK_LINK_CLICK] 使用View action trigger打开书籍成功")
                                else:
                                    logger.error(f"[BOOK_LINK_CLICK] View action不可用")
                            
                                # 使用QTimer延迟检查，因为对话框可能在稍后被关闭
                                from PyQt5.QtCore import QTimer
                                def check_dialog_state():
                                    print(f"[BOOK_LINK_CLICK] 打开后对话框状态: visible={self.parent_dialog.isVisible()}")
                                    print(f"[BOOK_LINK_CLICK] 打开后响应区域内容长度: {len(self.response_area.toPlainText())}")
                                    print(f"[BOOK_LINK_CLICK] 对话框是否被关闭: {self.parent_dialog.isHidden()}")
                                    print(f"[BOOK_LINK_CLICK] 成功打开书籍: {path}")
                                    print("="*80)
                                
                                # 立即检查
                                check_dialog_state()
                                # 1秒后再检查一次
                                QTimer.singleShot(1000, check_dialog_state)
                            else:
                                logger.error(f"[BOOK_LINK_CLICK] 找不到书籍文件路径")
                        else:
                            logger.error(f"[BOOK_LINK_CLICK] 书籍 {book_id} 没有可用格式")
                    except Exception as e:
                        logger.error(f"[BOOK_LINK_CLICK] 打开书籍失败: {str(e)}", exc_info=True)
                else:
                    logger.warning("[BOOK_LINK_CLICK] GUI 实例不可用")
            elif url_str.startswith('http://') or url_str.startswith('https://'):
                # 外部链接，在浏览器中打开
                QDesktopServices.openUrl(url)
                logger.info(f"在浏览器中打开: {url_str}")
            else:
                logger.warning(f"[BOOK_LINK_CLICK] 未知的链接格式: {url_str}")
        except Exception as e:
            logger.error(f"[BOOK_LINK_CLICK] 处理链接点击时出错: {str(e)}", exc_info=True)
        finally:
            logger.info(f"[BOOK_LINK_CLICK] _on_anchor_clicked 执行完成")
            logger.info("="*80)
