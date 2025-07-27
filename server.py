import socket 
from _thread import *
import sys
import pickle
from data.players import Jugador
from data.cards import Carta
import random

serverConnected = ""
serverStatus = ""
ip_add =  '' #Aqui debe ir la direccion IP del HOST
port = 5555

def iniciarJugadores():
    global jugadores

    mazo = Carta.generar_mazo()
    mazo = random.shuffle(mazo)

        
    jugadores = [Jugador("jugador1"),
                 Jugador("jugador2")]
    for i in range(3):
        jugadores[0].robar_carta(mazo.pop())
        jugadores[1].robar_carta(mazo.pop())
    
def get_local_ip_address():
    global ip_address
    """
    Retrieves and returns the local IP address of the machine.
    """
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()
        # Resolve the hostname to its corresponding IP address
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        return f"Error getting IP address: {e}"

ip_add = str(get_local_ip_address)

if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((ip_add, port))


    except socket.error as e:
        print(str(e))

    s.listen(2)
    serverStatus = "Esperando por conexion... Servidor iniciado!"
    print(serverStatus)

    

    def threaded_client(conn, player):

        conn.send(pickle.dumps(jugadores[player]))

        respuesta = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                jugadores[player] = data

                if not data:
                    serverConnected = "Desconectado!"
                    print(serverConnected)
                    break
                else:

                    if player == 1:
                        respuesta = jugadores[0]
                    else:
                        respuesta = jugadores[1]
                    
                    print("Recibido: ", respuesta)
                    print("Enviando: ", respuesta)
                
                conn.sendall(pickle.dumps(respuesta))
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