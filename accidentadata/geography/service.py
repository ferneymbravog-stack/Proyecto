
from collections import defaultdict

from accidentadata.processing.cleaners import clean_dane_code


def build_municipality_summary(records):
    """Agrupa víctimas por municipio usando el código DANE."""

    municipalities = defaultdict(lambda: {
        "codigo_dane": "",
        "municipio": "NO REPORTADO",
        "departamento": "NO REPORTADO",
        "total": 0,
    })

    without_location = 0

    for record in records:
        raw_code = (
            record.get("cod_muni")
            or record.get("codigo_dane")
            or record.get("codigo_dane_original")
        )

        code = clean_dane_code(raw_code, expected_digits=5)

        municipality = str(
            record.get("municipio") or "NO REPORTADO"
        ).strip()

        department = str(
            record.get("departamento") or "NO REPORTADO"
        ).strip()

        if not code or municipality == "NO REPORTADO":
            without_location += 1
            continue

        item = municipalities[code]

        item["codigo_dane"] = code
        item["municipio"] = municipality
        item["departamento"] = department

        try:
            cantidad = int(record.get("cantidad", 1) or 0)
        except (TypeError, ValueError):
            cantidad = 0

        item["total"] += cantidad

    return {
        "municipalities": sorted(
            municipalities.values(),
            key=lambda item: item["total"],
            reverse=True,
        ),
        "without_location": without_location,
    }