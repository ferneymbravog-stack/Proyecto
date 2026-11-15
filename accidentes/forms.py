from django import forms

from accidentadata.search.config import DEPARTMENTS, SEARCH_CONFIG, year_choices
from accidentadata.search.query import (
    InvalidCriteriaError,
    SearchCriteria,
    municipality_like,
)

# Mensajes propios: el proyecto usa LANGUAGE_CODE en inglés y los mensajes
# por defecto de Django aparecerían en inglés en una interfaz en español.
CHOICE_ERRORS = {'invalid_choice': 'Selecciona una opción de la lista.'}
TEXT_ERRORS = {'max_length': 'Escribe como máximo %(limit_value)d caracteres.'}


class SearchForm(forms.Form):
    """Formulario de búsqueda; sus filtros dependen de la fuente elegida."""

    def __init__(self, dataset_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset_key = dataset_key
        config = SEARCH_CONFIG[dataset_key]

        departments = sorted(DEPARTMENTS.items(), key=lambda item: item[1])
        self.fields['departamento'] = forms.ChoiceField(
            label='Departamento',
            required=False,
            choices=[('', 'Todos')] + departments,
            error_messages=CHOICE_ERRORS,
        )
        self.fields['municipio'] = forms.CharField(
            label='Municipio',
            required=False,
            max_length=40,
            error_messages=TEXT_ERRORS,
            help_text='Escribe el inicio del nombre; no importan las tildes.',
            widget=forms.TextInput(attrs={'placeholder': 'Ej.: Medellín'}),
        )
        self.fields['anio'] = forms.TypedChoiceField(
            label='Año',
            required=False,
            coerce=int,
            empty_value=None,
            choices=[('', 'Todos')] + [(year, year) for year in year_choices(dataset_key)],
            error_messages=CHOICE_ERRORS,
        )
        for name, options in config['extra_filters'].items():
            self.fields[name] = forms.ChoiceField(
                label=options['label'],
                required=False,
                choices=[('', 'Todos')] + [(choice, choice.capitalize()) for choice in options['choices']],
                error_messages=CHOICE_ERRORS,
            )

    def clean_municipio(self):
        value = ' '.join(self.cleaned_data.get('municipio', '').split())
        if value:
            try:
                municipality_like(value)
            except InvalidCriteriaError as error:
                raise forms.ValidationError(str(error))
        return value

    def criteria(self):
        data = self.cleaned_data
        extras = {
            name: data.get(name, '')
            for name in SEARCH_CONFIG[self.dataset_key]['extra_filters']
        }
        return SearchCriteria(
            departamento=data.get('departamento', ''),
            municipio=data.get('municipio', ''),
            anio=data.get('anio'),
            extras=extras,
        )

    def active_filters(self):
        """Pares (etiqueta, valor legible) de los filtros aplicados."""
        active = []
        for name, field in self.fields.items():
            value = self.cleaned_data.get(name)
            if value in (None, ''):
                continue
            if isinstance(field, forms.ChoiceField):
                value = dict(field.choices).get(value, value)
            active.append((field.label, value))
        return active
