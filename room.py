# better quit protocol
# add choice of max clients
# add choice of hostname
# add choice of port number
# add nickname capability

import socket
import sys
import threading

HOST = None
PORT = None
MAX = None
clients = []

if len(sys.argv) != 4:
    print('python room.py [HOSTNAME] [PORT] [MAX CLIENTS]')
    print('Taking default settings...')
    HOST = socket.gethostbyname('localhost')
    PORT = 50007
    MAX = 2
else:
    HOST = socket.gethostbyname(sys.argv[1])
    PORT = int(sys.argv[2])
    MAX = int(sys.argv[3])




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

