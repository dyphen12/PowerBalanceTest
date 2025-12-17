import obd
from obd import OBDStatus

print("🔍 Buscando conexión OBD2...")

connection = obd.OBD() # auto-connects to USB or RF port

# successful communication with the ELM327 adapter
print(OBDStatus.ELM_CONNECTED) # "ELM Connected"

#cmd = obd.commands.SPEED # select an OBD command (sensor)

#response = connection.query(cmd) # send the command, and parse the response

#print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("mph")) # user-friendly unit conversions