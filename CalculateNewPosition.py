import math
def calcular_nueva_posicion(x_actual, y_actual, phi_actual, grados_izq, grados_der, r, L):
    # 1. Convertir grados a distancia lineal (Paso 3A)
    dist_izq = (grados_izq / 360.0) * (2 * math.pi * r)
    dist_der = (grados_der / 360.0) * (2 * math.pi * r)

    # 2. Calcular cambio lineal y angular (Paso 3B)
    ds = (dist_der + dist_izq) / 2.0
    dphi = (dist_der - dist_izq) / L

    # 3. Actualizar coordenadas usando trigonometría
    # La nueva posición depende de hacia dónde estaba mirando el robot (phi)
    x_nueva = x_actual + ds * math.cos(phi_actual)
    y_nueva = y_actual + ds * math.sin(phi_actual)
    phi_nueva = phi_actual + dphi

    return x_nueva, y_nueva, phi_nueva