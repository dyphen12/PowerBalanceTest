# obd_backend.py
import obd

class OBDBackend:
    def __init__(self, port="COM3", baudrate=38400):
        self.port = port
        self.baudrate = baudrate
        self.connection = None  # Se conectará al OBD2 más adelante

    def connect(self):
        """
        Establece la conexión con el dispositivo OBD2.
        """
        print("🔍 Buscando conexión OBD2...")

        # Escanear puertos disponibles
        ports = obd.scan_serial()
        if not ports:
            print("❌ No se encontraron puertos OBD2 disponibles.")
            return False

        print("Puertos encontrados:", ports)

        try:
            # Intentar conectar al primer puerto disponible
            self.connection = obd.OBD(ports[0], fast=False, timeout=30)

            if self.connection.is_connected():
                print("✅ Conectado al vehículo")
                print("Protocolo:", self.connection.protocol_name())
                return True
            else:
                print("❌ No se pudo conectar al vehículo. Verifique el puerto y el dispositivo.")
                return False

        except Exception as e:
            print(f"❌ Error al intentar conectar: {e}")
            return False

    def read_rpm(self):
        """
        Recupera las RPM del vehículo.
        """
        if self.connection and self.connection.is_connected():
            print("🔍 Recuperando RPM...")
            try:
                rpm_response = self.connection.query(obd.commands.RPM)

                if rpm_response and rpm_response.value:
                    print("RPM:", rpm_response.value)
                    return rpm_response.value
                else:
                    print("❌ No se pudo recuperar el RPM.")
                    return None

            except Exception as e:
                print(f"❌ Error al recuperar el RPM: {e}")
                return None
        else:
            print("❌ No hay conexión con el dispositivo OBD2.")
            return None

    def read_power_balance(self):
        """
        Devolverá un array con los valores de Power Balance reales desde la F150.
        """
        # Placeholder temporal
        return [0]*8
