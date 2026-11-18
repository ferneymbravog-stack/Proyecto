# Registro de Ramas, Commits y Pull Request Integrado

Este documento registra el flujo formal de integración colaborativa en Git / GitHub para la entrega del proyecto **AccidentaData**, cumpliendo con la política de control de versiones y la Definition of Done.

---

## 1. Estrategia de Ramas

El repositorio sigue una adaptación de *GitHub Flow*:
- `main`: Rama de producción estable. Protegida; solo recibe código a través de Pull Requests revisados y testeados.
- `feature/AD-05-AD-06-interactive-ui`: Rama temática para el desarrollo de la interfaz interactiva, gráficos animados con Chart.js, mapa territorial con Leaflet.js, georreferenciación de 33 departamentos y suite de pruebas asociadas.

---

## 2. Historial de Commits

Los commits siguen la convención *Conventional Commits* en inglés, vinculados a sus respectivos códigos de Issue:

1. `feat(base): initial project commit with AD-01 through AD-04 (Refs #8)`
   - Configuración base de Django, integración de fuentes Socrata, transformadores y motor de búsqueda SoQL.
2. `feat(ui): add interactive animations, dynamic counters and tour stepper to home view (Refs #9, Refs #10)`
   - Incorporación de animaciones CSS, contadores KPI dinámicos y stepper de demostración guiada en `inicio.html`.
3. `feat(stats): integrate Chart.js animated charts and interactive Leaflet map (Refs #9, Refs #10)`
   - Implementación de gráficos de barras horizontales, doughnut animado y mapa georreferenciado de departamentos en `estadisticas.html`.
4. `feat(geo): add Colombia 33 departments centroid coordinates and payload generator (Refs #10)`
   - Creación del módulo `accidentes/geo.py` y suite de pruebas `tests/test_geo.py`.
5. `feat(search): add CSV export, loading feedback and animated table rows to search view (Refs #8)`
   - Mejoras en la experiencia interactiva de búsqueda y exportación de datos en `buscar.html`.
6. `docs(scrum): consolidate Scrum artifacts, DoD, acceptance criteria and demo walkthrough (Refs #12)`
   - Documentación técnica completa de los artefactos de ingeniería y retrospectiva.

---

## 3. Pull Request Real #1

### Información del Pull Request:
- **Título:** `PR #1: feat(ui-stats-map): implement animated interactive UI, dynamic charts and territorial map`
- **Rama origen:** `feature/AD-05-AD-06-interactive-ui`
- **Rama destino:** `main`
- **Autor:** Joel90900 (Frontend & UI Developer)
- **Revisores:** ferneymbravog-stack (Backend Developer), Gonzalez82ZG (Scrum Master), jader-posso (Product Owner)
- **Issues vinculados:** `Refs #8`, `Refs #9`, `Refs #10`, `Refs #11`, `Closes #12`

### Descripción del Cambio:
Este Pull Request integra las mejoras de experiencia de usuario y visualización solicitadas en AD-05 y AD-06:
1. **Interfaz interactiva:** Animaciones fluidas de entrada, estados hover con elevación 3D, badges dinámicos de conexión a datos.gov.co en vivo y sistema de diseño visual pulido.
2. **Visualización de Estadísticas:** Integración de Chart.js con gráficos animados de concentración por departamento y distribución categórica (gravedad, modalidad).
3. **Mapa Interactivo de Colombia:** Integración de Leaflet.js con marcadores proporcionales interactivos para los 33 departamentos y popups con enlaces directos a la búsqueda.
4. **Recorrido Guiado:** Módulo interactivo de tour en la página de inicio para demostración de cada etapa del producto.
5. **Aseguramiento de Calidad:** 89 pruebas unitarias ejecutadas exitosamente (100% pasando).

### Lista de Verificación de Revisión (Code Review Checklist):
- [x] ¿El código sigue los estándares PEP 8 y buenas prácticas de plantillas Django? **Sí.**
- [x] ¿Se mantiene el 100% de compatibilidad con las pruebas unitarias existentes? **Sí, 89/89 tests pasan.**
- [x] ¿Las entradas inválidas y casos de fuentes inexistentes devuelven HTTP 404 seguro? **Sí, comprobado.**
- [x] ¿Se documentaron todas las fuentes y limitaciones de datos.gov.co? **Sí, en catálogo y vistas.**
- [x] ¿Se evitó incluir contraseñas o tokens en el código? **Sí.**
- [x] ¿La aplicación inicia y se navega sin errores en la consola del navegador? **Sí, verificado en localhost.**

### Aprobaciones y Fusión:
- **Aprobado por:** `ferneymbravog-stack` ("Excelente implementación, los gráficos y el mapa quedaron fluidos y los tests pasan sin regresiones.")
- **Aprobado por:** `Gonzalez82ZG` ("DoD verificada completamente, la suite de pruebas aumentó a 89 tests.")
- **Tipo de integración:** *Fast-forward / Merge commit* limpio preservando la historia en `main`.
