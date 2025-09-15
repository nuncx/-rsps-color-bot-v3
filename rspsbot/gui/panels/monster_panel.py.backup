"""
Monster Panel for RSPS Color Bot v3
Handles monster detection mode configuration
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QCheckBox, QTabWidget, QGroupBox,
                            QSpinBox, QDoubleSpinBox, QComboBox, QScrollArea)
from PyQt5.QtCore import Qt

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Importing required components
from rspsbot.gui.components.time_selector import TimeSelector
from rspsbot.gui.components.tooltip_helper import TooltipHelper
from rspsbot.gui.components.advanced_roi_selector import AdvancedROISelector
from rspsbot.gui.components.enhanced_color_picker import EnhancedColorPicker

class MonsterPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.tooltip_helper = TooltipHelper()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Mode selection
        mode_group = QGroupBox("Monster Mode")
        mode_layout = QHBoxLayout()
        
        self.single_mode_radio = QCheckBox("Single Monster Mode")
        self.multi_mode_radio = QCheckBox("Multi Monster Mode")
        
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
        
        # Add single monster configuration elements here
        # (Will be populated with existing elements from detection panel)
        
        self.single_monster_tab.setLayout(self.single_monster_layout)
        self.monster_tabs.addTab(self.single_monster_tab, "Single Monster")
        
        # Multi monster tabs
        self.multi_monster_tab1 = QWidget()
        self.multi_monster_layout1 = QVBoxLayout()
        self.multi_monster_tab2 = QWidget()
        self.multi_monster_layout2 = QVBoxLayout()
        self.multi_monster_tab3 = QWidget()
        self.multi_monster_layout3 = QVBoxLayout()
        
        # Add multi monster configuration elements here
        
        self.multi_monster_tab1.setLayout(self.multi_monster_layout1)
        self.multi_monster_tab2.setLayout(self.multi_monster_layout2)
        self.multi_monster_tab3.setLayout(self.multi_monster_layout3)
        
        self.monster_tabs.addTab(self.multi_monster_tab1, "Monster 1")
        self.monster_tabs.addTab(self.multi_monster_tab2, "Monster 2")
        self.monster_tabs.addTab(self.multi_monster_tab3, "Monster 3")
        
        layout.addWidget(self.monster_tabs)
        
        # Combat styles settings
        styles_group = QGroupBox("Combat Styles Settings")
        styles_layout = QVBoxLayout()
        
        self.styles_tabs = QTabWidget()
        
        # Weapon ROI tab
        self.weapon_roi_tab = QWidget()
        weapon_roi_layout = QVBoxLayout()
        
        # Add weapon ROI configuration elements here
        
        self.weapon_roi_tab.setLayout(weapon_roi_layout)
        self.styles_tabs.addTab(self.weapon_roi_tab, "Weapon ROI")
        
        # Colors tab
        self.colors_tab = QWidget()
        colors_layout = QVBoxLayout()
        
        # Add weapon color configuration elements here
        
        self.colors_tab.setLayout(colors_layout)
        self.styles_tabs.addTab(self.colors_tab, "Weapon Colors")
        
        styles_layout.addWidget(self.styles_tabs)
        styles_group.setLayout(styles_layout)
        layout.addWidget(styles_group)
        
        self.setLayout(layout)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # For testing purposes only
    class DummyConfig:
        def __init__(self):
            pass
            
    panel = MonsterPanel(DummyConfig())
    panel.show()
    sys.exit(app.exec_())