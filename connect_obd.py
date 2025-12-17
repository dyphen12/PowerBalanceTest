import obd

print("🔍 Buscando conexión OBD2...")

# None = autodetectar puerto (recomendado primero)
connection = obd.OBD(port=None, baudrate=38400, fast=False)

if connection.is_connected():
    print("✅ Conectado correctamente al OBD2")
    print(f"📍 Puerto: {connection.port}")
    print(f"🚗 Protocolo: {connection.protocol_name()}")
else:
    print("❌ No se pudo conectar al OBD2")