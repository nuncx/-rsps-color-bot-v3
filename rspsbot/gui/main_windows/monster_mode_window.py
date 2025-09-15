"""
Main Window for Monster Mode of RSPS Color Bot v3
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from rspsbot.gui.panels.monster_panel import MonsterPanel
from rspsbot.gui.panels.combat_panel import CombatPanel
from rspsbot.gui.panels.control_panel import ControlPanel
from rspsbot.gui.panels.logs_panel import LogsPanel
from rspsbot.gui.panels.profiles_panel import ProfilesPanel
from rspsbot.gui.panels.stats_panel import StatsPanel
from rspsbot.gui.panels.teleport_panel import TeleportPanel
from rspsbot.gui.panels.potion_panel import PotionPanel

class MonsterModeWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("RSPS Color Bot v3 - Monster Mode")
        self.setGeometry(100, 100, 800, 600)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Add panels as tabs
        tab_widget.addTab(MonsterPanel(self.config), "Monster Settings")
        tab_widget.addTab(CombatPanel(self.config), "Combat Settings")
        tab_widget.addTab(ControlPanel(self.config), "Control Settings")
        tab_widget.addTab(PotionPanel(self.config), "Potion Settings")
        tab_widget.addTab(TeleportPanel(self.config), "Teleport Settings")
        tab_widget.addTab(ProfilesPanel(self.config), "Profiles")
        tab_widget.addTab(LogsPanel(self.config), "Logs")
        tab_widget.addTab(StatsPanel(self.config), "Statistics")
        
        self.setCentralWidget(tab_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # For testing purposes only
    class DummyConfig:
        def __init__(self):
            pass
            
    window = MonsterModeWindow(DummyConfig())
    window.show()
    sys.exit(app.exec_())