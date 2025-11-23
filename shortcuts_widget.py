from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QGroupBox, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from .i18n import get_translation, get_suggestion_template
from calibre_plugins.ask_ai_plugin.config import get_prefs
import sys

# Shortcut for ask: F3(macOS), Ctrl + L(other)
# Shortcut for config: F2(macOS), Ctrl + K(other)
# Shortcut for Send: Command + Enter(macOS), Ctrl + Enter(other)
# Shortcut for Random Question: Command + R(macOS), Ctrl + R(other)
# Note: macOS uses function keys (F2, F3) to avoid Qt keyboard mapping conflicts

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
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # 创建滚动区域以支持内容过多时滚动
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("shortcuts_scroll")
        # 去除滚动区域的边框和内边距
        # 使用 ID 选择器确保只影响这个特定的 QScrollArea
        style = """
            QScrollArea#shortcuts_scroll {
                padding: 0px;
                margin: 0px;
                border: none;
            }
            QScrollArea#shortcuts_scroll > QWidget {
                background: transparent;
            }
            QScrollArea#shortcuts_scroll QWidget#qt_scrollarea_viewport {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """
        scroll_area.setStyleSheet(style)
        # 直接设置 viewport 的边距
        if scroll_area.viewport():
            scroll_area.viewport().setContentsMargins(0, 0, 0, 0)
        
        # 创建内容容器
        content_widget = QWidget()
        # 只为这个特定的 widget 设置样式，不影响子控件
        content_widget.setStyleSheet("QWidget#shortcuts_container { background: transparent; border: none; }")
        content_widget.setObjectName("shortcuts_container")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建单个快捷键组 - 使用虚线边框而不是内阴影
        shortcuts_group = QGroupBox()
        shortcuts_group.setStyleSheet("QGroupBox { border: 1px dashed #cccccc; padding: 10px; }")
        shortcuts_layout = QGridLayout(shortcuts_group)
        shortcuts_layout.setColumnStretch(1, 1)
        shortcuts_layout.setSpacing(10)
        content_layout.addWidget(shortcuts_group)
        self.shortcuts_group = shortcuts_group
        self.shortcuts_layout = shortcuts_layout
        
        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        self.update_shortcuts()
        
    def update_shortcuts(self):
        """更新快捷键显示"""
        # 清除现有标签
        for label in self.labels:
            label.deleteLater()
        self.labels.clear()
        
        # 判断当前系统
        is_mac = sys.platform == 'darwin'
        modifier_display = '⌘' if is_mac else 'Ctrl'
        enter_key = '↩' if is_mac else 'Enter'
        
        # 获取当前语言的翻译
        prefs = get_prefs()
        language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(language)
        
        # 不设置组标题，保持空白
        self.shortcuts_group.setTitle("")
        
        # 定义所有快捷键（macOS和其他平台有所不同）
        if is_mac:
            # macOS使用功能键避免Qt键盘映射冲突
            shortcuts = [
                (self.i18n.get('menu_ask', 'Ask {model}').format(model='Grok'), 'F3'),
                (self.i18n.get('config_title', 'Configuration'), 'F2'),
                (self.i18n.get('send_button', 'Send'), f'{modifier_display}+{enter_key}'),
                (self.i18n.get('suggest_button', 'Random Question'), f'{modifier_display}+R'),
            ]
        else:
            # 其他系统使用标准组合键
            shortcuts = [
                (self.i18n.get('menu_ask', 'Ask {model}').format(model='Grok'), f'{modifier_display}+L'),
                (self.i18n.get('config_title', 'Configuration'), f'{modifier_display}+K'),
                (self.i18n.get('send_button', 'Send'), f'{modifier_display}+{enter_key}'),
                (self.i18n.get('suggest_button', 'Random Question'), f'{modifier_display}+R'),
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
