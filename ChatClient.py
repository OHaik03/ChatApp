import socket
import threading

HOST = '127.0.0.1'
SERVER_PORT = 5000

if __name__ == '__main__':
    
    #Haik - Created client instance, takes ipv4 and tcp packets
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)