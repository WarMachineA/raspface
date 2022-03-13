import I2C_LCD_driver
from smbus2 import SMBus
from mlx90614 import MLX90614

mylcd = I2C_LCD_driver.lcd()

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

ambientTemp = sensor.get_ambient()
ambientTemp = str(ambientTemp)

objectTemp = sensor.get_object_1()
objectTemp = str(objectTemp)


bus.close()