# RSPS Color Bot v3 Comprehensive Improvements

## 1. Profile Saving Enhancement
- [ ] Identify all variables across all panels
- [ ] Ensure ConfigManager saves all variables
- [ ] Test profile saving and loading with all settings

## 2. Bot Mode Splitting
- [ ] Update run.py to provide mode selection GUI
- [ ] Create separate MonsterModeWindow and InstanceModeWindow
- [ ] Ensure proper initialization of both modes
- [ ] Test both modes independently

## 3. Instance Mode Optimization
- [ ] Ensure Instance Mode uses the correct formula from the original implementation
- [ ] Remove unnecessary components from Instance Mode
- [ ] Test Instance Mode functionality

## 4. Multi-Monster Mode Implementation
- [ ] Add single/multi monster mode selection
- [ ] Create UI for configuring up to 3 monsters
- [ ] Implement combat style selection per monster (MELEE/RANGED/MAGE)
- [ ] Add weapon detection ROI selection
- [ ] Add weapon color selection with screenshot picker
- [ ] Implement weapon switching logic

## 5. First Aggro Potion Timer
- [ ] Add separate timer for first aggro potion
- [ ] Update Instance Panel UI to include first aggro timer
- [ ] Implement timer format "minutes:seconds" in TimeSelector component
- [ ] Update aggro potion logic to use first timer initially

## 6. Tooltip Enhancement
- [ ] Create TooltipHelper class for consistent tooltip styling
- [ ] Add comprehensive tooltips to all variables
- [ ] Ensure tooltips explain the effect of each variable

## 7. GUI Optimization
- [ ] Remove unused variables from UI
- [ ] Organize components for better layout
- [ ] Ensure all panels fit properly
- [ ] Test GUI appearance and usability

## 8. Anti-Ban Logic Implementation
- [ ] Create AntiBanManager class
- [ ] Implement various anti-ban techniques
- [ ] Add configuration options for anti-ban settings
- [ ] Integrate anti-ban logic with bot controller

## 9. Screenshot Picker Integration
- [ ] Ensure all color and ROI selections use screenshot picker
- [ ] Add RGB sliders for detection sensitivity
- [ ] Test screenshot picker functionality