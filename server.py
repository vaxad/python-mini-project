from socket import *
from threading import *

clients = set()         # set of all clients connected to the server

def clientThread(clientSocket, clientAddress):
    while True:
        message = clientSocket.recv(1024).decode("utf-8")                            # receive message from client     
        print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
        for client in clients:
            if client is not clientSocket:                                           # send message to all clients except the sender
                client.send((str(message)).encode("utf-8"))

        if not message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break

    clientSocket.close()

hostSocket = socket(AF_INET, SOCK_STREAM)                               # create socket with IPv4 and TCP protocol
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)                       # reuse socket address

hostIp = "192.168.29.163"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print ("Waiting for connection...")


while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients.add(clientSocket)                                       # add client to the set of clients
    print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress ))       # create a thread for each client
    thread.start()