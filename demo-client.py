import socket

def message():
    while True:
            msg = input("-> ")
            if msg != "":
                return msg
            else:
                continue
def client():
    # Currently the host has to be the same as the 
    host = socket.gethostname()
    port = 3645
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host,port))
        msg = message()
        while msg.lower().strip() != 'exit':
            client_socket.send(msg.encode())
            data = client_socket.recv(1024).decode()

            print("Server's Message:{}".format(data))

            msg = input ("-> ")


if __name__ == "__main__":
    client()




