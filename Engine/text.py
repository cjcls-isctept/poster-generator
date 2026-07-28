"""
engine/text.py
==============

Renderização de texto SVG.

Responsabilidades:

- ajuste automático do tamanho da fonte
- quebra automática de linhas
- medição do texto
- geração de elementos SVG

Autor: Cláudio Lopes + ChatGPT
"""

from __future__ import annotations

from dataclasses import replace
from typing import List

import svgwrite

from .fonts import get_font
from .geometry import Rect
from .renderer import Renderer
from .styles import TextStyle
from .svg import SVGDocument


class TextRenderer(Renderer):

    def __init__(self, style: TextStyle):

        self.style = style

    # ---------------------------------------------------------
    # Medição
    # ---------------------------------------------------------

    def _measure(
        self,
        text: str,
        size: int,
    ) -> tuple[int, int]:

        """
        Mede um texto utilizando Pillow.

        Devolve:
            largura, altura
        """

        font = get_font(
            self.style.font,
            size,
        )

        bbox = font.getbbox(text)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        return width, height

    # ---------------------------------------------------------

def _measure_lines(
    self,
    lines: list[str],
    size: int,
) -> tuple[int, int]:

    if not lines:
        return 0, 0

    widths = []

    line_height = int(size * self.style.line_spacing)

    for line in lines:

        w, _ = self._measure(
            line,
            size,
        )

        widths.append(w)

    return (
        max(widths),
        line_height * len(lines),
    )

    # ---------------------------------------------------------
    # Word wrapping
    # ---------------------------------------------------------

    def _wrap_text(
        self,
        text: str,
        size: int,
        max_width: int,
    ) -> List[str]:

        """
        Divide um texto em linhas respeitando max_width.
        """

        words = text.split()

        if not words:
            return []

        lines = []

        current = words[0]

        for word in words[1:]:

            candidate = current + " " + word

            w, _ = self._measure(
                candidate,
                size,
            )

            if w <= max_width:

                current = candidate

            else:

                lines.append(current)

                current = word

        lines.append(current)

        return lines

    
def _truncate_lines(
    self,
    lines: list[str],
    size: int,
    max_width: int,
) -> list[str]:

    """
    Aplica reticências à última linha quando necessário.
    """

    if (
        self.style.max_lines is None
        or
        len(lines) <= self.style.max_lines
    ):
        return lines

    lines = lines[: self.style.max_lines]

    last = lines[-1]

    while len(last) > 1:

        candidate = last + "..."

        w, _ = self._measure(
            candidate,
            size,
        )

        if w <= max_width:

            lines[-1] = candidate

            return lines

        last = last[:-1].rstrip()

    lines[-1] = "..."

    return lines
    
    # ---------------------------------------------------------
    # Ajuste automático
    # ---------------------------------------------------------

def _fit_font_size(
    self,
    text: str,
    rect: Rect,
    ) -> tuple[int, list[str]]:

    available_w = rect.width - self.style.padding * 2
    available_h = rect.height - self.style.padding * 2

    lo = self.style.min_size
    hi = self.style.max_size

    best_size = lo
    best_lines = [text]

    while lo <= hi:

        mid = (lo + hi) // 2

        if self.style.wrap:

            lines = self._wrap_text(
                text,
                mid,
                available_w,
            )

        else:

            lines = [text]

        lines = self._truncate_lines(
            lines,
            mid,
            available_w,
        )

        w, h = self._measure_lines(
            lines,
            mid,
        )

        if w <= available_w and h <= available_h:

            best_size = mid
            best_lines = lines

            lo = mid + 1

        else:

            hi = mid - 1

    return best_size, best_lines
    
    
    
    
    # ---------------------------------------------------------
    # Alinhamento
    # ---------------------------------------------------------

    def _anchor(self) -> str:

        if self.style.align == "left":
            return "start"

        if self.style.align == "right":
            return "end"

        return "middle"

    # ---------------------------------------------------------

    def _compute_position(
        self,
        rect: Rect,
        font_size: int,
        lines: list[str],
    ) -> tuple[float, float]:

        """
        Calcula a posição inicial (x,y) do bloco de texto.
        """

        line_height = font_size * self.style.line_spacing

        total_height = len(lines) * line_height

        # ---------- X ----------

        if self.style.align == "left":

            x = rect.left + self.style.padding

        elif self.style.align == "right":

            x = rect.right - self.style.padding

        else:

            x = rect.center_x

        # ---------- Y ----------

        if self.style.valign == "top":

            y = (
                rect.top
                + self.style.padding
                + font_size
            )

        elif self.style.valign == "bottom":

            y = (
                rect.bottom
                - self.style.padding
                - total_height
                + font_size
            )

        else:

            y = (
                rect.center_y
                - total_height / 2
                + font_size
            )

        return x, y

    # ---------------------------------------------------------
    # SVG
    # ---------------------------------------------------------

    def _create_text_element(
        self,
        document: SVGDocument,
        x: float,
        y: float,
        font_size: int,
        lines: list[str],
    ):

        """
        Cria um elemento SVG <text> contendo vários <tspan>.
        """

        drawing = document.drawing

        element = drawing.text(

            "",

            insert=(x, y),

            fill=self.style.color,

            font_family=self.style.font,

            font_size=font_size,

            text_anchor=self._anchor(),

        )

        dy = 0

        line_height = font_size * self.style.line_spacing

        for line in lines:

            element.add(

                drawing.tspan(

                    line,

                    x=[x],

                    dy=[dy],

                )

            )

            dy = line_height

        return element

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------

    def render(
        self,
        document: SVGDocument,
        rect: Rect,
        text: str,
    ) -> None:

        """
        Desenha o texto no documento SVG.
        """

        if not text:
            return

        if self.style.uppercase:

            text = text.upper()

        font_size, lines = self._fit_font_size(
            text,
            rect,
        )


        x, y = self._compute_position(
            rect,
            font_size,
            lines,
        )

        element = self._create_text_element(
            document,
            x,
            y,
            font_size,
            lines,
        )

        document.add(element)    
    