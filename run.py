import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rspsbot.core.config import ConfigManager
from rspsbot.core.state import BotController
from rspsbot.gui.main_windows.monster_mode_window import MonsterModeWindow
from rspsbot.gui.main_windows.instance_mode_window import InstanceModeWindow
from rspsbot.gui.components.tooltip_helper import TooltipHelper

def main():
    """Entry point for the RSPS Color Bot v3"""
    app = QApplication(sys.argv)
    
    # Create config manager
    config_manager = ConfigManager()
    
    # Create mode selection window
    mode_window = QWidget()
    mode_window.setWindowTitle("RSPS Color Bot v3 - Mode Selection")
    mode_window.setGeometry(100, 100, 500, 400)
    mode_layout = QVBoxLayout()
    
    # Add title label
    title_label = QLabel("RSPS Color Bot v3")
    title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px; color: #2c3e50;")
    title_label.setAlignment(Qt.AlignCenter)
    mode_layout.addWidget(title_label)
    
    # Add subtitle
    subtitle_label = QLabel("Select Bot Mode")
    subtitle_label.setStyleSheet("font-size: 18px; margin: 10px; color: #34495e;")
    subtitle_label.setAlignment(Qt.AlignCenter)
    mode_layout.addWidget(subtitle_label)
    
    # Create tooltip helper
    tooltip_helper = TooltipHelper()
    
    # Mode options group
    mode_group = QGroupBox("Bot Modes")
    mode_group_layout = QVBoxLayout()
    
    # Instance Only Mode toggle
    instance_only_layout = QHBoxLayout()
    instance_only_checkbox = QCheckBox("Instance Only Mode")
    instance_only_checkbox.setChecked(config_manager.get('instance_only_mode', False))
    instance_only_checkbox.toggled.connect(lambda checked: config_manager.set('instance_only_mode', checked))
    
    # Add tooltip
    tooltip_helper.add_tooltip(
        instance_only_checkbox,
        "Instance Only Mode",
        "Simplified mode that focuses only on aggro potion and instance teleport mechanics. Skips tile and monster detection."
    )
    
    instance_only_layout.addWidget(instance_only_checkbox)
    instance_only_layout.addStretch()
    mode_group_layout.addLayout(instance_only_layout)
    
    # Add mode buttons
    monster_mode_btn = QPushButton("Monster Mode")
    instance_mode_btn = QPushButton("Instance Mode")
    
    # Set button styles
    button_style = """
        QPushButton {
            padding: 15px;
            font-size: 16px;
            margin: 10px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1c6ea4;
        }
    """
    monster_mode_btn.setStyleSheet(button_style)
    instance_mode_btn.setStyleSheet(button_style)
    
    # Add tooltips
    tooltip_helper.add_tooltip(
        monster_mode_btn,
        "Monster Mode",
        "Full bot mode with monster detection, combat, and all features"
    )
    
    tooltip_helper.add_tooltip(
        instance_mode_btn,
        "Instance Mode",
        "Instance-focused mode with aggro potion and teleport management"
    )
    
    mode_group_layout.addWidget(monster_mode_btn)
    mode_group_layout.addWidget(instance_mode_btn)
    
    mode_group.setLayout(mode_group_layout)
    mode_layout.addWidget(mode_group)
    
    # Add functionality to buttons
    def open_monster_mode():
        mode_window.close()
        # Create a dummy bot controller for GUI testing
        class DummyBotController:
            def __init__(self):
                self.teleport_manager = None
                self.potion_manager = None
                self.stats_tracker = None
                
        bot_controller = DummyBotController()
        monster_window = MonsterModeWindow(config_manager, bot_controller)
        monster_window.show()
        sys.exit(app.exec_())
    
    def open_instance_mode():
        mode_window.close()
        # Create a dummy bot controller for GUI testing
        class DummyBotController:
            def __init__(self):
                self.teleport_manager = None
                self.potion_manager = None
                self.stats_tracker = None
                
        bot_controller = DummyBotController()
        instance_window = InstanceModeWindow(config_manager, bot_controller)
        instance_window.show()
        sys.exit(app.exec_())
    
    monster_mode_btn.clicked.connect(open_monster_mode)
    instance_mode_btn.clicked.connect(open_instance_mode)
    
    # Version info
    version_label = QLabel("Version 3.0")
    version_label.setStyleSheet("color: #7f8c8d; margin-top: 20px;")
    version_label.setAlignment(Qt.AlignCenter)
    mode_layout.addWidget(version_label)
    
    mode_window.setLayout(mode_layout)
    mode_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()