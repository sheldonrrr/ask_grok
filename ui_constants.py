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

# Ask 弹窗专用间距（更紧凑的布局）
SPACING_ASK_COMPACT = SPACING_UNIT // 2    # 4px - 区域内部元素间距
SPACING_ASK_SECTION = SPACING_SMALL          # 8px - 区域之间的间距（统一为 8px）

# Ask 弹窗布局尺寸
ASK_INPUT_HEIGHT = 60
ASK_INPUT_HEIGHT_COMPACT = 52
ASK_COMBO_MIN_WIDTH = 140
# 历史记录等 QToolButton 右侧为下拉箭头预留的空间
ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE = 36
ASK_METADATA_COLLAPSED_HEIGHT = 24
ASK_RESPONSE_PANEL_MIN_HEIGHT = 120


def configure_ask_dialog_root(layout):
    """Ask 弹窗根布局：边距与区块间距。"""
    if layout is None:
        return
    layout.setContentsMargins(MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM, MARGIN_MEDIUM)
    layout.setSpacing(SPACING_SMALL)


def reset_application_cursor():
    """清除 QApplication 可能残留的全局等待/忙碌光标（如 Calibre 读元数据后未恢复）。"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        return
    while app.overrideCursor() is not None:
        app.restoreOverrideCursor()


def configure_ask_dialog_cursors(dialog):
    """Ask 弹窗显示后统一恢复箭头光标，避免继承 loading 状态。"""
    from PyQt5.QtCore import Qt

    reset_application_cursor()
    if dialog is None:
        return
    dialog.setCursor(Qt.ArrowCursor)
    for attr in ('ask_toolbar', 'metadata_bar', 'input_area'):
        widget = getattr(dialog, attr, None)
        if widget is not None:
            widget.setCursor(Qt.ArrowCursor)
    for panel in getattr(dialog, 'response_panels', None) or []:
        area = getattr(panel, 'response_area', None)
        if area is None:
            continue
        area.setCursor(Qt.ArrowCursor)
        viewport = area.viewport()
        if viewport is not None:
            viewport.setCursor(Qt.ArrowCursor)


def get_ask_metadata_collapsed_style():
    """可折叠元数据栏摘要行样式（与设置页 section 标题同色，适配明暗主题）。"""
    return f"""
        color: {TEXT_COLOR_PRIMARY};
        font-size: {FONT_SIZE_SMALL};
        font-weight: bold;
        padding: 2px 0;
    """


def get_ask_metadata_toggle_style():
    """元数据展开/收起按钮样式。"""
    return f"""
        QPushButton {{
            border: none;
            background: transparent;
            color: {TEXT_COLOR_PRIMARY};
            padding: 0 4px;
            min-width: 20px;
        }}
    """

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
# 工具栏行高：控件 32px + 上下留白（容纳边框与焦点环，避免父容器裁切）
ASK_TOOLBAR_INSET_V = 2
ASK_TOOLBAR_HEIGHT = BUTTON_HEIGHT + ASK_TOOLBAR_INSET_V * 2
ASK_TOOLBAR_BUTTON_MIN_WIDTH = 100
# 样式表 height 为内容区，1px 边框各占一侧，合计 BUTTON_HEIGHT
ASK_TOOLBAR_CONTROL_INNER_HEIGHT = BUTTON_HEIGHT - 2

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
TEXT_COLOR_SECONDARY_STRONG = "palette(text)"  # 用于说明/提示文本，浅色主题下更易读
TEXT_COLOR_DISABLED = "palette(mid)"  # 使用 Qt 调色板，支持明暗模式

# 背景颜色
BG_COLOR_BASE = "palette(base)"
BG_COLOR_ALTERNATE = "palette(alternate-base)"

# ============ 字体系统 ============
# 使用相对单位 em，支持用户自定义字体大小
FONT_SIZE_SMALL = '0.9em'
FONT_SIZE_NORMAL = '1em'
FONT_SIZE_MEDIUM = '1.08em'
FONT_SIZE_LARGE = '1.15em'

# 回答区排版
RESPONSE_FONT_FAMILY = (
    "-apple-system, 'Segoe UI', 'Ubuntu', 'PingFang SC', 'Microsoft YaHei', sans-serif"
)
RESPONSE_LINE_HEIGHT = '1.65'
RESPONSE_CODE_FONT_FAMILY = "'Consolas', 'Menlo', 'Ubuntu Mono', monospace"


def get_response_area_qss():
    """QTextBrowser 容器样式（内边距由 document margin 承担）。"""
    return """
        QTextBrowser {
            border: 1px solid palette(mid);
            color: palette(text);
            border-radius: 4px;
            padding: 0;
            background: palette(base);
        }
    """


def get_response_content_stylesheet():
    """回答区 Markdown 内容样式（用于 document().setDefaultStyleSheet）。"""
    return f"""
        .response-body {{
            color: palette(text);
            font-family: {RESPONSE_FONT_FAMILY};
            line-height: {RESPONSE_LINE_HEIGHT};
        }}
        p {{
            margin: 0.4em 0;
            line-height: {RESPONSE_LINE_HEIGHT};
        }}
        h1 {{
            font-size: {FONT_SIZE_LARGE};
            font-weight: bold;
            margin: 0.6em 0 0.4em 0;
            line-height: 1.4;
        }}
        h2 {{
            font-size: {FONT_SIZE_MEDIUM};
            font-weight: bold;
            margin: 0.5em 0 0.35em 0;
            line-height: 1.4;
        }}
        h3, h4, h5, h6 {{
            font-size: {FONT_SIZE_NORMAL};
            font-weight: bold;
            margin: 0.45em 0 0.3em 0;
            line-height: 1.4;
        }}
        ul, ol {{
            margin: 0.5em 0;
            padding-left: 1.5em;
        }}
        li {{
            margin-bottom: 0.25em;
            line-height: {RESPONSE_LINE_HEIGHT};
        }}
        blockquote {{
            margin: 0.5em 0;
            padding-left: 1em;
            color: palette(dark);
        }}
        hr {{
            border: none;
            border-top: 1px solid palette(mid);
            margin: 0.8em 0;
        }}
        strong, b {{ font-weight: bold; }}
        em, i {{ font-style: italic; }}
        code, .inline-code {{
            background-color: palette(alternate-base);
            padding: 2px 4px;
            border-radius: 3px;
            font-family: {RESPONSE_CODE_FONT_FAMILY};
        }}
        pre, .code-block {{
            background-color: palette(alternate-base);
            padding: 10px;
            border-radius: 4px;
            margin: 0.6em 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: {RESPONSE_CODE_FONT_FAMILY};
        }}
        pre code, .code-block .inline-code {{
            background: none;
            padding: 0;
            border-radius: 0;
        }}
        table, .md-table {{
            border-collapse: collapse;
            width: 100%;
            margin: 0.6em 0;
        }}
        th, td {{
            border: 1px solid palette(mid);
            padding: 6px 10px;
            text-align: left;
        }}
        th {{
            background-color: palette(alternate-base);
            font-weight: bold;
        }}
        a {{
            color: palette(link);
            text-decoration: underline;
        }}
        .reasoning-process {{
            background-color: palette(alternate-base);
            color: palette(text);
            padding: 10px;
            margin: 0.6em 0;
            border-radius: 4px;
            font-size: {FONT_SIZE_SMALL};
        }}
        .reasoning-process-title {{
            font-weight: bold;
            color: palette(link);
            margin-bottom: 6px;
        }}
        .reasoning-process-footer {{
            margin-top: 6px;
            padding-top: 6px;
            border-top: 1px solid palette(mid);
            font-size: {FONT_SIZE_SMALL};
            color: palette(dark);
            text-align: right;
        }}
        .reasoning-process-body {{
            white-space: pre-wrap;
            font-family: {RESPONSE_CODE_FONT_FAMILY};
            line-height: {RESPONSE_LINE_HEIGHT};
        }}
    """


def get_reasoning_process_html(title, body_html, footer=None, incomplete=False):
    """推理块 HTML（极简 palette 样式，供 response_handler 使用）。"""
    footer_html = ''
    if footer:
        footer_html = f'<div class="reasoning-process-footer">{footer}</div>'
    incomplete_class = ' reasoning-process-incomplete' if incomplete else ''
    return (
        f'<div class="reasoning-process{incomplete_class}">'
        f'<div class="reasoning-process-title">{title}</div>'
        f'<div>{body_html}</div>'
        f'{footer_html}'
        f'</div>'
    )


# ============ GroupBox / Section 样式（兼容别名 → 设置弹窗规范） ============
def get_groupbox_style(border_style="none"):
    return get_settings_groupbox_style(border_style)


def get_section_title_style():
    return get_settings_title_style()


def get_first_section_title_style():
    return get_settings_title_style()


def get_subtitle_style():
    return get_settings_subtitle_style()


def get_separator_style():
    """分隔线：外边距由 layout 承担，避免与 section 内间距叠加。"""
    return f"""
        border: none;
        border-top: 1px dashed {SEPARATOR_COLOR};
        margin: 0;
        background: none;
    """

# ============ 表单布局规范 ============
FORM_LABEL_WIDTH = 150          # 表单标签宽度
FORM_SPACING = SPACING_MEDIUM   # 表单项之间的间距
FORM_MARGIN = MARGIN_MEDIUM     # 表单边距

# ============ 设置弹窗布局规范（对齐 tradsimp configure_layout 分层） ============
# 外层 content → section 块之间 SETTINGS_SECTION_GAP
# section 内 title / subtitle / groupbox → SETTINGS_SECTION_INNER
SETTINGS_CONTENT_MARGIN = SPACING_SMALL       # 8px — Tab 滚动内容区边距
SETTINGS_SECTION_GAP = 12                     # 12px — section 块之间（tradsimp SECTION_SPACING）
SETTINGS_SECTION_INNER = SPACING_SMALL        # 8px — section 内部元素
SETTINGS_FORM_ROW = SPACING_SMALL             # 8px — 表单行
SETTINGS_RADIO_ROW = 6                        # 6px — 单选/紧凑列表
SETTINGS_FOOTER_TOP = 12                      # 12px — 底部按钮区上方


def configure_layout(layout, role='settings_section'):
    """为布局应用统一的边距与间距（参考 tradsimp ui_style.configure_layout）。"""
    if layout is None:
        return
    if role == 'settings_content':
        layout.setContentsMargins(
            SETTINGS_CONTENT_MARGIN, SETTINGS_CONTENT_MARGIN,
            SETTINGS_CONTENT_MARGIN, SETTINGS_CONTENT_MARGIN,
        )
        layout.setSpacing(SETTINGS_SECTION_GAP)
    elif role == 'settings_section':
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SETTINGS_SECTION_INNER)
    elif role == 'form_row':
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SETTINGS_FORM_ROW)
    elif role == 'radio':
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SETTINGS_RADIO_ROW)
    elif role == 'footer':
        layout.setContentsMargins(0, SETTINGS_FOOTER_TOP, 0, 0)
        layout.setSpacing(SETTINGS_SECTION_INNER)
    elif role == 'zero':
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)


def setup_settings_tab_content(content_widget):
    """设置 Tab 滚动区内容容器布局，返回 content_layout。"""
    from PyQt5.QtWidgets import QVBoxLayout
    content_layout = QVBoxLayout(content_widget)
    configure_layout(content_layout, 'settings_content')
    return content_layout


def get_settings_title_style():
    """Section 标题：间距由 layout 控制，CSS 不设 margin。"""
    return f"""
        font-weight: bold;
        font-size: 1.08em;
        color: {TEXT_COLOR_PRIMARY};
        padding: 0;
        margin: 0;
    """


def get_settings_subtitle_style():
    """Section 副标题：间距由 layout 控制。"""
    return f"""
        color: {TEXT_COLOR_PRIMARY};
        font-size: 1em;
        padding: 0;
        margin: 0;
        opacity: 0.7;
    """


def get_settings_groupbox_style(border_style="none"):
    """GroupBox：无外边距，section 间距仅由 layout 承担。"""
    if border_style == "none":
        return f"""
            QGroupBox {{
                border: none;
                background-color: palette(window);
                border-radius: 6px;
                padding: {PADDING_LARGE}px;
                margin: 0;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0;
                margin: 0;
            }}
        """
    return f"""
        QGroupBox {{
            border: 1px {border_style} {BORDER_COLOR_MEDIUM};
            border-radius: 4px;
            padding: {PADDING_LARGE}px;
            margin: 0;
        }}
        QGroupBox::title {{
            font-weight: bold;
            color: {TEXT_COLOR_SECONDARY_STRONG};
            padding: 0 {SPACING_SMALL}px;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: {SPACING_MEDIUM}px;
        }}
    """


def add_settings_section(content_layout, title_text, subtitle_text=None, subtitle_style=None):
    """
    向设置 Tab 添加一个 section 块（title + 可选 subtitle + 内容由调用方加入 section_layout）。
    返回 (section_layout, title_label, subtitle_label_or_None)。
    """
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

    section = QWidget()
    section.setObjectName('settings_section')
    section_layout = QVBoxLayout(section)
    configure_layout(section_layout, 'settings_section')

    title_label = QLabel(title_text)
    title_label.setStyleSheet(get_settings_title_style())
    section_layout.addWidget(title_label)

    subtitle_label = None
    if subtitle_text is not None:
        subtitle_label = QLabel(subtitle_text)
        subtitle_label.setWordWrap(True)
        style = subtitle_style or get_settings_subtitle_style()
        subtitle_label.setStyleSheet(style)
        section_layout.addWidget(subtitle_label)

    content_layout.addWidget(section)
    return section_layout, title_label, subtitle_label


# ============ Tab 内容布局规范（兼容别名） ============
TAB_OUTER_MARGIN = SPACING_SMALL
TAB_CONTENT_MARGIN = SETTINGS_CONTENT_MARGIN
TAB_CONTENT_SPACING = SETTINGS_SECTION_GAP

def setup_tab_widget_layout(widget):
    """
    为 Tab Widget 设置统一的主布局
    
    所有配置 Tab 都应该调用此函数来确保布局完全一致。
    
    Args:
        widget: QWidget 实例（Tab 页面）
    
    Returns:
        QVBoxLayout: 已配置好的主布局
    
    使用示例:
        def __init__(self, parent=None):
            super().__init__(parent)
            main_layout = setup_tab_widget_layout(self)
            # 然后添加内容到 main_layout
    """
    from PyQt5.QtWidgets import QVBoxLayout
    
    layout = QVBoxLayout()
    layout.setContentsMargins(TAB_OUTER_MARGIN, TAB_OUTER_MARGIN, TAB_OUTER_MARGIN, TAB_OUTER_MARGIN)
    layout.setSpacing(0)
    widget.setLayout(layout)
    return layout

def get_tab_scroll_area_style(object_name="tab_scroll"):
    """
    获取统一的 Tab 滚动区域样式
    
    Args:
        object_name: QScrollArea 的 objectName
    
    Returns:
        str: 滚动区域的 CSS 样式字符串
    """
    return f"""
        QScrollArea#{object_name} {{
            padding: 0px;
            margin: 0px;
            border: none;
        }}
        QScrollArea#{object_name} > QWidget {{
            background: transparent;
        }}
        QScrollArea#{object_name} QWidget#qt_scrollarea_viewport {{
            background: transparent;
            border: none;
            margin: 0px;
            padding: 0px;
        }}
    """

# ============ 标准按钮样式 ============
STANDARD_BUTTON_MIN_WIDTH = 120  # 标准按钮最小宽度
STANDARD_BUTTON_PADDING = "5px 12px"  # 标准按钮内边距

def get_standard_button_style(min_width=STANDARD_BUTTON_MIN_WIDTH):
    """
    获取标准按钮样式
    
    注意：不设置 hover 和 pressed 样式，让 Qt 使用系统默认效果。
    这样可以确保在所有平台（Linux/macOS/Windows）和主题（浅色/深色）下都正常工作。
    
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
            min-height: 1.5em;
        }}
    """


def get_ask_toolbar_pushbutton_style(min_width=ASK_TOOLBAR_BUTTON_MIN_WIDTH):
    """Ask 工具栏 QPushButton：边框计入固定高度，焦点环不溢出容器。"""
    h = ASK_TOOLBAR_CONTROL_INNER_HEIGHT
    return f"""
        QPushButton {{
            min-width: {min_width}px;
            min-height: {h}px;
            max-height: {h}px;
            height: {h}px;
            border: 1px solid palette(mid);
            border-radius: 4px;
            padding: 0 12px;
            margin: 0;
            text-align: center;
        }}
        QPushButton:focus {{
            border: 1px solid palette(highlight);
        }}
    """


def get_ask_toolbar_toolbutton_style(min_width=ASK_COMBO_MIN_WIDTH):
    """Ask 工具栏 QToolButton（历史记录等）：与 PushButton 同高。"""
    arrow_reserve = ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE
    return f"""
        QToolButton {{
            min-width: {min_width}px;
            min-height: {BUTTON_HEIGHT}px;
            max-height: {BUTTON_HEIGHT}px;
            height: {BUTTON_HEIGHT}px;
            padding: 0 {arrow_reserve}px 0 12px;
            margin: 0;
            text-align: left;
        }}
        QToolButton::menu-indicator {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            right: 10px;
            width: 14px;
            height: 14px;
        }}
    """


def elide_ask_toolbar_toolbutton_text(text, font, button_width):
    """为带下拉箭头的工具栏按钮截断文字，避免与箭头重叠。"""
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFontMetrics

    reserve = ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE + 8
    max_width = max(int(button_width) - reserve, 48)
    return QFontMetrics(font).elidedText(text, Qt.ElideRight, max_width)


def get_ask_toolbar_combo_style(min_width=ASK_COMBO_MIN_WIDTH):
    """Ask 工具栏 QComboBox（AI 切换器）：与按钮同高。"""
    return f"""
        QComboBox {{
            min-width: {min_width}px;
            min-height: {BUTTON_HEIGHT}px;
            max-height: {BUTTON_HEIGHT}px;
            height: {BUTTON_HEIGHT}px;
            padding: 0 8px;
            margin: 0;
            text-align: left;
        }}
        QComboBox::drop-down {{
            width: 20px;
            border: none;
        }}
    """


def style_ask_toolbar_widget(widget, min_width=None):
    """为 Ask 工具栏控件应用统一尺寸与样式。"""
    from PyQt5.QtWidgets import QComboBox, QToolButton, QPushButton

    width = min_width or ASK_COMBO_MIN_WIDTH
    widget.setFixedHeight(BUTTON_HEIGHT)
    if hasattr(widget, 'setMinimumWidth'):
        widget.setMinimumWidth(width)
    if isinstance(widget, QComboBox):
        widget.setStyleSheet(get_ask_toolbar_combo_style(width))
    elif isinstance(widget, QToolButton):
        widget.setStyleSheet(get_ask_toolbar_toolbutton_style(width))
    elif isinstance(widget, QPushButton):
        widget.setStyleSheet(get_ask_toolbar_pushbutton_style(width))


# ============ QListWidget 样式 ============
# 列表项内边距（使用相对单位，支持用户自定义字体大小）
LIST_ITEM_PADDING_V = '0.5em'   # 垂直内边距（确保小写字母不被遮挡）
LIST_ITEM_PADDING_H = '0.7em'   # 水平内边距

def get_list_widget_style(with_border_bottom=False):
    """
    获取统一的 QListWidget 样式
    
    Args:
        with_border_bottom: 是否显示项目之间的分隔线
    
    Returns:
        str: QListWidget 的 CSS 样式字符串
    """
    border_bottom = "border-bottom: 1px solid palette(mid);" if with_border_bottom else ""
    last_child_border = "border-bottom: none;" if with_border_bottom else ""
    
    return f"""
        QListWidget {{
            border: 1px solid palette(mid);
            border-radius: 4px;
            background: palette(base);
        }}
        QListWidget::item {{
            padding: {LIST_ITEM_PADDING_V} {LIST_ITEM_PADDING_H};
            border: none;
            margin: 0;
            {border_bottom}
        }}
        QListWidget::item:last-child {{
            {last_child_border}
        }}
        QListWidget::item:selected {{
            background: palette(highlight);
            color: palette(highlighted-text);
            border: none;
            margin: 0;
            padding: {LIST_ITEM_PADDING_V} {LIST_ITEM_PADDING_H};
        }}
        QListWidget::item:hover:!selected {{
            background: palette(alternate-base);
            border: none;
            margin: 0;
            padding: {LIST_ITEM_PADDING_V} {LIST_ITEM_PADDING_H};
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
