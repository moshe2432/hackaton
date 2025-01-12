from socket import *
import time

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