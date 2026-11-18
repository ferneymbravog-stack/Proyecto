# AccidentaData | Analítica Vial en Colombia

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django 6.1](https://img.shields.io/badge/Django-6.1-092E20.svg?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Tests: 89 passing](https://img.shields.io/badge/Tests-89%20passing-10b981.svg)](tests/)

Plataforma web desarrollada con **Python y Django** para consultar, procesar, normalizar y visualizar datos abiertos oficiales sobre accidentalidad y siniestralidad vial en Colombia en tiempo real. Transforma datos públicos heterogéneos de **datos.gov.co** en información comprensible mediante un panel de estadísticas dinámico, gráficos animados interactivos, georreferenciación territorial con mapas y un motor de búsqueda con filtros avanzados SoQL.

---

## Índice

1. [Descripción del Proyecto y Problema](#descripción-del-proyecto-y-problema)
2. [Instalación y Ejecución Paso a Paso](#instalación-y-ejecución-paso-a-paso)
3. [Fuente de Datos, Entidades y Limitaciones](#fuente-de-datos-entidades-y-limitaciones)
4. [Objetivos y Artefactos Scrum](#objetivos-y-artefactos-scrum)
5. [Definition of Done (DoD) y Criterios de Aceptación](#definition-of-done-dod-y-criterios-de-aceptación)
6. [Flujo Git, Ramas y Pull Request Integrado](#flujo-git-ramas-y-pull-request-integrado)
7. [Guía de Demostración del Recorrido Disponible](#guía-de-demostración-del-recorrido-disponible)
8. [Pendientes y Acción de Mejora de la Retrospectiva](#pendientes-y-acción-de-mejora-de-la-retrospectiva)
9. [Equipo y Responsabilidades](#equipo-y-responsabilidades)

---

## Descripción del Proyecto y Problema

En Colombia, la información sobre accidentalidad vial se encuentra fragmentada entre múltiples entidades públicas (Ministerio de Transporte / RUNT, Dirección General de la Policía Nacional / DIJIN y Ministerio de Defensa Nacional). Cada entidad publica sus conjuntos de datos en **datos.gov.co** con esquemas dispares, formatos de fecha heterogéneos (`MM/AAAA`, `DD/MM/AAAA`, ISO), diferentes unidades de conteo (vehículos involucrados vs. víctimas) y distintos niveles de codificación geográfica.

**AccidentaData** resuelve este problema ofreciendo una solución integral:
- **Consumo directo en tiempo real** de la API pública Socrata.
- **Normalización estandarizada** a formatos ISO y códigos DANE DIVIPOLA de 2 y 5 dígitos.
- **Métricas de calidad de datos** y alternancia interactiva entre datos procesados y crudos.
- **Panel de estadísticas con gráficos dinámicos animados** (Chart.js).
- **Mapa interactivo territorial** con georreferenciación de los 33 departamentos (Leaflet.js).
- **Motor de búsqueda avanzado** con validación estricta y cláusulas SoQL seguras.

---

## Instalación y Ejecución Paso a Paso

Cualquier persona puede instalar y ejecutar el proyecto siguiendo estos sencillos pasos:

### 1. Requisitos Previos
- **Python 3.12 o superior** (imprescindible para compatibilidad con las librerías del proyecto).
- **Git** instalado en el sistema.
- Conexión a internet para la consulta de datos en vivo de datos.gov.co.

### 2. Clonar o Descargar el Proyecto
```bash
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-main
```

### 3. Crear y Activar el Entorno Virtual

- **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
  *(Si PowerShell restringe la ejecución de scripts, ejecutar previamente: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **En Linux / macOS (Bash / Zsh):**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Instalar Dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Aplicar Migraciones de la Base de Datos
```bash
python manage.py migrate
```

### 6. Ejecutar la Suite de Pruebas Automatizadas
Verificar que los 89 tests unitarios y de integración pasen con éxito (sin necesidad de conexión a internet):
```bash
python manage.py test
```
*Salida esperada:*
```text
Creating test database for alias 'default'...
.........................................................................................
Ran 89 tests in ~1.5s
OK
Destroying test database for alias 'default'...
```

### 7. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```

### 8. Explorar la Aplicación en el Navegador
Abrir las siguientes rutas locales:
- 🏠 **Inicio y Recorrido Guiado:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📊 **Panel de Estadísticas, Gráficos y Mapa:** [http://127.0.0.1:8000/estadisticas/](http://127.0.0.1:8000/estadisticas/)
- 📑 **Catálogo de Fuentes (Procesado vs Crudo):** [http://127.0.0.1:8000/fuentes/](http://127.0.0.1:8000/fuentes/)
- 🔍 **Búsqueda SoQL y Filtros:** [http://127.0.0.1:8000/buscar/](http://127.0.0.1:8000/buscar/)

*(Opcional: Para evitar limitaciones en consultas masivas desde una misma IP, configurar la variable de entorno `SOCRATA_APP_TOKEN=<tu_token>` antes de iniciar el servidor).*

---

## Fuente de Datos, Entidades y Limitaciones

La aplicación consulta en tiempo real la API pública Socrata de [datos.gov.co](https://www.datos.gov.co/) (`https://www.datos.gov.co/resource/{id}.json`). Metadatos verificados el 13 de noviembre de 2026:

| Conjunto de datos | ID Socrata | Entidad publicadora | Cobertura y periodo | Actualización | Unidad de conteo oficial |
|---|---|---|---|---|---|
| [Vehículos involucrados en accidentes](https://www.datos.gov.co/d/6jmc-vaxk) | `6jmc-vaxk` | Ministerio de Transporte (RUNT) | Nacional · ene. 2022 – sep. 2026 | Semestral | **Vehículo involucrado** |
| [Homicidios en accidente de tránsito](https://www.datos.gov.co/d/ha6j-pa2r) | `ha6j-pa2r` | Dirección General de la Policía Nacional (DIJIN) | Nacional · ene. 2010 – jul. 2026 | Trimestral | **Víctimas: suma de `cantidad`** |
| [Lesiones en accidentes de tránsito](https://www.datos.gov.co/d/ntej-qq7v) | `ntej-qq7v` | Ministerio de Defensa Nacional | Nacional · ene. 2003 – sep. 2026 | Mensual | **Víctimas: suma de `cantidad`** |

### Atribución y Licencia
Las tres fuentes se publican con licencia **Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0)**, que autoriza la reutilización y adaptación citando la autoría original.

### Limitaciones Identificadas y Calidad de Datos
1. **Disparidad de Unidades:** Las fuentes no deben sumarse aritméticamente entre sí. RUNT mide *vehículos*; DIJIN y MinDefensa miden *víctimas*.
2. **Filas que agrupan múltiples víctimas:** En lesiones y homicidios, una sola fila puede contener varias víctimas. El total real se calcula sumando la columna `cantidad` y no contando filas.
3. **Formatos de fecha dispares:** RUNT publica `MM/AAAA` (texto); DIJIN publica `DD/MM/AAAA` (texto); MinDefensa publica fechas ISO. Se normalizan a `AAAA-MM-DD` mediante el módulo `accidentadata/processing/cleaners.py`.
4. **Ausencia de coordenadas geográficas exactas:** Ninguna de las 3 fuentes publica latitud y longitud a nivel de punto de choque. La georreferenciación territorial de AccidentaData utiliza los centroides oficiales de los 33 departamentos según códigos DANE DIVIPOLA (`accidentes/geo.py`).
5. **Variación de cifras policiales:** La Policía Nacional advierte que sus datos están en proceso continuo de consolidación jurídica con la Fiscalía General de la Nación.

El detalle completo de las reglas técnicas se encuentra en [`docs/data-sources.md`](docs/data-sources.md).

---

## Objetivos y Artefactos Scrum

### Product Goal (Objetivo del Producto)
> *Ofrecer una aplicación web interactiva y accesible que permita explorar, procesar y visualizar información pública de accidentalidad vial en Colombia en tiempo real mediante búsqueda avanzada, filtros precisos, análisis estadísticos gráficos y mapas territoriales, convirtiendo datos abiertos en conocimiento útil para la prevención y la toma de decisiones ciudadana e institucional.*

### Sprint Goal (Objetivo del Sprint)
> *Entregar un incremento web completamente funcional, integrado y testeado en Django que consuma las tres fuentes oficiales de datos abiertos de datos.gov.co, normalice sus esquemas heterogéneos, ofrezca un panel de estadísticas dinámico con gráficos animados, un mapa interactivo de Colombia y una interfaz de búsqueda con validaciones y manejo predecible de casos borde.*

### Product Backlog
1. **AD-01:** Configuración base del proyecto Django y diseño de la interfaz web inicial.
2. **AD-02:** Integración del cliente HTTP Socrata y catálogo de datos abiertos de datos.gov.co.
3. **AD-03:** Motor de procesamiento, normalización de fechas a ISO, DIVIPOLA y métricas de calidad.
4. **AD-04:** Búsqueda avanzada con filtros SoQL en tiempo real y paginación estable.
5. **AD-05:** Panel de estadísticas con indicadores oficiales, desgloses y gráficos interactivos con animaciones (Chart.js).
6. **AD-06:** Visualización geográfica y mapa interactivo territorial de Colombia (Leaflet.js).
7. **AD-07:** Suite de pruebas unitarias automatizadas y validación funcional.
8. **AD-08:** Consolidación de documentación, revisión de PRs, recorrido demo y retrospectiva.

### Sprint Backlog y Mapeo de GitHub Issues
En GitHub los Issues están numerados del `#5` al `#12`, correspondiendo a los códigos de ingeniería `AD-01` a `AD-08`:

| Código | Issue GitHub | Trabajo / Componente | Responsables | Estado Kanban |
|---|---|---|---|---|
| **AD-01** | [#5](../../issues/5) | Configurar Django y arquitectura inicial | ferneymbravog-stack, Joel90900 | **Done** |
| **AD-02** | [#6](../../issues/6) | Integrar fuentes de datos abiertos | ferneymbravog-stack, jader-posso | **Done** |
| **AD-03** | [#7](../../issues/7) | Procesar, limpiar y normalizar datos | ferneymbravog-stack, Joel90900 | **Done** |
| **AD-04** | [#8](../../issues/8) | Búsqueda y filtros SoQL en tiempo real | Joel90900, jader-posso | **Done** |
| **AD-05** | [#9](../../issues/9) | Panel de estadísticas y gráficos animados | Joel90900, ferneymbravog-stack | **Done** |
| **AD-06** | [#10](../../issues/10) | Mapa territorial interactivo de Colombia | Gonzalez82ZG, ferneymbravog-stack | **Done** |
| **AD-07** | [#11](../../issues/11) | Pruebas automatizadas (89 tests) y calidad | Gonzalez82ZG, jader-posso | **Done** |
| **AD-08** | [#12](../../issues/12) | Consolidación, Pull Request y demo | Todos los integrantes | **Done** |

El detalle de la planificación y artefactos se encuentra en [`docs/scrum-artifacts.md`](docs/scrum-artifacts.md).

---

## Definition of Done (DoD) y Criterios de Aceptación

Un incremento se considera **Done** únicamente cuando:
- [x] Django inicia y opera sin advertencias ni errores bloqueantes (`python manage.py runserver`).
- [x] Se completa el recorrido completo desde el navegador (Inicio → Fuentes → Búsqueda → Estadísticas → Mapa).
- [x] Se utilizan datos reales de datos.gov.co con atribución explícita de entidad y licencia.
- [x] Las entradas inválidas y búsquedas vacías devuelven estados HTTP limpios (404) y mensajes amigables.
- [x] 89 pruebas unitarias automatizadas corren en verde (`python manage.py test`).
- [x] Los cambios se desarrollaron en ramas, con commits en inglés, y un Pull Request real revisado e integrado en `main`.
- [x] El README permite a otra persona instalar y ejecutar el proyecto desde cero.
- [x] GitHub Issues y Projects reflejan fielmente el estado verdadero del trabajo.

---

## Flujo Git, Ramas y Pull Request Integrado

El equipo opera bajo el flujo **Issue → Branch → Commit → Pull Request → Review → Check → Merge → DoD → Done**:

- **Rama principal:** `main` (código estable verificado).
- **Rama de desarrollo:** `feature/AD-05-AD-06-interactive-ui` (incorporación de interfaz interactiva, animaciones, Chart.js, mapa Leaflet y 89 tests).
- **Pull Request Real #1:**
  - **Título:** `PR #1: feat(ui-stats-map): implement animated interactive UI, dynamic charts and territorial map`
  - **Ramas:** `feature/AD-05-AD-06-interactive-ui` ➔ `main`
  - **Revisores:** `ferneymbravog-stack`, `Gonzalez82ZG`
  - **Estado:** Revisado, aprobado y fusionado en `main`.

El registro exhaustivo de la revisión de código por pares se encuentra en [`docs/pull-requests.md`](docs/pull-requests.md).

---

## Guía de Demostración del Recorrido Disponible

La demostración presenta **únicamente funcionalidades reales y comprobadas**:

1. **Recorrido Guiado en Inicio (`/`):**
   - Badge animado de estado en vivo de la API Socrata.
   - Stepper interactivo de 5 pasos donde el usuario navega entre Fuentes, Limpieza, Búsqueda, Estadísticas y Mapa.
   - Mapa preview interactivo de los 33 departamentos de Colombia con popups dinámicos.
2. **Exploración de Fuentes (`/fuentes/`):**
   - Consulta en vivo de muestras de 10 registros reales por fuente.
   - Alternancia entre el modo *Datos procesados y normalizados* (con métricas de calidad) y el modo *Datos originales crudos*.
3. **Búsqueda SoQL en Tiempo Real (`/buscar/`):**
   - Filtros por departamento, municipio, año y gravedad.
   - Conteo en toda la base de datos oficial.
   - Mensajes específicos de sin coincidencias y validación en vivo.
   - Exportación instantánea a CSV.
4. **Panel de Estadísticas y Gráficos Animados (`/estadisticas/`):**
   - Gráfico de barras horizontales de concentración regional con animaciones de carga (Chart.js).
   - Gráfico de dona de desglose categórico interactivo.
   - Mapa de Colombia con círculos proporcionales y navegación directa a la búsqueda por departamento (Leaflet.js).
   - Botón interactivo para copiar el resumen al portapapeles.

El libreto completo de demostración paso a paso está en [`docs/demo-walkthrough.md`](docs/demo-walkthrough.md).

---

## Pendientes y Acción de Mejora de la Retrospectiva

### Pendientes Registrados para el Siguiente Sprint:
1. **AD-09:** Geocodificación municipal mediante polígonos GeoJSON y mapas de calor.
2. **AD-10:** Análisis temporal con series de tiempo y comparativas interanuales.
3. **AD-11:** Módulo administrativo para gestión de credenciales Socrata.
4. **AD-12:** Generador de reportes ejecutivos en PDF.
5. **AD-13:** Pipeline de Integración Continua (CI) en GitHub Actions.

### Acción Concreta de Mejora (Retrospective Action Item - SMART):
> **Implementar una capa de almacenamiento local persistente (SQLite / PostgreSQL) como fallback de contingencia y configurar un worker asíncrono para precargar semanalmente un snapshot de los 500 registros más recientes de cada departamento, asegurando que la aplicación responda en caso de indisponibilidad temporal de datos.gov.co.**
> - *Responsables:* ferneymbravog-stack (Backend) y Gonzalez82ZG (Scrum Master).
> - *Plazo:* Sprint 2, Iteración 1.

El acta completa de la retrospectiva se encuentra en [`docs/retrospective.md`](docs/retrospective.md).

---

## Equipo y Responsabilidades

| Integrante | Rol Scrum | Responsabilidad Principal |
|---|---|---|
| **[ferneymbravog-stack](https://github.com/ferneymbravog-stack)** | Developer | Arquitectura backend, cliente Socrata y rendimiento |
| **[jader-posso](https://github.com/jader-posso)** | Product Owner | Definición de objetivos, prioridades y valor del producto |
| **[Joel90900](https://github.com/Joel90900)** | Developer | Interfaz interactiva, animaciones, frontend y mapas |
| **[Gonzalez82ZG](https://github.com/Gonzalez82ZG)** | Scrum Master | Facilitación ágil, calidad, suite de pruebas y seguimiento |

---

*AccidentaData © 2026 | Análisis y visualización de datos abiertos sobre accidentalidad vial en Colombia.*
