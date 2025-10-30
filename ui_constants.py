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
TEXT_COLOR_SECONDARY = "#666666"
TEXT_COLOR_DISABLED = "#999999"

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
