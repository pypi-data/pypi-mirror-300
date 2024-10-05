"""
Object detection using opencv
"""

from .object_detection import (
    # Thresher, HSVThresher, Image, Contour, Camera,
    RectangleContour,
    Processor,
    MultipleProcessor,
    Detector,
    Indicator,
    MultipleIndicator,
    Painter,
)
from .cv2_objects import (
    CV2Image as Image,
    CV2Contour as Contour,
    CV2Camera as Camera,
)
from .cv2_image_threshing import (
    CV2Thresher as Thresher,
    CV2HSVThresher as HSVThresher,
)
from .cv2_painting import (
    CV2ContourPainter as ContourPainter,
    CV2RectanglePainter as RectanglePainter,
    CV2CirclePainter as CirclePainter,
    CV2PointPainter as PointPainter,
)

__version__ = "1.1"
__name__ = 'ttt'
__all__ = [
    "Processor",
    "MultipleProcessor",
    "Detector",
    "Painter",
    "Indicator",
    "MultipleIndicator",
    "Image",
    "Contour",
    "RectangleContour",
    "Camera",
    "Thresher",
    "HSVThresher",
    "ContourPainter",
    "RectanglePainter",
    "CirclePainter",
    "PointPainter",
]
