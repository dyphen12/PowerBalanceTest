import obd

print("🔍 Buscando conexión OBD2...")

ports = obd.scan_serial()
print("Puertos encontrados:", ports)

# FORScan usaba COM12 → lo forzamos
connection = obd.OBD(
    port="COM12",
    baudrate=38400,
    fast=False,
    timeout=5
)

if connection.is_connected():
    print("✅ Conectado al vehículo")
    print("Protocolo:", connection.protocol_name())
else:
    print("❌ No se pudo conectar")
