# AccidentaData

Aplicación web desarrollada con **Python y Django** para consultar, procesar y visualizar datos abiertos relacionados con accidentalidad. El propósito es convertir datos públicos en información comprensible que ayude a los usuarios a explorar patrones y responder preguntas útiles.

> Las fuentes de datos, sus entidades publicadoras, cobertura y limitaciones están documentadas en la sección [Fuente de datos](#fuente-de-datos) y en [`docs/data-sources.md`](docs/data-sources.md). No se deben presentar hipótesis como necesidades validadas ni datos de ejemplo como datos reales.

## Objetivo del Producto (Product Goal)

Ofrecer una aplicación web que permita explorar información pública relacionada con accidentalidad mediante búsqueda, filtros y resúmenes comprensibles, facilitando la interpretación de los datos y la consulta de información relevante.

## Objetivo del Sprint (Sprint Goal)

Entregar un recorrido web funcional en Django que consuma o procese una fuente real de datos abiertos y permita al usuario consultar información mediante una acción útil, con resultados comprensibles y manejo de búsquedas vacías o entradas inválidas.

## Equipo y responsabilidades

| Integrante | Responsabilidad principal |
|---|---|
| [ferneymbravog-stack](https://github.com/ferneymbravog-stack) | Developer · Desarrollo backend y configuración |
| [jader-posso](https://github.com/jader-posso) | Product Owner · Objetivos, prioridades y valor del producto |
| [Joel90900](https://github.com/Joel90900) | Developer · Interfaz, frontend y funcionalidades web |
| [Gonzalez82ZG](https://github.com/Gonzalez82ZG) | Scrum Master · Facilitación, pruebas y seguimiento |

Todos participan en el descubrimiento, planificación, desarrollo y verificación. Jader puede contribuir al código y González puede desarrollar y probar funcionalidades.

## Issues y asignación

El trabajo se organiza en ocho Issues. Cada Issue incluye objetivo, actividades, criterios de aceptación y responsables.

> **Importante: el código AD-xx y el número del Issue en GitHub son distintos.** En GitHub los Issues están numerados del #5 al #12, mientras que sus códigos van de AD-01 a AD-08. Para evitar confusiones, en commits, ramas y conversaciones del equipo use el código **AD-xx**. Para enlazar un Pull Request con su Issue use el número de GitHub: por ejemplo, AD-02 se enlaza con `Refs #6`, no con `Refs #2`. El texto de algunos Issues todavía cita sus dependencias con la numeración antigua ("Issue #1", "Issue #2"), que corresponde a AD-01 y AD-02.

| Código | Issue en GitHub | Trabajo | Responsables |
|---|---|---|---|
| AD-01 | [#5](../../issues/5) | Configurar Django y construir la interfaz inicial | ferneymbravog-stack, Joel90900 |
| AD-02 | [#6](../../issues/6) | Integrar fuentes de datos abiertos | ferneymbravog-stack, jader-posso |
| AD-03 | [#7](../../issues/7) | Procesar, limpiar y preparar los datos | ferneymbravog-stack, Joel90900 |
| AD-04 | [#8](../../issues/8) | Implementar búsqueda y filtros | Joel90900, jader-posso |
| AD-05 | [#9](../../issues/9) | Construir el panel de estadísticas | Joel90900, ferneymbravog-stack |
| AD-06 | [#10](../../issues/10) | Incorporar mapa interactivo | Gonzalez82ZG, ferneymbravog-stack |
| AD-07 | [#11](../../issues/11) | Ejecutar pruebas y validar el funcionamiento | Gonzalez82ZG, jader-posso |
| AD-08 | [#12](../../issues/12) | Consolidar documentación e integrar la entrega | Los cuatro integrantes |

## Product Backlog

1. Configurar el proyecto Django y disponer de una interfaz web inicial.
2. Integrar una fuente de datos abiertos identificada y documentada.
3. Procesar y limpiar los datos necesarios para su consulta.
4. Permitir búsquedas y filtros útiles para el usuario.
5. Presentar estadísticas calculadas a partir de datos reales.
6. Representar datos geográficos en un mapa cuando la fuente lo permita.
7. Verificar el recorrido principal, casos vacíos y entradas inválidas.
8. Documentar, integrar y preparar la demostración del producto.

## Sprint Backlog

El Sprint Backlog comprende el Sprint Goal, los elementos priorizados que el equipo selecciona y el plan de trabajo de los Issues. El equipo debe actualizar el estado según el avance real:

- **Backlog:** pendiente y no seleccionado.
- **Ready:** preparado para comenzar.
- **In Progress:** en ejecución.
- **In Review:** pendiente de revisión.
- **Done:** terminado y verificado según la Definition of Done.

Prioridad recomendada: High para configuración, fuente de datos, procesamiento, búsqueda, pruebas y consolidación; Medium para estadísticas y mapa. Ajustar según la viabilidad y el valor real.

## Definition of Done (DoD)

Un incremento se considera terminado cuando:

- Django inicia sin errores bloqueantes.
- Se completa el recorrido principal desde el navegador.
- La aplicación responde de forma demostrable al problema o hipótesis elegida.
- Se usan datos reales y la fuente está identificada.
- Se cumplen los criterios de aceptación del Issue.
- Las entradas inválidas y resultados vacíos se manejan sin fallos bloqueantes.
- Se ejecutó y registró una comprobación funcional real.
- Los cambios están revisados e integrados en la rama principal.
- El README permite instalar y ejecutar el proyecto.
- Issues y Project reflejan el estado verdadero del trabajo.

La fusión de un Pull Request no significa automáticamente que el trabajo esté terminado.

## Fuente de datos

La aplicación consulta en tiempo real la API pública Socrata de [datos.gov.co](https://www.datos.gov.co/) (`https://www.datos.gov.co/resource/{id}.json`). Los metadatos de estas fuentes se verificaron el 13 de noviembre de 2026 en la ficha oficial de cada conjunto.

| Conjunto de datos | ID | Entidad publicadora | Cobertura y periodo | Actualización | Unidad de conteo |
|---|---|---|---|---|---|
| [Vehículos involucrados en un accidente de tránsito (Ley 2251 de 2022)](https://www.datos.gov.co/d/6jmc-vaxk) | `6jmc-vaxk` | Ministerio de Transporte (RUNT) | Nacional · ene. 2022 – sep. 2026 | Semestral | Vehículo involucrado |
| [Homicidios en accidente de tránsito](https://www.datos.gov.co/d/ha6j-pa2r) | `ha6j-pa2r` | Dirección General de la Policía Nacional (DIJIN) | Nacional · ene. 2010 – jul. 2026 | Trimestral | Víctimas: suma de `cantidad` |
| [Lesiones en accidentes de tránsito](https://www.datos.gov.co/d/ntej-qq7v) | `ntej-qq7v` | Ministerio de Defensa Nacional | Nacional · ene. 2003 – sep. 2026 | Mensual | Víctimas: suma de `cantidad` |

Las tres fuentes se publican con licencia **CC BY-SA 4.0**, que exige citar la entidad de origen. La página **Fuentes de datos** (`/fuentes/`) muestra una muestra de 10 registros reales de cada conjunto, junto con su entidad, enlace, licencia y limitaciones.

**Variables utilizadas**

- **Vehículos:** `marca_vehiculo`, `modelo_vehiculo`, `tipo_vehiculo`, `edad_vehiculo`, `fecha_accidente`, `gravedad_accidente`, `departamento_accidente`, `municipio_accidente`, `autoridad_de_transito`.
- **Homicidios:** `departamento`, `municipio`, `codigo_dane`, `armas_medios`, `fecha_hecho`, `genero`, `grupo_etar_o`, `descripci_n_conducta`, `cantidad`.
- **Lesiones:** `fecha_hecho`, `cod_depto`, `departamento`, `cod_muni`, `municipio`, `cantidad`.

**Limitaciones y calidad**

- Las fuentes tienen unidades distintas (vehículos frente a víctimas) y no se deben sumar entre sí como si fueran una sola cifra de accidentes.
- En homicidios y lesiones una fila puede representar más de una víctima: los totales se calculan sumando `cantidad`, no contando filas. Por ejemplo, lesiones tiene 644.042 filas, pero suman 885.829 víctimas.
- Cada fuente usa un formato de fecha diferente: `MM/AAAA` (vehículos), `DD/MM/AAAA` como texto (homicidios) y fecha ISO (lesiones). Su normalización corresponde a AD-03.
- Ninguna fuente incluye coordenadas; la ubicación llega como máximo a nivel de municipio. Para cruzar fuentes conviene usar los códigos DANE y no los nombres, porque las mayúsculas y las tildes varían.
- La Policía Nacional advierte que sus cifras están sujetas a variación.

El detalle de las reglas de interpretación está en [`docs/data-sources.md`](docs/data-sources.md).

## Flujo de colaboración GitHub

**Issue → Branch → Commit → Pull Request → Review → Check → Merge → DoD → Done**

- Trabajar en ramas para cada cambio.
- Escribir nombres de ramas y mensajes de commit en inglés.
- Crear al menos un Pull Request real que explique qué cambia, por qué y cómo se verificó.
- Solicitar revisión de otro integrante cuando sea posible.
- Relacionar el PR con el Issue usando `Refs #N`; usar `Closes #N` solo cuando corresponda cerrar el Issue al integrar.
- No publicar contraseñas, tokens, claves ni archivos secretos.

## Pruebas y validación

Como mínimo, verificar manualmente el recorrido principal y un caso de búsqueda sin coincidencias o con datos incompletos. No marcar pruebas como superadas si no se ejecutaron.

Las pruebas automatizadas se ejecutan con:

```bash
python manage.py test
```

Cubren el cliente de la API, el catálogo de fuentes, el servicio de muestras y las vistas: respuesta correcta, respuesta vacía, error de conexión, fuente inválida y caché. Las pruebas automatizadas no se conectan a internet; la consulta real a datos.gov.co se comprueba abriendo `/fuentes/` en el navegador.

## Entregables

- Problema o hipótesis, beneficiario y fuente de datos.
- Aplicación Django funcional y URL del repositorio.
- README con instalación, ejecución y procedencia de los datos.
- Product Goal, Sprint Goal, Product Backlog, Sprint Backlog y DoD.
- GitHub Project e Issues actualizados.
- Ramas, commits y al menos un Pull Request revisado e integrado.
- Evidencias de pruebas y demostración.
- Pendientes y una acción concreta de mejora de la retrospectiva.

## Instalación y ejecución

Requisitos: **Python 3.12 o superior** (Django 6.1 no funciona con versiones anteriores) y conexión a internet para consultar datos.gov.co.

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\activate
# Linux / macOS:         source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador. La página de fuentes está en http://127.0.0.1:8000/fuentes/.

Opcional: datos.gov.co limita las consultas anónimas. Para un uso frecuente, crear un *app token* gratuito en el portal y definirlo en la variable de entorno `SOCRATA_APP_TOKEN` antes de iniciar el servidor. El token no debe subirse al repositorio.

---

**Estado del proyecto:** AD-01 (#5) terminado. AD-02 (#6) implementado: la aplicación consulta datos reales de tres fuentes de datos.gov.co, identifica su procedencia, maneja errores y respuestas vacías y documenta variables y limitaciones; falta su revisión e integración mediante Pull Request. AD-03 a AD-08 (#7 a #12) están pendientes.
