#!/usr/bin/env python
# -*- coding: utf-8 -*
import time
import serial
import socket
import threading
import struct
import os
import argparse
'''
    Author: Keeeevin
'''
class serial_server():
    def __init__(self, _port, bauds, receive_multicast_group, receive_udp_port, send_multicast_group, send_udp_port):
        port = os.popen("./findusb | grep " + _port + " | egrep -o '^[^-]+'").read().rstrip()
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
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=bauds
            )
        except:
            print("There has been an error with that device. Are you sure it exists?")
            exit(-1)

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
parser = argparse.ArgumentParser(prog='serialserver', usage='%(prog)s [options]',description='Script to have several connections to one serial.')
parser.add_argument('-p','--port',dest='serial_port',type=str, required = True, help='Serial port to connect in')
parser.add_argument('-b','--bauds',dest='bauds',type=int, default=9600, help='Serial bauds')
parser.add_argument('-r','--receive',dest='receive_multicast',type=str, default="230.2.2.2", help='Multicast address to receive data')
parser.add_argument('-o','--receive_port',dest='receive_port',type=int, default=6000, help='Multicast port to receive data')
parser.add_argument('-s','--send',dest='send_multicast',type=str, default="230.1.1.1", help='Multicast address to send data')
parser.add_argument('-i','--send_port',dest='send_port',type=int, default=5000, help='Multicast port to send data')

args = parser.parse_args()

#serv = serial_server("/dev/ttyACM0", 230400, "230.2.2.2", 6000, "230.1.1.1", 5000)
serv = serial_server(args.serial_port, args.bauds, args.receive_multicast, args.receive_port, args.send_multicast, args.send_port)
serv.run()
