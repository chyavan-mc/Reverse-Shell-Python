import sys
import socket


#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Creation error:", str(msg))


#Bind socket to port and wait for client
def bind_socket():
    try:
        print("Binding to port", port)
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Binding error:", str(msg))
        bind_socket()


#Establish connection
def accept_socket():
    conn, address = s.accept()
    print("Established!\nIP:",address[0],"\nPort:",address[1])
    send_command(conn)
    conn.close()


def send_command(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")
            print(client_response, end="")

def main():
    create_socket()
    bind_socket()
    accept_socket()

main()