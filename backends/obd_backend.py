# obd_backend.py
class OBDBackend:
    def __init__(self, port="COM3", baudrate=38400):
        self.port = port
        self.baudrate = baudrate
        self.connection = None  # Se conectará al OBD2 más adelante

    def connect(self):
        # Aquí se hará la conexión con python-OBD cuando tengamos el hardware
        pass

    def read_power_balance(self):
        """
        Devolverá un array con los valores de Power Balance reales desde la F150.
        """
        # Placeholder temporal
        return [0]*8
