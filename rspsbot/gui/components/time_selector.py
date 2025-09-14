"""
Time selector component for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.time_selector')

class TimeSelector(QWidget):
    """
    Widget for selecting time with minutes and seconds
    """
    
    timeChanged = pyqtSignal(float)
    
    def __init__(self, label="Time:", initial_seconds=0, parent=None):
        """
        Initialize the time selector
        
        Args:
            label: Label text
            initial_seconds: Initial time in seconds
            parent: Parent widget
        """
        super().__init__(parent)
        self.label_text = label
        self.initial_seconds = initial_seconds
        
        # Initialize UI
        self.init_ui()
        
        # Set initial value
        self.set_time(initial_seconds)
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        if self.label_text:
            self.label = QLabel(self.label_text)
            main_layout.addWidget(self.label)
        
        # Minutes
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 60)
        self.minutes_spin.setSuffix(" min")
        self.minutes_spin.setToolTip("Minutes")
        self.minutes_spin.valueChanged.connect(self.on_time_changed)
        main_layout.addWidget(self.minutes_spin)
        
        # Seconds
        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setSuffix(" sec")
        self.seconds_spin.setToolTip("Seconds")
        self.seconds_spin.valueChanged.connect(self.on_time_changed)
        main_layout.addWidget(self.seconds_spin)
    
    def on_time_changed(self):
        """Handle time change"""
        total_seconds = self.minutes_spin.value() * 60 + self.seconds_spin.value()
        self.timeChanged.emit(total_seconds)
    
    def set_time(self, seconds):
        """
        Set the time value
        
        Args:
            seconds: Time in seconds
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        
        # Block signals to prevent multiple emissions
        self.minutes_spin.blockSignals(True)
        self.seconds_spin.blockSignals(True)
        
        self.minutes_spin.setValue(minutes)
        self.seconds_spin.setValue(secs)
        
        # Unblock signals
        self.minutes_spin.blockSignals(False)
        self.seconds_spin.blockSignals(False)
    
    def get_time(self):
        """
        Get the time value in seconds
        
        Returns:
            float: Time in seconds
        """
        return self.minutes_spin.value() * 60 + self.seconds_spin.value()