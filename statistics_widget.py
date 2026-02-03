#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics Widget for Ask AI Plugin.
Displays usage statistics including days using plugin, AI reply count, book collection count,
weekly trends bar chart, and monthly heatmap.
"""

import logging
import json
import random
from datetime import datetime, timedelta
import calendar
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QSizePolicy, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPainterPath

from .config import get_prefs
from .models.base import get_translation
from .ui_constants import (TEXT_COLOR_PRIMARY, TEXT_COLOR_SECONDARY, 
                           SPACING_SMALL, SPACING_MEDIUM, SPACING_LARGE,
                           get_section_title_style, get_subtitle_style)

logger = logging.getLogger(__name__)

# Constants for chart layout
CHART_WIDTH_PERCENT = 0.85  # 85% of container width
CHART_MAX_WIDTH = 800  # Maximum width in pixels
CHART_MIN_WIDTH = 500  # Minimum width in pixels


def get_user_title(reply_count, language='en'):
    """Get user title based on AI reply count."""
    if language.startswith('zh'):
        if reply_count <= 20:
            return '好奇心人士'
        elif reply_count <= 50:
            return '书籍探索者'
        elif reply_count <= 100:
            return '知识渴求者'
        elif reply_count <= 200:
            return '学习热情者'
        else:
            return '智慧追寻者'
    else:
        if reply_count <= 20:
            return 'Curious Explorer'
        elif reply_count <= 50:
            return 'Book Explorer'
        elif reply_count <= 100:
            return 'Knowledge Seeker'
        elif reply_count <= 200:
            return 'Learning Enthusiast'
        else:
            return 'Wisdom Pursuer'


def get_book_response(book_count, language='en'):
    """Get response text based on book collection count."""
    if language.startswith('zh'):
        if book_count <= 50:
            return '真不错！'
        elif book_count <= 200:
            return '很不错啊！'
        elif book_count <= 500:
            return '材料丰富！'
        elif book_count <= 1000:
            return '哇，厉害！'
        else:
            return '太棒了！'
    else:
        if book_count <= 50:
            return "That's impressive!"
        elif book_count <= 200:
            return 'Quite a collection!'
        elif book_count <= 500:
            return 'Great variety!'
        elif book_count <= 1000:
            return "Wow, that's awesome!"
        else:
            return 'Unbelievable!'


def get_month_comment(total_times, language='en', i18n=None):
    """Get comment for monthly heatmap based on total times.
    
    When total_times < 10, returns sample data text from i18n.
    Otherwise returns a comment based on the total times.
    """
    if total_times < 10:
        # Use i18n for sample data text
        if i18n:
            return i18n.get('stat_sample_data', '*This is sample data')
        return '*This is sample data'
    
    if language.startswith('zh'):
        if total_times < 50:
            return '轻松愉快'
        else:
            return '充实的一个月，对吧？'
    else:
        if total_times < 50:
            return 'It was easy.'
        else:
            return 'A fulfilling month, right?'


def format_number_display(number):
    """Format number for display (e.g., 1000+ for numbers over 1000)."""
    if number > 1000:
        return '1000+'
    elif number > 200:
        return '200+'
    return str(number)


def init_statistics(prefs):
    """Initialize statistics if not present."""
    changed = False
    
    # Initialize first use date
    if not prefs.get('stat_first_use_date'):
        prefs['stat_first_use_date'] = datetime.now().strftime('%Y-%m-%d')
        changed = True
    
    # Initialize AI reply count
    if prefs.get('stat_ai_reply_count') is None:
        # Try to get initial count from history
        try:
            from .history_manager import HistoryManager
            history_manager = HistoryManager()
            initial_count = len(history_manager.histories)
            prefs['stat_ai_reply_count'] = initial_count
        except Exception as e:
            logger.warning(f"Failed to get history count for stats init: {e}")
            prefs['stat_ai_reply_count'] = 0
        changed = True
    
    # Initialize book count (will be updated when AI Search updates library)
    if prefs.get('stat_book_count') is None:
        prefs['stat_book_count'] = 0
        changed = True
    
    # Initialize daily stats (for weekly trends and monthly heatmap)
    if prefs.get('stat_daily_counts') is None:
        prefs['stat_daily_counts'] = '{}'
        changed = True
    
    return changed


def increment_ai_reply_count(prefs):
    """Increment AI reply count by 1 and record daily count."""
    current = prefs.get('stat_ai_reply_count', 0)
    prefs['stat_ai_reply_count'] = current + 1
    
    # Record daily count
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        daily_counts = json.loads(prefs.get('stat_daily_counts', '{}'))
    except:
        daily_counts = {}
    
    daily_counts[today] = daily_counts.get(today, 0) + 1
    prefs['stat_daily_counts'] = json.dumps(daily_counts)
    
    logger.info(f"AI reply count incremented to {current + 1}, today: {daily_counts[today]}")


def update_book_count(prefs, count):
    """Update book collection count."""
    prefs['stat_book_count'] = count
    logger.info(f"Book count updated to {count}")


def get_weekly_data(prefs):
    """Get request counts for each day of the current week (Mon-Sun)."""
    try:
        daily_counts = json.loads(prefs.get('stat_daily_counts', '{}'))
    except:
        daily_counts = {}
    
    today = datetime.now()
    # Get Monday of current week
    monday = today - timedelta(days=today.weekday())
    
    weekly_data = []
    for i in range(7):
        day = monday + timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        count = daily_counts.get(day_str, 0)
        weekly_data.append(count)
    
    return weekly_data


def get_monthly_data(prefs):
    """Get request counts for each day of the current month."""
    try:
        daily_counts = json.loads(prefs.get('stat_daily_counts', '{}'))
    except:
        daily_counts = {}
    
    today = datetime.now()
    year, month = today.year, today.month
    
    # Get number of days in current month
    _, num_days = calendar.monthrange(year, month)
    
    monthly_data = {}
    for day in range(1, num_days + 1):
        day_str = f"{year}-{month:02d}-{day:02d}"
        monthly_data[day] = daily_counts.get(day_str, 0)
    
    return monthly_data, year, month, today.day


def generate_sample_weekly_data():
    """Generate random sample data for weekly chart."""
    return [random.randint(1, 8) for _ in range(7)]


def generate_sample_monthly_data(num_days, today):
    """Generate random sample data for monthly heatmap."""
    data = {}
    for day in range(1, num_days + 1):
        # More likely to have data on recent days
        if day <= today:
            if random.random() < 0.6:  # 60% chance of having data
                data[day] = random.randint(1, 5)
            else:
                data[day] = 0
        else:
            data[day] = 0
    return data


class StatCard(QWidget):
    """A card widget displaying a single statistic with number on top."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(2)
        
        # Number + unit in one line
        number_line = QHBoxLayout()
        number_line.setSpacing(4)
        number_line.setAlignment(Qt.AlignCenter)
        
        # Big number label (3x size)
        self.number_label = QLabel()
        self.number_label.setAlignment(Qt.AlignRight | Qt.AlignBaseline)
        self.number_label.setStyleSheet(f"color: {TEXT_COLOR_PRIMARY}; font-size: 2em; font-weight: bold;")
        
        # Unit label (normal size)
        self.unit_label = QLabel()
        self.unit_label.setAlignment(Qt.AlignLeft | Qt.AlignBaseline)
        self.unit_label.setStyleSheet(f"color: {TEXT_COLOR_PRIMARY}; font-size: 0.85em;")
        
        number_line.addStretch()
        number_line.addWidget(self.number_label)
        number_line.addWidget(self.unit_label)
        number_line.addStretch()
        
        # Subtitle label
        self.subtitle_label = QLabel()
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 0.8em;")
        self.subtitle_label.setWordWrap(True)
        
        self.layout.addLayout(number_line)
        self.layout.addWidget(self.subtitle_label)
    
    def set_data(self, number, unit, subtitle=''):
        """Set the card data."""
        self.number_label.setText(str(number))
        self.unit_label.setText(unit)
        self.subtitle_label.setText(subtitle)
        if not subtitle:
            self.subtitle_label.hide()
        else:
            self.subtitle_label.show()


class WeeklyBarChart(QWidget):
    """A bar chart widget showing weekly request counts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = [0] * 7
        self.day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.is_sample = False
        self.sample_tooltip = ''
        self.setMinimumHeight(100)
        self.setMaximumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
    def set_data(self, data, day_labels=None, is_sample=False, sample_tooltip=''):
        """Set the chart data."""
        self.data = data
        if day_labels:
            self.day_labels = day_labels
        self.is_sample = is_sample
        self.sample_tooltip = sample_tooltip
        if is_sample and sample_tooltip:
            self.setToolTip(sample_tooltip)
        else:
            self.setToolTip('')
        self.update()
    
    def paintEvent(self, event):
        """Paint the bar chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get colors from palette
        text_color = self.palette().text().color()
        bar_color = text_color
        
        width = self.width()
        height = self.height()
        
        # Calculate bar dimensions
        num_bars = len(self.data)
        bar_spacing = 10
        total_spacing = bar_spacing * (num_bars + 1)
        bar_width = (width - total_spacing) / num_bars
        bar_width = min(bar_width, 40)  # Max bar width
        
        # Recalculate to center bars
        actual_width = num_bars * bar_width + (num_bars + 1) * bar_spacing
        offset_x = (width - actual_width) / 2
        
        # Leave space for labels
        label_height = 18
        chart_height = height - label_height - 8
        
        # Find max value for scaling
        max_val = max(self.data) if max(self.data) > 0 else 1
        
        # Draw bars
        for i, value in enumerate(self.data):
            x = offset_x + bar_spacing + i * (bar_width + bar_spacing)
            bar_h = (value / max_val) * (chart_height - 15) if max_val > 0 else 0
            bar_h = max(bar_h, 4) if value > 0 else 4  # Minimum height
            y = chart_height - bar_h
            
            # Create rounded rect path (round top, flat bottom)
            path = QPainterPath()
            radius = min(5, bar_width / 3)
            
            # Start from bottom left
            path.moveTo(x, chart_height)
            # Line to top left (with curve)
            path.lineTo(x, y + radius)
            path.quadTo(x, y, x + radius, y)
            # Line to top right (with curve)
            path.lineTo(x + bar_width - radius, y)
            path.quadTo(x + bar_width, y, x + bar_width, y + radius)
            # Line to bottom right
            path.lineTo(x + bar_width, chart_height)
            path.closeSubpath()
            
            # Fill bar
            if value > 0:
                painter.fillPath(path, QBrush(bar_color))
            else:
                # Light color for zero values
                light_color = QColor(bar_color)
                light_color.setAlpha(40)
                painter.fillPath(path, QBrush(light_color))
            
            # Draw day label
            painter.setPen(QPen(text_color))
            font = painter.font()
            font.setPointSize(8)
            painter.setFont(font)
            label_rect = self.rect()
            label_rect.setLeft(int(x))
            label_rect.setWidth(int(bar_width))
            label_rect.setTop(int(chart_height + 3))
            label_rect.setHeight(label_height)
            painter.drawText(label_rect, Qt.AlignCenter, self.day_labels[i])
        
        painter.end()


class MonthlyHeatmap(QWidget):
    """A calendar heatmap widget showing monthly request counts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.today = datetime.now().day
        self.is_sample = False
        self.sample_tooltip = ''
        self.setMinimumHeight(200)  # Increased from 160 for larger cells
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
    def set_data(self, data, year, month, today, is_sample=False, sample_tooltip=''):
        """Set the heatmap data."""
        self.data = data
        self.year = year
        self.month = month
        self.today = today
        self.is_sample = is_sample
        self.sample_tooltip = sample_tooltip
        if is_sample and sample_tooltip:
            self.setToolTip(sample_tooltip)
        else:
            self.setToolTip('')
        self.update()
    
    def paintEvent(self, event):
        """Paint the heatmap calendar."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get colors from palette
        text_color = self.palette().text().color()
        bg_color = self.palette().window().color()
        base_color = self.palette().base().color()
        
        # Calculate reverse color for text on filled cells
        reverse_color = QColor(255 - text_color.red(), 255 - text_color.green(), 255 - text_color.blue())
        
        # Orange color for today
        today_color = QColor(255, 149, 0)  # Orange
        
        width = self.width()
        height = self.height()
        
        # Get calendar info
        _, num_days = calendar.monthrange(self.year, self.month)
        first_weekday = calendar.monthrange(self.year, self.month)[0]  # 0=Monday
        
        # Calculate cell dimensions
        cell_padding = 3
        cols = 7
        rows = (num_days + first_weekday + 6) // 7
        
        cell_width = (width - cell_padding * (cols + 1)) / cols
        cell_height = (height - cell_padding * (rows + 1)) / rows
        cell_size = min(cell_width, cell_height, 38)  # Increased from 32 for larger fonts
        
        # Center the grid
        grid_width = cols * cell_size + (cols + 1) * cell_padding
        grid_height = rows * cell_size + (rows + 1) * cell_padding
        offset_x = (width - grid_width) / 2
        offset_y = (height - grid_height) / 2
        
        # Draw cells
        day = 1
        for row in range(rows):
            for col in range(cols):
                if row == 0 and col < first_weekday:
                    continue
                if day > num_days:
                    break
                
                x = offset_x + cell_padding + col * (cell_size + cell_padding)
                y = offset_y + cell_padding + row * (cell_size + cell_padding)
                
                count = self.data.get(day, 0)
                is_today = (day == self.today)
                
                # Create rounded rect
                rect_path = QPainterPath()
                rect_path.addRoundedRect(x, y, cell_size, cell_size, 4, 4)
                
                # Determine colors
                if is_today:
                    fill_color = today_color
                    txt_color = reverse_color
                elif count > 0:
                    fill_color = text_color
                    txt_color = reverse_color
                else:
                    # Light background for empty days
                    fill_color = QColor(text_color)
                    fill_color.setAlpha(20)
                    txt_color = text_color
                
                # Fill cell
                painter.fillPath(rect_path, QBrush(fill_color))
                
                # Draw day number and count
                painter.setPen(QPen(txt_color))
                font = painter.font()
                font.setPointSize(10)  # Increased from 8
                font.setBold(True)
                painter.setFont(font)
                
                # Day number at top
                day_rect = self.rect()
                day_rect.setLeft(int(x))
                day_rect.setTop(int(y + 1))
                day_rect.setWidth(int(cell_size))
                day_rect.setHeight(int(cell_size / 2))
                painter.drawText(day_rect, Qt.AlignCenter, str(day))
                
                # Count at bottom (if > 0)
                if count > 0:
                    font.setPointSize(8)  # Increased from 6
                    font.setBold(False)
                    painter.setFont(font)
                    count_rect = self.rect()
                    count_rect.setLeft(int(x))
                    count_rect.setTop(int(y + cell_size / 2))
                    count_rect.setWidth(int(cell_size))
                    count_rect.setHeight(int(cell_size / 2 - 1))
                    painter.drawText(count_rect, Qt.AlignCenter, str(count))
                
                day += 1
        
        painter.end()


class SectionContainer(QFrame):
    """A container with light background for chart sections."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            SectionContainer {
                background-color: palette(window);
                border: none;
                border-radius: 8px;
            }
        """)


class StatisticsWidget(QWidget):
    """Statistics page widget - displays usage statistics."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        prefs = get_prefs()
        self.language = prefs.get('language', 'en') if hasattr(prefs, 'get') and callable(prefs.get) else 'en'
        self.i18n = get_translation(self.language)
        
        # Initialize statistics if needed
        if init_statistics(prefs):
            logger.info("Statistics initialized")
        
        self.setup_ui()
        self.refresh_stats()
    
    def setup_ui(self):
        """Setup the UI layout."""
        from .ui_constants import setup_tab_widget_layout, TAB_CONTENT_MARGIN
        
        main_layout = setup_tab_widget_layout(self)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN, 
                                          TAB_CONTENT_MARGIN, TAB_CONTENT_MARGIN)
        content_layout.setSpacing(SPACING_MEDIUM)
        
        # ========== Section 1: Overview ==========
        self.overview_title = QLabel(self.i18n.get('stat_overview', 'Overview'))
        self.overview_title.setStyleSheet(f"font-weight: bold; font-size: 1.1em; color: {TEXT_COLOR_PRIMARY};")
        content_layout.addWidget(self.overview_title)
        
        # Overview container with background - centered, 70% width, max-width
        overview_container_wrapper = QHBoxLayout()
        overview_container_wrapper.addStretch()
        
        self.overview_container = SectionContainer()
        self.overview_container.setMinimumWidth(CHART_MIN_WIDTH)
        self.overview_container.setMaximumWidth(CHART_MAX_WIDTH)
        overview_inner = QHBoxLayout(self.overview_container)
        overview_inner.setContentsMargins(8, 12, 8, 12)
        overview_inner.setSpacing(0)
        
        # Card 1: Days using plugin
        self.days_card = StatCard()
        overview_inner.addWidget(self.days_card, 1)
        
        # Separator 1
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.VLine)
        sep1.setStyleSheet("color: palette(mid); max-height: 40px;")
        overview_inner.addWidget(sep1)
        
        # Card 2: AI Reply count
        self.replies_card = StatCard()
        overview_inner.addWidget(self.replies_card, 1)
        
        # Separator 2
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setStyleSheet("color: palette(mid); max-height: 40px;")
        overview_inner.addWidget(sep2)
        
        # Card 3: Book collection
        self.books_card = StatCard()
        overview_inner.addWidget(self.books_card, 1)
        
        overview_container_wrapper.addWidget(self.overview_container)
        overview_container_wrapper.addStretch()
        content_layout.addLayout(overview_container_wrapper)
        
        content_layout.addSpacing(SPACING_MEDIUM)
        
        # ========== Section 2: Trends (Weekly Bar Chart) ==========
        # Header with title on left, avg on right - same line
        trends_header = QHBoxLayout()
        trends_header.setSpacing(SPACING_SMALL)
        
        # Left side: title and subtitle in vertical layout
        trends_left = QVBoxLayout()
        trends_left.setSpacing(2)
        
        self.trends_title = QLabel(self.i18n.get('stat_trends', 'Trends'))
        self.trends_title.setStyleSheet(f"font-weight: bold; font-size: 1.1em; color: {TEXT_COLOR_PRIMARY};")
        trends_left.addWidget(self.trends_title)
        
        self.trends_subtitle = QLabel(self.i18n.get('stat_curious_index', 'Curious Index this week'))
        self.trends_subtitle.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 0.85em;")
        trends_left.addWidget(self.trends_subtitle)
        
        trends_header.addLayout(trends_left)
        trends_header.addStretch()
        
        # Right side: daily average - align with title
        self.trends_avg_label = QLabel()
        self.trends_avg_label.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 0.85em;")
        self.trends_avg_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        trends_header.addWidget(self.trends_avg_label, 0, Qt.AlignBottom)
        
        content_layout.addLayout(trends_header)
        
        # Bar chart container - centered, 70% width, max-width, with background
        trends_container_wrapper = QHBoxLayout()
        trends_container_wrapper.addStretch()
        
        self.trends_container = SectionContainer()
        self.trends_container.setMinimumWidth(CHART_MIN_WIDTH)
        self.trends_container.setMaximumWidth(CHART_MAX_WIDTH)
        trends_inner = QVBoxLayout(self.trends_container)
        trends_inner.setContentsMargins(12, 12, 12, 8)
        
        self.weekly_chart = WeeklyBarChart()
        trends_inner.addWidget(self.weekly_chart)
        
        trends_container_wrapper.addWidget(self.trends_container)
        trends_container_wrapper.addStretch()
        content_layout.addLayout(trends_container_wrapper)
        
        content_layout.addSpacing(SPACING_MEDIUM)
        
        # ========== Section 3: Heatmap (Monthly Calendar) ==========
        # Header with title on left, comment on right - same line
        heatmap_header = QHBoxLayout()
        heatmap_header.setSpacing(SPACING_SMALL)
        
        # Left side: title and subtitle
        heatmap_left = QVBoxLayout()
        heatmap_left.setSpacing(2)
        
        self.heatmap_title = QLabel(self.i18n.get('stat_heatmap', 'Heatmap'))
        self.heatmap_title.setStyleSheet(f"font-weight: bold; font-size: 1.1em; color: {TEXT_COLOR_PRIMARY};")
        heatmap_left.addWidget(self.heatmap_title)
        
        self.heatmap_subtitle = QLabel()
        self.heatmap_subtitle.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 0.85em;")
        heatmap_left.addWidget(self.heatmap_subtitle)
        
        heatmap_header.addLayout(heatmap_left)
        heatmap_header.addStretch()
        
        # Right side: comment - align with title
        self.heatmap_comment = QLabel()
        self.heatmap_comment.setStyleSheet(f"color: {TEXT_COLOR_SECONDARY}; font-size: 0.85em;")
        self.heatmap_comment.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        heatmap_header.addWidget(self.heatmap_comment, 0, Qt.AlignBottom)
        
        content_layout.addLayout(heatmap_header)
        
        # Heatmap container - centered, 70% width, max-width, with background
        heatmap_container_wrapper = QHBoxLayout()
        heatmap_container_wrapper.addStretch()
        
        self.heatmap_container = SectionContainer()
        self.heatmap_container.setMinimumWidth(CHART_MIN_WIDTH)
        self.heatmap_container.setMaximumWidth(CHART_MAX_WIDTH)
        heatmap_inner = QVBoxLayout(self.heatmap_container)
        heatmap_inner.setContentsMargins(12, 12, 12, 8)
        
        self.monthly_heatmap = MonthlyHeatmap()
        heatmap_inner.addWidget(self.monthly_heatmap)
        
        heatmap_container_wrapper.addWidget(self.heatmap_container)
        heatmap_container_wrapper.addStretch()
        content_layout.addLayout(heatmap_container_wrapper)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def refresh_stats(self):
        """Refresh statistics display."""
        prefs = get_prefs()
        self.language = prefs.get('language', 'en')
        self.i18n = get_translation(self.language)
        
        # Get tooltip text for sample data
        sample_tooltip = self.i18n.get('stat_data_not_enough', 'Data is not enough')
        
        # ========== Overview Cards ==========
        # Card 1: Days using plugin
        first_use_date_str = prefs.get('stat_first_use_date')
        if first_use_date_str:
            try:
                first_use_date = datetime.strptime(first_use_date_str, '%Y-%m-%d')
                days = (datetime.now() - first_use_date).days + 1
                # Only show date like 12.31.2026 for cleaner layout
                formatted_date = first_use_date.strftime('%m.%d.%Y')
                
                days_unit = self.i18n.get('stat_days_unit', 'days')
                self.days_card.set_data(days, days_unit, formatted_date)
            except Exception as e:
                logger.error(f"Error parsing first use date: {e}")
                self.days_card.set_data(1, self.i18n.get('stat_days_unit', 'days'), '')
        else:
            self.days_card.set_data(1, self.i18n.get('stat_days_unit', 'days'), '')
        
        # Card 2: AI Reply count
        reply_count = prefs.get('stat_ai_reply_count', 0)
        reply_display = format_number_display(reply_count) if reply_count > 200 else str(reply_count)
        replies_unit = self.i18n.get('stat_replies_unit', 'times')
        user_title = get_user_title(reply_count, self.language)
        self.replies_card.set_data(reply_display, replies_unit, user_title)
        
        # Card 3: Book collection
        book_count = prefs.get('stat_book_count', 0)
        book_display = format_number_display(book_count)
        books_unit = self.i18n.get('stat_books_unit', 'books')
        book_response = get_book_response(book_count, self.language) if book_count > 0 else self.i18n.get('stat_no_books', 'Update in Search tab')
        self.books_card.set_data(book_display, books_unit, book_response)
        
        # ========== Weekly Trends ==========
        weekly_data = get_weekly_data(prefs)
        total_week = sum(weekly_data)
        
        # Day labels based on language
        if self.language.startswith('zh'):
            day_labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        else:
            day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Check if we need sample data
        is_sample_week = total_week < 10
        if is_sample_week:
            # Use sample data for display
            display_data = generate_sample_weekly_data()
            self.weekly_chart.set_data(display_data, day_labels, is_sample=True, sample_tooltip=sample_tooltip)
            self.trends_avg_label.setText(self.i18n.get('stat_sample_data', '*This is sample data'))
        else:
            self.weekly_chart.set_data(weekly_data, day_labels, is_sample=False)
            avg = total_week / 7
            avg_text = self.i18n.get('stat_daily_avg', 'Daily average {n} times').format(n=f"{avg:.1f}")
            self.trends_avg_label.setText(avg_text)
        
        # ========== Monthly Heatmap ==========
        monthly_data, year, month, today = get_monthly_data(prefs)
        total_month = sum(monthly_data.values())
        _, num_days = calendar.monthrange(year, month)
        
        # Check if we need sample data
        is_sample_month = total_month < 10
        if is_sample_month:
            # Use sample data for display
            display_data = generate_sample_monthly_data(num_days, today)
            self.monthly_heatmap.set_data(display_data, year, month, today, is_sample=True, sample_tooltip=sample_tooltip)
        else:
            self.monthly_heatmap.set_data(monthly_data, year, month, today, is_sample=False)
        
        # Update heatmap subtitle (current date)
        self.heatmap_subtitle.setText(f"{month:02d}/{today:02d}")
        
        # Update heatmap comment
        comment = get_month_comment(total_month, self.language, self.i18n)
        self.heatmap_comment.setText(comment)
    
    def update_language(self, language):
        """Update the widget language."""
        self.language = language
        self.i18n = get_translation(language)
        
        # Update section titles
        self.overview_title.setText(self.i18n.get('stat_overview', 'Overview'))
        self.trends_title.setText(self.i18n.get('stat_trends', 'Trends'))
        self.trends_subtitle.setText(self.i18n.get('stat_curious_index', 'Curious Index this week'))
        self.heatmap_title.setText(self.i18n.get('stat_heatmap', 'Heatmap'))
        
        # Refresh stats data (this updates cards, chart labels, etc.)
        self.refresh_stats()
