from __future__ import annotations
from abc import ABCMeta, abstractmethod


class Contour:
    __metaclass__ = ABCMeta

    def __init__(self, _contour) -> None:
        self._contour = _contour

    @property
    @abstractmethod
    def area(self) -> int | float:
        pass

    @property
    @abstractmethod
    def bounding_rect(self) -> list[int | float]:
        pass


class RectangleContour(Contour):
    __metaclass__ = ABCMeta

    def __init__(
        self, x: int | float, y: int | float, width: int | float, height: int | float
    ) -> None:
        super().__init__([x, y, width, height])

    @property
    def area(self) -> int | float:
        return self._contour[2] * self._contour[3]

    @property
    def bounding_rect(self) -> list[int | float]:
        return self._contour


class Image:
    __metaclass__ = ABCMeta

    def __init__(self, _image) -> None:
        self._image = _image

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def shape(self) -> list:
        pass

    @abstractmethod
    def get_base64(self) -> str:
        pass

    @abstractmethod
    def copy(self) -> Image:
        return Image([])

    @abstractmethod
    def write(self, path: str) -> None:
        pass

    @abstractmethod
    def get_image_by_bounding_rect(
        self, x: int | float, y: int | float, width: int | float, height: int | float
    ) -> Image:
        pass

    @classmethod
    @abstractmethod
    def read(cls, path: str) -> Image:
        pass

    @classmethod
    @abstractmethod
    def create_by_base64(cls, base64_image: str) -> Image:
        pass


class Camera:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def get_image(self) -> Image:
        pass
