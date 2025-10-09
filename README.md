# Proyecto de Recomendación de Jugadores para Fantasy Premier League (FPL)

## Descripción

Este proyecto es un sistema de análisis de datos y machine learning diseñado para ayudar a los jugadores de Fantasy Premier League (FPL) a tomar decisiones informadas. El sistema extrae datos de la FPL, predice los puntos que se espera que anote cada jugador en la próxima jornada (xP) y utiliza optimización matemática para recomendar un equipo ideal de 15 jugadores que maximiza la puntuación total esperada dentro de un presupuesto de 100M.

## Características Principales

- **Extracción de Datos Automatizada:** Obtiene los datos más recientes de jugadores, equipos, partidos y estadísticas de la API oficial de FPL.
- **Modelo Predictivo (xP):** Entrena un modelo de Gradient Boosting para predecir los "Puntos Esperados" (xP) de cada jugador para la siguiente jornada, basándose en su estado de forma, la dificultad del partido y su posición.
- **Optimización de Equipo (ILP):** Utiliza Programación Lineal Entera (Integer Linear Programming) para seleccionar el equipo óptimo de 15 jugadores que maximiza el xP total, respetando las reglas de FPL (presupuesto, formación, 3 jugadores por equipo).
- **Explicaciones Claras:** Genera justificaciones en lenguaje natural para cada jugador recomendado, explicando por qué es una buena elección (ej. "gran estado de forma", "partido fácil", "buena relación calidad-precio").
- **Pipeline Modular:** El proyecto está dividido en fases claras, desde la obtención de datos hasta la explicación de las recomendaciones.

## Estructura del Proyecto

El flujo de trabajo se divide en varios scripts de Python:

- `fpl_pipeline.py`: Orquesta todo el proceso. Extrae datos frescos de la API de FPL y los guarda en la base de datos.
- `fase2_modelado.py`: Prepara los datos para el modelo, calculando características como la forma y la dificultad del próximo partido.
- `fase3_recomendacion.py`: Entrena el modelo de xP, predice los puntos para la próxima jornada y realiza una selección inicial del equipo ideal.
- `fase4_explicacion.py`: Toma la selección del equipo, la refina y genera explicaciones detalladas para cada jugador recomendado.
- `index.html` y `fpl_web.py`: Una interfaz web simple para visualizar los resultados.

## Requisitos

- Python 3.x
- Bibliotecas: `pandas`, `sqlalchemy`, `scikit-learn`, `pulp`, `requests`.
- Una base de datos PostgreSQL (el proyecto está configurado para usar NeonDB).

## Uso

Para obtener una nueva recomendación para la próxima jornada, sigue estos pasos:

1.  **Actualizar los Datos:** Ejecuta el pipeline principal para obtener los datos más recientes de la FPL.
    ```bash
    python fpl_pipeline.py
    ```

2.  **Ejecutar el Modelado:** Prepara los datos para la predicción.
    ```bash
    python fase2_modelado.py
    ```

3.  **Generar Recomendaciones:** Entrena el modelo y genera las predicciones de xP.
    ```bash
    python fase3_recomendacion.py
    ```

4.  **Obtener Explicaciones y Equipo Final:** Ejecuta la fase final para ver el equipo recomendado con sus justificaciones.
    ```bash
    python fase4_explicacion.py
    ```

Después de ejecutar el paso 4, la consola mostrará la alineación titular, el capitán, el vicecapitán y los suplentes.
