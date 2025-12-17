# test_rpm.py
import time
from backends import OBDBackend

# Inicializar y conectar
backend = OBDBackend()
if not backend.connect():
    print("❌ No se pudo conectar al OBD2.")
    exit()

print("🔄 Mostrando RPM en tiempo real. Presiona Ctrl+C para salir.\n")

try:
    while True:
        rpm = backend.read_rpm()
        if rpm is not None:
            print(f"RPM: {rpm}")
        else:
            print("RPM no disponible")
        time.sleep(0.3)  # Actualiza cada 300ms

except KeyboardInterrupt:
    print("\n⏹ Interrumpido por usuario")

finally:
    backend.disconnect()
