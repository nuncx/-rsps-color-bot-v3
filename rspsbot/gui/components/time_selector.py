"""
Time Selector Component for RSPS Color Bot v3
Widget for selecting time in minutes/seconds/hours
"""

import sys
import re
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSpinBox, 
                            QComboBox, QApplication, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator

class TimeSelector(QWidget):
    """
    Widget for selecting time in various formats
    
    Modes:
    - min_sec: Minutes and seconds spinboxes
    - sec_only: Seconds spinbox only
    - hour_min: Hours and minutes spinboxes
    - min_sec_str: Minutes:seconds string input (mm:ss)
    - hour_min_sec_str: Hours:minutes:seconds string input (hh:mm:ss)
    """
    
    valueChanged = pyqtSignal(int)  # Signal emitted when value changes (seconds)
    
    def __init__(self, label_text="", mode="min_sec", parent=None):
        """
        Initialize the time selector
        
        Args:
            label_text: Optional label text
            mode: Time selection mode (min_sec, sec_only, hour_min, min_sec_str, hour_min_sec_str)
            parent: Parent widget
        """
        super().__init__(parent)
        self.mode = mode
        self.init_ui(label_text)
        
    def init_ui(self, label_text):
        """Initialize the UI components"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        if label_text:
            label = QLabel(label_text)
            layout.addWidget(label)
        
        # Create spinboxes based on mode
        if self.mode == "min_sec":
            self.minutes_spinbox = QSpinBox()
            self.minutes_spinbox.setRange(0, 59)
            self.minutes_spinbox.setSuffix(" min")
            self.minutes_spinbox.valueChanged.connect(self._emit_value_changed)
            layout.addWidget(self.minutes_spinbox)
            
            self.seconds_spinbox = QSpinBox()
            self.seconds_spinbox.setRange(0, 59)
            self.seconds_spinbox.setSuffix(" sec")
            self.seconds_spinbox.valueChanged.connect(self._emit_value_changed)
            layout.addWidget(self.seconds_spinbox)
            
        elif self.mode == "sec_only":
            self.seconds_spinbox = QSpinBox()
            self.seconds_spinbox.setRange(0, 9999)
            self.seconds_spinbox.setSuffix(" sec")
            self.seconds_spinbox.valueChanged.connect(self._emit_value_changed)
            layout.addWidget(self.seconds_spinbox)
            
        elif self.mode == "hour_min":
            self.hours_spinbox = QSpinBox()
            self.hours_spinbox.setRange(0, 23)
            self.hours_spinbox.setSuffix(" hr")
            self.hours_spinbox.valueChanged.connect(self._emit_value_changed)
            layout.addWidget(self.hours_spinbox)
            
            self.minutes_spinbox = QSpinBox()
            self.minutes_spinbox.setRange(0, 59)
            self.minutes_spinbox.setSuffix(" min")
            self.minutes_spinbox.valueChanged.connect(self._emit_value_changed)
            layout.addWidget(self.minutes_spinbox)
            
        elif self.mode == "min_sec_str":
            self.time_input = QLineEdit()
            self.time_input.setPlaceholderText("mm:ss")
            self.time_input.setInputMask("99:99")
            self.time_input.setText("00:00")
            self.time_input.textChanged.connect(self._validate_min_sec)
            self.time_input.editingFinished.connect(self._emit_value_changed)
            layout.addWidget(self.time_input)
            
        elif self.mode == "hour_min_sec_str":
            self.time_input = QLineEdit()
            self.time_input.setPlaceholderText("hh:mm:ss")
            self.time_input.setInputMask("99:99:99")
            self.time_input.setText("00:00:00")
            self.time_input.textChanged.connect(self._validate_hour_min_sec)
            self.time_input.editingFinished.connect(self._emit_value_changed)
            layout.addWidget(self.time_input)
        
        self.setLayout(layout)
        
    def _validate_min_sec(self, text):
        """Validate minutes:seconds format"""
        if not text:
            return
            
        # Check if the format is valid (mm:ss)
        match = re.match(r'^(\d{1,2}):(\d{1,2})$', text)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            
            # Validate ranges
            if minutes > 59:
                minutes = 59
            if seconds > 59:
                seconds = 59
                
            # Update text if needed
            new_text = f"{minutes:02d}:{seconds:02d}"
            if new_text != text:
                self.time_input.setText(new_text)
    
    def _validate_hour_min_sec(self, text):
        """Validate hours:minutes:seconds format"""
        if not text:
            return
            
        # Check if the format is valid (hh:mm:ss)
        match = re.match(r'^(\d{1,2}):(\d{1,2}):(\d{1,2})$', text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            
            # Validate ranges
            if hours > 23:
                hours = 23
            if minutes > 59:
                minutes = 59
            if seconds > 59:
                seconds = 59
                
            # Update text if needed
            new_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            if new_text != text:
                self.time_input.setText(new_text)
    
    def _emit_value_changed(self):
        """Emit the valueChanged signal with the current value in seconds"""
        self.valueChanged.emit(self.get_value())
        
    def get_value(self):
        """Get the time value in seconds"""
        if self.mode == "min_sec":
            return self.minutes_spinbox.value() * 60 + self.seconds_spinbox.value()
        elif self.mode == "sec_only":
            return self.seconds_spinbox.value()
        elif self.mode == "hour_min":
            return self.hours_spinbox.value() * 3600 + self.minutes_spinbox.value() * 60
        elif self.mode == "min_sec_str":
            time_str = self.time_input.text()
            if ":" in time_str:
                try:
                    minutes, seconds = time_str.split(":")
                    return int(minutes) * 60 + int(seconds)
                except (ValueError, IndexError):
                    return 0
            return 0
        elif self.mode == "hour_min_sec_str":
            time_str = self.time_input.text()
            if ":" in time_str:
                try:
                    hours, minutes, seconds = time_str.split(":")
                    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                except (ValueError, IndexError):
                    return 0
            return 0
            
    def set_value(self, seconds):
        """Set the time value from seconds"""
        if self.mode == "min_sec":
            minutes = seconds // 60
            secs = seconds % 60
            self.minutes_spinbox.setValue(minutes)
            self.seconds_spinbox.setValue(secs)
        elif self.mode == "sec_only":
            self.seconds_spinbox.setValue(seconds)
        elif self.mode == "hour_min":
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            self.hours_spinbox.setValue(hours)
            self.minutes_spinbox.setValue(minutes)
        elif self.mode == "min_sec_str":
            minutes = seconds // 60
            secs = seconds % 60
            self.time_input.setText(f"{minutes:02d}:{secs:02d}")
        elif self.mode == "hour_min_sec_str":
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            self.time_input.setText(f"{hours:02d}:{minutes:02d}:{secs:02d}")
    
    def get_formatted_value(self):
        """Get the time value as a formatted string"""
        seconds = self.get_value()
        
        if self.mode == "min_sec" or self.mode == "min_sec_str":
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes:02d}:{secs:02d}"
        elif self.mode == "sec_only":
            return f"{seconds} sec"
        elif self.mode == "hour_min" or self.mode == "hour_min_sec_str":
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test the widget
    widget = QWidget()
    layout = QVBoxLayout()
    
    selector1 = TimeSelector("Time 1 (min:sec):", "min_sec")
    selector2 = TimeSelector("Time 2 (sec only):", "sec_only")
    selector3 = TimeSelector("Time 3 (hr:min):", "hour_min")
    selector4 = TimeSelector("Time 4 (mm:ss):", "min_sec_str")
    selector5 = TimeSelector("Time 5 (hh:mm:ss):", "hour_min_sec_str")
    
    layout.addWidget(selector1)
    layout.addWidget(selector2)
    layout.addWidget(selector3)
    layout.addWidget(selector4)
    layout.addWidget(selector5)
    
    # Set some values
    selector1.set_value(125)  # 2:05
    selector2.set_value(45)   # 45 sec
    selector3.set_value(3720) # 1:02:00
    selector4.set_value(90)   # 01:30
    selector5.set_value(3665) # 01:01:05
    
    # Print values when changed
    def print_value(value):
        print(f"Value changed: {value} seconds")
    
    selector1.valueChanged.connect(print_value)
    
    widget.setLayout(layout)
    widget.show()
    
    sys.exit(app.exec_())