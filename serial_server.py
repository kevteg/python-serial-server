import time
import serial
import socket
import threading
import struct
'''
    Author: Keeeevin
'''
class serial_server():
    def __init__(self, port, bauds, receive_multicast_group, receive_udp_port, send_multicast_group, send_udp_port):
        #Setting udp socket to send information that comes through serial:
        self.send_multicast_group = send_multicast_group
        self.send_udp_port = send_udp_port
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        #Setting udp socket to receive and send to serial
        self.receive_multicast_group = receive_multicast_group
        self.receive_udp_port = receive_udp_port
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(('', receive_udp_port))

        mreq = struct.pack("4sl", socket.inet_aton(receive_multicast_group), socket.INADDR_ANY)
        self.receive_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
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
                self.send_sock.sendto(out.encode(), (self.send_multicast_group, self.send_udp_port))
                print("Comming: " + out)
        print("Stoping reader")
        self.send_sock.close()

    def write(self):
        print("Starting writer")
        while self.dowork :
            #_in = input()
            _in = self.receive_socket.recv(10240).decode('utf-8')
            print("Sending: " + _in)
            if _in == 'exit':
                self.dowork = False
            else:
                self.ser.write(_in.encode('latin-1'))
        print("Stoping writer")
        self.ser.close()

#TODO:
#Set udp server to receive
#Run script to find XBee port name
serv = serial_server("/dev/ttyACM0", 9600, "230.2.2.2", 6000, "230.1.1.1", 5000)
serv.run()
