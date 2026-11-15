"""Configuración de los filtros de búsqueda por fuente.

Los valores de departamento, gravedad, tipo de vehículo, género y grupo etario
se verificaron contra los valores reales de la API de datos.gov.co el 14 de
noviembre de 2026. Cada fuente escribe los departamentos de forma distinta
(tildes, "VALLE" frente a "VALLE DEL CAUCA"), por eso el usuario elige un
departamento de una lista común y la búsqueda usa la escritura de cada fuente.
"""

import unicodedata

# Código DANE de departamento -> nombre para mostrar.
DEPARTMENTS = {
    "05": "Antioquia",
    "08": "Atlántico",
    "11": "Bogotá D.C.",
    "13": "Bolívar",
    "15": "Boyacá",
    "17": "Caldas",
    "18": "Caquetá",
    "19": "Cauca",
    "20": "Cesar",
    "23": "Córdoba",
    "25": "Cundinamarca",
    "27": "Chocó",
    "41": "Huila",
    "44": "La Guajira",
    "47": "Magdalena",
    "50": "Meta",
    "52": "Nariño",
    "54": "Norte de Santander",
    "63": "Quindío",
    "66": "Risaralda",
    "68": "Santander",
    "70": "Sucre",
    "73": "Tolima",
    "76": "Valle del Cauca",
    "81": "Arauca",
    "85": "Casanare",
    "86": "Putumayo",
    "88": "San Andrés y Providencia",
    "91": "Amazonas",
    "94": "Guainía",
    "95": "Guaviare",
    "97": "Vaupés",
    "99": "Vichada",
}


def strip_accents(text):
    """Quita tildes y diéresis; la ñ también pierde su virgulilla (Ñ -> N)."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


SEARCH_CONFIG = {
    "runt_vehicles": {
        "department_field": "departamento_accidente",
        "municipality_field": "municipio_accidente",
        "date_field": "fecha_accidente",
        "date_format": "month_year",  # MM/AAAA como texto
        "years": (2022, 2026),
        "metric_label": "Vehículos involucrados",
        "metric_field": None,
        # Escritura de la fuente cuando no coincide con el nombre sin tildes.
        "department_names": {
            "11": "BOGOTA D.C.",
            "88": "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA",
        },
        "extra_filters": {
            "gravedad_accidente": {
                "label": "Gravedad",
                "choices": ["CON HERIDOS", "CON MUERTOS"],
            },
            "tipo_vehiculo": {
                "label": "Tipo de vehículo",
                "choices": [
                    "MOTOCICLETA",
                    "AUTOMOVIL",
                    "CAMIONETA",
                    "BUS",
                    "CAMION",
                    "CAMPERO",
                    "TRACTOCAMION",
                    "MICROBUS",
                    "BUSETA",
                    "VOLQUETA",
                    "MOTOCARRO",
                ],
            },
        },
    },
    "police_fatalities": {
        "department_field": "departamento",
        "municipality_field": "municipio",
        "date_field": "fecha_hecho",
        "date_format": "day_month_year",  # DD/MM/AAAA como texto
        "years": (2010, 2026),
        "metric_label": "Víctimas",
        "metric_field": "cantidad",
        "department_names": {
            "08": "ATLÁNTICO",
            "11": "BOGOTA",
            "13": "BOLÍVAR",
            "15": "BOYACÁ",
            "18": "CAQUETÁ",
            "23": "CÓRDOBA",
            "27": "CHOCÓ",
            "44": "GUAJIRA",
            "52": "NARIÑO",
            "63": "QUINDÍO",
            "76": "VALLE",
            "88": "SAN ANDRÉS",
            "94": "GUAINÍA",
            "97": "VAUPÉS",
        },
        "extra_filters": {
            "genero": {
                "label": "Género",
                "choices": ["MASCULINO", "FEMENINO"],
            },
            "grupo_etar_o": {
                "label": "Grupo de edad",
                "choices": ["ADULTOS", "ADOLESCENTES", "MENORES"],
            },
        },
    },
    "police_injuries": {
        "department_field": "departamento",
        "municipality_field": "municipio",
        "date_field": "fecha_hecho",
        "date_format": "iso",  # Campo de fecha real
        "years": (2003, 2026),
        "metric_label": "Víctimas",
        "metric_field": "cantidad",
        "department_names": {
            "11": "BOGOTA D.C.",
            "52": "NARIÑO",
            "88": "SAN ANDRES ISLAS",
        },
        "extra_filters": {},
    },
}


def department_value(dataset_key, code):
    """Devuelve el nombre del departamento tal como lo escribe la fuente."""
    config = SEARCH_CONFIG[dataset_key]
    if code in config["department_names"]:
        return config["department_names"][code]
    return strip_accents(DEPARTMENTS[code]).upper()


def year_choices(dataset_key):
    first, last = SEARCH_CONFIG[dataset_key]["years"]
    return list(range(last, first - 1, -1))
