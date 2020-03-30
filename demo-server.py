import socket
from cryptography.fernet import Fernet


# ------------------------------------------------------------------------- #
# Method to create the socket for the server
# ------------------------------------------------------------------------- #
def create_socket():
    try:
        global server_socket
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: {}".format(msg))
# ------------------------------------------------------------------------- #
# Method to bind the server's ports and IP Address
# ------------------------------------------------------------------------- #
def bind_socket():
    try:
        print("Attempting to bind to the port: {}".format(port))
        server_socket.bind((host,port))
        server_socket.listen()
        print("Bind successful")
    except socket.error as msg:
        print("Socket binding error: {}".format(msg))
        bind_socket()
# -------------------------------------------------------------------------- #
# Method to encrypt the message using a Fernet Object with the encryption    
# key recieved                                      
# -------------------------------------------------------------------------- #
def encryptMsg(message,fernetObj):
    return fernetObj.encrypt(message.encode())

# -------------------------------------------------------------------------- #
# Method to decrypt the message using a Fernet Object with the encryption    
# key recieved                                      
# -------------------------------------------------------------------------- #
def decryptMsg(message,fernetObj):
    return fernetObj.decrypt(message)

#def serverprompt():
  #  choice = input("Would you like to host another client? (Y/N)")
   # return choice == "Y"

# --------------------------------------------------------------------------- #
# Main event loop to allow the server to communicate with the client 
# --------------------------------------------------------------------------- #
def communication_loop(connection,FernObj):
    while True:
        # The message is recieved and decrypted
        data = decryptMsg(connection.recv(1024),FernObj).decode()
        if data == "disconnecting":
            break
        # If no data has been recieved the loop will break
        elif not data:
            break
        else:
            print("Client's message: {}".format(data))
            # Encryption of message
            msg = input("-> ")
            connection.send(encryptMsg(msg,FernObj))

# -------------------------------------------------------------------------------------- #
# Function to accept the connection from the Client
# -------------------------------------------------------------------------------------- #
def accepting_connection():
    conn,addr = server_socket.accept()
    with conn:
        print("Client has connected - IP Address: {} | Port: {}".format(addr[0],addr[1]))
        # Accepting the key
        key = conn.recv(1024)
        FernObj = Fernet(key)
        communication_loop(conn,FernObj)
        
# -------------------------------------------------------------------------------------- #
# Main driver function for the server
# -------------------------------------------------------------------------------------- #
def main():
    create_socket()
    bind_socket()
    accepting_connection()

if __name__ == '__main__':
    host = socket.gethostname()
    port = 3645
    server_socket = socket.socket()
    main()