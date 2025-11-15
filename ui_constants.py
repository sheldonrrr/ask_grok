#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI设计系统常量
定义统一的间距、尺寸、颜色等设计规范
"""

# ============ 间距系统 (8px基准) ============
# 使用8px作为基准单位，所有间距都是8的倍数
SPACING_UNIT = 8

# 组件内部间距
SPACING_TINY = SPACING_UNIT // 2      # 4px - 极小间距
SPACING_SMALL = SPACING_UNIT          # 8px - 小间距
SPACING_MEDIUM = SPACING_UNIT * 2     # 16px - 中等间距
SPACING_LARGE = SPACING_UNIT * 3      # 24px - 大间距
SPACING_XLARGE = SPACING_UNIT * 4     # 32px - 超大间距

# 边距（Margins）
MARGIN_SMALL = 8
MARGIN_MEDIUM = 16
MARGIN_LARGE = 24

# 内边距（Padding）
PADDING_SMALL = 8
PADDING_MEDIUM = 12
PADDING_LARGE = 16

# ============ 尺寸系统 ============
# 按钮
BUTTON_MIN_WIDTH = 100
BUTTON_MEDIUM_WIDTH = 150
BUTTON_LARGE_WIDTH = 200
BUTTON_HEIGHT = 32

# 输入框
INPUT_MIN_WIDTH = 200
INPUT_MEDIUM_WIDTH = 300
INPUT_LARGE_WIDTH = 400
INPUT_HEIGHT = 28

# 下拉框
COMBO_MIN_WIDTH = 150
COMBO_MEDIUM_WIDTH = 200
COMBO_LARGE_WIDTH = 300

# ============ 颜色系统 ============
# 边框颜色
BORDER_COLOR_LIGHT = "#e0e0e0"
BORDER_COLOR_MEDIUM = "#cccccc"
BORDER_COLOR_DARK = "#aaaaaa"

# 分隔线颜色
SEPARATOR_COLOR = "#d0d0d0"

# 文字颜色
TEXT_COLOR_PRIMARY = "palette(text)"
TEXT_COLOR_SECONDARY = "palette(dark)"  # 使用 Qt 调色板，支持明暗模式
TEXT_COLOR_DISABLED = "palette(mid)"  # 使用 Qt 调色板，支持明暗模式

# 背景颜色
BG_COLOR_BASE = "palette(base)"
BG_COLOR_ALTERNATE = "palette(alternate-base)"

# ============ 字体系统 ============
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 12
FONT_SIZE_MEDIUM = 13
FONT_SIZE_LARGE = 14

# ============ GroupBox样式 ============
def get_groupbox_style(border_style="dashed"):
    """
    获取统一的GroupBox样式
    
    Args:
        border_style: 边框样式 "solid" 或 "dashed"
    """
    return f"""
        QGroupBox {{
            border: 1px {border_style} {BORDER_COLOR_MEDIUM};
            border-radius: 4px;
            padding: {PADDING_LARGE}px;
            margin-top: {SPACING_SMALL}px;
            margin-bottom: {SPACING_MEDIUM}px;
            margin-left: {SPACING_SMALL}px;
            margin-right: {SPACING_SMALL}px;
        }}
        QGroupBox::title {{
            font-weight: bold;
            color: {TEXT_COLOR_SECONDARY};
            padding: 0 {SPACING_SMALL}px;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: {SPACING_MEDIUM}px;
        }}
    """

# ============ 分隔线样式 ============
def get_separator_style():
    """获取统一的分隔线样式"""
    return f"""
        border: none;
        border-top: 1px dashed {SEPARATOR_COLOR};
        margin-top: {SPACING_MEDIUM}px;
        margin-bottom: {SPACING_MEDIUM}px;
        background: none;
    """

# ============ 表单布局规范 ============
FORM_LABEL_WIDTH = 150          # 表单标签宽度
FORM_SPACING = SPACING_MEDIUM   # 表单项之间的间距
FORM_MARGIN = MARGIN_MEDIUM     # 表单边距

# ============ 标准按钮样式 ============
STANDARD_BUTTON_MIN_WIDTH = 120  # 标准按钮最小宽度
STANDARD_BUTTON_PADDING = "5px 12px"  # 标准按钮内边距

def get_standard_button_style(min_width=STANDARD_BUTTON_MIN_WIDTH):
    """
    获取标准按钮样式
    
    Args:
        min_width: 最小宽度（默认 120px）
    
    Returns:
        str: 按钮的 CSS 样式字符串
    """
    return f"""
        QPushButton {{
            padding: {STANDARD_BUTTON_PADDING};
            text-align: center;
            min-width: {min_width}px;
        }}
    """


def get_toolbutton_menu_style():
    """
    获取带下拉菜单的 QToolButton 样式
    
    Returns:
        str: QToolButton 的 CSS 样式字符串
    """
    # 解析标准 padding
    padding_parts = STANDARD_BUTTON_PADDING.split()
    vertical_padding = padding_parts[0] if len(padding_parts) > 0 else "5px"
    horizontal_padding = padding_parts[1] if len(padding_parts) > 1 else "12px"
    
    return f"""
        QToolButton {{
            padding-top: {vertical_padding};
            padding-bottom: {vertical_padding};
            padding-left: {horizontal_padding};
            padding-right: 30px;
            text-align: left;
            font-size: 13px;
        }}
        QToolButton::menu-indicator {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            right: 8px;
            width: 12px;
            height: 12px;
        }}
    """


# ============ 按钮加载动画工具类 ============
class ButtonLoadingAnimation:
    """
    按钮加载动画工具类
    提供统一的按钮加载动画效果，避免重复代码
    
    使用示例:
        # 创建动画实例
        self.loading_animation = ButtonLoadingAnimation(
            button=self.my_button,
            loading_text='加载中',
            original_text='加载模型'
        )
        
        # 开始加载
        self.loading_animation.start()
        
        # 停止加载
        self.loading_animation.stop()
    """
    
    def __init__(self, button, loading_text='Loading', original_text=None, interval=250, min_display_time=500):
        """
        初始化按钮加载动画
        
        Args:
            button: QPushButton 实例
            loading_text: 加载时显示的文本（默认 'Loading'）
            original_text: 原始按钮文本（如果为 None，则使用按钮当前文本）
            interval: 动画更新间隔（毫秒，默认 250ms）
            min_display_time: 最小显示时间（毫秒，默认 500ms），避免闪烁
        """
        from PyQt5.QtCore import QTimer
        import time
        
        self.button = button
        self.loading_text = loading_text
        self.original_text = original_text if original_text else button.text()
        self.interval = interval
        self.min_display_time = min_display_time
        
        self.timer = None
        self.dots = ['', '.', '..', '...']
        self.current_dot_index = 0
        self.is_running = False
        self.start_time = None  # 记录开始时间
        self.pending_stop = False  # 标记是否有待处理的停止请求
    
    def start(self):
        """开始加载动画"""
        if self.is_running:
            return
        
        from PyQt5.QtCore import QTimer
        import time
        
        self.is_running = True
        self.current_dot_index = 0
        self.start_time = time.time()  # 记录开始时间
        self.pending_stop = False  # 重置待处理停止标记
        
        # 禁用按钮
        self.button.setEnabled(False)
        
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(self.interval)
        
        # 立即更新一次
        self._update_animation()
    
    def stop(self, restore_text=True):
        """
        停止加载动画
        
        Args:
            restore_text: 是否恢复原始文本（默认 True）
        """
        if not self.is_running:
            return
        
        import time
        from PyQt5.QtCore import QTimer
        
        # 计算已经运行的时间
        if self.start_time is not None:
            elapsed_time = (time.time() - self.start_time) * 1000  # 转换为毫秒
            
            # 如果运行时间小于最小显示时间，延迟停止
            if elapsed_time < self.min_display_time:
                remaining_time = int(self.min_display_time - elapsed_time)
                self.pending_stop = True
                
                # 使用 QTimer 延迟停止
                QTimer.singleShot(remaining_time, lambda: self._do_stop(restore_text))
                return
        
        # 立即停止
        self._do_stop(restore_text)
    
    def _do_stop(self, restore_text=True):
        """实际执行停止操作（内部方法）"""
        if not self.is_running and not self.pending_stop:
            return
        
        self.is_running = False
        self.pending_stop = False
        
        # 停止定时器
        if self.timer is not None:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        
        # 恢复按钮状态
        self.button.setEnabled(True)
        if restore_text:
            self.button.setText(self.original_text)
    
    def _update_animation(self):
        """更新动画（内部方法）"""
        if not self.is_running:
            return
        
        # 更新按钮文本
        self.button.setText(f"{self.loading_text}{self.dots[self.current_dot_index]}")
        
        # 更新点的索引
        self.current_dot_index = (self.current_dot_index + 1) % len(self.dots)
    
    def set_loading_text(self, text):
        """
        设置加载文本
        
        Args:
            text: 新的加载文本
        """
        self.loading_text = text
    
    def set_original_text(self, text):
        """
        设置原始文本
        
        Args:
            text: 新的原始文本
        """
        self.original_text = text
    
    def is_active(self):
        """
        检查动画是否正在运行
        
        Returns:
            bool: 动画是否正在运行
        """
        return self.is_running
