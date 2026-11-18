# Guía de Demostración del Recorrido Disponible (Demo Walkthrough)

Esta guía presenta **únicamente funcionalidades reales y comprobadas** en vivo en la aplicación **AccidentaData**, listas para ser demostradas ante el Product Owner, stakeholders o evaluadores.

---

## Preparación Previa a la Demostración

1. Asegurarse de tener el entorno virtual activo:
   ```powershell
   # En Windows PowerShell:
   .\.venv\Scripts\activate
   ```
2. Ejecutar la suite de pruebas para confirmar el estado verde:
   ```bash
   python manage.py test
   # Debe responder: Ran 89 tests in ~1.5s - OK
   ```
3. Iniciar el servidor local de desarrollo:
   ```bash
   python manage.py runserver
   ```
4. Abrir un navegador web en: `http://127.0.0.1:8000/`

---

## Recorrido Guiado Paso a Paso (Demostración)

### Paso 1: Página de Inicio y Recorrido Guiado Interactivo
- **URL:** `http://127.0.0.1:8000/`
- **Qué observar y demostrar:**
  1. **Encabezado y Estado en Vivo:** Observar el badge pulsante `🟢 API SOCRATA DATOS.GOV.CO EN VIVO` que confirma la conectividad con el portal oficial.
  2. **Hero Interactivo:** Título dinámico con gradiente animado, subtítulo explicativo y botones con elevación hover.
  3. **Contadores de Impacto KPI:** Visualizar los contadores superiores que reflejan los volúmenes reales de las fuentes (450.335+ vehículos, 98.430+ víctimas fatales, 885.829+ víctimas lesionadas y 33 departamentos).
  4. **Componente de Recorrido Guiado ("Tour de la Aplicación"):**
     - Hacer clic en los botones `1️⃣ Fuentes Oficiales`, `2️⃣ Limpieza y Normalización`, `3️⃣ Búsqueda SoQL`, `4️⃣ Panel Estadístico` y `5️⃣ Mapa Territorial`.
     - Observar cómo el panel central actualiza dinámicamente la descripción, los criterios de aceptación cumplidos y el botón de acceso directo.
  5. **Mapa Interactivo de Colombia (Preview):** Pasar el mouse sobre los círculos azules de los departamentos para ver la animación de expansión y hacer clic para ver el popup con enlace directo a búsqueda.

---

### Paso 2: Catálogo de Fuentes y Comparativa Procesado vs Crudo
- **URL:** `http://127.0.0.1:8000/fuentes/`
- **Qué observar y demostrar:**
  1. **Tarjetas de Catálogo Oficial:** Se presentan las 3 fuentes (RUNT, DIJIN, MinDefensa) con su entidad, frecuencia y botón de consulta.
  2. **Consulta en Tiempo Real:** Hacer clic en "Ver muestra" en la fuente *Homicidios en accidente de tránsito* (`?fuente=police_fatalities`).
  3. **Métricas de Calidad de Datos (AD-03):** Se despliegan 5 tarjetas KPI con: Registros procesados, Víctimas reportadas (suma real de `cantidad`), Fechas estandarizadas a formato ISO, Ubicación completa (Dpto + Muni) y Valores ausentes tratados.
  4. **Alternancia Interactiva Procesado / Crudo:**
     - Hacer clic en el botón `✨ Datos procesados y normalizados (AD-03)`: Observar la tabla con columnas limpias, fechas en `AAAA-MM-DD` y valores ausentes sustituidos por `—`.
     - Hacer clic en el botón `📄 Datos originales (crudos)`: Observar la tabla original tal como la expone Socrata (fechas en texto `DD/MM/AAAA` y campos en crudo).
  5. **Atribución Legal:** Revisar la sección inferior con la licencia oficial **CC BY-SA 4.0**, ID de conjunto y advertencias de variación de la Policía Nacional.

---

### Paso 3: Búsqueda Avanzada y Filtros SoQL
- **URL:** `http://127.0.0.1:8000/buscar/`
- **Qué observar y demostrar:**
  1. **Selección de Fuente:** Hacer clic en la pestaña *Vehículos involucrados en un accidente (RUNT)* (`?fuente=runt_vehicles`).
  2. **Formulario Dinámico:** Observar que aparecen los campos específicos de esta fuente: Departamento, Municipio, Año, Gravedad del accidente y Tipo de vehículo.
  3. **Búsqueda con Filtros Combinados:**
     - Seleccionar Departamento: `Antioquia`.
     - Año: `2024`.
     - Gravedad: `CON MUERTOS`.
     - Hacer clic en **Buscar**: Observar el feedback del botón y los resultados devueltos en vivo desde la API de datos.gov.co.
  4. **Pills de Filtros Activos:** Revisar los badges interactivos `🎯 Departamento: Antioquia`, `🎯 Año: 2024`, `🎯 Gravedad del accidente: CON MUERTOS`.
  5. **Manejo de Casos Borde y Búsquedas sin Coincidencias:**
     - Probar en Municipio: `ZZZ_INEXISTENTE`.
     - Enviar la búsqueda: Observar el mensaje claro y no bloqueante: *"No hay registros que coincidan con estos filtros. Prueba con menos filtros..."*.
  6. **Exportación a CSV:** En una búsqueda con resultados, hacer clic en `📥 Descargar página a CSV` y verificar que el archivo `.csv` se genera de inmediato en el navegador.

---

### Paso 4: Panel de Estadísticas y Gráficos Animados
- **URL:** `http://127.0.0.1:8000/estadisticas/`
- **Qué observar y demostrar:**
  1. **Selección de Fuente:** Alternar entre *Vehículos*, *Homicidios* y *Lesiones*.
  2. **KPIs del Resumen:** Tarjetas con Total acumulado según unidad oficial (vehículos o víctimas), Promedio por registro, Cobertura geográfica (ej. 24 departamentos / 120 municipios observados) y Departamento principal con su porcentaje.
  3. **Gráficos Dinámicos con Animaciones (Chart.js):**
     - **Gráfico 1 (Barras Horizontales):** Concentración de siniestros por los principales departamentos. Pasar el cursor sobre cada barra para ver los tooltips animados con el porcentaje exacto.
     - **Gráfico 2 (Doughnut / Dona):** Desglose categórico interactivo (por Gravedad de accidente, Grupo etario o Modalidad).
  4. **Mapa Territorial Interactivo (Leaflet.js):**
     - Ubicado en la sección inferior de estadísticas.
     - Los círculos de cada departamento tienen un radio proporcional a la concentración de registros en esa fuente.
     - Hacer clic en cualquier círculo: se abre un popup estilizado que muestra el departamento, la cantidad, el porcentaje nacional y un botón directo para consultar ese departamento en la página de Búsqueda.
  5. **Copiar Resumen:** Hacer clic en `📋 Copiar resumen al portapapeles` para obtener el texto formateado al instante.
