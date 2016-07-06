import time
import serial
import socket
import threading
'''
    Author: Keeeevin
'''
class serial_server():
    def __init__(self, port, bauds, multicast_group, udp_port):
        #Setting udp socket to send information that comes through serial:
        self.multicast_group = multicast_group
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        #Serial:
        self.ser = serial.Serial(
            port=port,
            baudrate=bauds
        )
    def run(self):
        print("Starting serial server")
        self.dowork = True
        reader = threading.Thread(name='read', target=self.read)
        writer = threading.Thread(name='write', target=self.write)
        reader.start()
        writer.start()

    def read(self):
        print("Starting reader")
        while self.dowork :
            out = ''
            while self.ser.inWaiting() > 0:
                out += str(self.ser.readline().decode('utf-8'))
            if out != '':
                self.sock.sendto(out.encode(), (self.multicast_group, self.udp_port))
                print("Comming: " + out)
        print("Stoping reader")
        self.sock.close()

    def write(self):
        print("Starting writer")
        while self.dowork :
            _in = input()
            if _in == 'exit':
                self.dowork = False
            else:
                self.ser.write(_in.encode('latin-1'))
        print("Stoping writer")
        self.ser.close()

#TODO:
#Set udp server to receive
#Run script to find XBee port name
serv = serial_server("/dev/ttyACM0", 9600, "230.1.1.1", 5000)
serv.run()
