# Retrospectiva del Sprint y Registro de Pendientes

Este documento registra los aprendizajes del equipo de trabajo de **AccidentaData**, las lecciones aprendidas durante el Sprint, los ítems pendientes para futuros incrementos y una acción de mejora concreta (SMART).

---

## 1. Balance del Sprint

### ¿Qué funcionó muy bien?
- **Consumo directo y desacoplado de la API Socrata:** La arquitectura modular en `accidentadata/data_sources/` y `processing/` permitió mantener las vistas Django limpias y aisladas de la lógica de red.
- **Normalización estricta temprana (AD-03):** Estandarizar las fechas a ISO y desglosar los códigos DIVIPOLA previno errores en cálculos estadísticos y en la visualización geográfica.
- **Visualización interactiva (AD-05 y AD-06):** La integración de Chart.js y Leaflet.js transformó tablas estáticas en un producto interactivo y atractivo visualmente.
- **Pruebas automatizadas (AD-07):** Contar con 89 pruebas unitarias permitió realizar refactorizaciones y mejoras de interfaz con cero regresiones.

### ¿Qué dificultades surgieron?
- **Disparidad de unidades de medida:** RUNT mide vehículos involucrados, mientras que DIJIN y MinDefensa miden víctimas acumuladas en la columna `cantidad`. Requirió especial cuidado para no sumar métricas incomparables.
- **Falta de coordenadas exactas en datos abiertos:** Ninguno de los 3 conjuntos oficiales publica latitud/longitud de los accidentes (solo departamento y municipio).
- **Límites de peticiones anónimas en Socrata:** Sin app token, datos.gov.co puede ralentizar consultas sucesivas masivas.

---

## 2. Acción Concreta de Mejora (Retrospective Improvement)

| Parámetro | Detalle de la Acción de Mejora |
|---|---|
| **Tema** | Optimización de Caché y Resiliencia ante fallos externos de la API |
| **Problema identificado** | Si la API de datos.gov.co experimenta latencia o caída temporal, las consultas de búsqueda no cacheadas podrían degradar la experiencia de usuario. |
| **Acción Concreta (SMART)** | **Implementar una capa de almacenamiento local persistente (SQLite / PostgreSQL) como fallback de contingencia y configurar un worker asíncrono con Celery o cron job para precargar semanalmente un snapshot de los 500 registros más recientes de cada departamento.** |
| **Responsables** | `ferneymbravog-stack` (Backend) y `Gonzalez82ZG` (Scrum Master / Pruebas) |
| **Criterio de éxito** | En caso de desconexión o fallo 503 de datos.gov.co, el sistema debe responder de inmediato con los datos del snapshot local anotando claramente en la UI: *"Datos en modo contingencia (última sincronización: DD/MM/AAAA)"*. |
| **Fecha límite** | Sprint 2 - Iteración 1 |

---

## 3. Registro de Pendientes para Próximos Sprints (Future Backlog)

Los siguientes requerimientos fueron identificados y registrados en el Product Backlog para siguientes iteraciones:

1. **AD-09: Integración de Geocodificación Automática de Municipios:**
   - Incorporar polígonos GeoJSON a nivel de municipio para permitir mapas de calor (heatmaps) basados en los códigos DIVIPOLA de 5 dígitos generados en AD-03.
2. **AD-10: Módulo de Series de Tiempo y Tendencias Mensuales:**
   - Visualizar curvas de tendencia histórica mensual y comparativas interanuales (ej. 2023 vs 2024 vs 2025) por departamento.
3. **AD-11: Autenticación con Token Socrata gestionado en UI:**
   - Permitir a administradores ingresar y rotar su propio `SOCRATA_APP_TOKEN` desde un panel de configuración seguro en Django.
4. **AD-12: Exportación de Informes en PDF:**
   - Generación automática de reportes ejecutivos en PDF con las gráficas y tablas de una consulta específica.
5. **AD-13: Pipeline de Integración Continua (CI) en GitHub Actions:**
   - Ejecución automática de `python manage.py test` y análisis de cobertura de código en cada Pull Request a `main`.
