"""Coordenadas geográficas de los departamentos de Colombia y helpers para mapas y visualización."""

import json

# Coordenadas centroides de los 33 departamentos oficiales de Colombia (DANE DIVIPOLA)
DEPARTMENTS_COORDS = {
    "ANTIOQUIA": {"lat": 6.2442, "lng": -75.5812, "code": "05", "name": "Antioquia"},
    "ATLANTICO": {"lat": 10.9685, "lng": -74.7813, "code": "08", "name": "Atlántico"},
    "BOGOTA D.C.": {"lat": 4.7110, "lng": -74.0721, "code": "11", "name": "Bogotá D.C."},
    "BOGOTA": {"lat": 4.7110, "lng": -74.0721, "code": "11", "name": "Bogotá D.C."},
    "BOLIVAR": {"lat": 9.4206, "lng": -75.1221, "code": "13", "name": "Bolívar"},
    "BOYACA": {"lat": 5.5353, "lng": -73.3678, "code": "15", "name": "Boyacá"},
    "CALDAS": {"lat": 5.0689, "lng": -75.5174, "code": "17", "name": "Caldas"},
    "CAQUETA": {"lat": 0.8698, "lng": -73.8419, "code": "18", "name": "Caquetá"},
    "CAUCA": {"lat": 2.4448, "lng": -76.6147, "code": "19", "name": "Cauca"},
    "CESAR": {"lat": 9.3373, "lng": -73.6536, "code": "20", "name": "Cesar"},
    "CORDOBA": {"lat": 8.7479, "lng": -75.8814, "code": "23", "name": "Córdoba"},
    "CUNDINAMARCA": {"lat": 4.8143, "lng": -74.3541, "code": "25", "name": "Cundinamarca"},
    "CHOCO": {"lat": 5.6919, "lng": -76.6583, "code": "27", "name": "Chocó"},
    "HUILA": {"lat": 2.9273, "lng": -75.2819, "code": "41", "name": "Huila"},
    "LA GUAJIRA": {"lat": 11.5444, "lng": -72.9072, "code": "44", "name": "La Guajira"},
    "MAGDALENA": {"lat": 10.4631, "lng": -74.4057, "code": "47", "name": "Magdalena"},
    "META": {"lat": 3.7500, "lng": -73.2500, "code": "50", "name": "Meta"},
    "NARINO": {"lat": 1.2891, "lng": -77.3579, "code": "52", "name": "Nariño"},
    "NORTE DE SANTANDER": {"lat": 7.8939, "lng": -72.5078, "code": "54", "name": "Norte de Santander"},
    "QUINDIO": {"lat": 4.4610, "lng": -75.6674, "code": "63", "name": "Quindío"},
    "RISARALDA": {"lat": 4.8133, "lng": -75.6961, "code": "66", "name": "Risaralda"},
    "SANTANDER": {"lat": 7.1254, "lng": -73.1198, "code": "68", "name": "Santander"},
    "SUCRE": {"lat": 9.3047, "lng": -75.3978, "code": "70", "name": "Sucre"},
    "TOLIMA": {"lat": 4.4389, "lng": -75.2322, "code": "73", "name": "Tolima"},
    "VALLE DEL CAUCA": {"lat": 3.4516, "lng": -76.5320, "code": "76", "name": "Valle del Cauca"},
    "VALLE": {"lat": 3.4516, "lng": -76.5320, "code": "76", "name": "Valle del Cauca"},
    "ARAUCA": {"lat": 7.0847, "lng": -70.7591, "code": "81", "name": "Arauca"},
    "CASANARE": {"lat": 5.3378, "lng": -72.3959, "code": "85", "name": "Casanare"},
    "PUTUMAYO": {"lat": 0.5144, "lng": -76.5011, "code": "86", "name": "Putumayo"},
    "SAN ANDRES Y PROVIDENCIA": {"lat": 12.5847, "lng": -81.7006, "code": "88", "name": "San Andrés y Providencia"},
    "AMAZONAS": {"lat": -1.4429, "lng": -71.5724, "code": "91", "name": "Amazonas"},
    "GUAINIA": {"lat": 2.5859, "lng": -68.5247, "code": "94", "name": "Guainía"},
    "GUAVIARE": {"lat": 1.8540, "lng": -72.3959, "code": "95", "name": "Guaviare"},
    "VAUPES": {"lat": 0.8554, "lng": -70.8120, "code": "97", "name": "Vaupés"},
    "VICHADA": {"lat": 4.4235, "lng": -69.2878, "code": "99", "name": "Vichada"},
}


def build_map_and_charts_payload(stats_summary, dataset_key):
    """Construye un payload JSON serializable para Leaflet y Chart.js."""
    if not stats_summary or stats_summary.is_empty:
        return {
            "has_data": False,
            "departments": [],
            "breakdown_chart": None,
            "unit": stats_summary.unit_label if stats_summary else "Registros",
        }

    dept_items = []
    other_breakdown = None

    for bg in stats_summary.breakdowns:
        if bg.key == "departamento":
            for item in bg.items:
                norm_label = item.label.upper().strip()
                coords = DEPARTMENTS_COORDS.get(norm_label)
                if not coords:
                    for k, v in DEPARTMENTS_COORDS.items():
                        if k in norm_label or norm_label in k:
                            coords = v
                            break

                dept_items.append({
                    "name": coords["name"] if coords else item.label,
                    "raw_name": item.label,
                    "code": coords["code"] if coords else "",
                    "lat": coords["lat"] if coords else 4.5708,
                    "lng": coords["lng"] if coords else -74.2973,
                    "count": item.count,
                    "percentage": item.percentage,
                    "unit": bg.unit,
                })
        elif other_breakdown is None and bg.key != "departamento":
            other_breakdown = {
                "title": bg.title,
                "unit": bg.unit,
                "labels": [it.label for it in bg.items[:7]],
                "counts": [it.count for it in bg.items[:7]],
                "percentages": [it.percentage for it in bg.items[:7]],
            }

    return {
        "has_data": True,
        "dataset_key": dataset_key,
        "unit": stats_summary.unit_label,
        "total_metric": stats_summary.total_metric,
        "total_records": stats_summary.total_records,
        "departments": dept_items,
        "other_breakdown": other_breakdown,
    }
