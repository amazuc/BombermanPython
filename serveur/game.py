import json
import pygame
import sys
import random
import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time
from enums.power_up_type import PowerUpType
from clientthread import ClientListener
from sendjson import Json
from player import Player
from explosion import Explosion
from power_up import PowerUp

class Game():
    global ene_blocks
    global player
    global running
    global game_ended
    global explosions
    global bombs
    global emptyBomb
    global emptyExplosion
    global power_ups
    global clients_sockets
    global json

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
        self.json = Json()

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


    def receiveData(self, data, adresse) :
        parts = data.split(": ", 1)
        if len(parts) >= 2:
            instruction = parts[1]
            index = self.find_client_index(adresse)
            if index != -1:
                if self.player[index].life:
                    temp = self.player[index].direction
                    movement = False
                    if instruction == "DOWN" :
                        temp = 0
                        if self.player[index].move(0, 1, self.grid, self.ene_blocks, self.power_ups):
                            if len(self.power_ups) >0:
                                self.json.sendPowerUps(self.clients_sockets, self.running, self.power_ups)
                            else :
                                self.json.sendEmptyPowerUp(self.clients_sockets, self.running)
                        movement = True
                    elif instruction == "RIGHT" :
                        temp = 1
                        if self.player[index].move(1, 0, self.grid, self.ene_blocks, self.power_ups):
                            if len(self.power_ups) >0:
                                self.json.sendPowerUps(self.clients_sockets, self.running, self.power_ups)
                            else :
                                self.json.sendEmptyPowerUp(self.clients_sockets, self.running)
                        movement = True
                    elif instruction == "UP" :
                        temp = 2
                        if self.player[index].move(0, -1, self.grid, self.ene_blocks, self.power_ups):
                            if len(self.power_ups) >0:
                                self.json.sendPowerUps(self.clients_sockets, self.running, self.power_ups)
                            else :
                                self.json.sendEmptyPowerUp(self.clients_sockets, self.running)
                        movement = True
                    elif instruction == "LEFT" :
                        temp = 3
                        if self.player[index].move(-1, 0, self.grid, self.ene_blocks, self.power_ups):
                            if len(self.power_ups) >0:
                                self.json.sendPowerUps(self.clients_sockets, self.running, self.power_ups)
                            else :
                                self.json.sendEmptyPowerUp(self.clients_sockets, self.running)
                        movement = True
                    if temp != self.player[index].direction:
                        self.player[index].frame = 0
                        self.player[index].direction = temp
                    if movement:
                        if self.player[index].frame == 2:
                            self.player[index].frame = 0
                        else:
                            self.player[index].frame += 1
                    self.json.sendPlayer1(self.clients_sockets, self.running, self.player[0])
                    self.json.sendPlayer2(self.clients_sockets, self.running, self.player[1])
                    if instruction == "QUIT" :
                        sys.exit(0)
                    if instruction == "SPACE" :
                        if self.player[index].bomb_limit != 0 :
                            temp_bomb = self.player[index].plant_bomb(self.grid)
                            self.bombs.append(temp_bomb)
                            self.grid[temp_bomb.pos_x][temp_bomb.pos_y] = 3
                            self.player[index].bomb_limit -= 1
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
        self.json.sendPlayer1(self.clients_sockets, self.running, self.player[0])
        self.json.sendPlayer2(self.clients_sockets, self.running, self.player[1])
        self.json.sendGrid(self.clients_sockets, self.running, self.grid)
        self.json.sendEnded(self.clients_sockets, self.running, self.game_ended)
        self.json.sendRunning(self.clients_sockets, self.running)
        clock = pygame.time.Clock()
        self.emptyBomb = False
        self.emptyExplosion = False

        while self.running:
            dt = clock.tick(15)          
            if not self.game_ended:
                self.game_ended = self.check_end_game()
                if self.game_ended:
                    self.json.sendPlayer1(self.clients_sockets, self.running, self.player[0])
                    self.json.sendPlayer2(self.clients_sockets, self.running, self.player[1])
                    self.json.sendEnded(self.clients_sockets, self.running, self.game_ended)
            self.update_bombs(dt)

        self.explosions.clear()
        self.ene_blocks.clear()
        self.power_ups.clear()

    def update_bombs(self, dt):
        if len(self.bombs) >0 :
            self.json.sendBombs(self.clients_sockets, self.running, self.bombs)
            self.emptyBomb = True
        else : 
            if self.emptyBomb:
                self.json.sendEmptyBomb(self.clients_sockets, self.running)
                self.emptyBomb = False

        if len(self.explosions) >0 :
            self.json.sendExplosions(self.clients_sockets, self.running, self.explosions)
            self.emptyExplosion = True
        else : 
            if self.emptyExplosion:
                self.json.sendEmptyExplosions(self.clients_sockets, self.running)
                self.emptyExplosion = False

        for b in self.bombs:
            b.update(dt)
            if b.time < 1:
                b.bomber.bomb_limit += 1
                self.grid[b.pos_x][b.pos_y] = 0
                exp_temp = Explosion(b.pos_x, b.pos_y, b.range)
                exp_temp.explode(self.grid, self.bombs, b, self.power_ups)
                exp_temp.clear_sectors(self.grid, random, self.power_ups)
                self.explosions.append(exp_temp)
        for pl in self.player:
            pl.check_death(self.explosions)
        for e in self.explosions:
            e.update(dt)
            self.json.sendGrid(self.clients_sockets, self.running, self.grid)
            self.json.sendPowerUps(self.clients_sockets, self.running, self.power_ups)
            if e.time < 1:
                self.explosions.remove(e)


    def check_end_game(self):
        end = False
        for pl in self.player:
            if not pl.life:
                end=True
        return end


if __name__ == "__main__":
    server= Game(59001)
    server.run()