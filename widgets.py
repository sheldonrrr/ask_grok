#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自定义UI组件
"""

from PyQt5.QtWidgets import QComboBox, QPushButton, QSplitter, QSplitterHandle
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush


class GripSplitterHandle(QSplitterHandle):
    """绘制上下排列圆点的分栏手柄；拖拽按下时高亮。"""

    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self._dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            # Calibre/Qt6: QPainter.RenderHint.Antialiasing
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = self.rect()
            pal = self.palette()

            if self._dragging:
                # 与此前 hover 高亮一致：highlight 背景
                painter.fillRect(rect, pal.highlight().color())
                dot_color = pal.highlightedText().color()
            else:
                painter.fillRect(rect, Qt.transparent)
                dot_color = pal.mid().color()

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(dot_color))
            cx = rect.center().x()
            cy = rect.center().y()
            radius = 2
            gap = 5
            # 水平分栏手柄：中间一列上下排列的圆点
            for i in (-1, 0, 1):
                painter.drawEllipse(QPoint(int(cx), int(cy + i * gap)), radius, radius)
        finally:
            painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.update()
        super().mouseReleaseEvent(event)


class GripSplitter(QSplitter):
    """使用圆点手柄的水平/垂直分栏。"""

    def createHandle(self):
        return GripSplitterHandle(self.orientation(), self)


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


def apply_button_style(button, min_width=None, padding=None, max_width=None):
    """
    为文字按钮应用统一样式。字号比正文小 2，高度随按钮字体变化。

    默认按文字收缩：短标签不会铺在很宽的底上，长标签宽到 BUTTON_MAX_WIDTH 为止。
    min_width=0 表示布局要拉伸这个按钮（例如左右各占一半），此时不设宽度上下限。

    Args:
        button: QPushButton实例
        min_width: 内容区最小宽度（像素）。None 使用 button_min_width；0 表示交给布局
        padding: 内边距（可选，默认使用 STANDARD_BUTTON_PADDING）
        max_width: 外宽上限（像素）。None 使用 button_max_width
    """
    from .ui_constants import (
        get_standard_button_style, install_button_font, button_min_width,
        apply_text_button_width,
    )

    font = install_button_font(button)
    stretch = min_width == 0
    if min_width is None:
        min_width = button_min_width(font)

    button.setStyleSheet(get_standard_button_style(min_width, padding, font))
    apply_text_button_width(button, font, min_width, max_width, stretch=stretch)


def create_styled_button(text, parent=None, min_width=None, padding=None, tooltip=None):
    """
    创建一个带有统一样式的按钮。字号和高度与 apply_button_style 相同。

    Args:
        text: 按钮文字
        parent: 父组件
        min_width: 最小宽度（可选）
        padding: 内边距（可选，默认 STANDARD_BUTTON_PADDING）
        tooltip: 工具提示（可选）

    Returns:
        QPushButton: 配置好的按钮实例
    """
    button = QPushButton(text, parent)
    apply_button_style(button, min_width, padding)
    
    if tooltip:
        button.setToolTip(tooltip)
    
    return button
