"""
Monster Panel for RSPS Color Bot v3
Handles monster detection mode configuration
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QCheckBox, QTabWidget, QGroupBox,
                            QSpinBox, QDoubleSpinBox, QComboBox, QScrollArea,
                            QRadioButton, QButtonGroup, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Importing required components
from rspsbot.gui.components.time_selector import TimeSelector
from rspsbot.gui.components.tooltip_helper import TooltipHelper
from rspsbot.gui.components.advanced_roi_selector import AdvancedROISelector
from rspsbot.gui.components.enhanced_color_picker import EnhancedColorPicker
from rspsbot.core.config import ColorSpec

class MonsterConfigTab(QWidget):
    """Widget for configuring a single monster"""
    
    def __init__(self, config_manager, monster_index, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.monster_index = monster_index  # 1, 2, or 3
        self.tooltip_helper = TooltipHelper()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Monster Color
        color_group = QGroupBox("Monster Color")
        color_layout = QVBoxLayout()
        
        self.color_picker = EnhancedColorPicker("Select monster color:")
        
        # Load color from config if available
        color_key = f"monster{self.monster_index}_color"
        color_spec = self.config_manager.get_color_spec(color_key)
        if color_spec:
            self.color_picker.color = color_spec.rgb
            self.color_picker.update_color_preview()
        
        self.tooltip_helper.add_tooltip(
            self.color_picker,
            "Monster Color",
            "The color used to detect this monster. Use the pipette tool to pick from the screen."
        )
        
        color_layout.addWidget(self.color_picker)
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Combat Style
        style_group = QGroupBox("Combat Style")
        style_layout = QVBoxLayout()
        
        self.style_combo = QComboBox()
        self.style_combo.addItems(["MELEE", "RANGED", "MAGE"])
        
        # Load style from config if available
        style_key = f"monster{self.monster_index}_combat_style"
        style = self.config_manager.get(style_key, "MELEE")
        self.style_combo.setCurrentText(style)
        
        self.tooltip_helper.add_tooltip(
            self.style_combo,
            "Combat Style",
            "The combat style to use against this monster. The bot will switch to the appropriate weapon."
        )
        
        style_layout.addWidget(QLabel("Select combat style:"))
        style_layout.addWidget(self.style_combo)
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        # Save button
        save_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Monster Settings")
        self.save_button.clicked.connect(self.save_settings)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
    def save_settings(self):
        """Save monster settings to config"""
        # Save color
        color_key = f"monster{self.monster_index}_color"
        color_spec = ColorSpec(
            rgb=self.color_picker.color,
            tol_rgb=35,  # Default tolerance
            use_hsv=True,
            tol_h=14,
            tol_s=70,
            tol_v=70
        )
        self.config_manager.set_color_spec(color_key, color_spec)
        
        # Save combat style
        style_key = f"monster{self.monster_index}_combat_style"
        self.config_manager.set(style_key, self.style_combo.currentText())
        
        print(f"Saved settings for Monster {self.monster_index}")

class WeaponConfigTab(QWidget):
    """Widget for configuring weapon detection"""
    
    def __init__(self, config_manager, weapon_type, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.weapon_type = weapon_type  # "MELEE", "RANGED", or "MAGE"
        self.tooltip_helper = TooltipHelper()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Weapon Color
        color_group = QGroupBox(f"{self.weapon_type} Weapon Color")
        color_layout = QVBoxLayout()
        
        self.color_picker = EnhancedColorPicker("Select weapon color:")
        
        # Load color from config if available
        color_key = f"{self.weapon_type.lower()}_weapon_color"
        color_spec = self.config_manager.get_color_spec(color_key)
        if color_spec:
            self.color_picker.color = color_spec.rgb
            self.color_picker.update_color_preview()
        
        self.tooltip_helper.add_tooltip(
            self.color_picker,
            f"{self.weapon_type} Weapon Color",
            f"The color used to detect {self.weapon_type.lower()} weapons. Use the pipette tool to pick from the screen."
        )
        
        color_layout.addWidget(self.color_picker)
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Save button
        save_layout = QHBoxLayout()
        self.save_button = QPushButton(f"Save {self.weapon_type} Weapon Settings")
        self.save_button.clicked.connect(self.save_settings)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
    def save_settings(self):
        """Save weapon settings to config"""
        # Save color
        color_key = f"{self.weapon_type.lower()}_weapon_color"
        color_spec = ColorSpec(
            rgb=self.color_picker.color,
            tol_rgb=35,  # Default tolerance
            use_hsv=True,
            tol_h=14,
            tol_s=70,
            tol_v=70
        )
        self.config_manager.set_color_spec(color_key, color_spec)
        
        print(f"Saved settings for {self.weapon_type} weapon")

class MonsterPanel(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.tooltip_helper = TooltipHelper()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Mode selection
        mode_group = QGroupBox("Monster Mode")
        mode_layout = QHBoxLayout()
        
        self.mode_button_group = QButtonGroup(self)
        self.single_mode_radio = QRadioButton("Single Monster Mode")
        self.multi_mode_radio = QRadioButton("Multi Monster Mode")
        
        self.mode_button_group.addButton(self.single_mode_radio, 1)
        self.mode_button_group.addButton(self.multi_mode_radio, 2)
        
        # Load mode from config
        monster_mode = self.config_manager.get("monster_mode", "single")
        if monster_mode == "single":
            self.single_mode_radio.setChecked(True)
        else:
            self.multi_mode_radio.setChecked(True)
        
        # Connect mode change signal
        self.mode_button_group.buttonClicked.connect(self.on_mode_changed)
        
        # Add tooltips
        self.tooltip_helper.add_tooltip(
            self.single_mode_radio,
            "Single Monster Mode",
            "Detect and interact with one type of monster at a time"
        )
        
        self.tooltip_helper.add_tooltip(
            self.multi_mode_radio,
            "Multi Monster Mode",
            "Detect and interact with multiple types of monsters"
        )
        
        mode_layout.addWidget(self.single_mode_radio)
        mode_layout.addWidget(self.multi_mode_radio)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Monster configuration tabs
        self.monster_tabs = QTabWidget()
        
        # Single monster tab
        self.single_monster_tab = QWidget()
        self.single_monster_layout = QVBoxLayout()
        
        # Single monster color
        single_color_group = QGroupBox("Monster Color")
        single_color_layout = QVBoxLayout()
        
        self.single_color_picker = EnhancedColorPicker("Select monster color:")
        
        # Load color from config if available
        color_spec = self.config_manager.get_color_spec("monster1_color")
        if color_spec:
            self.single_color_picker.color = color_spec.rgb
            self.single_color_picker.update_color_preview()
        
        self.tooltip_helper.add_tooltip(
            self.single_color_picker,
            "Monster Color",
            "The color used to detect monsters. Use the pipette tool to pick from the screen."
        )
        
        single_color_layout.addWidget(self.single_color_picker)
        single_color_group.setLayout(single_color_layout)
        self.single_monster_layout.addWidget(single_color_group)
        
        # Single monster ROI
        single_roi_group = QGroupBox("Monster ROI")
        single_roi_layout = QVBoxLayout()
        
        self.single_roi_selector = AdvancedROISelector("Select monster detection region:")
        
        # Load ROI from config if available
        roi = self.config_manager.get_roi("search_roi")
        if roi:
            self.single_roi_selector.set_roi(roi)
        
        self.tooltip_helper.add_tooltip(
            self.single_roi_selector,
            "Monster ROI",
            "The region of interest where monsters will be detected. Use the Select ROI button to pick from the screen."
        )
        
        single_roi_layout.addWidget(self.single_roi_selector)
        single_roi_group.setLayout(single_roi_layout)
        self.single_monster_layout.addWidget(single_roi_group)
        
        # Save button for single monster
        single_save_layout = QHBoxLayout()
        self.single_save_button = QPushButton("Save Single Monster Settings")
        self.single_save_button.clicked.connect(self.save_single_monster_settings)
        single_save_layout.addWidget(self.single_save_button)
        self.single_monster_layout.addLayout(single_save_layout)
        
        # Add stretch to push everything to the top
        self.single_monster_layout.addStretch()
        
        self.single_monster_tab.setLayout(self.single_monster_layout)
        self.monster_tabs.addTab(self.single_monster_tab, "Single Monster")
        
        # Multi monster tabs
        self.multi_monster_tab1 = MonsterConfigTab(self.config_manager, 1)
        self.multi_monster_tab2 = MonsterConfigTab(self.config_manager, 2)
        self.multi_monster_tab3 = MonsterConfigTab(self.config_manager, 3)
        
        self.monster_tabs.addTab(self.multi_monster_tab1, "Monster 1")
        self.monster_tabs.addTab(self.multi_monster_tab2, "Monster 2")
        self.monster_tabs.addTab(self.multi_monster_tab3, "Monster 3")
        
        layout.addWidget(self.monster_tabs)
        
        # Combat styles settings
        styles_group = QGroupBox("Combat Styles Settings")
        styles_layout = QVBoxLayout()
        
        # Weapon ROI
        weapon_roi_group = QGroupBox("Weapon ROI")
        weapon_roi_layout = QVBoxLayout()
        
        self.weapon_roi_selector = AdvancedROISelector("Select weapon detection region:")
        
        # Load ROI from config if available
        roi = self.config_manager.get_roi("weapon_roi")
        if roi:
            self.weapon_roi_selector.set_roi(roi)
        
        self.tooltip_helper.add_tooltip(
            self.weapon_roi_selector,
            "Weapon ROI",
            "The region of interest where weapons will be detected. Use the Select ROI button to pick from the screen."
        )
        
        weapon_roi_layout.addWidget(self.weapon_roi_selector)
        
        # Save weapon ROI button
        weapon_roi_save_layout = QHBoxLayout()
        self.weapon_roi_save_button = QPushButton("Save Weapon ROI")
        self.weapon_roi_save_button.clicked.connect(self.save_weapon_roi)
        weapon_roi_save_layout.addWidget(self.weapon_roi_save_button)
        weapon_roi_layout.addLayout(weapon_roi_save_layout)
        
        weapon_roi_group.setLayout(weapon_roi_layout)
        styles_layout.addWidget(weapon_roi_group)
        
        # Weapon colors tabs
        self.styles_tabs = QTabWidget()
        
        # Create weapon tabs
        self.melee_tab = WeaponConfigTab(self.config_manager, "MELEE")
        self.ranged_tab = WeaponConfigTab(self.config_manager, "RANGED")
        self.mage_tab = WeaponConfigTab(self.config_manager, "MAGE")
        
        self.styles_tabs.addTab(self.melee_tab, "Melee Weapon")
        self.styles_tabs.addTab(self.ranged_tab, "Ranged Weapon")
        self.styles_tabs.addTab(self.mage_tab, "Mage Weapon")
        
        styles_layout.addWidget(self.styles_tabs)
        styles_group.setLayout(styles_layout)
        layout.addWidget(styles_group)
        
        # Update UI based on current mode
        self.update_ui_for_mode()
        
        self.setLayout(layout)
    
    def on_mode_changed(self, button):
        """Handle mode change"""
        if button == self.single_mode_radio:
            self.config_manager.set("monster_mode", "single")
        else:
            self.config_manager.set("monster_mode", "multi")
        
        self.update_ui_for_mode()
    
    def update_ui_for_mode(self):
        """Update UI based on selected mode"""
        monster_mode = self.config_manager.get("monster_mode", "single")
        
        # Enable/disable tabs based on mode
        if monster_mode == "single":
            # In single mode, only show the single monster tab
            self.monster_tabs.setTabEnabled(0, True)
            self.monster_tabs.setTabEnabled(1, False)
            self.monster_tabs.setTabEnabled(2, False)
            self.monster_tabs.setTabEnabled(3, False)
            self.monster_tabs.setCurrentIndex(0)
            
            # Hide combat styles settings
            self.styles_tabs.setVisible(False)
        else:
            # In multi mode, show all monster tabs
            self.monster_tabs.setTabEnabled(0, False)
            self.monster_tabs.setTabEnabled(1, True)
            self.monster_tabs.setTabEnabled(2, True)
            self.monster_tabs.setTabEnabled(3, True)
            self.monster_tabs.setCurrentIndex(1)
            
            # Show combat styles settings
            self.styles_tabs.setVisible(True)
    
    def save_single_monster_settings(self):
        """Save single monster settings to config"""
        # Save color
        color_spec = ColorSpec(
            rgb=self.single_color_picker.color,
            tol_rgb=35,  # Default tolerance
            use_hsv=True,
            tol_h=14,
            tol_s=70,
            tol_v=70
        )
        self.config_manager.set_color_spec("monster1_color", color_spec)
        
        # Save ROI
        roi = self.single_roi_selector.get_roi()
        self.config_manager.set_roi("search_roi", roi)
        
        print("Saved single monster settings")
    
    def save_weapon_roi(self):
        """Save weapon ROI to config"""
        roi = self.weapon_roi_selector.get_roi()
        self.config_manager.set_roi("weapon_roi", roi)
        
        print("Saved weapon ROI")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # For testing purposes only
    class DummyConfig:
        def __init__(self):
            self._config = {}
            
        def get(self, key, default=None):
            return self._config.get(key, default)
            
        def set(self, key, value):
            self._config[key] = value
            print(f"Set {key} to {value}")
            
        def get_color_spec(self, key):
            return None
            
        def set_color_spec(self, key, value):
            print(f"Set color spec {key}")
            
        def get_roi(self, key):
            return None
            
        def set_roi(self, key, value):
            print(f"Set ROI {key}")
            
    panel = MonsterPanel(DummyConfig())
    panel.show()
    sys.exit(app.exec_())