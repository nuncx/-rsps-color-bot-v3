"""
Enhanced logs panel for RSPS Color Bot v3
"""
import logging
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QTextEdit, QComboBox, QCheckBox, QFileDialog,
    QSplitter, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont

from ..components.structured_logger import StructuredLogger
from ..components.tooltip_helper import TooltipHelper

# Get module logger
logger = logging.getLogger('rspsbot.gui.panels.logs_panel_enhanced')

class LogsPanelEnhanced(QWidget):
    """
    Enhanced panel for displaying log messages
    """
    
    def __init__(self, config_manager):
        """
        Initialize the logs panel
        
        Args:
            config_manager: Configuration manager
        """
        super().__init__()
        self.config_manager = config_manager
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Logs tab
        logs_widget = QWidget()
        logs_layout = QVBoxLayout(logs_widget)
        
        # Create structured logger
        self.structured_logger = StructuredLogger()
        logs_layout.addWidget(self.structured_logger)
        
        # Add logs tab
        self.tab_widget.addTab(logs_widget, "Logs")
        
        # Debug info tab
        debug_widget = QWidget()
        debug_layout = QVBoxLayout(debug_widget)
        
        # Debug text area
        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)
        self.debug_text.setLineWrapMode(QTextEdit.NoWrap)
        self.debug_text.setFont(QFont("Courier New", 9))
        debug_layout.addWidget(self.debug_text)
        
        # Add debug tab
        self.tab_widget.addTab(debug_widget, "Debug Info")
        
        # Statistics tab
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        
        # Stats text area
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setLineWrapMode(QTextEdit.NoWrap)
        self.stats_text.setFont(QFont("Courier New", 9))
        stats_layout.addWidget(self.stats_text)
        
        # Add stats tab
        self.tab_widget.addTab(stats_widget, "Statistics")
        
        # Add tooltips
        TooltipHelper.add_tooltip(self.tab_widget.tabBar().tabButton(0, QTabWidget.LeftSide), "View application logs")
        TooltipHelper.add_tooltip(self.tab_widget.tabBar().tabButton(1, QTabWidget.LeftSide), "View system and environment information")
        TooltipHelper.add_tooltip(self.tab_widget.tabBar().tabButton(2, QTabWidget.LeftSide), "View bot statistics")
        
        # Update debug info
        self.update_debug_info()
        
        # Update stats
        self.update_stats()
        
        # Schedule updates
        QTimer.singleShot(5000, self.update_debug_info)
        QTimer.singleShot(2000, self.update_stats)
    
    def update_debug_info(self):
        """Update debug information"""
        try:
            # Get system info
            import platform
            import psutil
            import sys
            
            # Clear debug text
            self.debug_text.clear()
            
            # Add system info
            self.debug_text.append(f"Python: {sys.version}")
            self.debug_text.append(f"Platform: {platform.platform()}")
            self.debug_text.append(f"CPU: {platform.processor()}")
            self.debug_text.append(f"Memory: {psutil.virtual_memory().total / (1024 * 1024 * 1024):.2f} GB")
            self.debug_text.append("")
            
            # Add dependency versions
            self.debug_text.append("Dependency Versions:")
            
            try:
                import numpy
                self.debug_text.append(f"NumPy: {numpy.__version__}")
            except ImportError:
                self.debug_text.append("NumPy: Not installed")
            
            try:
                import cv2
                self.debug_text.append(f"OpenCV: {cv2.__version__}")
            except ImportError:
                self.debug_text.append("OpenCV: Not installed")
            
            try:
                import PyQt5.QtCore
                self.debug_text.append(f"PyQt5: {PyQt5.QtCore.QT_VERSION_STR}")
            except ImportError:
                self.debug_text.append("PyQt5: Not installed")
            
            try:
                import pyautogui
                try:
                    ver = getattr(pyautogui, "__version__", None)
                    if ver is None:
                        # fallback to package metadata
                        try:
                            from importlib.metadata import version, PackageNotFoundError
                        except Exception:
                            from importlib_metadata import version, PackageNotFoundError  # type: ignore
                        try:
                            ver = version("pyautogui")
                        except PackageNotFoundError:
                            ver = "Unknown"
                    self.debug_text.append(f"PyAutoGUI: {ver}")
                except Exception:
                    self.debug_text.append("PyAutoGUI: Unknown")
            except ImportError:
                self.debug_text.append("PyAutoGUI: Not installed")
            
            try:
                import mss
                try:
                    ver = getattr(mss, "__version__", None)
                    if ver is None:
                        try:
                            from importlib.metadata import version, PackageNotFoundError
                        except Exception:
                            from importlib_metadata import version, PackageNotFoundError  # type: ignore
                        try:
                            ver = version("mss")
                        except PackageNotFoundError:
                            ver = "Unknown"
                    self.debug_text.append(f"MSS: {ver}")
                except Exception:
                    self.debug_text.append("MSS: Unknown")
            except ImportError:
                self.debug_text.append("MSS: Not installed")
            
            try:
                import pynput
                try:
                    ver = getattr(pynput, "__version__", None)
                    if ver is None:
                        try:
                            from importlib.metadata import version, PackageNotFoundError
                        except Exception:
                            from importlib_metadata import version, PackageNotFoundError  # type: ignore
                        try:
                            ver = version("pynput")
                        except PackageNotFoundError:
                            ver = "Unknown"
                    self.debug_text.append(f"PyInput: {ver}")
                except Exception:
                    self.debug_text.append("PyInput: Unknown")
            except ImportError:
                self.debug_text.append("PyInput: Not installed")
            
            self.debug_text.append("")
            
            # Add runtime info
            self.debug_text.append("Runtime Information:")
            self.debug_text.append(f"CPU Usage: {psutil.cpu_percent()}%")
            self.debug_text.append(f"Memory Usage: {psutil.Process().memory_info().rss / (1024 * 1024):.2f} MB")
            
            # Schedule next update
            QTimer.singleShot(5000, self.update_debug_info)
        
        except Exception as e:
            self.debug_text.append(f"Error updating debug info: {e}")
    
    def update_stats(self):
        """Update statistics"""
        try:
            # Clear stats text
            self.stats_text.clear()
            
            # Add bot statistics
            self.stats_text.append("Bot Statistics:")
            self.stats_text.append("=============")
            
            # Get statistics from config
            runtime = self.config_manager.get('total_runtime_s', 0)
            hours, remainder = divmod(runtime, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.stats_text.append(f"Total Runtime: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            
            monsters_killed = self.config_manager.get('monsters_killed', 0)
            self.stats_text.append(f"Monsters Killed: {monsters_killed}")
            
            potions_used = self.config_manager.get('potions_used', 0)
            self.stats_text.append(f"Potions Used: {potions_used}")
            
            teleports_used = self.config_manager.get('teleports_used', 0)
            self.stats_text.append(f"Teleports Used: {teleports_used}")
            
            instances_entered = self.config_manager.get('instances_entered', 0)
            self.stats_text.append(f"Instances Entered: {instances_entered}")
            
            self.stats_text.append("")
            
            # Add efficiency metrics
            if runtime > 0:
                monsters_per_hour = monsters_killed / (runtime / 3600)
                self.stats_text.append(f"Monsters per Hour: {monsters_per_hour:.2f}")
                
                potions_per_hour = potions_used / (runtime / 3600)
                self.stats_text.append(f"Potions per Hour: {potions_per_hour:.2f}")
                
                teleports_per_hour = teleports_used / (runtime / 3600)
                self.stats_text.append(f"Teleports per Hour: {teleports_per_hour:.2f}")
            
            # Schedule next update
            QTimer.singleShot(2000, self.update_stats)
        
        except Exception as e:
            self.stats_text.append(f"Error updating stats: {e}")