# simulator.py
import numpy as np

def simulate_f150(weak_cyl=None, weakness=0.30, misfire_cyl=None, misfire_chance=0.2, noise_level=0.03, seed=None):
    """
    Simula un Power Balance Test de una F-150 5.4L 3V.

    Parámetros:
    - weak_cyl: número del cilindro débil (1-8)
    - weakness: porcentaje de reducción del cilindro débil (0.0 - 0.5)
    - misfire_cyl: número del cilindro con misfire intermitente (1-8)
    - misfire_chance: probabilidad de misfire en cada frame
    - noise_level: ruido mecánico normal
    - seed: para reproducibilidad

    Retorna:
    - numpy array con 8 valores escalados [-60, 40]
    """
    if seed is not None:
        np.random.seed(seed)

    base = 1.0
    contributions = []

    for cyl in range(1, 9):
        value = base + np.random.normal(0, noise_level)

        # Aplicar cilindro débil
        if cyl == weak_cyl:
            value *= (1 - weakness)

        # Aplicar misfire intermitente
        if cyl == misfire_cyl:
            if np.random.rand() < misfire_chance:
                value *= 0.5  # Misfire reduce drásticamente la contribución

        contributions.append(value)

    raw = np.array(contributions)
    mean = raw.mean()
    delta = raw - mean

    # Escalado estilo scanner
    scaled = delta / np.max(np.abs(delta)) * 60
    scaled = np.clip(scaled, -60, 40)

    return scaled


# -----------------------------
# Prueba rápida
# -----------------------------
if __name__ == "__main__":
    # Motor sano
    print("Motor sano:", simulate_f150(seed=42))

    # Cilindro 3 débil
    print("Cilindro 3 débil:", simulate_f150(weak_cyl=3, weakness=0.35, seed=42))

    # Cilindro 6 con misfire
    print("Cilindro 6 misfire:", simulate_f150(misfire_cyl=6, misfire_chance=0.5, seed=42))
