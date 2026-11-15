import unittest
from unittest.mock import MagicMock

from accidentadata.data_sources.socrata_client import SocrataError
from accidentadata.processing.service import (
    calculate_stats,
    fetch_processed_sample,
    process_records,
)


class ProcessingServiceTests(unittest.TestCase):
    def test_calculate_stats_for_runt(self):
        cleaned = [
            {
                "fecha_accidente": "2026-09",
                "departamento": "ANTIOQUIA",
                "municipio": "MEDELLIN",
                "cantidad_vehiculos": 1,
            },
            {
                "fecha_accidente": "",
                "departamento": "NO REPORTADO",
                "municipio": "MEDELLIN",
                "cantidad_vehiculos": 1,
            },
        ]
        stats = calculate_stats("runt_vehicles", cleaned)

        self.assertEqual(stats.total_records, 2)
        self.assertEqual(stats.total_metric, 2)
        self.assertEqual(stats.metric_label, "Vehículos involucrados")
        self.assertEqual(stats.valid_dates_count, 1)
        self.assertEqual(stats.complete_geo_count, 1)
        self.assertGreater(stats.missing_values_handled, 0)

    def test_calculate_stats_for_fatalities(self):
        cleaned = [
            {"fecha_hecho": "2014-02-15", "departamento": "CAUCA", "municipio": "CALI", "cantidad": 2},
            {"fecha_hecho": "2014-02-16", "departamento": "CAUCA", "municipio": "POPAYAN", "cantidad": 3},
        ]
        stats = calculate_stats("police_fatalities", cleaned)

        self.assertEqual(stats.total_records, 2)
        self.assertEqual(stats.total_metric, 5)  # Suma de víctimas: 2 + 3 = 5
        self.assertEqual(stats.metric_label, "Víctimas reportadas")
        self.assertEqual(stats.valid_dates_count, 2)
        self.assertEqual(stats.complete_geo_count, 2)

    def test_process_records_creates_rows_and_columns(self):
        raw_records = [
            {
                "fecha_hecho": "2026-09-30T00:00:00.000",
                "cod_depto": "76",
                "departamento": "valle del cauca",
                "cod_muni": "76001",
                "municipio": "cali",
                "cantidad": "1",
            }
        ]
        res = process_records("police_injuries", raw_records)

        self.assertEqual(len(res.records), 1)
        self.assertIn("municipio", res.columns)
        self.assertEqual(res.records[0]["municipio"], "CALI")
        self.assertEqual(len(res.table_rows), 1)
        self.assertEqual(res.stats.total_metric, 1)
        self.assertFalse(res.is_empty)

    def test_process_records_empty_input(self):
        res = process_records("runt_vehicles", [])
        self.assertTrue(res.is_empty)
        self.assertEqual(res.records, [])
        self.assertEqual(res.columns, [])
        self.assertEqual(res.stats.total_records, 0)

    def test_fetch_processed_sample_success(self):
        client = MagicMock()
        client.fetch.return_value = [
            {"marca_vehiculo": "MAZDA", "modelo_vehiculo": "2020", "fecha_accidente": "08/2024"}
        ]
        res = fetch_processed_sample("runt_vehicles", limit=5, client=client)

        client.fetch.assert_called_once_with("6jmc-vaxk", limit=5)
        self.assertEqual(len(res.records), 1)
        self.assertEqual(res.records[0]["marca_vehiculo"], "MAZDA")
        self.assertEqual(res.stats.total_records, 1)
        self.assertEqual(res.error, "")

    def test_fetch_processed_sample_api_error(self):
        client = MagicMock()
        client.fetch.side_effect = SocrataError("Error de conexion")

        res = fetch_processed_sample("runt_vehicles", client=client)
        self.assertEqual(res.error, "Error de conexion")
        self.assertEqual(res.records, [])
        self.assertFalse(res.is_empty)


if __name__ == "__main__":
    unittest.main()
