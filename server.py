import socket
import threading
from queue import Queue
import select

queue = Queue()


class ClientThread(threading.Thread):
    def __init__(self, client1, client2):
        threading.Thread.__init__(self)
        self.addr1 = client1[0]
        self.sock1 = client1[1]
        self.addr2 = client2[0]
        self.sock2 = client2[1]
        print("New connection added: ", self.addr1, self.addr2)

    def run(self):
        isRunning = False
        ok1 = False
        ok2 = False
        print("Connection from : ", self.addr1, self.addr2)
        while True:
            if isRunning == False:
                print("hiiii")
                ready1 = select.select([self.sock1], [], [], 0.05)
                if ready1[0]:
                    sock1_rep = self.sock1.recv(1024)
                    if sock1_rep.decode() == "ok":
                        print("1")
                        print(sock1_rep)
                        ok1 = True
                ready2 = select.select([self.sock2], [], [], 0.05)
                if ready2[0]:
                    sock2_rep = self.sock2.recv(1024)
                    if sock2_rep.decode() == "ok":
                        print("2")
                        print(sock2_rep)
                        ok2 = True
                if ok1 == True and ok2 == True:
                    print("startasdfasdfasdfasdfasd")
                    self.sock1.send(bytes("start", 'UTF-8'))
                    self.sock2.send(bytes("start", 'UTF-8'))
                    isRunning = True
                    ok1 = False
                    ok2 = False
            else:
                self.sock1.setblocking(0)
                self.sock2.setblocking(0)
                ready1 = select.select([self.sock1], [], [], 0.05)
                if ready1[0]:
                    data1 = self.sock1.recv(4096)
                    msg1 = data1.decode()
                    print("from client 1", msg1)
                    self.sock2.send(bytes(msg1, 'UTF-8'))
                    if msg1 == 'endgame':
                        isRunning = False
                ready2 = select.select([self.sock2], [], [], 0.05)
                if ready2[0]:
                    data2 = self.sock2.recv(4096)
                    msg2 = data2.decode()
                    print("from client 2", msg2)
                    self.sock1.send(bytes(msg2, 'UTF-8'))
                    if msg2 == 'endgame':
                        isRunning = False
        print("Client at ", self.addr1, self.addr2, " disconnected...")



LOCALHOST = "127.0.0.1"
PORT = 8080
# IPv4, TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen()
    clientSocket, clientAddress = server.accept()
    queue.put([clientAddress, clientSocket])
    if queue.qsize() > 1:
        newthread = ClientThread(queue.get(), queue.get())
        newthread.start()
