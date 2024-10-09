import socket
import threading

#Haik - these have to match the server IP and port in order to connect 
#Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
#Jian - Changed CLIENT_HOST to '8.8.8.8' to utilize user's IP as parameter
CLIENT_HOST = '8.8.8.8'
CLIENT_PORT = 5000


    
def client_start():    
    try: #Haik - trys connecting to server
        #Haik - Created client instance, takes ipv4 and tcp packets
        #Jian - Changed socket parameter SOCK_STREAM to SOCK_DGRAM to connect client, had issues connecting earlier
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect((CLIENT_HOST, CLIENT_PORT))
        print(f"You Connected!")
        # Jian (debugging) - test to check your IP
        print(f"Your IP: " + client.getsockname()[0])
    except socket.error:
        print(f"Unable to connect to CLIENT_HOST {CLIENT_HOST} and port {CLIENT_PORT}. ")
   
   
while True:
    choice = input("Enter a number:\n(1) Start Client\n> ")
    if choice == '1':
        client_start()
        break


disconnect = False


def listen():
    print(f"Listen IP: " + client.getsockname()[0])

    test = 5
        
    
def send():
    print(f"Send IP: " + client.getsockname()[0])

    # while True:
    #     if disconnect:
    #         break
    #     # Jian - asks for input and formats message
    #     message = f'Message received from {client.getsockname()[0]}\n'
    #     message += f'Sender\'s Port: {CLIENT_PORT}\n'
    #     message += f'Message: {input("")}'
    #     if message[22 + len(client.getsockname()[0]) + 15 + len(CLIENT_PORT) + 11].startswith('/'):
    #         print("this is a command")
    test = 4
            

def handle_command(command):
    test = command
            
    

try:
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()
    print(f"Listen Thread works")
except:
    print(f"Listen Thread broke...")

try:
    send_thread = threading.Thread(target=send)
    send_thread.start()
    print(f"Send Thread works")
except:
    print("Send Thread broke...")