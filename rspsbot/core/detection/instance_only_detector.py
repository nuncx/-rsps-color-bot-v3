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
        self.instance_empty_start_time = None
        self.instance_empty_timeout = 30  # 30 seconds timeout for empty instance detection
        
    def detect_instance_state(self):
        """
        Detect if the instance is empty or populated based on HP bar visibility
        Returns True if instance is populated, False if empty
        
        Uses a timeout mechanism to ensure the instance is truly empty before signaling
        """
        # Get the instance HP bar ROI from config
        hp_bar_roi = self.config.get('hpbar_roi', None)
        if not hp_bar_roi:
            return False
            
        # Capture the HP bar region
        screenshot = self.capture_service.capture(hp_bar_roi)
        if screenshot is None:
            return False
            
        # Get the HP bar color from config
        hp_bar_color_spec = self.config.get_color_spec('hpbar_color')
        if not hp_bar_color_spec:
            hp_bar_color = (255, 0, 0)  # Default red
            tolerance = 10
        else:
            hp_bar_color = hp_bar_color_spec.rgb
            tolerance = hp_bar_color_spec.tol_rgb
        
        # Detect the HP bar color in the screenshot
        detected = self.color_detector.detect_color(screenshot, hp_bar_color, tolerance)
        
        current_time = time.time()
        
        if detected:
            # HP bar detected, instance is populated
            self.instance_empty_start_time = None
            self.instance_populated.emit()
            return True
        else:
            # No HP bar detected, check if this is a persistent empty state
            if self.instance_empty_start_time is None:
                # First detection of empty instance
                self.instance_empty_start_time = current_time
                return False
            elif current_time - self.instance_empty_start_time >= self.instance_empty_timeout:
                # Instance has been empty for the timeout period
                self.instance_empty.emit()
                return False
            else:
                # Instance might be empty but hasn't reached timeout yet
                return False
            
    def should_use_aggro_potion(self):
        """
        Determine if an aggro potion should be used
        Returns True if potion should be used, False otherwise
        """
        current_time = time.time()
        
        # Check if we've already used the first aggro potion
        if not self.aggro_potion_used:
            # Get the first aggro potion timer from config (in seconds)
            first_potion_timer = self.config.get('first_aggro_potion_timer', 60)
            
            # Log the time remaining for first aggro potion
            time_remaining = first_potion_timer - (current_time - self.last_aggro_time)
            if time_remaining > 0:
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)
                print(f"First aggro potion in: {minutes:02d}:{seconds:02d}")
            
            if current_time - self.last_aggro_time >= first_potion_timer:
                self.aggro_potion_used = True
                self.aggro_potion_needed.emit()
                self.last_aggro_time = current_time
                print("Using first aggro potion")
                return True
        else:
            # Get the general aggro potion interval from config (in seconds)
            general_interval = self.config.get('aggro_duration', 300)
            
            # Log the time remaining for regular aggro potion
            time_remaining = general_interval - (current_time - self.last_aggro_time)
            if time_remaining > 0:
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)
                print(f"Next aggro potion in: {minutes:02d}:{seconds:02d}")
            
            if current_time - self.last_aggro_time >= general_interval:
                self.aggro_potion_needed.emit()
                self.last_aggro_time = current_time
                print("Using regular aggro potion")
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