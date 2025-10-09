# Documentación del Proyecto: Sistema Inteligente de Recomendación para FPL

## 1. ¿Cuál es el Propósito de este Sistema?

El Fantasy Premier League (FPL) es un juego de estrategia que requiere analizar una enorme cantidad de datos para tomar buenas decisiones. Este sistema actúa como un **asistente experto automatizado** que hace el trabajo pesado por ti.

Su objetivo es simple: **recomendarte el mejor equipo posible para la próxima jornada**, maximizando tus puntos potenciales mientras se adhiere a las reglas del juego, como el presupuesto de 100M.

---

## 2. Cómo Ejecutar el Proyecto (Guía Rápida)

Gracias al script maestro `run_project.py`, obtener una recomendación de equipo completa solo requiere dos pasos.

1.  **Instalar Dependencias (solo la primera vez):**
    Abre una terminal en el directorio del proyecto y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ejecutar el Proyecto:**
    Una vez instaladas las dependencias, simplemente ejecuta el siguiente comando:
    ```bash
    python run_project.py
    ```

El script se encargará de todo el proceso y, al finalizar, te mostrará en la consola la alineación titular, el capitán, el vicecapitán y los suplentes para la jornada.

---

## 3. ¿Cómo Funciona por Dentro? El Proceso Detallado

Para aquellos interesados en los detalles técnicos, el script `run_project.py` orquesta una línea de producción inteligente de 4 fases.

### Fase 1: Recopilación de Datos (El Observador)

En esta primera fase, el sistema se conecta directamente a la base de datos oficial de la Fantasy Premier League para recopilar toda la información relevante y actualizada.

- **¿Qué se recopila?**
    - **Datos de Jugadores:** Precio, posición, equipo, estado de salud, etc.
    - **Datos de Equipos:** Quién juega contra quién, y qué tan fuertes son ofensiva y defensivamente.
    - **Historial de Rendimiento:** Puntos, goles, asistencias y otras estadísticas de cada jugador en cada partido que ha jugado esta temporada.

> **En resumen:** Esta fase actúa como un ojeador global, reuniendo la información más fresca y completa sobre todo el universo FPL.

### Fase 2: Creación de Métricas Clave (El Analista)

Una vez que tenemos los datos, el siguiente paso es darles sentido. Para ello, el sistema calcula métricas más inteligentes:

- **Estado de Forma (`form`):** Un promedio de los puntos que un jugador ha conseguido en sus últimos 5 partidos. Esto nos dice si el jugador está "en racha".
- **Dificultad del Próximo Partido (`difficulty`):** Una puntuación de dificultad para cada partido basándose en la fortaleza del equipo rival.
- **Valor (Calidad-Precio):** Relaciona el rendimiento de un jugador con su precio para encontrar las "gangas" del mercado.

> **En resumen:** Esta fase transforma datos básicos en conocimiento táctico. Nos dice quién está en forma, quién tiene un partido favorable y quién ofrece el mejor retorno de inversión.

### Fase 3: Predicción del Futuro (El Oráculo)

Aquí es donde entra en juego el **Machine Learning**. El sistema utiliza un modelo predictivo que ha sido entrenado con miles de datos de partidos históricos para identificar qué patrones conducen a una alta puntuación.

- **El Resultado:** Para cada jugador de la liga, el sistema genera una predicción: los **"Puntos Esperados" (xP)** para la próxima jornada.

> **En resumen:** Esta fase es el corazón predictivo del sistema. Nos da una estimación numérica del rendimiento probable de cada jugador.

### Fase 4: Construcción del Equipo Ideal (El Director Técnico)

Con las predicciones de `xP`, el sistema utiliza **optimización matemática** para encontrar la única combinación de 15 jugadores que logra la **máxima puntuación total de `xP`** sin salirse del presupuesto y respetando todas las reglas del juego.

- **La Explicación:** Finalmente, genera una justificación en lenguaje claro para cada jugador elegido, explicando por qué es una buena opción.

> **En resumen:** Esta fase final actúa como un director técnico de clase mundial, seleccionando la plantilla óptima basada en datos y explicando la lógica detrás de cada elección.

---
## 4. Cómo Convertir a Word

Para convertir este archivo a un documento de Word:

1.  **Opción Manual (Recomendada):** Abre este archivo, selecciona todo el texto (Ctrl+A), cópialo (Ctrl+C) y pégalo (Ctrl+V) en un documento de Microsoft Word.
2.  **Opción Automática:** Utiliza un conversor online (busca "Markdown to Word") o una herramienta como Pandoc.
