import socket 
import threading

# Jian - Special placeholder IP to tell Server to listen and accept connections from ALL IPs
HOST = "8.8.8.8"
PORT = 5001
USERS = 4
currentUsers = [] #Haik - lists of users with their IP

#server_thread = threading.Thread(target=server_start)
#server_thread.start()
#client_thread = threading.Thread(target=client_start)
#client_thread.start()

#Haik - created socket class object for the mainServer. SOCK_DGRAM lets us use tcp datagrams
# Jian - Changed SOCK_DGRAM to SOCK_STREAM to utilize socket.listen() in whileListening Function
mainServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def messageManager(client, clientIP, message):#Haik - Gets message and sends the message to everyone (work in progress)
    while 1:        
        tempMsg = client.recv(2048).decode('utf-8')#receives and decodes the message
        if message != ' ':
            finalMsg = clientIP + ': ' + message
            client.sendall(finalMsg.encode()) #Haik - encodes the message then sends the message to all clients
            
        else:
            print(f"The message from {clientIP}is empty.")
            
             

def get_clientIP(client): #Haik - gets client IP adress
    clientIP = socket.gethostbyname(client)
    return clientIP
        
def get_clientSocket(client):#Haik - gets client socket
   clientSocket = client(socket.gethostbyaddr)
   return clientSocket

def manageClient(client):#Haik - puts client into user list with their IP address
        
    while 1:
        currentUsers.append(get_clientIP) 
        
    threading.Thread(target = messageManager, args=(client)).start()


def whileListening():
    #Haik - listens for incoming connections
    mainServer.listen(USERS)

    # (Debugging): Check if enters whileListening()
    print(f"Listening...")
    
    # Jian - Currently crashes file, temporarily commented out 
    
    while 1: #Haik - accepts incoming connections
        print("I am in while")
        client, address = mainServer.accept()
        #Haik - start multi threading to manage the users 
        threading.Thread(target = manageClient, args=(client, )).start()


def server_start():    
    #Haik - after it starts running, it confirms it is set up then says it is unable to set up.
    try:
        #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        mainServer.bind((HOST, PORT))
        print(f"Server is set up!")
        whileListening()
          
            
    except:   
        print(f"Unable to bind to host {HOST} and server port {PORT}.") #error message



#Haik - these have to match the server IP and port in order to connect 
#Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
#Jian - Changed HOST to '8.8.8.8' to utilize user's IP as parameter

disconnect = False
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def client_start():
    #Haik - Created client instance, takes ipv4 and tcp packets
    #Jian - Changed socket parameter SOCK_STREAM to SOCK_DGRAM to connect client, had issues connecting earlier

    try: #Haik - trys connecting to server
        client.connect((HOST, PORT))
        print(f"You Connected!")
        
        # Jian (debugging) - test to check your IP
        print(f"Your IP: " + client.getsockname()[0])

        listen_thread = threading.Thread(target=listen)
        listen_thread.start()
        
        send_thread = threading.Thread(target=send)
        send_thread.start()
    except:
        print(f"Unable to connect to host {HOST} and port {PORT}. ")


def listen():
    print(f"Listen Thread works")

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
    print(f"Send Thread works")

    while True:
        if disconnect:
            break
        # Jian - asks for input and formats message
        message = f'Message received from {client.getsockname()[0]}\n'
        message += f'Sender\'s Port: {PORT}\n'
        message += f'Message: {input("")}'
        if message[22 + len(client.getsockname()[0]) + 15 + len(PORT) + 11].startswith('/'):
            print("this is a command")
            
    
def receive(server, message):
        if message != '':
            final = server.recv(2048).decode('utf-8')
            
        else:
            print("The message is empty")
