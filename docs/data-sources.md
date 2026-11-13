# Fuentes nacionales de AccidentaData

## Alcance

AccidentaData inicia con cobertura nacional de Colombia. Las fuentes se consultan desde la API pública de Socrata de datos.gov.co.

## Catálogo inicial

| Clave interna | ID Socrata | Entidad | Alcance |
|---|---|---|---|
| `runt_vehicles` | `6jmc-vaxk` | RUNT / MinTransporte | Vehículos involucrados en siniestros con muertos o heridos |
| `police_fatalities` | `ha6j-pa2r` | Policía Nacional / DIJIN | Homicidios en accidentes de tránsito |
| `police_injuries` | `72sg-cybi` | Policía Nacional / DIJIN | Lesiones personales y lesiones en accidentes de tránsito |

## Reglas de interpretación

- Los registros del RUNT describen vehículos involucrados, no necesariamente el total de siniestros.
- El conjunto de homicidios de la Policía contabiliza víctimas/casos según la definición y estructura publicada por la fuente.
- El conjunto de lesiones debe revisarse para separar lesiones de tránsito de otras lesiones personales.
- No se deben sumar filas de fuentes distintas como si fueran una única cifra de accidentes.
- Antes de publicar indicadores, se deben revisar nombres de campos, fechas, cobertura temporal, duplicados y actualización efectiva.
- La disponibilidad de departamento y municipio no significa que existan coordenadas exactas para un mapa de puntos.

## API

La consulta usa el endpoint público:

`https://www.datos.gov.co/resource/{dataset_id}.json`

Se admiten paginación mediante `$limit` y `$offset`, además de filtros Socrata. Para un uso frecuente, configurar la variable de entorno `SOCRATA_APP_TOKEN`.

## Próxima validación

1. Consultar una muestra de cada conjunto.
2. Registrar los campos reales devueltos por la API.
3. Confirmar el campo de fecha y los campos geográficos.
4. Definir indicadores comparables antes de construir estadísticas.
