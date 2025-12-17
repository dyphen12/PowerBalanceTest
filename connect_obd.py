import obd

print("🔍 Buscando conexión OBD2...")

ports = obd.scan_serial()
print("Puertos encontrados:", ports)

connection = obd.OBD(ports[0])  # COM12

if connection.is_connected():
    print("✅ Conectado al vehículo")
    print("Protocolo:", connection.protocol_name())
else:
    print("❌ No se pudo conectar")
