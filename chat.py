import socket  # For socket programming use
import threading  # For handling multiple connections concrurrently
import select  # For using select() to handle multiple connections
import sys  # For handling command-line arguments and standard input

# Create a function to display all the helps menu with the available commands


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

# Create a function to get the actual IP address of this machine


def get_ip_address():
    return socket.gethostbyname(socket.gethostbyname())

# Create a function to handle each client's connection in a separate thread


def handle_client(client_socket, client_address):
    # Continuously listen for message from the connected client (handle errors without crash)
    try:
        while True:
            # Read incoming daa from the client (max amout date is 1024 bytes)
            message = client_socket.recv(1024)
            if message:  # If there is message from the client
                # client_address[0] and client_address[1] meansing IP address and port number
                # message.decode('utf-8') means to converts the received byte data into a string format using utf-8 encoding
                print(f"Message from {client_address[0]}:{client_address[1]} - {message.decode('utf-8')}")
            else:  # If no message received, the client has disconnected
                print(f"Client {client_address[0]}:{client_address[1]} hass disconnected.")
                break  # Exit the loop to close the connection
    # Ensure the client socket is always closed when done, even with an error occurs
    finally:
        client_socket.close()  # Close the client socket when the clients disconnected

# Create a main function in order to start the chat server


def main():
    # Chect if the port number is proved as a command-line argument
    if len(sys.argv) != 2:  # If the length != 2, it means the user didn't provide the required port number
        print("Usage: python chat.py <port>")
        # Generally indicates an error. It stops the execution because the port num was not supplied
        sys.exit(1)

    # Get the port number from the command-line argument
    port = int(sys.argv[1])
    ip_address = get_ip_address  # Get the IP address of this machine

    # Create and set up the listening socket for incoming connections
    # AF_INET means Address Family - Internet; socket will use IPv4 address protocol
    # SOCK_STREAM means socket type is TCP
    # Create TCP socket using IPv4 communication
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the IP address and port
    server_socket.bind((ip_address, port))
    server_socket.listen(3)  # Start listening with a backlog of 3 connections
    print(f"Chat server started on {ip_address}:{port}")
    print(f"Type 'help' to see the list of available commands.")

    # List to keep track of socket connections
    # Includes the server socket and standard input(commands)
    sockets_list = {server_socket, sys.stdin}
    clients = {}  # Dictionary to keep track of connected clients

    while True:
        # Use select to monitor multiple sockets and standard input
        # The first assingment only interested in the sockets that are ready to be read, ignore the other 2 list
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            # If the event is on the server socket, it means a new connection is incoming
            if notified_socket == server_socket:
                # If the server socket is notified, accept a new cliect connection
                client_socket, client_address = server_socket.accept()
                # Add the new client socket to the list
                sockets_list.append(client_socket)
                # Keep track of the client's address
                clients[client_socket] = client_address
                # client_address[0] and client_address[1] meansing IP address and port number
                print(f"New connection established from {client_address[0]}:{client_address[1]}")

                # Create a new thread to handle the client's connection
                # client_thread creats a new thread in the program
                # target = handle_client means the function that the new thread will run
                # args = (client_socket, client_address) means the thread will use these values to interact with specific client
                client_thread = threading.Thread(
                    target=handle_client, args=(client_socket, client_address))
                # Start the new created thread to handle communication with the client
                client_thread.start()

            # If the event is on standard input (when user typed a command)
            elif notified_socket == sys.stdin:
                command = input().strip()  # Read the command from the user

                # For handle different comments
                if command == "help":
                    help_list()

                elif command == "myip":
                    print(f"IP address: {ip_address}")

                elif command == "myport":
                    print(f"Port number: {port}")

                elif command == "exit":
                    print("Exiting the program...")
                    for sock in socket_list:  # Repeat through each socket stored in the socket_list
                        sock.close()  # Close all sockets
                    # Exit the program with a success status. If it's non-zero value, there will be an error.
                    sys.exit(0)

            else:
                print("Unknown command. Type 'help' for available commands.")
                
if __name__ == "__main__":
    main()  # Call the main function to start the server
