import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time

from clientthread import ClientListener
from game import Game

class Server() :

    def __init__(self, port):
            self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.bind(('', port))
            self.listener.listen(1)
            print("Listening on port", port)
            self.clients_sockets= []
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            self.running = False
            self.nbJoueur = 2
    
    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread= ClientListener(self, client_socket, client_adress, self)
            client_thread.start()
            time.sleep(0.1)
            if len(self.clients_sockets) >= self.nbJoueur and not self.running:
                self.game = Game(self.nbJoueur, self.clients_sockets)


    def signal_handler(self, signal, data):
        self.listener.close()
        print("QUIT")
        sys.exit()

    def initJoueur(self, data) :
        parts = data.split(": ", 1)
        if len(parts) >= 2:
            self.nbJoueur = int(parts[1])

    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)

    def receiveData(self, data, adresse) :
        self.game.receiveData(data, adresse)
    
if __name__ == "__main__":
    server= Server(59001)
    server.run()