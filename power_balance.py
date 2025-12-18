# power_balance.py
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from backends.obd_backend import OBDBackend

# Orden de encendido F150 5.4L 3V (V8)
F150_ORDER = [1, 3, 7, 2, 6, 5, 4, 8]

class PowerBalance:
    def __init__(self, obd_backend, buffer_size=8):
        self.obd = obd_backend
        self.buffer_size = buffer_size  # Cuántos ciclos para promedio
        self.rpm_history = []
        self.power = np.zeros(8)

    def update(self):
        rpm = self.obd.read_rpm()
        if rpm is None:
            return self.power
        rpm = rpm.magnitude  # quitar unidades Pint
        self.rpm_history.append(rpm)
        
        if len(self.rpm_history) > self.buffer_size:
            self.rpm_history.pop(0)
        
        # Inferir contribución de cada cilindro
        # Simplificado: variación del RPM por cilindro
        mean_rpm = np.mean(self.rpm_history)
        diff = [mean_rpm - rpm for _ in range(8)]
        
        # Mapear al orden de encendido
        self.power = np.array(diff)
        return self.power

def animate(obd_backend):
    pb = PowerBalance(obd_backend)
    
    fig, ax = plt.subplots()
    ax.set_ylim(-60, 40)
    ax.set_xlim(1, 8)
    ax.set_xlabel("Cilindro")
    ax.set_ylabel("RPM delta")
    ax.set_title("Power Balance Inferido")
    
    line, = ax.plot([], [], marker='o', color='blue', lw=2)
    
    def update_plot(frame):
        power = pb.update()
        line.set_data(range(1, 9), power)
        return line,
    
    ani = FuncAnimation(fig, update_plot, interval=500, blit=True)
    plt.show()

if __name__ == "__main__":
    obd = OBDBackend()
    if obd.connect():
        animate(obd)
    else:
        print("❌ No se pudo conectar al OBD2")
