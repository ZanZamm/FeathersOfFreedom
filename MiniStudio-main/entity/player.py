import pygame, math
from entity.entity import Entity
from entity.projectile import Projectile

class Player(Entity):

    def __init__(self, x: int, y: int, w: int, h: int, projectile, life: int, destruct: bool):
        super().__init__(destruct, x, y, w, h, spritePath="img/sprite_bird.png")
        self.life = life
        self.speed = 6
        self.angle = 0
        self.damage = False
        self.all_projectiles = projectile
        self.fireCooldown = pygame.time.get_ticks()
        self.abilityCooldown = pygame.time.get_ticks()
        # Création de variables pour animation
        self.scale = 7
        self.charaWidth, self.charaHeigh = w, h
        self.spriteSheet = pygame.transform.scale(pygame.image.load("img/sprite_bird.png").convert_alpha(), (self.charaWidth * 5 * self.scale, self.charaHeigh * self.scale))
        self.frame = 0
        self.actualFrame = pygame.Rect(self.frame * self.charaWidth * self.scale, 0, self.charaWidth * self.scale, self.charaHeigh * self.scale)
        self.timeNextFrame = 150
        self.rect.update(self.rect.x, self.rect.y, self.charaWidth*self.scale, self.charaHeigh*self.scale)
    
    def takeDamage(self, damageNumber):
        self.life -= damageNumber
        self.damage = True
    
    def update(self, dt):
        self.timeNextFrame -= dt
        if self.timeNextFrame < 0:
            self.timeNextFrame += 150
            if self.damage:
                self.frame = 5
                self.damage = False
            else:
                if self.frame >= 5:
                    self.frame = 0
                else:
                    self.frame = (self.frame + 1) % 4
            self.actualFrame = pygame.Rect(self.frame * self.charaWidth * self.scale, 0, self.charaWidth * self.scale, self.charaHeigh * self.scale)

    def draw(self, screen):
        screen.blit(self.spriteSheet, dest=(self.rect.x, self.rect.y), area=self.actualFrame)

    def resetFireCooldown(self):
        self.fireCooldown = pygame.time.get_ticks()+10*50
    
    def resetAbilityCooldown(self):
        self.abilityCooldown = pygame.time.get_ticks()+1800*16

    def left(self):
        if self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed

    def right(self, screen):
        if self.rect.x + self.speed <= screen.get_size()[0] - self.rect.width:
            self.rect.x  += self.speed
            self.timeNextFrame -= 25

    def up(self):
        if self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed

    def down(self, screen):
        if self.rect.y + self.speed <= screen.get_size()[1] - self.rect.height - 100:
            self.rect.y += self.speed

    def setImgAngle(self):
        self.img = pygame.transform.rotozoom(self.imgBase, self.angle, 1)
        self.rect = self.img.get_rect(center=self.rect.center)
        
    def isDead(self):
        return self.life <= 0
    
    def launchProjectile(self):
        if pygame.time.get_ticks() > self.fireCooldown:
            offSetX = self.rect.x
            offSetY = self.rect.y
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseY -= 25
            vectX, vectY = mouseX - offSetX, mouseY - offSetY
            norm = math.sqrt( vectX**2 + vectY**2 )
            vect = (vectX/norm, vectY/norm)
            self.resetFireCooldown()

            for projIndex in range(len(self.all_projectiles)):
                if not self.all_projectiles[projIndex]:
                    self.all_projectiles[projIndex] = Projectile("img/boule_de_feu_bleu2-Sheet.png", False, offSetX, offSetY, 21, 9, vect, 3, True, 20)
                    break
    
    def juanAbility(self):
        if pygame.time.get_ticks() > self.abilityCooldown:
            spawnX = 0
            spawnY = 600 - self.rect.y/2
            upX = spawnX - 25
            upY = spawnY - 70
            downX = spawnX - 20
            downY = spawnY + 70
            vect = (1, 0)
            self.resetAbilityCooldown()

            for projIndex in range(len(self.all_projectiles)):
                if not self.all_projectiles[projIndex]:
                    self.all_projectiles[projIndex] = Projectile("img/boule_de_feu_bleu2-Sheet.png", False, spawnX, spawnY, 21, 9, vect, 3, True)
                    self.all_projectiles[projIndex + 1] = Projectile("img/boule_de_feu_bleu2-Sheet.png", False, upX, upY, 21, 9, vect, 3, True)
                    self.all_projectiles[projIndex + 2] = Projectile("img/boule_de_feu_bleu2-Sheet.png", False, downX, downY, 21, 9, vect, 3, True)
                    break