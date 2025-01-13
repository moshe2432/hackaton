from socket import *
import time
import _thread
import struct

packet_size = 1024

def main():

    # Create a socket object
    tcp_socet = socket(AF_INET, SOCK_STREAM)
    print("Socket created")

    # Define the port on which you want to connect
    port = 12345
    Host_ip = '172.0.0.1'
    

    tcp_socet.bind((Host_ip, port))
    print("socket binded to %s" % (port))
    tcp_socet.listen()
    print("socket is listening")
    
    conn, addr = tcp_socet.accept()

    print("Got connection from", addr)
    while True:
        data = conn.recv(1024)
        print("Server received", repr(data))
        reply = input("Reply: ")
        conn.sendall(reply.encode())
        if not data:
            break


def TCP_Payload(addres,size,file):
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect(addres)
    file = open(file, "rb")  
    data = file.read(size) + '\n'
    tcp_socket.sendall(data.encode())
    tcp_socket.close()

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
    packet = struct.pack(0xabcddcba,0x02,)  # Packet index as unsigned int
    # Define the port on which you want to connect
    port = 12345

    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        udp_socket.sendto(packet.encode(), ('<broadcast>', port))
        time.sleep(1)



if __name__ == "__main__":
    main()