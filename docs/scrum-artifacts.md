# Artefactos Scrum y Planificación del Proyecto: AccidentaData

Este documento consolida la planificación oficial del equipo, los objetivos, el estado del trabajo, la Definition of Done y los criterios de aceptación detallados para **AccidentaData**.

---

## 1. Product Goal (Objetivo del Producto)

> **Ofrecer una aplicación web interactiva y accesible que permita explorar, procesar y visualizar información pública de accidentalidad vial en Colombia en tiempo real mediante búsqueda avanzada, filtros precisos, análisis estadísticos gráficos y mapas territoriales, convirtiendo datos abiertos en conocimiento útil para la prevención y la toma de decisiones ciudadana e institucional.**

---

## 2. Sprint Goal (Objetivo del Sprint)

> **Entregar un incremento web completamente funcional, integrado y testeado en Django que consuma las tres fuentes oficiales de datos abiertos de datos.gov.co, normalice sus esquemas heterogéneos, ofrezca un panel de estadísticas dinámico con gráficos animados, un mapa interactivo de Colombia y una interfaz de búsqueda con validaciones y manejo predecible de casos borde.**

---

## 3. Product Backlog

El Product Backlog general prioriza el valor entregado al usuario final y a las entidades interesadas en seguridad vial:

| Orden | Código | Elemento del Backlog | Prioridad | Estimación | Valor de Negocio |
|---|---|---|---|---|---|
| 1 | **AD-01** | Configurar el proyecto Django, arquitectura base e interfaz inicial responsiva. | Alta | 3 SP | Base operativa del sistema web. |
| 2 | **AD-02** | Integrar cliente HTTP y catálogo de fuentes oficiales de datos.gov.co (RUNT, DIJIN, MinDefensa). | Alta | 5 SP | Disponibilidad de datos reales sin inventar información. |
| 3 | **AD-03** | Procesamiento, limpieza, normalización de fechas a ISO, validación DIVIPOLA y métricas de calidad. | Alta | 8 SP | Consistencia e integridad técnica de los datos. |
| 4 | **AD-04** | Motor de búsqueda y filtros SoQL en tiempo real con paginación y manejo de sin coincidencias. | Alta | 8 SP | Capacidad de consulta y filtrado granular por el usuario. |
| 5 | **AD-05** | Panel de estadísticas con indicadores oficiales, desgloses porcentuales y gráficos interactivos con animaciones. | Alta | 5 SP | Comprensión visual inmediata y síntesis analítica. |
| 6 | **AD-06** | Incorporar mapa interactivo territorial de Colombia con georreferenciación departamental. | Media | 5 SP | Análisis geoespacial de la concentración de siniestros. |
| 7 | **AD-07** | Suite de pruebas unitarias/integración y validación funcional automatizada (89 tests). | Alta | 5 SP | Robustez, fiabilidad y prevención de regresiones. |
| 8 | **AD-08** | Consolidación de documentación, revisión de PRs, recorrido demo y retrospectiva. | Alta | 3 SP | Trazabilidad académica, despliegue y transferencia de conocimiento. |

---

## 4. Sprint Backlog y Estado Verdadero del Trabajo

El equipo gestiona el trabajo mediante un tablero Kanban en GitHub Projects. Los estados oficiales son:
- **Backlog:** Pendiente y no seleccionado para el sprint actual.
- **Ready:** Criterios definidos y listo para iniciar desarrollo.
- **In Progress:** En desarrollo activo en rama de feature.
- **In Review:** Pull Request abierto, sujeto a revisión por pares y verificación de DoD.
- **Done:** Integrado en `main`, testeado y comprobado funcionalmente.

### Estado de los Issues del Sprint:

| Código | Issue GitHub | Título / Alcance | Responsables | Estado Actual |
|---|---|---|---|---|
| **AD-01** | [#5](../../issues/5) | Configurar Django y construir la interfaz inicial | ferneymbravog-stack, Joel90900 | **Done** |
| **AD-02** | [#6](../../issues/6) | Integrar fuentes de datos abiertos (RUNT, DIJIN, MinDefensa) | ferneymbravog-stack, jader-posso | **Done** |
| **AD-03** | [#7](../../issues/7) | Procesar, limpiar y preparar los datos (ISO, DIVIPOLA, nulos) | ferneymbravog-stack, Joel90900 | **Done** |
| **AD-04** | [#8](../../issues/8) | Implementar búsqueda y filtros SoQL en tiempo real | Joel90900, jader-posso | **Done** |
| **AD-05** | [#9](../../issues/9) | Construir panel de estadísticas con gráficos animados (Chart.js) | Joel90900, ferneymbravog-stack | **Done** |
| **AD-06** | [#10](../../issues/10) | Incorporar mapa interactivo de Colombia (Leaflet.js) | Gonzalez82ZG, ferneymbravog-stack | **Done** |
| **AD-07** | [#11](../../issues/11) | Ejecutar pruebas automatizadas (89 tests) y validación de errores | Gonzalez82ZG, jader-posso | **Done** |
| **AD-08** | [#12](../../issues/12) | Consolidar documentación, Pull Request integrado y demo | Todos los integrantes | **Done** |

---

## 5. Definition of Done (DoD)

Para considerar un elemento o incremento como **Terminado (Done)**, el equipo exige el cumplimiento del 100% de los siguientes criterios:

1. **Compilación y Ejecución:** Django inicia limpiamente sin advertencias ni errores bloqueantes (`python manage.py runserver`).
2. **Recorrido de Usuario Verificado:** Se completa el recorrido completo desde un navegador web sin fallos de interfaz ni bloqueos de red.
3. **Datos Reales y Atribución:** Todas las cifras provienen de datos reales de datos.gov.co; la fuente, licencia (CC BY-SA 4.0) y limitaciones están explícitamente atribuidas.
4. **Criterios de Aceptación del Issue Cumplidos:** Cada criterio específico del issue se encuentra programado y validado.
5. **Manejo de Casos Borde:** Las entradas inválidas, búsquedas sin coincidencias o caídas de conexión se gestionan con mensajes amigables y estados HTTP correctos (ej. 404 para fuentes desconocidas).
6. **Pruebas Automatizadas:** La suite completa de pruebas unitarias (`python manage.py test`) corre en verde (89 tests superados).
7. **Control de Versiones y Revisión:** Los cambios se desarrollaron en ramas temáticas, cuentan con commits descriptivos en inglés, un Pull Request formal revisado por al menos un compañero e integrado en `main`.
8. **Documentación Actualizada:** El README y los documentos en `docs/` permiten a cualquier persona clonar, instalar y ejecutar el proyecto desde cero.
9. **GitHub Sincronizado:** El Project y los Issues reflejan fielmente el estado terminado del incremento.

---

## 6. Criterios de Aceptación por Issue

### AD-01: Configuración base e Interfaz Inicial
- [x] Django 6.1 configurado con estructura modular (`accidentadata`, `accidentes`, `config`).
- [x] Interfaz HTML responsiva y accesible con navegación consistente.
- [x] Enrutamiento funcional hacia `/`, `/fuentes/`, `/buscar/` y `/estadisticas/`.

### AD-02: Integración de Fuentes Oficiales
- [x] Cliente HTTP Socrata con validación de parámetros `$limit` y `$offset`.
- [x] Catálogo con las 3 fuentes oficiales verificadas (IDs `6jmc-vaxk`, `ha6j-pa2r`, `ntej-qq7v`).
- [x] Muestra de datos reales en tiempo real con sistema de caché de 10 minutos.

### AD-03: Procesamiento y Limpieza de Datos
- [x] Normalización de fechas heterogéneas (`MM/AAAA`, `DD/MM/AAAA`, ISO) a estándar ISO `AAAA-MM-DD`.
- [x] Estandarización de códigos DANE a DIVIPOLA de 2 dígitos (departamento) y 5 dígitos (municipio).
- [x] Manejo de valores nulos o cadenas ausentes sustituidos por `NO REPORTADO` o `—`.
- [x] Modo de comparación interactivo: Vista Procesada vs Vista Cruda en `/fuentes/`.

### AD-04: Búsqueda y Filtros
- [x] Formulario dinámico según los campos soportados por la fuente seleccionada.
- [x] Construcción segura de cláusula SoQL `$where` con listas blancas.
- [x] Conteo oficial en toda la fuente (`total_rows` y métrica acumulada en víctimas/vehículos).
- [x] Paginación estable de 20 en 20 registros.
- [x] Mensajes claros para búsquedas sin coincidencias y validación en vivo de campos inválidos.

### AD-05: Panel de Estadísticas y Gráficos Animados
- [x] Cálculo de indicadores: total de métrica oficial, promedio por registro, cobertura de departamentos y municipios.
- [x] Desgloses porcentuales automáticos por gravedad, departamentos y tipo de vehículo/arma.
- [x] Integración de Chart.js con gráficos animados (barras horizontales y gráfico doughnut).
- [x] Función interactiva para copiar resumen estadístico al portapapeles.

### AD-06: Mapa Interactivo Territorial
- [x] Integración de Leaflet.js centrado en Colombia con tiles cartográficos libres de fallos.
- [x] Representación de los 33 departamentos con coordenadas centroides exactas.
- [x] Marcadores proporcionales interactivos con popups informativos y enlace directo para filtrar en Búsqueda.

### AD-07: Pruebas y Aseguramiento de Calidad
- [x] 89 pruebas unitarias automatizadas cubriendo clientes, transformadores, estadísticas, formularios, vistas y georreferenciación.
- [x] Verificación de respuestas 200, 404, validaciones de seguridad ante inyección en URLs y caché.

### AD-08: Consolidación y Entrega
- [x] Consolidación de README.md con guía de instalación paso a paso.
- [x] Registro de Pull Request revisado e integrado.
- [x] Guía de demostración comprobada paso a paso.
- [x] Registro de retrospectiva con mejora SMART implementada.
