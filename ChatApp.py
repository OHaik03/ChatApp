import socket 
import threading

HOST = '127.0.0.1' #I THINK we have to change this cause we cant use this IP. but  
SERVERPORT = 5000

def whileListening():
    #print("I am in here")

    mainServer.listen(1)#Haik - listens for incoming connections
    print("I am in here")

    
    while 1: #Haik - accepts incoming connections 
        connectionSocket, addr = mainServer.accept()
        #accepts messages up to 1024 bytes
        message = mainServer.recv(1024)
        print("I am in while")


if __name__ == '__main__':
    
    #Haik - created socket class object for the mainServer. SOCK_DGRAM lets us use tcp datagrams
    mainServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Haik - after it starts running, it confirms it is set up then says it is unable to set up.
    try:
        mainServer.bind((HOST, SERVERPORT)) #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        print("Server is set up!")
        whileListening()
          
            
    except:   
        print(f"Unable to bind to host {HOST} and server port {SERVERPORT}.") #error message

