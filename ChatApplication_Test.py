import socket 
import sys
import threading
import sys

# Jian - Special placeholder IP to tell Server to listen and accept connections from ALL IPs
HOST = "8.8.8.8"
USERS = 4
currentUsers = [] #Haik - lists of users with their IP


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

def manageClient(client):#Haik - puts client into user list with their IP address
        
    while 1:
        currentUsers.append(get_clientIP) 
        
    #threading.Thread(target = messageManager, args=(client)).start()


def whileListening():
    #Haik - listens for incoming connections
    mainServer.listen(USERS)

    # (Debugging): Check if enters whileListening()
    print(f"Listening...")
    acceptingThread = threading.Thread(target=accepting())
    acceptingThread.start()
    # Jian - Currently crashes file, temporarily commented out 
    
def accepting():
    while 1: #Haik - accepts incoming connections
        print("I am accepting")
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
    #HOST = "8.8.8.8"

    try: #Haik - trys connecting to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"You connected to {HOST} {PORT}!")
        manageClient(client)
        
        # Jian (debugging) - test to check your IP
        print(f"Your IP: " + client.getsockname()[0])

        listen_thread = threading.Thread(target=listen)
        listen_thread.start()
        
        send_thread = threading.Thread(target=send)
        send_thread.start()
        
        # yongk
        receive_thread = threading.Thread(target = receive)
        receive_thread.start()
        
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

# yongk This function is to list all the connections
def list_connection():
    # Check if there are active connections
    if len(currentUsers) > 0:  # If the currentUsers list is not empty
        print("Here are the current connections:")
        
        # This the loop through each user in the list 
        index = 1  # It start the index at 1 
        for client_info in currentUsers:
            print(f"{index}: {client_info}")  # Display the client number and IP address
            index += 1  # Increment the index for each client
    else:
        print("No active connections at this moment.")  # This is a message when no users are connected
                    
# yongk   
def send():
    
    while True:
        if disconnect:
            break # If the client is disconnected, this will exit the loop
        
        try:# This will ask the user to enter connection id to send the message or exit 
            connection_id = input("Enter a connection ID you want to send a message (or type 'exit' to quit): ").strip()
            if connection_id.lower() == 'exit':
                break # If user type 'exit', it will exit the loop
            
            connection_id = int(connection_id)
            if 1 <= connection_id <= len(currentUsers):
                message = input ("Enter your message: ").strip() # This will get the user's message
                
                # This will use the connection ID to get the client socket
                clientSocket = currentUsers[connection_id - 1]
                
                # This will send the message to the connection you select
                clientSocket.sendall(message.encode('utf-8'))
                print(f"You send a message to connection {connection_id}.")
            else:
                print("You entered invalid connection ID. Tpye the /list command to see the list of active connections.")
        
        except ValueError:
            print("You need to enter a valid connection ID number.")
            
        except Exception as e:
            print(f"There is an error occurred while sending the message: {e}")

# yongk 
def receive():
    while True:
        try:
            # This will try to receive a message from the server
            message = client.recv(2048).decode('utf-8')  # This is going to read and decode the coming message
            
            if message:  # THis will check if we received a message or not
                print(f"You got a new message: {message}")  # Display the message to the user
                
            else: # If there is no message, server might have disconnected
                print("You did not get the message. The connection might be closed by the server.")  
                break  # So we exit the loop since the connection to the server is lost
            
        except Exception as e:
            print(f"Oh no, something is wrong when receiving the message: {e}")  # This will handle the errors 
            client.close()  # If there is error, the client connection will close
            break  # Exit this loop to stop receiving messages)

def takeCommands(): #Haik - method for detecting and processing commands
    while True:
        command = input().strip()
        if command == '/help':
            help_list()
            
        elif command == '/list': # yongk
            list_connection()
            
        elif command == '/send':  # yongk
            send() 

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
    # Check if the port number is provided as a command-line argument
    if len(sys.argv) != 2:
         print("Usage: python chat.py <port>")
         #Stop the execution because the port number was not supplied
         sys.exit(1)

    # Get the port number from the command-line argument
    PORT = int(sys.argv[1])
    
    server_thread = threading.Thread(target=server_start)
    server_thread.start()
    
    #server_start() #Haik - Starts teh server and binds it
    print("Type /help for a menu of app commands.")
    #client_start()
    
    
    client_thread = threading.Thread(target=client_start)
    client_thread.start()
    
    takeCommands()
