import hashlib
import json

from django.core.cache import cache
from django.shortcuts import render

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import DEFAULT_SAMPLE_SIZE, fetch_sample
from accidentadata.processing.service import process_records
from accidentadata.processing.statistics import build_statistical_summary
from accidentadata.search.query import InvalidCriteriaError
from accidentadata.search.service import search

from .forms import SearchForm
from .geo import build_map_and_charts_payload, generate_map_accidents_dataset, DEPARTMENTS_COORDS

SAMPLE_CACHE_SECONDS = 600
SEARCH_CACHE_SECONDS = 600


def inicio(request):
    # Enriquecer inicio con datasets y mapa base de Colombia para el tour interactivo
    departments_summary = [
        {"name": info["name"], "lat": info["lat"], "lng": info["lng"], "code": info["code"]}
        for info in DEPARTMENTS_COORDS.values()
    ]
    context = {
        'datasets': DATASETS,
        'departments_summary_json': json.dumps(departments_summary),
    }
    return render(request, 'accidentes/inicio.html', context)


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

    visual_payload = build_map_and_charts_payload(stats_summary, key)

    context['result'] = result
    context['processed_result'] = processed_result
    context['stats_summary'] = stats_summary
    context['visual_payload_json'] = json.dumps(visual_payload)
    return render(request, 'accidentes/estadisticas.html', context)


def _page_number(value):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return 1


def buscar(request):
    context = {'datasets': DATASETS, 'selected': None, 'form': None, 'result': None,
               'active_filters': [], 'invalid': '', 'querystring': ''}
    key = request.GET.get('fuente', '').strip()

    if not key:
        return render(request, 'accidentes/buscar.html', context)

    if key not in DATASETS:
        context['invalid'] = key
        return render(request, 'accidentes/buscar.html', context, status=404)

    context['selected'] = key
    submitted = 'buscar' in request.GET
    form = SearchForm(key, request.GET if submitted else None)
    context['form'] = form

    if not submitted or not form.is_valid():
        return render(request, 'accidentes/buscar.html', context)

    page = _page_number(request.GET.get('pagina'))
    criteria = form.criteria()
    cache_key = 'busqueda:' + hashlib.sha256(
        f'{key}|{criteria}|{page}'.encode('utf-8')
    ).hexdigest()
    result = cache.get(cache_key)
    if result is None:
        try:
            result = search(key, criteria, page=page)
        except InvalidCriteriaError as error:
            form.add_error(None, str(error))
            return render(request, 'accidentes/buscar.html', context)
        if not result.error:
            cache.set(cache_key, result, SEARCH_CACHE_SECONDS)

    params = request.GET.copy()
    params.pop('pagina', None)
    context['querystring'] = params.urlencode()
    context['result'] = result
    context['active_filters'] = form.active_filters()
    return render(request, 'accidentes/buscar.html', context)


def mapa(request):
    default_key = next(iter(DATASETS))
    key = request.GET.get('fuente', default_key).strip() or default_key
    if key not in DATASETS:
        key = default_key

    result, processed_result, stats_summary = _load_source_data(key)
    sample_records = getattr(processed_result, 'records', None) if processed_result else None

    accidents_points = generate_map_accidents_dataset(key, sample_records)
    departments_summary = [
        {"name": info["name"], "lat": info["lat"], "lng": info["lng"], "code": info["code"]}
        for info in DEPARTMENTS_COORDS.values()
    ]

    context = {
        'datasets': DATASETS,
        'selected': key,
        'accidents_json': json.dumps(accidents_points),
        'departments_summary_json': json.dumps(departments_summary),
        'total_accidents': len(accidents_points),
        'fatalities_count': sum(1 for p in accidents_points if p.get('severidad') == 'fatal'),
        'injuries_count': sum(1 for p in accidents_points if p.get('severidad') != 'fatal'),
    }
    return render(request, 'accidentes/mapa.html', context)
