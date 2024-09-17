import socket
import threading


#Haik - these have to match the server IP and port in order to connect 
HOST = '127.0.0.1' #Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
SERVER_PORT = 5000

if __name__ == '__main__':
    
    #Haik - Created client instance, takes ipv4 and tcp packets
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, SERVER_PORT))
    except:
        print(f"Unable to connect to host {HOST} and port {SERVER_PORT}. ")