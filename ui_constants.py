#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI设计系统常量
定义统一的间距、尺寸、颜色等设计规范
"""
import sys

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
ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE = 42 if sys.platform == 'darwin' else 36
# 折叠摘要行旁的方形按钮边长 = 文字按钮外高（见 button_outer_height）
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
    restored = 0
    while app.overrideCursor() is not None:
        app.restoreOverrideCursor()
        restored += 1
        if restored >= 30:
            break
    # Qt 的光标栈已经空了，但 Fedora 的 Wayland/XWayland 仍会继续播放
    # 之前的转圈光标。压入再弹出一次箭头，强制显示服务更新指针图像。
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QCursor
    app.setOverrideCursor(QCursor(Qt.ArrowCursor))
    app.restoreOverrideCursor()


def _force_widget_cursor(widget, cursor_shape):
    """先清掉再设置，避免 Qt 认为光标没变而跳过系统光标更新。"""
    if widget is None:
        return
    widget.unsetCursor()
    widget.setCursor(cursor_shape)
    viewport = widget.viewport() if hasattr(widget, 'viewport') else None
    if viewport is not None:
        viewport.unsetCursor()
        viewport.setCursor(cursor_shape)


def configure_ask_dialog_cursors(dialog):
    """Ask 弹窗显示后统一恢复箭头光标，避免继承 loading 状态。"""
    from PyQt5.QtCore import Qt

    reset_application_cursor()
    if dialog is None:
        return
    _force_widget_cursor(dialog, Qt.ArrowCursor)
    for attr in ('ask_toolbar', 'metadata_bar'):
        _force_widget_cursor(getattr(dialog, attr, None), Qt.ArrowCursor)
    _force_widget_cursor(getattr(dialog, 'input_area', None), Qt.IBeamCursor)
    for panel in getattr(dialog, 'response_panels', None) or []:
        _force_widget_cursor(getattr(panel, 'response_area', None), Qt.ArrowCursor)


def get_ask_metadata_collapsed_style():
    """可折叠元数据栏摘要行样式（与设置页 section 标题同色，适配明暗主题）。"""
    return f"""
        color: {TEXT_COLOR_PRIMARY};
        font-size: {FONT_SIZE_SMALL};
        font-weight: bold;
        padding: 2px 0;
    """


def get_ask_metadata_toggle_style(side, font_css=None):
    """元数据展开/收起：方形图标按钮，边长与文字按钮外高相同。"""
    font_decl = f'font-size: {font_css};' if font_css else ''
    return f"""
        QPushButton {{
            border: none;
            background: transparent;
            color: {TEXT_COLOR_PRIMARY};
            {font_decl}
            padding: 0;
            min-width: {side}px;
            max-width: {side}px;
            min-height: {side}px;
            max-height: {side}px;
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
# 按钮宽度按按钮字号推导。短标签只占文字本身的宽度，长标签在达到上限前尽量多显示字符。
# BUTTON_MIN_WIDTH = button_min_width(font)：约 3 个 “n” 的内容区宽度。
# BUTTON_MAX_WIDTH = button_max_width(font)：约 40 个 “n” 的外宽（含水平内边距和边框）。
BUTTON_MIN_WIDTH_CHARS = 3
BUTTON_MAX_WIDTH_CHARS = 40
BUTTON_MEDIUM_WIDTH = 150
BUTTON_LARGE_WIDTH = 200
# 外高 = 按钮字体的像素大小 + 上下内边距。样式表 min/max-height 写内容区
# （外高减去两侧边框），避免和垂直 padding 叠成另一套高度。
BUTTON_PADDING_V = 4
BUTTON_PADDING_H = 12
BUTTON_BORDER_PX = 1
# 工具栏行在控件外高之外再留一圈，容纳边框与焦点环，避免父容器裁切。
ASK_TOOLBAR_INSET_V = 2

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
# 按钮文字比正文小 2 个字号。正文是控件继承的应用字体（点或像素，FONT_SIZE_NORMAL = 1em）。
BUTTON_FONT_SIZE_DELTA = 2


def _font_metrics_width(font, text):
    from PyQt5.QtGui import QFontMetrics

    metrics = QFontMetrics(font)
    if hasattr(metrics, 'horizontalAdvance'):
        return metrics.horizontalAdvance(text)
    return metrics.width(text)


def body_font_size(font):
    """正文的单位和字号。点数字体减点，像素字体减像素，不另造一套正文大小。"""
    from PyQt5.QtGui import QFontInfo

    if font is None:
        return None, 0
    if font.pixelSize() > 0:
        return 'px', int(font.pixelSize())
    if font.pointSize() > 0:
        return 'pt', int(font.pointSize())
    info = QFontInfo(font)
    if info.pointSize() > 0:
        return 'pt', int(info.pointSize())
    if info.pixelSize() > 0:
        return 'px', int(info.pixelSize())
    return None, 0


def button_font_from_body(body_font):
    """按钮字体：与正文同一单位，小 BUTTON_FONT_SIZE_DELTA 个字号。"""
    from PyQt5.QtGui import QFont

    font = QFont(body_font)
    unit, size = body_font_size(body_font)
    if not size:
        return font
    smaller = max(1, int(size) - BUTTON_FONT_SIZE_DELTA)
    if unit == 'px':
        font.setPixelSize(smaller)
    else:
        font.setPointSize(smaller)
    return font


def button_font_css(font):
    """样式表 font-size，单位与按钮字体一致。"""
    unit, size = body_font_size(font)
    if not size:
        return None
    return f'{int(size)}{unit}'


def install_button_font(widget):
    """把控件字体设为正文减 2。重复调用不会再减一次。"""
    from PyQt5.QtGui import QFont

    key = 'ask_button_body_size'
    stored = widget.property(key) if widget is not None else None
    if stored:
        unit, _, num = str(stored).partition(':')
        body = QFont(widget.font())
        if unit == 'px':
            body.setPixelSize(int(num))
        else:
            body.setPointSize(int(num))
    else:
        body = QFont(widget.font()) if widget is not None else QFont()
        unit, size = body_font_size(body)
        if widget is not None and size:
            widget.setProperty(key, f'{unit}:{int(size)}')
    font = button_font_from_body(body)
    if widget is not None:
        widget.setFont(font)
    return font


def button_pixel_size(font):
    """按钮字体对应的像素大小，用来推外高。"""
    from PyQt5.QtGui import QFontInfo

    px = QFontInfo(font).pixelSize()
    if px > 0:
        return int(px)
    unit, size = body_font_size(font)
    if unit == 'px':
        return int(size)
    if unit == 'pt' and size:
        return max(1, int(round(size * 96 / 72.0)))
    return 0


def button_outer_height(font):
    """文字按钮外高：按钮字体像素大小 + 上下内边距。"""
    return button_pixel_size(font) + BUTTON_PADDING_V * 2


def button_content_height(font):
    """样式表 min-height 的内容区。两侧边框在内容区之外。"""
    return max(1, button_outer_height(font) - BUTTON_BORDER_PX * 2)


def button_min_width(font):
    """BUTTON_MIN_WIDTH：短标签的内容区下限（像素）。"""
    return max(1, _font_metrics_width(font, 'n' * BUTTON_MIN_WIDTH_CHARS))


def button_max_width(font):
    """BUTTON_MAX_WIDTH：长标签的外宽上限（像素，含水平内边距和边框）。"""
    text = _font_metrics_width(font, 'n' * BUTTON_MAX_WIDTH_CHARS)
    return text + BUTTON_PADDING_H * 2 + BUTTON_BORDER_PX * 2


def _button_metric_declarations(font, min_width):
    """字号、相对高度、最小宽度。不写 max-width，避免纵向布局把短按钮拉到上限。"""
    rules = []
    if font is not None:
        css = button_font_css(font)
        if css:
            rules.append(f'font-size: {css};')
        height = button_content_height(font)
        rules.append(f'min-height: {height}px;')
        rules.append(f'max-height: {height}px;')
    if min_width:
        rules.append(f'min-width: {int(min_width)}px;')
    return '\n            '.join(rules)


def apply_text_button_width(button, font, min_width, max_width=None, stretch=False):
    """短按钮按文字收缩；只有文字宽于上限时才封顶。拉伸按钮交给布局。"""
    from PyQt5.QtWidgets import QSizePolicy, QWIDGETSIZE_MAX

    if stretch or min_width == 0:
        button.setMinimumWidth(0)
        button.setMaximumWidth(QWIDGETSIZE_MAX)
        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    button.setMaximumWidth(QWIDGETSIZE_MAX)
    button.ensurePolished()
    cap = button_max_width(font) if max_width is None else int(max_width)
    if cap and button.sizeHint().width() > cap:
        button.setMaximumWidth(cap)


def style_metadata_toggle_button(button):
    """元数据展开/收起方钮：边长等于文字按钮外高。"""
    font = install_button_font(button)
    side = button_outer_height(font)
    button.setFixedSize(side, side)
    button.setStyleSheet(get_ask_metadata_toggle_style(side, button_font_css(font)))


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
            padding: 0.15em 0 0.15em 1em;
            border-left: 3px solid palette(mid);
            color: palette(text);
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
            color: palette(text);
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
# 只留水平内边距。垂直空间放在 min/max-height 里，避免和内容区高度叠在一起。
STANDARD_BUTTON_PADDING = f"0 {BUTTON_PADDING_H}px"

def get_standard_button_style(min_width=None, padding=None, font=None):
    """
    标准文字按钮样式。字号比正文小 2，高度由按钮字体和内边距推出。

    不设置 hover 和 pressed，让 Qt 使用系统默认按压效果，
    以便在各平台和明暗主题下保持原生观感。
    不写 max-width：纵向布局会把控件拉到最大宽度，短标签就会铺满一行。

    Args:
        min_width: 内容区最小宽度（像素）。None 时由调用方填 button_min_width。
        padding: 内边距；默认 STANDARD_BUTTON_PADDING（垂直为 0）
        font: 已经比正文小 2 个字号的按钮字体

    Returns:
        str: 按钮的 CSS 样式字符串
    """
    pad = STANDARD_BUTTON_PADDING if padding is None else padding
    metrics = _button_metric_declarations(font, min_width)
    return f"""
        QPushButton {{
            padding: {pad};
            text-align: center;
            {metrics}
        }}
    """


def get_ask_toolbar_pushbutton_style(min_width=None, font=None):
    """Ask 工具栏 QPushButton（发送/停止/随机）：字号和高度与标准按钮一致。"""
    is_macos = sys.platform == 'darwin'
    border_decl = "border: 1px solid palette(mid);" if is_macos else ""
    radius_decl = "border-radius: 4px;" if is_macos else ""
    focus_style = (
        "QPushButton:focus {\n            border: 1px solid palette(highlight);\n        }"
        if is_macos else ""
    )
    metrics = _button_metric_declarations(font, min_width)
    return f"""
        QPushButton {{
            {metrics}
            {border_decl}
            {radius_decl}
            padding: 0 {BUTTON_PADDING_H}px;
            margin: 0;
            text-align: center;
        }}
        {focus_style}
    """


def get_ask_toolbar_toolbutton_style(min_width=None, font=None):
    """Ask 工具栏 QToolButton（历史记录等）：与 PushButton 同字号、同高。"""
    arrow_reserve = ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE
    is_macos = sys.platform == 'darwin'
    border_decl = "border: 1px solid palette(mid);" if is_macos else ""
    radius_decl = "border-radius: 4px;" if is_macos else ""
    focus_style = (
        "QToolButton:focus {\n            border: 1px solid palette(highlight);\n        }"
        if is_macos else ""
    )
    indicator_right = 12 if is_macos else 10
    metrics = _button_metric_declarations(font, min_width)
    return f"""
        QToolButton {{
            {metrics}
            {border_decl}
            {radius_decl}
            padding: 0 {arrow_reserve}px 0 {BUTTON_PADDING_H}px;
            margin: 0;
            text-align: left;
        }}
        {focus_style}
        QToolButton::menu-indicator {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            right: {indicator_right}px;
            width: 14px;
            height: 14px;
        }}
    """


def elide_ask_toolbar_toolbutton_text(text, font, button_width):
    """为带下拉箭头的工具栏按钮截断文字，避免与箭头重叠。"""
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFontMetrics

    reserve = ASK_TOOLBAR_TOOLBUTTON_ARROW_RESERVE + (12 if sys.platform == 'darwin' else 8)
    max_width = max(int(button_width) - reserve, 48)
    return QFontMetrics(font).elidedText(text, Qt.ElideRight, max_width)


def get_ask_toolbar_combo_style(min_width=ASK_COMBO_MIN_WIDTH, font=None):
    """Ask 工具栏 QComboBox（AI 切换器）：与按钮同字号、同高。最小宽度仍按内容。"""
    metrics = _button_metric_declarations(font, min_width)
    return f"""
        QComboBox {{
            {metrics}
            padding: 0 8px;
            margin: 0;
            text-align: left;
        }}
        QComboBox::drop-down {{
            width: 20px;
            border: none;
        }}
    """


def _clear_widget_fixed_height(widget):
    """去掉固定像素高度，改由样式表里的相对高度决定。"""
    from PyQt5.QtWidgets import QWIDGETSIZE_MAX

    widget.setMinimumHeight(0)
    widget.setMaximumHeight(QWIDGETSIZE_MAX)


def style_ask_toolbar_widget(widget, min_width=None, max_width=None):
    """为 Ask 工具栏控件应用统一字号、相对高度和宽度。"""
    from PyQt5.QtWidgets import QComboBox, QToolButton, QPushButton, QWIDGETSIZE_MAX

    font = install_button_font(widget)
    _clear_widget_fixed_height(widget)
    if isinstance(widget, QComboBox):
        width = ASK_COMBO_MIN_WIDTH if min_width is None else min_width
        widget.setMinimumWidth(width)
        widget.setStyleSheet(get_ask_toolbar_combo_style(width, font))
    elif isinstance(widget, QToolButton):
        width = button_min_width(font) if min_width is None else min_width
        widget.setMinimumWidth(width)
        widget.setMaximumWidth(QWIDGETSIZE_MAX)
        widget.setStyleSheet(get_ask_toolbar_toolbutton_style(width, font))
    elif isinstance(widget, QPushButton):
        width = button_min_width(font) if min_width is None else min_width
        widget.setStyleSheet(get_ask_toolbar_pushbutton_style(width, font))
        apply_text_button_width(
            widget, font, width, max_width, stretch=(width == 0),
        )


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
    # 解析标准 padding。高度与文字按钮相同，随按钮字号变化。
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import QApplication

    padding_parts = STANDARD_BUTTON_PADDING.split()
    vertical_padding = padding_parts[0] if len(padding_parts) > 0 else "0px"
    horizontal_padding = padding_parts[1] if len(padding_parts) > 1 else f"{BUTTON_PADDING_H}px"
    app = QApplication.instance()
    font = button_font_from_body(app.font() if app is not None else QFont())
    metrics = _button_metric_declarations(font, None)

    return f"""
        QToolButton {{
            padding-top: {vertical_padding};
            padding-bottom: {vertical_padding};
            padding-left: {horizontal_padding};
            padding-right: 30px;
            text-align: left;
            {metrics}
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
