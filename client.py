from socket import *
import time
import struct
import threading



def udp_client(addres,size):
    socket = socket(AF_INET, SOCK_DGRAM)
    packet = struct.pack('I B I',0xabcddcba,0x03,size)
    socket.sendto(packet, addres)
    packet_resived = []
    #start timer
    start = time.time()
    #receive the packets
    while True:
        data = socket.recv(1045)
        if not data:
            break
        #parse the header
        header = struct.unpack('I B L L',data[:21])
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
    print(f"UDP transfer finished, total time: {end-start} seconds. \ntotal speed: {size/(end-start)} bits/second.\npercentage of packets received successfully: {len(packet_resived)*100/header[2]}")
        
def tcp_client(addr,size):
    with socket(AF_INET,SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.connect(addr)
            time_start = time.time()
            tcp_socket.sendall(str(size)+"\n")
            data = tcp_socket.recv(size)
            time_end = time.time()
            print(f"TCP transfer finished, total time {time_end - time_start}, total speed {size*8/(time_end-time_start)}")

        except ConnectionRefusedError:
            print("[TCP] unable to connect to the server")
    


def main():
    file_size = int(input("please enter file size: "))
    num_of_udp_connections = int(input("please enter how much udp connections:  "))
    num_of_tcp_connections = int(input("please enter how much tcp connections:  "))
    broadcast_socket = socket(AF_INET,SOCK_DGRAM)
    port = 12345
    socket.bind('',port)
    AddressList = []
    TheredsList = []

    while num_of_tcp_connections or num_of_udp_connections: 
        data,addr = broadcast_socket.recvfrom(1024)
        if addr not in AddressList:
            AddressList.append(addr)
            head = struct.unpack('I B H H',data[:9])
            new_tcp_address = (addr[0],head[3])
            new_udp_address = (addr[0],head[2])
            if num_of_tcp_connections > 0:
                thread1 = threading.Thread(target=tcp_client,args=(new_tcp_address,file_size))
                TheredsList.append(thread1)
                thread1.start
                num_of_tcp_connections -= 1

            if num_of_udp_connections > 0:
                thread1 = threading.Thread(target=udp_client,args=(new_udp_address,file_size))
                TheredsList.append(thread1)
                thread1.start
                num_of_tcp_connections -= 1


    for thred in TheredsList:
        thred.join()


if __name__ == "__main__":
    main()