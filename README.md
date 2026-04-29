# 🤖 Planificación de Movimientos para Robot de Tracción Diferencial (Lego NXT)

Este repositorio contiene el código fuente para el diseño, simulación e implementación física de un sistema de planificación de trayectorias en entornos bidimensionales con obstáculos. El proyecto cierra la brecha entre los modelos matemáticos ideales y la ejecución física en el mundo real.

## 🚀 Características del Proyecto

* **Espacio de Configuración ($\mathcal{C}_{free}$):** Detección de colisiones basada en modelos poligonales y aproximación de la suma de Minkowski.
* **Algoritmo PRM (Probabilistic Roadmap):** Muestreo estocástico de 1000 nodos para discretizar un mapa de 2x2 metros.
* **Búsqueda Óptima (A*):** Integración con la librería `networkx` para encontrar la ruta más corta libre de colisiones.
* **Cinemática Inversa:** Traductor matemático que convierte rutas vectoriales $(x, y)$ en comandos físicos de motor (grados de avance y rotación).
* **Calibración Empírica:** Ajuste de parámetros físicos del robot para compensar la fricción y el deslizamiento en laboratorio.

## 🛠️ Tecnologías y Hardware Utilizado

* **Lenguaje Principal:** Python 3.x
* **Librerías:** `matplotlib` (visualización), `networkx` (grafos), `math` (cinemática), `random`.
* **Hardware:** Kit LEGO Mindstorms NXT Education (9797).
* **Entorno del Robot:** Firmware NXT 2.1 (Programación por bloques basada en las recetas generadas por el simulador).

## 📂 Estructura de Archivos

* `RobotSimulator.py`: Motor gráfico y controlador principal del simulador. Genera el mapa, ejecuta el PRM, traza la ruta y genera la "receta" de comandos NXT.
* `CalculateNewPosition.py`: Módulo matemático que contiene las ecuaciones de odometría y cinemática diferencial.

## 📝 Autores y Referencias
Proyecto desarrollado basándose en la teoría de algoritmos de planificación de Steve M. LaValle (*Planning Algorithms*) y J.P. Laumond.
