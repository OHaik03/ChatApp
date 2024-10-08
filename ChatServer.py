import socket 
import threading

# Jian - Special placeholder IP to tell Server to listen and accept connections from ALL IPs
HOST = "0.0.0.0"
SERVERPORT = 5001
USERS = 4
currentUsers = [] #Haik - lists of users with their IP

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
        
def get_clientSocket(client):
   clientSocket = client(socket.gethostbyaddr)
   return clientSocket

def manageClient():#Haik - puts client into user list with their IP address
    while 1:
        currentUsers.append(get_clientIP) 




def whileListening():
    #Haik - listens for incoming connections
    mainServer.listen(USERS)

    # (Debugging): Check if enters whileListening()
    print(f"Server Listening...")
    
    # Jian - Currently crashes file, temporarily commented out 
    # print(f"I am in here. connected to {client} {address[0]} {address[1]}")



    
    while 1: #Haik - accepts incoming connections
        print("Server in while")
        client, address = mainServer.accept()
        
        threading.Thread(target = manageClient, args=(client, )).start()


def server_start():    
    #Haik - after it starts running, it confirms it is set up then says it is unable to set up.
    try:
        #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        mainServer.bind((HOST, SERVERPORT))
        print(f"Server is set up!")
        whileListening()
          
            
    except:   
        print(f"Unable to bind to host {HOST} and server port {SERVERPORT}.") #error message

