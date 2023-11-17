import json
import socket

class Json():

    global nbJoueur

    def __init__(self, nbJoueur) :
        self.nbJoueur = nbJoueur
    
    def sendPlayer1(self, clients_sockets, running, player):
        if len(clients_sockets) >= 2 and running:
            jsonPlayer1 = [{
            "type": "player1",
            "data": player.to_json()
            }]

            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer1)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendPlayer2(self, clients_sockets, running, player):
        if len(clients_sockets) >= 2 and running:
            jsonPlayer2 = [{
                    "type": "player2",
                    "data": player.to_json()
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer2)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendPlayer3(self, clients_sockets, running, player):
        if len(clients_sockets) >= 2 and running:
            jsonPlayer3 = [{
                    "type": "player3",
                    "data": player.to_json()
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer3)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendPlayer4(self, clients_sockets, running, player):
        if len(clients_sockets) >= 2 and running:
            jsonPlayer4 = [{
                    "type": "player4",
                    "data": player.to_json()
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer4)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendBombs(self, clients_sockets, running, bombs):
        if len(clients_sockets) >= 2 and running:
            jsonBombs = [{
                    "type": "bomb",
                    "data": bomb.to_json()
                } for bomb in bombs]           
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonBombs)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendExplosions(self, clients_sockets, running, explosions):
        if len(clients_sockets) >= 2 and running:
            jsonExplosions = [{
                    "type": "explosion",
                    "data": exlpo.to_json()
                } for exlpo in explosions]          
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonExplosions)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendPowerUps(self, clients_sockets, running, power_ups):
        if len(clients_sockets) >= 2 and running:
            jsonPowerUps = [{
                    "type": "power_up",
                    "data": power.to_json()
                } for power in power_ups]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPowerUps)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendGrid(self, clients_sockets, running, grid):
        if len(clients_sockets) >= 2 and running:
            jsonGrid = [{
                    "type": "grid",
                    "data": {"grid": json.dumps(grid)}
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonGrid)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendRunning(self, clients_sockets, running):
        if len(clients_sockets) >= 2 and running:
            jsonRunning = [{
                    "type": "running",
                    "data": json.dumps({'running': running})
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonRunning)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendEnded(self, clients_sockets, running, game_ended):
        if len(clients_sockets) >= 2 and running:
            jsonEnded = [{
                    "type": "game_ended",
                    "data": json.dumps({'game_ended': game_ended})
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonEnded)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendEmptyBomb(self, clients_sockets, running):
         if len(clients_sockets) >= 2 and running:
            jsonEmptyBomb = [{
                    "type": "emptybomb"
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonEmptyBomb)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    
    def sendEmptyExplosions(self, clients_sockets, running):
         if len(clients_sockets) >= 2 and running:
            jsonEmptyExplosion = [{
                    "type": "emptyexplosion"
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonEmptyExplosion)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendEmptyPowerUp(self, clients_sockets, running):
         if len(clients_sockets) >= 2 and running:
            jsonEmptyPowerUp = [{
                    "type": "emptypower"
                }]            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonEmptyPowerUp)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")