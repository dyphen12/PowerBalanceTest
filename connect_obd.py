import obd
import time  # Import time for adding delays

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

    # Conectar al puerto seleccionado
    connection = obd.OBD(ports[selected_index], fast=False, timeout=30)

    if connection.is_connected():
        print("✅ Conectado al vehículo")
        print("Protocolo:", connection.protocol_name())

        # Recuperar RPM
        print("🔍 Recuperando RPM...")
        cmd = obd.commands.SPEED # select an OBD command (sensor)

        response = connection.query(cmd) # send the command, and parse the response

        print(response.value) # returns unit-bearing values thanks to Pint
        print(response.value.to("mph")) # user-friendly unit conversions

        print("🔍 Recuperando DTCs...")

        cmd = obd.commands.GET_CURRENT_DTC

        response = connection.query(cmd) # send the command, and parse the response

        print(response.value) 

        print("\n🧪 Probando MODE $06...")

        cmd = obd.commands.MONITOR_MISFIRE_CYLINDER_1

        response = connection.query(cmd) # send the command, and parse the response

        print(response.value)



    else:
        print("❌ No se pudo conectar al vehículo. Verifique el puerto y el dispositivo.")

except ValueError:
    print("❌ Entrada inválida. Por favor, ingrese un número.")
except Exception as e:
    print(f"❌ Error al intentar conectar: {e}")
