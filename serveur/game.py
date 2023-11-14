import json
import pygame
import sys
import random

import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time
from clientthread import ClientListener

from player import Player
from explosion import Explosion

class Game():
    global ene_blocks
    global player
    global running
    global game_ended
    global explosions
    global bombs
    global power_ups
    global clients_sockets

    global grid

    def __init__(self, port):
        self.grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets= []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.running = False

    def signal_handler(self, signal):
        self.listener.close()
        self.echo("QUIT")

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
            if len(self.clients_sockets) >= 2 and not self.running:
                self.game_init()

    def remove_socket(self, socket):
        self.client_sockets.remove(socket)

    def sendPlayer1(self):
        if len(self.clients_sockets) >= 2 and self.running:

            jsonPlayer1 = {
            "type": "player1",
            "data": self.player[0].to_json()
            }

            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer1)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in self.clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendPlayer2(self):
        if len(self.clients_sockets) >= 2 and self.running:

            jsonPlayer2 = {
                    "type": "player2",
                    "data": self.player[1].to_json()
                }
            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonPlayer2)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in self.clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendBombs(self):
        if len(self.clients_sockets) >= 2 and self.running:
            delimiter = b'\x00'
            try:
                for bomb in self.bombs:
                    # Conversion de l'objet JSON en chaîne et envoi au client
                    json_str = json.dumps({
                        "type": "bomb",
                        "data": bomb.to_json()
                    })
                    json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                    
                    for sock in self.clients_sockets:
                        sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendExplosions(self):
        if len(self.clients_sockets) >= 2 and self.running:
            delimiter = b'\x00'
            try:
                for explosion in self.explosions:
                    # Conversion de l'objet JSON en chaîne et envoi au client
                    json_str = json.dumps({
                        "type": "explosion",
                        "data": explosion.to_json()
                    })
                    json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                    
                    for sock in self.clients_sockets:
                        sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendPowerUps(self):
        if len(self.clients_sockets) >= 2 and self.running:
            delimiter = b'\x00'
            try:
                for power_up in self.power_ups:
                    # Conversion de l'objet JSON en chaîne et envoi au client
                    json_str = json.dumps({
                        "type": "power_up",
                        "data": power_up.to_json()
                    })
                    json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                    
                    for sock in self.clients_sockets:
                        sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def sendGrid(self):
        if len(self.clients_sockets) >= 2 and self.running:

            jsonGrid = {
                    "type": "grid",
                    "data": {"grid": json.dumps(self.grid)}
                }
            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonGrid)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in self.clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendRunning(self):
        if len(self.clients_sockets) >= 2 and self.running:

            jsonRunning = {
                    "type": "running",
                    "data": json.dumps({'running': self.running})
                }
            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonRunning)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in self.clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")

    def sendEnded(self):
        if len(self.clients_sockets) >= 2 and self.running:

            jsonEnded = {
                    "type": "game_ended",
                    "data": json.dumps({'game_ended': self.game_ended})
                }
            
            delimiter = b'\x00'
            try:
                # Conversion de l'objet JSON en chaîne et envoi au client
                json_str = json.dumps(jsonEnded)
                json_str_with_delimiter = json_str.encode("UTF-8") + delimiter
                for sock in self.clients_sockets:
                    sock.sendall(json_str_with_delimiter)
            except socket.error:
                print("Impossible d'envoyer le message")


    def receiveData(self, data, adresse) :
        parts = data.split(": ", 1)
        if len(parts) >= 2:
            username = parts[0]
            instruction = parts[1]
            index = self.find_client_index(adresse)
            if index != -1:
                if self.player[index].life:
                    temp = self.player[index].direction
                    movement = False
                    if instruction == "DOWN" :
                        temp = 0
                        self.player[index].move(0, 1, self.grid, self.ene_blocks, self.power_ups)
                        movement = True
                    elif instruction == "RIGHT" :
                        temp = 1
                        self.player[index].move(1, 0, self.grid, self.ene_blocks, self.power_ups)
                        movement = True
                    elif instruction == "UP" :
                        temp = 2
                        self.player[index].move(0, -1, self.grid, self.ene_blocks, self.power_ups)
                        movement = True
                    elif instruction == "LEFT" :
                        temp = 3
                        self.player[index].move(-1, 0, self.grid, self.ene_blocks, self.power_ups)
                        movement = True
                    if temp != self.player[index].direction:
                        self.player[index].frame = 0
                        self.player[index].direction = temp
                    if movement:
                        if self.player[index].frame == 2:
                            self.player[index].frame = 0
                        else:
                            self.player[index].frame += 1
                    self.sendPlayer1()
                    self.sendPlayer2()

                    if instruction == "QUIT" :
                        sys.exit(0)
                    if instruction == "SPACE" :
                        if self.player[index].bomb_limit != 0 :
                            temp_bomb = self.player[index].plant_bomb(self.grid)
                            self.bombs.append(temp_bomb)
                            self.grid[temp_bomb.pos_x][temp_bomb.pos_y] = 3
                            self.player[index].bomb_limit -= 1
                            self.sendBombs()
                    elif instruction == "ESCAPE" :
                        self.running = False
        

    def find_client_index(self, adresse):
        for index, client_socket in enumerate(self.clients_sockets):
            if client_socket.getpeername() == adresse:
                return index
        return -1

    def game_init(self):
        self.game_ended = False
        self.bombs = []
        self.explosions = []
        self.power_ups = []
        self.ene_blocks = []
        self.bombs.clear()
        self.explosions.clear()
        self.power_ups.clear()

        self.player = [Player(4,4),Player(44,44)]

        self.ene_blocks.append(self.player[0])
        self.ene_blocks.append(self.player[1])
        
        self.running = True
        self.main()


    def generate_map(self):
        for i in range(1, len(self.grid) - 1):
            for j in range(1, len(self.grid[i]) - 1):
                if self.grid[i][j] != 0:
                    continue
                elif (i < 3 or i > len(self.grid) - 4) and (j < 3 or j > len(self.grid[i]) - 4):
                    continue
                if random.randint(0, 9) < 7:
                    self.grid[i][j] = 2

        return


    def main(self):
        self.grid = [row[:] for row in self.grid]
        self.generate_map()
        self.sendPlayer1()
        self.sendPlayer2()
        self.sendGrid()
        self.sendEnded()
        self.sendRunning()
        # power_ups.append(PowerUp(1, 2, PowerUpType.BOMB))
        # power_ups.append(PowerUp(2, 1, PowerUpType.FIRE))
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(15)
            self.sendGrid()
                
            if not self.game_ended:
                self.game_ended = self.check_end_game()

            self.update_bombs(dt)

        self.explosions.clear()
        self.ene_blocks.clear()
        self.power_ups.clear()

    def update_bombs(self, dt):
        for b in self.bombs:
            b.update(dt)
            if b.time < 1:
                b.bomber.bomb_limit += 1
                self.grid[b.pos_x][b.pos_y] = 0
                exp_temp = Explosion(b.pos_x, b.pos_y, b.range)
                exp_temp.explode(self.grid, self.bombs, b, self.power_ups)
                exp_temp.clear_sectors(self.grid, random, self.power_ups)
                self.explosions.append(exp_temp)
                self.sendBombs()
                self.sendExplosions()
        for pl in self.player:
            pl.check_death(self.explosions)
        for e in self.explosions:
            e.update(dt)
            if e.time < 1:
                self.explosions.remove(e)
                self.sendExplosions()


    def check_end_game(self):
        for pl in self.player:
            if pl.life:
                return False

        return True



if __name__ == "__main__":
    server= Game(59001)
    server.run()