from socket import *
import time
import struct



def udp_client(server_ip,server_port):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_socket:
        while True:
            message = input("enter message")
            udp_socket.sendto(message.encode(),(server_ip,server_port))
            data,addr = udp_socket.recvfrom(1024)
            return data, addr 
        

def tcp_client(server_ip,server_port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.connect((server_ip,server_port))
            while True:
                message = input("enter message")
                tcp_socket.sendall(message.encode())
                data = tcp_socket.recvfrom(1024)
                return data
            
        except ConnectionRefusedError:
            print("[TCP] unable to connect to the server")
    


def main():
    server_ip = input("enter server IP (deafault: 127.0.0.1): ") or "127.0.0.1"
    server_port = int(input("enter server port (deafaut: 12345)") or 12345)

    while True: 
        print("\nselect protocol: ")
        print("1. UDP")
        print("2. TCP")

        choice = input("enter your choice: ")

        if choice == "1":
            udp_client(server_ip,server_port)
        elif choice == "2":
            tcp_client(server_ip,server_port)
        time.sleep(1)





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