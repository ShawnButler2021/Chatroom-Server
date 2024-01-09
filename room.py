# better quit protocol
# add nickname capability

import socket
import sys
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
MAX = None
clients = []

if len(sys.argv) != 4:
    print('python room.py [HOSTNAME] [PORT] [MAX CLIENTS]')
    print('Taking default settings...')
    HOST = socket.gethostbyname('localhost')
    PORT = 50007
    MAX = 2
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

    MAX = sys.argv[3]
    while not is_valid_int(MAX):
        MAX = input("Max number of clients: ")
    MAX = int(MAX)



print(f'Host: {HOST}')
print(f'Port: {PORT}')
print(f'Max # of clients: {MAX}')
# taken from echo server program at
# https://docs.python.org/3/library/socket.html#example
# and annotated for own understanding
# ================
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res

    # attempting to create socket
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue

    # attempting to bind socket and setting to listen
    try:
        s.bind(sa)
        s.listen(MAX)
    except OSError as msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

# ================





# for sending messages to all clients
def broadcast(msg):
    for client in clients:
        client[0].sendall(msg.encode('utf-8'))


def recv_data(client, hostname):
    try:
        while True:
            data = client.recv(1024).decode()
            msg = f'{hostname}: ' + data
            broadcast(msg)

            if data == b'/q':
                clients.remove((client, hostname))
                client.close()
                raise ConnectionResetError


    except ConnectionResetError:
        print(f'{hostname} has left...')
        return


# starting thread
# thread specifically for accepting connections,
# other threads branch from this one to follow connections
def accept_connections():
    while True:
        if len(clients) < MAX:
            conn, addr = s.accept()
            name = socket.gethostbyaddr(addr[0])[0]
            clients.append((conn, name))
            threads.append(threading.Thread(target=recv_data, args=(conn, name,)))
            threads[-1].start()
            msg = f'{name} has joined the chat...'
            broadcast(msg)


if __name__ == '__main__':
    threads = []
    threads.append(threading.Thread(target=accept_connections))

    threads[0].start()

