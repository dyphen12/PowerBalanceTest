import obd

ports = obd.scan_serial()
print("Puertos encontrados:", ports)

connection = obd.OBD(ports[1], baudrate=9600, fast=False)

print("Estado:", connection.status())

if connection.is_connected():
    print("✅ Conectado al vehículo")
    print("Protocolo:", connection.protocol_name())
else:
    print("❌ No se pudo conectar")
