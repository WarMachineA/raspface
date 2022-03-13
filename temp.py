from smbus2 import SMBus
from mlx90614 import MLX90614

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
Temp = sensor.get_object_1()

if Temp > 30:
    print ("High Temperature !")
else :
    print ("Temperature :", Temp)

bus.close()