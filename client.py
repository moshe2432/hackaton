from socket import *
import time
import struct

def main():
    # Create a socket object
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    print("Socket created")

    # Define the port on which you want to connect
    port = 12345
    Host_ip = input("Enter the IP address of the server: ")

    tcp_socket.connect((Host_ip, port))
    print("socket connected to %s" % (port))
    while True:
        message = input("Enter message: ")
        tcp_socket.sendall(message.encode())
        data = tcp_socket.recv(1024)
        print("Client received", repr(data))
        time.sleep(1)
        if not data:
            break

def UDP_Request(addres,size):
    socket = socket(AF_INET, SOCK_DGRAM)
    packet = struct.pack(0xabcddcba,0x03,size)
    socket.sendto(packet.encode(), addres)
    packet_resived = []
    #start timer
    start = time.time()
    #receive the packets
    while True:
        data = socket.recv(1045)
        if not data:
            break
        #parse the header
        header = struct.unpack(data[:21])
        #check if the packet is correct
        if header[0] != 0xabcddcba or header[1] != 0x04:
            continue
        packet_resived.append(header[3])
        #check if the packet is the last one
        if header[3] == header[2]:
            break
    
    #end timer
    end = time.time()

    #calculate and print the speed
    print(f"UDP transfer {x} finished, total time: {end-start} seconds. \ntotal speed: {size/(end-start)} bits/second.\npercentage of packets received successfully: {len(packet_resived)*100/header[2]}")













if __name__ == "__main__":
    main()