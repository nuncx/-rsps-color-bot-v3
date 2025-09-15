"""
Detection Package for RSPS Color Bot v3
"""

from .detector import DetectionEngine
from .color_detector import (
    build_mask,
    build_mask_multi,
    contours_to_screen_points,
    closest_contour_to_point,
    largest_contour,
    random_contour,
    draw_contours,
    draw_points
)
from .adaptive_detector import AdaptiveDetector
from .enhanced_adaptive_detector import EnhancedAdaptiveDetector
from .ml_detector import MLDetector
from .parallel_detector import ParallelDetector
from .capture import CaptureService

__all__ = [
    'DetectionEngine',
    'build_mask',
    'build_mask_multi',
    'contours_to_screen_points',
    'closest_contour_to_point',
    'largest_contour',
    'random_contour',
    'draw_contours',
    'draw_points',
    'AdaptiveDetector',
    'EnhancedAdaptiveDetector',
    'MLDetector',
    'ParallelDetector',
    'CaptureService'
]