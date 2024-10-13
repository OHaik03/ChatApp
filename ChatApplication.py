import socket 
import sys
import threading
import sys

# Jian - Special placeholder IP to tell Server to listen and accept connections from ALL IPs
HOST = "0.0.0.0"
USERS = 4
currentUsers = {} #Haik - Stores connected users' IP : Port

# Yongkang - Check if the port number is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python chat.py <port>")
    #Stop the execution because the port number was not supplied
    sys.exit(1)

PORT = int(sys.argv[1])


disconnect = False
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        
def send(connection_id, message):
    # This function sends a message to a specific client identified by its connection ID
    if connection_id in currentUsers:
        client_socket, client_address = currentUsers[connection_id]
        try:
            client_socket.send(str.encode(message))
            print(f"Message sent to {client_address}: {message}")
        except Exception as e:
            print(f"Failed to send message to {client_address}.\nReason: {e}")
    else:
        print("Invalid connection ID.")


def peer_connect(peerIP, peerPort):
    # Jian - Reject if trying to connect to itself
    if(peerIP == socket.gethostbyname(socket.gethostname()) and peerPort == PORT):
        print("You cannot connect to your own server.")
        return
    # Jian - Rejects duplicate connections
    elif ( (peerIP, peerPort) in currentUsers.values()):
        print("This connection already exists.")
        return
    
    #Haik - Created client instance, takes ipv4 and tcp packets
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peerIP, int(peerPort)))
        connection_id = len(currentUsers) + 1  # Assign a new ID for the connection
        #Yongkang - Stores peer's socket instance, ip, and port 
        currentUsers[connection_id] = (client_socket, (peerIP, peerPort))
        
        print(f"Successfully connected to {peerIP} : {peerPort}")
    except Exception as e:
        print(f"Couldn't connect to {peerIP}:{peerPort}.\nReason: {e}")



def help_list():
    print("Commands available:")
    print("1. help - Display the available commands.")
    print("2. myip - Display the IP address of this process.")
    print("3. myport - Display the port on which this process is listening.")
    print("4. connect <destination> <port> - Connect to a remote peer.")
    print("5. list - Display a list of active connections.")
    print("6. terminate <connection id> - Terminate a connection.")
    print("7. send <connection id> <message> - Send a message to a connection.")
    print("8. exit - Closes the program.")    



# Yongkang - Lists all connections and respective IDs
def list_connections():
    if currentUsers:
        print("Active connections:")
        for connection_id, (_, (client_ip, client_port)) in currentUsers.items():
            print(f"{connection_id}: {client_ip} : {client_port}")
    else:
        print("No active connections.")
        

#Haik - method for detecting and processing commands
def takeCommands(): 
    print("Type 'help' for a menu of app commands.")
    while True:
        #Haik - prints command menu without spaces
        command = input("> ").strip()
        
        if command.startswith("help"):
            help_list()
            
        elif command.startswith("myip"): #Haik - prints ip
            your_ip = socket.gethostbyname(socket.gethostname())
            print(f"Your IP: {your_ip}")
            
        elif command.startswith("myport"):#Haik - prints port
            print(f"Your port: {PORT}")
            
        elif command.startswith("connect"):
            parts = command.split()
            if len(parts) == 3:
                peer_connect(parts[1], parts[2])
            else:
                print("Correct usage: connect <destination_ip> <port>")
            
        elif command == "list":
            list_connections()
            
        elif command.startswith("terminate"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                id = int(parts[1])
                if id in currentUsers.keys():
                    client_socket, _ = currentUsers[id]
                    client_socket.send(str.encode("/&terminate"))
                    del currentUsers[id]
                    
                else:
                    print("Invalid id for termination.")
            else:
                print("Usage: terminate <connection_id>")
            
        elif command.startswith("send"):
            parts = command.split(maxsplit=2)
            if len(parts) == 3 and parts[1].isdigit():
                send(int(parts[1]), parts[2])
            else:
                print("Usage: send <connection_id> <message>")
        
        elif command == "exit":
            print("Closing all connections and shutting down the server...")
            server_ip = socket.gethostbyname(socket.gethostname())
            for client_socket, _ in currentUsers.values():
                client_socket.send(str.encode("/&exit"))
                client_socket.close()
            currentUsers.clear()
            print("Server shut down.")
            sys.exit(0)
            
        else:
            print("Unknown command. Type 'help' to see the list of commands.")
    

# Jian - Server handling incoming msgs from newly connected clients/users
def manageClient(client_socket, client_addr):
    # This function manages incoming messages from a connected client
    try:
        while True:
            try:
                message = client_socket.recv(1024).decode()  # Get messages from the client
                
                if message.startswith("/&connect"):
                    connection = message.split()
                elif message.startswith("/&terminate") or message.startswith("/&exit"):
                    id = list(currentUsers.keys())[list(currentUsers.values()).index((client_socket, client_addr))]
                    del currentUsers[id]
                    print(f"{client_addr} has disconnected.")
                    break                    
                else:
                    print(f"Message from {client_addr}: {message}")

            except ConnectionAbortedError:
                # This exception happens if the server closes the connection
                print(f"Connection with {client_addr} ended by the server.")
                break  # Exit the loop

    except ConnectionResetError:
        # This exception happens if the client forcefully closes the connection
        print(f"Lost connection to {client_addr}.")
    finally:
        client_socket.close()  # Always make sure to close the connection
    

    
def server_start(): 
    #Haik - created socket class object for the mainServer.
    mainServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #Haik - binds the server to the host and port number. if it doesnt work, it prints the error.
        mainServer.bind(('', PORT))
        mainServer.listen(USERS)
        server_ip = socket.gethostbyname(socket.gethostname())
        print(f"Server is running at {server_ip} : {PORT}.")
        
    except:   
        print(f"Unable to bind to host {HOST} and server port {PORT}.") #error message
        sys.exit(1)
    
    # Jian - Start accepting input
    threading.Thread(target=takeCommands, daemon=True).start()

    while True:
        client_socket, client_addr = mainServer.accept()
        
        new_ip = client_addr[0]
        new_port = client_addr[1]
        print(f"New connection from {new_ip} : {new_port}")
        connection_id = len(currentUsers) + 1
        currentUsers[connection_id] = (client_socket, (new_ip, new_port))
        
        threading.Thread(target=manageClient, args=(client_socket, client_addr)).start()
        

if __name__ == "__main__":
    server_start()