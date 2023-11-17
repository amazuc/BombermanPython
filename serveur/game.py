import threading
import pygame
import random
from sendjson import Json
from grid import Grid
from player import Player
from explosion import Explosion

class Game():

    def __init__(self, nbJoueur, clients_sockets):
        self.nbJoueur = nbJoueur
        self.clients_sockets = clients_sockets
        self.json = Json(self.nbJoueur)
        self.grid = Grid.getGrid()
        self.game_ended = False
        self.bombs = []
        self.explosions = []
        self.power_ups = []
        self.ene_blocks = []
        self.bombs.clear()
        self.explosions.clear()
        self.power_ups.clear()
        self.emptyBomb = False
        self.emptyExplosion = False
        if self.nbJoueur == 2 :
            self.player = [Player(4,4),Player(44,44)]
        if(self.nbJoueur == 3):
            self.player = [Player(4,4),Player(44,44),Player(4,44)]
            self.ene_blocks.append(self.player[2])
        if(self.nbJoueur == 4):
            self.player = [Player(4,4),Player(44,44),Player(4,44),Player(44,4)]
            self.ene_blocks.append(self.player[2])
            self.ene_blocks.append(self.player[3])
        self.ene_blocks.append(self.player[0])
        self.ene_blocks.append(self.player[1])
        self.running = True
        self.game_thread = threading.Thread(target=self.main, args=())
        self.game_thread.start()

    def main(self):
        self.grid = [row[:] for row in self.grid]
        self.generate_map()
        for i, pl in enumerate(self.player):
            self.json.sendPlayer(self.clients_sockets, self.running, pl, str(i+1))
        self.json.sendGrid(self.clients_sockets, self.running, self.grid)
        self.json.sendEnded(self.clients_sockets, self.running, self.game_ended)
        self.json.sendRunning(self.clients_sockets, self.running)
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(15)          
            if not self.game_ended:
                self.game_ended = self.check_end_game()
                if self.game_ended:
                    for i, pl in enumerate(self.player):
                        self.json.sendPlayer(self.clients_sockets, self.running, pl, str(i+1))
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
                    for i, pl in enumerate(self.player):
                        self.json.sendPlayer(self.clients_sockets, self.running, pl, str(i+1))
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

    def check_end_game(self):
        i = 0
        for pl in self.player:
            if pl.life:
                i = i + 1
        return i < 2