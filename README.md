# AccidentaData

Aplicación web desarrollada con **Python y Django** para consultar, procesar y visualizar datos abiertos relacionados con accidentalidad. El propósito es convertir datos públicos en información comprensible que ayude a los usuarios a explorar patrones y responder preguntas útiles.

> El conjunto de datos definitivo, su entidad publicadora, cobertura y limitaciones deben quedar registrados aquí cuando el equipo confirme la fuente seleccionada en datos.gov.co. No se deben presentar hipótesis como necesidades validadas ni datos de ejemplo como datos reales.

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

| Issue | Trabajo | Responsables |
|---|---|---|
| [#1 Configuración Django e interfaz inicial](../../issues/1) | Configurar Django y construir la interfaz inicial | ferneymbravog-stack, Joel90900 |
| [#2 Integración de datos abiertos](../../issues/2) | Integrar fuentes de datos abiertos | ferneymbravog-stack, jader-posso |
| [#3 Procesamiento y limpieza](../../issues/3) | Procesar, limpiar y preparar los datos | ferneymbravog-stack, Joel90900 |
| [#4 Filtros de búsqueda](../../issues/4) | Implementar búsqueda y filtros | Joel90900, jader-posso |
| [#5 Panel de estadísticas](../../issues/5) | Construir el panel de estadísticas | Joel90900, ferneymbravog-stack |
| [#6 Mapa interactivo](../../issues/6) | Incorporar mapa interactivo | Gonzalez82ZG, ferneymbravog-stack |
| [#7 Pruebas y validación](../../issues/7) | Ejecutar pruebas y validar el funcionamiento | Gonzalez82ZG, jader-posso |
| [#8 Documentación e integración](../../issues/8) | Consolidar documentación e integrar la entrega | Los cuatro integrantes |

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

- Portal: [datos.gov.co](https://www.datos.gov.co/)
- Conjunto de datos: **Pendiente de confirmar por el equipo**
- Entidad publicadora: **Pendiente**
- URL directa del conjunto: **Pendiente**
- Variables utilizadas: **Pendiente**
- Cobertura y periodo: **Pendiente**
- Limitaciones y calidad: **Pendiente**

La aplicación puede consumir una API o procesar un archivo CSV/JSON descargado. Ambas modalidades son válidas. Debe conservarse la atribución y explicarse si se utiliza una muestra.

## Flujo de colaboración GitHub

**Issue → Branch → Commit → Pull Request → Review → Check → Merge → DoD → Done**

- Trabajar en ramas para cada cambio.
- Escribir nombres de ramas y mensajes de commit en inglés.
- Crear al menos un Pull Request real que explique qué cambia, por qué y cómo se verificó.
- Solicitar revisión de otro integrante cuando sea posible.
- Relacionar el PR con el Issue usando `Refs #N`; usar `Closes #N` solo cuando corresponda cerrar el Issue al integrar.
- No publicar contraseñas, tokens, claves ni archivos secretos.

## Pruebas y validación

Como mínimo, verificar manualmente el recorrido principal y un caso de búsqueda sin coincidencias o con datos incompletos. Ejecutar `python manage.py test` cuando existan pruebas automatizadas apropiadas y registrar el resultado real. No marcar pruebas como superadas si no se ejecutaron.

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

Completar estos pasos cuando el equipo confirme la estructura y dependencias del proyecto. Como referencia general:

```bash
python -m venv .venv
# Activar el entorno virtual según el sistema operativo
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador.

---

**Estado del proyecto:** planificación e Issues iniciales registrados. Completar los datos de la fuente, validar cada criterio y actualizar los estados conforme avance el trabajo.
