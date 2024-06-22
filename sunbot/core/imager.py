"""imager.py"""

import re
from turtle import back
import warnings
from abc import ABC
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageColor


def is_color(color_string):
    # Define a regular expression pattern for common color representations
    color_pattern = re.compile(
        r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$|^rgb\((\d{1,3},){2}(\d{1,3})\)$|^rgba\((\d{1,3},){3}(\d{1,3}|1\.0)\)$"
    )

    # Check if the color string matches the pattern
    return bool(color_pattern.match(color_string))


class VisualAsset(ABC):

    def __init__(
        self,
        size: Optional[Tuple[int, int]] = None,
        background: Optional[Path | str | Tuple[float]] = None,
        ratio: Optional[float | str] = None,
        fixed_ratio: Optional[bool] = False,
    ):

        self.fixed_ratio = fixed_ratio

        if isinstance(background, (str, Path)):
            background = str(background)
            try:
                color = ImageColor.getcolor(background, "RGBA")
            except ValueError:
                self.background = Image.open(background)
                if not size:
                    size = (self.background.width, self.background.height)

        elif isinstance(background, tuple):
            num_elem = len(background)
            if num_elem < 3 or num_elem > 4:
                raise ValueError()
            if min(background) < 0 or max(background) > 255:
                raise ValueError()
            color = background

        # dimension have to be passed to create consistent asset
        if not size:
            raise ValueError("Unable to create asset because asset size is missing")

        self.__setup_asset_dimension(size, ratio)

        self.background = Image.new("RGBA", self.dimensions, background_color)

        # resize asset with appropriated dimensions
        self.background = self.background.resize(())

        # an asset have zero (root asset) or one parent, and zero, one or more contained asset
        self.__contained_assets = {}  # dict of contained elements
        self.__parent = None

    @property
    def width(self) -> int:
        """Visual asset width"""
        return self.__width

    @width.setter
    def width(self, value: int) -> None:
        self.__update_dimension("width", value)
        if self.fixed_ratio:
            self.__height = int(self.__width * (1 / self.__ratio))
        else:
            self.__ratio = self.width / self.height
        self.background.resize(self.dimensions)

    @property
    def height(self) -> int:
        """Visual asset height"""
        return self.__height

    @height.setter
    def height(self, value: int) -> None:
        self.__update_dimension("height", value)
        if self.fixed_ratio:
            self.__width = int(self.height * self.__ratio)
        else:
            self.__ratio = self.width / self.height
        self.background.resize(self.dimensions)

    @property
    def __ratio(self):
        return self.__ratio

    @__ratio.setter
    def __ratio(self, value):
        raise AttributeError("Asset ratio cannot be manually updated")

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Get asset dimensions"""
        return (self.__width, self.__height)

    def parent(self):
        return self.__parent

    def __update_dimension(self, dim_name: str, value: int) -> None:
        if value < 0:
            raise ValueError(
                f"Update failed: {dim_name} only support positive value. Specified value: {value}"
            )
        setattr(self, f"__{dim_name}", value)

    def __setup_asset_dimension(self, size, ratio) -> None:
        if len(size) == 1:
            self.__width = size[0]
            if not ratio:
                raise ValueError("Height or size ratio must be specified")
            if isinstance(ratio, str):
                quotient = ratio.split(":")
                self.__ratio = int(quotient[0]) / int(quotient[1])
            else:
                self.__ratio = ratio
            self.__height = int(self.__width * (1 / self.__ratio))
        elif len(size) == 2:
            self.__width, self.__height = size
            self.__ratio = self.__width / self.__height
            if ratio:
                warnings.warn(
                    "Specified ratio value was ignored as width and height were passed in arguments"
                )
        else:
            raise ValueError("Only 2D assets are supported")

    def add_asset(self, asset: "VisualAsset", position: Tuple[int, int]) -> None:
        """Add asset on this asset at specified (x, y) position"""
        x, y = position
        if (x < 0) or (x >= self.width):
            raise IndexError(f"{x} out of asset bounds: (0, {self.width})")
        if (y < 0) or (y >= self.height):
            raise IndexError(f"{y} out of asset bounds: (0, {self.height})")
        if (x + asset.width > self.width) or (y + asset.height > self.height):
            warnings.warn(
                "The asset to be added will overflow from the asset container"
            )

    def save(self):
        raise NotImplementedError
