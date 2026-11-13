# Fuentes nacionales de AccidentaData

## Alcance

AccidentaData inicia con cobertura nacional de Colombia. Las fuentes se consultan desde la API pública Socrata de datos.gov.co.

## Catálogo inicial de fuentes

| Clave interna | ID Socrata | Entidad | Alcance / uso |
|---|---|---|---|
| `runt_vehicles` | `6jmc-vaxk` | Ministerio de Transporte / RUNT 2.0 | Nacional; vehículos involucrados en siniestros con muertos o heridos |
| `police_fatalities` | `ha6j-pa2r` | Policía Nacional | Homicidios en accidentes de tránsito; validar cobertura temporal y campos |
| `police_injuries` | `ntej-qq7v` | Policía Nacional | Lesiones en accidentes de tránsito; validar cobertura, campos y definición |

La fuente del RUNT informa cobertura nacional, actualización semestral y aproximadamente 450.000 filas en su ficha consultada. Sus campos publicados incluyen marca, modelo, tipo y edad del vehículo, fecha del siniestro, gravedad, departamento, municipio y autoridad de tránsito.

## Reglas de interpretación

- Los registros del RUNT describen vehículos involucrados, no necesariamente el total de siniestros.
- La fuente de homicidios registra muertes y no debe confundirse con el total de accidentes.
- La fuente de lesiones debe revisarse para confirmar si cada fila representa una víctima, un caso u otra unidad estadística.
- No se deben sumar filas de fuentes distintas como si fueran una única cifra de accidentes.
- Antes de publicar indicadores, revisar nombres de campos, fechas, cobertura temporal, duplicados y actualización efectiva.
- La presencia de departamento y municipio no significa que existan coordenadas exactas para un mapa de puntos.
- La fuente histórica `wacd-xkg8` aparece citada en proyectos de análisis de accidentalidad, pero su cobertura geográfica debe verificarse en su ficha antes de incorporarla como fuente nacional.

## API

La consulta usa el endpoint público:

`https://www.datos.gov.co/resource/{dataset_id}.json`

Se admiten paginación mediante `$limit` y `$offset`, además de filtros Socrata. Para un uso frecuente, configurar la variable de entorno `SOCRATA_APP_TOKEN`.

## Primera validación técnica

1. Consultar una muestra pequeña de cada conjunto.
2. Registrar los campos reales devueltos por la API.
3. Confirmar el campo de fecha y los campos geográficos.
4. Identificar la unidad de conteo de cada fuente.
5. Definir indicadores comparables antes de construir estadísticas.
