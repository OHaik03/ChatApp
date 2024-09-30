import socket
import threading


#Haik - these have to match the server IP and port in order to connect 
#Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
#Jian - Changed HOST to '8.8.8.8' to utilize user's IP as parameter
HOST = '8.8.8.8' 
SERVER_PORT = 80

def getMessage():
    print("Hi")
    
if __name__ == '__main__':
    
    #Haik - Created client instance, takes ipv4 and tcp packets
    #Jian - Changed socket parameter SOCK_STREAM to SOCK_DGRAM to connect client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try: #Haik - trys connecting to server
        client.connect((HOST, SERVER_PORT))
        print("Connected!")
        
     
    except:
        print(f"Unable to connect to host {HOST} and port {SERVER_PORT}. ")
         
