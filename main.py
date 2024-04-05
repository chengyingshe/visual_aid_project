import threading
from socket_client import socket_client
from socket_server import socket_server
import time

def run_socket_client_thread():
    t = threading.Thread(target=socket_client)
    t.start()
    print('socket_client thread start.')
    return t

def run_socket_server_thread():
    t = threading.Thread(target=socket_server)
    t.start()
    print('socket_server thread start.')
    return t

if __name__ == '__main__':
    run_socket_client_thread()
    time.sleep(5)  # wait 5s
    run_socket_server_thread()
