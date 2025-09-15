# RSPS Color Bot v3 Enhancement Implementation Plan

## 1. Profile Saving Enhancement

### Issues to Fix
- Currently, not all variables are being saved in profiles
- Missing variables include:
  - First aggro potion timer
  - Aggro visual check
  - Instance token delay
  - Instance only mode
  - Anti-ban settings

### Implementation Plan
1. Update `ConfigManager._get_default_config()` to include all missing variables
2. Ensure all GUI components properly update the config manager when values change
3. Verify that all settings are properly loaded when a profile is loaded

## 2. Bot Mode Splitting

### Current State
- The bot already has a mode selection window in run.py
- There are separate MonsterModeWindow and InstanceModeWindow classes
- The Instance Mode window still includes unnecessary panels

### Implementation Plan
1. Update InstanceModeWindow to only include necessary panels:
   - InstancePanel
   - CombatPanel (for HP bar detection)
   - ControlPanel (for basic controls)
   - ProfilesPanel
   - LogsPanel
   - StatsPanel
2. Remove unnecessary panels from InstanceModeWindow:
   - PotionPanel (integrate into InstancePanel)
   - TeleportPanel (integrate into InstancePanel)
3. Update the mode selection window styling for better UX

## 3. Multi-Monster Mode Implementation

### Current State
- MonsterPanel has placeholders for single/multi monster mode
- Combat styles settings are not fully implemented

### Implementation Plan
1. Complete the MonsterPanel implementation:
   - Add proper radio button behavior for single/multi monster mode
   - Implement tab visibility based on selected mode
2. Implement single monster tab:
   - Move existing monster detection settings from DetectionPanel
   - Add color picker with screenshot integration
   - Add ROI selection with screenshot integration
3. Implement multi-monster tabs (3 monsters):
   - Add color picker for each monster
   - Add combat style selection (MELEE/RANGED/MAGE) for each monster
4. Implement Combat Styles Settings:
   - Add Weapon ROI selection with screenshot picker
   - Add weapon color selection for each combat style
   - Implement proper config saving/loading

## 4. First Aggro Potion Timer

### Current State
- InstancePanel already has a first aggro timer implementation
- TimeSelector component supports various time formats
- InstanceOnlyDetector has logic for first aggro potion

### Implementation Plan
1. Update TimeSelector to properly support "minutes:seconds" format
2. Enhance InstancePanel to make first aggro timer more prominent
3. Update InstanceOnlyDetector to properly use the first aggro timer
4. Ensure the timer is properly saved in profiles

## 5. Tooltip Enhancement

### Current State
- TooltipHelper class exists but is not used consistently
- Many variables lack tooltips

### Implementation Plan
1. Create a comprehensive list of all variables that need tooltips
2. Update all panels to use TooltipHelper for consistent tooltip styling
3. Add detailed tooltips to all variables explaining their effects

## 6. Anti-Ban Logic Implementation

### Current State
- Basic anti-ban settings exist in ControlPanel
- No dedicated anti-ban manager class

### Implementation Plan
1. Create AntiBanManager class with sophisticated techniques:
   - Click timing randomization (±30% variation)
   - Human-like mouse movement patterns using control points
   - Random breaks and micro-movements
2. Add configuration options in ControlPanel
3. Integrate AntiBanManager with BotController

## 7. GUI Optimization

### Current State
- Some panels have unused variables
- Layout could be improved for better organization

### Implementation Plan
1. Review all panels for unused variables and remove them
2. Reorganize components for better layout
3. Ensure all elements fit properly in the interface
4. Test GUI appearance and usability

## 8. Screenshot Picker Integration

### Current State
- Screen picker components exist but are not used consistently
- Some color and ROI selections don't use screenshot picker

### Implementation Plan
1. Update all color selection components to use ZoomColorPickerDialog
2. Update all ROI selection components to use ZoomRoiPickerDialog
3. Add RGB sliders for detection sensitivity
4. Test screenshot picker functionality

## Implementation Order

1. Profile Saving Enhancement (ensure all variables are saved)
2. Bot Mode Splitting (clean up mode windows)
3. First Aggro Potion Timer (update TimeSelector and InstancePanel)
4. Anti-Ban Logic Implementation (create AntiBanManager)
5. Tooltip Enhancement (add tooltips to all variables)
6. Multi-Monster Mode Implementation (complete MonsterPanel)
7. Screenshot Picker Integration (ensure consistent usage)
8. GUI Optimization (final cleanup and testing)