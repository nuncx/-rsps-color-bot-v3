"""
Instance settings panel for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QCheckBox, QSpinBox, QDoubleSpinBox, QLineEdit,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from ...core.config import Coordinate, ROI, ColorSpec
from .teleport_panel import CoordinateSelector
from ..components.screen_picker import ZoomRoiPickerDialog
from .detection_panel import ColorSpecEditor

# Get module logger
logger = logging.getLogger('rspsbot.gui.panels.instance_panel')

class ROISelector(QWidget):
    """
    Widget for selecting a region of interest
    """
    
    def __init__(self, config_manager=None, parent=None):
        """
        Initialize the ROI selector
        
        Args:
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
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Position
        position_layout = QHBoxLayout()
        
        position_layout.addWidget(QLabel("Left:"))
        self.left_spin = QSpinBox()
        self.left_spin.setRange(0, 9999)
        position_layout.addWidget(self.left_spin)
        
        position_layout.addWidget(QLabel("Top:"))
        self.top_spin = QSpinBox()
        self.top_spin.setRange(0, 9999)
        position_layout.addWidget(self.top_spin)
        
        main_layout.addLayout(position_layout)
        
        # Size
        size_layout = QHBoxLayout()
        
        size_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.width_spin.setValue(100)
        size_layout.addWidget(self.width_spin)
        
        size_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.height_spin.setValue(100)
        size_layout.addWidget(self.height_spin)
        
        main_layout.addLayout(size_layout)
        
        # Select button
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Select ROI")
        self.select_button.clicked.connect(self.on_select_clicked)
        button_layout.addWidget(self.select_button)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
    
    def on_select_clicked(self):
        """Handle select button click"""
        dialog = ZoomRoiPickerDialog(self.config_manager, self)
        if dialog.exec_() == dialog.Accepted and dialog.result_rect:
            rect = dialog.result_rect
            # QRect is in global coordinates already because we used globalPos
            self.left_spin.setValue(rect.left())
            self.top_spin.setValue(rect.top())
            self.width_spin.setValue(rect.width())
            self.height_spin.setValue(rect.height())
    
    def set_roi(self, roi: ROI):
        """Set the ROI values"""
        self.left_spin.setValue(roi.left)
        self.top_spin.setValue(roi.top)
        self.width_spin.setValue(roi.width)
        self.height_spin.setValue(roi.height)
    
    def get_roi(self) -> ROI:
        """Get the ROI values"""
        return ROI(
            left=self.left_spin.value(),
            top=self.top_spin.value(),
            width=self.width_spin.value(),
            height=self.height_spin.value()
        )

class InstancePanel(QWidget):
    """
    Panel for instance settings
    """
    
    def __init__(self, config_manager, bot_controller):
        """
        Initialize the instance panel
        
        Args:
            config_manager: Configuration manager
            bot_controller: Bot controller
        """
        super().__init__()
        self.config_manager = config_manager
        self.bot_controller = bot_controller
        
        # Initialize UI
        self.init_ui()
        
        # Load settings
        self.load_settings()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Instance entry group
        entry_group = QGroupBox("Instance Entry")
        entry_layout = QVBoxLayout(entry_group)
        
        # Instance token
        token_group = QGroupBox("Instance Token")
        token_layout = QVBoxLayout(token_group)
        
        self.token_selector = CoordinateSelector()
        token_layout.addWidget(self.token_selector)
        
        entry_layout.addWidget(token_group)
        
        # Instance teleport
        teleport_group = QGroupBox("Instance Teleport")
        teleport_layout = QVBoxLayout(teleport_group)
        
        self.teleport_selector = CoordinateSelector()
        teleport_layout.addWidget(self.teleport_selector)
        
        # Delay
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay:"))
        
        # Use TimeSelector instead of QDoubleSpinBox
        from ..components.time_selector import TimeSelector
        self.token_delay_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('instance_token_delay', 1.0))
        self.token_delay_selector.setToolTip("Time to wait between clicking the instance token and the teleport spot")
        delay_layout.addWidget(self.token_delay_selector)
        
        delay_layout.addStretch()
        
        teleport_layout.addLayout(delay_layout)
        
        entry_layout.addWidget(teleport_group)
        
        # Test button
        test_layout = QHBoxLayout()
        
        self.test_entry_button = QPushButton("Test Instance Entry")
        self.test_entry_button.clicked.connect(self.on_test_entry_clicked)
        test_layout.addWidget(self.test_entry_button)
        
        self.save_entry_button = QPushButton("Save Entry Settings")
        self.save_entry_button.clicked.connect(self.on_save_entry_clicked)
        test_layout.addWidget(self.save_entry_button)
        
        entry_layout.addLayout(test_layout)
        
        main_layout.addWidget(entry_group)
        
        # Aggro potion group
        aggro_group = QGroupBox("Aggro Potion")
        aggro_layout = QVBoxLayout(aggro_group)
        
        # Aggro potion location
        location_group = QGroupBox("Potion Location")
        location_layout = QVBoxLayout(location_group)
        
        self.aggro_selector = CoordinateSelector()
        location_layout.addWidget(self.aggro_selector)
        
        aggro_layout.addWidget(location_group)
        
        # Aggro duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duration:"))
        
        # Use TimeSelector instead of QDoubleSpinBox
        from ..components.time_selector import TimeSelector
        self.aggro_duration_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('aggro_duration', 300.0))
        self.aggro_duration_selector.setToolTip("Duration of the aggro potion effect")
        duration_layout.addWidget(self.aggro_duration_selector)
        
        duration_layout.addStretch()
        
        aggro_layout.addLayout(duration_layout)
        
        # Aggro effect detection
        effect_group = QGroupBox("Effect Detection")
        effect_layout = QVBoxLayout(effect_group)
        
        # Enable visual check
        check_layout = QHBoxLayout()
        
        self.visual_check_checkbox = QCheckBox("Enable Visual Check")
        self.visual_check_checkbox.toggled.connect(self.on_visual_check_toggled)
        check_layout.addWidget(self.visual_check_checkbox)
        
        check_layout.addStretch()
        
        effect_layout.addLayout(check_layout)
        
        # Effect ROI
        self.roi_group = QGroupBox("Effect ROI")
        roi_layout = QVBoxLayout(self.roi_group)
        
        self.roi_selector = ROISelector()
        roi_layout.addWidget(self.roi_selector)
        
        effect_layout.addWidget(self.roi_group)
        
        # Effect color
        self.color_group = QGroupBox("Effect Color")
        color_layout = QVBoxLayout(self.color_group)
        
        self.color_editor = ColorSpecEditor(self.config_manager, 'aggro_effect_color')
        color_layout.addWidget(self.color_editor)
        
        effect_layout.addWidget(self.color_group)
        
        aggro_layout.addWidget(effect_group)
        
        # Test button
        aggro_test_layout = QHBoxLayout()
        
        self.test_aggro_button = QPushButton("Test Aggro Potion")
        self.test_aggro_button.clicked.connect(self.on_test_aggro_clicked)
        aggro_test_layout.addWidget(self.test_aggro_button)
        
        self.save_aggro_button = QPushButton("Save Aggro Settings")
        self.save_aggro_button.clicked.connect(self.on_save_aggro_clicked)
        aggro_test_layout.addWidget(self.save_aggro_button)
        
        aggro_layout.addLayout(aggro_test_layout)
        
        main_layout.addWidget(aggro_group)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
    
    def load_settings(self):
        """Load settings from config"""
        # Instance token
        token_coord = self.config_manager.get_coordinate('instance_token_location')
        if token_coord:
            self.token_selector.set_coordinate(token_coord.x, token_coord.y)
        
        # Instance teleport
        teleport_coord = self.config_manager.get_coordinate('instance_teleport_location')
        if teleport_coord:
            self.teleport_selector.set_coordinate(teleport_coord.x, teleport_coord.y)
        
        # Token delay
        self.token_delay_selector.set_time(self.config_manager.get('instance_token_delay', 1.0))
        
        # Aggro potion
        aggro_coord = self.config_manager.get_coordinate('aggro_potion_location')
        if aggro_coord:
            self.aggro_selector.set_coordinate(aggro_coord.x, aggro_coord.y)
        
        # Aggro duration
        self.aggro_duration_selector.set_time(self.config_manager.get('aggro_duration', 300.0))
        
        # Visual check
        self.visual_check_checkbox.setChecked(self.config_manager.get('aggro_visual_check', True))
        
        # Effect ROI
        roi = self.config_manager.get_roi('aggro_effect_roi')
        if roi:
            self.roi_selector.set_roi(roi)
        
        # Update UI state
        self.on_visual_check_toggled(self.visual_check_checkbox.isChecked())
    
    def on_visual_check_toggled(self, checked):
        """Handle visual check checkbox toggle"""
        self.roi_group.setEnabled(checked)
        self.color_group.setEnabled(checked)
        self.config_manager.set('aggro_visual_check', checked)
    
    def on_test_entry_clicked(self):
        """Handle test entry button click"""
        token_x, token_y = self.token_selector.get_coordinate()
        teleport_x, teleport_y = self.teleport_selector.get_coordinate()
        
        if token_x == 0 and token_y == 0:
            QMessageBox.warning(self, "Warning", "Instance token location not set")
            return
        
        if teleport_x == 0 and teleport_y == 0:
            QMessageBox.warning(self, "Warning", "Instance teleport location not set")
            return
        
        # Get delay in minutes and seconds for display
        delay_seconds = self.token_delay_selector.get_time()
        delay_minutes = int(delay_seconds // 60)
        delay_secs = int(delay_seconds % 60)
        delay_str = f"{delay_minutes} min {delay_secs} sec" if delay_minutes > 0 else f"{delay_secs} sec"
        
        QMessageBox.information(
            self,
            "Test Instance Entry",
            f"Instance entry sequence will be executed:\n\n"
            f"1. Click instance token at ({token_x}, {token_y})\n"
            f"2. Wait {delay_str}\n"
            f"3. Click teleport at ({teleport_x}, {teleport_y})\n\n"
            "Note: This is just a test. The actual entry will not be executed."
        )
    
    def on_save_entry_clicked(self):
        """Handle save entry button click"""
        try:
            # Get values
            token_x, token_y = self.token_selector.get_coordinate()
            teleport_x, teleport_y = self.teleport_selector.get_coordinate()
            token_delay = self.token_delay_selector.get_time()
            
            # Create coordinates
            token_coord = Coordinate(token_x, token_y, "Instance Token")
            teleport_coord = Coordinate(teleport_x, teleport_y, "Instance Teleport")
            
            # Save to config
            self.config_manager.set_coordinate('instance_token_location', token_coord)
            self.config_manager.set_coordinate('instance_teleport_location', teleport_coord)
            self.config_manager.set('instance_token_delay', token_delay)
            
            QMessageBox.information(
                self,
                "Settings Saved",
                "Instance entry settings saved successfully."
            )
        
        except Exception as e:
            logger.error(f"Error saving instance entry settings: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving instance entry settings: {e}"
            )
    
    def on_test_aggro_clicked(self):
        """Handle test aggro button click"""
        aggro_x, aggro_y = self.aggro_selector.get_coordinate()
        
        if aggro_x == 0 and aggro_y == 0:
            QMessageBox.warning(self, "Warning", "Aggro potion location not set")
            return
        
        # Get duration in minutes and seconds for display
        duration_seconds = self.aggro_duration_selector.get_time()
        duration_minutes = int(duration_seconds // 60)
        duration_secs = int(duration_seconds % 60)
        duration_str = f"{duration_minutes} min {duration_secs} sec" if duration_minutes > 0 else f"{duration_secs} sec"
        
        QMessageBox.information(
            self,
            "Test Aggro Potion",
            f"Aggro potion will be used at ({aggro_x}, {aggro_y}).\n\n"
            f"Duration: {duration_str}\n\n"
            "Note: This is just a test. The actual potion will not be used."
        )
    
    def on_save_aggro_clicked(self):
        """Handle save aggro button click"""
        try:
            # Get values
            aggro_x, aggro_y = self.aggro_selector.get_coordinate()
            aggro_duration = self.aggro_duration_selector.get_time()
            visual_check = self.visual_check_checkbox.isChecked()
            
            # Create coordinate
            aggro_coord = Coordinate(aggro_x, aggro_y, "Aggro Potion")
            
            # Save to config
            self.config_manager.set_coordinate('aggro_potion_location', aggro_coord)
            self.config_manager.set('aggro_duration', aggro_duration)
            self.config_manager.set('aggro_visual_check', visual_check)
            
            # Save ROI if visual check is enabled
            if visual_check:
                roi = self.roi_selector.get_roi()
                self.config_manager.set_roi('aggro_effect_roi', roi)
                
                # Color is saved automatically by the ColorSpecEditor
            
            QMessageBox.information(
                self,
                "Settings Saved",
                "Aggro potion settings saved successfully."
            )
        
        except Exception as e:
            logger.error(f"Error saving aggro potion settings: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving aggro potion settings: {e}"
            )