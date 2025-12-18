# power_balance_real.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import time
from backends.obd_backend import OBDBackend

class PowerBalance:
    def __init__(self, obd_backend, buffer_size=5):
        self.obd = obd_backend
        self.buffer_size = buffer_size
        self.rpm_history = deque(maxlen=buffer_size)
        self.power = [0] * 8  # Inicializa para 8 cilindros

    def update(self):
        """
        Lee el RPM y calcula la diferencia para cada cilindro
        (placeholder de Power Balance)
        """
        rpm = self.obd.read_rpm()  # ya es un float
        if rpm is None:
            return self.power

        self.rpm_history.append(rpm)
        mean_rpm = sum(self.rpm_history) / len(self.rpm_history)
        # Por ahora: simulación simple, todos los cilindros iguales
        self.power = [mean_rpm - rpm for _ in range(8)]
        return self.power

def animate(obd_backend):
    pb = PowerBalance(obd_backend)

    fig, ax = plt.subplots()
    ax.set_title("Power Balance Test (RPM en tiempo real)")
    ax.set_xlabel("Cilindros")
    ax.set_ylabel("Dif. RPM")
    ax.set_xticks(range(1, 9))
    ax.set_ylim(-100, 100)

    line, = ax.plot([], [], 'o-', color='red', lw=2)
    
    def update_plot(frame):
        power = pb.update()
        line.set_data(range(1, 9), power)
        return line,

    ani = FuncAnimation(fig, update_plot, interval=300, blit=False)
    plt.show()

if __name__ == "__main__":
    backend = OBDBackend()
    if backend.connect():
        try:
            animate(backend)
        finally:
            backend.disconnect()
    else:
        print("❌ No se pudo conectar al OBD2.")
