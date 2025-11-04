#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自定义UI组件
"""

from PyQt5.QtWidgets import QComboBox, QPushButton
from PyQt5.QtCore import Qt


class NoScrollComboBox(QComboBox):
    """
    自定义QComboBox，禁用未展开时的滚轮事件
    只有在下拉菜单展开时才允许滚轮滚动
    修复了下拉菜单在鼠标悬停时消失的问题
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # 只设置必要的左侧间距，其他完全使用Qt默认样式
        # 这样可以确保在所有平台（Linux/macOS/Windows）和主题（浅色/深色）下都正常工作
        self.setStyleSheet("""
            QComboBox {
                padding-left: 8px;
            }
        """)
        
        # 设置下拉列表视图的鼠标跟踪，防止下拉菜单在hover时消失
        self.view().setMouseTracking(True)
        
        # 确保下拉列表使用系统默认样式（包括 hover 效果）
        # 不设置任何自定义背景色，让 Qt 使用默认的 palette
        self.view().setStyleSheet("")
    
    def wheelEvent(self, event):
        """重写滚轮事件，只在下拉菜单展开时才处理"""
        # 只有在下拉菜单展开时才允许滚轮事件
        if self.view().isVisible():
            super().wheelEvent(event)
        else:
            # 未展开时忽略滚轮事件
            event.ignore()


def apply_button_style(button, min_width=None, padding="5px 12px"):
    """
    为按钮应用统一的样式
    
    Args:
        button: QPushButton实例
        min_width: 最小宽度（可选）
        padding: 内边距，默认为"5px 12px"（上下5px，左右12px）
    
    功能：
    - 添加合适的内边距，防止文字过于拥挤
    - 文字居中对齐
    - 如果指定了min_width，设置最小宽度
    """
    if min_width:
        button.setMinimumWidth(min_width)
    
    button.setStyleSheet(f"""
        QPushButton {{
            padding: {padding};
            text-align: center;
        }}
    """)


def create_styled_button(text, parent=None, min_width=None, padding="5px 12px", tooltip=None):
    """
    创建一个带有统一样式的按钮
    
    Args:
        text: 按钮文字
        parent: 父组件
        min_width: 最小宽度（可选）
        padding: 内边距
        tooltip: 工具提示（可选）
    
    Returns:
        QPushButton: 配置好的按钮实例
    """
    button = QPushButton(text, parent)
    apply_button_style(button, min_width, padding)
    
    if tooltip:
        button.setToolTip(tooltip)
    
    return button
