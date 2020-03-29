import socket


def create_socket():
    try:
        global server_socket
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: {}".format(msg))

def bind_socket():
    try:
        print("Attempting to bind to the port: {}".format(port))
        server_socket.bind((host,port))
        server_socket.listen()
        print("Bind successful")
    except socket.error as msg:
        print("Socket binding error: {}".format(msg))
        bind_socket()

def communication_loop(connection):
    while True:
        # Decrypt message

        data = connection.recv(1024).decode()
        # If no data has been recieved the loop will break
        if not data:
            break
        else:
            print("Client's message: {}".format(data))
            # Encryption of message

            msg = input("-> ")
            connection.send(msg.encode())

def accepting_connection():
    conn,addr = server_socket.accept()
    with conn:
        print("Client has connected - IP Address: {} | Port: {}".format(addr[0],addr[1]))
        communication_loop(conn)

def main():
    create_socket()
    bind_socket()
    accepting_connection()

if __name__ == '__main__':
    host = socket.gethostname()
    port = 3645
    server_socket = socket.socket()
    main()