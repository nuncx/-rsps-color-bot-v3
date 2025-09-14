"""
Detection settings panel for RSPS Color Bot v3
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QCheckBox, QSpinBox, QDoubleSpinBox, QColorDialog,
    QFrame, QSlider, QGridLayout, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette

from ...core.config import ColorSpec
from ..components.screen_picker import ZoomColorPickerDialog
from ..components.enhanced_color_editor import EnhancedColorEditor
from ..components.advanced_roi_selector import AdvancedROISelector

# Get module logger
logger = logging.getLogger('rspsbot.gui.panels.detection_panel')

class ColorButton(QPushButton):
    """
    Button that displays and allows selection of a color
    """
    
    def __init__(self, color=None, parent=None):
        """
        Initialize the color button
        
        Args:
            color: Initial color (QColor or tuple)
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Set fixed size
        self.setFixedSize(30, 30)
        
        # Set color
        if color is None:
            self.color = QColor(255, 0, 0)
        elif isinstance(color, tuple):
            self.color = QColor(*color)
        else:
            self.color = color
        
        # Update button appearance
        self.update_color()
        
        # Connect click handler
        self.clicked.connect(self.on_clicked)
    
    def update_color(self):
        """Update button appearance with current color"""
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Button, self.color)
        self.setPalette(palette)
        
        # Set style sheet for better appearance
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color.name()};
                border: 1px solid #888888;
            }}
            QPushButton:hover {{
                border: 1px solid #000000;
            }}
        """)
        
        # Force update
        self.update()
    
    def on_clicked(self):
        """Handle button click"""
        # Open color dialog
        color = QColorDialog.getColor(self.color, self.parent(), "Select Color")
        
        # Update color if valid
        if color.isValid():
            self.color = color
            self.update_color()
            
            # Emit custom signal
            self.color_changed()
    
    def color_changed(self):
        """Custom signal for color change"""
        # This is a placeholder for subclasses to override
        pass
    
    def get_color(self):
        """Get current color as RGB tuple"""
        return (self.color.red(), self.color.green(), self.color.blue())
    
    def set_color(self, color):
        """Set current color"""
        if isinstance(color, tuple):
            self.color = QColor(*color)
        else:
            self.color = color
        
        self.update_color()

class ColorSpecEditor(QWidget):
    """
    Editor for ColorSpec objects
    """
    
    def __init__(self, config_manager, color_key, parent=None):
        """
        Initialize the color spec editor
        
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
        
        # Color selection
        color_layout = QHBoxLayout()
        
        color_layout.addWidget(QLabel("Color:"))
        
        self.color_button = ColorButton(self.color_spec.rgb)
        self.color_button.color_changed = self.on_color_changed
        color_layout.addWidget(self.color_button)

        self.pick_color_button = QPushButton("Pick From Screen")
        self.pick_color_button.clicked.connect(self.on_pick_color_from_screen)
        color_layout.addWidget(self.pick_color_button)
        
        color_layout.addStretch()
        
        main_layout.addLayout(color_layout)
        
        # RGB tolerance
        rgb_layout = QHBoxLayout()
        
        rgb_layout.addWidget(QLabel("RGB Tolerance:"))
        
        # Slider + spin pair for tolerance
        self.rgb_tol_slider = QSlider(Qt.Horizontal)
        self.rgb_tol_slider.setRange(0, 100)
        self.rgb_tol_slider.setValue(self.color_spec.tol_rgb)
        self.rgb_tol_slider.valueChanged.connect(self.on_rgb_tol_changed)
        rgb_layout.addWidget(self.rgb_tol_slider)

        self.rgb_tol_spin = QSpinBox()
        self.rgb_tol_spin.setRange(0, 100)
        self.rgb_tol_spin.setValue(self.color_spec.tol_rgb)
        self.rgb_tol_spin.valueChanged.connect(self.on_rgb_tol_changed)
        rgb_layout.addWidget(self.rgb_tol_spin)
        
        rgb_layout.addStretch()
        
        main_layout.addLayout(rgb_layout)
        
        # HSV settings
        hsv_layout = QGridLayout()
        
        # Use HSV checkbox
        self.use_hsv_checkbox = QCheckBox("Use HSV")
        self.use_hsv_checkbox.setChecked(self.color_spec.use_hsv)
        self.use_hsv_checkbox.toggled.connect(self.on_use_hsv_toggled)
        hsv_layout.addWidget(self.use_hsv_checkbox, 0, 0, 1, 2)
        
        # HSV tolerances
        hsv_layout.addWidget(QLabel("Hue Tolerance:"), 1, 0)
        self.h_tol_slider = QSlider(Qt.Horizontal)
        self.h_tol_slider.setRange(0, 30)
        self.h_tol_slider.setValue(self.color_spec.tol_h)
        self.h_tol_slider.valueChanged.connect(self.on_h_tol_changed)
        hsv_layout.addWidget(self.h_tol_slider, 1, 1)

        self.h_tol_spin = QSpinBox()
        self.h_tol_spin.setRange(0, 30)
        self.h_tol_spin.setValue(self.color_spec.tol_h)
        self.h_tol_spin.valueChanged.connect(self.on_h_tol_changed)
        hsv_layout.addWidget(self.h_tol_spin, 1, 2)
        
        hsv_layout.addWidget(QLabel("Saturation Tolerance:"), 2, 0)
        self.s_tol_slider = QSlider(Qt.Horizontal)
        self.s_tol_slider.setRange(0, 100)
        self.s_tol_slider.setValue(self.color_spec.tol_s)
        self.s_tol_slider.valueChanged.connect(self.on_s_tol_changed)
        hsv_layout.addWidget(self.s_tol_slider, 2, 1)

        self.s_tol_spin = QSpinBox()
        self.s_tol_spin.setRange(0, 100)
        self.s_tol_spin.setValue(self.color_spec.tol_s)
        self.s_tol_spin.valueChanged.connect(self.on_s_tol_changed)
        hsv_layout.addWidget(self.s_tol_spin, 2, 2)
        
        hsv_layout.addWidget(QLabel("Value Tolerance:"), 3, 0)
        self.v_tol_slider = QSlider(Qt.Horizontal)
        self.v_tol_slider.setRange(0, 100)
        self.v_tol_slider.setValue(self.color_spec.tol_v)
        self.v_tol_slider.valueChanged.connect(self.on_v_tol_changed)
        hsv_layout.addWidget(self.v_tol_slider, 3, 1)

        self.v_tol_spin = QSpinBox()
        self.v_tol_spin.setRange(0, 100)
        self.v_tol_spin.setValue(self.color_spec.tol_v)
        self.v_tol_spin.valueChanged.connect(self.on_v_tol_changed)
        hsv_layout.addWidget(self.v_tol_spin, 3, 2)
        
        main_layout.addLayout(hsv_layout)
        
        # Update HSV controls enabled state
        self.update_hsv_controls()
    
    def update_ui_from_color_spec(self):
        """Update UI components from color spec"""
        self.color_button.set_color(self.color_spec.rgb)
        self.rgb_tol_spin.setValue(self.color_spec.tol_rgb)
        self.rgb_tol_slider.setValue(self.color_spec.tol_rgb)
        self.use_hsv_checkbox.setChecked(self.color_spec.use_hsv)
        self.h_tol_spin.setValue(self.color_spec.tol_h)
        self.h_tol_slider.setValue(self.color_spec.tol_h)
        self.s_tol_spin.setValue(self.color_spec.tol_s)
        self.s_tol_slider.setValue(self.color_spec.tol_s)
        self.v_tol_spin.setValue(self.color_spec.tol_v)
        self.v_tol_slider.setValue(self.color_spec.tol_v)
        
        # Update HSV controls enabled state
        self.update_hsv_controls()
    
    def update_hsv_controls(self):
        """Update HSV controls enabled state"""
        enabled = self.use_hsv_checkbox.isChecked()
        self.h_tol_spin.setEnabled(enabled)
        self.h_tol_slider.setEnabled(enabled)
        self.s_tol_spin.setEnabled(enabled)
        self.s_tol_slider.setEnabled(enabled)
        self.v_tol_spin.setEnabled(enabled)
        self.v_tol_slider.setEnabled(enabled)
    
    def update_color_spec(self):
        """Update color spec from UI components"""
        try:
            self.color_spec = ColorSpec(
                rgb=self.color_button.get_color(),
                tol_rgb=self.rgb_tol_spin.value(),
                use_hsv=self.use_hsv_checkbox.isChecked(),
                tol_h=self.h_tol_spin.value(),
                tol_s=self.s_tol_spin.value(),
                tol_v=self.v_tol_spin.value()
            )
            
            # Save to config
            self.config_manager.set_color_spec(self.color_key, self.color_spec)
            
            logger.debug(f"Updated color spec for {self.color_key}")
        
        except Exception as e:
            logger.error(f"Error updating color spec: {e}")
    
    def on_color_changed(self):
        """Handle color change"""
        self.update_color_spec()
    
    def on_rgb_tol_changed(self, value):
        """Handle RGB tolerance change"""
        # keep slider and spin in sync
        if self.rgb_tol_slider.value() != value:
            self.rgb_tol_slider.blockSignals(True)
            self.rgb_tol_slider.setValue(value)
            self.rgb_tol_slider.blockSignals(False)
        if self.rgb_tol_spin.value() != value:
            self.rgb_tol_spin.blockSignals(True)
            self.rgb_tol_spin.setValue(value)
            self.rgb_tol_spin.blockSignals(False)
        self.update_color_spec()
    
    def on_use_hsv_toggled(self, checked):
        """Handle use HSV toggle"""
        self.update_hsv_controls()
        self.update_color_spec()
    
    def on_h_tol_changed(self, value):
        """Handle hue tolerance change"""
        if self.h_tol_slider.value() != value:
            self.h_tol_slider.blockSignals(True)
            self.h_tol_slider.setValue(value)
            self.h_tol_slider.blockSignals(False)
        if self.h_tol_spin.value() != value:
            self.h_tol_spin.blockSignals(True)
            self.h_tol_spin.setValue(value)
            self.h_tol_spin.blockSignals(False)
        self.update_color_spec()
    
    def on_s_tol_changed(self, value):
        """Handle saturation tolerance change"""
        if self.s_tol_slider.value() != value:
            self.s_tol_slider.blockSignals(True)
            self.s_tol_slider.setValue(value)
            self.s_tol_slider.blockSignals(False)
        if self.s_tol_spin.value() != value:
            self.s_tol_spin.blockSignals(True)
            self.s_tol_spin.setValue(value)
            self.s_tol_spin.blockSignals(False)
        self.update_color_spec()
    
    def on_v_tol_changed(self, value):
        """Handle value tolerance change"""
        if self.v_tol_slider.value() != value:
            self.v_tol_slider.blockSignals(True)
            self.v_tol_slider.setValue(value)
            self.v_tol_slider.blockSignals(False)
        if self.v_tol_spin.value() != value:
            self.v_tol_spin.blockSignals(True)
            self.v_tol_spin.setValue(value)
            self.v_tol_spin.blockSignals(False)
        self.update_color_spec()

    def on_pick_color_from_screen(self):
        dialog = ZoomColorPickerDialog(self.config_manager, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_color:
            self.color_button.set_color(dialog.selected_color)
            self.update_color_spec()

class MonsterColorDialog(QDialog):
    """
    Dialog for editing monster color
    """
    
    def __init__(self, parent=None, color_spec=None, config_manager=None):
        """
        Initialize the monster color dialog
        
        Args:
            parent: Parent widget
            color_spec: Color specification to edit (None for new color)
        """
        super().__init__(parent)
        self.color_spec = color_spec or ColorSpec((0, 255, 0))
        self.config_manager = config_manager
        
        self.setWindowTitle("Monster Color")
        self.setMinimumWidth(400)
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Color selection
        color_layout = QHBoxLayout()
        
        color_layout.addWidget(QLabel("Color:"))
        
        self.color_button = ColorButton(self.color_spec.rgb)
        color_layout.addWidget(self.color_button)

        # Pick from screen for monster color
        self.pick_color_button = QPushButton("Pick From Screen")
        self.pick_color_button.clicked.connect(self.on_pick_color_from_screen)
        color_layout.addWidget(self.pick_color_button)
        
        color_layout.addStretch()
        
        main_layout.addLayout(color_layout)
        
        # RGB tolerance
        rgb_layout = QHBoxLayout()
        
        rgb_layout.addWidget(QLabel("RGB Tolerance:"))
        
        self.rgb_tol_spin = QSpinBox()
        self.rgb_tol_spin.setRange(0, 100)
        self.rgb_tol_spin.setValue(self.color_spec.tol_rgb)
        rgb_layout.addWidget(self.rgb_tol_spin)
        
        rgb_layout.addStretch()
        
        main_layout.addLayout(rgb_layout)
        
        # HSV settings
        hsv_layout = QGridLayout()
        
        # Use HSV checkbox
        self.use_hsv_checkbox = QCheckBox("Use HSV")
        self.use_hsv_checkbox.setChecked(self.color_spec.use_hsv)
        self.use_hsv_checkbox.toggled.connect(self.on_use_hsv_toggled)
        hsv_layout.addWidget(self.use_hsv_checkbox, 0, 0, 1, 2)
        
        # HSV tolerances
        hsv_layout.addWidget(QLabel("Hue Tolerance:"), 1, 0)
        self.h_tol_spin = QSpinBox()
        self.h_tol_spin.setRange(0, 30)
        self.h_tol_spin.setValue(self.color_spec.tol_h)
        hsv_layout.addWidget(self.h_tol_spin, 1, 1)
        
        hsv_layout.addWidget(QLabel("Saturation Tolerance:"), 2, 0)
        self.s_tol_spin = QSpinBox()
        self.s_tol_spin.setRange(0, 100)
        self.s_tol_spin.setValue(self.color_spec.tol_s)
        hsv_layout.addWidget(self.s_tol_spin, 2, 1)
        
        hsv_layout.addWidget(QLabel("Value Tolerance:"), 3, 0)
        self.v_tol_spin = QSpinBox()
        self.v_tol_spin.setRange(0, 100)
        self.v_tol_spin.setValue(self.color_spec.tol_v)
        hsv_layout.addWidget(self.v_tol_spin, 3, 1)
        
        main_layout.addLayout(hsv_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Update HSV controls enabled state
        self.on_use_hsv_toggled(self.use_hsv_checkbox.isChecked())

    def on_pick_color_from_screen(self):
        dialog = ZoomColorPickerDialog(self.config_manager, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_color:
            self.color_button.set_color(dialog.selected_color)
    
    def on_use_hsv_toggled(self, checked):
        """Handle use HSV toggle"""
        self.h_tol_spin.setEnabled(checked)
        self.s_tol_spin.setEnabled(checked)
        self.v_tol_spin.setEnabled(checked)
    
    def get_color_spec(self):
        """Get color specification from UI components"""
        return ColorSpec(
            rgb=self.color_button.get_color(),
            tol_rgb=self.rgb_tol_spin.value(),
            use_hsv=self.use_hsv_checkbox.isChecked(),
            tol_h=self.h_tol_spin.value(),
            tol_s=self.s_tol_spin.value(),
            tol_v=self.v_tol_spin.value()
        )

class MonsterColorsEditor(QWidget):
    """
    Editor for multiple monster colors
    """
    
    def __init__(self, config_manager, parent=None):
        """
        Initialize the monster colors editor
        
        Args:
            config_manager: Configuration manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.config_manager = config_manager
        
        # Initialize UI
        self.init_ui()
        
        # Load monster colors
        self.load_monster_colors()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Colors table
        self.colors_table = QTableWidget()
        self.colors_table.setColumnCount(6)
        self.colors_table.setHorizontalHeaderLabels(["Color", "RGB", "RGB Tol", "HSV", "H Tol", "S/V Tol"])
        self.colors_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.colors_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.colors_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.colors_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.colors_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.colors_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.colors_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.colors_table.setSelectionMode(QTableWidget.SingleSelection)
        self.colors_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # Enable/disable buttons based on selection
        self.colors_table.itemSelectionChanged.connect(self.update_button_states)
        # Optional UX: double-click to edit
        self.colors_table.cellDoubleClicked.connect(lambda *_: self.on_edit_clicked())
        main_layout.addWidget(self.colors_table)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Color")
        self.add_button.clicked.connect(self.on_add_clicked)
        buttons_layout.addWidget(self.add_button)

        self.add_from_screen_button = QPushButton("Add From Screen")
        self.add_from_screen_button.clicked.connect(self.on_add_from_screen_clicked)
        buttons_layout.addWidget(self.add_from_screen_button)
        
        self.edit_button = QPushButton("Edit Color")
        self.edit_button.clicked.connect(self.on_edit_clicked)
        buttons_layout.addWidget(self.edit_button)
        
        self.remove_button = QPushButton("Remove Color")
        self.remove_button.clicked.connect(self.on_remove_clicked)
        buttons_layout.addWidget(self.remove_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Update button states
        self.update_button_states()
        # If rows exist and none selected yet, select the first row for convenience
        if self.colors_table.rowCount() > 0 and self.colors_table.currentRow() < 0:
            self.colors_table.selectRow(0)
    
    def load_monster_colors(self):
        """Load monster colors from config"""
        monster_colors = self.config_manager.get('monster_colors', [])
        
        # Clear table
        self.colors_table.setRowCount(0)
        
        # Add colors to table
        for i, color_dict in enumerate(monster_colors):
            try:
                # Create color spec
                color_spec = ColorSpec(
                    rgb=tuple(color_dict['rgb']),
                    tol_rgb=color_dict.get('tol_rgb', 8),
                    use_hsv=color_dict.get('use_hsv', True),
                    tol_h=color_dict.get('tol_h', 4),
                    tol_s=color_dict.get('tol_s', 30),
                    tol_v=color_dict.get('tol_v', 30)
                )
                
                # Add row
                self.colors_table.insertRow(i)
                
                # Color preview
                color_button = ColorButton(color_spec.rgb)
                color_button.setEnabled(False)
                self.colors_table.setCellWidget(i, 0, color_button)
                
                # RGB
                rgb_text = f"({color_spec.rgb[0]}, {color_spec.rgb[1]}, {color_spec.rgb[2]})"
                self.colors_table.setItem(i, 1, QTableWidgetItem(rgb_text))
                
                # RGB tolerance
                self.colors_table.setItem(i, 2, QTableWidgetItem(str(color_spec.tol_rgb)))
                
                # HSV
                hsv_text = "Yes" if color_spec.use_hsv else "No"
                self.colors_table.setItem(i, 3, QTableWidgetItem(hsv_text))
                
                # H tolerance
                self.colors_table.setItem(i, 4, QTableWidgetItem(str(color_spec.tol_h)))
                
                # S/V tolerance
                sv_text = f"{color_spec.tol_s}/{color_spec.tol_v}"
                self.colors_table.setItem(i, 5, QTableWidgetItem(sv_text))
            
            except Exception as e:
                logger.error(f"Error loading monster color: {e}")
        
        # Update button states
        self.update_button_states()
    
    def update_button_states(self):
        """Update button states based on selection"""
        has_selection = self.colors_table.currentRow() >= 0
        
        self.edit_button.setEnabled(has_selection)
        self.remove_button.setEnabled(has_selection)
    
    def on_add_clicked(self):
        """Handle add button click"""
        # Create default color spec
        color_spec = ColorSpec(
            rgb=(0, 255, 0),
            tol_rgb=35,
            use_hsv=True,
            tol_h=14,
            tol_s=70,
            tol_v=70
        )
        
        # Open dialog
        dialog = MonsterColorDialog(self, color_spec, self.config_manager)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get color spec from dialog
            new_color_spec = dialog.get_color_spec()
            
            # Add to config
            monster_colors = self.config_manager.get('monster_colors', [])
            monster_colors.append({
                'rgb': new_color_spec.rgb,
                'tol_rgb': new_color_spec.tol_rgb,
                'use_hsv': new_color_spec.use_hsv,
                'tol_h': new_color_spec.tol_h,
                'tol_s': new_color_spec.tol_s,
                'tol_v': new_color_spec.tol_v
            })
            
            self.config_manager.set('monster_colors', monster_colors)
            
            # Reload colors
            self.load_monster_colors()

    def on_add_from_screen_clicked(self):
        """Quick add a monster color by picking from the focused client screenshot."""
        picker = ZoomColorPickerDialog(self.config_manager, self)
        if picker.exec_() == QDialog.Accepted and picker.selected_color:
            # Start with defaults but use selected color
            color_spec = ColorSpec(
                rgb=picker.selected_color,
                tol_rgb=35,
                use_hsv=True,
                tol_h=14,
                tol_s=70,
                tol_v=70
            )
            # Let user tweak before saving
            dialog = MonsterColorDialog(self, color_spec, self.config_manager)
            if dialog.exec_() == QDialog.Accepted:
                new_color_spec = dialog.get_color_spec()
                monster_colors = self.config_manager.get('monster_colors', [])
                monster_colors.append({
                    'rgb': new_color_spec.rgb,
                    'tol_rgb': new_color_spec.tol_rgb,
                    'use_hsv': new_color_spec.use_hsv,
                    'tol_h': new_color_spec.tol_h,
                    'tol_s': new_color_spec.tol_s,
                    'tol_v': new_color_spec.tol_v
                })
                self.config_manager.set('monster_colors', monster_colors)
                self.load_monster_colors()
    
    def on_edit_clicked(self):
        """Handle edit button click"""
        row = self.colors_table.currentRow()
        
        if row < 0:
            return
        
        # Get color data
        monster_colors = self.config_manager.get('monster_colors', [])
        
        if row >= len(monster_colors):
            return
        
        color_dict = monster_colors[row]
        
        # Create color spec
        color_spec = ColorSpec(
            rgb=tuple(color_dict['rgb']),
            tol_rgb=color_dict.get('tol_rgb', 8),
            use_hsv=color_dict.get('use_hsv', True),
            tol_h=color_dict.get('tol_h', 4),
            tol_s=color_dict.get('tol_s', 30),
            tol_v=color_dict.get('tol_v', 30)
        )
        
        # Open dialog
        dialog = MonsterColorDialog(self, color_spec, self.config_manager)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get color spec from dialog
            new_color_spec = dialog.get_color_spec()
            
            # Update config
            monster_colors[row] = {
                'rgb': new_color_spec.rgb,
                'tol_rgb': new_color_spec.tol_rgb,
                'use_hsv': new_color_spec.use_hsv,
                'tol_h': new_color_spec.tol_h,
                'tol_s': new_color_spec.tol_s,
                'tol_v': new_color_spec.tol_v
            }
            
            self.config_manager.set('monster_colors', monster_colors)
            
            # Reload colors
            self.load_monster_colors()
    
    def on_remove_clicked(self):
        """Handle remove button click"""
        row = self.colors_table.currentRow()
        
        if row < 0:
            return
        
        # Confirm removal
        reply = QMessageBox.question(
            self,
            "Remove Monster Color",
            "Are you sure you want to remove this monster color?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Remove color
        monster_colors = self.config_manager.get('monster_colors', [])
        
        if row < len(monster_colors):
            del monster_colors[row]
            
            # Save to config
            self.config_manager.set('monster_colors', monster_colors)
            
            # Reload colors
            self.load_monster_colors()

class DetectionPanel(QWidget):
    """
    Panel for detection settings
    """
    
    def __init__(self, config_manager, bot_controller):
        """
        Initialize the detection panel
        
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
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # General settings tab
        general_tab = QWidget()
        tab_widget.addTab(general_tab, "General")
        
        general_layout = QVBoxLayout(general_tab)
        
        # Detection settings group
        detection_group = QGroupBox("Detection Settings")
        detection_layout = QVBoxLayout(detection_group)
        
        # Scan interval
        scan_layout = QHBoxLayout()
        
        scan_layout.addWidget(QLabel("Scan Interval:"))
        
        self.scan_interval_spin = QDoubleSpinBox()
        self.scan_interval_spin.setRange(0.05, 1.0)
        self.scan_interval_spin.setSingleStep(0.05)
        self.scan_interval_spin.setValue(self.config_manager.get('scan_interval', 0.2))
        self.scan_interval_spin.setSuffix(" s")
        self.scan_interval_spin.valueChanged.connect(self.on_scan_interval_changed)
        scan_layout.addWidget(self.scan_interval_spin)
        
        scan_layout.addStretch()
        
        detection_layout.addLayout(scan_layout)
        
        # Search step
        step_layout = QHBoxLayout()
        
        step_layout.addWidget(QLabel("Search Step:"))
        
        self.search_step_spin = QSpinBox()
        self.search_step_spin.setRange(1, 5)
        self.search_step_spin.setValue(self.config_manager.get('search_step', 2))
        self.search_step_spin.valueChanged.connect(self.on_search_step_changed)
        step_layout.addWidget(self.search_step_spin)
        
        step_layout.addStretch()
        
        detection_layout.addLayout(step_layout)
        
        # Detection checkboxes
        detect_layout = QHBoxLayout()
        
        self.detect_tiles_checkbox = QCheckBox("Detect Tiles")
        self.detect_tiles_checkbox.setChecked(self.config_manager.get('detect_tiles', True))
        self.detect_tiles_checkbox.toggled.connect(self.on_detect_tiles_toggled)
        detect_layout.addWidget(self.detect_tiles_checkbox)
        
        self.detect_monsters_checkbox = QCheckBox("Detect Monsters")
        self.detect_monsters_checkbox.setChecked(self.config_manager.get('detect_monsters', True))
        self.detect_monsters_checkbox.toggled.connect(self.on_detect_monsters_toggled)
        detect_layout.addWidget(self.detect_monsters_checkbox)
        
        detect_layout.addStretch()
        
        detection_layout.addLayout(detect_layout)
        
        # Precise mode
        precise_layout = QHBoxLayout()
        
        self.precise_mode_checkbox = QCheckBox("Use Precise Mode")
        self.precise_mode_checkbox.setChecked(self.config_manager.get('use_precise_mode', True))
        self.precise_mode_checkbox.toggled.connect(self.on_precise_mode_toggled)
        precise_layout.addWidget(self.precise_mode_checkbox)
        
        precise_layout.addStretch()
        
        detection_layout.addLayout(precise_layout)
        
        # Add detection group to general layout
        general_layout.addWidget(detection_group)
        
        # Tile settings group
        tile_group = QGroupBox("Tile Settings")
        tile_layout = QVBoxLayout(tile_group)
        
        # Tile min area
        tile_area_layout = QHBoxLayout()
        
        tile_area_layout.addWidget(QLabel("Minimum Area:"))
        
        self.tile_min_area_spin = QSpinBox()
        self.tile_min_area_spin.setRange(5, 100)
        self.tile_min_area_spin.setValue(self.config_manager.get('tile_min_area', 30))
        self.tile_min_area_spin.valueChanged.connect(self.on_tile_min_area_changed)
        tile_area_layout.addWidget(self.tile_min_area_spin)
        
        tile_area_layout.addStretch()
        
        tile_layout.addLayout(tile_area_layout)
        
        # Add tile group to general layout
        general_layout.addWidget(tile_group)
        
        # Monster settings group
        monster_group = QGroupBox("Monster Settings")
        monster_layout = QVBoxLayout(monster_group)
        
        # Monster min area
        monster_area_layout = QHBoxLayout()
        
        monster_area_layout.addWidget(QLabel("Minimum Area:"))
        
        self.monster_min_area_spin = QSpinBox()
        self.monster_min_area_spin.setRange(5, 100)
        self.monster_min_area_spin.setValue(self.config_manager.get('monster_min_area', 15))
        self.monster_min_area_spin.valueChanged.connect(self.on_monster_min_area_changed)
        monster_area_layout.addWidget(self.monster_min_area_spin)
        
        monster_area_layout.addStretch()
        
        monster_layout.addLayout(monster_area_layout)
        
        # Around tile radius
        radius_layout = QHBoxLayout()
        
        radius_layout.addWidget(QLabel("Around Tile Radius:"))
        
        self.around_tile_radius_spin = QSpinBox()
        self.around_tile_radius_spin.setRange(50, 300)
        self.around_tile_radius_spin.setValue(self.config_manager.get('around_tile_radius', 120))
        self.around_tile_radius_spin.valueChanged.connect(self.on_around_tile_radius_changed)
        radius_layout.addWidget(self.around_tile_radius_spin)
        
        radius_layout.addStretch()
        
        monster_layout.addLayout(radius_layout)
        
        # Monster scan step
        monster_step_layout = QHBoxLayout()
        
        monster_step_layout.addWidget(QLabel("Monster Scan Step:"))
        
        self.monster_scan_step_spin = QSpinBox()
        self.monster_scan_step_spin.setRange(1, 3)
        self.monster_scan_step_spin.setValue(self.config_manager.get('monster_scan_step', 1))
        self.monster_scan_step_spin.valueChanged.connect(self.on_monster_scan_step_changed)
        monster_step_layout.addWidget(self.monster_scan_step_spin)
        
        monster_step_layout.addStretch()
        
        monster_layout.addLayout(monster_step_layout)
        
        # Enable monster full fallback
        fallback_layout = QHBoxLayout()
        
        self.monster_fallback_checkbox = QCheckBox("Enable Monster Full Fallback")
        self.monster_fallback_checkbox.setChecked(self.config_manager.get('enable_monster_full_fallback', False))
        self.monster_fallback_checkbox.toggled.connect(self.on_monster_fallback_toggled)
        fallback_layout.addWidget(self.monster_fallback_checkbox)
        
        fallback_layout.addStretch()
        
        monster_layout.addLayout(fallback_layout)
        
        # Add monster group to general layout
        general_layout.addWidget(monster_group)

        # Low-confidence click settings
        lowconf_group = QGroupBox("Low-Confidence Click Mode")
        lowconf_group.setToolTip(
            "When detections are weak (few monsters or very small areas), click the largest-area target instead of the nearest."
        )
        lowconf_layout = QGridLayout(lowconf_group)

        # Enable toggle
        self.lowconf_enable_checkbox = QCheckBox("Enable low-confidence target selection")
        self.lowconf_enable_checkbox.setToolTip(
            "If enabled, the bot switches to clicking the biggest detected target when detections are uncertain."
        )
        self.lowconf_enable_checkbox.setChecked(self.config_manager.get('low_confidence_click_enabled', True))
        self.lowconf_enable_checkbox.toggled.connect(self.on_lowconf_enabled_toggled)
        lowconf_layout.addWidget(self.lowconf_enable_checkbox, 0, 0, 1, 3)

        # Area threshold
        lowconf_layout.addWidget(QLabel("Area threshold:"), 1, 0)
        self.lowconf_area_spin = QDoubleSpinBox()
        self.lowconf_area_spin.setToolTip(
            "If the largest detected target area is below this value (in pixels squared), low-confidence mode triggers."
        )
        self.lowconf_area_spin.setDecimals(1)
        self.lowconf_area_spin.setRange(0.0, 5000.0)
        self.lowconf_area_spin.setSingleStep(10.0)
        self.lowconf_area_spin.setValue(self.config_manager.get('low_confidence_area_threshold', 220.0))
        self.lowconf_area_spin.valueChanged.connect(self.on_lowconf_area_changed)
        lowconf_layout.addWidget(self.lowconf_area_spin, 1, 1)
        lowconf_layout.addWidget(QLabel("px^2"), 1, 2)

        # Minimum count
        lowconf_layout.addWidget(QLabel("Minimum count:"), 2, 0)
        self.lowconf_count_spin = QSpinBox()
        self.lowconf_count_spin.setToolTip(
            "If fewer than this number of monsters are detected, low-confidence mode triggers."
        )
        self.lowconf_count_spin.setRange(1, 20)
        self.lowconf_count_spin.setValue(self.config_manager.get('low_conf_min_count', 3))
        self.lowconf_count_spin.valueChanged.connect(self.on_lowconf_count_changed)
        lowconf_layout.addWidget(self.lowconf_count_spin, 2, 1)
        lowconf_layout.addWidget(QLabel("monsters"), 2, 2)

        general_layout.addWidget(lowconf_group)

        # Add stretch to push everything to the top
        general_layout.addStretch()
        
        # Colors tab
        colors_tab = QWidget()
        tab_widget.addTab(colors_tab, "Colors")
        
        colors_layout = QVBoxLayout(colors_tab)
        
        # Tile color group
        tile_color_group = QGroupBox("Tile Color")
        tile_color_layout = QVBoxLayout(tile_color_group)
        
        # Tile color editor
        self.tile_color_editor = ColorSpecEditor(self.config_manager, 'tile_color')
        tile_color_layout.addWidget(self.tile_color_editor)
        
        # Add tile color group to colors layout
        colors_layout.addWidget(tile_color_group)
        
        # Monster colors group
        monster_colors_group = QGroupBox("Monster Colors")
        monster_colors_layout = QVBoxLayout(monster_colors_group)
        
        # Monster colors editor
        self.monster_colors_editor = MonsterColorsEditor(self.config_manager)
        monster_colors_layout.addWidget(self.monster_colors_editor)
        
        # Add monster colors group to colors layout
        colors_layout.addWidget(monster_colors_group)
        
        # Add stretch to push everything to the top
        colors_layout.addStretch()
        
        # ROI tab
        roi_tab = QWidget()
        tab_widget.addTab(roi_tab, "ROI")
        
        roi_layout = QVBoxLayout(roi_tab)
        
        # ROI group
        roi_group = QGroupBox("Search Region of Interest")
        roi_group_layout = QVBoxLayout(roi_group)
        
        # ROI description
        roi_description = QLabel(
            "The search region of interest (ROI) defines the area of the screen where the bot will look for tiles and monsters. "
            "This can significantly improve performance by limiting the search area."
        )
        roi_description.setWordWrap(True)
        roi_group_layout.addWidget(roi_description)
        
        # ROI selector
        from .instance_panel import ROISelector
        self.roi_selector = ROISelector(self.config_manager)
        roi_group_layout.addWidget(self.roi_selector)
        
        # ROI buttons
        roi_buttons_layout = QHBoxLayout()
        
        self.save_roi_button = QPushButton("Save ROI")
        self.save_roi_button.clicked.connect(self.on_save_roi_clicked)
        roi_buttons_layout.addWidget(self.save_roi_button)
        
        self.clear_roi_button = QPushButton("Clear ROI")
        self.clear_roi_button.clicked.connect(self.on_clear_roi_clicked)
        roi_buttons_layout.addWidget(self.clear_roi_button)
        
        roi_group_layout.addLayout(roi_buttons_layout)
        
        roi_layout.addWidget(roi_group)
        
        # Load ROI if exists
        roi = self.config_manager.get_roi('search_roi')
        if roi:
            self.roi_selector.set_roi(roi)
        
        # Add stretch to push everything to the top
        roi_layout.addStretch()
    
    def on_scan_interval_changed(self, value):
        """Handle scan interval change"""
        logger.debug(f"Scan interval set to {value} seconds")
        self.config_manager.set('scan_interval', value)
    
    def on_search_step_changed(self, value):
        """Handle search step change"""
        logger.debug(f"Search step set to {value}")
        self.config_manager.set('search_step', value)
    
    def on_detect_tiles_toggled(self, checked):
        """Handle detect tiles toggle"""
        logger.debug(f"Detect tiles {'enabled' if checked else 'disabled'}")
        self.config_manager.set('detect_tiles', checked)
    
    def on_detect_monsters_toggled(self, checked):
        """Handle detect monsters toggle"""
        logger.debug(f"Detect monsters {'enabled' if checked else 'disabled'}")
        self.config_manager.set('detect_monsters', checked)
    
    def on_precise_mode_toggled(self, checked):
        """Handle precise mode toggle"""
        logger.debug(f"Precise mode {'enabled' if checked else 'disabled'}")
        self.config_manager.set('use_precise_mode', checked)
    
    def on_tile_min_area_changed(self, value):
        """Handle tile min area change"""
        logger.debug(f"Tile minimum area set to {value}")
        self.config_manager.set('tile_min_area', value)
    
    def on_monster_min_area_changed(self, value):
        """Handle monster min area change"""
        logger.debug(f"Monster minimum area set to {value}")
        self.config_manager.set('monster_min_area', value)
    
    def on_around_tile_radius_changed(self, value):
        """Handle around tile radius change"""
        logger.debug(f"Around tile radius set to {value}")
        self.config_manager.set('around_tile_radius', value)
    
    def on_monster_scan_step_changed(self, value):
        """Handle monster scan step change"""
        logger.debug(f"Monster scan step set to {value}")
        self.config_manager.set('monster_scan_step', value)
    
    def on_monster_fallback_toggled(self, checked):
        """Handle monster fallback toggle"""
        logger.debug(f"Monster full fallback {'enabled' if checked else 'disabled'}")
        self.config_manager.set('enable_monster_full_fallback', checked)

    def on_lowconf_enabled_toggled(self, checked):
        """Handle low-confidence mode toggle"""
        logger.debug(f"Low-confidence click mode {'enabled' if checked else 'disabled'}")
        self.config_manager.set('low_confidence_click_enabled', checked)

    def on_lowconf_area_changed(self, value: float):
        """Handle area threshold change"""
        logger.debug(f"Low-confidence area threshold set to {value}")
        self.config_manager.set('low_confidence_area_threshold', float(value))

    def on_lowconf_count_changed(self, value: int):
        """Handle minimum count change"""
        logger.debug(f"Low-confidence minimum count set to {value}")
        self.config_manager.set('low_conf_min_count', int(value))
    
    def on_save_roi_clicked(self):
        """Handle save ROI button click"""
        try:
            # Get ROI from selector
            roi = self.roi_selector.get_roi()
            
            # Save to config
            self.config_manager.set_roi('search_roi', roi)
            
            QMessageBox.information(
                self,
                "ROI Saved",
                f"Search ROI saved: Left={roi.left}, Top={roi.top}, Width={roi.width}, Height={roi.height}"
            )
        
        except Exception as e:
            logger.error(f"Error saving ROI: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving ROI: {e}"
            )
    
    def on_clear_roi_clicked(self):
        """Handle clear ROI button click"""
        # Confirm clear
        reply = QMessageBox.question(
            self,
            "Clear ROI",
            "Are you sure you want to clear the search ROI? This will make the bot search the entire screen.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Clear ROI in config
        self.config_manager.set('search_roi', None)
        
        # Reset ROI selector
        self.roi_selector.left_spin.setValue(0)
        self.roi_selector.top_spin.setValue(0)
        self.roi_selector.width_spin.setValue(100)
        self.roi_selector.height_spin.setValue(100)
        
        QMessageBox.information(
            self,
            "ROI Cleared",
            "Search ROI has been cleared. The bot will now search the entire screen."
        )