from .object_detection import Image, Contour
from .object_detection.indication import Painter
from .cv2_objects import CV2Image
import cv2


class CV2RectanglePainter(Painter):

    def draw(self, image: Image, contour: Contour) -> Image:
        new_image = image.copy()._image
        x, y, w, h = contour.bounding_rect
        cv2.rectangle(
            new_image,
            (x, y),
            (x + w, y + h),
            color=self.color,
            thickness=self.thickness,
        )
        return CV2Image(new_image)


class CV2ContourPainter(Painter):

    def draw(self, image: Image, contour: Contour) -> Image:
        new_image = image.copy()._image
        cv2.drawContours(
            new_image, [contour._contour], 0, color=self.color, thickness=self.thickness
        )
        return CV2Image(new_image)


class CV2CirclePainter(Painter):

    def __init__(
        self, color: tuple = (0, 255, 0), thickness=3, radius: int = 1
    ) -> None:
        self.radius = radius
        super().__init__(color, thickness)

    def draw(self, image: Image, contour: Contour) -> Image:
        new_image = image.copy()._image
        x, y, w, h = contour.bounding_rect
        cv2.circle(
            new_image,
            (x + w // 2, y + h // 2),
            radius=self.radius,
            color=self.color,
            thickness=self.thickness,
        )
        return CV2Image(new_image)


class CV2PointPainter(CV2CirclePainter):
    def __init__(self, color: tuple = (0, 255, 0), thickness=3) -> None:
        super().__init__(color, thickness, radius=0)
