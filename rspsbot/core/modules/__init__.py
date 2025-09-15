"""
Modules for RSPS Color Bot v3

This package contains various modules that extend the bot's functionality.
"""

from .teleport import TeleportManager
from .potion import PotionManager
from .instance import InstanceManager

__all__ = [
    'TeleportManager',
    'PotionManager',
    'InstanceManager'
]