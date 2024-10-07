from abc import ABCMeta, abstractmethod
from .objects import Image, Contour


class Thresher:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **options: dict) -> None:
        pass

    def get_contours(self, image: Image) -> list[Contour]:
        threshold_image = self.get_finished_image(image)
        return self.get_contours_by_threshold_image(threshold_image)

    def get_finished_image(self, image: Image) -> Image:
        threshold_image = self.get_threshold_image(image)
        return self.get_enhanced_threshold_image(threshold_image)

    @abstractmethod
    def get_threshold_image(self, image: Image) -> Image:
        pass

    @abstractmethod
    def get_enhanced_threshold_image(self, threshold_image: Image) -> Image:
        pass

    @abstractmethod
    def get_contours_by_threshold_image(self, threshold_image: Image) -> list[Contour]:
        pass


class HSVThresher(Thresher):
    __metaclass__ = ABCMeta

    _hsv_ranges = []

    @abstractmethod
    def __init__(self, hsv_ranges, **options: dict) -> None:
        self.set_hsv_ranges(hsv_ranges)

    @property
    def hsv_ranges(self) -> list:
        return list(self._hsv_ranges)

    @abstractmethod
    def set_hsv_ranges(self, hsv_ranges) -> None:
        pass
