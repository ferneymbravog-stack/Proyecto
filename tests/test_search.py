import unittest
from unittest.mock import MagicMock

from accidentadata.data_sources.socrata_client import SocrataError
from accidentadata.search.config import DEPARTMENTS, SEARCH_CONFIG, department_value
from accidentadata.search.query import (
    InvalidCriteriaError,
    SearchCriteria,
    build_where,
    count_select,
    municipality_like,
)
from accidentadata.search.service import PAGE_SIZE, search

# Valores reales de departamento publicados por cada fuente (consultados en la
# API el 14 de noviembre de 2026 con $group=departamento).
REAL_DEPARTMENT_VALUES = {
    "runt_vehicles": {
        "ANTIOQUIA", "ARAUCA", "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA", "ATLANTICO",
        "BOGOTA D.C.", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CASANARE", "CAUCA",
        "CESAR", "CHOCO", "CORDOBA", "CUNDINAMARCA", "GUAINIA", "GUAVIARE", "HUILA",
        "LA GUAJIRA", "MAGDALENA", "META", "NARINO", "NORTE DE SANTANDER", "PUTUMAYO",
        "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA",
        "VICHADA",
    },
    "police_fatalities": {
        "AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLÁNTICO", "BOGOTA", "BOLÍVAR", "BOYACÁ",
        "CALDAS", "CAQUETÁ", "CASANARE", "CAUCA", "CESAR", "CHOCÓ", "CÓRDOBA",
        "CUNDINAMARCA", "GUAINÍA", "GUAJIRA", "GUAVIARE", "HUILA", "MAGDALENA", "META",
        "NARIÑO", "NORTE DE SANTANDER", "PUTUMAYO", "QUINDÍO", "RISARALDA", "SAN ANDRÉS",
        "SANTANDER", "SUCRE", "TOLIMA", "VALLE", "VAUPÉS", "VICHADA",
    },
    "police_injuries": {
        "AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLANTICO", "BOGOTA D.C.", "BOLIVAR", "BOYACA",
        "CALDAS", "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO", "CORDOBA",
        "CUNDINAMARCA", "GUAINIA", "GUAVIARE", "HUILA", "LA GUAJIRA", "MAGDALENA", "META",
        "NARIÑO", "NORTE DE SANTANDER", "PUTUMAYO", "QUINDIO", "RISARALDA",
        "SAN ANDRES ISLAS", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "VAUPES",
        "VICHADA",
    },
}

# Departamentos sin registros en el RUNT al momento de la verificación.
RUNT_WITHOUT_DATA = {"91", "97"}


class DepartmentMappingTests(unittest.TestCase):
    def test_every_department_maps_to_a_real_source_value(self):
        for key, real_values in REAL_DEPARTMENT_VALUES.items():
            for code in DEPARTMENTS:
                if key == "runt_vehicles" and code in RUNT_WITHOUT_DATA:
                    continue
                with self.subTest(fuente=key, codigo=code):
                    self.assertIn(department_value(key, code), real_values)

    def test_every_source_has_search_config(self):
        self.assertEqual(set(SEARCH_CONFIG), set(REAL_DEPARTMENT_VALUES))


class MunicipalityPatternTests(unittest.TestCase):
    def test_ignores_case_and_accents(self):
        self.assertEqual(municipality_like("cajibío"), "C_J_B__%")
        self.assertEqual(municipality_like("CAJIBIO"), "C_J_B__%")

    def test_collapses_spaces(self):
        self.assertEqual(municipality_like("  santa   marta "), "S_NT_ M_RT_%")

    def test_rejects_invalid_characters(self):
        for value in ["x' OR 1=1", "a", "medellin%", "cali;", "1234", "a" * 41]:
            with self.subTest(value=value):
                with self.assertRaises(InvalidCriteriaError):
                    municipality_like(value)


class BuildWhereTests(unittest.TestCase):
    def test_no_filters_returns_empty_string(self):
        self.assertEqual(build_where("police_injuries", SearchCriteria()), "")

    def test_combines_filters_with_source_spelling(self):
        criteria = SearchCriteria(departamento="76", municipio="cali", anio=2024)

        where = build_where("police_fatalities", criteria)

        self.assertEqual(
            where,
            "departamento = 'VALLE' AND upper(municipio) like 'C_L_%' "
            "AND fecha_hecho like '%/2024'",
        )

    def test_year_on_iso_date_uses_range(self):
        where = build_where("police_injuries", SearchCriteria(anio=2003))

        self.assertEqual(
            where,
            "fecha_hecho between '2003-01-01T00:00:00' and '2003-12-31T23:59:59'",
        )

    def test_runt_uses_its_own_fields(self):
        criteria = SearchCriteria(
            departamento="52",
            extras={"gravedad_accidente": "CON MUERTOS", "tipo_vehiculo": ""},
        )

        where = build_where("runt_vehicles", criteria)

        self.assertEqual(
            where,
            "departamento_accidente = 'NARINO' AND gravedad_accidente = 'CON MUERTOS'",
        )

    def test_rejects_unknown_department(self):
        with self.assertRaises(InvalidCriteriaError):
            build_where("runt_vehicles", SearchCriteria(departamento="00"))

    def test_rejects_year_out_of_source_range(self):
        with self.assertRaises(InvalidCriteriaError):
            build_where("runt_vehicles", SearchCriteria(anio=2021))

    def test_rejects_value_outside_choices(self):
        with self.assertRaises(InvalidCriteriaError):
            build_where("police_fatalities", SearchCriteria(extras={"genero": "X' OR '1'='1"}))

    def test_rejects_filter_from_another_source(self):
        with self.assertRaises(InvalidCriteriaError):
            build_where("police_injuries", SearchCriteria(extras={"genero": "MASCULINO"}))

    def test_count_select_sums_metric_as_number(self):
        self.assertEqual(
            count_select("police_fatalities"),
            "count(*) as filas, sum(cantidad::number) as total",
        )
        self.assertEqual(count_select("runt_vehicles"), "count(*) as filas")


class SearchServiceTests(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()

    def test_counts_all_matches_and_fetches_requested_page(self):
        self.client.fetch.side_effect = [
            [{"filas": "45", "total": "52"}],
            [{"fecha_hecho": "2024-03-01T00:00:00.000", "municipio": "CALI", "cantidad": "2"}],
        ]
        criteria = SearchCriteria(departamento="76")

        result = search("police_injuries", criteria, page=2, client=self.client)

        count_call, page_call = self.client.fetch.call_args_list
        self.assertEqual(count_call.kwargs["filters"]["$where"], "departamento = 'VALLE DEL CAUCA'")
        self.assertEqual(page_call.kwargs["offset"], PAGE_SIZE)
        self.assertEqual(page_call.kwargs["limit"], PAGE_SIZE)
        self.assertEqual(page_call.kwargs["filters"]["$order"], ":id")
        self.assertEqual(result.total_rows, 45)
        self.assertEqual(result.metric_total, 52)
        self.assertEqual(result.pages, 3)
        self.assertEqual(result.page, 2)
        self.assertEqual(result.first_row, PAGE_SIZE + 1)
        self.assertIn("2024-03-01", result.rows[0])
        self.assertTrue(result.has_results)

    def test_page_beyond_last_is_clamped(self):
        self.client.fetch.side_effect = [[{"filas": "5", "total": "5"}], [{"municipio": "CALI"}]]

        result = search("police_injuries", SearchCriteria(), page=99, client=self.client)

        self.assertEqual(result.page, 1)
        self.assertEqual(self.client.fetch.call_args_list[1].kwargs["offset"], 0)

    def test_no_matches_skips_page_query(self):
        self.client.fetch.return_value = [{"filas": "0", "total": None}]

        result = search("police_fatalities", SearchCriteria(anio=2010), client=self.client)

        self.assertTrue(result.no_matches)
        self.assertEqual(result.metric_total, 0)
        self.client.fetch.assert_called_once()

    def test_runt_metric_is_row_count(self):
        self.client.fetch.side_effect = [[{"filas": "3"}], [{"marca_vehiculo": "AKT"}]]

        result = search("runt_vehicles", SearchCriteria(), client=self.client)

        self.assertEqual(result.metric_total, 3)
        self.assertEqual(result.metric_label, "Vehículos involucrados")

    def test_api_error_is_returned(self):
        self.client.fetch.side_effect = SocrataError("No fue posible conectar con datos.gov.co.")

        result = search("police_injuries", SearchCriteria(), client=self.client)

        self.assertEqual(result.error, "No fue posible conectar con datos.gov.co.")
        self.assertFalse(result.has_results)
        self.assertFalse(result.no_matches)

    def test_invalid_criteria_raise_before_calling_api(self):
        with self.assertRaises(InvalidCriteriaError):
            search("police_injuries", SearchCriteria(anio=1990), client=self.client)
        self.client.fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
