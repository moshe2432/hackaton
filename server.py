from socket import *
import time
import _thread
import struct

packet_size = 1024

def main():

    _thread.start_new_thread(UDP_Brodcast,())
    _thread.start_new_thread(TCP_Server,())
    _thread.start_new_thread(UDP_Server,())

def TCP_Server():
    #create a socket object
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    port = 0x303B
    tcp_socket.bind(('', port))
    #start listening
    tcp_socket.listen(5)
    print("socket is listening")
    while True:
        conn, addr = tcp_socket.accept()
        print("Got connection from", addr)
        _thread.start_new_thread(TCP_Payload,(conn,addr,"file.txt"))

def UDP_Server():
    #create a socket object
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    port = 0x303A
    udp_socket.bind(('', port))
    print("socket is listening")
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print("Server received", repr(data))
        header = struct.unpack(data[:13])
        if header[0] != 0xabcddcba or header[1] != 0x03:
            continue
        _thread.start_new_thread(UDP_Payload,(addr,header[3],"file.txt"))

def TCP_Payload(conn,addr,file):
    file = open(file, "rb")
    data = conn.recv(1024)
    data = file.read(data[:-1]) + '\n'
    conn.send(data.encode())
    conn.close()

def UDP_Payload(addres,size,file):
    socket = socket(AF_INET, SOCK_DGRAM)
    file = open(file, "rb")
    index = 0
    while size:
        if size > packet_size:
            data = file.read(packet_size)
            size -= packet_size
        else:
            data = file.read(size)
            size = 0
        index+=1

        """
        21 bit header:
        magic number: 0xabcddcba
        message type: 0x04
        Total segment count: unsigned int, size/packet_size
        Packet index: unsigned int, index
        """
        header = struct.pack(0xabcddcba,0x04,size//packet_size + 1 ,index)  
        packet = header + data
        socket.sendto(packet.encode(), addres)
    socket.close()


def UDP_Brodcast():
    # Create a socket object
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    print("Socket created")
    """
    9 bit messege:
    magic number: 0xabcddcba
    message type: 0x02
    UDP port: 0x303A
    TCP port: 0x303B
    """
    packet = struct.pack(0xabcddcba,0x02,0x303A,0x303B)  # Packet index as unsigned int
    # Define the port on which you want to connect
    port = 12345

    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        udp_socket.sendto(packet.encode(), ('<broadcast>', port))
        time.sleep(1)


if __name__ == "__main__":
    main()