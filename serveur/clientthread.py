from socket import socket
import threading
import re
import time

class ClientListener(threading.Thread):

    global premiereConnexion

    def __init__(self, server, socket, address, game):
        super(ClientListener, self).__init__()
        self.server= server
        self.socket= socket
        self.address= address
        self.game = game
        self.listening= True
        self.username= "No username"
        self.premiereConnexion = True

    def run(self):
        while self.listening:
            data= ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except OSError as e:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        print("{0} has quit\n".format(self.username))

    def handle_msg(self, data):
        #print(self.address, "sent :", data)
        if self.premiereConnexion :
            self.game.initJoueur(data)
            self.premiereConnexion = False
        else :
            username_result = re.search('^USERNAME (.*)$', data)
            if username_result:
                self.username = username_result.group(1)
                self.game.receiveData(data, self.address)
            elif data == "QUIT":
                self.quit()
            elif data == "":
                self.quit()
            else:
                self.game.receiveData(data, self.address)