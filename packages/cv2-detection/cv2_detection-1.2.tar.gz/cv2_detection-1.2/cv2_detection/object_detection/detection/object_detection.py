from .image_threshing import Thresher
from .contour_processing import MultipleProcessor
from .objects import Image, Contour


class Detector:

    def __init__(
        self, thresher: Thresher, multiple_processor: MultipleProcessor
    ) -> None:
        self.thresher = thresher
        self.multiple_processor = multiple_processor

    def get_contours_by_image(self, image: Image) -> list[Contour]:
        contours = self.thresher.get_contours(image)
        return self.multiple_processor.get_contours(contours, image.height, image.width)
