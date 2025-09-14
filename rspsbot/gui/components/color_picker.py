"""
Advanced color picker component for RSPS Color Bot v3
"""
import logging
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QFrame, QColorDialog, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QColor, QPixmap, QImage, QCursor

from ...core.config import ColorSpec
from ...core.detection.capture import CaptureService

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.color_picker')

class ColorDisplay(QFrame):
    """
    Widget for displaying a color
    """
    
    def __init__(self, parent=None):
        """
        Initialize the color display
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setMinimumSize(50, 30)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.color = QColor(255, 0, 0)
    
    def set_color(self, color):
        """
        Set the color to display
        
        Args:
            color: QColor to display
        """
        self.color = color
        self.update()
    
    def paintEvent(self, event):
        """
        Paint the color display
        
        Args:
            event: Paint event
        """
        super().paintEvent(event)
        
        # Fill with color
        self.setStyleSheet(f"background-color: {self.color.name()};")

class ColorPicker(QWidget):
    """
    Advanced color picker widget
    """
    
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, config_manager=None, parent=None):
        """
        Initialize the color picker
        
        Args:
            config_manager: Configuration manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.config_manager = config_manager
        self.capture_service = None
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Color display and buttons
        top_layout = QHBoxLayout()
        
        # Color display
        self.color_display = ColorDisplay()
        top_layout.addWidget(self.color_display)
        
        # Buttons
        buttons_layout = QVBoxLayout()
        
        self.pick_button = QPushButton("Pick Color")
        self.pick_button.setToolTip("Select a color using the color dialog")
        self.pick_button.clicked.connect(self.on_pick_clicked)
        buttons_layout.addWidget(self.pick_button)
        
        self.pipette_button = QPushButton("Pipette")
        self.pipette_button.setToolTip("Pick a color from the screen")
        self.pipette_button.clicked.connect(self.on_pipette_clicked)
        buttons_layout.addWidget(self.pipette_button)
        
        top_layout.addLayout(buttons_layout)
        
        main_layout.addLayout(top_layout)
        
        # RGB sliders
        rgb_layout = QVBoxLayout()
        
        # Red slider
        red_layout = QHBoxLayout()
        red_layout.addWidget(QLabel("R:"))
        
        self.red_slider = QSlider(Qt.Horizontal)
        self.red_slider.setRange(0, 255)
        self.red_slider.setValue(255)
        self.red_slider.valueChanged.connect(self.on_color_component_changed)
        red_layout.addWidget(self.red_slider)
        
        self.red_spin = QSpinBox()
        self.red_spin.setRange(0, 255)
        self.red_spin.setValue(255)
        self.red_spin.valueChanged.connect(self.on_spin_value_changed)
        red_layout.addWidget(self.red_spin)
        
        rgb_layout.addLayout(red_layout)
        
        # Green slider
        green_layout = QHBoxLayout()
        green_layout.addWidget(QLabel("G:"))
        
        self.green_slider = QSlider(Qt.Horizontal)
        self.green_slider.setRange(0, 255)
        self.green_slider.setValue(0)
        self.green_slider.valueChanged.connect(self.on_color_component_changed)
        green_layout.addWidget(self.green_slider)
        
        self.green_spin = QSpinBox()
        self.green_spin.setRange(0, 255)
        self.green_spin.setValue(0)
        self.green_spin.valueChanged.connect(self.on_spin_value_changed)
        green_layout.addWidget(self.green_spin)
        
        rgb_layout.addLayout(green_layout)
        
        # Blue slider
        blue_layout = QHBoxLayout()
        blue_layout.addWidget(QLabel("B:"))
        
        self.blue_slider = QSlider(Qt.Horizontal)
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setValue(0)
        self.blue_slider.valueChanged.connect(self.on_color_component_changed)
        blue_layout.addWidget(self.blue_slider)
        
        self.blue_spin = QSpinBox()
        self.blue_spin.setRange(0, 255)
        self.blue_spin.setValue(0)
        self.blue_spin.valueChanged.connect(self.on_spin_value_changed)
        blue_layout.addWidget(self.blue_spin)
        
        rgb_layout.addLayout(blue_layout)
        
        # Tolerance slider
        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(QLabel("Tolerance:"))
        
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(30)
        self.tolerance_slider.valueChanged.connect(self.on_tolerance_changed)
        tolerance_layout.addWidget(self.tolerance_slider)
        
        self.tolerance_spin = QSpinBox()
        self.tolerance_spin.setRange(0, 100)
        self.tolerance_spin.setValue(30)
        self.tolerance_spin.valueChanged.connect(self.on_tolerance_spin_changed)
        tolerance_layout.addWidget(self.tolerance_spin)
        
        rgb_layout.addLayout(tolerance_layout)
        
        main_layout.addLayout(rgb_layout)
        
        # Set initial color
        self.set_color(QColor(255, 0, 0))
    
    def on_pick_clicked(self):
        """Handle pick button click"""
        color = QColorDialog.getColor(self.get_color(), self, "Select Color")
        
        if color.isValid():
            self.set_color(color)
    
    def on_pipette_clicked(self):
        """Handle pipette button click"""
        # Hide this window temporarily
        self.window().setWindowOpacity(0.3)
        QApplication.processEvents()
        
        try:
            # Create capture service if needed
            if self.capture_service is None:
                self.capture_service = CaptureService()
            
            # Capture screen
            screenshot = self.capture_service.capture_screen()
            
            if screenshot is None:
                logger.error("Failed to capture screen")
                return
            
            # Wait for mouse click
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
            
            # Show message
            logger.info("Click on the screen to pick a color")
            
            # Wait for click
            original_pos = QCursor.pos()
            
            # This is a simple implementation - in a real application,
            # you would use a global event filter to capture mouse clicks
            # For now, we'll just wait a bit and then get the cursor position
            QApplication.processEvents()
            import time
            time.sleep(2)  # Wait for user to position cursor
            
            # Get cursor position
            pos = QCursor.pos()
            
            # Reset cursor
            QCursor.setPos(original_pos)
            QApplication.restoreOverrideCursor()
            
            # Get color at position
            x, y = pos.x(), pos.y()
            
            # Convert to BGR
            img_np = np.array(screenshot)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
            # Get color at position
            if 0 <= y < img_bgr.shape[0] and 0 <= x < img_bgr.shape[1]:
                b, g, r = img_bgr[y, x]
                color = QColor(r, g, b)
                self.set_color(color)
                logger.info(f"Picked color: RGB({r}, {g}, {b})")
            else:
                logger.warning(f"Position ({x}, {y}) is outside the screen")
        
        except Exception as e:
            logger.error(f"Error picking color: {e}")
        
        finally:
            # Restore window
            self.window().setWindowOpacity(1.0)
    
    def on_color_component_changed(self):
        """Handle color component slider change"""
        r = self.red_slider.value()
        g = self.green_slider.value()
        b = self.blue_slider.value()
        
        # Update spin boxes
        self.red_spin.blockSignals(True)
        self.green_spin.blockSignals(True)
        self.blue_spin.blockSignals(True)
        
        self.red_spin.setValue(r)
        self.green_spin.setValue(g)
        self.blue_spin.setValue(b)
        
        self.red_spin.blockSignals(False)
        self.green_spin.blockSignals(False)
        self.blue_spin.blockSignals(False)
        
        # Update color
        color = QColor(r, g, b)
        self.color_display.set_color(color)
        self.colorChanged.emit(color)
    
    def on_spin_value_changed(self):
        """Handle spin box value change"""
        r = self.red_spin.value()
        g = self.green_spin.value()
        b = self.blue_spin.value()
        
        # Update sliders
        self.red_slider.blockSignals(True)
        self.green_slider.blockSignals(True)
        self.blue_slider.blockSignals(True)
        
        self.red_slider.setValue(r)
        self.green_slider.setValue(g)
        self.blue_slider.setValue(b)
        
        self.red_slider.blockSignals(False)
        self.green_slider.blockSignals(False)
        self.blue_slider.blockSignals(False)
        
        # Update color
        color = QColor(r, g, b)
        self.color_display.set_color(color)
        self.colorChanged.emit(color)
    
    def on_tolerance_changed(self, value):
        """Handle tolerance slider change"""
        self.tolerance_spin.blockSignals(True)
        self.tolerance_spin.setValue(value)
        self.tolerance_spin.blockSignals(False)
    
    def on_tolerance_spin_changed(self, value):
        """Handle tolerance spin box change"""
        self.tolerance_slider.blockSignals(True)
        self.tolerance_slider.setValue(value)
        self.tolerance_slider.blockSignals(False)
    
    def set_color(self, color):
        """
        Set the color
        
        Args:
            color: QColor to set
        """
        # Update sliders
        self.red_slider.blockSignals(True)
        self.green_slider.blockSignals(True)
        self.blue_slider.blockSignals(True)
        
        self.red_slider.setValue(color.red())
        self.green_slider.setValue(color.green())
        self.blue_slider.setValue(color.blue())
        
        self.red_slider.blockSignals(False)
        self.green_slider.blockSignals(False)
        self.blue_slider.blockSignals(False)
        
        # Update spin boxes
        self.red_spin.blockSignals(True)
        self.green_spin.blockSignals(True)
        self.blue_spin.blockSignals(True)
        
        self.red_spin.setValue(color.red())
        self.green_spin.setValue(color.green())
        self.blue_spin.setValue(color.blue())
        
        self.red_spin.blockSignals(False)
        self.green_spin.blockSignals(False)
        self.blue_spin.blockSignals(False)
        
        # Update color display
        self.color_display.set_color(color)
        
        # Emit signal
        self.colorChanged.emit(color)
    
    def get_color(self):
        """
        Get the current color
        
        Returns:
            QColor: Current color
        """
        return QColor(
            self.red_slider.value(),
            self.green_slider.value(),
            self.blue_slider.value()
        )
    
    def get_tolerance(self):
        """
        Get the current tolerance
        
        Returns:
            int: Current tolerance
        """
        return self.tolerance_slider.value()
    
    def set_tolerance(self, tolerance):
        """
        Set the tolerance
        
        Args:
            tolerance: Tolerance value
        """
        self.tolerance_slider.setValue(tolerance)
    
    def get_color_spec(self):
        """
        Get the color specification
        
        Returns:
            ColorSpec: Color specification
        """
        color = self.get_color()
        tolerance = self.get_tolerance()
        
        return ColorSpec(
            r=color.red(),
            g=color.green(),
            b=color.blue(),
            tolerance=tolerance
        )
    
    def set_color_spec(self, color_spec):
        """
        Set the color specification
        
        Args:
            color_spec: ColorSpec object
        """
        if color_spec:
            self.set_color(QColor(color_spec.r, color_spec.g, color_spec.b))
            self.set_tolerance(color_spec.tolerance)