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

    # Configurar un tiempo de espera más largo para la conexión
    connection = obd.OBD(ports[selected_index], fast=False, timeout=30)  # Conectar al puerto seleccionado con timeout extendido

    if connection.is_connected():
        print("✅ Conectado al vehículo")
        print("Protocolo:", connection.protocol_name())

        # Obtener códigos de diagnóstico de fallas (DTCs)
        print("🔍 Recuperando códigos de diagnóstico de fallas (DTCs)...")
        dtc_response = connection.query(obd.commands.GET_DTC)

        if dtc_response and dtc_response.value:
            dtcs = dtc_response.value  # Lista de códigos DTC
            if dtcs:
                print("✅ Códigos de diagnóstico encontrados:")
                for code, description in dtcs:
                    print(f"- {code}: {description}")
            else:
                print("✅ No se encontraron códigos de diagnóstico.")
        else:
            print("❌ Error al recuperar los códigos de diagnóstico o no hay datos disponibles.")

        # Probar otros comandos
        print("🔍 Probando otros comandos...")
        rpm_response = connection.query(obd.commands.RPM)
        if rpm_response and rpm_response.value:
            print("RPM:", rpm_response.value)
        else:
            print("❌ No se pudo recuperar el RPM.")

        speed_response = connection.query(obd.commands.SPEED)
        if speed_response and speed_response.value:
            print("Velocidad:", speed_response.value)
        else:
            print("❌ No se pudo recuperar la velocidad.")

    else:
        print("❌ No se pudo conectar al vehículo. Verifique el puerto y el dispositivo.")

except ValueError:
    print("❌ Entrada inválida. Por favor, ingrese un número.")
except Exception as e:
    print(f"❌ Error al intentar conectar: {e}")
