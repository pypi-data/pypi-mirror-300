from .detection import Image, Contour
from abc import ABCMeta, abstractmethod


class Painter:
    __metaclass__ = ABCMeta

    def __init__(self, color: tuple = (0, 255, 0), thickness=3) -> None:
        self.color = color
        self.thickness = thickness

    @abstractmethod
    def draw(self, image: Image, contour: Contour) -> Image:
        pass

    def draw_all(self, image: Image, contours: list[Contour]) -> Image:
        new_image = image.copy()
        for contour in contours:
            new_image = self.draw(new_image, contour)
        return new_image
