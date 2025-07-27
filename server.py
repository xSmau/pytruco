import socket 
from _thread import *
import sys
from menu import ip_address

serverConnected = ""
serverStatus = ""
server = str(ip_address) #Aqui debe ir la direccion IP del HOST
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
serverStatus = "Esperando por conexion... Servidor iniciado!"
print(serverStatus)

def threaded_client(conn):

    conn.send(str.encode("Conectado!"))

    respuesta = ""
    while True:
        try:
            data = conn.recv(2048)
            respuesta = data.decode("utf-8")

            if not data:
                serverConnected = "Desconectado!"
                print(serverConnected)
                break
            else:
                print("Recibido: ", respuesta)
                print("Enviando: ", respuesta)
            
            conn.sendall(str.encode(respuesta))
        except error as e:
            print(e)
            serverConnected = "Conexion perdida!"
            break

    print(serverConnected)
    conn.close()

while True:
    conn, addr = s.accept()
    serverConnected = ("Conectado a: ", addr)
    print(str(serverConnected))

    start_new_thread(threaded_client, (conn, ))