import obd

print("🔍 Buscando conexión OBD2...")

# Escanear puertos disponibles
ports = obd.scan_serial()
if not ports:
    print("❌ No se encontraron puertos OBD2 disponibles.")
    exit()

print("Puertos encontrados:", ports)

# Permitir al usuario seleccionar el puerto
print("Seleccione el puerto al que desea conectarse:")
for i, port in enumerate(ports):
    print(f"[{i}] {port}")

try:
    selected_index = int(input("Ingrese el número del puerto: "))
    if selected_index < 0 or selected_index >= len(ports):
        print("❌ Selección inválida.")
        exit()

    connection = obd.OBD(ports[selected_index])  # Conectar al puerto seleccionado

    if connection.is_connected():
        print("✅ Conectado al vehículo")
        print("Protocolo:", connection.protocol_name())
    else:
        print("❌ No se pudo conectar al vehículo. Verifique el puerto y el dispositivo.")

except ValueError:
    print("❌ Entrada inválida. Por favor, ingrese un número.")
except Exception as e:
    print(f"❌ Error al intentar conectar: {e}")
