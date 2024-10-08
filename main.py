import socket
import threading
from ChatServer import server_start
from ChatClient import client_start


# Jian - Runs 2 threads on 1 machine for client and server
server_thread = threading.Thread(target=server_start)
server_thread.start()
client_thread = threading.Thread(target=client_start)
client_thread.start()