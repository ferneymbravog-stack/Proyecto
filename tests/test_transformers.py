import unittest

from accidentadata.processing.transformers import (
    clean_record,
    clean_records,
    transform_police_fatality,
    transform_police_injury,
    transform_runt_vehicle,
)


class TransformersTests(unittest.TestCase):
    def test_transform_runt_vehicle_normalizes_fields(self):
        raw = {
            "marca_vehiculo": "  volkswagen ",
            "modelo_vehiculo": "2018",
            "tipo_vehiculo": "camion",
            "edad_vehiculo": "7",
            "fecha_accidente": "09/2026",
            "gravedad_accidente": "con heridos",
            "departamento_accidente": "antioquia",
            "municipio_accidente": "medellin",
            "autoridad_de_transito": "direccion de transito",
        }
        transformed = transform_runt_vehicle(raw)

        self.assertEqual(transformed["marca_vehiculo"], "VOLKSWAGEN")
        self.assertEqual(transformed["modelo_vehiculo"], 2018)
        self.assertEqual(transformed["tipo_vehiculo"], "CAMION")
        self.assertEqual(transformed["edad_vehiculo"], 7)
        self.assertEqual(transformed["fecha_accidente"], "2026-09")
        self.assertEqual(transformed["anio"], 2026)
        self.assertEqual(transformed["mes"], 9)
        self.assertEqual(transformed["gravedad_accidente"], "CON HERIDOS")
        self.assertEqual(transformed["departamento"], "ANTIOQUIA")
        self.assertEqual(transformed["municipio"], "MEDELLIN")
        self.assertEqual(transformed["cantidad_vehiculos"], 1)

    def test_transform_runt_vehicle_handles_nulls_and_computes_age(self):
        raw = {
            "marca_vehiculo": "SIN INFORMACION",
            "modelo_vehiculo": "2020",
            "tipo_vehiculo": "",
            "edad_vehiculo": "-1",  # Inválido
            "fecha_accidente": "05/2024",
            "departamento_accidente": None,
            "municipio_accidente": None,
        }
        transformed = transform_runt_vehicle(raw)

        self.assertEqual(transformed["marca_vehiculo"], "NO REPORTADO")
        self.assertEqual(transformed["tipo_vehiculo"], "NO REPORTADO")
        self.assertEqual(transformed["departamento"], "NO REPORTADO")
        self.assertEqual(transformed["municipio"], "NO REPORTADO")
        # 2024 - 2020 = 4 años calculados de forma predecible
        self.assertEqual(transformed["edad_vehiculo"], 4)

    def test_transform_police_fatality_normalizes_fields(self):
        raw = {
            "departamento": "cauca",
            "municipio": "Santander de Quilichao (CT)",
            "codigo_dane": "19698000",
            "armas_medios": "NO REPORTADO",
            "fecha_hecho": "15/02/2014",
            "genero": "masculino",
            "grupo_etar_o": "menores",
            "descripci_n_conducta": "ARTÍCULO 109. HOMICIDIO CULPOSO",
            "cantidad": "2",
        }
        transformed = transform_police_fatality(raw)

        self.assertEqual(transformed["departamento"], "CAUCA")
        self.assertEqual(transformed["municipio"], "SANTANDER DE QUILICHAO")
        self.assertEqual(transformed["cod_depto"], "19")
        self.assertEqual(transformed["cod_muni"], "19698")
        self.assertEqual(transformed["fecha_hecho"], "2014-02-15")
        self.assertEqual(transformed["anio"], 2014)
        self.assertEqual(transformed["mes"], 2)
        self.assertEqual(transformed["dia"], 15)
        self.assertEqual(transformed["genero"], "MASCULINO")
        self.assertEqual(transformed["grupo_etario"], "MENORES")
        self.assertEqual(transformed["cantidad"], 2)

    def test_transform_police_fatality_handles_invalid_cantidad(self):
        raw = {
            "departamento": "CALDAS",
            "cantidad": "invalido",
        }
        transformed = transform_police_fatality(raw)
        self.assertEqual(transformed["cantidad"], 1)

    def test_transform_police_injury_normalizes_fields(self):
        raw = {
            "fecha_hecho": "2026-09-30T00:00:00.000",
            "cod_depto": "76",
            "departamento": "valle del cauca",
            "cod_muni": "76001",
            "municipio": "cali",
            "cantidad": "3",
        }
        transformed = transform_police_injury(raw)

        self.assertEqual(transformed["fecha_hecho"], "2026-09-30")
        self.assertEqual(transformed["anio"], 2026)
        self.assertEqual(transformed["mes"], 9)
        self.assertEqual(transformed["dia"], 30)
        self.assertEqual(transformed["cod_depto"], "76")
        self.assertEqual(transformed["departamento"], "VALLE DEL CAUCA")
        self.assertEqual(transformed["cod_muni"], "76001")
        self.assertEqual(transformed["municipio"], "CALI")
        self.assertEqual(transformed["cantidad"], 3)

    def test_clean_record_handles_non_dict(self):
        self.assertIsNone(clean_record("runt_vehicles", "no_dict"))
        self.assertIsNone(clean_record("runt_vehicles", None))
        self.assertIsNone(clean_record("runt_vehicles", 123))

    def test_clean_records_skips_invalid_items(self):
        records = [
            "invalido",
            {"marca_vehiculo": "CHEVROLET"},
            None,
            {"marca_vehiculo": "MAZDA"},
        ]
        cleaned = clean_records("runt_vehicles", records)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned[0]["marca_vehiculo"], "CHEVROLET")
        self.assertEqual(cleaned[1]["marca_vehiculo"], "MAZDA")


if __name__ == "__main__":
    unittest.main()
