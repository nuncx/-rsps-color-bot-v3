"""
Instance Only Detector for RSPS Color Bot v3
Specialized detection logic for instance-only mode
"""

import time
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from .color_detector import ColorDetector
from .capture import CaptureService

class InstanceOnlyDetector(QObject):
    # Signals for communication with other components
    instance_empty = pyqtSignal()  # Emitted when instance is determined to be empty
    instance_populated = pyqtSignal()  # Emitted when instance is determined to be populated
    aggro_potion_needed = pyqtSignal()  # Emitted when aggro potion should be used
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.capture_service = CaptureService()
        self.color_detector = ColorDetector()
        self.last_aggro_time = time.time()
        self.aggro_potion_used = False
        
    def detect_instance_state(self):
        """
        Detect if the instance is empty or populated based on HP bar visibility
        Returns True if instance is populated, False if empty
        """
        # Get the instance HP bar ROI from config
        hp_bar_roi = self.config.get('instance_hp_bar_roi', (0, 0, 100, 100))
        
        # Capture the HP bar region
        screenshot = self.capture_service.capture(hp_bar_roi)
        if screenshot is None:
            return False
            
        # Get the HP bar color from config
        hp_bar_color = self.config.get('instance_hp_bar_color', (255, 0, 0))  # Default red
        tolerance = self.config.get('instance_hp_bar_tolerance', 10)
        
        # Detect the HP bar color in the screenshot
        detected = self.color_detector.detect_color(screenshot, hp_bar_color, tolerance)
        
        if detected:
            self.instance_populated.emit()
            return True
        else:
            self.instance_empty.emit()
            return False
            
    def should_use_aggro_potion(self):
        """
        Determine if an aggro potion should be used
        Returns True if potion should be used, False otherwise
        """
        # Check if we've already used the first aggro potion
        if not self.aggro_potion_used:
            # Get the first aggro potion timer from config
            first_potion_timer = self.config.get('first_aggro_potion_timer', 0)
            if time.time() - self.last_aggro_time >= first_potion_timer:
                self.aggro_potion_used = True
                self.aggro_potion_needed.emit()
                self.last_aggro_time = time.time()
                return True
        else:
            # Get the general aggro potion interval from config
            general_interval = self.config.get('aggro_potion_interval', 60)
            if time.time() - self.last_aggro_time >= general_interval:
                self.aggro_potion_needed.emit()
                self.last_aggro_time = time.time()
                return True
                
        return False

if __name__ == "__main__":
    # This is just for testing purposes
    import sys
    from PyQt5.QtWidgets import QApplication
    
    class DummyConfig:
        def get(self, key, default=None):
            # Return some dummy values for testing
            if key == 'instance_hp_bar_roi':
                return (100, 100, 200, 20)
            elif key == 'instance_hp_bar_color':
                return (255, 0, 0)
            elif key == 'instance_hp_bar_tolerance':
                return 10
            elif key == 'first_aggro_potion_timer':
                return 30
            elif key == 'aggro_potion_interval':
                return 60
            return default
    
    app = QApplication(sys.argv)
    detector = InstanceOnlyDetector(DummyConfig())
    print("Instance Only Detector initialized")
    app.exec_()