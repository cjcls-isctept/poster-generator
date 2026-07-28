"""
engine/styles.py
================

Definição dos estilos utilizados pelo motor de composição.

Este módulo não desenha nada.
Define apenas as propriedades de apresentação
dos diferentes elementos do poster.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ----------------------------------------------------------------------
# Tipos
# ----------------------------------------------------------------------

HorizontalAlign = Literal["left", "center", "right"]
VerticalAlign = Literal["top", "middle", "bottom"]

# ----------------------------------------------------------------------
# Estilo de texto
# ----------------------------------------------------------------------

@dataclass(slots=True)
class TextStyle:
    """
    Estilo de um bloco de texto.
    """

    # Fonte
    font: str = "title"

    # Cor
    color: str = "#000000"

    # Tamanho automático
    min_size: int = 12
    max_size: int = 120

    # Alinhamento
    align: HorizontalAlign = "center"
    valign: VerticalAlign = "middle"

    # Espaçamento entre linhas
    line_spacing: float = 1.10

    # Margens internas
    padding: int = 0

    # Permitir quebra de linha
    wrap: bool = True

    # Número máximo de linhas
    max_lines: int | None = None

    # Texto em maiúsculas
    uppercase: bool = False

    # Negrito (para futura utilização)
    bold: bool = False

# ----------------------------------------------------------------------
# Estilo do preço
# ----------------------------------------------------------------------

@dataclass(slots=True)
class PriceStyle:
    """
    Estilo dos preços.
    """

    color: str = "#D80000"

    font_big: str = "price_bold"
    font_small: str = "price_regular"

    min_size: int = 24
    max_size: int = 260

    # Percentagem da largura disponível que o preço deve ocupar
    fill_ratio: float = 0.97

    # Escala dos cêntimos
    cents_scale: float = 0.48

    # Espaço entre euros e cêntimos
    gap_ratio: float = 0.04

    # Quanto os cêntimos sobem relativamente ao valor principal
    superscript_ratio: float = 0.08

# ----------------------------------------------------------------------
# Estilo da imagem
# ----------------------------------------------------------------------

@dataclass(slots=True)
class ImageStyle:
    """
    Estilo da imagem do produto.
    """

    keep_aspect: bool = True

    zoom: float = 1.0

    shadow: bool = False

    shadow_offset: int = 8

    shadow_blur: int = 18

# ----------------------------------------------------------------------
# Estilo da badge
# ----------------------------------------------------------------------

@dataclass(slots=True)
class BadgeStyle:
    """
    Etiquetas de desconto.
    """

    background: str = "#E30613"

    text_color: str = "#FFFFFF"

    font: str = "small_bold"

    min_size: int = 18

    max_size: int = 48

# ----------------------------------------------------------------------
# Estilo do poster
# ----------------------------------------------------------------------

@dataclass(slots=True)
class PosterStyle:
    """
    Estilo geral do poster.
    """

    background: str = "#FFFFFF"

    header_background: str = "#000000"

    header_text: str = "#FFFFFF"

    accent_color: str = "#D80000"

    border_radius: int = 0