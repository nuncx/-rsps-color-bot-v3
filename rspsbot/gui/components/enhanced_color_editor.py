"""
Enhanced color editor component for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QCheckBox, QGridLayout, QColorDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from ...core.config import ColorSpec
from .color_picker import ColorPicker

# Get module logger
logger = logging.getLogger('rspsbot.gui.components.enhanced_color_editor')

class EnhancedColorEditor(QWidget):
    """
    Enhanced editor for ColorSpec objects
    """
    
    colorChanged = pyqtSignal(ColorSpec)
    
    def __init__(self, config_manager, color_key, parent=None):
        """
        Initialize the enhanced color editor
        
        Args:
            config_manager: Configuration manager
            color_key: Configuration key for the color spec
            parent: Parent widget
        """
        super().__init__(parent)
        self.config_manager = config_manager
        self.color_key = color_key
        
        # Get initial color spec
        self.color_spec = self.config_manager.get_color_spec(color_key)
        if self.color_spec is None:
            # Create default color spec
            self.color_spec = ColorSpec((255, 0, 0))
        
        # Initialize UI
        self.init_ui()
        
        # Update UI with current values
        self.update_ui_from_color_spec()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Color picker
        self.color_picker = ColorPicker(self.config_manager)
        self.color_picker.colorChanged.connect(self.on_color_changed)
        self.color_picker.setToolTip("Select a color using the color picker or pipette tool")
        main_layout.addWidget(self.color_picker)
        
        # HSV settings
        hsv_group = QWidget()
        hsv_layout = QGridLayout(hsv_group)
        hsv_layout.setContentsMargins(0, 0, 0, 0)
        
        # Use HSV checkbox
        self.use_hsv_checkbox = QCheckBox("Use HSV")
        self.use_hsv_checkbox.setChecked(self.color_spec.use_hsv if hasattr(self.color_spec, 'use_hsv') else False)
        self.use_hsv_checkbox.toggled.connect(self.on_use_hsv_toggled)
        self.use_hsv_checkbox.setToolTip("Use HSV color space instead of RGB for more accurate color detection")
        hsv_layout.addWidget(self.use_hsv_checkbox, 0, 0, 1, 2)
        
        # HSV tolerances
        hsv_layout.addWidget(QLabel("Hue Tolerance:"), 1, 0)
        self.h_tol_slider = QSlider(Qt.Horizontal)
        self.h_tol_slider.setRange(0, 30)
        self.h_tol_slider.setValue(self.color_spec.tol_h if hasattr(self.color_spec, 'tol_h') else 5)
        self.h_tol_slider.valueChanged.connect(self.on_h_tol_changed)
        self.h_tol_slider.setToolTip("Tolerance for hue component in HSV color space")
        hsv_layout.addWidget(self.h_tol_slider, 1, 1)

        self.h_tol_spin = QSpinBox()
        self.h_tol_spin.setRange(0, 30)
        self.h_tol_spin.setValue(self.color_spec.tol_h if hasattr(self.color_spec, 'tol_h') else 5)
        self.h_tol_spin.valueChanged.connect(self.on_h_tol_changed)
        hsv_layout.addWidget(self.h_tol_spin, 1, 2)
        
        hsv_layout.addWidget(QLabel("Saturation Tolerance:"), 2, 0)
        self.s_tol_slider = QSlider(Qt.Horizontal)
        self.s_tol_slider.setRange(0, 100)
        self.s_tol_slider.setValue(self.color_spec.tol_s if hasattr(self.color_spec, 'tol_s') else 50)
        self.s_tol_slider.valueChanged.connect(self.on_s_tol_changed)
        self.s_tol_slider.setToolTip("Tolerance for saturation component in HSV color space")
        hsv_layout.addWidget(self.s_tol_slider, 2, 1)

        self.s_tol_spin = QSpinBox()
        self.s_tol_spin.setRange(0, 100)
        self.s_tol_spin.setValue(self.color_spec.tol_s if hasattr(self.color_spec, 'tol_s') else 50)
        self.s_tol_spin.valueChanged.connect(self.on_s_tol_changed)
        hsv_layout.addWidget(self.s_tol_spin, 2, 2)
        
        hsv_layout.addWidget(QLabel("Value Tolerance:"), 3, 0)
        self.v_tol_slider = QSlider(Qt.Horizontal)
        self.v_tol_slider.setRange(0, 100)
        self.v_tol_slider.setValue(self.color_spec.tol_v if hasattr(self.color_spec, 'tol_v') else 50)
        self.v_tol_slider.valueChanged.connect(self.on_v_tol_changed)
        self.v_tol_slider.setToolTip("Tolerance for value component in HSV color space")
        hsv_layout.addWidget(self.v_tol_slider, 3, 1)

        self.v_tol_spin = QSpinBox()
        self.v_tol_spin.setRange(0, 100)
        self.v_tol_spin.setValue(self.color_spec.tol_v if hasattr(self.color_spec, 'tol_v') else 50)
        self.v_tol_spin.valueChanged.connect(self.on_v_tol_changed)
        hsv_layout.addWidget(self.v_tol_spin, 3, 2)
        
        main_layout.addWidget(hsv_group)
        
        # Update HSV controls state
        self.update_hsv_controls_state()
    
    def update_ui_from_color_spec(self):
        """Update UI from color spec"""
        # Set color
        if hasattr(self.color_spec, 'r') and hasattr(self.color_spec, 'g') and hasattr(self.color_spec, 'b'):
            self.color_picker.set_color(QColor(self.color_spec.r, self.color_spec.g, self.color_spec.b))
        
        # Set tolerance
        if hasattr(self.color_spec, 'tolerance'):
            self.color_picker.set_tolerance(self.color_spec.tolerance)
        
        # Set HSV settings
        if hasattr(self.color_spec, 'use_hsv'):
            self.use_hsv_checkbox.setChecked(self.color_spec.use_hsv)
        
        if hasattr(self.color_spec, 'tol_h'):
            self.h_tol_slider.setValue(self.color_spec.tol_h)
            self.h_tol_spin.setValue(self.color_spec.tol_h)
        
        if hasattr(self.color_spec, 'tol_s'):
            self.s_tol_slider.setValue(self.color_spec.tol_s)
            self.s_tol_spin.setValue(self.color_spec.tol_s)
        
        if hasattr(self.color_spec, 'tol_v'):
            self.v_tol_slider.setValue(self.color_spec.tol_v)
            self.v_tol_spin.setValue(self.color_spec.tol_v)
        
        # Update HSV controls state
        self.update_hsv_controls_state()
    
    def update_hsv_controls_state(self):
        """Update HSV controls state"""
        use_hsv = self.use_hsv_checkbox.isChecked()
        
        self.h_tol_slider.setEnabled(use_hsv)
        self.h_tol_spin.setEnabled(use_hsv)
        self.s_tol_slider.setEnabled(use_hsv)
        self.s_tol_spin.setEnabled(use_hsv)
        self.v_tol_slider.setEnabled(use_hsv)
        self.v_tol_spin.setEnabled(use_hsv)
    
    def on_color_changed(self, color):
        """Handle color change"""
        self.update_color_spec()
    
    def on_use_hsv_toggled(self, checked):
        """Handle use HSV checkbox toggle"""
        self.update_hsv_controls_state()
        self.update_color_spec()
    
    def on_h_tol_changed(self, value):
        """Handle hue tolerance change"""
        # Sync slider and spin box
        if self.sender() == self.h_tol_slider:
            self.h_tol_spin.blockSignals(True)
            self.h_tol_spin.setValue(value)
            self.h_tol_spin.blockSignals(False)
        else:
            self.h_tol_slider.blockSignals(True)
            self.h_tol_slider.setValue(value)
            self.h_tol_slider.blockSignals(False)
        
        self.update_color_spec()
    
    def on_s_tol_changed(self, value):
        """Handle saturation tolerance change"""
        # Sync slider and spin box
        if self.sender() == self.s_tol_slider:
            self.s_tol_spin.blockSignals(True)
            self.s_tol_spin.setValue(value)
            self.s_tol_spin.blockSignals(False)
        else:
            self.s_tol_slider.blockSignals(True)
            self.s_tol_slider.setValue(value)
            self.s_tol_slider.blockSignals(False)
        
        self.update_color_spec()
    
    def on_v_tol_changed(self, value):
        """Handle value tolerance change"""
        # Sync slider and spin box
        if self.sender() == self.v_tol_slider:
            self.v_tol_spin.blockSignals(True)
            self.v_tol_spin.setValue(value)
            self.v_tol_spin.blockSignals(False)
        else:
            self.v_tol_slider.blockSignals(True)
            self.v_tol_slider.setValue(value)
            self.v_tol_slider.blockSignals(False)
        
        self.update_color_spec()
    
    def update_color_spec(self):
        """Update color spec from UI"""
        # Get color
        color = self.color_picker.get_color()
        
        # Create color spec
        color_spec = ColorSpec(
            r=color.red(),
            g=color.green(),
            b=color.blue(),
            tolerance=self.color_picker.get_tolerance()
        )
        
        # Set HSV settings
        if hasattr(color_spec, 'use_hsv'):
            color_spec.use_hsv = self.use_hsv_checkbox.isChecked()
        
        if hasattr(color_spec, 'tol_h'):
            color_spec.tol_h = self.h_tol_spin.value()
        
        if hasattr(color_spec, 'tol_s'):
            color_spec.tol_s = self.s_tol_spin.value()
        
        if hasattr(color_spec, 'tol_v'):
            color_spec.tol_v = self.v_tol_spin.value()
        
        # Save color spec
        self.color_spec = color_spec
        self.config_manager.set_color_spec(self.color_key, color_spec)
        
        # Emit signal
        self.colorChanged.emit(color_spec)
    
    def get_color_spec(self):
        """
        Get the current color spec
        
        Returns:
            ColorSpec: Current color spec
        """
        return self.color_spec