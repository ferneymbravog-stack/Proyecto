"""Pruebas unitarias para el módulo geográfico y payload de visualización."""

from django.test import TestCase

from accidentadata.processing.statistics import (
    BreakdownGroup,
    CategoryStat,
    StatisticalSummary,
)
from accidentes.geo import DEPARTMENTS_COORDS, build_map_and_charts_payload


class GeoPayloadTests(TestCase):
    def test_department_coords_contains_33_departments(self):
        # 32 departamentos + Bogotá D.C.
        self.assertIn("ANTIOQUIA", DEPARTMENTS_COORDS)
        self.assertIn("BOGOTA D.C.", DEPARTMENTS_COORDS)
        self.assertIn("VALLE DEL CAUCA", DEPARTMENTS_COORDS)
        self.assertIn("lat", DEPARTMENTS_COORDS["ANTIOQUIA"])
        self.assertIn("lng", DEPARTMENTS_COORDS["ANTIOQUIA"])

    def test_build_payload_empty_summary(self):
        empty_summary = StatisticalSummary(
            dataset_key="runt_vehicles",
            dataset_name="RUNT",
            publisher="MinTransporte",
            is_empty=True,
            unit_label="Vehículos involucrados",
        )
        payload = build_map_and_charts_payload(empty_summary, "runt_vehicles")

        self.assertFalse(payload["has_data"])
        self.assertEqual(payload["departments"], [])
        self.assertIsNone(payload["breakdown_chart"])

    def test_build_payload_with_department_breakdown(self):
        summary = StatisticalSummary(
            dataset_key="runt_vehicles",
            dataset_name="RUNT",
            publisher="MinTransporte",
            is_empty=False,
            total_metric=10,
            total_records=10,
            unit_label="Vehículos involucrados",
            breakdowns=[
                BreakdownGroup(
                    key="departamento",
                    title="Departamento",
                    unit="vehículos involucrados",
                    description="Distribución territorial",
                    items=[
                        CategoryStat(label="ANTIOQUIA", count=6, records_count=6, percentage=60.0),
                        CategoryStat(label="VALLE DEL CAUCA", count=4, records_count=4, percentage=40.0),
                    ],
                ),
                BreakdownGroup(
                    key="gravedad",
                    title="Gravedad del accidente",
                    unit="vehículos involucrados",
                    description="Clasificación por gravedad",
                    items=[
                        CategoryStat(label="CON HERIDOS", count=7, records_count=7, percentage=70.0),
                        CategoryStat(label="CON MUERTOS", count=3, records_count=3, percentage=30.0),
                    ],
                ),
            ],
        )

        payload = build_map_and_charts_payload(summary, "runt_vehicles")

        self.assertTrue(payload["has_data"])
        self.assertEqual(len(payload["departments"]), 2)
        self.assertEqual(payload["departments"][0]["name"], "Antioquia")
        self.assertEqual(payload["departments"][0]["code"], "05")
        self.assertEqual(payload["departments"][0]["count"], 6)

        # Gráfico adicional
        self.assertIsNotNone(payload["other_breakdown"])
        self.assertEqual(payload["other_breakdown"]["title"], "Gravedad del accidente")
        self.assertIn("CON HERIDOS", payload["other_breakdown"]["labels"])


class MapaViewTests(TestCase):
    def test_mapa_view_returns_200_and_contains_elements(self):
        from django.urls import reverse
        response = self.client.get(reverse('mapa'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mapa de Accidentalidad Vial en Colombia')
        self.assertContains(response, 'id="accidents-map"')
        self.assertContains(response, 'id="incidents-list"')
        self.assertContains(response, 'Con Fallecidos')
