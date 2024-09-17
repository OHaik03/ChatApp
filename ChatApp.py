import socket 
import threading


HOST = '127.0.0.1'
SERVERPORT = 5000


if __name__ == '__main__':
    
    #Haik - created socket class object for the mainServer. SOCK_DGRAM lets us use tcp datagrams
    mainServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        mainServer.bind((HOST, SERVERPORT)) #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
    except:   
        print(f"Unable to bind to host {HOST} and server port {SERVERPORT}.") #error message


