from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from calibre_plugins.ask_gpt.i18n import get_translation
from calibre_plugins.ask_gpt.config import get_prefs
import sys

class ShortcutsWidget(QWidget):
    """快捷键展示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels = []  # 保存所有标签的引用
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)
        
        # 创建网格布局用于对齐快捷键
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setColumnStretch(1, 1)  # 让第二列（快捷键）可以拉伸
        main_layout.addLayout(self.grid_layout)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        self.update_shortcuts()
        
    def update_shortcuts(self):
        """更新快捷键显示"""
        # 清除现有标签
        for label in self.labels:
            self.grid_layout.removeWidget(label)
            label.deleteLater()
        self.labels.clear()
        
        # 判断当前系统
        is_mac = sys.platform == 'darwin'
        modifier = 'Command' if is_mac else 'Ctrl'
        
        # 获取当前语言的翻译
        i18n = get_translation(get_prefs()['language'])
        
        # 定义快捷键列表
        shortcuts = [
            (i18n['menu_ask_grok'], f'{modifier}+L'),  # 打开询问窗口
        ]
        
        # 创建快捷键标签
        label_style = """
            QLabel {
                font-size: 13px;
                color: #333;
            }
        """
        
        for row, (action, key) in enumerate(shortcuts):
            # 创建动作标签（左侧）
            action_label = QLabel(f"{action}:")
            action_label.setStyleSheet(label_style)
            self.grid_layout.addWidget(action_label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
            
            # 创建快捷键标签（右侧）
            key_label = QLabel(f"<b>{key}</b>")
            key_label.setTextFormat(Qt.RichText)
            key_label.setStyleSheet(label_style)
            self.grid_layout.addWidget(key_label, row, 1, Qt.AlignLeft | Qt.AlignVCenter)
            
            self.labels.extend([action_label, key_label])
    
    def showEvent(self, event):
        """当组件显示时更新快捷键"""
        super().showEvent(event)
        self.update_shortcuts()
