"""
Configuration management for RSPS Color Bot v3
"""
import os
import json
import logging
from typing import Any, Dict, Optional, List, Union
from dataclasses import dataclass, field, asdict

# Get module logger
logger = logging.getLogger('rspsbot.core.config')

@dataclass
class ColorSpec:
    """
    Color specification with tolerance settings
    
    Attributes:
        rgb: RGB color tuple (0-255 for each channel)
        tol_rgb: Tolerance for RGB color matching (0-50 recommended)
        use_hsv: Whether to use HSV color space for detection
        tol_h: Hue tolerance for HSV matching (0-20 recommended)
        tol_s: Saturation tolerance for HSV matching (0-100)
        tol_v: Value tolerance for HSV matching (0-100)
    """
    rgb: tuple[int, int, int]
    tol_rgb: int = 8
    use_hsv: bool = True
    tol_h: int = 4
    tol_s: int = 30
    tol_v: int = 30
    
    def __post_init__(self):
        """Validate color specification parameters"""
        # Validate RGB tuple format
        if not isinstance(self.rgb, tuple):
            raise TypeError("RGB must be a tuple")
        
        if len(self.rgb) != 3:
            raise TypeError(f"RGB tuple must have exactly 3 elements, got {len(self.rgb)}")
        
        # Validate RGB values
        if not all(isinstance(c, int) for c in self.rgb):
            raise TypeError("RGB values must be integers")
            
        if not all(0 <= c <= 255 for c in self.rgb):
            raise ValueError(f"RGB values must be between 0 and 255, got {self.rgb}")
        
        # Validate tolerance values with warnings for extreme values
        if not 0 <= self.tol_rgb <= 50:
            logger.warning(f"tol_rgb value {self.tol_rgb} is outside recommended range 0-50")
        if not 0 <= self.tol_h <= 20:
            logger.warning(f"tol_h value {self.tol_h} is outside recommended range 0-20")
        if not 0 <= self.tol_s <= 100:
            logger.warning(f"tol_s value {self.tol_s} is outside recommended range 0-100")
        if not 0 <= self.tol_v <= 100:
            logger.warning(f"tol_v value {self.tol_v} is outside recommended range 0-100")

@dataclass
class ROI:
    """
    Region of interest on the screen
    
    Attributes:
        left: Left coordinate of the ROI
        top: Top coordinate of the ROI
        width: Width of the ROI in pixels
        height: Height of the ROI in pixels
    """
    left: int
    top: int
    width: int
    height: int
    
    def __post_init__(self):
        """Validate ROI parameters"""
        if self.width <= 0:
            raise ValueError(f"ROI width must be positive, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"ROI height must be positive, got {self.height}")
    
    def to_dict(self) -> Dict[str, int]:
        """Convert ROI to dictionary format"""
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'ROI':
        """Create ROI from dictionary"""
        return cls(
            left=data["left"],
            top=data["top"],
            width=data["width"],
            height=data["height"]
        )

@dataclass
class Coordinate:
    """
    XY coordinate on the screen
    
    Attributes:
        x: X coordinate
        y: Y coordinate
        name: Optional name for the coordinate
    """
    x: int
    y: int
    name: str = ""
    
    def __post_init__(self):
        """Validate coordinate parameters"""
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise TypeError("Coordinates must be integers")
        if self.x < 0 or self.y < 0:
            logger.warning(f"Negative coordinate values: ({self.x}, {self.y})")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert coordinate to dictionary format"""
        return {
            "x": self.x,
            "y": self.y,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Coordinate':
        """Create coordinate from dictionary"""
        return cls(
            x=data["x"],
            y=data["y"],
            name=data.get("name", "")
        )

class ConfigManager:
    """
    Manages configuration settings for the bot
    
    This class handles loading, saving, and accessing configuration settings.
    It also provides validation and default values for settings.
    """
    
    def __init__(self, config_dir: str = "profiles"):
        """
        Initialize the configuration manager
        
        Args:
            config_dir: Directory for configuration profiles
        """
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
        
        # Default configuration
        self._config = self._get_default_config()
        
        # Current profile name
        self.current_profile = None
        
        logger.info("Configuration manager initialized")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            # Window settings
            "window_title": "Velador - Donikk",
            
            # Detection settings
            "scan_interval": 0.2,
            "search_step": 2,
            "detect_tiles": True,
            "detect_monsters": True,
            "tile_min_area": 20,
            "monster_min_area": 10,
            "around_tile_radius": 120,
            "use_precise_mode": True,
            "monster_scan_step": 1,
            "enable_monster_full_fallback": False,
            "adaptive_search": True,
            "adaptive_monster_detection": True,
            "monster_sat_min": 40,
            "monster_val_min": 40,
            "monster_exclude_tile_color": True,
            "monster_exclude_tile_dilate": 1,
            "monster_morph_open_iters": 1,
            "monster_morph_close_iters": 2,
            "monster_use_lab_assist": False,
            "monster_lab_tolerance": 22,
            
            # Colors
            "tile_color": asdict(ColorSpec((255, 0, 0))),
            "monster_colors": [
                asdict(ColorSpec((0, 255, 0), tol_rgb=35, tol_h=14, tol_s=70, tol_v=70)),
                asdict(ColorSpec((255, 255, 0), tol_rgb=35, tol_h=14, tol_s=70, tol_v=70))
            ],
            "hpbar_color": asdict(ColorSpec((255, 0, 0))),
            
            # ROIs
            "search_roi": None,
            "hpbar_roi": None,
            
            # Combat settings
            "hpbar_detect_enabled": True,
            "hpbar_min_area": 50,
            "hpbar_min_pixel_matches": 150,
            "post_combat_delay_min_s": 1.0,
            "post_combat_delay_max_s": 3.0,
            "combat_not_seen_timeout_s": 10.0,
            "combat_leave_immediately": True,
            "skip_detection_when_in_combat": True,
            
            # Camera adjustment
            "enable_cam_adjust": True,
            "cam_adjust_keys": ["up", "down", "right"],
            "cam_adjust_hold_s": 0.08,
            "cam_adjust_gap_s": 0.03,
            "micro_adjust_keys": ["right"],
            "micro_adjust_hold_s": 0.04,
            "micro_adjust_gap_s": 0.03,
            "micro_adjust_every_loops": 8,
            
            # Click settings
            "click_delay": 0.05,
            "click_after_found_sleep": 0.4,
            "min_monster_click_cooldown_s": 0.8,
            "min_monster_click_distance_px": 12,
            # Low-confidence click mode
            "low_confidence_click_enabled": True,
            "low_confidence_area_threshold": 220.0,
            "low_conf_min_count": 3,
            
            # Humanization
            "humanize_on": True,
            "break_every_s": 180.0,
            "break_duration_s": 4.0,
            "max_runtime_s": 0.0,
            
            # Anti-ban settings
            "antiban_mouse_movement_min": 5.0,
            "antiban_mouse_movement_max": 15.0,
            "antiban_micro_movement_min": 1.0,
            "antiban_micro_movement_max": 3.0,
            "antiban_break_interval_min": 180.0,
            "antiban_break_interval_max": 300.0,
            "antiban_break_duration_min": 2.0,
            "antiban_break_duration_max": 8.0,

            # Power management
            # Keep the system awake so the bot keeps running when the screen is off.
            # If you want to also force the display to stay on (so Windows doesn't blank it),
            # set keep_display_awake to True. For most users who want the monitor off but the
            # PC awake, keep_display_awake should remain False and turn the monitor off physically.
            "keep_awake_enabled": True,
            "keep_display_awake": True,
            
            # Debug settings
            "debug_overlay": False,
            "overlay_mode": "tile",
            "show_overlay_counts": True,
            "overlay_clip_to_roi": False,
            "overlay_follow_window": False,
            "debug_save_snapshots": False,
            "debug_output_dir": "outputs",
            
            # New v3 settings
            
            # Teleport settings
            "teleport_locations": [],
            "emergency_teleport_hotkey": "ctrl+h",
            "return_teleport_hotkey": "ctrl+t",
            
            # Potion settings
            "potion_locations": [],
            
            # Boost settings
            "boost_locations": [],
            
            # Instance settings
            "instance_token_location": None,
            "instance_teleport_location": None,
            "aggro_potion_location": None,
            "aggro_effect_roi": None,
            "aggro_effect_color": asdict(ColorSpec((255, 0, 0))),
            "aggro_duration": 300,
            "first_aggro_potion_timer": 60,
            "aggro_visual_check": True,
            "instance_token_delay": 1.0,
            "instance_only_mode": False,
            
            # Timeout settings
            "no_monster_timeout": 180,
            "camera_adjust_interval": 10,
            "emergency_teleport_threshold": 60
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        # Handle nested keys with dot notation
        if "." in key:
            parts = key.split(".")
            value = self._config
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value
        
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        # Handle nested keys with dot notation
        if "." in key:
            parts = key.split(".")
            config = self._config
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]
            config[parts[-1]] = value
        else:
            self._config[key] = value
    
    def get_color_spec(self, key: str) -> Optional[ColorSpec]:
        """
        Get a color specification
        
        Args:
            key: Configuration key for color spec
        
        Returns:
            ColorSpec object or None if not found
        """
        color_dict = self.get(key)
        if not color_dict:
            return None
        
        try:
            return ColorSpec(
                rgb=tuple(color_dict["rgb"]),
                tol_rgb=color_dict.get("tol_rgb", 8),
                use_hsv=color_dict.get("use_hsv", True),
                tol_h=color_dict.get("tol_h", 4),
                tol_s=color_dict.get("tol_s", 30),
                tol_v=color_dict.get("tol_v", 30)
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating ColorSpec from {key}: {e}")
            return None
    
    def get_roi(self, key: str) -> Optional[ROI]:
        """
        Get a region of interest
        
        Args:
            key: Configuration key for ROI
        
        Returns:
            ROI object or None if not found
        """
        roi_dict = self.get(key)
        if not roi_dict:
            return None
        
        try:
            return ROI(
                left=roi_dict["left"],
                top=roi_dict["top"],
                width=roi_dict["width"],
                height=roi_dict["height"]
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating ROI from {key}: {e}")
            return None
    
    def get_coordinate(self, key: str) -> Optional[Coordinate]:
        """
        Get a coordinate
        
        Args:
            key: Configuration key for coordinate
        
        Returns:
            Coordinate object or None if not found
        """
        coord_dict = self.get(key)
        if not coord_dict:
            return None
        
        try:
            return Coordinate(
                x=coord_dict["x"],
                y=coord_dict["y"],
                name=coord_dict.get("name", "")
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating Coordinate from {key}: {e}")
            return None
    
    def get_coordinates_list(self, key: str) -> List[Coordinate]:
        """
        Get a list of coordinates
        
        Args:
            key: Configuration key for coordinates list
        
        Returns:
            List of Coordinate objects
        """
        coords_list = self.get(key, [])
        result = []
        
        for i, coord_dict in enumerate(coords_list):
            try:
                coord = Coordinate(
                    x=coord_dict["x"],
                    y=coord_dict["y"],
                    name=coord_dict.get("name", f"Coordinate {i+1}")
                )
                result.append(coord)
            except (KeyError, ValueError, TypeError) as e:
                logger.error(f"Error creating Coordinate {i} from {key}: {e}")
        
        return result
    
    def set_color_spec(self, key: str, color_spec: ColorSpec) -> None:
        """
        Set a color specification
        
        Args:
            key: Configuration key for color spec
            color_spec: ColorSpec object
        """
        self.set(key, asdict(color_spec))
    
    def set_roi(self, key: str, roi: ROI) -> None:
        """
        Set a region of interest
        
        Args:
            key: Configuration key for ROI
            roi: ROI object
        """
        self.set(key, roi.to_dict())
    
    def set_coordinate(self, key: str, coordinate: Coordinate) -> None:
        """
        Set a coordinate
        
        Args:
            key: Configuration key for coordinate
            coordinate: Coordinate object
        """
        self.set(key, coordinate.to_dict())
    
    def set_coordinates_list(self, key: str, coordinates: List[Coordinate]) -> None:
        """
        Set a list of coordinates
        
        Args:
            key: Configuration key for coordinates list
            coordinates: List of Coordinate objects
        """
        self.set(key, [coord.to_dict() for coord in coordinates])
    
    def load_profile(self, profile_name: str) -> bool:
        """
        Load a configuration profile
        
        Args:
            profile_name: Name of the profile to load
        
        Returns:
            True if profile was loaded successfully, False otherwise
        """
        # Add .json extension if not present
        if not profile_name.endswith('.json'):
            profile_name += '.json'
        
        profile_path = os.path.join(self.config_dir, profile_name)
        
        if not os.path.exists(profile_path):
            logger.error(f"Profile not found: {profile_path}")
            return False
        
        try:
            with open(profile_path, 'r') as f:
                config_data = json.load(f)
            
            # Validate and merge with defaults
            self._config = {**self._get_default_config(), **config_data}
            self.current_profile = profile_name
            
            logger.info(f"Profile loaded: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Error loading profile {profile_name}: {e}")
            return False
    
    def save_profile(self, profile_name: str) -> bool:
        """
        Save current configuration to a profile
        
        Args:
            profile_name: Name of the profile to save
        
        Returns:
            True if profile was saved successfully, False otherwise
        """
        # Add .json extension if not present
        if not profile_name.endswith('.json'):
            profile_name += '.json'
        
        profile_path = os.path.join(self.config_dir, profile_name)
        
        try:
            with open(profile_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            
            self.current_profile = profile_name
            logger.info(f"Profile saved: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Error saving profile {profile_name}: {e}")
            return False
    
    def list_profiles(self) -> List[str]:
        """
        List available profiles
        
        Returns:
            List of profile names
        """
        try:
            profiles = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
            return profiles
        except Exception as e:
            logger.error(f"Error listing profiles: {e}")
            return []
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        self._config = self._get_default_config()
        self.current_profile = None
        logger.info("Configuration reset to defaults")