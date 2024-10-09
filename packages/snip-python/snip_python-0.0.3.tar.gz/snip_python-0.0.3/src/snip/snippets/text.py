"""Text snip module allows to display text in the labbook."""

from typing import TypedDict

from typing_extensions import NotRequired

from .base import BaseSnip


class TextStyles(TypedDict):
    """Text styles."""

    font_size: NotRequired[int]
    font_family: NotRequired[str]
    font_color: NotRequired[str]

    # percent of the font size
    # Defaults to 1.25
    line_height: NotRequired[float]

    """Wrap text after a certain number of pixels."""
    line_wrap: NotRequired[int]


class TextSnip(BaseSnip[dict, dict]):
    """Text snip class.

    Represents a text in the labbook.
    """

    type = "text"

    def __init__(self, text: str, book_id: int, **kwargs):
        """Create a text snip from a string.

        Parameters
        ----------
        text : str
            The text to display.
        book_id : int
            The book_id of the snippet.
        kwargs : Any
            Additional keyword arguments to pass to the Base
        """
        super().__init__(book_id=book_id, **kwargs)
        self.text = text

    def _data(self) -> dict:
        """Get the data representation of the text snip."""
        return {"text": self.text}

    styles = TextStyles(
        font_family="Arial",
    )

    def _view(self) -> dict:
        """Get the view representation of the text snip."""
        ret = super()._view() or {}

        if self.styles and self.styles.get("font_size") is not None:
            ret["size"] = self.styles.get("font_size")

        if self.styles and self.styles.get("font_family") is not None:
            ret["font"] = self.styles.get("font_family")

        if self.styles and self.styles.get("font_color") is not None:
            ret["colour"] = self.styles.get("font_color")

        if self.styles and self.styles.get("line_height") is not None:
            ret["lheight"] = self.styles.get("line_height")

        if self.styles and self.styles.get("line_wrap") is not None:
            ret["wrap"] = self.styles.get("line_wrap")

        return ret

    # ---------------------------------------------------------------------------- #
    #                          Some helpers for the styles                         #
    # ---------------------------------------------------------------------------- #

    @property
    def font_size(self) -> int:
        """Get the font size."""
        return self.styles.get("font_size", 12)

    @font_size.setter
    def font_size(self, value: int):
        """Set the font size."""
        self.styles["font_size"] = value

    @property
    def font_family(self) -> str:
        """Get the font family."""
        return self.styles.get("font_family", "Arial")

    @font_family.setter
    def font_family(self, value: str):
        """Set the font family."""
        self.styles["font_family"] = value

    @property
    def font_color(self) -> str:
        """Get the font color."""
        return self.styles.get("font_color", "#ffffff")

    @font_color.setter
    def font_color(self, value: str):
        """Set the font color."""
        self.styles["font_color"] = value
