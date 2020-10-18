from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s е поврзан." % client_address)
        client.send("Внеси го своето име и притисни „Испрати“".encode("utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = """Добредојде %s! За излез испрати „Чао(*)“ """ % name
    client.send(welcome.encode("utf-8"))
    msg = "%s се приклучи!" % name
    broadcast(msg.encode("utf-8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != "Чао(*)".encode("utf-8"):
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[client]
            broadcast("%s ја напушти собата." % name.encode("utf-8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(prefix.encode("utf-8")+msg)

        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Серверот е воспоставен!")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()