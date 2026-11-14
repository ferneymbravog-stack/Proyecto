"""Catálogo de fuentes nacionales de datos abiertos usadas por AccidentaData.

Los metadatos se verificaron el 13 de noviembre de 2026 en la ficha oficial de
cada conjunto en datos.gov.co (endpoint /api/views/{dataset_id}.json).
"""

DATASETS = {
    "runt_vehicles": {
        "name": "Vehículos involucrados en un accidente de tránsito - Ley 2251 de 2022",
        "dataset_id": "6jmc-vaxk",
        "publisher": "Ministerio de Transporte (RUNT)",
        "purpose": "Vehículos involucrados en siniestros con resultado de muerte o lesión.",
        "coverage": "Nacional; siniestros entre enero de 2022 y septiembre de 2026",
        "frequency": "Semestral",
        "license": "CC BY-SA 4.0",
        "count_unit": "Cada fila es un vehículo involucrado, no un siniestro.",
        "count_field": None,
        "fields": [
            "marca_vehiculo",
            "modelo_vehiculo",
            "tipo_vehiculo",
            "edad_vehiculo",
            "fecha_accidente",
            "gravedad_accidente",
            "departamento_accidente",
            "municipio_accidente",
            "autoridad_de_transito",
        ],
        "limitations": [
            "La fecha solo trae mes y año, como texto con formato MM/AAAA.",
            "La gravedad solo distingue entre 'CON HERIDOS' y 'CON MUERTOS'.",
            "No incluye coordenadas ni código DANE del municipio.",
        ],
        "source_url": "https://www.datos.gov.co/d/6jmc-vaxk",
    },
    "police_fatalities": {
        "name": "Homicidios en accidente de tránsito - Policía Nacional",
        "dataset_id": "ha6j-pa2r",
        "publisher": "Dirección General de la Policía Nacional (DIJIN)",
        "purpose": "Muertes por homicidio culposo en accidentes de tránsito.",
        "coverage": "Nacional; hechos entre enero de 2010 y julio de 2026",
        "frequency": "Trimestral",
        "license": "CC BY-SA 4.0",
        "count_unit": "Cada fila agrupa casos; el total de víctimas se obtiene sumando 'cantidad'.",
        "count_field": "cantidad",
        "fields": [
            "departamento",
            "municipio",
            "codigo_dane",
            "armas_medios",
            "fecha_hecho",
            "genero",
            "grupo_etar_o",
            "descripci_n_conducta",
            "cantidad",
        ],
        "limitations": [
            "La fecha es texto con formato DD/MM/AAAA, no un campo de fecha.",
            "El campo 'cantidad' se publica como texto.",
            "La entidad advierte que las cifras están sujetas a variación.",
        ],
        "source_url": "https://www.datos.gov.co/d/ha6j-pa2r",
    },
    "police_injuries": {
        "name": "Lesiones en accidentes de tránsito",
        "dataset_id": "ntej-qq7v",
        "publisher": "Ministerio de Defensa Nacional",
        "purpose": "Víctimas de lesiones personales en accidentes de tránsito.",
        "coverage": "Nacional; hechos entre enero de 2003 y septiembre de 2026",
        "frequency": "Mensual",
        "license": "CC BY-SA 4.0",
        "count_unit": "Se mide en víctimas; el total se obtiene sumando 'cantidad', no contando filas.",
        "count_field": "cantidad",
        "fields": [
            "fecha_hecho",
            "cod_depto",
            "departamento",
            "cod_muni",
            "municipio",
            "cantidad",
        ],
        "limitations": [
            "Solo informa lugar, fecha y número de víctimas; no describe el siniestro.",
            "No incluye coordenadas; la ubicación llega hasta municipio.",
        ],
        "source_url": "https://www.datos.gov.co/d/ntej-qq7v",
    },
}
