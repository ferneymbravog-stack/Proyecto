# Fuentes nacionales de AccidentaData

## Alcance

AccidentaData inicia con cobertura nacional de Colombia. Las fuentes se consultan desde la API pública Socrata de datos.gov.co. Los metadatos de este documento se verificaron el 13 de noviembre de 2026 en la ficha oficial de cada conjunto (`https://www.datos.gov.co/api/views/{id}.json`).

## Catálogo de fuentes

| Clave interna | ID Socrata | Entidad | Cobertura y periodo | Actualización | Filas |
|---|---|---|---|---|---|
| `runt_vehicles` | `6jmc-vaxk` | Ministerio de Transporte (RUNT) | Nacional · ene. 2022 – sep. 2026 | Semestral | 450.335 |
| `police_fatalities` | `ha6j-pa2r` | Dirección General de la Policía Nacional (DIJIN) | Nacional · ene. 2010 – jul. 2026 | Trimestral | 98.430 |
| `police_injuries` | `ntej-qq7v` | Ministerio de Defensa Nacional | Nacional · ene. 2003 – sep. 2026 | Mensual | 644.042 |

Las tres fuentes se publican con licencia CC BY-SA 4.0. El número de filas cambia con cada actualización.

La clave `police_injuries` se conserva por compatibilidad, aunque la ficha oficial registra como publicador al Ministerio de Defensa Nacional y no a la Policía Nacional.

## Campos publicados

| Fuente | Campos | Formato de fecha |
|---|---|---|
| `runt_vehicles` | `marca_vehiculo`, `modelo_vehiculo`, `tipo_vehiculo`, `edad_vehiculo`, `fecha_accidente`, `gravedad_accidente`, `departamento_accidente`, `municipio_accidente`, `autoridad_de_transito` | Texto `MM/AAAA` (solo mes y año) |
| `police_fatalities` | `departamento`, `municipio`, `codigo_dane`, `armas_medios`, `fecha_hecho`, `genero`, `grupo_etar_o`, `descripci_n_conducta`, `cantidad` | Texto `DD/MM/AAAA` |
| `police_injuries` | `fecha_hecho`, `cod_depto`, `departamento`, `cod_muni`, `municipio`, `cantidad` | Fecha ISO (`AAAA-MM-DDT00:00:00.000`) |

En `police_fatalities` todos los campos, incluido `cantidad`, se publican como texto. En `runt_vehicles`, `gravedad_accidente` solo toma los valores `CON HERIDOS` y `CON MUERTOS`.

## Reglas de interpretación

- Los registros del RUNT describen vehículos involucrados, no necesariamente el total de siniestros.
- La fuente de homicidios registra muertes y no debe confundirse con el total de accidentes.
- La fuente de lesiones se mide en víctimas, según su ficha. Una fila puede agrupar varias víctimas: los totales se obtienen sumando `cantidad`. Por ejemplo, en la verificación las 644.042 filas sumaban 885.829 víctimas.
- La misma regla aplica a homicidios: sumar `cantidad`, no contar filas.
- No se deben sumar filas de fuentes distintas como si fueran una única cifra de accidentes.
- La Policía Nacional advierte que sus cifras están sujetas a variación y en proceso de consolidación con la Fiscalía.
- La presencia de departamento y municipio no significa que existan coordenadas exactas para un mapa de puntos. Ninguna de las tres fuentes incluye coordenadas.
- Para cruzar fuentes por ubicación conviene usar los códigos DANE (`codigo_dane`, `cod_depto`, `cod_muni`), porque los nombres de municipio cambian de mayúsculas y tildes entre fuentes. El RUNT no publica código DANE. Los formatos tampoco coinciden: `codigo_dane` de homicidios tiene 8 dígitos (por ejemplo `19130000`), mientras que `cod_muni` de lesiones tiene 5 (`76001`); los 5 primeros dígitos de `codigo_dane` corresponden al código DIVIPOLA del municipio, lo que debe confirmarse en AD-03.
- La fuente histórica `wacd-xkg8` aparece citada en proyectos de análisis de accidentalidad, pero su cobertura geográfica debe verificarse en su ficha antes de incorporarla como fuente nacional.

## API

La consulta usa el endpoint público:

`https://www.datos.gov.co/resource/{dataset_id}.json`

Se admiten paginación mediante `$limit` y `$offset`, además de filtros Socrata. Para un uso frecuente, configurar la variable de entorno `SOCRATA_APP_TOKEN`.

## Integración en la aplicación

- `accidentadata/data_sources/catalog.py`: metadatos de cada fuente (entidad, cobertura, campos, unidad de conteo, limitaciones y enlace).
- `accidentadata/data_sources/socrata_client.py`: cliente HTTP con validación de parámetros y errores controlados.
- `accidentadata/data_sources/service.py`: obtiene una muestra de una fuente del catálogo. Los errores de conexión o de formato se devuelven como mensaje, sin interrumpir la aplicación.
- `accidentadata/processing/cleaners.py`: funciones puras de limpieza de textos, números, fechas y códigos DIVIPOLA/DANE.
- `accidentadata/processing/transformers.py`: transformadores específicos por fuente (`transform_runt_vehicle`, `transform_police_fatality`, `transform_police_injury`).
- `accidentadata/processing/service.py`: servicio reutilizable de procesamiento y cálculo de métricas de calidad (`process_records`, `fetch_processed_sample`, `calculate_stats`).
- Página `/fuentes/`: lista las fuentes y, con `?fuente=<clave>`, permite alternar entre la vista de datos procesados/normalizados (modo por defecto) y datos originales crudos (`modo=crudo`). Las muestras correctas se guardan en caché durante 10 minutos.

## Limpieza y normalización de datos (AD-03)

1. **Tipos de datos y formatos inconsistentes:**
   - **Fechas:** Estandarización a ISO. RUNT (`MM/AAAA`) se normaliza a `AAAA-MM` y extrae año y mes; DIJIN (`DD/MM/AAAA`) y Mindefensa (`ISO con hora`) se normalizan a `AAAA-MM-DD` y extraen año, mes y día.
   - **Cantidades:** Conversión estricta de cadenas de texto a enteros positivos (`int`). En caso de valores inválidos o nulos, se aplica fallback predecible de 1 víctima por fila de incidente.
   - **Geografía:** Normalización de departamentos y municipios a mayúsculas limpias, eliminando sufijos como `(CT)` y espacios repetidos.
   - **Códigos DANE:** Extracción del código DIVIPOLA de 5 dígitos para municipios y de 2 dígitos para departamentos a partir del código de 8 dígitos de la Policía Nacional (`19130000` -> dpto `19`, muni `19130`), y relleno con ceros a la izquierda para fuentes con códigos de longitud variable.
2. **Valores ausentes o inválidos:**
   - Cadenas vacías o representaciones comunes de ausencia (`SIN INFORMACION`, `NO APLICA`, `null`, `nan`, etc.) se convierten de forma predecible en `NO REPORTADO` o `—`.
   - Números fuera de rango (como modelos de vehículos `<= 1900` o edades negativas) se filtran de forma no bloqueante o se calculan consistentemente (`anio_accidente - modelo_vehiculo`).
3. **Métricas de calidad calculadas:**
   - Conteo oficial según la unidad de cada fuente (suma de víctimas para homicidios y lesiones, vehículos involucrados para el RUNT).
   - Indicadores de completitud de fechas y ubicaciones geográficas.

## Primera validación técnica

1. ~~Consultar una muestra pequeña de cada conjunto.~~ Hecho.
2. ~~Registrar los campos reales devueltos por la API.~~ Hecho (sección "Campos publicados").
3. ~~Confirmar el campo de fecha y los campos geográficos.~~ Hecho.
4. ~~Identificar la unidad de conteo de cada fuente.~~ Hecho.
5. Definir indicadores comparables antes de construir estadísticas (AD-05).
