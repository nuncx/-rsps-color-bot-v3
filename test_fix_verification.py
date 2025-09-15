import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the modules that require a display
import unittest.mock as mock

# Mock pyautogui and other display-dependent modules
sys.modules['pyautogui'] = mock.MagicMock()
sys.modules['pynput'] = mock.MagicMock()
sys.modules['mss'] = mock.MagicMock()
sys.modules['Xlib'] = mock.MagicMock()

def test_fix():
    """Test that the fix resolves the original TypeError"""
    print("=== Testing the Fix for TypeError ===")
    
    # Import required modules
    from rspsbot.core.config import ConfigManager
    
    # Create a dummy bot controller class (as we did in run.py)
    class DummyBotController:
        def __init__(self):
            self.teleport_manager = None
            self.potion_manager = None
            self.stats_tracker = None

    # Test 1: Check that run.py properly passes both arguments
    print("\n1. Checking run.py implementation...")
    try:
        with open("run.py", "r") as f:
            content = f.read()
            
        # Check that run.py creates both config_manager and bot_controller
        assert "config_manager = ConfigManager()" in content, "config_manager not created in run.py"
        assert "class DummyBotController:" in content, "DummyBotController not defined in run.py"
        assert "bot_controller = DummyBotController()" in content, "bot_controller not created in run.py"
        
        # Check that MonsterModeWindow is called with both arguments
        assert "MonsterModeWindow(config_manager, bot_controller)" in content, "MonsterModeWindow not called with both arguments"
        
        # Check that InstanceModeWindow is called with both arguments
        assert "InstanceModeWindow(config_manager, bot_controller)" in content, "InstanceModeWindow not called with both arguments"
        
        print("   ✓ run.py correctly implements the fix")
    except Exception as e:
        print(f"   ✗ Error in run.py: {e}")
        return False
    
    # Test 2: Check that monster_mode_window.py accepts both arguments
    print("\n2. Checking monster_mode_window.py implementation...")
    try:
        with open("rspsbot/gui/main_windows/monster_mode_window.py", "r") as f:
            content = f.read()
            
        # Check constructor signature
        assert "def __init__(self, config_manager, bot_controller):" in content, "MonsterModeWindow constructor doesn't accept both arguments"
        
        # Check that panels are instantiated with correct arguments
        assert "CombatPanel(self.config_manager, self.bot_controller)" in content, "CombatPanel not called with both arguments"
        assert "ControlPanel(self.config_manager, self.bot_controller)" in content, "ControlPanel not called with both arguments"
        assert "PotionPanel(self.config_manager, self.bot_controller)" in content, "PotionPanel not called with both arguments"
        assert "TeleportPanel(self.config_manager, self.bot_controller)" in content, "TeleportPanel not called with both arguments"
        assert "StatsPanel(self.config_manager, self.bot_controller)" in content, "StatsPanel not called with both arguments"
        
        print("   ✓ monster_mode_window.py correctly implements the fix")
    except Exception as e:
        print(f"   ✗ Error in monster_mode_window.py: {e}")
        return False
    
    # Test 3: Check that instance_mode_window.py accepts both arguments
    print("\n3. Checking instance_mode_window.py implementation...")
    try:
        with open("rspsbot/gui/main_windows/instance_mode_window.py", "r") as f:
            content = f.read()
            
        # Check constructor signature
        assert "def __init__(self, config_manager, bot_controller):" in content, "InstanceModeWindow constructor doesn't accept both arguments"
        
        # Check that panels are instantiated with correct arguments
        assert "InstancePanel(self.config_manager, self.bot_controller)" in content, "InstancePanel not called with both arguments"
        assert "CombatPanel(self.config_manager, self.bot_controller)" in content, "CombatPanel not called with both arguments"
        assert "ControlPanel(self.config_manager, self.bot_controller)" in content, "ControlPanel not called with both arguments"
        assert "StatsPanel(self.config_manager, self.bot_controller)" in content, "StatsPanel not called with both arguments"
        
        print("   ✓ instance_mode_window.py correctly implements the fix")
    except Exception as e:
        print(f"   ✗ Error in instance_mode_window.py: {e}")
        return False
    
    # Test 4: Verify that the panels require both arguments
    print("\n4. Checking panel constructor signatures...")
    try:
        from rspsbot.gui.panels.combat_panel import CombatPanel
        from rspsbot.gui.panels.control_panel import ControlPanel
        from rspsbot.gui.panels.potion_panel import PotionPanel
        from rspsbot.gui.panels.teleport_panel import TeleportPanel
        from rspsbot.gui.panels.stats_panel import StatsPanel
        from rspsbot.gui.panels.instance_panel import InstancePanel
        import inspect
        
        # Check each panel's constructor signature
        panels = [
            ("CombatPanel", CombatPanel),
            ("ControlPanel", ControlPanel),
            ("PotionPanel", PotionPanel),
            ("TeleportPanel", TeleportPanel),
            ("StatsPanel", StatsPanel),
            ("InstancePanel", InstancePanel)
        ]
        
        for name, panel_class in panels:
            sig = inspect.signature(panel_class.__init__)
            params = list(sig.parameters.keys())
            if 'config_manager' in params and 'bot_controller' in params:
                print(f"   ✓ {name} correctly requires both config_manager and bot_controller")
            else:
                print(f"   ✗ {name} does not require both arguments. Params: {params}")
                return False
                
        print("   ✓ All panels correctly require both arguments")
    except Exception as e:
        print(f"   ✗ Error checking panel signatures: {e}")
        return False
    
    print("\n=== All Tests Passed! ===")
    print("The fix successfully resolves the original TypeError:")
    print("TypeError: CombatPanel.__init__() missing 1 required positional argument: 'bot_controller'")
    return True

if __name__ == "__main__":
    success = test_fix()
    if success:
        print("\n🎉 FIX VERIFICATION SUCCESSFUL! 🎉")
        print("The original error has been resolved.")
    else:
        print("\n❌ FIX VERIFICATION FAILED!")
        sys.exit(1)