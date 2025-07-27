import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with open("data\\ip_address.txt", "r", encoding="utf-8") as archivo:
            ip_address = archivo.readline()  # Lee solo la primera línea
            self.server = str(ip_address.strip())
        #self.server = str(ip_add) 
        #Aqui ^ va el IP del HOST
        #   Ademas debe de ser el que esta en server.py
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
            