# main.py
from plotter import plot_power_balance, animate_power_balance
from backends.simulator_backend import SimulatorBackend
from backends.obd_backend import OBDBackend

# --------------------------------
# Selección de backend
# --------------------------------
USE_SIMULATOR = False

if USE_SIMULATOR:
    backend = SimulatorBackend(weak_cyl=3, misfire_cyl=6)
else:
    backend = OBDBackend(port="COM3", baudrate=38400)
    backend.connect()

backend.read_rpm()

# --------------------------------
# Ejecutar prueba estática
# --------------------------------
#values = backend.read_power_balance()
#plot_power_balance(values, title="Power Balance Test — Backend Seleccionado")

# --------------------------------
# Ejecutar animación
# --------------------------------
#animate_power_balance(lambda *_: backend.read_power_balance(), weak_cyl=None, misfire_cyl=None, frames=100, interval=300)
