import socket
import threading


#Haik - these have to match the server IP and port in order to connect 
#Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
#Jian - Changed HOST to '8.8.8.8' to utilize user's IP as parameter
HOST = '8.8.8.8'
CLIENT_PORT = 5000
disconnect = False
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def client_start():
    #Haik - Created client instance, takes ipv4 and tcp packets
    #Jian - Changed socket parameter SOCK_STREAM to SOCK_DGRAM to connect client, had issues connecting earlier

    
    try: #Haik - trys connecting to server
        client.connect((HOST, CLIENT_PORT))
        print(f"You Connected!")
        listen_thread = threading.Thread(target=listen)
        listen_thread.start()
        print(f"Listen Thread works")
        send_thread = threading.Thread(target=send)
        send_thread.start()
        print(f"Send Thread works")
        
        
        # Jian (debugging) - test to check your IP
        print(f"Your IP: " + client.getsockname()[0])

        
     
    except:
        print(f"Unable to connect to host {HOST} and port {CLIENT_PORT}. ")


def listen():
    while True:
        global disconnect
        if disconnect:
            break
        try:
            message = client.recv(1024).decode('ascii')
        except socket.error:
            print(f"Error when connecting...")
            client.close()      #Jian - ToDo: create server event to remove this client from all current connected users
            break
            
        
    
def send():
    while True:
        if disconnect:
            break
        # Jian - asks for input and formats message
        message = f'Message received from {client.getsockname()[0]}\n'
        message += f'Sender\'s Port: {CLIENT_PORT}\n'
        message += f'Message: {input("")}'
        if message[22 + len(client.getsockname()[0]) + 15 + len(CLIENT_PORT) + 11].startswith('/'):
            print("this is a command")
            
    

