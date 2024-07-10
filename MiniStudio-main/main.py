import pygame
from random import randint
from game.level.level import Level
from entity.player import Player
from entity.entity import Entity, Button, Egg
from entity.enemy import SuicidePigeon, StrafingDrone, DrunkPigeon, Boss
from game.gameLogic.movement import move
from settings import Setting

class Game:
    
    def __init__(self):
        # Initialise Pygame
        pygame.init()
        self.state = "menu"

        # Définir la taille de la fenêtre
        self.screenSize = (1920, 1080)
        self.screen = pygame.display.set_mode(self.screenSize)
        self.screenEntity = Entity(False, 0, 0, self.screenSize[0], self.screenSize[1])

        #Définis une clock pour limiter les actions
        self.clock = pygame.time.Clock()

        # Définir le titre de la fenêtre
        pygame.display.set_caption("Feathers of Freedom")

        # initialisation des variables de cooldown
        self.enemySpawnCooldown = 0
        self.actionCooldown = 0
        # initialisation des paramettres
        self.settings = Setting()
        self.startButton = None
        self.level = None
        self.controleArrowsToggle = False
        self.controleQWERTYToggle = False

        # chargement et réduction de l'image de background pour un affichage moins gourmand
        self.background = pygame.Surface(self.screenSize).convert_alpha()
        self.background.blit(pygame.image.load("img/bg1.png"),(0,0), (0,0,self.screenSize[0],self.screenSize[1]))

        # chargement et réduction de l'image de coeur pour un affichage moins gourmand
        self.ui_sheet = pygame.transform.scale(pygame.image.load("img/ui_sheet.png"), (256*7.5, 128*7.5))

        self.backgroundGacha = pygame.Surface(self.screenSize).convert_alpha()
        self.backgroundGacha.blit(pygame.image.load("img/bg_gacha.png"), (0,0), (0,0,self.screenSize[0],self.screenSize[1]))
        
        
        self.controleSpriteSheet = pygame.transform.scale(pygame.image.load("img/mapping-options_sheet.png"), (112*7, 64*7))

        #initialisation des boutons
        # bouton de pause
        self.PauseButton = Button(self.screenSize[0]/2 + 725, self.screenSize[1]/2 - 509 + 65, "pause")
        self.pauseHomeButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 260 , "menu")
        self.pauseReplayButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 80 , "replay")


        # bouton de mort
        self.backButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 260 , "menu")
        self.gachaButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 80 , "gacha")
        self.replayButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 - 100, "replay")
        self.game_overButton = Button(self.screenSize[0]/2 - 460 + 100, self.screenSize[1]/2 - 300, "game_over")

        # bouton menu principal
        self.winButton = Button(self.screenSize[0]/2 - 375 , self.screenSize[1]/2 - 300, "win")
        self.startButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 - 100, "start")
        self.optionButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 80, "option")
        self.quitButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 260, "quit")
        self.openButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 180, "open")
        self.back1Button = Button(self.screenSize[0] - 680 + 100, self.screenSize[1]/2 + 400 , "menu")
        self.oeufOpening = Egg(self.screenSize[0]/2 - 550 + 100, self.screenSize[1]/2 - 450, "oeuf")

        # bouton menu option
        self.optionQuitButton = Button(self.screenSize[0]/2 - 365 + 100, self.screenSize[1]/2 + 260, "menu")

        # grace
        self.grace = False
        self.graceCooldown = 0
        self.graceTime = 1500
        
        # Boucle principale
        self.game = True
        while self.game:
            self.timeStart = pygame.time.get_ticks()
            self.frames = self.timeStart//16
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
            self.update()
            self.draw()
        
        # Quitter Pygame
        self.settings.saveSettings()
        pygame.quit()
    
    def draw(self):
        self.screen.fill("aliceblue")
        if self.state == "game":
            self.drawLevel()
        elif self.state == "menu":
            self.drawMenu()
        elif self.state == "option":
            self.drawOption()
        elif self.state == "end":
            self.drawEnd()
        elif self.state == "gacha":
            self.drawReward()
        elif self.state == "oeuf":
            self.drawEgg()
        elif self.state == "win":
            self.drawWin()
        # Mise à jour de l'affichage
        pygame.display.flip()
    
    def update(self):
        self.dt = self.clock.tick(60)
        if self.state == "game":
            self.updateLevel()
        elif self.state == "menu":
            self.updateMenu()
        elif self.state == "option":
            self.updateOption()
        elif self.state == "end" :
            self.updateEnd()
        elif self.state == "gacha":
            self.updateReward()
        elif self.state == "oeuf":
            self.updateEgg()
        elif self.state == "win":
            self.updateWin()

        # timer
        timeEnd = pygame.time.get_ticks()
        if self.timeStart + 7 > timeEnd:
            pygame.time.delay(timeEnd - self.timeStart + 7)
                
    def updateMenu(self):
        
        if self.startButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.initLevel()
            self.state = "game"
            self.level = Level(1)
            self.gameTimeStart = pygame.time.get_ticks()
        elif self.optionButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "option"
        elif self.quitButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.game = False
    
    def drawMenu(self):
        self.screen.blit(self.background, (0,0,0,0))
        self.startButton.draw(self.screen)
        self.optionButton.draw(self.screen)
        self.quitButton.draw(self.screen)
        title = pygame.transform.scale(pygame.image.load("img/game-title.png"), (256*7, 64*7))
        titleW, titleH = 256*7, 64*7
        self.screen.blit(title, (self.screenSize[0]/2 - titleW/2, 0, 0, 0))
       
    def updateEnd(self):
        
        if self.backButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "menu"
        elif self.gachaButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "gacha"
        elif self.replayButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.initLevel()
            self.state = "game"
            self.level = Level(1)
            self.gameTimeStart = pygame.time.get_ticks()

    def drawEnd(self):
        self.drawLevel()
        self.game_overButton.draw(self.screen)
        self.replayButton.draw(self.screen)
        self.gachaButton.draw(self.screen)
        self.backButton.draw(self.screen)

    def updateWin(self):
        if self.backButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "menu"
        elif self.gachaButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "gacha"
        elif self.replayButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.initLevel()
            self.state = "game"
            self.level = Level(1)
            self.gameTimeStart = pygame.time.get_ticks()
        
    def rect_overlap(self, x1, x2, y1, y2, w1, w2, h1, h2):
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2
    
    def drawWin(self):
        self.drawLevel()
        self.winButton.draw(self.screen)
        self.replayButton.draw(self.screen)
        self.gachaButton.draw(self.screen)
        self.backButton.draw(self.screen)
    
    def updateReward(self):
        self.oeufOpening.update(self.dt)
        if self.oeufOpening.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "oeuf"
        if self.openButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "open"
        if self.back1Button.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.state = "menu"
    
    def drawReward(self):
        image = pygame.transform.scale(pygame.image.load("img/bg_gacha.png"),(self.screenSize[0]*1,self.screenSize[1]*1))
        self.screen.blit(image, (0,0))
        self.oeufOpening.draw(self.screen)
        self.openButton.draw(self.screen)
        self.back1Button.draw(self.screen)
    
    def updateEgg(self):
        # Création de variables pour animation
        Egg.timeNextFrame -= self.dt
        if Egg.timeNextFrame < 0:
            Egg.timeNextFrame += 150
            if Egg.frame >= 9:
                Egg.frame = 0
            else:
                Egg.frame = (Egg.frame + 1) % 8
        Egg.actualFrame = pygame.Rect(Egg.frame * Egg.w * Egg.scale, 0, Egg.w * Egg.scale, Egg.h * Egg.scale)
    
    def drawEgg(self):
        Egg.update(self.dt)
        Egg.rect.update(Egg.rect.x, Egg.rect.y, 160*Egg.scale, 160*Egg.scale)
        Egg.draw(self.screen)
    
    def updateOption(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            self.state = "menu"
        if self.optionQuitButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.5
            if self.controleArrowsToggle:
                self.settings.changeBinds({'up': 1073741906,'down': 1073741905,'left':1073741904,'right': 1073741903}) #pour les fleches
            else:
                if not self.controleQWERTYToggle:
                    self.settings.changeBinds({'up': 122,'down': 115,'left':113,'right': 100}) #pour azerty
                else:
                    self.settings.changeBinds({'up': 119,'down': 115,'left':97,'right': 100}) #pour qwerty
            self.state = "menu"

        if self.rect_overlap(mouseX, self.screenSize[0]-600, mouseY, 300, 1, 41*7, 1, 24*7) and pygame.mouse.get_pressed()[0] and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.controleArrowsToggle = not self.controleArrowsToggle

        if self.rect_overlap(mouseX, 300, mouseY, 300, 1, 41*7, 1, 24*7) and pygame.mouse.get_pressed()[0] and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.controleQWERTYToggle = not self.controleQWERTYToggle


    def drawOption(self):
        self.screen.blit(self.background, (0,0,0,0))
        self.optionQuitButton.draw(self.screen)
        if not self.controleQWERTYToggle:
            self.screen.blit(self.controleSpriteSheet, (300,300,0,0), (4*7, 5*7, 41*7, 24*7))
        else:
            self.screen.blit(self.controleSpriteSheet, (300,300,0,0), (4*7, 37*7, 41*7, 24*7))
        if not self.controleArrowsToggle:
            self.screen.blit(self.controleSpriteSheet, (self.screenSize[0]-600,300,0,0), (67*7, 5*7, 41*7, 24*7))
        else:
            self.screen.blit(self.controleSpriteSheet, (self.screenSize[0]-600,300,0,0), (67*7, 37*7, 41*7, 24*7))

    def initLevel(self):
        # intialisation de la variable en la remplissant de None
        self.level = Level(1)
        self.projectiles = [None for i in range(100)]
        self.enemies = [None for i in range(100)]
        self.obstacle = [None for i in range(100)]
        self.player = Player(self.screenSize[0]/3-56, self.screenSize[1]/2-56, 16, 16, self.projectiles, 50, True)
        self.gamePause = False
        self.gameTimeStart = pygame.time.get_ticks()

    def drawLife(self):
        self.screen.blit(self.ui_sheet, (90, 85, 0, 0), (16*7.5,16*7.5,68*7.5,13*7.5))
        health = self.player.life
        incr = 0

        while health > 0:
            incr += 90
            x = incr - 35 +50
            y = 100
            self.screen.blit(self.ui_sheet, (x,y,0,0), (98*7.5, 18*7.5, 11*7.5, 9*7.5))
            health -= 10

    def updateLevel(self):

        if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.gamePause = not self.gamePause
        
        if self.PauseButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
            self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
            self.gamePause = not self.gamePause

        if not self.gamePause:
            # déplacement du joueur si il est vivant
            if not self.player.isDead():
                
                move(self.settings, self.screen, self.player,self)
            else:
                self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 1
                self.state = "end"
                self.updateEnd()
                self.drawEnd()
            self.level.update()
            self.player.update(self.dt)
            
            # ajout d'ennemis
            onGarde = -1
            leStock = None
            self.level.ennemiesSpawn(pygame.time.get_ticks() - self.gameTimeStart, self)
            for i in range(len(self.enemies)):
                if type(self.enemies[i]) == Boss:
                    onGarde = i
            if onGarde != -1:
                leStock = self.enemies[onGarde]
                self.enemies[onGarde] = self.enemies[-1]
                self.enemies[-1] = leStock

            # ajout d'obstacle
            #self.level.obstaclesSpawn(pygame.time.get_ticks() - self.gameTimeStart, self)

            if pygame.time.get_ticks() - self.graceCooldown >= self.graceTime:
                self.grace = False
            print(self.grace)
            # update de la position des projectiles
            for i in range(len(self.projectiles)):
                if self.projectiles[i]:
                    self.projectiles[i].update(self.dt)
                    # si la balle touche un ennemi
                    if self.projectiles[i].friendly:
                        for j in range(len(self.enemies)):
                            if self.enemies[j] and self.projectiles[i] and self.enemies[j].rectOverlap(self.projectiles[i]):
                                self.enemies[j].takeDamage(10)
                                # suppression lorsqu'ils entrent en colision avec un ennemi
                                self.projectiles[i] = None
                    elif self.player.rectOverlap(self.projectiles[i]) and not self.grace:
                        self.player.takeDamage(10)
                        self.projectiles[i] = None
                        self.grace = True
                        self.graceCooldown = pygame.time.get_ticks()
                    else:
                        if self.projectiles[i] and self.player.rectOverlap(self.projectiles[i]) and not self.grace:
                                self.player.takeDamage(10)
                                self.projectiles[i] = None
                                self.grace = True
                                self.graceCooldown = pygame.time.get_ticks()

                    # si la balle sors de l'écran
                    if self.projectiles[i] and not self.projectiles[i].rectOverlap(self.screenEntity):
                        self.projectiles[i] = None
                        pass
                    
            # update de la position des ennemis et suppression de ces dernier
            for i in range(len(self.enemies)):
                if self.enemies[i]:
                    self.enemies[i].update(self.dt)
                    self.enemies[i].shoot()
                    if self.enemies[i].rectOverlap(self.player) and not self.grace:
                        self.enemies[i].takeDamage(10)
                        self.player.takeDamage(10)
                        self.grace = True
                        self.graceCooldown = pygame.time.get_ticks()
                    if self.enemies[i].isDead() or not self.enemies[i].rectOverlap(self.screenEntity):
                        if type(self.enemies[i]) == Boss:
                            self.state = 'win'
                        self.enemies[i] = None
        else:
            if self.pauseHomeButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
                self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
                self.state = "menu"
            if self.pauseReplayButton.isPressed() and self.actionCooldown < pygame.time.get_ticks():
                self.actionCooldown = pygame.time.get_ticks() + 16 * 60 * 0.2
                self.gamePause = not self.gamePause
                self.initLevel()
    
    def drawLevel(self):

        # Affichage du jeu
        self.level.draw(self.screen)

        # Affichage du joueur
        if self.player:
            self.player.draw(self.screen)

        # Affichage des projectiles
        for i in self.projectiles:
            if i:
                i.draw(self.screen)
        
        # Affichage des ennemis
        for en in self.enemies:
            if en:
                en.draw(self.screen)

        self.PauseButton.draw(self.screen)
        self.drawLife()

        if self.gamePause:
            self.pauseHomeButton.draw(self.screen)
            self.pauseReplayButton.draw(self.screen)

Game()