from .detection import Detector, Image, Contour
from .painting import Painter


class Indicator:

    def __init__(self, detector: Detector, painter: Painter):
        self.detector = detector
        self.painter = painter

    def display(self, image: Image) -> Image:
        return self.painter.draw_all(image, self.get_contours(image))

    def get_contours(self, image: Image) -> list[Contour]:
        return self.detector.get_contours_by_image(image)


class MultipleIndicator:

    def __init__(self, indicators: list[Indicator]):
        self.indicators = indicators

    def display(self, image: Image) -> Image:
        new_image = image.copy()
        for indicator in self.indicators:
            new_image = indicator.display(new_image)
        return new_image
