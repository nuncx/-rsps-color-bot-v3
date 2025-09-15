"""
Antiban module for RSPS Color Bot v3
Implements non-interfering antiban techniques
"""

import random
import time
import logging
import math
from typing import Tuple, List, Optional, Callable
import pyautogui

# Get module logger
logger = logging.getLogger('rspsbot.core.antiban')

class AntiBanManager:
    """
    Manages anti-ban techniques to make bot behavior more human-like
    """
    
    def __init__(self, config_manager=None):
        """Initialize the anti-ban manager"""
        self.config = config_manager
        self.last_mouse_move = time.time()
        self.last_break = time.time()
        self.last_micro_movement = time.time()
        
        # Default settings if config is not provided
        self.mouse_movement_interval = (5.0, 15.0)  # Random interval between mouse movements
        self.micro_movement_interval = (1.0, 3.0)   # Random interval between micro movements
        self.break_interval = (180.0, 300.0)        # Random interval between breaks
        self.break_duration = (2.0, 8.0)            # Random break duration
        self.click_variation = 30.0                 # Percentage variation in click timing
        self.enabled = True                         # Whether anti-ban is enabled
        
        # Load settings from config if available
        if self.config:
            self._load_settings()
            
        logger.info("Anti-ban manager initialized")
    
    def _load_settings(self):
        """Load settings from config"""
        # Check if anti-ban is enabled
        self.enabled = self.config.get('antiban_enabled', True)
        
        # Mouse movement settings
        min_move = self.config.get('antiban_mouse_movement_min', 5.0)
        max_move = self.config.get('antiban_mouse_movement_max', 15.0)
        self.mouse_movement_interval = (min_move, max_move)
        
        # Micro movement settings
        min_micro = self.config.get('antiban_micro_movement_min', 1.0)
        max_micro = self.config.get('antiban_micro_movement_max', 3.0)
        self.micro_movement_interval = (min_micro, max_micro)
        
        # Break settings
        min_break = self.config.get('antiban_break_interval_min', 180.0)
        max_break = self.config.get('antiban_break_interval_max', 300.0)
        self.break_interval = (min_break, max_break)
        
        min_duration = self.config.get('antiban_break_duration_min', 2.0)
        max_duration = self.config.get('antiban_break_duration_max', 8.0)
        self.break_duration = (min_duration, max_duration)
        
        # Click timing variation
        self.click_variation = self.config.get('antiban_click_variation', 30.0)
    
    def randomize_click_timing(self, base_delay: float = 0.05) -> float:
        """
        Add randomization to click timing
        
        Args:
            base_delay: Base delay in seconds
            
        Returns:
            Randomized delay in seconds
        """
        if not self.enabled:
            return base_delay
            
        # Add random variation based on configured percentage
        variation = base_delay * (self.click_variation / 100.0)
        return base_delay + random.uniform(-variation, variation)
    
    def randomize_movement(self, 
                          start_x: int, start_y: int, 
                          end_x: int, end_y: int, 
                          duration: float = 0.2) -> None:
        """
        Move mouse in a human-like pattern from start to end point
        
        Args:
            start_x, start_y: Starting coordinates
            end_x, end_y: Ending coordinates
            duration: Movement duration in seconds
        """
        # Calculate distance
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # For very short distances, just move directly
        if distance < 10:
            pyautogui.moveTo(end_x, end_y, duration=duration)
            return
        
        # For longer distances, use bezier curve or other human-like pattern
        # Number of control points based on distance
        num_points = min(max(int(distance / 100), 2), 5)
        
        # Generate control points
        control_points = []
        for i in range(num_points):
            # Random offset perpendicular to movement direction
            dx = end_x - start_x
            dy = end_y - start_y
            
            # Perpendicular vector
            perp_x = -dy
            perp_y = dx
            
            # Normalize and scale
            length = math.sqrt(perp_x**2 + perp_y**2)
            if length > 0:
                perp_x = perp_x / length * random.uniform(-50, 50)
                perp_y = perp_y / length * random.uniform(-50, 50)
            
            # Position along the path
            t = (i + 1) / (num_points + 1)
            point_x = start_x + dx * t + perp_x
            point_y = start_y + dy * t + perp_y
            
            control_points.append((point_x, point_y))
        
        # Move through control points
        pyautogui.moveTo(start_x, start_y, duration=0)
        
        # Move through each control point
        segment_duration = duration / (len(control_points) + 1)
        for point_x, point_y in control_points:
            # Add slight randomization to timing
            actual_duration = segment_duration * random.uniform(0.8, 1.2)
            pyautogui.moveTo(point_x, point_y, duration=actual_duration)
        
        # Final move to destination
        pyautogui.moveTo(end_x, end_y, duration=segment_duration * random.uniform(0.8, 1.2))
    
    def should_take_break(self) -> Tuple[bool, float]:
        """
        Check if it's time to take a break
        
        Returns:
            Tuple of (should_break, break_duration)
        """
        if not self.enabled:
            return False, 0.0
            
        now = time.time()
        elapsed = now - self.last_break
        
        # Get random interval
        interval = random.uniform(*self.break_interval)
        
        if elapsed >= interval:
            # Time for a break
            duration = random.uniform(*self.break_duration)
            self.last_break = now
            return True, duration
        
        return False, 0.0
    
    def should_move_mouse(self) -> bool:
        """
        Check if it's time to move the mouse randomly
        
        Returns:
            True if mouse should be moved
        """
        if not self.enabled:
            return False
            
        now = time.time()
        elapsed = now - self.last_mouse_move
        
        # Get random interval
        interval = random.uniform(*self.mouse_movement_interval)
        
        if elapsed >= interval:
            self.last_mouse_move = now
            return True
        
        return False
    
    def perform_random_mouse_movement(self) -> None:
        """Perform a random mouse movement"""
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        
        # Random position within screen bounds
        x = random.randint(100, screen_width - 100)
        y = random.randint(100, screen_height - 100)
        
        # Move mouse with human-like pattern
        current_x, current_y = pyautogui.position()
        self.randomize_movement(current_x, current_y, x, y, duration=random.uniform(0.3, 0.8))
        
        logger.debug(f"Performed random mouse movement to ({x}, {y})")
    
    def perform_micro_movement(self) -> None:
        """Perform a small mouse movement"""
        if not self.enabled:
            return
            
        now = time.time()
        elapsed = now - self.last_micro_movement
        
        # Get random interval
        interval = random.uniform(*self.micro_movement_interval)
        
        if elapsed >= interval:
            # Get current position
            current_x, current_y = pyautogui.position()
            
            # Small random offset
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            
            # Move mouse slightly
            pyautogui.moveTo(current_x + offset_x, current_y + offset_y, duration=0.1)
            
            self.last_micro_movement = now
            logger.debug("Performed micro mouse movement")
    
    def randomize_delay(self, min_delay: float, max_delay: float) -> float:
        """
        Generate a random delay between min and max
        
        Args:
            min_delay: Minimum delay in seconds
            max_delay: Maximum delay in seconds
            
        Returns:
            Random delay in seconds
        """
        return random.uniform(min_delay, max_delay)
    
    def take_break(self, duration: float) -> None:
        """
        Take a break for the specified duration
        
        Args:
            duration: Break duration in seconds
        """
        logger.info(f"Taking a break for {duration:.2f} seconds")
        
        # During the break, perform some random actions
        break_end = time.time() + duration
        
        while time.time() < break_end:
            # Random action
            action = random.choice([
                "move_mouse",
                "micro_movement",
                "wait"
            ])
            
            if action == "move_mouse":
                self.perform_random_mouse_movement()
            elif action == "micro_movement":
                self.perform_micro_movement()
            
            # Wait a bit
            time.sleep(random.uniform(0.5, 1.5))
        
        logger.info("Break finished")

if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.DEBUG)
    
    antiban = AntiBanManager()
    
    # Test randomize_click_timing
    for _ in range(5):
        print(f"Randomized click timing: {antiban.randomize_click_timing():.4f}s")
    
    # Test randomize_movement
    print("Testing randomize_movement...")
    antiban.randomize_movement(100, 100, 400, 300)
    
    # Test should_take_break
    antiban.break_interval = (1.0, 2.0)  # For testing
    should_break, duration = antiban.should_take_break()
    print(f"Should take break: {should_break}, duration: {duration:.2f}s")
    
    if should_break:
        antiban.take_break(duration)