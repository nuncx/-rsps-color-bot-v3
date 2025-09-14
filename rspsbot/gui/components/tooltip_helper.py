"""
Tooltip helper for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import QWidget, QToolTip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.tooltip_helper')

class TooltipHelper:
    """
    Helper class for adding tooltips to widgets
    """
    
    @staticmethod
    def set_tooltip_font(font_size=10):
        """
        Set the font for all tooltips
        
        Args:
            font_size: Font size
        """
        font = QFont()
        font.setPointSize(font_size)
        QToolTip.setFont(font)
    
    @staticmethod
    def add_tooltip(widget, text, rich_text=True):
        """
        Add a tooltip to a widget
        
        Args:
            widget: Widget to add tooltip to
            text: Tooltip text
            rich_text: Whether to use rich text formatting
        """
        if rich_text:
            widget.setToolTip(f"<div style='font-size: 10pt;'>{text}</div>")
        else:
            widget.setToolTip(text)
    
    @staticmethod
    def add_tooltips(widgets_and_texts):
        """
        Add tooltips to multiple widgets
        
        Args:
            widgets_and_texts: List of (widget, text) tuples
        """
        for widget, text in widgets_and_texts:
            TooltipHelper.add_tooltip(widget, text)