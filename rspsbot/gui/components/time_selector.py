"""
Time Selector Component for RSPS Color Bot v3
Widget for selecting time in minutes/seconds/hours
"""

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSpinBox, 
                            QComboBox, QApplication, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt

class TimeSelector(QWidget):
    def __init__(self, label_text="", mode="min_sec", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.init_ui(label_text)
        
    def init_ui(self, label_text):
        layout = QHBoxLayout()
        
        if label_text:
            label = QLabel(label_text)
            layout.addWidget(label)
        
        # Create spinboxes based on mode
        if self.mode == "min_sec":
            self.minutes_spinbox = QSpinBox()
            self.minutes_spinbox.setRange(0, 59)
            self.minutes_spinbox.setSuffix(" min")
            layout.addWidget(self.minutes_spinbox)
            
            self.seconds_spinbox = QSpinBox()
            self.seconds_spinbox.setRange(0, 59)
            self.seconds_spinbox.setSuffix(" sec")
            layout.addWidget(self.seconds_spinbox)
            
        elif self.mode == "sec_only":
            self.seconds_spinbox = QSpinBox()
            self.seconds_spinbox.setRange(0, 9999)
            self.seconds_spinbox.setSuffix(" sec")
            layout.addWidget(self.seconds_spinbox)
            
        elif self.mode == "hour_min":
            self.hours_spinbox = QSpinBox()
            self.hours_spinbox.setRange(0, 23)
            self.hours_spinbox.setSuffix(" hr")
            layout.addWidget(self.hours_spinbox)
            
            self.minutes_spinbox = QSpinBox()
            self.minutes_spinbox.setRange(0, 59)
            self.minutes_spinbox.setSuffix(" min")
            layout.addWidget(self.minutes_spinbox)
            
        elif self.mode == "min_sec_str":
            self.time_input = QLineEdit()
            self.time_input.setPlaceholderText("mm:ss")
            layout.addWidget(self.time_input)
            
        elif self.mode == "hour_min_sec_str":
            self.time_input = QLineEdit()
            self.time_input.setPlaceholderText("hh:mm:ss")
            layout.addWidget(self.time_input)
        
        self.setLayout(layout)
        
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
                parts = time_str.split(":")
                if len(parts) == 2:
                    minutes, seconds = parts
                    return int(minutes) * 60 + int(seconds)
            return 0
        elif self.mode == "hour_min_sec_str":
            time_str = self.time_input.text()
            if ":" in time_str:
                parts = time_str.split(":")
                if len(parts) == 3:
                    hours, minutes, seconds = parts
                    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test the widget
    widget = QWidget()
    layout = QVBoxLayout()
    
    selector1 = TimeSelector("Time 1 (min:sec):", "min_sec")
    selector2 = TimeSelector("Time 2 (sec only):", "sec_only")
    selector3 = TimeSelector("Time 3 (hr:min):", "hour_min")
    
    layout.addWidget(selector1)
    layout.addWidget(selector2)
    layout.addWidget(selector3)
    
    widget.setLayout(layout)
    widget.show()
    
    sys.exit(app.exec_())