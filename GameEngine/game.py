from Actors.Player import *
from Scene.Camera import *
from GameEngine.GameHUD import *
from Party import *
from Actors.Enemies import *


class Game:

    def __init__(self, event_mgr, game_window):
        self.window = game_window
        self.manager = event_mgr
        self.running = False
        self.dungeon = Dungeon(4)
        #self.player = Player(self.dungeon.playerSpawn, "images/character1")
        self.party_list = Party(self.dungeon.playerSpawn,
                                ["images/Characters/character1"])
        self.player = self.party_list.active_member
        self.player.rect.bottom = self.dungeon.playerSpawn.bottom
        self.camera = Camera(self.dungeon)
        self.camera.setCameraPosition(self.player.rect.center)
        self.manager.addGameObject(self.player)
        self.manager.addParty(self.party_list)
        self.HUD = GameHUD(self.window)
        self.manager.addGameObject(self.HUD)
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.color.THECOLORS["black"]
        for room in self.dungeon.rooms:
            for wall in room.walls.sprites():
                self.manager.addGameObject(wall)
        self.enemiesByRoom = []
        for room in self.dungeon.rooms:
            enemy_list = []
            for enemyspawnpoint in room.enemySpawnPoints:
                enemy = Enemy(enemyspawnpoint.midbottom, "images/Characters/enemy1")
                enemy_list.append(enemy)
                self.manager.addGameObject(enemy)
            room.enemies = enemy_list
            self.enemiesByRoom.append(enemy_list)
        self.gameOverScreen = pygame.Surface(SCREEN_RES)
        self.font = pygame.font.Font('./fonts/LuckiestGuy-Regular.ttf',100)
        self.gameOverCondition = None
        self.fontSurface = None
        self.font_color = pygame.color.THECOLORS['red']
        self.postTime = 3


    def start_game(self):
        self.running = True

    def launch_game(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.gameOverCondition and self.postTime > 0:
                self.postTime -= dt
                fontSurface = self.font.render(self.gameOverCondition,False,self.font_color)
                fontrect = fontSurface.get_rect()
                fontrect.center = (SCREEN_RES[0]>>1,SCREEN_RES[1]>>1)
                self.window.fill(pygame.color.THECOLORS['black'])
                self.window.blit(fontSurface,fontrect)
                self.manager.poll_input(dt)
            else:
                if self.postTime <= 0:
                    self.gameOver()
                    break

                self.running = self.manager.process_input(dt)
                self.running = self.manager.poll_input(dt)
                self.player_swap_cd(dt)
                cur_pos = self.player.rect
                self.manager.removeGameObject(self.player)
                self.player = self.party_list.active_member
                self.manager.addGameObject(self.player)
                self.player.set_pos(cur_pos)

                # events = pygame.event.get()
                # for event in events:
                #     if event.type == pygame.QUIT:
                #         self.running = False

                self.collisionHandling(dt)

                #Win Condition
                if self.player.pos.x >= self.dungeon.dungeonExit.left:
                    self.gameWin()

                #Lose Conditions
                if self.outOfBounds(self.player.rect.center) or self.allPlayersDead():
                    self.gameOverCondition = "You Died!"

                if self.HUD.getTime() <=0:
                    self.gameOverCondition = "Times Up!"

                self.camera.setCameraPosition(self.player.rect.center)
                pygame.draw.rect(self.window, (255, 255, 255), self.player.rect, 2)
                self.window.fill(self.bg_color)
                self.camera.draw(self.window, self.player, self.enemiesByRoom)
                self.HUD.draw(self.window, self.party_list)
            pygame.display.flip()

    def player_swap_cd(self, dt):
        """ 3 second cooldown on switching
            active party member."""
        self.party_list.last_active += dt
        #print(self.party_list.last_active)

    def allPlayersDead(self):
        for player in self.party_list.party_members:
            if player.stats['CUR_HP'] > 0:
                return False
        return True

    def outOfBounds(self,playerPos):
        for room in self.camera.dungeon.rooms:
            bounds = room.bgImageRect
            if bounds.collidepoint(playerPos):
                return False
        return True

    def collisionHandling(self,dt):
        """ Move Player and Check for Collisions"""

        hasCollided = False
        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                hasCollided = True
                objective = room.determineObj()
                self.HUD.getRoomObj(objective)
                break

        if not hasCollided:
            self.gameOver()

        currentRoomIndex = None
        roomWidth = self.dungeon.rooms[0].bgImageRect.w
        tiles = pygame.sprite.Group()
        for i in range(len(self.dungeon.rooms)):
            if self.player.rect.colliderect(self.dungeon.rooms[i].bgImageRect):
                tiles.add(self.dungeon.rooms[i].walls.sprites())

        self.collisionCheck(tiles,dt)

    def collisionCheck(self,tiles,dt):

        self.player.moveX(dt)
        collisions = pygame.sprite.spritecollide(self.player, tiles, False)
        if collisions:
            hit = collisions[0]
            self.player.handleXCollision(hit.rect)

        self.player.moveY(dt)
        collisions = pygame.sprite.spritecollide(self.player, tiles, False)

        vertCollisions = False
        if collisions:
            hit = collisions[0]
            vertCollisions = self.player.handleYCollision(hit.rect)

        rect = self.player.rect.copy()

        if not vertCollisions:
            for i in range(PIXEL_DIFFERENCE):
                rect.move_ip(0,1)
                for wall in tiles.sprites():
                    if rect.colliderect(wall.rect) and self.player.velocity.y >= 0:
                        self.player.handleYCollision(wall.rect)
                        vertCollisions = True
                        break
                if vertCollisions:
                    break

        if not vertCollisions:
            self.player.isInAir()

        self.player.determineState()

        for room in self.dungeon.rooms:
            if self.player.rect.colliderect(room.bgImageRect):
                for enemy in room.enemies:
                    if(not self.manager.hasReferenceToGameObject(enemy)):
                        self.manager.addGameObject(enemy)
                    enemy.moveX(dt)
                    collisions = pygame.sprite.spritecollide(enemy, tiles, False)
                    if collisions:
                        hit = collisions[0]
                        enemy.handleXCollision(hit.rect)

                    enemy.moveY(dt)
                    collisions = pygame.sprite.spritecollide(enemy, tiles, False)

                    vertCollisions = False
                    if collisions:
                        hit = collisions[0]
                        vertCollisions = enemy.handleYCollision(hit.rect)

                    rect = enemy.rect.copy()

                    if not vertCollisions:
                        for i in range(PIXEL_DIFFERENCE):
                            rect.move_ip(0, 1)
                            for wall in tiles.sprites():
                                if rect.colliderect(wall.rect) and enemy.velocity.y >= 0:
                                    enemy.handleYCollision(wall.rect)
                                    vertCollisions = True
                                    break
                            if vertCollisions:
                                break

                    if not vertCollisions:
                        enemy.isInAir()

                    rect = enemy.rect.clamp(room.bgImageRect)
                    enemy.set_pos(rect)

                    enemy.determineState()
            else:
                for enemy in room.enemies:
                    if self.manager.hasReferenceToGameObject(enemy):
                        self.manager.removeGameObject(enemy)

    def gameWin(self):
        "Award Experience and level up"
        self.running = False

    def gameOver(self):
        "The Player's Experience gets reset"
        self.running = False