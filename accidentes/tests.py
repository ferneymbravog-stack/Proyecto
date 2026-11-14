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
