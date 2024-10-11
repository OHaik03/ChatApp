import socket  # Importing socket to create network connections
import threading  # Importing threading to manage multiple clients at the same time
import sys  # Importing sys to handle command-line arguments and to exit the program

# Check if a port number is provided when running the script
if len(sys.argv) != 2:
    print("Please use the format: python chat.py <port_number>")  # Show correct usage
    sys.exit(1)  # Exit if port number is missing

# Get the port number from the command-line argument
SERVER_PORT = int(sys.argv[1])  # We'll use this port to start our server

# Dictionary to keep track of connected clients using a unique ID
clients = {}  # This dictionary will store each client's socket and address

# Show the list of available commands for the server user
def help_list():
    # This function displays all the commands that the server can use
    print("Here's a list of commands you can use:")
    print("1. help - Shows all available commands.")
    print("2. myip - Displays this server's IP address.")
    print("3. myport - Displays this server's port number.")
    print("4. connect <destination_ip> <port> - Connects to another server.")
    print("5. list - Lists all active connections.")
    print("6. send <connection_id> <message> - Sends a message to a specific client.")
    print("7. terminate <connection_id> - Disconnects a specific client.")
    print("8. exit - Closes all connections and shuts down the server.")

# Handle communication with a client
def handle_client(client_socket, client_address):
    # This function manages incoming messages from a connected client
    try:
        client_socket.send("Welcome! Type 'help' to see what you can do.".encode())

        while True:
            try:
                message = client_socket.recv(1024).decode()  # Get messages from the client

                if message.lower() == "help":  # If the client asks for help
                    # Send the list of commands to the client
                    client_socket.send("Commands you can use: "
                                       "\n1. help - Shows available commands."
                                       "\n2. myip - Displays this server's IP."
                                       "\n3. myport - Displays this server's port."
                                       "\n4. connect <destination_ip> <port> - Connects to another server."
                                       "\n5. list - Lists all connections."
                                       "\n6. send <connection_id> <message> - Sends a message to a client."
                                       "\n7. terminate <connection_id> - Disconnects your connection."
                                       "\n8. exit - Close your connection.".encode())

                elif message.lower() == "list":  # If the client wants to see active connections
                    if clients:
                        # Build a list of active connections and send it to the client
                        connection_list = "Active connections:\n"
                        for connection_id, (_, (client_ip, client_port)) in clients.items():
                            connection_list += f"{connection_id}: {client_ip}:{client_port}\n"
                        client_socket.send(connection_list.encode())
                    else:
                        client_socket.send("No active connections at the moment.".encode())

                elif message:  # For other received messages that don't match a command
                    print(f"Message from {client_address}: {message}")  # Display the client's message

                else:  # If the message is empty, it means the client has disconnected
                    print(f"{client_address} disconnected.")
                    break  # Exit the loop

            except ConnectionAbortedError:
                # This exception happens if the server closes the connection
                print(f"Connection with {client_address} ended by the server.")
                break  # Exit the loop

    except ConnectionResetError:
        # This exception happens if the client forcefully closes the connection
        print(f"Lost connection to {client_address}.")
    finally:
        client_socket.close()  # Always make sure to close the connection

# Connect to another server or peer
def connect_to_peer(destination_ip, destination_port):
    # This function connects to another server using the given IP address and port number
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((destination_ip, int(destination_port)))
        connection_id = len(clients) + 1  # Assign a new ID for the connection
        clients[connection_id] = (client_socket, (destination_ip, destination_port))
        print(f"Successfully connected to {destination_ip}:{destination_port}")
    except Exception as e:
        print(f"Couldn't connect to {destination_ip}:{destination_port}. Reason: {e}")

# List all active client connections
def list_connections():
    # This function displays all currently connected clients to the server user
    if clients:
        print("Here are the current connections:")
        for connection_id, (_, (client_ip, client_port)) in clients.items():
            print(f"{connection_id}: {client_ip}:{client_port}")
    else:
        print("No connections right now.")

# Disconnect a specific client
def terminate_connection(connection_id):
    # This function closes the connection to a specific client using its ID
    if connection_id in clients:
        client_socket, client_address = clients.pop(connection_id)
        try:
            client_socket.send("Connection closed by the server.".encode())
        except Exception as e:
            print(f"Couldn't notify {client_address} about termination: {e}")
        client_socket.close()
        print(f"Disconnected from {client_address}")
    else:
        print("That connection ID doesn't exist.")

# Send a message to a specific client
def send_message_to_client(connection_id, message):
    # This function sends a message to a specific client identified by its connection ID
    if connection_id in clients:
        client_socket, client_address = clients[connection_id]
        try:
            client_socket.send(message.encode())
            print(f"Message sent to {client_address}: {message}")
        except Exception as e:
            print(f"Failed to send message to {client_address}: {e}")
    else:
        print("Invalid connection ID.")

# Handle server commands entered by the user
def handle_commands():
    while True:
        command = input("\nCommand (type 'help' to see options): ").strip()

        if command == "help":
            help_list()  # Show the list of commands
        elif command == "myip":
            server_ip = socket.gethostbyname(socket.gethostname())
            print(f"Server IP: {server_ip}")
        elif command == "myport":
            print(f"Server Port: {SERVER_PORT}")
        elif command.startswith("connect"):
            parts = command.split()
            if len(parts) == 3:
                connect_to_peer(parts[1], parts[2])
            else:
                print("Correct usage: connect <destination_ip> <port>")
        elif command == "list":
            list_connections()
        elif command.startswith("send"):
            parts = command.split(maxsplit=2)
            if len(parts) == 3 and parts[1].isdigit():
                send_message_to_client(int(parts[1]), parts[2])
            else:
                print("Usage: send <connection_id> <message>")
        elif command.startswith("terminate"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                terminate_connection(int(parts[1]))
            else:
                print("Usage: terminate <connection_id>")
        elif command == "exit":
            print("Closing all connections and shutting down the server...")
            for client_socket, _ in clients.values():
                client_socket.close()
            clients.clear()
            print("Server shut down.")
            sys.exit(0)
        else:
            print("Unknown command. Type 'help' to see the list of commands.")

# Start the server and wait for connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(3)
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server running at {server_ip}:{SERVER_PORT}. Waiting for connections...")

    threading.Thread(target=handle_commands, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        connection_id = len(clients) + 1
        clients[connection_id] = (client_socket, client_address)

        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
