import time
import serial

class serial_server:
    def __init__(self, port, bauds):
        self.ser = serial.Serial(
            port=port,
            baudrate=bauds
        )
    def readloop(self):
        while 1 :
            _in = input(">> ")
            if _in == 'exit':
                self.ser.close()
                exit()
            else:
                out = ''
                self.ser.write(_in.encode('latin-1'))
                while self.ser.inWaiting() > 0:
                    out += str(self.ser.readline().decode('utf-8'))

                if out != '':
                    print(">>" + out)

#TODO:
#Set udp server
#Set threads to send and receive
#Run script to find XBee port name
serv = serial_server("/dev/ttyACM0", 9600)
serv.readloop()
