from django.core.cache import cache
from django.shortcuts import render

from accidentadata.data_sources.catalog import DATASETS
from accidentadata.data_sources.service import DEFAULT_SAMPLE_SIZE, fetch_sample

SAMPLE_CACHE_SECONDS = 600


def inicio(request):
    return render(request, 'accidentes/inicio.html')


def fuentes(request):
    context = {'datasets': DATASETS, 'selected': None, 'result': None, 'invalid': ''}
    key = request.GET.get('fuente', '').strip()

    if not key:
        return render(request, 'accidentes/fuentes.html', context)

    if key not in DATASETS:
        context['invalid'] = key
        return render(request, 'accidentes/fuentes.html', context, status=404)

    cache_key = f'fuente-muestra:{key}:{DEFAULT_SAMPLE_SIZE}'
    result = cache.get(cache_key)
    if result is None:
        result = fetch_sample(key, limit=DEFAULT_SAMPLE_SIZE)
        if not result.error:
            cache.set(cache_key, result, SAMPLE_CACHE_SECONDS)

    context['selected'] = key
    context['result'] = result
    return render(request, 'accidentes/fuentes.html', context)
