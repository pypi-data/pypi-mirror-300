"""Image snip module allows to display images in the labbook."""

from __future__ import annotations

import base64
import importlib.util
import io
from typing import TYPE_CHECKING, Optional, Tuple

from PIL import Image

from .base import BaseSnip

if TYPE_CHECKING:  # pragma: no cover
    try:
        from matplotlib.figure import Figure
    except ImportError:
        pass


class ImageSnip(BaseSnip[dict, dict]):
    """Image snip class.

    Represents an image in the labbook. You may construct an image from
    a matplotlib figure, a PIL image, or a numpy array.

    The default constructor is not meant to be used directly. Instead, use the
    `from_array`, `from_pil`, or `from_matplotlib` constructors.
    """

    type = "image"

    def __init__(
        self,
        image: Image.Image,
        book_id: int,
        deployment: Optional[str] = None,
    ):
        """Create an image snip from a PIL image.

        Parameters
        ----------
        image : Image.Image
            The image to display.
        book_id : int
            The book_id of the snippet.
        deployment : Optional[str]
            The deployment to upload the snippet to. If None, the default deployment is used.
        """
        super().__init__(book_id=book_id, deployment=deployment)
        self.image = image

    @classmethod
    def from_pil(
        cls,
        image: Image.Image,
        book_id: int,
        deployment: Optional[str] = None,
    ) -> ImageSnip:
        """Create an image snip from a PIL image.

        Parameters
        ----------
        image : Image.Image
            The image to display.
        book_id : int
            The book_id of the snippet.
        deployment : Optional[str]
            The deployment to upload the snippet to. If None, the default deployment is used.

        Returns
        -------
        ImageSnip
            The image snip.
        """
        return cls(image, book_id, deployment)

    @classmethod
    def from_array(
        cls,
        array,
        book_id: int,
        deployment: Optional[str] = None,
        **kwargs,
    ) -> ImageSnip:
        """Create an image snip from a numpy array.

        Parameters
        ----------
        array : Any
            The numpy 3d array to display. The array should be in the format
            (height, width, 3) or (height, width, 4). See `pillow.Image.fromarray`
            for more information on the supported array formats.
        book_id : int
            The book_id of the snippet.
        deployment : Optional[str]
            The deployment to upload the snippet to. If None, the default deployment is used.
        kwargs : Any
            Additional keyword arguments to pass to `pillow.Image.fromarray`.

        Returns
        -------
        ImageSnip
            The image snip.
        """
        return cls(Image.fromarray(array, **kwargs), book_id, deployment)

    @classmethod
    def from_matplotlib(
        cls,
        figure: Figure,
        book_id: int,
        deployment: Optional[str] = None,
        **kwargs,
    ) -> ImageSnip:
        """Create an image snip from a matplotlib figure.

        Parameters
        ----------
        figure : matplotlib.figure.Figure
            The figure to display.
        book_id : int
            The book_id of the snippet.
        deployment : Optional[str]
            The deployment to upload the snippet to. If None, the default deployment is used.
        kwargs : Any
            Additional keyword arguments to pass to `figure.savefig`

        Returns
        -------
        ImageSnip
            The image snip.
        """
        available = importlib.util.find_spec("matplotlib")
        if available is None:  # pragma: no cover
            raise ImportError(
                "Matplotlib is required to use this function. Install it via `pip install matplotlib`."
            )

        buf = io.BytesIO()
        figure.savefig(buf, format="png", **kwargs)
        buf.seek(0)
        return cls(Image.open(buf), book_id, deployment)

    def _data(self):
        """Return the image data."""
        return {
            "blob": {
                "mime": "image/png",
                "data": self._as_b64(),
                "size": self.image.__sizeof__(),
            }
        }

    __size: Optional[Tuple[int, int]] = None

    @property
    def size(self):
        """Return the width and height of the image."""
        size = self.__size
        if size is None:
            size = (self.image.width, self.image.height)
            if size[0] > 1400:
                size = (1400, int(1400 / size[0] * size[1]))
        return size

    @property
    def width(self):
        """Return the width of the image."""
        return self.size[0]

    @property
    def height(self):
        """Return the height of the image."""
        return self.size[1]

    @width.setter
    def width(self, width: int):
        self.set_width(width)

    @height.setter
    def height(self, height: int):
        self.set_height(height)

    def set_width(self, width: int, keep_ratio: bool = True):
        """Set the width of the image."""
        if keep_ratio:
            self.__size = (width, int(width / self.size[0] * self.size[1]))
        else:
            self.__size = (width, self.size[1])

    def set_height(self, height: int, keep_ratio: bool = True):
        """Set the height of the image."""
        if keep_ratio:
            self.__size = (int(height / self.size[1] * self.size[0]), height)
        else:
            self.__size = (self.size[0], height)

    def scale(self, ratio: float):
        """Scale the image by a given ratio."""
        self.__size = (int(self.size[0] * ratio), int(self.size[1] * ratio))

    def _view(self):
        """Return the image view."""
        ret = super()._view() or {}

        if self.__size is not None:
            ret["width"] = self.width
            ret["height"] = self.height
        return ret if ret != {} else None

    def _as_b64(self):
        buffered = io.BytesIO()
        self.image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
