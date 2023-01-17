import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1" 
PROXY_SERVER_PORT = 8080 #This is the port that the proxy server will listen on.

def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        #sending data to the server(google)
        client_socket.connect((host, port))
        client_socket.sendall(request_data)
        client_socket.shutdown(socket.SHUT_WR)
        #receiving data from the server(google)
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        
        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Got a connection from {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data: 
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT)) #This is the port that the proxy server will listen on.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #This is to make sure that the port is not in use.
        server_socket.listen(2) #This is the number of connections that can be queued.
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT)) #This is the port that the proxy server will listen on.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #This is to make sure that the port is not in use.
        server_socket.listen(2) #This is the number of connections that can be queued.
        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()

#https://github.com/aianta/cmmput404-tcp-lab