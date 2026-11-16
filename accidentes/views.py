import hashlib

from django.core.cache import cache
from django.shortcuts import render

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import DEFAULT_SAMPLE_SIZE, fetch_sample
from accidentadata.processing.service import process_records
from accidentadata.processing.statistics import build_statistical_summary
from accidentadata.search.query import InvalidCriteriaError
from accidentadata.search.service import search

from .forms import SearchForm

SAMPLE_CACHE_SECONDS = 600
SEARCH_CACHE_SECONDS = 600


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



from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import DEFAULT_SAMPLE_SIZE, fetch_sample
from accidentadata.processing.service import process_records
from accidentadata.geography.service import build_municipality_summary
from accidentadata.search.query import InvalidCriteriaError
from accidentadata.search.service import search


def mapa(request):
    """Muestra información geográfica de accidentalidad."""

    available_sources = [
        "police_fatalities",
        "police_injuries",
    ]

    selected = request.GET.get(
        "fuente", "police_injuries"
    ).strip()

    if selected not in available_sources:
        selected = "police_injuries"

    result, processed_result, stats_summary = _load_source_data(selected)

    records = (
        processed_result.records
        if processed_result and not result.error
        else []
    )

    geographic_data = build_municipality_summary(records)

    context = {
        "datasets": DATASETS,
        "selected": selected,
        "municipalities": geographic_data["municipalities"],
        "without_location": geographic_data["without_location"],
        "error": result.error if result else "",
    }

    return render(request, "accidentes/mapa.html", context)