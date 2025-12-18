# power_balance.py
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from backends.obd_backend import OBDBackend

class PowerBalance:
    def __init__(self, backend, num_cylinders=8, history_len=10):
        self.backend = backend
        self.num_cylinders = num_cylinders
        self.history_len = history_len
        self.rpm_history = []  # aquí guardaremos solo valores numéricos
        self.power = [0] * num_cylinders

    def update(self):
        rpm_resp = self.backend.read_rpm()
        if rpm_resp is None:
            return self.power

        # Obtener valor numérico de las RPM
        rpm_val = rpm_resp.magnitude if hasattr(rpm_resp, 'magnitude') else rpm_resp

        # Guardar en el historial limitado
        self.rpm_history.append(rpm_val)
        if len(self.rpm_history) > self.history_len:
            self.rpm_history.pop(0)

        # Calcular RPM promedio
        mean_rpm = sum(self.rpm_history) / len(self.rpm_history)

        # Power balance: diferencia del promedio
        self.power = [mean_rpm - rpm_val for _ in range(self.num_cylinders)]
        return self.power

def animate(backend):
    pb = PowerBalance(backend)
    
    fig, ax = plt.subplots()
    bars = ax.bar(range(pb.num_cylinders), [0]*pb.num_cylinders)
    ax.set_ylim(-1000, 1000)  # ajustar según las RPM de tu motor
    ax.set_xlabel("Cilindro")
    ax.set_ylabel("Diferencia con RPM promedio")
    ax.set_title("Power Balance en tiempo real")

    def update_plot(frame):
        power = pb.update()
        for bar, val in zip(bars, power):
            bar.set_height(val)
        return bars

    ani = FuncAnimation(fig, update_plot, interval=300, blit=False)
    plt.show()

if __name__ == "__main__":
    backend = OBDBackend()
    if not backend.connect():
        print("❌ No se pudo conectar al OBD2.")
        exit()

    try:
        animate(backend)
    finally:
        backend.disconnect()
