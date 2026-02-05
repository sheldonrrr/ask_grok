from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QGroupBox, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from .i18n import get_translation, get_suggestion_template
from calibre_plugins.ask_ai_plugin.config import get_prefs
from calibre_plugins.ask_ai_plugin.ui_constants import TEXT_COLOR_SECONDARY_STRONG
import sys

# Shortcut for ask: Ctrl+K (all platforms, including macOS)
# Shortcut for config: F2 (all platforms)
# Shortcut for Send: Command + Enter(macOS), Ctrl + Enter(other)
# Shortcut for Random Question: Command + Shift + R(macOS), Ctrl + Shift + R(other)

class ShortcutsWidget(QWidget):
    """快捷键展示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels = []  # 保存所有标签的引用
        
        # 获取当前语言的翻译
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        from .ui_constants import TAB_CONTENT_MARGIN, TAB_CONTENT_SPACING, setup_tab_widget_layout, get_tab_scroll_area_style, SPACING_SMALL, TEXT_COLOR_SECONDARY_STRONG
        
        # 创建主布局 - 使用统一的 Tab 布局函数
        main_layout = setup_tab_widget_layout(self)
        
        # 创建滚动区域以支持内容过多时滚动
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("shortcuts_scroll")
        scroll_area.setStyleSheet(get_tab_scroll_area_style("shortcuts_scroll"))
        # 直接设置 viewport 的边距
        if scroll_area.viewport():
            scroll_area.viewport().setContentsMargins(0, 0, 0, 0)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setStyleSheet("QWidget#shortcuts_container { background: transparent; border: none; }")
        content_widget.setObjectName("shortcuts_container")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(TAB_CONTENT_SPACING)
        content_layout.setContentsMargins(TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN)
        
        # 添加说明标签
        self.note_label = QLabel()
        self.note_label.setWordWrap(True)
        self.note_label.setStyleSheet(f"QLabel {{ color: {TEXT_COLOR_SECONDARY_STRONG}; font-size: 0.95em; padding: {SPACING_SMALL}px 0; }}")
        self.note_label.setText(self.i18n.get(
            'shortcuts_note',
            "You can customize these shortcuts in calibre: Preferences -> Shortcuts (search 'Ask AI').\n"
            "This page shows the default/example shortcuts. If you changed them in Shortcuts, calibre settings take precedence."
        ))
        content_layout.addWidget(self.note_label)
        
        # 创建单个快捷键组 - 使用虚线边框而不是内阴影
        shortcuts_group = QGroupBox()
        shortcuts_group.setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 10px; }")
        shortcuts_layout = QGridLayout(shortcuts_group)
        shortcuts_layout.setColumnStretch(1, 1)
        shortcuts_layout.setSpacing(10)
        content_layout.addWidget(shortcuts_group)
        self.shortcuts_group = shortcuts_group
        self.shortcuts_layout = shortcuts_layout
        
        # 添加弹性空间
        content_layout.addStretch()
        
        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        self.update_shortcuts()
        
    def update_shortcuts(self):
        """更新快捷键显示"""
        # 获取当前语言的翻译
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)

        # 更新顶部说明文字
        if hasattr(self, 'note_label') and self.note_label is not None:
            self.note_label.setText(self.i18n.get(
                'shortcuts_note',
                "You can customize these shortcuts in calibre: Preferences -> Shortcuts (search 'Ask AI').\n"
                "This page shows the default/example shortcuts. If you changed them in Shortcuts, calibre settings take precedence."
            ))

        # 完整清理布局，避免语言切换时旧控件未及时销毁导致叠加
        self._clear_layout(self.shortcuts_layout)
        self.labels.clear()
        
        # 判断当前系统
        is_mac = sys.platform == 'darwin'
        modifier_display = '⌘' if is_mac else 'Ctrl'
        enter_key = '↩' if is_mac else 'Enter'
        
        # 不设置组标题，保持空白
        self.shortcuts_group.setTitle("")
        
        # 定义所有快捷键（部分快捷键在不同平台有所不同）
        shortcuts = [
            (self.i18n.get('menu_ask', 'Ask'), 'Ctrl+K'),
            (self.i18n.get('config_title', 'Configuration'), 'F2'),
            (self.i18n.get('library_search', 'AI Search'), 'Ctrl+Shift+L'),
            (self.i18n.get('send_button', 'Send'), f'{modifier_display}+{enter_key}'),
            (self.i18n.get('suggest_button', 'Random Question'), f'{modifier_display}+Shift+R'),
        ]
        
        # 创建快捷键标签样式
        label_style = """
            QLabel {
                color: palette(text);
                padding: 2px;
            }
        """
        
        # 添加快捷键
        self._add_shortcuts_to_layout(shortcuts, self.shortcuts_layout, label_style)

    def _clear_layout(self, layout):
        """彻底清理布局中的所有子控件，避免重复叠加"""
        if layout is None:
            return
        while True:
            item = layout.takeAt(0)
            if item is None:
                break
            w = item.widget()
            child_layout = item.layout()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)
    
    def _add_shortcuts_to_layout(self, shortcuts, layout, style):
        """将快捷键添加到指定布局中"""
        # 添加标题行
        header_style = style + "font-weight: bold;"
        
        action_header = QLabel(self.i18n.get('action', 'Action'))
        action_header.setStyleSheet(header_style)
        layout.addWidget(action_header, 0, 0)
        
        shortcut_header = QLabel(self.i18n.get('shortcut', 'Shortcut Key'))
        shortcut_header.setStyleSheet(header_style)
        layout.addWidget(shortcut_header, 0, 1)
        
        self.labels.extend([action_header, shortcut_header])
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator, 1, 0, 1, 2)
        self.labels.append(separator)
        
        # 添加快捷键行
        for row, (action, key) in enumerate(shortcuts, 2):  # 从第2行开始（第0行是标题，第1行是分隔线）
            action_label = QLabel(action)
            action_label.setStyleSheet(style)
            layout.addWidget(action_label, row, 0)
            
            key_label = QLabel(f"<b>{key}</b>")
            key_label.setTextFormat(Qt.RichText)
            key_label.setStyleSheet(style)
            layout.addWidget(key_label, row, 1)
            
            self.labels.extend([action_label, key_label])
    
    def showEvent(self, event):
        """当组件显示时更新快捷键"""
        super().showEvent(event)
        self.update_shortcuts()
