# Documentación Técnica del Proyecto FPL

## 1. Introducción

Este documento proporciona una descripción técnica completa del sistema de recomendación para Fantasy Premier League (FPL). El objetivo es detallar la arquitectura, el flujo de datos, la configuración y el propósito de cada componente del proyecto.

---

## 2. Arquitectura y Estructura del Proyecto

El proyecto adopta una estructura de directorios estándar que separa las responsabilidades, facilitando el mantenimiento y la claridad.

```
. 
├── data/                 # Almacena datos generados por el pipeline (ej. resultados_fase2.csv).
├── docs/                 # Contiene esta documentación.
├── outputs/              # Destino para salidas no-tabulares como imágenes o reportes.
├── scripts/              # Scripts auxiliares, de análisis exploratorio (EDA) o pruebas.
├── src/                  # El código fuente principal de la aplicación.
│   ├── __init__.py       # Convierte a src en un paquete de Python.
│   ├── data_pipeline.py  # Fase 1: Extrae y carga datos de la API de FPL a la BD.
│   ├── feature_engineering.py # Fase 2: Calcula métricas como forma y dificultad.
│   ├── model_training.py # Fase 3: Entrena el modelo y predice puntos esperados (xP).
│   └── team_selection.py # Fase 4: Selecciona el equipo óptimo y genera explicaciones.
├── .gitignore            # Especifica los archivos que Git debe ignorar.
├── README.md             # Guía de inicio rápido.
├── requirements.txt      # Lista de dependencias de Python para el proyecto.
└── run_project.py        # Script maestro que orquesta todo el pipeline.
```

---

## 3. Configuración y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en un nuevo entorno.

### 3.1. Requisitos Previos

- Python 3.8 o superior.
- Git para clonar el repositorio.

### 3.2. Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-DIRECTORIO>
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar Dependencias:**
    El archivo `requirements.txt` contiene todas las bibliotecas necesarias.
    ```bash
    pip install -r requirements.txt
    ```

### 3.3. Configuración de la Base de Datos (NeonDB)

El proyecto está pre-configurado para usar una base de datos PostgreSQL gratuita alojada en **Neon**.

- **Cadena de Conexión:** La conexión a la base de datos está codificada en los scripts dentro de `src/`. La URL utilizada es:
  ```
  postgresql://neondb_owner:npg_siXJHlLYwC10@ep-muddy-mode-ad05g277-pooler.c-2.us-east-1.aws.neon.tech/neondb
  ```
- **Uso Propio:** Si deseas utilizar tu propia instancia de PostgreSQL, deberás reemplazar esta cadena de conexión en todos los scripts que la contengan dentro de la carpeta `src/`.

---

## 4. Cómo Usar el Proyecto

La ejecución del proyecto se ha simplificado a un único comando gracias al script maestro `run_project.py`.

```bash
python run_project.py
```

Este comando ejecutará secuencialmente todas las fases del pipeline:
1.  Actualizará los datos desde la API de FPL.
2.  Calculará las nuevas métricas.
3.  Re-entrenará el modelo y predecirá los puntos.
4.  Seleccionará el equipo óptimo.
5.  Finalmente, imprimirá en la consola la alineación recomendada, el capitán, el vicecapitán y los suplentes.

---

## 5. El Pipeline Explicado a Fondo

Cada fase del pipeline es un script independiente dentro de la carpeta `src/`, diseñado para una tarea específica.

### Fase 1: `src/data_pipeline.py`
- **Propósito:** Extraer los datos más recientes de la API de FPL y cargarlos en la base de datos Neon.
- **Proceso:** 
    1. Se conecta a la API de FPL.
    2. Descarga datos de jugadores, equipos e historial de partidos.
    3. Limpia y formatea los datos.
    4. Sube los datos limpios a las tablas correspondientes en la base de datos PostgreSQL, sobrescribiendo la información anterior para mantenerla actualizada.

### Fase 2: `src/feature_engineering.py`
- **Propósito:** Tomar los datos básicos y enriquecerlos con métricas de rendimiento (ingeniería de características).
- **Proceso:**
    1. Carga los datos de la base de datos.
    2. Calcula el **estado de forma (`form`)** de cada jugador (promedio de puntos en los últimos 5 partidos).
    3. Calcula la **dificultad del próximo partido (`difficulty`)** basándose en la fortaleza del oponente.
    4. Genera un archivo `data/resultados_fase2.csv` con los datos enriquecidos.

### Fase 3: `src/model_training.py`
- **Propósito:** Predecir el rendimiento futuro de los jugadores.
- **Proceso:**
    1. Carga los datos de la fase anterior y el historial completo de la base de datos.
    2. **Entrena un modelo de Machine Learning** (Gradient Boosting Regressor) para aprender la relación entre la forma, la dificultad y los puntos obtenidos.
    3. Usa el modelo para predecir los **Puntos Esperados (xP)** para la siguiente jornada.
    4. Guarda los resultados, incluyendo los xP, en `data/resultados_fase3.csv`.

### Fase 4: `src/team_selection.py`
- **Propósito:** Construir el equipo óptimo y presentar los resultados.
- **Proceso:**
    1. Carga los datos con las predicciones de xP.
    2. Resuelve un **problema de optimización matemática** para encontrar la combinación de 15 jugadores que maximiza el `xP` total, sujeto a las restricciones de presupuesto y formación de FPL.
    3. Genera una explicación basada en reglas para cada jugador seleccionado.
    4. Guarda el equipo final en `data/equipo_ideal.csv` y lo muestra en consola.