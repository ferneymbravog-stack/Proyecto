import unittest

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.processing.service import process_records
from accidentadata.processing.statistics import build_statistical_summary


class StatisticalSummaryTests(unittest.TestCase):
    def test_runt_vehicles_summary_matches_real_records(self):
        raw = [
            {
                "marca_vehiculo": "MAZDA",
                "modelo_vehiculo": "2020",
                "tipo_vehiculo": "AUTOMOVIL",
                "edad_vehiculo": "4",
                "fecha_accidente": "08/2024",
                "gravedad_accidente": "CON HERIDOS",
                "departamento_accidente": "ANTIOQUIA",
                "municipio_accidente": "MEDELLIN",
            },
            {
                "marca_vehiculo": "YAMAHA",
                "modelo_vehiculo": "2022",
                "tipo_vehiculo": "MOTOCICLETA",
                "edad_vehiculo": "4",
                "fecha_accidente": "09/2026",
                "gravedad_accidente": "CON MUERTOS",
                "departamento_accidente": "ANTIOQUIA",
                "municipio_accidente": "ENVIGADO",
            },
            {
                "marca_vehiculo": "CHEVROLET",
                "modelo_vehiculo": "2016",
                "tipo_vehiculo": "AUTOMOVIL",
                "edad_vehiculo": "10",
                "fecha_accidente": "09/2026",
                "gravedad_accidente": "CON HERIDOS",
                "departamento_accidente": "VALLE DEL CAUCA",
                "municipio_accidente": "CALI",
            },
        ]
        processed = process_records("runt_vehicles", raw, dataset=DATASETS["runt_vehicles"])
        summary = processed.summary

        self.assertIsNotNone(summary)
        self.assertFalse(summary.is_empty)
        self.assertEqual(summary.total_records, 3)
        self.assertEqual(summary.total_metric, 3)
        self.assertEqual(summary.unit_label, "Vehículos involucrados")
        self.assertEqual(summary.avg_metric_per_record, 1.0)
        self.assertEqual(summary.period_label, "2024-08 a 2026-09")
        self.assertEqual(summary.unique_departments, 2)
        self.assertEqual(summary.unique_municipalities, 3)
        self.assertEqual(summary.avg_vehicle_age, 6.0)
        self.assertEqual(summary.vehicle_age_count, 3)
        self.assertEqual(summary.top_department.label, "ANTIOQUIA")
        self.assertEqual(summary.top_department.count, 2)
        self.assertEqual(summary.top_department.percentage, 66.7)

        breakdown_keys = [b.key for b in summary.breakdowns]
        self.assertIn("severity", breakdown_keys)
        self.assertIn("vehicle_types", breakdown_keys)
        severity = next(b for b in summary.breakdowns if b.key == "severity")
        self.assertEqual(severity.items[0].label, "CON HERIDOS")
        self.assertEqual(severity.items[0].count, 2)

    def test_police_fatalities_sums_cantidad_and_builds_demographics(self):
        raw = [
            {
                "departamento": "CAUCA",
                "municipio": "POPAYAN",
                "codigo_dane": "19001000",
                "armas_medios": "MOTO",
                "fecha_hecho": "15/02/2024",
                "genero": "MASCULINO",
                "grupo_etar_o": "ADULTOS",
                "cantidad": "3",
            },
            {
                "departamento": "CAUCA",
                "municipio": "SANTANDER DE QUILICHAO",
                "codigo_dane": "19698000",
                "armas_medios": "AUTOMOVIL",
                "fecha_hecho": "20/03/2025",
                "genero": "FEMENINO",
                "grupo_etar_o": "JOVENES",
                "cantidad": "2",
            },
        ]
        processed = process_records(
            "police_fatalities", raw, dataset=DATASETS["police_fatalities"]
        )
        summary = processed.summary

        self.assertEqual(summary.total_records, 2)
        self.assertEqual(summary.total_metric, 5)
        self.assertEqual(summary.avg_metric_per_record, 2.5)
        self.assertEqual(summary.unit_label, "Víctimas fallecidas")
        self.assertEqual(summary.period_label, "2024-02-15 a 2025-03-20")
        self.assertIsNone(summary.avg_vehicle_age)

        gender = next(b for b in summary.breakdowns if b.key == "gender")
        self.assertEqual(gender.items[0].label, "MASCULINO")
        self.assertEqual(gender.items[0].count, 3)
        self.assertEqual(gender.items[0].percentage, 60.0)

    def test_police_injuries_omits_unavailable_breakdowns(self):
        raw = [
            {
                "fecha_hecho": "2026-09-30T00:00:00.000",
                "cod_depto": "76",
                "departamento": "VALLE DEL CAUCA",
                "cod_muni": "76001",
                "municipio": "CALI",
                "cantidad": "4",
            }
        ]
        processed = process_records("police_injuries", raw, dataset=DATASETS["police_injuries"])
        summary = processed.summary

        self.assertEqual(summary.total_records, 1)
        self.assertEqual(summary.total_metric, 4)
        self.assertEqual(summary.period_label, "2026-09-30")
        breakdown_keys = [b.key for b in summary.breakdowns]
        self.assertEqual(breakdown_keys, ["departments", "municipalities", "years"])

    def test_empty_dataset_handled_gracefully(self):
        summary = build_statistical_summary(
            "police_injuries", [], dataset=DATASETS["police_injuries"]
        )
        self.assertTrue(summary.is_empty)
        self.assertEqual(summary.total_records, 0)
        self.assertEqual(summary.total_metric, 0)
        self.assertEqual(summary.avg_metric_per_record, 0.0)
        self.assertEqual(summary.breakdowns, [])
        self.assertTrue(summary.empty_message)

    def test_records_without_valid_dates_or_geo(self):
        cleaned = [
            {
                "fecha_hecho": "",
                "anio": None,
                "departamento": "NO REPORTADO",
                "municipio": "NO REPORTADO",
                "cantidad": 2,
            }
        ]
        summary = build_statistical_summary(
            "police_injuries", cleaned, dataset=DATASETS["police_injuries"]
        )
        self.assertFalse(summary.is_empty)
        self.assertEqual(summary.period_label, "Sin fechas válidas en la muestra")
        self.assertEqual(summary.unique_departments, 0)
        self.assertEqual(summary.unique_municipalities, 0)
        self.assertEqual(summary.total_metric, 2)


if __name__ == "__main__":
    unittest.main()
