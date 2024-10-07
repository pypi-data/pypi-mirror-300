from abc import abstractmethod
from .objects import Contour


class Processor:

    def get_contours(
        self, contours: list[Contour], height: int | float = 0, width: int | float = 0
    ) -> list[Contour]:
        self.height = height
        self.width = width
        return [contour for contour in contours if self.is_correct_contour(contour)]

    @abstractmethod
    def is_correct_contour(self, contour: Contour) -> bool:
        pass


class MultipleProcessor:
    def __init__(self, processors: list[Processor]) -> None:
        self.processors = processors

    def get_contours(self, contours: list, height=0, width=0) -> list[Contour]:
        for processor in self.processors:
            contours = processor.get_contours(contours, height, width)
        return contours
