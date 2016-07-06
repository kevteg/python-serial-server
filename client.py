import socket
import struct
import threading

MCAST_GRP = '230.1.1.1'
MCAST_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


send_multicast_group = "230.2.2.2"
send_udp_port = 6000
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

def read():
    while True:
      print(sock.recv(10240).decode('utf-8'))
def write():
    while True:
        _in = input(">>")
        if _in != '':
            send_sock.sendto(_in.encode(), (send_multicast_group, send_udp_port))

reader = threading.Thread(name='read', target=read)
writer = threading.Thread(name='write', target=write)
reader.start()
writer.start()
