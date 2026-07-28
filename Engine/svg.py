"""
engine/svg.py
=============

Camada de abstração sobre svgwrite.

Este módulo representa apenas um documento SVG.

Não conhece posters, preços nem produtos.
"""

from __future__ import annotations

from pathlib import Path

import svgwrite


class SVGDocument:

    def __init__(
        self,
        width: int,
        height: int,
    ):

        self.width = width
        self.height = height

        self._drawing = svgwrite.Drawing(
            size=(width, height),
            profile="full",
        )

    # ----------------------------------------------------------

    @property
    def drawing(self) -> svgwrite.Drawing:
        return self._drawing

    # ----------------------------------------------------------

    def add(self, element):

        """
        Adiciona qualquer elemento SVG ao documento.

        Exemplo:

            Text
            Image
            Rect
            Group
            Circle
        """

        self._drawing.add(element)

    # ----------------------------------------------------------

    def group(self, id: str | None = None):

        g = self._drawing.g(id=id)

        self._drawing.add(g)

        return g

    # ----------------------------------------------------------

    def defs(self):

        return self._drawing.defs

    # ----------------------------------------------------------

    def save(
        self,
        filename: str | Path,
    ):

        self._drawing.saveas(str(filename))