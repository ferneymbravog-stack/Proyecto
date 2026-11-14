import unittest
from unittest.mock import MagicMock

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import (
    MAX_SAMPLE_SIZE,
    UnknownDatasetError,
    fetch_sample,
)
from accidentadata.data_sources.socrata_client import SocrataError


class CatalogTests(unittest.TestCase):
    def test_every_dataset_documents_origin_and_limitations(self):
        required = {
            "name", "dataset_id", "publisher", "coverage", "frequency",
            "license", "count_unit", "fields", "limitations", "source_url",
        }
        for key, dataset in DATASETS.items():
            with self.subTest(key=key):
                self.assertTrue(required <= dataset.keys())
                self.assertTrue(dataset["fields"])
                self.assertTrue(dataset["source_url"].startswith("https://www.datos.gov.co/"))


class FetchSampleTests(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()

    def test_returns_rows_in_catalog_field_order(self):
        self.client.fetch.return_value = [
            {"municipio": "CALI", "cantidad": "2", "fecha_hecho": "2026-09-30T00:00:00.000"},
        ]

        result = fetch_sample("police_injuries", limit=5, client=self.client)

        self.client.fetch.assert_called_once_with("ntej-qq7v", limit=5)
        self.assertEqual(result.columns, ["fecha_hecho", "municipio", "cantidad"])
        self.assertEqual(result.records, [["2026-09-30T00:00:00.000", "CALI", "2"]])
        self.assertEqual(result.error, "")
        self.assertFalse(result.is_empty)

    def test_missing_values_become_empty_strings(self):
        self.client.fetch.return_value = [
            {"municipio": "CALI", "cantidad": "1"},
            {"municipio": "PASTO"},
        ]

        result = fetch_sample("police_injuries", client=self.client)

        self.assertEqual(result.records, [["CALI", "1"], ["PASTO", ""]])

    def test_empty_response_is_reported_as_empty(self):
        self.client.fetch.return_value = []

        result = fetch_sample("runt_vehicles", client=self.client)

        self.assertTrue(result.is_empty)
        self.assertEqual(result.error, "")

    def test_api_error_is_returned_instead_of_raised(self):
        self.client.fetch.side_effect = SocrataError("No fue posible conectar con datos.gov.co.")

        result = fetch_sample("police_fatalities", client=self.client)

        self.assertEqual(result.error, "No fue posible conectar con datos.gov.co.")
        self.assertEqual(result.records, [])
        self.assertFalse(result.is_empty)

    def test_unknown_fields_are_shown_as_received(self):
        self.client.fetch.return_value = [{"campo_nuevo": "x"}]

        result = fetch_sample("runt_vehicles", client=self.client)

        self.assertEqual(result.columns, ["campo_nuevo"])
        self.assertEqual(result.records, [["x"]])

    def test_non_dict_records_are_ignored(self):
        self.client.fetch.return_value = ["texto", {"municipio": "CALI"}]

        result = fetch_sample("police_injuries", client=self.client)

        self.assertEqual(result.records, [["CALI"]])

    def test_limit_is_kept_within_bounds(self):
        self.client.fetch.return_value = []

        fetch_sample("runt_vehicles", limit=10_000, client=self.client)
        fetch_sample("runt_vehicles", limit=0, client=self.client)

        limits = [call.kwargs["limit"] for call in self.client.fetch.call_args_list]
        self.assertEqual(limits, [MAX_SAMPLE_SIZE, 1])

    def test_unknown_dataset_raises(self):
        with self.assertRaises(UnknownDatasetError):
            fetch_sample("no_existe", client=self.client)
        self.client.fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
