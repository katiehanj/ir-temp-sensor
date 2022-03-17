# script for reading temperture values from MLX90614 sensor.

import time
from smbus2 import SMBus
from mlx90614 import MLX90614
import paho.mqtt.client as mqtt

server = 'mqtt.thingspeak.com'
port = 1883

write_api_key = 'OPXUKZ0TGC3MRVSM'
channel_id = '1670351'
topic = 'channels/'+channel_id+'/publish/'+write_api_key

client = mqtt.Client()
client.connect(server, port)



# define sensor i2c address
thermometer_address = 0x5a

try:
    # create sensor object
    bus = SMBus(1)
    sensor = MLX90614(bus, address=thermometer_address)

    print("* MLX90614 Temperature *")
    print("Object | Ambient")

    while True:
        # read sensor values
        object_temp = sensor.get_obj_temp() #note: method might have changed to get_obj_temp()
        ambient_temp = sensor.get_amb_temp() #note: method might have changed to get_amb_temp()

        # print readings to console
        # {} is used in conjunction with format() for substitution.
        # .2f       - format to 2 decimal places.
        print("{0:>5.2f}C | {1:>5.2f}C".format(object_temp, ambient_temp), end='\r')
        print("Body Temp =", object_temp)
        print("Ambient Temp = ", ambient_temp)
        data = 'field1='+str(object_temp)+'&field2='+str(ambient_temp)
        client.publish(topic, data)
        print("Data sent to cloud")
        

        time.sleep(15)


except KeyboardInterrupt:
    print('script stopped by user')
finally:
    bus.close()
    print('Goodbye!')
