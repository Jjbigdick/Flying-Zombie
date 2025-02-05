import socket
import threading
import asyncio

BACKEND_SERVERS = [("127.0.0.1", 8081), ("127.0.0.1", 8082)]  # List of backend servers



def handle_client(client_socket):
    request = client_socket.recv(4096)
    backend_index = hash(request) % len(BACKEND_SERVERS)  # Simple load balancing logic
    backend_server = BACKEND_SERVERS[backend_index]
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.connect(backend_server)
    backend_socket.send(request)
    response = backend_socket.recv(4096)
    client_socket.send(response)
    client_socket.close()
    backend_socket.close()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:8080")
    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
