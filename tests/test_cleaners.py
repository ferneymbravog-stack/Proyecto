import unittest

from accidentadata.processing.cleaners import (
    clean_dane_code,
    clean_date_str,
    clean_int,
    clean_name,
    clean_text,
    extract_date_parts,
)


class CleanersTests(unittest.TestCase):
    def test_clean_text_strips_and_collapses_whitespace(self):
        self.assertEqual(clean_text("  Bogota   D.C.  "), "Bogota D.C.")
        self.assertEqual(clean_text("Medellín"), "Medellín")

    def test_clean_text_identifies_null_representations(self):
        for null_val in ["", "   ", "null", "None", "NAN", "N/A", "Sin Información", "No Reportado", "-"]:
            with self.subTest(null_val=null_val):
                self.assertEqual(clean_text(null_val, default="DEFAULT"), "DEFAULT")

    def test_clean_name_converts_to_uppercase_and_removes_ct_suffix(self):
        self.assertEqual(clean_name("Riohacha (CT)"), "RIOHACHA")
        self.assertEqual(clean_name("  cajibío  "), "CAJIBÍO")
        self.assertEqual(clean_name("Santander de Quilichao (ct)"), "SANTANDER DE QUILICHAO")
        self.assertEqual(clean_name(None, default="NO REPORTADO"), "NO REPORTADO")

    def test_clean_int_parses_valid_integers_and_strings(self):
        self.assertEqual(clean_int(2024), 2024)
        self.assertEqual(clean_int("2024"), 2024)
        self.assertEqual(clean_int("  15 "), 15)
        self.assertEqual(clean_int("2020.0"), 2020)

    def test_clean_int_handles_invalid_and_bounds(self):
        self.assertIsNone(clean_int("no_numero"))
        self.assertIsNone(clean_int(None))
        self.assertEqual(clean_int("sin dato", default=0), 0)
        self.assertIsNone(clean_int(-5, min_val=0))
        self.assertEqual(clean_int(-1, default=0, min_val=0), 0)
        self.assertIsNone(clean_int(2050, max_val=2030))

    def test_clean_date_str_parses_all_three_supported_formats(self):
        # Formato RUNT: MM/AAAA
        self.assertEqual(clean_date_str("09/2026"), "2026-09")
        self.assertEqual(clean_date_str("5/2023"), "2023-05")

        # Formato Homicidios: DD/MM/AAAA
        self.assertEqual(clean_date_str("13/02/2014"), "2014-02-13")
        self.assertEqual(clean_date_str("1/5/2020"), "2020-05-01")

        # Formato Lesiones: ISO datetime
        self.assertEqual(clean_date_str("2026-09-30T00:00:00.000"), "2026-09-30")
        self.assertEqual(clean_date_str("2024-11-14"), "2024-11-14")

    def test_clean_date_str_rejects_invalid_dates(self):
        self.assertIsNone(clean_date_str("32/01/2024"))
        self.assertIsNone(clean_date_str("15/13/2024"))
        self.assertIsNone(clean_date_str("fecha_invalida"))
        self.assertIsNone(clean_date_str(""))
        self.assertIsNone(clean_date_str(None))

    def test_extract_date_parts(self):
        self.assertEqual(
            extract_date_parts("2026-09-30"),
            {"anio": 2026, "mes": 9, "dia": 30},
        )
        self.assertEqual(
            extract_date_parts("2026-09"),
            {"anio": 2026, "mes": 9, "dia": None},
        )
        self.assertEqual(
            extract_date_parts(None),
            {"anio": None, "mes": None, "dia": None},
        )

    def test_clean_dane_code_pads_and_extracts_subdivisions(self):
        # Código de 8 dígitos de homicidios (19130000 -> Cauca / Cajibío)
        self.assertEqual(clean_dane_code("19130000", expected_digits=2), "19")
        self.assertEqual(clean_dane_code("19130000", expected_digits=5), "19130")

        # Código de lesiones
        self.assertEqual(clean_dane_code("76", expected_digits=2), "76")
        self.assertEqual(clean_dane_code(5, expected_digits=2), "05")
        self.assertEqual(clean_dane_code("76001", expected_digits=5), "76001")
        self.assertEqual(clean_dane_code(5001, expected_digits=5), "05001")

        # Inválidos o nulos
        self.assertEqual(clean_dane_code(None), "")
        self.assertEqual(clean_dane_code("sin_codigo"), "")


if __name__ == "__main__":
    unittest.main()
