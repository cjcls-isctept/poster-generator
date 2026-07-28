"""
compose.py
Junta um template (templates.py) + os dados de um produto + a foto encontrada
no disco, e produz a imagem final do poster, num tamanho de saída à escolha
(print_a4 / social_square / social_story).
"""

from __future__ import annotations
from dataclasses import dataclass
from PIL import Image, ImageDraw
import math

from templates import TEMPLATES, OUTPUT_FORMATS
from poster_engine import (
    fit_text_multiline,
    fit_font_size,
    measure_text,
    render_price,
    fit_product_image,
    draw_discount_badge,
    get_font,
)


@dataclass
class Product:
    codigo_interno: str
    codigo_barras: str
    descricao: str
    preco: float
    preco_promocao: float | None
    desconto_pct: int | None
    photo_path: str | None


def _zone_px(zone_frac: tuple[float, float, float, float], w: int, h: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = zone_frac
    return int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)


def _draw_decor(draw: ImageDraw.ImageDraw, template: dict, w: int, h: int) -> None:
    """Elementos decorativos leves por template — mantém o layout genérico intacto
    e só acrescenta o 'tempero' sazonal por cima."""
    decor = template.get("decor", "none")
    if decor == "snow":
        import random
        rnd = random.Random(42)  # seed fixa: resultado reprodutível entre execuções
        for _ in range(40):
            x, y = rnd.uniform(0, w), rnd.uniform(0.10 * h, h)
            r = rnd.uniform(2, 5)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 180))
    elif decor == "sun":
        cx, cy, R = int(w * 0.9), int(h * 0.06), int(w * 0.18)
        for i in range(12):
            angle = i * (360 / 12)
            x2 = cx + R * 1.4 * math.cos(math.radians(angle))
            y2 = cy + R * 1.4 * math.sin(math.radians(angle))
            draw.line([cx, cy, x2, y2], fill=template["header_bg"], width=6)
        draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=template["header_bg"])


def generate_poster(product: Product, template_key: str, output_format: str) -> Image.Image:
    template = TEMPLATES[template_key]
    fmt = OUTPUT_FORMATS[output_format]
    w, h = fmt["size"]

    canvas = Image.new("RGBA", (w, h), template["bg_color"])
    draw = ImageDraw.Draw(canvas)
    zones = template["zones"]

    # --- header ---
    #hx0, hy0, hx1, hy1 = _zone_px(zones["header"], w, h)
    #draw.rectangle([hx0, hy0, hx1, hy1], fill=template["header_bg"])
    #header_font = fit_font_size(draw, template["header_text"], "title_bold",
    #                             int((hx1 - hx0) * 0.9), int((hy1 - hy0) * 0.7), 10, 200)
    #tw, th = measure_text(draw, template["header_text"], header_font)
    #draw.text(((hx0 + hx1 - tw) / 2, hy0 + ((hy1 - hy0) - th) / 2),
    #           template["header_text"], font=header_font, fill="white")

    _draw_decor(draw, template, w, h)

    # --- imagem do produto ---
    ix0, iy0, ix1, iy1 = _zone_px(zones["image"], w, h)
    product_img = fit_product_image(product.photo_path, (ix1 - ix0, iy1 - iy0))
    canvas.paste(product_img, (ix0, iy0), product_img)

    # --- título (auto-fit, até 2 linhas) ---
    tx0, ty0, tx1, ty1 = _zone_px(zones["title"], w, h)
    font, lines = fit_text_multiline(
        draw, product.descricao, "title_medium",
        max_width=tx1 - tx0, max_height=ty1 - ty0,
        min_size=int(h * 0.012), max_size=int(h * 0.045), max_lines=2,
    )
    _, line_h = measure_text(draw, "Ag", font)
    line_h = int(line_h * 1.08)
    total_h = line_h * len(lines)
    start_y = ty0 + ((ty1 - ty0) - total_h) // 2
    for i, line in enumerate(lines):
        lw, _ = measure_text(draw, line, font)
        draw.text((tx0 + ((tx1 - tx0) - lw) / 2, start_y + i * line_h),
                   line, font=font, fill=template["title_color"])

    # --- preço original riscado (só se houver promoção) ---
    if product.preco_promocao is not None and product.preco_promocao < product.preco:
        opx0, opy0, opx1, opy1 = _zone_px(zones["original_price"], w, h)
        orig_text = f"{product.preco:,.2f}€".replace(",", "X").replace(".", ",").replace("X", ".")
        of = fit_font_size(draw, orig_text, "price_regular", opx1 - opx0, opy1 - opy0, 8, 100)
        ow, oh = measure_text(draw, orig_text, of)
        oy = opy0 + ((opy1 - opy0) - oh) // 2
        draw.text((opx0, oy), orig_text, font=of, fill=template["original_price_color"])
        # linha de "riscado"
        draw.line([opx0, oy + oh / 2, opx0 + ow, oy + oh / 2],
                   fill=template["original_price_color"], width=max(2, int(oh * 0.06)))
        final_price = product.preco_promocao
    else:
        final_price = product.preco

    # --- preço final (grande, autoajustado) ---
    px0, py0, px1, py1 = _zone_px(zones["price"], w, h)
    label_font = get_font(
    "title_bold",
    int((py1 - py0) * 0.12)
    )

    draw.text(
        (px0, py0 - 45),
        "AGORA",
        font=label_font,
        fill=template["price_color"]
    )
    render_price(
    canvas,
    (px0,py0,px1,py1),
    final_price,
    template["price_color"],
    )   

    # --- badge de desconto (só se houver desconto) ---
    if product.desconto_pct:
        bcx, bcy = zones["badge_center"]
        radius = int(zones["badge_radius_frac"] * min(w, h))
        draw_discount_badge(canvas, draw, (int(bcx * w), int(bcy * h)), radius,
                             product.desconto_pct, template["badge_bg"], template["badge_text"])

    return canvas.convert("RGB")
