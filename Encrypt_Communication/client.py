import socket
import ssl

def create_secure_client():
    # Server Certificate to authenticate the connection
    CERT_FILE = 'server.crt'
    
    # Create a regular TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    # Load the server's certificate (if using self-signed certs)
    context.load_verify_locations(CERT_FILE)

    # Connect to the server using the wrapped socket
    secure_sock = context.wrap_socket(sock, server_hostname='localhost')
    
    try:
        secure_sock.connect(('localhost', 8443))
        print("Client connected securely.")
        secure_sock.sendall(b"Hello, secure server!")
        
        # Receive response from the server
        data = secure_sock.recv(1024)
        print(f"Received: {data.decode('utf-8')}")
    finally:
        # Properly close the secure socket connection
        secure_sock.close()

if __name__ == "__main__":
    create_secure_client()
