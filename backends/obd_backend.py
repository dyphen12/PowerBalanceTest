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
            self.connection = obd.OBD(ports[selected_index], fast=False, timeout=30)


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
        if not self.connection or not self.connection.is_connected():
            print("❌ No hay conexión OBD2.")
            return None

        try:
            rpm_response = self.connection.query(obd.commands.RPM)
            if rpm_response and rpm_response.value:
                return rpm_response.value.magnitude  # devuelve solo el número
            else:
                return None
        except Exception as e:
            print(f"❌ Error al leer RPM: {e}")
            return None

    def read_speed(self):
        """
        Recupera la velocidad del vehículo.
        """
        if not self.connection or not self.connection.is_connected():
            return None
        try:
            print("🔍 Recuperando RPM...")
            cmd = obd.commands.SPEED # select an OBD command (sensor)

            response = self.connection.query(cmd) # send the command, and parse the response

            #print(response.value) # returns unit-bearing values thanks to Pint
            #print(response.value.to("mph")) # user-friendly unit conversions

            return response.value.to("mph")
        
        except Exception as e:
            print(f"❌ Error al leer velocidad: {e}")
            return None

    def read_misfires(self):
        """
        Intenta leer los misfire counts de los cilindros (Mode $06)
        Devuelve una lista de 8 elementos con los conteos de misfire.
        """
        if not self.connection or not self.connection.is_connected():
            return [0]*8

        misfire_cmds = [
            obd.commands.MONITOR_MISFIRE_CYLINDER_1,
            obd.commands.MONITOR_MISFIRE_CYLINDER_2,
            obd.commands.MONITOR_MISFIRE_CYLINDER_3,
            obd.commands.MONITOR_MISFIRE_CYLINDER_4,
            obd.commands.MONITOR_MISFIRE_CYLINDER_5,
            obd.commands.MONITOR_MISFIRE_CYLINDER_6,
            obd.commands.MONITOR_MISFIRE_CYLINDER_7,
            obd.commands.MONITOR_MISFIRE_CYLINDER_8,
        ]

        misfires = []
        for cmd in misfire_cmds:
            if cmd is None:
                misfires.append(0)
                continue
            try:
                response = self.connection.query(cmd)
                if response and response.value is not None:
                    misfires.append(response.value)
                else:
                    misfires.append(0)
            except:
                misfires.append(0)
        return misfires

    def read_power_balance(self):
        """
        Devuelve un array de 8 elementos con la contribución de cada cilindro.
        Por ahora usa misfire counts o placeholder (0 si todo bien)
        """
        misfires = self.read_misfires()
        # Placeholder simple: cilindro con misfire = -50, cilindro sano = 0
        return [-50 if m > 0 else 0 for m in misfires]

    def disconnect(self):
        """
        Cierra la conexión OBD.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            print("🔌 Conexión OBD cerrada.")
