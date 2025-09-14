"""
Structured logger component for RSPS Color Bot v3
"""
import logging
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.structured_logger')

class LogHandler(logging.Handler):
    """
    Custom logging handler that emits signals for log messages
    """
    
    def __init__(self, callback):
        """
        Initialize the log handler
        
        Args:
            callback: Function to call with log records
        """
        super().__init__()
        self.callback = callback
    
    def emit(self, record):
        """
        Emit a log record
        
        Args:
            record: Log record
        """
        try:
            msg = self.format(record)
            self.callback(record, msg)
        except Exception:
            self.handleError(record)

class StructuredLogger(QWidget):
    """
    Widget for displaying structured log messages
    """
    
    def __init__(self, parent=None):
        """
        Initialize the structured logger
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Log buffer
        self.log_buffer = []
        self.max_log_buffer = 1000
        
        # Initialize UI
        self.init_ui()
        
        # Set up log handler
        self.log_handler = LogHandler(self.handle_log)
        self.log_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s', '%H:%M:%S'))
        self.log_handler.setLevel(logging.DEBUG)
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        
        # Start auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_logs)
        self.refresh_timer.start(250)  # Refresh every 250ms
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Log controls
        controls_layout = QHBoxLayout()
        
        # Level filter
        controls_layout.addWidget(QLabel("Level:"))
        
        self.level_combo = QComboBox()
        self.level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.setCurrentText("INFO")
        self.level_combo.currentTextChanged.connect(self.on_level_changed)
        self.level_combo.setToolTip("Filter log messages by level")
        controls_layout.addWidget(self.level_combo)
        
        # Module filter
        controls_layout.addWidget(QLabel("Module:"))
        
        self.module_combo = QComboBox()
        self.module_combo.addItem("All")
        self.module_combo.addItems([
            "rspsbot.core",
            "rspsbot.gui",
            "rspsbot.utils"
        ])
        self.module_combo.setCurrentText("All")
        self.module_combo.currentTextChanged.connect(self.on_module_changed)
        self.module_combo.setToolTip("Filter log messages by module")
        controls_layout.addWidget(self.module_combo)
        
        # Auto-scroll checkbox
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll")
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.setToolTip("Automatically scroll to the latest log messages")
        controls_layout.addWidget(self.auto_scroll_checkbox)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.on_clear_clicked)
        self.clear_button.setToolTip("Clear all log messages")
        controls_layout.addWidget(self.clear_button)
        
        # Save button
        self.save_button = QPushButton("Save Logs")
        self.save_button.clicked.connect(self.on_save_clicked)
        self.save_button.setToolTip("Save log messages to a file")
        controls_layout.addWidget(self.save_button)
        
        main_layout.addLayout(controls_layout)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text.setFont(QFont("Courier New", 9))
        main_layout.addWidget(self.log_text)
    
    def handle_log(self, record, message):
        """
        Handle a log record
        
        Args:
            record: Log record
            message: Formatted message
        """
        # Add to buffer
        self.log_buffer.append((record, message))
        
        # Trim buffer if needed
        if len(self.log_buffer) > self.max_log_buffer:
            self.log_buffer = self.log_buffer[-self.max_log_buffer:]
    
    def refresh_logs(self):
        """Refresh the log display"""
        # Check if there are new logs
        if not self.log_buffer:
            return
        
        # Get current filter settings
        level_name = self.level_combo.currentText()
        level = getattr(logging, level_name)
        
        module_filter = self.module_combo.currentText()
        if module_filter == "All":
            module_filter = None
        
        # Get current cursor
        cursor = self.log_text.textCursor()
        
        # Remember if we were at the end
        at_end = cursor.atEnd()
        
        # Process new logs
        for record, message in self.log_buffer:
            # Apply filters
            if record.levelno < level:
                continue
            
            if module_filter and not record.name.startswith(module_filter):
                continue
            
            # Create format for this log level
            format = QTextCharFormat()
            
            if record.levelno >= logging.CRITICAL:
                format.setForeground(QColor(255, 0, 0))  # Red
                format.setFontWeight(QFont.Bold)
            elif record.levelno >= logging.ERROR:
                format.setForeground(QColor(255, 0, 0))  # Red
            elif record.levelno >= logging.WARNING:
                format.setForeground(QColor(255, 165, 0))  # Orange
            elif record.levelno >= logging.INFO:
                format.setForeground(QColor(0, 0, 0))  # Black
            else:  # DEBUG
                format.setForeground(QColor(128, 128, 128))  # Gray
            
            # Add message
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(message + "\n", format)
        
        # Clear buffer
        self.log_buffer = []
        
        # Auto-scroll if enabled
        if self.auto_scroll_checkbox.isChecked() or at_end:
            cursor.movePosition(QTextCursor.End)
            self.log_text.setTextCursor(cursor)
    
    def on_level_changed(self, level_name):
        """
        Handle log level change
        
        Args:
            level_name: New level name
        """
        # Clear and refresh
        self.log_text.clear()
    
    def on_module_changed(self, module_name):
        """
        Handle module filter change
        
        Args:
            module_name: New module filter
        """
        # Clear and refresh
        self.log_text.clear()
    
    def on_clear_clicked(self):
        """Handle clear button click"""
        self.log_text.clear()
    
    def on_save_clicked(self):
        """Handle save button click"""
        from PyQt5.QtWidgets import QFileDialog
        import os
        
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Logs",
            os.path.expanduser("~/rspsbot_logs.txt"),
            "Log Files (*.log);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # Save logs
                with open(file_path, 'w') as f:
                    f.write(self.log_text.toPlainText())
                
                logger.info(f"Logs saved to: {file_path}")
            
            except Exception as e:
                logger.error(f"Failed to save logs: {e}")
    
    def add_log_message(self, level, message):
        """
        Add a log message directly
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Log message
        """
        log_level = getattr(logging, level.upper())
        logger.log(log_level, message)