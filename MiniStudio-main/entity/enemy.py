import pygame, math, random
from entity.entity import Entity
from entity.projectile import Projectile

class Enemy(Entity):

    def __init__(self, life: int, x: int, y: int, w: int, h: int, spritePath: str):
        super().__init__(True, x, y, w, h, spritePath=spritePath)
        self.life = life
    
    def takeDamage(self, damageNumber):
        self.life -= damageNumber

    def isDead(self):
        return self.life <= 0
    
    def update(self, dt):
        self.rect.x += self.speedVect[0] * self.speed
        self.rect.y += self.speedVect[1] * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class SuicidePigeon(Enemy):

    def __init__(self, life: int, x: int, y: int):
        super().__init__(life, x, y, 50, 50, spritePath="img/drone.png")
        self.scale = 7
        self.imgWidth = 32
        self.imgHeigh = 32
        self.sprite = pygame.transform.scale(pygame.image.load("img/drone.png"), (self.imgWidth*self.scale, self.imgHeigh*self.scale))
        self.speedVect = (-1, 0)
        self.speed = 20

    def update(self, dt):
        self.rect.x += self.speedVect[0] * self.speed
        self.rect.y += self.speedVect[1] * self.speed
    
    def draw(self, screen):
        self.rect.update(self.rect.x, self.rect.y, self.imgWidth*self.scale, self.imgHeigh*self.scale)
        screen.blit(self.sprite, dest=(self.rect.x, self.rect.y))

    def shoot(self):
        None

class StrafingDrone(Enemy):

    def __init__(self, life: int, x: int, y: int, projectile):
        super().__init__(life, x, y, 100, 100, spritePath="img/drone.png")
        self.scale = 7
        self.imgWidth = 32
        self.imgHeigh = 32
        self.sprite = pygame.transform.scale(pygame.image.load("img/drone.png"), (self.imgWidth*self.scale, self.imgHeigh*self.scale))
        self.speedVect = (-1, 0)
        self.threshold = False
        self.speed = 2
        self.angle = 0
        self.all_projectiles = projectile
        self.fireCooldown = pygame.time.get_ticks()

    def update(self, dt):
        self.rect.x += self.speedVect[0] * self.speed
        self.rect.y += self.speedVect[1] * self.speed
        # avance puis monte et descend
        if self.rect.x <= 1500 and not self.threshold:
            self.speedVect = (0, -1)
            self.threshold = True
        elif self.rect.y <= 50:
            self.speedVect = (0, 1)
        elif self.rect.y >= 900:
            self.speedVect = (0, -1)
        
    def draw(self, screen):
        self.rect.update(self.rect.x, self.rect.y, self.imgWidth*self.scale, self.imgHeigh*self.scale)
        screen.blit(self.sprite, dest=(self.rect.x, self.rect.y))
    
    def resetFireCooldown(self):
        self.fireCooldown = pygame.time.get_ticks()+10*150
    
    def shoot(self):
        # fonction de tir des ennemies
        if self.threshold and pygame.time.get_ticks() > self.fireCooldown:
            offSetX = self.rect.x - 60
            offSetY = self.rect.y
            vect = (-1, 0)
            self.resetFireCooldown()
            for projIndex in range(len(self.all_projectiles)):
                if not self.all_projectiles[projIndex]:
                    self.all_projectiles[projIndex] = Projectile("img/fusée_rouge-Sheet.png", False, offSetX, offSetY, 23, 7, vect, 3, False)
                    break


class DrunkPigeon(Enemy):
    def __init__(self, life, reverse=False):
        super().__init__(life, 1920, 250, 50, 50, spritePath="img/drone.png")
        self.scale = 7
        self.imgWidth = 32
        self.imgHeigh = 32
        self.sprite = pygame.transform.scale(pygame.image.load("img/drone.png"), (self.imgWidth*self.scale, self.imgHeigh*self.scale))
        self.speedVect = (-1, 0)
        self.reversed = reverse
        self.speed = 3

    def update(self, dt):
        # self.pathXAxis += self.speedVect[0] * self.speed
        self.rect.x += self.speedVect[0] * self.speed
        if self.reversed:
            self.rect.y = 275 + math.cos(self.rect.x/80) * 250
        else:
            self.rect.y = 275 + math.sin(self.rect.x/80) * 250

    def draw(self, screen):
        self.rect.update(self.rect.x, self.rect.y, self.imgWidth*self.scale, self.imgHeigh*self.scale)
        screen.blit(self.sprite, dest=(self.rect.x, self.rect.y))
    
    def shoot(self):
        None

class Scientist(Enemy):
    def __init__(self, life: int, projectile):
        super().__init__(life, 1920, 860, 80, 80, spritePath="img/scient-cat-Sheet.png")
        self.speedVect = (-1, 0)
        self.speed = 7
        self.all_projectiles = projectile
        self.fireCooldown = pygame.time.get_ticks()
        # Création de variables pour animation
        self.scale = 7
        spritesWidth, spritesHeigh = 80, 48
        self.imgWidth = self.imgHeigh = 16
        liste = [16, 32]
        couleur = random.choice(liste)
        self.spriteY = couleur
        self.spriteSheet = pygame.transform.scale(pygame.image.load("img/scient-cat-Sheet.png").convert_alpha(), (spritesWidth * self.scale, spritesHeigh * self.scale))
        self.frame = 0
        self.actualFrame = pygame.Rect(self.frame * self.imgWidth * self.scale, self.spriteY * self.scale, self.imgWidth * self.scale, self.imgHeigh * self.scale)
        self.timeNextFrame = 150

    def update(self, dt):
        self.rect.x += self.speedVect[0] * self.speed
        self.rect.y += self.speedVect[1] * self.speed
        # Algo animation
        self.timeNextFrame -= dt
        if self.timeNextFrame < 0:
            self.timeNextFrame += 150
            self.frame = (self.frame + 1) % (4)
            self.actualFrame = pygame.Rect(self.frame * self.imgWidth * self.scale, self.spriteY * self.scale, self.imgWidth * self.scale, self.imgHeigh * self.scale)

    def draw(self, screen):
        self.rect.update(self.rect.x, self.rect.y, self.imgWidth*self.scale, self.imgHeigh*self.scale)
        screen.blit(self.spriteSheet, dest=(self.rect.x, self.rect.y), area=self.actualFrame)

    def resetFireCooldown(self):
            self.fireCooldown = pygame.time.get_ticks()+10*150

    def shoot(self):
        # fonction de tir des ennemies
        if pygame.time.get_ticks() > self.fireCooldown:
            offSetX = self.rect.x - 60
            offSetY = self.rect.y
            vect = (-1, -1)
            self.resetFireCooldown()
            for projIndex in range(len(self.all_projectiles)):
                if not self.all_projectiles[projIndex]:
                    self.all_projectiles[projIndex] = Projectile("img/fusée_jaune-Sheet-export.png", False, offSetX, offSetY, 24, 7, vect, 3, False)
                    break

class Boss(Enemy):

    def __init__(self, level, projectile):
        path = 'img/boss' + str(level) + '.png'
        super().__init__(level*1000, 1150, 50, 128, 128, path)
        self.maxLife = self.life
        self.level = level
        self.Cooldown = 3000
        self.timeStart = pygame.time.get_ticks()
        self.all_projectiles = projectile
        self.shootCount = 1
        # Création de variables pour animation
        self.scale = 7
        self.spriteY, self.spriteX = 4, 7
        spritesWidth, spritesHeigh = 768, 128
        self.imgWidth, self.imgHeigh = 128, 128
        self.spriteSheet = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (spritesWidth * self.scale, spritesHeigh * self.scale))
        self.frame = 0
        self.actualFrame = pygame.Rect(self.spriteX + self.frame * self.imgWidth * self.scale, 0, self.imgWidth * self.scale, self.imgHeigh * self.scale)
        self.timeNextFrame = 150
        
    def update(self, dt):
        # Algo animation
        self.timeNextFrame -= dt
        if self.timeNextFrame < 0:
            self.timeNextFrame += 150
            self.frame = (self.frame + 1) % (5)
            self.actualFrame = pygame.Rect(self.spriteX + self.frame * self.imgWidth * self.scale, 0, self.imgWidth * self.scale, self.imgHeigh * self.scale)
        # Définition des phases
        if self.life < self.maxLife//2:
                self.shootCount = 2
                self.Cooldown = 2000
        if self.life < self.maxLife//3:
                self.shootCount = 3
                self.Cooldown = 1500
        if self.life < self.maxLife//6:
                self.shootCount = 4
                self.Cooldown = 1000
    
    def draw(self, screen):
        self.rect.update(self.rect.x, self.rect.y, self.imgWidth*self.scale, self.imgHeigh*self.scale)
        screen.blit(self.spriteSheet, dest=(self.rect.x, self.rect.y), area=self.actualFrame)

    def canShot(self):
        if pygame.time.get_ticks() - self.timeStart > self.Cooldown:
            return True
        return False

    def shoot(self):
        if self.canShot():
            self.timeStart = pygame.time.get_ticks()
            for i in range(self.shootCount):
                offSetX = self.rect.x - 60
                offSetY = self.rect.y
                vect = (-1, random.random() - 0.5)
                for projIndex in range(len(self.all_projectiles)):
                    if not self.all_projectiles[projIndex]:
                        self.all_projectiles[projIndex] = Projectile("img/egges-in-fire.png", False, offSetX, offSetY + 468, 39, 16, vect, 2, False)
                        break