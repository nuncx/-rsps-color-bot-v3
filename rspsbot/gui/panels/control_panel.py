"""
Control panel for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

# Get module logger
logger = logging.getLogger('rspsbot.gui.panels.control_panel')

class ControlPanel(QWidget):
    """
    Main control panel for the bot
    """
    
    def __init__(self, config_manager, bot_controller):
        """
        Initialize the control panel
        
        Args:
            config_manager: Configuration manager
            bot_controller: Bot controller
        """
        super().__init__()
        self.config_manager = config_manager
        self.bot_controller = bot_controller
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Window selection group
        window_group = QGroupBox("Window Selection")
        window_layout = QVBoxLayout(window_group)
        
        # Window selection combo box
        self.window_combo = QComboBox()
        self.window_combo.setEditable(True)
        self.window_combo.setMinimumWidth(300)
        window_layout.addWidget(self.window_combo)
        
        # Refresh and focus buttons
        window_buttons_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        window_buttons_layout.addWidget(self.refresh_button)
        
        self.focus_button = QPushButton("Focus")
        self.focus_button.clicked.connect(self.on_focus_clicked)
        window_buttons_layout.addWidget(self.focus_button)
        
        window_layout.addLayout(window_buttons_layout)
        
        # Add window group to main layout
        main_layout.addWidget(window_group)
        
        # Bot settings group
        settings_group = QGroupBox("Bot Settings")
        settings_layout = QVBoxLayout(settings_group)

        # Feature toggles
        toggles_layout = QHBoxLayout()

        self.enable_instance_checkbox = QCheckBox("Enable Instance")
        self.enable_instance_checkbox.setChecked(self.config_manager.get('enable_instance', True))
        self.enable_instance_checkbox.toggled.connect(lambda v: self.config_manager.set('enable_instance', v))
        toggles_layout.addWidget(self.enable_instance_checkbox)

        self.enable_potions_checkbox = QCheckBox("Enable Potions")
        self.enable_potions_checkbox.setChecked(self.config_manager.get('enable_potions', True))
        self.enable_potions_checkbox.toggled.connect(lambda v: self.config_manager.set('enable_potions', v))
        toggles_layout.addWidget(self.enable_potions_checkbox)

        self.enable_teleport_checkbox = QCheckBox("Enable Teleport")
        self.enable_teleport_checkbox.setChecked(self.config_manager.get('enable_teleport', True))
        self.enable_teleport_checkbox.toggled.connect(lambda v: self.config_manager.set('enable_teleport', v))
        toggles_layout.addWidget(self.enable_teleport_checkbox)

        toggles_layout.addStretch()
        settings_layout.addLayout(toggles_layout)

        # Humanization settings
        humanize_layout = QHBoxLayout()
        
        self.humanize_checkbox = QCheckBox("Enable Humanization")
        self.humanize_checkbox.setChecked(self.config_manager.get('humanize_on', True))
        self.humanize_checkbox.toggled.connect(self.on_humanize_toggled)
        humanize_layout.addWidget(self.humanize_checkbox)
        
        settings_layout.addLayout(humanize_layout)
        
        # Break settings
        break_layout = QVBoxLayout()
        
        # Break every
        break_every_layout = QHBoxLayout()
        break_every_layout.addWidget(QLabel("Break Every:"))
        
        # Use TimeSelector instead of QDoubleSpinBox
        from ..components.time_selector import TimeSelector
        self.break_every_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('break_every_s', 180))
        self.break_every_selector.setToolTip("Time between breaks")
        self.break_every_selector.timeChanged.connect(self.on_break_every_changed)
        break_every_layout.addWidget(self.break_every_selector)
        break_every_layout.addStretch()
        break_layout.addLayout(break_every_layout)
        
        # Break duration
        break_duration_layout = QHBoxLayout()
        break_duration_layout.addWidget(QLabel("Break Duration:"))
        
        self.break_duration_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('break_duration_s', 4))
        self.break_duration_selector.setToolTip("Duration of each break")
        self.break_duration_selector.timeChanged.connect(self.on_break_duration_changed)
        break_duration_layout.addWidget(self.break_duration_selector)
        break_duration_layout.addStretch()
        break_layout.addLayout(break_duration_layout)
        
        settings_layout.addLayout(break_layout)
        
        # Max runtime settings
        runtime_layout = QHBoxLayout()
        
        runtime_layout.addWidget(QLabel("Max Runtime:"))
        
        # Use TimeSelector instead of QDoubleSpinBox
        from ..components.time_selector import TimeSelector
        self.max_runtime_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('max_runtime_s', 0))
        self.max_runtime_selector.setToolTip("Maximum time the bot will run (0 = unlimited)")
        self.max_runtime_selector.timeChanged.connect(self.on_max_runtime_changed)
        runtime_layout.addWidget(self.max_runtime_selector)
        
        # Add unlimited checkbox
        self.unlimited_runtime_checkbox = QCheckBox("Unlimited")
        self.unlimited_runtime_checkbox.setChecked(self.config_manager.get('max_runtime_s', 0) == 0)
        self.unlimited_runtime_checkbox.toggled.connect(self.on_unlimited_runtime_toggled)
        self.unlimited_runtime_checkbox.setToolTip("Run the bot without time limit")
        runtime_layout.addWidget(self.unlimited_runtime_checkbox)
        
        runtime_layout.addStretch()
        settings_layout.addLayout(runtime_layout)
        
        # Add settings group to main layout
        main_layout.addWidget(settings_group)
        
        # Debug settings group
        debug_group = QGroupBox("Debug Settings")
        debug_layout = QVBoxLayout(debug_group)
        
        # Debug overlay checkbox
        self.debug_overlay_checkbox = QCheckBox("Enable Debug Overlay")
        self.debug_overlay_checkbox.setChecked(self.config_manager.get('debug_overlay', False))
        self.debug_overlay_checkbox.toggled.connect(self.on_debug_overlay_toggled)
        debug_layout.addWidget(self.debug_overlay_checkbox)
        
        # Overlay mode
        overlay_layout = QHBoxLayout()
        
        overlay_layout.addWidget(QLabel("Overlay Mode:"))
        
        self.overlay_mode_combo = QComboBox()
        self.overlay_mode_combo.addItems(["tile", "monster", "both"])
        self.overlay_mode_combo.setCurrentText(self.config_manager.get('overlay_mode', 'tile'))
        self.overlay_mode_combo.currentTextChanged.connect(self.on_overlay_mode_changed)
        overlay_layout.addWidget(self.overlay_mode_combo)
        
        debug_layout.addLayout(overlay_layout)

        # Overlay options
        overlay_opts = QHBoxLayout()
        self.overlay_counts_checkbox = QCheckBox("Show Counts")
        self.overlay_counts_checkbox.setChecked(self.config_manager.get('show_overlay_counts', True))
        self.overlay_counts_checkbox.toggled.connect(lambda v: self.config_manager.set('show_overlay_counts', v))
        overlay_opts.addWidget(self.overlay_counts_checkbox)

        self.overlay_follow_checkbox = QCheckBox("Follow Window")
        self.overlay_follow_checkbox.setChecked(self.config_manager.get('overlay_follow_window', False))
        self.overlay_follow_checkbox.toggled.connect(lambda v: self.config_manager.set('overlay_follow_window', v))
        overlay_opts.addWidget(self.overlay_follow_checkbox)

        self.overlay_clip_checkbox = QCheckBox("Clip to ROI")
        self.overlay_clip_checkbox.setChecked(self.config_manager.get('overlay_clip_to_roi', False))
        self.overlay_clip_checkbox.toggled.connect(lambda v: self.config_manager.set('overlay_clip_to_roi', v))
        overlay_opts.addWidget(self.overlay_clip_checkbox)

        overlay_opts.addStretch()
        debug_layout.addLayout(overlay_opts)

        # Save snapshots checkbox
        self.save_snapshots_checkbox = QCheckBox("Save Debug Snapshots")
        self.save_snapshots_checkbox.setChecked(self.config_manager.get('debug_save_snapshots', False))
        self.save_snapshots_checkbox.toggled.connect(self.on_save_snapshots_toggled)
        debug_layout.addWidget(self.save_snapshots_checkbox)
        
        # Add debug group to main layout
        main_layout.addWidget(debug_group)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
        
        # Populate window list
        self.refresh_window_list()
    
    def refresh_window_list(self):
        """Refresh the window list"""
        try:
            from rspsbot.core.detection.capture import CaptureService
            
            # Create temporary capture service
            capture_service = CaptureService()
            
            # Get window list
            windows = capture_service.list_windows()
            
            # Clear and populate combo box
            self.window_combo.clear()
            self.window_combo.addItems(windows)
            
            # Set current window from config
            current_window = self.config_manager.get('window_title', '')
            if current_window:
                index = self.window_combo.findText(current_window)
                if index >= 0:
                    self.window_combo.setCurrentIndex(index)
        
        except Exception as e:
            logger.error(f"Error refreshing window list: {e}")
    
    def on_refresh_clicked(self):
        """Handle refresh button click"""
        logger.debug("Refreshing window list")
        self.refresh_window_list()
    
    def on_focus_clicked(self):
        """Handle focus button click"""
        window_title = self.window_combo.currentText()
        
        if not window_title:
            logger.warning("No window selected")
            return
        
        logger.debug(f"Focusing window: {window_title}")
        
        try:
            from rspsbot.core.detection.capture import CaptureService
            
            # Create temporary capture service
            capture_service = CaptureService()
            
            # Focus window
            success = capture_service.focus_window(window_title)
            
            if success:
                # Update config
                self.config_manager.set('window_title', window_title)
                logger.info(f"Focused window: {window_title}")
            else:
                logger.warning(f"Failed to focus window: {window_title}")
        
        except Exception as e:
            logger.error(f"Error focusing window: {e}")
    
    def on_humanize_toggled(self, checked):
        """Handle humanize checkbox toggle"""
        logger.debug(f"Humanization {'enabled' if checked else 'disabled'}")
        self.config_manager.set('humanize_on', checked)
    
    def on_break_every_changed(self, value):
        """Handle break every value change"""
        logger.debug(f"Break every set to {value} seconds")
        self.config_manager.set('break_every_s', value)
    
    def on_break_duration_changed(self, value):
        """Handle break duration value change"""
        logger.debug(f"Break duration set to {value} seconds")
        self.config_manager.set('break_duration_s', value)
    
    def on_max_runtime_changed(self, value):
        """Handle max runtime value change"""
        if value == 0:
            logger.debug("Max runtime set to unlimited")
            self.unlimited_runtime_checkbox.setChecked(True)
        else:
            logger.debug(f"Max runtime set to {value} seconds")
            self.unlimited_runtime_checkbox.setChecked(False)
        
        self.config_manager.set('max_runtime_s', value)
        
    def on_unlimited_runtime_toggled(self, checked):
        """Handle unlimited runtime checkbox toggle"""
        if checked:
            self.max_runtime_selector.set_time(0)
            self.max_runtime_selector.setEnabled(False)
            logger.debug("Max runtime set to unlimited")
            self.config_manager.set('max_runtime_s', 0)
        else:
            self.max_runtime_selector.setEnabled(True)
            # Only update if it's currently 0
            if self.max_runtime_selector.get_time() == 0:
                self.max_runtime_selector.set_time(3600)  # Default to 1 hour
                self.config_manager.set('max_runtime_s', 3600)
    
    def on_debug_overlay_toggled(self, checked):
        """Handle debug overlay checkbox toggle"""
        logger.debug(f"Debug overlay {'enabled' if checked else 'disabled'}")
        self.config_manager.set('debug_overlay', checked)
    
    def on_overlay_mode_changed(self, mode):
        """Handle overlay mode change"""
        logger.debug(f"Overlay mode set to {mode}")
        self.config_manager.set('overlay_mode', mode)
    
    def on_save_snapshots_toggled(self, checked):
        """Handle save snapshots checkbox toggle"""
        logger.debug(f"Save snapshots {'enabled' if checked else 'disabled'}")
        self.config_manager.set('debug_save_snapshots', checked)