# obd_backend.py
import obd  # Import the python-OBD library
from simulator import simulate_f150  # Import simulation for fallback

class OBDBackend:
    def __init__(self, port="COM3", baudrate=38400):
        self.port = port
        self.baudrate = baudrate
        self.connection = None  # Connection to the OBD2 device

    def connect(self):
        """
        Establish a connection to the OBD2 device using Bluetooth.
        """
        try:
            # Use the Bluetooth protocol for the connection
            self.connection = obd.OBD(portstr=self.port, baudrate=self.baudrate, protocol=obd.protocols.AUTO)
            if self.connection.is_connected():
                print("Successfully connected to the OBD2 device via Bluetooth.")
            else:
                print("Failed to connect to the OBD2 device via Bluetooth.")
        except Exception as e:
            print(f"Error connecting to OBD2 device via Bluetooth: {e}")

    def read_power_balance(self):
        """
        Retrieve real-time Power Balance values from the OBD2 device.
        If the connection fails, fallback to the simulator.
        Returns:
            A list of 8 values representing the power balance for each cylinder.
        """
        if self.connection and self.connection.is_connected():
            try:
                # Define custom commands for cylinder power balance (replace with actual commands for the F-150)
                CYLINDER_BALANCE_COMMANDS = [
                    obd.commands.CUSTOM_COMMAND_1,  # Replace with actual command for cylinder 1
                    obd.commands.CUSTOM_COMMAND_2,  # Replace with actual command for cylinder 2
                    obd.commands.CUSTOM_COMMAND_3,  # Replace with actual command for cylinder 3
                    obd.commands.CUSTOM_COMMAND_4,  # Replace with actual command for cylinder 4
                    obd.commands.CUSTOM_COMMAND_5,  # Replace with actual command for cylinder 5
                    obd.commands.CUSTOM_COMMAND_6,  # Replace with actual command for cylinder 6
                    obd.commands.CUSTOM_COMMAND_7,  # Replace with actual command for cylinder 7
                    obd.commands.CUSTOM_COMMAND_8   # Replace with actual command for cylinder 8
                ]

                power_balance_values = []
                for cyl, command in enumerate(CYLINDER_BALANCE_COMMANDS, start=1):
                    response = self.connection.query(command)

                    if response.is_successful():
                        # Append the value to the list
                        power_balance_values.append(response.value.magnitude)  # Assuming response.value has magnitude
                    else:
                        print(f"Failed to retrieve data for cylinder {cyl}.")
                        power_balance_values.append(0)  # Default value for failed reads

                return power_balance_values

            except Exception as e:
                print(f"Error reading power balance data: {e}")
        else:
            print("No connection to OBD2 device. Falling back to simulator.")

        # Fallback to simulation if OBD2 connection fails
        return simulate_f150(weak_cyl=3, misfire_cyl=6, weakness=0.3, misfire_chance=0.2, noise_level=0.03)
