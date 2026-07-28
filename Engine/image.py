"""
engine/image.py
===============

Renderização de imagens em SVG.

Responsabilidades:

- carregar imagens
- calcular escalas
- contain
- cover
- center
- produzir elemento SVG <image>

Autor: Cláudio Lopes + ChatGPT
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

import svgwrite

from .geometry import Rect
from .renderer import Renderer
from .styles import ImageStyle
from .svg import SVGDocument


class ImageRenderer(Renderer):

    def __init__(
        self,
        style: ImageStyle,
    ):

        self.style = style

    # ---------------------------------------------------------

    def _load_image(
        self,
        filename: str | Path,
    ) -> Image.Image:

        return Image.open(filename)

    # ---------------------------------------------------------

    def _image_size(
        self,
        filename: str | Path,
    ) -> tuple[int, int]:

        with Image.open(filename) as img:

            return img.width, img.height

    # ---------------------------------------------------------

    def _contain(
        self,
        image_w: int,
        image_h: int,
        rect: Rect,
    ) -> Rect:

        scale = min(

            rect.width / image_w,

            rect.height / image_h,

        )

        w = image_w * scale
        h = image_h * scale

        x = rect.left + (rect.width - w) / 2
        y = rect.top + (rect.height - h) / 2

        return Rect(

            int(x),
            int(y),
            int(x + w),
            int(y + h),

        )

    # ---------------------------------------------------------

    def _cover(
        self,
        image_w: int,
        image_h: int,
        rect: Rect,
    ) -> Rect:

        scale = max(

            rect.width / image_w,

            rect.height / image_h,

        )

        w = image_w * scale
        h = image_h * scale

        x = rect.left + (rect.width - w) / 2
        y = rect.top + (rect.height - h) / 2

        return Rect(

            int(x),
            int(y),
            int(x + w),
            int(y + h),

        )

    # ---------------------------------------------------------

    def _fit_rect(
        self,
        filename: str | Path,
        rect: Rect,
    ) -> Rect:

        image_w, image_h = self._image_size(
            filename,
        )

        if self.style.fit == "contain":

            return self._contain(

                image_w,

                image_h,

                rect,

            )

        if self.style.fit == "cover":

            return self._cover(

                image_w,

                image_h,

                rect,

            )

        return rect
    
        # ---------------------------------------------------------

    def _preserve_aspect_ratio(self) -> str:
        """
        Valor SVG preserveAspectRatio correspondente ao modo escolhido.
        """

        if self.style.fit == "contain":
            return "xMidYMid meet"

        if self.style.fit == "cover":
            return "xMidYMid slice"

        return "none"

    # ---------------------------------------------------------

    def _create_image_element(
        self,
        document: SVGDocument,
        filename: str | Path,
        rect: Rect,
    ):

        drawing = document.drawing

        return drawing.image(

            href=str(filename),

            insert=(
                rect.left,
                rect.top,
            ),

            size=(
                rect.width,
                rect.height,
            ),

            preserveAspectRatio=self._preserve_aspect_ratio(),

        )

    # ---------------------------------------------------------

    def render(
        self,
        document: SVGDocument,
        rect: Rect,
        filename: str | Path,
    ) -> None:

        """
        Desenha a imagem no documento SVG.
        """

        filename = Path(filename)

        if not filename.exists():

            raise FileNotFoundError(filename)

        image_rect = self._fit_rect(
            filename,
            rect,
        )

        element = self._create_image_element(

            document,

            filename,

            image_rect,

        )

        document.add(element)