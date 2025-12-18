import time
from backends.obd_backend import OBDBackend

# Inicializar y conectar
backend = OBDBackend()
if not backend.connect():
    print("❌ No se pudo conectar al OBD2.")
    exit()



print("🔄 Mostrando misfires por cilindro en tiempo real. Presiona Ctrl+C para salir.\n")

try:
    while True:
        misfires = backend.read_misfires()  # devuelve lista de 8 elementos
        for i, m in enumerate(misfires, start=1):
            print(f"Cilindro {i}: {m} misfires", end=" | ")
        print()
        time.sleep(0.5)  # actualiza cada 500ms

except KeyboardInterrupt:
    print("\n⏹ Interrumpido por usuario")

finally:
    backend.disconnect()