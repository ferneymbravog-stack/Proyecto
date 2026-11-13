import json
import unittest
from unittest.mock import MagicMock, patch

from accidentadata.data_sources.socrata_client import (
    SocrataClient,
    SocrataError,
)


class SocrataClientTests(unittest.TestCase):
    def setUp(self):
        self.client = SocrataClient()

    @patch("accidentadata.data_sources.socrata_client.urlopen")
    def test_fetch_returns_records(self, mocked_urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps(
            [{"departamento": "BOGOTA D.C."}]
        ).encode("utf-8")
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response

        records = self.client.fetch("ha6j-pa2r", limit=10)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["departamento"], "BOGOTA D.C.")

    def test_rejects_invalid_dataset_id(self):
        with self.assertRaises(ValueError):
            self.client.fetch("invalid")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            self.client.fetch("ha6j-pa2r", limit=0)

    def test_rejects_negative_offset(self):
        with self.assertRaises(ValueError):
            self.client.fetch("ha6j-pa2r", offset=-1)

    @patch("accidentadata.data_sources.socrata_client.urlopen")
    def test_rejects_non_list_response(self, mocked_urlopen):
        response = MagicMock()
        response.read.return_value = b'{"error": "invalid"}'
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response

        with self.assertRaises(SocrataError):
            self.client.fetch("ha6j-pa2r")


if __name__ == "__main__":
    unittest.main()
