"""
Combat settings panel for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QCheckBox, QSpinBox, QDoubleSpinBox, QComboBox, QGridLayout
)
from PyQt5.QtCore import Qt

from .detection_panel import ColorSpecEditor
from ..components.screen_picker import ZoomRoiPickerDialog

# Get module logger
logger = logging.getLogger('rspsbot.gui.panels.combat_panel')

class CombatPanel(QWidget):
    """
    Panel for combat settings
    """
    
    def __init__(self, config_manager, bot_controller):
        """
        Initialize the combat panel
        
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
        
        # HP bar detection group
        hpbar_group = QGroupBox("HP Bar Detection")
        hpbar_layout = QVBoxLayout(hpbar_group)
        
        # Enable HP bar detection
        enable_layout = QHBoxLayout()
        
        self.hpbar_detect_checkbox = QCheckBox("Enable HP Bar Detection")
        self.hpbar_detect_checkbox.setChecked(self.config_manager.get('hpbar_detect_enabled', True))
        self.hpbar_detect_checkbox.toggled.connect(self.on_hpbar_detect_toggled)
        enable_layout.addWidget(self.hpbar_detect_checkbox)
        
        enable_layout.addStretch()
        
        hpbar_layout.addLayout(enable_layout)
        
        # HP bar color
        hpbar_color_group = QGroupBox("HP Bar Color")
        hpbar_color_layout = QVBoxLayout(hpbar_color_group)
        
        # HP bar color editor
        self.hpbar_color_editor = ColorSpecEditor(self.config_manager, 'hpbar_color')
        hpbar_color_layout.addWidget(self.hpbar_color_editor)
        
        hpbar_layout.addWidget(hpbar_color_group)

        # HP bar ROI selection
        hpbar_roi_group = QGroupBox("HP Bar ROI")
        hpbar_roi_layout = QVBoxLayout(hpbar_roi_group)

        roi_row = QHBoxLayout()
        self.hpbar_roi_label = QLabel(self._roi_text(self.config_manager.get('hpbar_roi')))
        roi_row.addWidget(self.hpbar_roi_label)
        roi_row.addStretch()
        self.hpbar_roi_pick_btn = QPushButton("Pick From Screen")
        self.hpbar_roi_pick_btn.clicked.connect(self.on_pick_hpbar_roi)
        roi_row.addWidget(self.hpbar_roi_pick_btn)
        self.hpbar_roi_clear_btn = QPushButton("Clear")
        self.hpbar_roi_clear_btn.clicked.connect(self.on_clear_hpbar_roi)
        roi_row.addWidget(self.hpbar_roi_clear_btn)
        hpbar_roi_layout.addLayout(roi_row)

        hpbar_layout.addWidget(hpbar_roi_group)

        # HP bar settings
        settings_layout = QGridLayout()
        
        settings_layout.addWidget(QLabel("Minimum Area:"), 0, 0)
        self.hpbar_min_area_spin = QSpinBox()
        self.hpbar_min_area_spin.setRange(10, 200)
        self.hpbar_min_area_spin.setValue(self.config_manager.get('hpbar_min_area', 50))
        self.hpbar_min_area_spin.valueChanged.connect(self.on_hpbar_min_area_changed)
        settings_layout.addWidget(self.hpbar_min_area_spin, 0, 1)
        
        settings_layout.addWidget(QLabel("Minimum Pixel Matches:"), 1, 0)
        self.hpbar_min_pixel_matches_spin = QSpinBox()
        self.hpbar_min_pixel_matches_spin.setRange(50, 500)
        self.hpbar_min_pixel_matches_spin.setValue(self.config_manager.get('hpbar_min_pixel_matches', 150))
        self.hpbar_min_pixel_matches_spin.valueChanged.connect(self.on_hpbar_min_pixel_matches_changed)
        settings_layout.addWidget(self.hpbar_min_pixel_matches_spin, 1, 1)
        
        hpbar_layout.addLayout(settings_layout)
        
        # Add HP bar group to main layout
        main_layout.addWidget(hpbar_group)
        
        # Combat timing group
        timing_group = QGroupBox("Combat Timing")
        timing_layout = QVBoxLayout(timing_group)
        
        # Post-combat delay
        post_combat_layout = QGridLayout()
        
        post_combat_layout.addWidget(QLabel("Post-Combat Delay Min:"), 0, 0)
        self.post_combat_delay_min_spin = QDoubleSpinBox()
        self.post_combat_delay_min_spin.setRange(0.1, 10.0)
        self.post_combat_delay_min_spin.setSingleStep(0.1)
        self.post_combat_delay_min_spin.setValue(self.config_manager.get('post_combat_delay_min_s', 1.0))
        self.post_combat_delay_min_spin.setSuffix(" s")
        self.post_combat_delay_min_spin.valueChanged.connect(self.on_post_combat_delay_min_changed)
        post_combat_layout.addWidget(self.post_combat_delay_min_spin, 0, 1)
        
        post_combat_layout.addWidget(QLabel("Post-Combat Delay Max:"), 1, 0)
        self.post_combat_delay_max_spin = QDoubleSpinBox()
        self.post_combat_delay_max_spin.setRange(0.1, 10.0)
        self.post_combat_delay_max_spin.setSingleStep(0.1)
        self.post_combat_delay_max_spin.setValue(self.config_manager.get('post_combat_delay_max_s', 3.0))
        self.post_combat_delay_max_spin.setSuffix(" s")
        self.post_combat_delay_max_spin.valueChanged.connect(self.on_post_combat_delay_max_changed)
        post_combat_layout.addWidget(self.post_combat_delay_max_spin, 1, 1)
        
        post_combat_layout.addWidget(QLabel("Combat Not Seen Timeout:"), 2, 0)
        
        # Use TimeSelector instead of QDoubleSpinBox
        from ..components.time_selector import TimeSelector
        self.combat_timeout_selector = TimeSelector(label="", initial_seconds=self.config_manager.get('combat_not_seen_timeout_s', 10.0))
        self.combat_timeout_selector.timeChanged.connect(self.on_combat_timeout_changed)
        self.combat_timeout_selector.setToolTip("Time to wait after combat is not detected before considering combat to be over")
        post_combat_layout.addWidget(self.combat_timeout_selector, 2, 1)
        
        timing_layout.addLayout(post_combat_layout)
        
        # Add timing group to main layout
        main_layout.addWidget(timing_group)
        
        # Camera adjustment group
        camera_group = QGroupBox("Camera Adjustment")
        camera_layout = QVBoxLayout(camera_group)
        
        # Enable camera adjustment
        enable_cam_layout = QHBoxLayout()
        
        self.enable_cam_adjust_checkbox = QCheckBox("Enable Camera Adjustment")
        self.enable_cam_adjust_checkbox.setChecked(self.config_manager.get('enable_cam_adjust', True))
        self.enable_cam_adjust_checkbox.toggled.connect(self.on_enable_cam_adjust_toggled)
        enable_cam_layout.addWidget(self.enable_cam_adjust_checkbox)
        
        enable_cam_layout.addStretch()
        
        camera_layout.addLayout(enable_cam_layout)
        
        # Camera adjustment settings
        cam_settings_layout = QGridLayout()
        
        cam_settings_layout.addWidget(QLabel("Hold Time:"), 0, 0)
        self.cam_adjust_hold_spin = QDoubleSpinBox()
        self.cam_adjust_hold_spin.setRange(0.01, 0.5)
        self.cam_adjust_hold_spin.setSingleStep(0.01)
        self.cam_adjust_hold_spin.setValue(self.config_manager.get('cam_adjust_hold_s', 0.08))
        self.cam_adjust_hold_spin.setSuffix(" s")
        self.cam_adjust_hold_spin.valueChanged.connect(self.on_cam_adjust_hold_changed)
        cam_settings_layout.addWidget(self.cam_adjust_hold_spin, 0, 1)
        
        cam_settings_layout.addWidget(QLabel("Gap Time:"), 1, 0)
        self.cam_adjust_gap_spin = QDoubleSpinBox()
        self.cam_adjust_gap_spin.setRange(0.01, 0.5)
        self.cam_adjust_gap_spin.setSingleStep(0.01)
        self.cam_adjust_gap_spin.setValue(self.config_manager.get('cam_adjust_gap_s', 0.03))
        self.cam_adjust_gap_spin.setSuffix(" s")
        self.cam_adjust_gap_spin.valueChanged.connect(self.on_cam_adjust_gap_changed)
        cam_settings_layout.addWidget(self.cam_adjust_gap_spin, 1, 1)
        
        camera_layout.addLayout(cam_settings_layout)
        
        # Micro adjustment settings
        micro_layout = QGridLayout()
        
        micro_layout.addWidget(QLabel("Micro Adjust Every:"), 0, 0)
        self.micro_adjust_every_spin = QSpinBox()
        self.micro_adjust_every_spin.setRange(1, 20)
        self.micro_adjust_every_spin.setValue(self.config_manager.get('micro_adjust_every_loops', 8))
        self.micro_adjust_every_spin.valueChanged.connect(self.on_micro_adjust_every_changed)
        micro_layout.addWidget(self.micro_adjust_every_spin, 0, 1)
        
        micro_layout.addWidget(QLabel("Micro Hold Time:"), 1, 0)
        self.micro_adjust_hold_spin = QDoubleSpinBox()
        self.micro_adjust_hold_spin.setRange(0.01, 0.5)
        self.micro_adjust_hold_spin.setSingleStep(0.01)
        self.micro_adjust_hold_spin.setValue(self.config_manager.get('micro_adjust_hold_s', 0.04))
        self.micro_adjust_hold_spin.setSuffix(" s")
        self.micro_adjust_hold_spin.valueChanged.connect(self.on_micro_adjust_hold_changed)
        micro_layout.addWidget(self.micro_adjust_hold_spin, 1, 1)
        
        micro_layout.addWidget(QLabel("Micro Gap Time:"), 2, 0)
        self.micro_adjust_gap_spin = QDoubleSpinBox()
        self.micro_adjust_gap_spin.setRange(0.01, 0.5)
        self.micro_adjust_gap_spin.setSingleStep(0.01)
        self.micro_adjust_gap_spin.setValue(self.config_manager.get('micro_adjust_gap_s', 0.03))
        self.micro_adjust_gap_spin.setSuffix(" s")
        self.micro_adjust_gap_spin.valueChanged.connect(self.on_micro_adjust_gap_changed)
        micro_layout.addWidget(self.micro_adjust_gap_spin, 2, 1)
        
        camera_layout.addLayout(micro_layout)
        
        # Add camera group to main layout
        main_layout.addWidget(camera_group)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

    def _roi_text(self, roi_dict):
        if not roi_dict:
            return "(none)"
        try:
            return f"{roi_dict['left']},{roi_dict['top']}  {roi_dict['width']}x{roi_dict['height']}"
        except Exception:
            return str(roi_dict)

    def on_pick_hpbar_roi(self):
        dlg = ZoomRoiPickerDialog(self.config_manager, self)
        if dlg.exec_() == dlg.Accepted and dlg.result_rect is not None:
            r = dlg.result_rect
            roi = {"left": int(r.left()), "top": int(r.top()), "width": int(r.width()), "height": int(r.height())}
            self.config_manager.set('hpbar_roi', roi)
            self.hpbar_roi_label.setText(self._roi_text(roi))
            logger.info(f"HP bar ROI set to {roi}")

    def on_clear_hpbar_roi(self):
        self.config_manager.set('hpbar_roi', None)
        self.hpbar_roi_label.setText(self._roi_text(None))
        logger.info("HP bar ROI cleared")
    
    def on_hpbar_detect_toggled(self, checked):
        """Handle HP bar detection toggle"""
        logger.debug(f"HP bar detection {'enabled' if checked else 'disabled'}")
        self.config_manager.set('hpbar_detect_enabled', checked)
    
    def on_hpbar_min_area_changed(self, value):
        """Handle HP bar min area change"""
        logger.debug(f"HP bar minimum area set to {value}")
        self.config_manager.set('hpbar_min_area', value)
    
    def on_hpbar_min_pixel_matches_changed(self, value):
        """Handle HP bar min pixel matches change"""
        logger.debug(f"HP bar minimum pixel matches set to {value}")
        self.config_manager.set('hpbar_min_pixel_matches', value)
    
    def on_post_combat_delay_min_changed(self, value):
        """Handle post-combat delay min change"""
        logger.debug(f"Post-combat delay min set to {value} seconds")
        self.config_manager.set('post_combat_delay_min_s', value)
        
        # Ensure max is not less than min
        if value > self.post_combat_delay_max_spin.value():
            self.post_combat_delay_max_spin.setValue(value)
    
    def on_post_combat_delay_max_changed(self, value):
        """Handle post-combat delay max change"""
        logger.debug(f"Post-combat delay max set to {value} seconds")
        self.config_manager.set('post_combat_delay_max_s', value)
        
        # Ensure min is not greater than max
        if value < self.post_combat_delay_min_spin.value():
            self.post_combat_delay_min_spin.setValue(value)
    
    def on_combat_timeout_changed(self, value):
        """Handle combat timeout change"""
        logger.debug(f"Combat not seen timeout set to {value} seconds")
        self.config_manager.set('combat_not_seen_timeout_s', value)
    
    def on_enable_cam_adjust_toggled(self, checked):
        """Handle enable camera adjustment toggle"""
        logger.debug(f"Camera adjustment {'enabled' if checked else 'disabled'}")
        self.config_manager.set('enable_cam_adjust', checked)
    
    def on_cam_adjust_hold_changed(self, value):
        """Handle camera adjust hold change"""
        logger.debug(f"Camera adjust hold set to {value} seconds")
        self.config_manager.set('cam_adjust_hold_s', value)
    
    def on_cam_adjust_gap_changed(self, value):
        """Handle camera adjust gap change"""
        logger.debug(f"Camera adjust gap set to {value} seconds")
        self.config_manager.set('cam_adjust_gap_s', value)
    
    def on_micro_adjust_every_changed(self, value):
        """Handle micro adjust every change"""
        logger.debug(f"Micro adjust every set to {value} loops")
        self.config_manager.set('micro_adjust_every_loops', value)
    
    def on_micro_adjust_hold_changed(self, value):
        """Handle micro adjust hold change"""
        logger.debug(f"Micro adjust hold set to {value} seconds")
        self.config_manager.set('micro_adjust_hold_s', value)
    
    def on_micro_adjust_gap_changed(self, value):
        """Handle micro adjust gap change"""
        logger.debug(f"Micro adjust gap set to {value} seconds")
        self.config_manager.set('micro_adjust_gap_s', value)