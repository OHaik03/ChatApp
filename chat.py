import socket  # For socket programming use
import threading  # For handling multiple connections concurrently
import select  # For using select() to handle multiple connections
import sys  # For handling command-line arguments and standard input

# Function to display the help menu with available commands
def help_list():
    print("Commands available:")
    print("1. help - Display the available commands.")
    print("2. myip - Display the IP address of this process.")
    print("3. myport - Display the port on which this process is listening.")
    print("4. connect <destination> <port> - Connect to a remote peer.")
    print("5. list - Display a list of active connections.")
    print("6. terminate <connection id> - Terminate a connection.")
    print("7. send <connection id> <message> - Send a message to a connection.")
    print("8. exit - Close all connections and terminate the program.")

# Function to get the actual IP address of this machine
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())  # Get the machine's IP address

# Function to handle each client's connection in a separate thread
def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(1024)  # Read incoming data from the client
            if message:  # If there is a message from the client
                print(f"Message from {client_address[0]}:{client_address[1]} - {message.decode('utf-8')}")
            else:  # If no message is received, the client has disconnected
                print(f"Client {client_address[0]}:{client_address[1]} has disconnected.")
                break  # Exit the loop to close the connection
    finally:
        client_socket.close()  # Close the client socket when the client disconnects

# Function to handle user input commands in a separate thread
def handle_user_input(ip_address, port, sockets_list, clients):
    while True:
        command = input().strip()  # Wait for the user to enter a command and remove any extra spaces
        command_parts = command.split()  # Split the command into words to make it easier to process

        if command_parts[0] == "help":  # If the command is 'help'
            help_list()  # Call the function to display the list of available commands

        elif command_parts[0] == "myip":  # If the command is 'myip'
            print(f"My IP address: {ip_address}")  # Display the server's IP address

        elif command_parts[0] == "myport":  # If the command is 'myport'
            print(f"My port number: {port}")  # Display the port number the server is using

        elif command_parts[0] == "connect" and len(command_parts) == 3:  # If the command is 'connect' and has the right format
            destination_ip = command_parts[1]  # Get the destination IP address from the command
            destination_port = int(command_parts[2])  # Get the destination port number from the command
            connect_to_peer(destination_ip, destination_port, sockets_list, clients)  # Call the function to connect to the peer

        elif command_parts[0] == "list": # If the command is 'list'
            if clients: # Check if there are any active connection in the clients dictionary
                print("Actice connections:") # Header for list of connections
                # Loop for each client connection and display the detail
                # 'idx' holes the index of the current item in the iteration
                # 'enumerate' adds a numerical index to each of these items, start from 1 
                for idx, (client_socket, (client_ip, client_port)) in enumerate(clients.items(), start=1):
                    print(f"{idx}: {client_ip}:{client_port}") # Print the connection index, IP address, and port number
            else:
                print("No active connections now.") # Display a message if there are no connections

        elif command_parts[0] == "exit":  # If the command is 'exit'
            print("Exiting the program...")  # Inform the user that the program is closing
            for sock in sockets_list:  # Loop through all the sockets in the list
                sock.close()  # Close each socket to release the resources
            sys.exit(0)  # Exit the program safely

        else:  # If the command is not recognized
            print("Unknown command. Type 'help' for available commands.")  # Display an error message for invalid commands


# Function to connect to a remote peer and add the connection to the list
def connect_to_peer(destination_ip, destination_port, sockets_list, clients):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        client_socket.connect((destination_ip, destination_port))  # Connect to the remote peer

        # Add the new connection to the list of sockets and clients
        sockets_list.append(client_socket)
        clients[client_socket] = (destination_ip, destination_port)

        print(f"Connected to {destination_ip}:{destination_port}")
    except Exception as e:
        print(f"Failed to connect to {destination_ip}:{destination_port}. Error: {e}")

# Main function to start the chat server
def main():
    # Check if the port number is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python chat.py <port>")
        sys.exit(1)  # Stop the execution because the port number was not supplied

    port = int(sys.argv[1])  # Get the port number from the command-line argument
    ip_address = get_ip_address()  # Get the IP address of this machine

    # Create and set up the listening socket for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket using IPv4
    server_socket.bind((ip_address, port))  # Bind the socket to the IP address and port
    server_socket.listen(3)  # Start listening with a backlog of 3 connections
    print(f"Chat server started on {ip_address}:{port}")
    print("Type 'help' to see the list of available commands.")

    # List to keep track of socket connections
    sockets_list = [server_socket]  # Includes only the server socket for select
    clients = {}  # Dictionary to keep track of connected clients

    # Start a separate thread to handle user input
    user_input_thread = threading.Thread(target=handle_user_input, args=(ip_address, port, sockets_list, clients))
    user_input_thread.daemon = True  # Set as a daemon thread so it closes when the main program exits
    user_input_thread.start()

    while True:
        # Use select to monitor multiple sockets (only sockets, no standard input)
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == server_socket:  # A new connection is incoming
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)  # Add the new client socket to the list
                clients[client_socket] = client_address  # Keep track of the client's address
                print(f"New connection established from {client_address[0]}:{client_address[1]}")

                # Create a new thread to handle the client's connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()  # Start the new thread to handle communication with the client

if __name__ == "__main__":
    main()  # Call the main function to start the server
