import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import networkx as nx
import math

# Configuración del Mapa (200x200 cm = 2x2 metros)
FIG_SIZE = 200

# Definición de obstáculos: (x_inicio, y_inicio, ancho, alto)
# Basado en la imagen de tu tarea
obstaculos = [
    (0, 150, 100, 50),  # Rectángulo superior izquierdo
    (50, 50, 50, 50),  # Rectángulo central
    (150, 50, 15, 100),  # Rectángulo vertical derecha (0.15 de ancho)
    (100, 0, 100, 10)  # Rectángulo inferior (0.1 de alto)
]


def es_colision(x, y, radio_robot=7.5):
    """
    Verifica si un punto (x,y) choca con un obstáculo.
    'radio_robot' infla los obstáculos (C-Space) para que el robot no roce.
    """
    for (ox, oy, w, h) in obstaculos:
        # Inflamos el área del obstáculo con el radio del robot
        if (ox - radio_robot) <= x <= (ox + w + radio_robot) and \
                (oy - radio_robot) <= y <= (oy + h + radio_robot):
            return True

    # También checamos si se sale del mapa de 2x2m
    if x < 0 or x > 200 or y < 0 or y > 200:
        return True

    return False


def dibujar_mapa():
    fig, ax = plt.subplots(figsize=(8, 8))

    # Dibujar obstáculos en negro
    for (ox, oy, w, h) in obstaculos:
        rect = patches.Rectangle((ox, oy), w, h, linewidth=1, edgecolor='black', facecolor='black')
        ax.add_patch(rect)

    # Configurar límites del mapa
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.title("Simulador de Planificación de Movimientos - Mapa 2x2m")
    plt.xlabel("X (cm)")
    plt.ylabel("Y (cm)")
    return ax


# PRUEBA: Dibujar el mapa
ax = dibujar_mapa()
plt.show()


def generar_1000_nodos(n=1000):
    nodos_libres = []
    nodos_colision = []

    while len(nodos_libres) < n:
        # Generar coordenadas al azar en el mapa de 200x200
        x = random.uniform(0, 200)
        y = random.uniform(0, 200)

        if es_colision(x, y):
            nodos_colision.append((x, y))
        else:
            nodos_libres.append((x, y))

    return nodos_libres, nodos_colision


# --- ACTUALIZACIÓN DEL DIBUJO ---
ax = dibujar_mapa()
libres, colisiones = generar_1000_nodos(1000)

# Dibujar nodos libres en verde (pequeños)
x_l, y_l = zip(*libres)
ax.scatter(x_l, y_l, c='green', s=2, alpha=0.5, label='Espacio Libre (C-free)')

# Opcional: Dibujar algunos de colisión en rojo para mostrar que el algoritmo funciona
# x_c, y_c = zip(*colisiones[:100])
# ax.scatter(x_c, y_c, c='red', s=2, alpha=0.3)

plt.legend()
plt.show()



# --- 1. CONFIGURACIÓN DE TRAYECTORIA ---
INICIO = (20, 20)
META = (180, 180)


def distancia(n1, n2):
    """Calcula la distancia euclidiana entre dos nodos."""
    return math.hypot(n1[0] - n2[0], n1[1] - n2[1])


def colision_linea(n1, n2, pasos=20):
    """
    Local Planner: Verifica si una línea recta entre dos nodos choca con un obstáculo.
    Interpola 'pasos' puntos a lo largo de la línea y usa tu función es_colision.
    """
    for i in range(pasos + 1):
        t = i / pasos
        x = n1[0] + t * (n2[0] - n1[0])
        y = n1[1] + t * (n2[1] - n1[1])
        # Usamos el radio seguro de 7.5cm que ya tenías
        if es_colision(x, y, radio_robot=7.5):
            return True  # ¡Choca!
    return False  # Camino libre


def planificar_trayectoria(nodos_libres, inicio, meta, radio_conexion=35):
    """
    Construye el Grafo PRM y usa el Algoritmo A* para encontrar la ruta óptima.
    """
    # 1. Asegurar que inicio y meta estén en la lista de nodos
    nodos = nodos_libres.copy()
    if inicio not in nodos: nodos.append(inicio)
    if meta not in nodos: nodos.append(meta)

    # 2. Inicializar el Grafo
    G = nx.Graph()
    for n in nodos:
        G.add_node(n)

    print("Construyendo aristas (Edges)... esto puede tardar unos segundos.")

    # 3. Conectar nodos cercanos (Crear el PRM)
    for i, n1 in enumerate(nodos):
        for n2 in nodos[i + 1:]:
            dist = distancia(n1, n2)
            # Solo intentamos conectar si están a menos de 'radio_conexion' cm
            if dist < radio_conexion:
                # Si la línea recta entre ellos no choca, creamos un "Edge"
                if not colision_linea(n1, n2):
                    G.add_edge(n1, n2, weight=dist)

    # 4. Búsqueda de la ruta óptima usando Algoritmo de Dijkstra / A*
    try:
        ruta = nx.shortest_path(G, source=inicio, target=meta, weight='weight')
        print(f"¡Ruta encontrada! Consiste en {len(ruta)} nodos.")
        return ruta, G
    except nx.NetworkXNoPath:
        print("Error: No se encontró un camino válido. Intenta generar más nodos.")
        return None, G

# ==========================================================
# EJECUCIÓN PRINCIPAL DEL SIMULADOR
# ==========================================================

# 1. Dibujar el mapa base
ax = dibujar_mapa()

# 2. Generar los nodos
print("Generando nodos...")
libres, colisiones = generar_1000_nodos(1000)

# Dibujar nodos libres (Aseguramos que tenga el parámetro 'label')
x_l, y_l = zip(*libres)
ax.scatter(x_l, y_l, c='green', s=2, alpha=0.5, label='Espacio Libre (C-free)')

# 3. Planificar la trayectoria
ruta_optima, grafo = planificar_trayectoria(libres, INICIO, META, radio_conexion=35)

# 4. Dibujar la ruta si fue exitosa
if ruta_optima:
    rx, ry = zip(*ruta_optima)
    ax.plot(rx, ry, color='blue', linewidth=2, label='Trayectoria 3 Óptima')
    ax.scatter(*INICIO, color='cyan', s=100, marker='s', label='Inicio (20,20)')
    ax.scatter(*META, color='magenta', s=100, marker='*', label='Meta (180,180)')
else:
    print("No se dibujará la ruta porque el algoritmo no encontró un camino.")

# 5. Mostrar la gráfica (¡Solo debe haber UN legend y UN show al final de todo el archivo!)
plt.legend(loc='upper right') # loc='upper right' acomoda el cuadro arriba a la derecha
plt.show()

# ==========================================================
# TRADUCTOR A COMANDOS DE LEGO NXT (CINEMÁTICA INVERSA)
# ==========================================================
import math


def generar_receta_nxt(ruta, radio_llanta=2.7, grados_giro_360=595):
    print("\n" + "=" * 50)
    print("MOVIMIENTOS PARA LEGO NXT")
    print("=" * 50)

    if not ruta or len(ruta) < 2:
        print("La ruta está vacía o es demasiado corta.")
        return

    # Asumimos que el robot empieza posicionado mirando hacia el primer nodo (Tramo 1)
    dx_inicial = ruta[1][0] - ruta[0][0]
    dy_inicial = ruta[1][1] - ruta[0][1]
    angulo_actual_rad = math.atan2(dy_inicial, dx_inicial)

    print(f"0. Coloca el robot en Inicio {ruta[0]}.")
    print(f"   IMPORTANTE: Alinea el frente del robot para que apunte")
    print(f"   directamente hacia la coordenada {ruta[1]}.\n")

    for i in range(len(ruta) - 1):
        p1 = ruta[i]
        p2 = ruta[i + 1]

        # 1. Calcular distancia lineal y grados de motor para avanzar
        distancia_cm = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        circunferencia = 2 * math.pi * radio_llanta
        grados_avance = (distancia_cm / circunferencia) * 360

        print(f"  [Bloque MOVE {i + 1}] De {p1} a {p2}:")
        print(f"   -> AVANZAR: {distancia_cm:.1f} cm")
        print(f"       NXT: Volante al Centro (0) | Duración: {int(grados_avance)} Grados")

        # 2. Calcular ángulo para el siguiente tramo (si no es el último punto)
        if i < len(ruta) - 2:
            p3 = ruta[i + 2]
            dx = p3[0] - p2[0]
            dy = p3[1] - p2[1]
            angulo_nuevo_rad = math.atan2(dy, dx)

            # Calcular la diferencia de ángulo
            delta_angulo_rad = angulo_nuevo_rad - angulo_actual_rad

            # Normalizar el ángulo para que no dé giros innecesarios (ej. girar 270 en vez de -90)
            delta_angulo_rad = (delta_angulo_rad + math.pi) % (2 * math.pi) - math.pi
            delta_angulo_deg = math.degrees(delta_angulo_rad)

            # Calcular grados del motor usando TU calibración empírica (595 grados para 1 vuelta)
            grados_giro_motor = (abs(delta_angulo_deg) / 360.0) * grados_giro_360
            direccion_giro = "DERECHA" if delta_angulo_deg < 0 else "IZQUIERDA"

            # Solo imprimir el giro si es mayor a 1 grado (para evitar micro-ajustes)
            if abs(delta_angulo_deg) > 1.0:
                print(f"\n    [Bloque MOVE de Giro]")
                print(f"   -> GIRAR A LA {direccion_giro}: {abs(delta_angulo_deg):.1f}° (sobre su eje)")
                print(f"       NXT: Volante al Extremo (100) | Duración: {int(grados_giro_motor)} Grados\n")

            angulo_actual_rad = angulo_nuevo_rad

    print("=" * 50)
    print(" LLEGADA A LA META")
    print("=" * 50)


# Llama a la función al final de tu script enviando la ruta que el A* encontró
generar_receta_nxt(ruta_optima)