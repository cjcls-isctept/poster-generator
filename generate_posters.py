"""
generate_posters.py
Script principal: lê o Excel de produtos + a pasta de fotos (nomeadas por código de
barras), valida os dados, e gera os posters em lote nos formatos escolhidos.

Uso:
    python generate_posters.py --excel sample_data/produtos.xlsx \
                                --photos sample_data/photos \
                                --template natal \
                                --formats print_a4 social_square \
                                --output output

Espera estas colunas no Excel (o nome exato pode ser ajustado em COLUMN_MAP abaixo,
para casares com o Excel real do cliente sem mexer no resto do código):
    Codigo interno | Codigo de barras | Descricao | Preco | Preco promocao | Desconto
"""

from __future__ import annotations
import argparse
import os
import sys
import pandas as pd

from templates import TEMPLATES, OUTPUT_FORMATS
from compose import Product, generate_poster

# Ajusta aqui se os nomes das colunas no Excel do cliente forem diferentes.
COLUMN_MAP = {
    "codigo_interno": "Codigo",
    "codigo_barras": "Codigo de barras",
    "descricao": "Descricão",
    "preco": "Preco",
    "preco_promocao": "Preco promocao",
    "desconto": "Desconto",
}

PHOTO_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]


def find_photo(photos_dir: str, barcode: str) -> str | None:
    for ext in PHOTO_EXTENSIONS:
        candidate = os.path.join(photos_dir, f"{barcode}{ext}")
        if os.path.exists(candidate):
            return candidate
    return None


def load_products(excel_path: str, photos_dir: str) -> tuple[list[Product], list[dict]]:
    """Lê o Excel e devolve (produtos_válidos, avisos). Nunca rebenta por causa de
    uma linha malformada — regista o aviso e segue para a próxima."""
    df = pd.read_excel(excel_path)
    products, warnings = [], []

    for idx, row in df.iterrows():
        line_no = idx + 2  # +2: cabeçalho + índice 0-based do Excel
        try:
            codigo_interno = str(row[COLUMN_MAP["codigo_interno"]]).strip()
            barcode = str(row[COLUMN_MAP["codigo_barras"]]).strip()
            # normaliza código de barras vindo do Excel como float (ex: 5601234567890.0)
            if barcode.endswith(".0"):
                barcode = barcode[:-2]
            descricao = str(row[COLUMN_MAP["descricao"]]).strip()
            preco = float(row[COLUMN_MAP["preco"]])
        except Exception as e:
            warnings.append({"linha": line_no, "codigo_interno": "?", "aviso": f"Linha inválida/incompleta: {e}"})
            continue

        preco_promocao = row.get(COLUMN_MAP["preco_promocao"])
        preco_promocao = float(preco_promocao) if pd.notna(preco_promocao) else None

        desconto = row.get(COLUMN_MAP["desconto"])
        desconto_pct = int(round(float(desconto))) if pd.notna(desconto) else None

        photo_path = find_photo(photos_dir, barcode)

        # --- validações não-bloqueantes: geram o poster na mesma, mas ficam no relatório ---
        if not descricao or descricao.lower() == "nan":
            warnings.append({"linha": line_no, "codigo_interno": codigo_interno, "aviso": "Descrição em falta"})
        if preco <= 0:
            warnings.append({"linha": line_no, "codigo_interno": codigo_interno, "aviso": f"Preço inválido: {preco}"})
        if preco_promocao is not None and preco_promocao >= preco:
            warnings.append({"linha": line_no, "codigo_interno": codigo_interno,
                              "aviso": f"Preço promocional ({preco_promocao}) não é inferior ao preço original ({preco})"})
        if photo_path is None:
            warnings.append({"linha": line_no, "codigo_interno": codigo_interno,
                              "aviso": f"Sem foto encontrada para o código de barras {barcode}"})
        if desconto_pct is not None and preco_promocao is not None:
            calc = round((1 - preco_promocao / preco) * 100)
            if abs(calc - desconto_pct) > 2:  # tolerância de arredondamento
                warnings.append({"linha": line_no, "codigo_interno": codigo_interno,
                                  "aviso": f"Desconto indicado ({desconto_pct}%) não bate com o calculado ({calc}%)"})

        products.append(Product(
            codigo_interno=codigo_interno,
            codigo_barras=barcode,
            descricao=descricao,
            preco=preco,
            preco_promocao=preco_promocao,
            desconto_pct=desconto_pct,
            photo_path=photo_path,
        ))

    return products, warnings


def main():
    parser = argparse.ArgumentParser(description="Gera posters de promoção em lote.")
    parser.add_argument("--excel", required=True, help="Caminho para o Excel de produtos")
    parser.add_argument("--photos", required=True, help="Pasta com as fotos (nome = código de barras)")
    parser.add_argument("--template", default="generico", choices=TEMPLATES.keys())
    parser.add_argument("--formats", nargs="+", default=["social_square"], choices=OUTPUT_FORMATS.keys())
    parser.add_argument("--output", default="output", help="Pasta de saída")
    args = parser.parse_args()

    products, warnings = load_products(args.excel, args.photos)
    print(f"{len(products)} produtos carregados. {len(warnings)} avisos.")

    for fmt in args.formats:
        out_dir = os.path.join(args.output, fmt)
        os.makedirs(out_dir, exist_ok=True)
        for product in products:
            poster = generate_poster(product, args.template, fmt)
            filename = f"{product.codigo_interno}_{product.codigo_barras}.png"
            poster.save(os.path.join(out_dir, filename))
        print(f"  -> {len(products)} posters gerados em: {out_dir}")

    if warnings:
        report_path = os.path.join(args.output, "avisos.csv")
        pd.DataFrame(warnings).to_csv(report_path, index=False)
        print(f"Relatório de avisos (não-bloqueante, para reveres com o cliente): {report_path}")

    return 0 if not any("inválida" in w["aviso"] for w in warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
