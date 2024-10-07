from .object_detection import Image, Contour, Camera
from cv2.typing import MatLike
import cv2, numpy as np, base64


class CV2Contour(Contour):

    def __init__(self, _contour: MatLike) -> None:
        super().__init__(_contour)

    @property
    def area(self) -> int | float:
        return cv2.contourArea(self._contour)

    @property
    def bounding_rect(self) -> list[int | float]:
        return cv2.boundingRect(self._contour)


class CV2Image(Image):
    def __init__(self, _image: MatLike) -> None:
        super().__init__(_image)

    @property
    def height(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def shape(self) -> list:
        return self._image.shape

    def get_base64(self) -> str:
        _, buffer = cv2.imencode(".png", self._image)
        return base64.b64encode(buffer).decode("utf-8")

    def copy(self) -> Image:
        return CV2Image(self._image.copy())

    def get_image_by_bounding_rect(
        self, x: int | float, y: int | float, width: int | float, height: int | float
    ) -> Image:
        x1 = min(x + width, self.width)
        y1 = min(y + height, self.height)
        return CV2Image(self._image[y:y1, x:x1])

    def write(self, path: str) -> None:
        cv2.imwrite(path, self._image)

    @classmethod
    def read(cls, path: str) -> Image:
        return cls(cv2.imread(path))

    @classmethod
    def create_by_base64(cls, base64_image: str) -> Image:
        buffer = base64.b64decode(base64_image)
        numpy_image = np.frombuffer(buffer, np.uint8)
        image = cv2.imdecode(numpy_image, cv2.IMREAD_COLOR)
        return cls(image)


class DeadVideoCapture:

    def isOpened(self):
        return False

    def read(self):
        return 1, []


class CV2Camera(Camera):

    def __init__(self, path: int = 0, debug: bool = False) -> None:
        video_capture = DeadVideoCapture()
        if not debug:
            video_capture = cv2.VideoCapture(path)

        self._camera = video_capture

    @property
    def is_connected(self) -> bool:
        return self._camera.isOpened()

    def get_image(self) -> Image:
        success, frame = self._camera.read()
        return CV2Image(frame)
