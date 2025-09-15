"""
Advanced ROI Selector Component for RSPS Color Bot v3
Enhanced ROI selection with preview capability
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QApplication, QDialog, QGraphicsView,
                            QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,
                            QGraphicsItem, QFileDialog)
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt, QRect, QPoint, QRectF
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from rspsbot.gui.components.screen_picker import ZoomRoiPickerDialog

class AdvancedROISelector(QWidget):
    def __init__(self, label_text="", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.roi = QRect(0, 0, 100, 100)  # Default ROI
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        if self.label_text:
            label = QLabel(self.label_text)
            layout.addWidget(label)
        
        # ROI info display
        self.roi_info = QLabel(f"ROI: {self.roi.x()}, {self.roi.y()}, {self.roi.width()}, {self.roi.height()}")
        layout.addWidget(self.roi_info)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.select_btn = QPushButton("Select ROI")
        self.preview_btn = QPushButton("Preview ROI")
        
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.preview_btn)
        layout.addLayout(button_layout)
        
        self.select_btn.clicked.connect(self.select_roi)
        self.preview_btn.clicked.connect(self.preview_roi)
        
        self.setLayout(layout)
        
    def select_roi(self):
        """Open the ROI selection dialog"""
        dialog = ZoomRoiPickerDialog()
        if dialog.exec_() == QDialog.Accepted:
            if dialog.result_rect:
                self.roi = dialog.result_rect
                self.update_roi_info()
                
    def preview_roi(self):
        """Preview the current ROI"""
        # In a real implementation, this would show a preview of the ROI
        # For now, we'll just print the ROI coordinates
        print(f"Previewing ROI: {self.roi.x()}, {self.roi.y()}, {self.roi.width()}, {self.roi.height()}")
        
    def update_roi_info(self):
        """Update the ROI information display"""
        self.roi_info.setText(f"ROI: {self.roi.x()}, {self.roi.y()}, {self.roi.width()}, {self.roi.height()}")
        
    def get_roi(self):
        """Get the current ROI"""
        return self.roi
        
    def set_roi(self, roi):
        """Set the ROI"""
        self.roi = roi
        self.update_roi_info()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test the widget
    widget = AdvancedROISelector("Test ROI Selector:")
    widget.show()
    
    sys.exit(app.exec_())