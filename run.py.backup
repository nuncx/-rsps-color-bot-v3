import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from rspsbot.gui.main_windows.monster_mode_window import MonsterModeWindow
from rspsbot.gui.main_windows.instance_mode_window import InstanceModeWindow

def main():
    """Entry point for the RSPS Color Bot v3"""
    app = QApplication(sys.argv)
    
    # Create mode selection window
    mode_window = QWidget()
    mode_window.setWindowTitle("RSPS Color Bot v3 - Mode Selection")
    mode_layout = QVBoxLayout()
    
    # Add title label
    title_label = QLabel("Select Bot Mode")
    title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
    mode_layout.addWidget(title_label)
    
    # Add mode buttons
    monster_mode_btn = QPushButton("Monster Mode")
    instance_mode_btn = QPushButton("Instance Mode")
    
    # Set button styles
    button_style = """
        QPushButton {
            padding: 15px;
            font-size: 16px;
            margin: 5px;
        }
    """
    monster_mode_btn.setStyleSheet(button_style)
    instance_mode_btn.setStyleSheet(button_style)
    
    # Add functionality to buttons
    def open_monster_mode():
        mode_window.close()
        monster_window = MonsterModeWindow(None)  # Pass config when available
        monster_window.show()
        sys.exit(app.exec_())
    
    def open_instance_mode():
        mode_window.close()
        instance_window = InstanceModeWindow(None)  # Pass config when available
        instance_window.show()
        sys.exit(app.exec_())
    
    monster_mode_btn.clicked.connect(open_monster_mode)
    instance_mode_btn.clicked.connect(open_instance_mode)
    
    mode_layout.addWidget(monster_mode_btn)
    mode_layout.addWidget(instance_mode_btn)
    
    mode_window.setLayout(mode_layout)
    mode_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()