import socket

BYTES_TO_READ = 4096
HOST = "127.0.0.1"
PORT = 8080

def handle_connection(conn, addr):
    with conn: 
        print(f"Got a connection from {addr}") 
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            conn.sendall(data) 
            

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(1)

        conn, addr = s.accept() #It returns a new socket object representing the connection and a tuple holding the address of the client.
        handle_connection(conn, addr)

start_server()