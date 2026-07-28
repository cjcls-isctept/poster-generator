"""
templates.py
Cada template define ZONAS EM FRAÇÕES (0.0 a 1.0) do canvas, não em pixels fixos.
Isto é o que permite gerar o MESMO template em tamanhos diferentes (A4 para
impressão, quadrado para Instagram, story vertical) sem reescrever nada —
a zona "title" a 6%-58%-94%-70% do canvas significa a mesma coisa em qualquer
resolução.

Para criar um template sazonal novo (ex. Páscoa, Black Friday):
copia um dos dicts abaixo, muda cores/decor/header_text, e adiciona à lista TEMPLATES.
"""

TEMPLATES = {
    "generico": {
        "label": "Genérico",
        "bg_color": (255, 255, 255, 255),
        "accent_color": "#E30613",
        "price_color": "#E30613",
        "original_price_color": "#8A8A8A",
        "title_color": "#1A1A1A",
        "badge_bg": "#E30613",
        "badge_text": "#FFFFFF",
        "header_text": "PROMOÇÃO",
        "header_bg": "#1A1A1A",
        "decor": "none",
        "zones": {
            # Header (mantém ou reduz)
            "header": (0.0, 0.0, 1.0, 0.08),
            # Descrição no topo
            "title": (
                0.08,
                0.10,
                0.92,
                0.22
            ),
            # Imagem do lado esquerdo
            "image": (
                0.05,
                0.25,
                0.48,
                0.92
            ),
            # Preço antigo no lado direito
            "original_price": (
                0.56,
                0.32,
                0.92,
                0.42
            ),
            # Preço novo por baixo
            "price": (
                0.52,
                0.45,
                0.95,
                0.85
            ),
            # Badge
            "badge_center": (0.90, 0.12),
            "badge_radius_frac": 0.09,
        },
    },
    "natal": {
        "label": "Natal",
        "bg_color": (250, 245, 240, 255),
        "accent_color": "#0F6B3C",
        "price_color": "#C21807",
        "original_price_color": "#7A7A7A",
        "title_color": "#0F3D24",
        "badge_bg": "#C21807",
        "badge_text": "#FFFFFF",
        "header_text": "PROMOÇÃO DE NATAL",
        "header_bg": "#0F6B3C",
        "decor": "snow",
        "zones": {
            "header": (0.0, 0.0, 1.0, 0.10),
            "image": (0.08, 0.13, 0.92, 0.56),
            "title": (0.08, 0.58, 0.92, 0.70),
            "original_price": (0.08, 0.71, 0.55, 0.79),
            "price": (0.08, 0.79, 0.68, 0.97),
            "badge_center": (0.84, 0.85),
            "badge_radius_frac": 0.13,
        },
    },
    "verao": {
        "label": "Verão",
        "bg_color": (255, 251, 235, 255),
        "accent_color": "#0A7EA4",
        "price_color": "#E85D04",
        "original_price_color": "#8A8A8A",
        "title_color": "#023047",
        "badge_bg": "#0A7EA4",
        "badge_text": "#FFFFFF",
        "header_text": "PROMOÇÃO DE VERÃO",
        "header_bg": "#F4A300",
        "decor": "sun",
        "zones": {
            "header": (0.0, 0.0, 1.0, 0.09),
            "image": (0.08, 0.12, 0.92, 0.56),
            "title": (0.08, 0.58, 0.92, 0.70),
            "original_price": (0.08, 0.71, 0.55, 0.79),
            "price": (0.08, 0.79, 0.68, 0.97),
            "badge_center": (0.84, 0.85),
            "badge_radius_frac": 0.13,
        },
    },
}

# Tamanhos de saída suportados. width/height em pixels; dpi só é relevante
# para o PDF de impressão (define a escala física quando abrires no software de imprensa).
OUTPUT_FORMATS = {
    "print_a4": {"size": (2480, 3508), "dpi": 300},   # A4 vertical, pronto a imprimir
    "social_square": {"size": (1080, 1080), "dpi": 72},   # feed Instagram/Facebook
    "social_story": {"size": (1080, 1920), "dpi": 72},   # stories/reels
}
