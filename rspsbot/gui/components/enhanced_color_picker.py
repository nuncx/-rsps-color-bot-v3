"""
Enhanced Color Picker Component for RSPS Color Bot v3
RGB sliders with tolerance control and visual preview
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QApplication, QDialog, QSlider,
                            QSpinBox, QLineEdit, QColorDialog, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QPainter, QBrush

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from rspsbot.gui.components.screen_picker import ZoomColorPickerDialog

class EnhancedColorPicker(QWidget):
    color_changed = pyqtSignal(tuple)  # Signal emitted when color changes (r, g, b)
    
    def __init__(self, label_text="", initial_color=(255, 255, 255), parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.color = initial_color
        self.tolerance = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        if self.label_text:
            label = QLabel(self.label_text)
            layout.addWidget(label)
        
        # Color preview
        self.color_preview = QLabel()
        self.update_color_preview()
        layout.addWidget(self.color_preview)
        
        # RGB sliders
        sliders_layout = QVBoxLayout()
        self.red_slider = self.create_slider("Red:", 0, 255, self.color[0])
        self.green_slider = self.create_slider("Green:", 0, 255, self.color[1])
        self.blue_slider = self.create_slider("Blue:", 0, 255, self.color[2])
        sliders_layout.addLayout(self.red_slider)
        sliders_layout.addLayout(self.green_slider)
        sliders_layout.addLayout(self.blue_slider)
        layout.addLayout(sliders_layout)
        
        # Tolerance control
        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(QLabel("Tolerance:"))
        self.tolerance_spinbox = QSpinBox()
        self.tolerance_spinbox.setRange(0, 100)
        self.tolerance_spinbox.setValue(self.tolerance)
        tolerance_layout.addWidget(self.tolerance_spinbox)
        layout.addLayout(tolerance_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.pipette_btn = QPushButton("Pipette")
        self.dialog_btn = QPushButton("Color Dialog")
        self.file_btn = QPushButton("From File")
        
        button_layout.addWidget(self.pipette_btn)
        button_layout.addWidget(self.dialog_btn)
        button_layout.addWidget(self.file_btn)
        layout.addLayout(button_layout)
        
        # Connect signals
        self.red_slider.itemAt(1).widget().valueChanged.connect(self.on_color_changed)
        self.green_slider.itemAt(1).widget().valueChanged.connect(self.on_color_changed)
        self.blue_slider.itemAt(1).widget().valueChanged.connect(self.on_color_changed)
        self.tolerance_spinbox.valueChanged.connect(self.on_tolerance_changed)
        
        self.pipette_btn.clicked.connect(self.pick_color_from_screen)
        self.dialog_btn.clicked.connect(self.pick_color_from_dialog)
        self.file_btn.clicked.connect(self.pick_color_from_file)
        
        self.setLayout(layout)
        
    def create_slider(self, label, min_val, max_val, initial_value):
        """Create a slider with label and spinbox"""
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial_value)
        layout.addWidget(slider)
        
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(initial_value)
        layout.addWidget(spinbox)
        
        # Connect slider and spinbox
        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        
        return layout
        
    def update_color_preview(self):
        """Update the color preview label"""
        pixmap = QPixmap(50, 20)
        pixmap.fill(QColor(self.color[0], self.color[1], self.color[2]))
        self.color_preview.setPixmap(pixmap)
        self.color_preview.setStyleSheet("border: 1px solid black;")
        
    def on_color_changed(self):
        """Handle color changes from sliders"""
        red = self.red_slider.itemAt(1).widget().value()
        green = self.green_slider.itemAt(1).widget().value()
        blue = self.blue_slider.itemAt(1).widget().value()
        self.color = (red, green, blue)
        self.update_color_preview()
        self.color_changed.emit(self.color)
        
    def on_tolerance_changed(self, value):
        """Handle tolerance changes"""
        self.tolerance = value
        
    def pick_color_from_screen(self):
        """Open the screen color picker dialog"""
        dialog = ZoomColorPickerDialog()
        if dialog.exec_() == QDialog.Accepted:
            if dialog.selected_color:
                self.color = dialog.selected_color
                self.red_slider.itemAt(1).widget().setValue(self.color[0])
                self.green_slider.itemAt(1).widget().setValue(self.color[1])
                self.blue_slider.itemAt(1).widget().setValue(self.color[2])
                self.color_changed.emit(self.color)
                
    def pick_color_from_dialog(self):
        """Open the standard color dialog"""
        color = QColorDialog.getColor(QColor(self.color[0], self.color[1], self.color[2]))
        if color.isValid():
            self.color = (color.red(), color.green(), color.blue())
            self.red_slider.itemAt(1).widget().setValue(self.color[0])
            self.green_slider.itemAt(1).widget().setValue(self.color[1])
            self.blue_slider.itemAt(1).widget().setValue(self.color[2])
            self.color_changed.emit(self.color)
            
    def pick_color_from_file(self):
        """Pick a color from an image file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # For simplicity, we'll pick the color from the top-left pixel
                # In a real implementation, you might want a more sophisticated picker
                image = pixmap.toImage()
                if not image.isNull():
                    color = image.pixelColor(0, 0)
                    self.color = (color.red(), color.green(), color.blue())
                    self.red_slider.itemAt(1).widget().setValue(self.color[0])
                    self.green_slider.itemAt(1).widget().setValue(self.color[1])
                    self.blue_slider.itemAt(1).widget().setValue(self.color[2])
                    self.color_changed.emit(self.color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test the widget
    widget = EnhancedColorPicker("Test Color Picker:", (128, 128, 128))
    widget.show()
    
    sys.exit(app.exec_())