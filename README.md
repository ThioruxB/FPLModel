# Proyecto de Recomendación de Jugadores para Fantasy Premier League (FPL)

<table>
  <tr>
    <td align="center"><b>Dashboard Principal</b></td>
    <td align="center"><b>Detalle de Jugadores</b></td>
  </tr>
  <tr>
    <td>!(outputs/demos1.png)
</td>
    <td><img src="outputs/demos2.png" alt="Demo 2" width="420"></td>
  </tr>
</table>

Este proyecto es un sistema de análisis de datos y machine learning diseñado para ayudar a los jugadores de Fantasy Premier League (FPL) a construir un equipo óptimo. El sistema extrae datos de la FPL, predice los puntos esperados (xP) de cada jugador y utiliza optimización matemática para recomendar un equipo ideal que maximiza la puntuación total dentro del presupuesto.

## Características

- **Pipeline Automatizado:** Ejecuta todo el proceso, desde la extracción de datos hasta la recomendación final, con un solo comando.
- **Modelo Predictivo (xP):** Utiliza un modelo de Gradient Boosting para predecir los "Puntos Esperados" (xP) de cada jugador para la siguiente jornada.
- **Optimización de Equipo:** Usa Programación Lineal Entera para seleccionar la plantilla óptima de 15 jugadores que maximiza el xP total, respetando las reglas de FPL.
- **Explicaciones Claras:** Justifica la selección de cada jugador basándose en su estado de forma, la dificultad del partido y su valor.

---

## Estructura del Proyecto

El proyecto está organizado siguiendo una estructura estándar para facilitar su mantenimiento y escalabilidad.

```
. 
├── data/                 # Archivos de datos generados por el pipeline
├── docs/                 # Documentación detallada
├── outputs/              # Archivos de salida (imágenes, reportes)
├── scripts/              # Scripts auxiliares y de análisis exploratorio
├── src/                  # Código fuente principal de la aplicación
│   ├── data_pipeline.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── team_selection.py
├── .gitignore            # Archivos a ignorar por Git
├── README.md             # Este archivo
├── requirements.txt      # Dependencias del proyecto
└── run_project.py        # Script maestro para ejecutar todo el pipeline
```

---

## Guía de Uso

Para obtener una nueva recomendación de equipo, sigue estos pasos:

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-DIRECTORIO>
    ```

2.  **Instalar Dependencias:**
    Se recomienda crear un entorno virtual primero. Luego, instala las bibliotecas necesarias.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar el Pipeline Completo:**
    Este único comando se encargará de todo y te mostrará la alineación final.
    ```bash
    python run_project.py
    ```

## Base de Datos

El sistema utiliza una base de datos PostgreSQL, alojada en [Neon](https://neon.tech/), para almacenar los datos históricos de jugadores y equipos. La configuración de la conexión está definida directamente en los scripts de la carpeta `src`. Si deseas utilizar tu propia base de datos, deberás actualizar la cadena de conexión en dichos archivos.

---

## Diccionario de Datos de la Base de Datos

A continuación se describen las tablas y columnas más relevantes que se crean en la base de datos, basado en la información del esquema proporcionado.

### Tabla: `teams`
Almacena información y estadísticas de cada equipo.

| Columna                 | Tipo de Dato | Descripción                                                 |
| ----------------------- | ------------ | ----------------------------------------------------------- |
| `id`                    | `bigint`     | Identificador numérico único para el equipo.                |
| `name`                  | `text`       | Nombre del equipo (ej. "Arsenal").                          |
| `short_name`            | `text`       | Abreviatura del nombre del equipo (ej. "ARS").            |
| `strength`              | `bigint`     | Fortaleza general del equipo.                               |
| `strength_overall_home` | `bigint`     | Fortaleza general del equipo jugando en casa.               |
| `strength_overall_away` | `bigint`     | Fortaleza general del equipo jugando como visitante.        |

### Tabla: `players`
Almacena la información principal de cada jugador.

| Columna        | Tipo de Dato | Descripción                                                                 |
| -------------- | ------------ | --------------------------------------------------------------------------- |
| `id`           | `bigint`     | Identificador numérico único del jugador en FPL.                            |
| `Nombre`       | `text`       | Nombre de pila del jugador.                                                 |
| `Apellido`     | `text`       | Apellido del jugador.                                                       |
| `team_id`      | `bigint`     | ID del equipo al que pertenece el jugador (referencia a `teams.id`).        |
| `Posicion`     | `text`       | Nombre de la posición del jugador (ej. "Forward").                        |
| `Precio`       | `bigint`     | Costo actual del jugador, multiplicado por 10 (ej. 145 para 14.5M).         |

### Tabla: `player_types`
Tabla de mapeo para las posiciones de los jugadores.

| Columna         | Tipo de Dato | Descripción                                                         |
| --------------- | ------------ | ------------------------------------------------------------------- |
| `id`            | `bigint`     | ID numérico de la posición (1: GKP, 2: DEF, 3: MID, 4: FWD).      |
| `singular_name` | `text`       | Nombre de la posición en singular (ej. "Goalkeeper").             |
| `plural_name`   | `text`       | Nombre de la posición en plural (ej. "Goalkeepers").              |

### Tabla: `gameweeks`
Almacena información sobre cada jornada (semana de juego) de la temporada.

| Columna         | Tipo de Dato | Descripción                                                         |
| --------------- | ------------ | ------------------------------------------------------------------- |
| `id`            | `bigint`     | Número de la jornada (ej. 1, 2, 3...).                              |
| `name`          | `text`       | Nombre de la jornada (ej. "Gameweek 1").                          |
| `deadline_time` | `text`       | Fecha y hora límite para hacer cambios en el equipo (formato ISO). |
| `is_current`    | `boolean`    | Verdadero si es la jornada que se está jugando actualmente.         |
| `is_next`       | `boolean`    | Verdadero si es la próxima jornada en jugarse.                      |

### Tabla: `fixtures`
Almacena información sobre cada partido programado en la temporada.

| Columna             | Tipo de Dato | Descripción                                                         |
| ------------------- | ------------ | ------------------------------------------------------------------- |
| `id`                | `bigint`     | ID único del partido.                                               |
| `event`             | `bigint`     | Número de la jornada a la que pertenece (referencia a `gameweeks.id`). |
| `team_h`            | `bigint`     | ID del equipo local (referencia a `teams.id`).                      |
| `team_a`            | `bigint`     | ID del equipo visitante (referencia a `teams.id`).                  |
| `kickoff_time`      | `text`       | Fecha y hora de inicio del partido (formato ISO).                   |
| `finished`          | `boolean`    | Verdadero si el partido ha finalizado.                              |

### Tabla: `player_history`
Almacena el rendimiento detallado de un jugador en cada partido que ha jugado.

| Columna         | Tipo de Dato | Descripción                                                              |
| --------------- | ------------ | ------------------------------------------------------------------------ |
| `element`       | `bigint`     | ID del jugador al que pertenece el registro (referencia a `players.id`). |
| `fixture`       | `bigint`     | ID del partido jugado (referencia a `fixtures.id`).                    |
| `opponent_team` | `bigint`     | ID del equipo oponente.                                                  |
| `total_points`  | `bigint`     | Puntos totales que el jugador anotó en ese partido.                      |
| `was_home`      | `boolean`    | Verdadero si el jugador jugó en casa.                                    |
| `minutes`       | `bigint`     | Minutos jugados en el partido.                                           |
| `goals_scored`  | `bigint`     | Goles anotados en el partido.                                            |
| `assists`       | `bigint`     | Asistencias realizadas en el partido.                                    |
| `bps`           | `bigint`     | Puntuación en el "Bonus Points System" para ese partido.                 |
| `value`         | `bigint`     | Precio del jugador en esa jornada, multiplicado por 10.                  |
