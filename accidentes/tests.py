from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import SampleResult


def sample(key, **kwargs):
    return SampleResult(key=key, dataset=DATASETS[key], **kwargs)


class InicioViewTests(TestCase):
    def test_home_page_links_to_data_sources(self):
        response = self.client.get(reverse('inicio'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('fuentes'))
        self.assertContains(response, reverse('estadisticas'))


class FuentesViewTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('accidentes.views.fetch_sample')
    def test_lists_catalog_without_calling_api(self, mocked_fetch):
        response = self.client.get(reverse('fuentes'))

        self.assertEqual(response.status_code, 200)
        for dataset in DATASETS.values():
            self.assertContains(response, dataset['name'])
            self.assertContains(response, dataset['publisher'])
        mocked_fetch.assert_not_called()

    @patch('accidentes.views.fetch_sample')
    def test_shows_records_and_attribution(self, mocked_fetch):
        mocked_fetch.return_value = sample(
            'police_injuries',
            columns=['municipio', 'cantidad'],
            records=[['CALI', '3']],
        )

        response = self.client.get(reverse('fuentes'), {'fuente': 'police_injuries'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<td>CALI</td>', html=True)
        self.assertContains(response, 'ntej-qq7v')
        self.assertContains(response, DATASETS['police_injuries']['source_url'])
        self.assertContains(response, DATASETS['police_injuries']['limitations'][0])

    @patch('accidentes.views.fetch_sample')
    def test_shows_processed_mode_with_stats(self, mocked_fetch):
        mocked_fetch.return_value = sample(
            'police_injuries',
            columns=['municipio', 'cantidad', 'cod_muni', 'fecha_hecho'],
            records=[['cali', '3', '76001', '2026-09-30T00:00:00.000']],
        )

        response = self.client.get(reverse('fuentes'), {'fuente': 'police_injuries', 'modo': 'procesado'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Datos procesados y normalizados')
        self.assertContains(response, 'Registros procesados')
        self.assertContains(response, 'Víctimas reportadas')
        self.assertContains(response, 'Resumen estadístico')
        self.assertContains(response, 'Víctimas lesionadas')
        self.assertContains(response, '2026-09-30')
        self.assertContains(response, '<td>CALI</td>', html=True)

    @patch('accidentes.views.fetch_sample')
    def test_shows_raw_mode_when_selected(self, mocked_fetch):
        mocked_fetch.return_value = sample(
            'police_injuries',
            columns=['municipio', 'cantidad'],
            records=[['cali_crudo', '1']],
        )

        response = self.client.get(reverse('fuentes'), {'fuente': 'police_injuries', 'modo': 'crudo'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sin limpieza ni transformación')
        self.assertContains(response, '<td>cali_crudo</td>', html=True)

    @patch('accidentes.views.fetch_sample')
    def test_api_error_is_shown_without_failing(self, mocked_fetch):
        mocked_fetch.return_value = sample(
            'runt_vehicles', error='No fue posible conectar con datos.gov.co.'
        )

        response = self.client.get(reverse('fuentes'), {'fuente': 'runt_vehicles'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No fue posible obtener los datos.')
        self.assertContains(response, 'No fue posible conectar con datos.gov.co.')

    @patch('accidentes.views.fetch_sample')
    def test_empty_response_shows_message(self, mocked_fetch):
        mocked_fetch.return_value = sample('runt_vehicles')

        response = self.client.get(reverse('fuentes'), {'fuente': 'runt_vehicles'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no devolvió registros')
        self.assertContains(response, 'Resumen estadístico')
        self.assertContains(response, 'Sin datos para resumir.')

    @patch('accidentes.views.fetch_sample')
    def test_unknown_source_returns_404_with_escaped_message(self, mocked_fetch):
        response = self.client.get(reverse('fuentes'), {'fuente': '<script>x</script>'})

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Fuente no encontrada', status_code=404)
        self.assertContains(response, '&lt;script&gt;', status_code=404)
        self.assertNotContains(response, '<script>x</script>', status_code=404)
        mocked_fetch.assert_not_called()

    @patch('accidentes.views.fetch_sample')
    def test_successful_sample_is_cached(self, mocked_fetch):
        mocked_fetch.return_value = sample('police_injuries', columns=['municipio'], records=[['CALI']])

        self.client.get(reverse('fuentes'), {'fuente': 'police_injuries'})
        self.client.get(reverse('fuentes'), {'fuente': 'police_injuries'})

        self.assertEqual(mocked_fetch.call_count, 1)

    @patch('accidentes.views.fetch_sample')
    def test_failed_sample_is_not_cached(self, mocked_fetch):
        mocked_fetch.return_value = sample('police_injuries', error='Fallo temporal.')

        self.client.get(reverse('fuentes'), {'fuente': 'police_injuries'})
        self.client.get(reverse('fuentes'), {'fuente': 'police_injuries'})

        self.assertEqual(mocked_fetch.call_count, 2)


class EstadisticasViewTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('accidentes.views.fetch_sample')
    def test_default_estadisticas_loads_first_dataset(self, mocked_fetch):
        mocked_fetch.return_value = sample(
            'runt_vehicles',
            columns=['departamento_accidente', 'municipio_accidente', 'fecha_accidente'],
            records=[['ANTIOQUIA', 'MEDELLIN', '09/2026']],
        )

        response = self.client.get(reverse('estadisticas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de estadísticas')
        self.assertContains(response, 'Resumen estadístico')
        self.assertContains(response, 'Vehículos involucrados')
        self.assertContains(response, 'ANTIOQUIA')

    @patch('accidentes.views.fetch_sample')
    def test_estadisticas_handles_empty_dataset(self, mocked_fetch):
        mocked_fetch.return_value = sample('police_injuries')

        response = self.client.get(reverse('estadisticas'), {'fuente': 'police_injuries'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sin datos para resumir.')

    @patch('accidentes.views.fetch_sample')
    def test_estadisticas_unknown_source_returns_404(self, mocked_fetch):
        response = self.client.get(reverse('estadisticas'), {'fuente': 'no_existe'})

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Fuente no encontrada', status_code=404)
        mocked_fetch.assert_not_called()


class BuscarViewTests(TestCase):
    def setUp(self):
        cache.clear()

    def result(self, key='police_injuries', **kwargs):
        from accidentadata.search.service import SearchResult
        defaults = {'key': key, 'dataset': DATASETS[key], 'metric_label': 'Víctimas'}
        defaults.update(kwargs)
        return SearchResult(**defaults)

    @patch('accidentes.views.search')
    def test_without_source_asks_to_choose_one(self, mocked_search):
        response = self.client.get(reverse('buscar'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Selecciona una fuente')
        mocked_search.assert_not_called()

    @patch('accidentes.views.search')
    def test_choosing_source_shows_its_filters_without_searching(self, mocked_search):
        response = self.client.get(reverse('buscar'), {'fuente': 'runt_vehicles'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="gravedad_accidente"')
        self.assertContains(response, 'name="tipo_vehiculo"')
        self.assertNotContains(response, 'name="genero"')
        mocked_search.assert_not_called()

    @patch('accidentes.views.search')
    def test_search_shows_totals_rows_and_active_filters(self, mocked_search):
        mocked_search.return_value = self.result(
            total_rows=45, metric_total=52, pages=3, page=1,
            columns=['municipio', 'cantidad'], rows=[['CALI', 2]],
        )

        response = self.client.get(reverse('buscar'), {
            'fuente': 'police_injuries', 'buscar': '1', 'departamento': '76', 'anio': '2024',
        })

        self.assertEqual(response.status_code, 200)
        criteria = mocked_search.call_args.args[1]
        self.assertEqual(criteria.departamento, '76')
        self.assertEqual(criteria.anio, 2024)
        self.assertContains(response, '<td>CALI</td>', html=True)
        self.assertContains(response, 'Departamento: Valle del Cauca')
        self.assertContains(response, 'Año: 2024')
        self.assertContains(response, 'Siguiente')
        self.assertContains(response, DATASETS['police_injuries']['source_url'])

    @patch('accidentes.views.search')
    def test_no_matches_shows_clear_message(self, mocked_search):
        mocked_search.return_value = self.result(total_rows=0)

        response = self.client.get(reverse('buscar'), {
            'fuente': 'police_injuries', 'buscar': '1', 'municipio': 'zzz',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay registros que coincidan con estos filtros.')

    @patch('accidentes.views.search')
    def test_api_error_is_shown_without_failing(self, mocked_search):
        mocked_search.return_value = self.result(error='No fue posible conectar con datos.gov.co.')

        response = self.client.get(reverse('buscar'), {'fuente': 'police_injuries', 'buscar': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No fue posible realizar la búsqueda.')

    @patch('accidentes.views.search')
    def test_invalid_inputs_show_errors_and_skip_search(self, mocked_search):
        cases = [
            {'municipio': "x' OR 1=1"},
            {'departamento': '00'},
            {'anio': '1990'},
            {'anio': 'abc'},
            {'genero': 'OTRO'},
        ]
        for params in cases:
            with self.subTest(params=params):
                data = {'fuente': 'police_fatalities', 'buscar': '1', **params}
                response = self.client.get(reverse('buscar'), data)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Revisa los filtros')
                self.assertNotContains(response, 'Select a valid choice')
        mocked_search.assert_not_called()

    def test_field_errors_are_in_spanish(self):
        response = self.client.get(reverse('buscar'), {
            'fuente': 'police_fatalities', 'buscar': '1', 'anio': '1990', 'municipio': 'a' * 41,
        })

        self.assertContains(response, 'Selecciona una opción de la lista.')
        self.assertContains(response, 'Escribe como máximo 40 caracteres.')

    @patch('accidentes.views.search')
    def test_unknown_source_returns_404(self, mocked_search):
        response = self.client.get(reverse('buscar'), {'fuente': '<b>x</b>', 'buscar': '1'})

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, '&lt;b&gt;x&lt;/b&gt;', status_code=404)
        mocked_search.assert_not_called()

    @patch('accidentes.views.search')
    def test_invalid_page_falls_back_to_first(self, mocked_search):
        mocked_search.return_value = self.result(total_rows=1, pages=1, rows=[['CALI']], columns=['municipio'])

        self.client.get(reverse('buscar'), {'fuente': 'police_injuries', 'buscar': '1', 'pagina': 'abc'})

        self.assertEqual(mocked_search.call_args.kwargs['page'], 1)

    @patch('accidentes.views.search')
    def test_pagination_links_keep_filters(self, mocked_search):
        mocked_search.return_value = self.result(
            total_rows=60, pages=3, page=2, rows=[['CALI']], columns=['municipio'],
        )

        response = self.client.get(reverse('buscar'), {
            'fuente': 'police_injuries', 'buscar': '1', 'departamento': '76', 'pagina': '2',
        })

        self.assertContains(response, 'departamento=76&amp;pagina=1')
        self.assertContains(response, 'departamento=76&amp;pagina=3')

    @patch('accidentes.views.search')
    def test_successful_search_is_cached(self, mocked_search):
        mocked_search.return_value = self.result(total_rows=1, pages=1, rows=[['CALI']], columns=['municipio'])
        params = {'fuente': 'police_injuries', 'buscar': '1', 'departamento': '76'}

        self.client.get(reverse('buscar'), params)
        self.client.get(reverse('buscar'), params)

        self.assertEqual(mocked_search.call_count, 1)

    def test_navigation_links_to_search(self):
        for name in ('inicio', 'fuentes', 'estadisticas'):
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), reverse('buscar'))
