import socket

def main():
    # Create a socket object
    s = socket.socket()
    print("Socket created")

    # Define the port on which you want to connect
    port = 12345
    ipAddr = '172.1.0.4'
    # connect to the server on local computer
    s.listen(5)