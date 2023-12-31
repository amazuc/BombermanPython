import json
from time import sleep
import pygame
import sys
from client import Client
from grid import Grid
from bomb import Bomb
from enums.power_up_type import PowerUpType
from player import Player
from explosion import Explosion
from power_up import PowerUp

class GameVs():

    def game_init(self, surface, scale, username, ip, port, nbJoueur):
        self.nbJoueur = int(nbJoueur)
        self.ene_blocks = []
        self.running = True
        self.bombs = []
        self.explosions = []
        self.power_ups = []
        self.autrejoueur = False
        self.game_ended = False
        self.client = None
        self.BACKGROUND_COLOR = (107, 142, 35)
        self.grid = Grid.getGrid()
        self.client = ClientSocket(username, ip, port, nbJoueur, self.callBackData)
        self.client.listen()
        self.font = pygame.font.SysFont('Bebas', scale)
        self.bombs.clear()
        self.explosions.clear()
        self.power_ups.clear()
        self.player_type_mapping = {"player1": 0,"player2": 1,"player3": 2,"player4": 3}
        self.player = [Player() for _ in range(self.nbJoueur)]
        for player in self.player:
            player.load_animations(scale)
        
        grass_img = pygame.image.load('images/terrain/grass.png')
        grass_img = pygame.transform.scale(grass_img, (scale, scale))
        block_img = pygame.image.load('images/terrain/block.png')
        block_img = pygame.transform.scale(block_img, (scale, scale))
        box_img = pygame.image.load('images/terrain/box.png')
        box_img = pygame.transform.scale(box_img, (scale, scale))
        bomb1_img = pygame.image.load('images/bomb/1.png')
        bomb1_img = pygame.transform.scale(bomb1_img, (scale, scale))
        bomb2_img = pygame.image.load('images/bomb/2.png')
        bomb2_img = pygame.transform.scale(bomb2_img, (scale, scale))
        bomb3_img = pygame.image.load('images/bomb/3.png')
        bomb3_img = pygame.transform.scale(bomb3_img, (scale, scale))
        explosion1_img = pygame.image.load('images/explosion/1.png')
        explosion1_img = pygame.transform.scale(explosion1_img, (scale, scale))
        explosion2_img = pygame.image.load('images/explosion/2.png')
        explosion2_img = pygame.transform.scale(explosion2_img, (scale, scale))
        explosion3_img = pygame.image.load('images/explosion/3.png')
        explosion3_img = pygame.transform.scale(explosion3_img, (scale, scale))
        terrain_images = [grass_img, block_img, box_img, grass_img]
        bomb_images = [bomb1_img, bomb2_img, bomb3_img]
        explosion_images = [explosion1_img, explosion2_img, explosion3_img]
        power_up_bomb_img = pygame.image.load('images/power_up/bomb.png')
        power_up_bomb_img = pygame.transform.scale(power_up_bomb_img, (scale, scale))
        power_up_fire_img = pygame.image.load('images/power_up/fire.png')
        power_up_fire_img = pygame.transform.scale(power_up_fire_img, (scale, scale))
        power_ups_images = [power_up_bomb_img, power_up_fire_img]

        self.main(surface, scale, terrain_images, bomb_images, explosion_images, power_ups_images)


    def draw(self, s, grid, tile_size, terrain_images, bomb_images, explosion_images, power_ups_images):
        s.fill(self.BACKGROUND_COLOR)   
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                s.blit(terrain_images[grid[i][j]], (i * tile_size, j * tile_size, tile_size, tile_size))
        for pu in self.power_ups:
            s.blit(power_ups_images[pu.type.value], (pu.pos_x * tile_size, pu.pos_y * tile_size, tile_size, tile_size))
        for x in self.bombs:
            s.blit(bomb_images[x.frame], (x.pos_x * tile_size, x.pos_y * tile_size, tile_size, tile_size))
        for y in self.explosions:
            for x in y.sectors:
                s.blit(explosion_images[y.frame], (x[0] * tile_size, x[1] * tile_size, tile_size, tile_size))
        for pl in self.player:
            if pl.life:
                s.blit(pl.animation[pl.direction][pl.frame],
                (pl.pos_x * (tile_size / 4), pl.pos_y * (tile_size / 4), tile_size, tile_size))
        
        if self.game_ended:
            fin = ""
            for i, player in enumerate(self.player, start=1):
                if i <= self.nbJoueur and player.life:
                    fin = f"Joueur {i}"
            tf = self.font.render(fin + " a gagné la partie !", False, (255, 255, 255))
            s.blit(tf, (65, 120))
            tf = self.font.render("Press ESC to go back to menu !", False, (255, 255, 255))
            s.blit(tf, (50, 200))

        if not self.autrejoueur:
            tf = self.font.render("En attente d'autres joueurs !", False, (255, 255, 255))
            s.blit(tf, (50, 95))

        pygame.display.update()


    def main(self, s, tile_size, terrain_images, bomb_images, explosion_images, power_ups_images):
        while self.running:
            self.draw(s, self.grid, tile_size, terrain_images, bomb_images, explosion_images, power_ups_images)
            if(self.autrejoueur):                    
                #recupère et envoi la direction du joueur
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    self.client.send('DOWN')
                elif keys[pygame.K_RIGHT]:
                    self.client.send('RIGHT')
                elif keys[pygame.K_UP]:
                    self.client.send('UP')
                elif keys[pygame.K_LEFT]:
                    self.client.send('LEFT')
                sleep(0.1)
                #recupère et envoi l'action du joueur'
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit(0)
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE:
                            self.client.send('SPACE')
                        elif e.key == pygame.K_ESCAPE:
                            self.client.send('ESCAPE')
                            self.client.tidy_up()
                            self.running = False

            
    def callBackData(self, datas):
        if datas is not None :
            self.autrejoueur = True
        clear = False
        for data in datas:
            if data.get("type") == "player1" or data.get("type") == "player2" or data.get("type") == "player3" or data.get("type") == "player4":
                player_index = self.player_type_mapping.get(data.get("type"))
                self.player[player_index].setX(int(json.loads(data["data"])["pos_x"]))
                self.player[player_index].setY(int(json.loads(data["data"])["pos_y"]))
                self.player[player_index].setDir(json.loads(data["data"])["direction"])
                self.player[player_index].setFrame(json.loads(data["data"])["frame"])
                self.player[player_index].setLife(bool(json.loads(data["data"])["life"]))

            if data.get("type") == "bomb":
                if not clear :
                    clear = True
                    self.bombs.clear()
                self.bombs.append(Bomb(json.loads(data["data"])["range"],json.loads(data["data"])["pos_x"],json.loads(data["data"])["pos_y"]))
                self.bombs[len(self.bombs)-1].setTime(int(json.loads(data["data"])["time"]))
            
            if data.get("type") == "explosion":
                if not clear :
                    clear = True
                    self.explosions.clear()
                self.explosions.append(Explosion(json.loads(data["data"])["sourceX"],json.loads(data["data"])["sourceY"],json.loads(data["data"])["range"], json.loads(data["data"])["time"],json.loads(data["data"])["frame"],json.loads(data["data"])["sectors"]))              
                    
            if data.get("type") == "power_up":
                if not clear :
                    clear = True
                    self.power_ups.clear()
                if json.loads(data["data"])["type"] == 0 :
                    self.power_ups.append(PowerUp(json.loads(data["data"])["pos_x"],json.loads(data["data"])["pos_y"],PowerUpType.BOMB))
                else :
                    self.power_ups.append(PowerUp(json.loads(data["data"])["pos_x"],json.loads(data["data"])["pos_y"],PowerUpType.FIRE))
            
            if data.get("type") == "grid":
                received_data = data.get("data", {})
                if "grid" in received_data and isinstance(received_data["grid"], str):
                    try:
                        parsed_grid = json.loads(received_data["grid"])
                        if isinstance(parsed_grid, list) and all(isinstance(row, list) for row in parsed_grid):
                            self.grid = parsed_grid
                        else:
                            print("Erreur dans le format de la grille reçue.")
                    except json.JSONDecodeError:
                        print("Erreur de décodage JSON pour la grille.")
                else:
                    print("La clé 'grid' est absente ou n'est pas une chaîne JSON.")
                    
            if data.get("type") == "running":
                self.running = bool(json.loads(data["data"])["running"])

            if data.get("type") == "game_ended":
                self.game_ended = bool(json.loads(data["data"])["game_ended"])

            if data.get("type") == "emptybomb":
                self.bombs.clear()

            if data.get("type") == "emptyexplosion":
                self.explosions.clear()

            if data.get("type") == "emptypower":
                self.power_ups.clear()

class ClientSocket(Client):
    def __init__(self, username ,server, port, nbJoueur, callback):
        super(ClientSocket,self).__init__(username, server, port, nbJoueur)
        self.callback = callback

    def handle_msg(self,data):
        self.callback(data)