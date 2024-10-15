import socket
import ssl

# Server Certificate and Private Key
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

def create_secure_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8443))  # Bind to localhost on port 8443 (default HTTPS port)
    sock.listen(5)
    print("Server listening on port 8443...")

    # Wrap socket with SSL/TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    while True:
        # Accept connections
        client_socket, addr = sock.accept()
        print(f"Connection from {addr}")

        # Secure the connection with SSL/TLS
        secure_sock = context.wrap_socket(client_socket, server_side=True)

        try:
            # Receive data from the client
            data = secure_sock.recv(1024)
            print(f"Received: {data.decode('utf-8')}")
            secure_sock.sendall(b"Hello, secure client!")
        finally:
            # Properly close the secure socket connection
            secure_sock.shutdown(socket.SHUT_RDWR)
            secure_sock.close()

if __name__ == "__main__":
    create_secure_server()
