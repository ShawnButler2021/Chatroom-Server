# add better quit protocol
# add nickname capability


import socket
import sys
import time
import threading
import re

def is_valid_int(string):
    try:
        value = int(string)
        return True
    except ValueError:
        return False

def is_valid_ipv4(arg):
    ip_pattern=re.compile(r'^([0-9]{1,3}\.){3}\d{1,3}$')
    return bool(ip_pattern.findall(HOST))

def is_valid_hostname(string):
    pattern = re.compile(r'^[a-zA-Z0-9.-]+$', re.IGNORECASE)
    return bool(pattern.match(string))

PORT, HOST = None, None

if len(sys.argv) != 3:
    print("python client.py [HOST] [PORT]")
    print('Taking default settings...')
    HOST = socket.gethostbyname('localhost')
    PORT = 50007
else:
    HOST = sys.argv[1]
    # checking if hostname is valid using regex
    while not is_valid_ipv4(HOST) or not is_valid_hostname(HOST):
        HOST = input('HOST: ')
    
    PORT = sys.argv[2]
    # checking if port number is valid
    while True:
        while not is_valid_int(PORT):
            PORT = input('PORT: ')
        PORT = int(PORT)
        if 1 <= int(PORT) <= 65535:
            break
        PORT = 'None'
    PORT = int(PORT)



# taken & tweaked from echo client program at
# https://docs.python.org/3/library/socket.html#example
# and annotated for own understanding
# ================
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res

    # attempting to create the socket
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue

    # attempting to connect
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
# ================


def accept_msg():
    try:
        with s:
            while True:
                data = s.recv(1024)

                if len(data) > 0:
                    print(data.decode())
    except ConnectionAbortedError:
        print("Connection aborted...")


def send_msg():
    with s:
        while True:
            msg = input("")

            if msg == '/q':
                print('quiting...')
                break

            s.sendall(msg.encode('utf-8'))




if __name__ == '__main__':
    t1 = threading.Thread(target=accept_msg)
    t2 = threading.Thread(target=send_msg)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
