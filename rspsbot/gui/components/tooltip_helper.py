"""
Tooltip Helper Component for RSPS Color Bot v3
Helper class for consistent tooltip styling
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class TooltipHelper:
    def __init__(self):
        pass
        
    def add_tooltip(self, widget, title, description):
        """Add a tooltip to a widget with consistent styling"""
        tooltip_text = f"<b>{title}</b><br>{description}"
        widget.setToolTip(tooltip_text)
        
    def create_rich_tooltip(self, title, description, additional_info=""):
        """Create a rich text tooltip with title and description"""
        tooltip = f"<b>{title}</b><br>{description}"
        if additional_info:
            tooltip += f"<br><br><i>{additional_info}</i>"
        return tooltip

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test the tooltip helper
    widget = QWidget()
    layout = QVBoxLayout()
    
    helper = TooltipHelper()
    
    button = QPushButton("Test Button")
    helper.add_tooltip(button, "Test Button", "This is a test button for tooltip helper")
    
    label = QLabel("Test Label")
    label.setToolTip(helper.create_rich_tooltip("Test Label", "This is a test label", "Additional information here"))
    
    layout.addWidget(button)
    layout.addWidget(label)
    
    widget.setLayout(layout)
    widget.show()
    
    sys.exit(app.exec_())