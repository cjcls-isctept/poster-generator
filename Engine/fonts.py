"""
engine/fonts.py
================

Gestão centralizada de fontes TrueType.

Responsabilidades:
    • carregar fontes
    • cache de fontes
    • medir texto
    • medir texto multilinha
    • métricas das fontes

Não desenha texto.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------
# Diretórios
# ---------------------------------------------------------------------

ENGINE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ENGINE_DIR.parent

ASSETS_DIR = PROJECT_DIR / "assets"
FONT_DIR = ASSETS_DIR / "fonts"

# ---------------------------------------------------------------------
# Fontes disponíveis
# ---------------------------------------------------------------------

FONT_FILES = {
    "title": "Montserrat-Regular.ttf",
    "title_bold": "Montserrat-Bold.ttf",
    "subtitle": "Montserrat-Medium.ttf",
    "subtitle_bold": "Montserrat-SemiBold.ttf",
    "price": "Montserrat-ExtraBold.ttf",
    "price_bold": "Montserrat-ExtraBold.ttf",
    "price_regular": "Montserrat-SemiBold.ttf",
    "small": "Montserrat-Regular.ttf",
    "small_bold": "Montserrat-Bold.ttf",
}

# ---------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------

@lru_cache(maxsize=256)
def get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """
    Devolve uma fonte TrueType com cache.
    """

    if size < 1:
        size = 1

    filename = FONT_FILES.get(name)

    if filename is None:
        raise ValueError(f"Fonte desconhecida: {name}")

    font_path = FONT_DIR / filename

    if not font_path.exists():
        raise FileNotFoundError(
            f"Fonte não encontrada:\n{font_path}"
        )

    return ImageFont.truetype(str(font_path), size=size)

# ---------------------------------------------------------------------
# Medição
# ---------------------------------------------------------------------

def measure_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
) -> tuple[int, int]:
    """
    Mede o tamanho real do texto.
    """

    if not text:
        return (0, 0)

    left, top, right, bottom = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return (
        right - left,
        bottom - top,
    )


def measure_multiline_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    spacing: int = 4,
) -> tuple[int, int]:
    """
    Mede texto multilinha.
    """

    if not text:
        return (0, 0)

    left, top, right, bottom = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        spacing=spacing,
    )

    return (
        right - left,
        bottom - top,
    )

# ---------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------

def line_height(
    font: ImageFont.FreeTypeFont,
) -> int:
    """
    Altura total da linha.
    """

    ascent, descent = font.getmetrics()

    return ascent + descent


def ascent(
    font: ImageFont.FreeTypeFont,
) -> int:

    return font.getmetrics()[0]


def descent(
    font: ImageFont.FreeTypeFont,
) -> int:

    return font.getmetrics()[1]


def text_bbox(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
):

    return draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

# ---------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------

def font_exists(name: str) -> bool:

    filename = FONT_FILES.get(name)

    if filename is None:
        return False

    return (FONT_DIR / filename).exists()


def available_fonts() -> list[str]:

    return sorted(FONT_FILES.keys())