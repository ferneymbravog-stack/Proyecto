from django.core.cache import cache
from django.shortcuts import render

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import DEFAULT_SAMPLE_SIZE, fetch_sample
from accidentadata.processing.service import process_records
from accidentadata.processing.statistics import build_statistical_summary

SAMPLE_CACHE_SECONDS = 600


def inicio(request):
    return render(request, 'accidentes/inicio.html')


def _load_source_data(key):
    """Obtiene la muestra cacheada, la procesa y construye el resumen estadístico."""
    cache_key = f'fuente-muestra:{key}:{DEFAULT_SAMPLE_SIZE}'
    result = cache.get(cache_key)
    if result is None:
        result = fetch_sample(key, limit=DEFAULT_SAMPLE_SIZE)
        if not result.error:
            cache.set(cache_key, result, SAMPLE_CACHE_SECONDS)

    processed_result = None
    stats_summary = None
    if result and not result.error:
        if not result.is_empty:
            raw_list = getattr(result, 'raw_records', None)
            if not raw_list and result.records:
                # Reconstruir diccionarios a partir de columnas y registros (para compatibilidad con mocks)
                raw_list = [dict(zip(result.columns, row)) for row in result.records]
            if raw_list:
                processed_result = process_records(key, raw_list, dataset=result.dataset)
                stats_summary = processed_result.summary
        if stats_summary is None:
            stats_summary = build_statistical_summary(key, [], dataset=result.dataset)

    return result, processed_result, stats_summary


def fuentes(request):
    modo = request.GET.get('modo', 'procesado').strip().lower()
    if modo not in ('procesado', 'crudo'):
        modo = 'procesado'

    context = {
        'datasets': DATASETS,
        'selected': None,
        'result': None,
        'processed_result': None,
        'stats_summary': None,
        'modo': modo,
        'invalid': '',
    }
    key = request.GET.get('fuente', '').strip()

    if not key:
        return render(request, 'accidentes/fuentes.html', context)

    if key not in DATASETS:
        context['invalid'] = key
        return render(request, 'accidentes/fuentes.html', context, status=404)

    result, processed_result, stats_summary = _load_source_data(key)

    context['selected'] = key
    context['result'] = result
    context['processed_result'] = processed_result
    context['stats_summary'] = stats_summary
    return render(request, 'accidentes/fuentes.html', context)


def estadisticas(request):
    default_key = next(iter(DATASETS))
    key = request.GET.get('fuente', default_key).strip() or default_key

    context = {
        'datasets': DATASETS,
        'selected': key,
        'result': None,
        'processed_result': None,
        'stats_summary': None,
        'invalid': '',
    }

    if key not in DATASETS:
        context['selected'] = None
        context['invalid'] = key
        return render(request, 'accidentes/estadisticas.html', context, status=404)

    result, processed_result, stats_summary = _load_source_data(key)

    context['result'] = result
    context['processed_result'] = processed_result
    context['stats_summary'] = stats_summary
    return render(request, 'accidentes/estadisticas.html', context)
