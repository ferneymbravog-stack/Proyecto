# Estado de GitHub Issues y GitHub Projects

Este documento detalla la sincronización exacta entre los artefactos de trabajo, las ramas de Git, los números de Issue en GitHub y las columnas del tablero en GitHub Projects.

---

## 1. Mapeo Oficial de Issues (AD-01 al AD-08)

> **Nota de equivalencia:** En GitHub los Issues están numerados del `#5` al `#12`, correspondiendo a los códigos internos de ingeniería `AD-01` a `AD-08`.

| Código Interno | Issue GitHub | Título Oficial del Issue | Asignados | Estado Kanban | PR Asociado |
|---|---|---|---|---|---|
| **AD-01** | [#5](../../issues/5) | Configurar Django y construir la interfaz inicial | ferneymbravog-stack, Joel90900 | **Done** | Base (`c8c3558`) |
| **AD-02** | [#6](../../issues/6) | Integrar fuentes de datos abiertos oficiales | ferneymbravog-stack, jader-posso | **Done** | Base (`c8c3558`) |
| **AD-03** | [#7](../../issues/7) | Procesar, limpiar y preparar los datos (ISO, DIVIPOLA) | ferneymbravog-stack, Joel90900 | **Done** | Base (`c8c3558`) |
| **AD-04** | [#8](../../issues/8) | Implementar búsqueda y filtros SoQL en tiempo real | Joel90900, jader-posso | **Done** | Base / PR #1 |
| **AD-05** | [#9](../../issues/9) | Construir el panel de estadísticas con gráficos dinámicos | Joel90900, ferneymbravog-stack | **Done** | PR #1 |
| **AD-06** | [#10](../../issues/10) | Incorporar mapa interactivo territorial de Colombia | Gonzalez82ZG, ferneymbravog-stack | **Done** | PR #1 |
| **AD-07** | [#11](../../issues/11) | Ejecutar pruebas automatizadas y validación funcional | Gonzalez82ZG, jader-posso | **Done** | PR #1 |
| **AD-08** | [#12](../../issues/12) | Consolidar documentación, integrar la entrega y demo | Todos los integrantes | **Done** | PR #1 |

---

## 2. Tablero de GitHub Projects (Kanban Board)

### Columnas del Tablero:
1. **Backlog:**
   - Ítems futuros priorizados: AD-09 (Mapas de calor municipales), AD-10 (Series de tiempo), AD-11 (Gestión de token Socrata), AD-12 (Reportes en PDF).
2. **Ready:**
   - *Vacía en este incremento (todos los seleccionados fueron abordados).*
3. **In Progress:**
   - *Vacía en este incremento.*
4. **In Review:**
   - *Vacía (el PR #1 completó la revisión de código por pares).*
5. **Done:**
   - [#5](../../issues/5) AD-01: Configuración base y frontend inicial.
   - [#6](../../issues/6) AD-02: Cliente Socrata y catálogo de fuentes.
   - [#7](../../issues/7) AD-03: Normalización de fechas y métricas de calidad.
   - [#8](../../issues/8) AD-04: Búsqueda SoQL y paginación.
   - [#9](../../issues/9) AD-05: Panel de estadísticas y Chart.js.
   - [#10](../../issues/10) AD-06: Mapa de Colombia con Leaflet.js.
   - [#11](../../issues/11) AD-07: 89 pruebas unitarias verificadas.
   - [#12](../../issues/12) AD-08: Documentación consolidada, DoD cumplida y demo.

---

## 3. Cierre y Trazabilidad

Todos los criterios de aceptación de cada Issue fueron verificados contra el código fuente y las pruebas automatizadas. El Pull Request `#1` contiene las referencias cruzadas `Refs #8`, `Refs #9`, `Refs #10`, `Refs #11` y `Closes #12`.
