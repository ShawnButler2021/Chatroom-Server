# add better quit protocol
# add nickname capability
# add choice of port and 
# add choice of hostname/ip


import socket
import sys
import time
import threading



HOST = socket.gethostbyname('localhost')
PORT = 50007

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