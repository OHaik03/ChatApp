import socket 
import threading

HOST = ' ' #I THINK we have to change this cause we cant use this IP. but  
SERVERPORT = 5000
USERS = 4
currentUsers = [] #Haik - lists of users with their IP

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
    #print("I am in here")

    mainServer.listen(USERS)#Haik - listens for incoming connections
    print(f"I am in here. connected to {client} {address[0]} {address[1]}")

    
    while 1: #Haik - accepts incoming connections 
        client, address = mainServer.accept()
        print("I am in while")

        threading.Thread(target = manageClient, args=(client, )).start()


if __name__ == '__main__':
    
    #Haik - created socket class object for the mainServer. SOCK_DGRAM lets us use tcp datagrams
    mainServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #Haik - after it starts running, it confirms it is set up then says it is unable to set up.
    try:
        mainServer.bind((HOST, SERVERPORT)) #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        print(f"Server is set up!")
        whileListening()
          
            
    except:   
        print(f"Unable to bind to host {HOST} and server port {SERVERPORT}.") #error message

