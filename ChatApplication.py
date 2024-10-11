import socket 
import sys
import threading
import sys

# Jian - Special placeholder IP to tell Server to listen and accept connections from ALL IPs
HOST = "127.0.0.1"
USERS = 4
currentUsers = {} #Haik - Stores connected users' IP : Port


#Haik - created socket class object for the mainServer. SOCK_DGRAM lets us use tcp datagrams
mainServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Jian - Changed SOCK_DGRAM to SOCK_STREAM to utilize socket.listen() in whileListening Function

def messageManager(client, clientIP, message):#Haik - Gets message and sends the message to everyone (work in progress)
    print("in message thread")
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

def manageClient(connection):#Haik - puts client into user list with their IP address
    connection.send(str.encode("Connected to server!"))
    while 1:
        currentUsers[connection.getsockname()[0]] = connection.getsock
        
    #threading.Thread(target = messageManager, args=(client)).start()

    
def accepting():
    while 1: #Haik - accepts incoming connections
        print("Server accepting connections...")
        client, address = mainServer.accept()
        print("Connected to " + address[0] + str(address[1]))
        #Haik - start multi threading to manage the users 
        threading.Thread(target = manageClient, args=(client, )).start()

def whileListening():
    #Haik - listens for incoming connections
    mainServer.listen(USERS)

    # (Debugging): Check if enters whileListening()
    print(f"Listening...")
    acceptingThread = threading.Thread(target=accepting())
    acceptingThread.start()
        


def server_start():    
    #Haik - after it starts running, it confirms it is set up then says it is unable to set up.
    try:
        #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        mainServer.bind((HOST, PORT))
        print(f"Server is set up!")
        whileListening()
        
    except:   
        print(f"Unable to bind to host {HOST} and server port {PORT}.") #error message
        sys.exit(1)


#Haik - these have to match the server IP and port in order to connect 
#Haik - I THINK we cant use this IP so we'll need to change it, keeping for now so we can test stuff. 
#Jian - Changed HOST to '8.8.8.8' to utilize user's IP as parameter

disconnect = False
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def client_start():
    #Haik - Created client instance, takes ipv4 and tcp packets
    #Jian - Changed socket parameter SOCK_STREAM to SOCK_DGRAM to connect client, had issues connecting earlier
    # HOST = "8.8.8.8"

    try: #Haik - trys connecting to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"You connected to {HOST} {PORT}!")
        print("Client IP: " + client.getsockname()[0])
        manageClient(client)
    except:
        print(f"Unable to connect to host {HOST} and port {PORT}. ")
        sys.exit(1)


    try:        
        # Jian (debugging) - test to check your IP
        listen_thread = threading.Thread(target=listen)
        listen_thread.start()
    except:
        print(f"Listen thread broke")
        sys.exit(1)
        
        
    try:
        send_thread = threading.Thread(target=send)
        send_thread.start()
    except:
        print(f"Send thread broke")
        sys.exit(1)    


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
            print("this is a command") #Jian - Implement later
            
    
def receive(server, message):
        if message != '':
            final = server.recv(2048).decode('utf-8')
            
        else:
            print("The message is empty")

def takeCommands(): #Haik - method for detecting and processing commands
    while True:
        command = input().strip()
        if command == '/help':
            help_list()

def help_list():
    print("Commands available:")
    print("1. /help - Display the available commands.")
    print("2. /myip - Display the IP address of this process.")
    print("3. /myport - Display the port on which this process is listening.")
    print("4. /connect <destination> <port> - Connect to a remote peer.")
    print("5. /list - Display a list of active connections.")
    print("6. /terminate <connection id> - Terminate a connection.")
    print("7. /send <connection id> <message> - Send a message to a connection.")
    print("8. /exit - Closes the program.")

if __name__ == "__main__":
    # Yongkang - Check if the port number is provided as a command-line argument
    if len(sys.argv) != 2:
         print("Usage: python chat.py <port>")
         #Stop the execution because the port number was not supplied
         sys.exit(1)

    # Yongkang - Get the port number from the command-line argument
    PORT = int(sys.argv[1])
    
    server_thread = threading.Thread(target=server_start)
    server_thread.start()
    
    #server_start() #Haik - Starts the server and binds it
    print("Type /help for a menu of app commands.")
    #client_start()
    
    
    client_thread = threading.Thread(target=client_start)
    client_thread.start()
    
    takeCommands()