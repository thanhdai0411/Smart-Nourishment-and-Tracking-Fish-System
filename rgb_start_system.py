import serial
from time import sleep


serial_port = serial.Serial(
        port = "/dev/ttyTHS1",
        baudrate = 115200,
       bytesize = serial.EIGHTBITS,
       parity = serial.PARITY_NONE,
       stopbits = serial.STOPBITS_ONE, 
       timeout = 1 ,
       xonxoff = False, 
       rtscts = False,
       dsrdtr = False, 
       writeTimeout = 1
)

def serial_send(payload) :
    data_send = payload.decode("utf-8")  + '\n'
    print(data_send)
    serial_port.write(data_send.encode())


serial_send("R255G0B0E".encode())
sleep(1)
serial_send("R0G255B0E".encode())
sleep(1)
serial_send("R0G0B255E".encode())
sleep(1)
serial_send("R255G255B255E".encode())



