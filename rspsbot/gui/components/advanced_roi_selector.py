"""
Advanced ROI selector component for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush

from ...core.config import ROI
from ..components.screen_picker import ZoomRoiPickerDialog

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.advanced_roi_selector')

class ROIPreview(QFrame):
    """
    Widget for displaying a ROI preview
    """
    
    def __init__(self, parent=None):
        """
        Initialize the ROI preview
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setMinimumSize(100, 80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        
        self.roi = None
        self.screen_size = (1920, 1080)  # Default screen size
    
    def set_roi(self, roi):
        """
        Set the ROI to display
        
        Args:
            roi: ROI object
        """
        self.roi = roi
        self.update()
    
    def set_screen_size(self, width, height):
        """
        Set the screen size for scaling
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.screen_size = (width, height)
        self.update()
    
    def paintEvent(self, event):
        """
        Paint the ROI preview
        
        Args:
            event: Paint event
        """
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor(240, 240, 240))
        
        # Draw screen outline
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.drawRect(self.rect())
        
        # Draw ROI if available
        if self.roi:
            # Calculate scaled position
            scale_x = self.width() / self.screen_size[0]
            scale_y = self.height() / self.screen_size[1]
            
            x = int(self.roi.left * scale_x)
            y = int(self.roi.top * scale_y)
            width = int(self.roi.width * scale_x)
            height = int(self.roi.height * scale_y)
            
            # Draw ROI rectangle
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.setBrush(QBrush(QColor(255, 0, 0, 50)))
            painter.drawRect(x, y, width, height)
            
            # Draw ROI coordinates
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawText(
                x + 5, y + 15,
                f"({self.roi.left}, {self.roi.top}) {self.roi.width}x{self.roi.height}"
            )

class AdvancedROISelector(QWidget):
    """
    Advanced ROI selector widget
    """
    
    roiChanged = pyqtSignal(ROI)
    
    def __init__(self, config_manager=None, parent=None):
        """
        Initialize the ROI selector
        
        Args:
            config_manager: Configuration manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.config_manager = config_manager
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # ROI preview
        self.roi_preview = ROIPreview()
        main_layout.addWidget(self.roi_preview)
        
        # Position controls
        position_group = QFrame()
        position_layout = QHBoxLayout(position_group)
        position_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left
        position_layout.addWidget(QLabel("Left:"))
        self.left_spin = QSpinBox()
        self.left_spin.setRange(0, 9999)
        self.left_spin.valueChanged.connect(self.on_roi_changed)
        self.left_spin.setToolTip("Left coordinate of the ROI")
        position_layout.addWidget(self.left_spin)
        
        # Top
        position_layout.addWidget(QLabel("Top:"))
        self.top_spin = QSpinBox()
        self.top_spin.setRange(0, 9999)
        self.top_spin.valueChanged.connect(self.on_roi_changed)
        self.top_spin.setToolTip("Top coordinate of the ROI")
        position_layout.addWidget(self.top_spin)
        
        main_layout.addWidget(position_group)
        
        # Size controls
        size_group = QFrame()
        size_layout = QHBoxLayout(size_group)
        size_layout.setContentsMargins(0, 0, 0, 0)
        
        # Width
        size_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.width_spin.setValue(100)
        self.width_spin.valueChanged.connect(self.on_roi_changed)
        self.width_spin.setToolTip("Width of the ROI")
        size_layout.addWidget(self.width_spin)
        
        # Height
        size_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.height_spin.setValue(100)
        self.height_spin.valueChanged.connect(self.on_roi_changed)
        self.height_spin.setToolTip("Height of the ROI")
        size_layout.addWidget(self.height_spin)
        
        main_layout.addWidget(size_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Select from Screen")
        self.select_button.clicked.connect(self.on_select_clicked)
        self.select_button.setToolTip("Select ROI directly from the screen")
        buttons_layout.addWidget(self.select_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.on_clear_clicked)
        self.clear_button.setToolTip("Clear the current ROI")
        buttons_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Set initial ROI
        self.set_roi(ROI(0, 0, 100, 100))
    
    def on_roi_changed(self):
        """Handle ROI value change"""
        roi = ROI(
            left=self.left_spin.value(),
            top=self.top_spin.value(),
            width=self.width_spin.value(),
            height=self.height_spin.value()
        )
        
        # Update preview
        self.roi_preview.set_roi(roi)
        
        # Emit signal
        self.roiChanged.emit(roi)
    
    def on_select_clicked(self):
        """Handle select button click"""
        if self.config_manager:
            dialog = ZoomRoiPickerDialog(self.config_manager, self)
            if dialog.exec_() == dialog.Accepted and dialog.result_rect:
                rect = dialog.result_rect
                self.set_roi(ROI(
                    left=rect.left(),
                    top=rect.top(),
                    width=rect.width(),
                    height=rect.height()
                ))
    
    def on_clear_clicked(self):
        """Handle clear button click"""
        self.set_roi(ROI(0, 0, 100, 100))
    
    def set_roi(self, roi):
        """
        Set the ROI
        
        Args:
            roi: ROI object
        """
        if roi:
            # Block signals to prevent multiple emissions
            self.left_spin.blockSignals(True)
            self.top_spin.blockSignals(True)
            self.width_spin.blockSignals(True)
            self.height_spin.blockSignals(True)
            
            self.left_spin.setValue(roi.left)
            self.top_spin.setValue(roi.top)
            self.width_spin.setValue(roi.width)
            self.height_spin.setValue(roi.height)
            
            # Unblock signals
            self.left_spin.blockSignals(False)
            self.top_spin.blockSignals(False)
            self.width_spin.blockSignals(False)
            self.height_spin.blockSignals(False)
            
            # Update preview
            self.roi_preview.set_roi(roi)
            
            # Emit signal
            self.roiChanged.emit(roi)
    
    def get_roi(self):
        """
        Get the current ROI
        
        Returns:
            ROI: Current ROI
        """
        return ROI(
            left=self.left_spin.value(),
            top=self.top_spin.value(),
            width=self.width_spin.value(),
            height=self.height_spin.value()
        )