from socket import *
import time
import _thread

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


def UDP_Brodcast():
    # Create a socket object
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    print("Socket created")
    mesege = "Server started, listening on IP address ??.??.??.??"
    # Define the port on which you want to connect
    port = 12345

    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        udp_socket.sendto(mesege.encode(), ('<broadcast>', port))
        time.sleep(1)



if __name__ == "__main__":
    main()