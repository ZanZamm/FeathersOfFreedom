import pygame

class Entity():

    def __init__(self, destructible: bool, x=0, y=0, w=0, h=0, spritePath=None):
        """spritePath est une string optionelle à n'utiliser que pour les entité visible"""
        self.destructible = destructible
        if spritePath:
            self.imgBase = pygame.transform.scale(pygame.image.load(spritePath), (w, h))
            self.image = self.imgBase
            self.rect = self.image.get_rect()
            if x != 0 and y != 0:
                self.rect.update(x, y, self.rect.width, self.rect.height)
        else:
            self.rect = pygame.Rect(x, y, w, h)

    def rectOverlap(self, otherEntity):
        """Renvoie True si l'entité entre en colision avec un autre"""
        return self.rect.x < otherEntity.rect.x + otherEntity.rect.width and self.rect.x + self.rect.width > otherEntity.rect.x and self.rect.y < otherEntity.rect.y + otherEntity.rect.height and self.rect.y + self.rect.height > otherEntity.rect.y

class Button(Entity):

    def __init__(self, x: int, y: int, type: str):
        super().__init__(False, x, y, 73*7.5, 14*7.5, "img/ui_sheet.png")
        self.type = type
        self.hover = False
        self.image = pygame.transform.scale(pygame.image.load("img/ui_sheet.png").convert_alpha(), (1920, 960))
        self.image2 = pygame.transform.scale(pygame.image.load("img/ui_hold_to_open_Sheet.png").convert_alpha(), (512*5, 32*5))
        self.oeuf = pygame.transform.scale(pygame.image.load("img/ui_eggs2-Sheet.png").convert_alpha(), (1442*5, 112*5))
        self.background = pygame.Surface((self.rect.width,self.rect.height)).convert_alpha()
    
    def isPressed(self):
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            return self.rectOverlap(Entity(False, mouseX, mouseY))

    def draw(self, screen):
        scale = 7.5
        if self.type == "game_over":
            screen.blit(self.image, (self.rect.x, self.rect.y), (128*scale, 16*scale, 101*scale, 14*scale)) 
        elif self.type == "win":
            screen.blit(self.image, (self.rect.x, self.rect.y), (128*scale, 16*scale, 101*scale, 14*scale)) 
        elif self.type == "HP":
            screen.blit(self.image, (self.rect.x, self.rect.y), (98*scale, 18*scale, 11*scale, 9*scale)) 
        elif self.type == "pause":
            screen.blit(self.image, (self.rect.x, self.rect.y), (16*scale, 48*scale, 18*scale, 13*scale))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y), (16*scale, 32*scale, 73*scale, 14*scale)) 
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.rectOverlap(Entity(False, mouseX, mouseY)):
            if self.type == "start":
                screen.blit(self.image, (self.rect.x + 18*scale, self.rect.y + 2*scale), (118*scale, 49*scale, 36*scale, 10*scale))
            elif self.type == "option":
                screen.blit(self.image, (self.rect.x + 10*scale, self.rect.y + 2*scale), (23*scale, 82*scale, 56*scale, 10*scale))
            elif self.type == "quit":
                screen.blit(self.image, (self.rect.x + 20*scale, self.rect.y + 2*scale), (35*scale, 114*scale, 32*scale, 10*scale))
            elif self.type == "menu":
                screen.blit(self.image, (self.rect.x + 18*scale, self.rect.y + 2*scale), (199*scale, 81*scale, 37*scale, 10*scale))
            elif self.type == "gacha":
                screen.blit(self.image, (self.rect.x + 13*scale, self.rect.y + 2*scale), (194*scale, 113*scale, 48*scale, 10*scale))
            elif self.type == "replay":
                screen.blit(self.image, (self.rect.x + 11*scale, self.rect.y + 2*scale), (113*scale, 112*scale, 53*scale, 10*scale))
            elif self.type == "game_over":
                screen.blit(self.image, (self.rect.x + 11*scale, self.rect.y + 2*scale), (101*scale, 65*scale, 78*scale, 10*scale))
            elif self.type == "pause":
                screen.blit(self.image, (self.rect.x + 7*scale, self.rect.y + 3*scale), (58*scale, 51*scale, 7*scale, 7*scale))
            elif self.type == "open":
                screen.blit(self.image2, (self.rect.x + 8*5, self.rect.y + 5*5), (401*5, 19*5, 93*5, 10*5))
            elif self.type == "oeuf":
                screen.blit(self.oeuf, (self.rect.x + 8*5, self.rect.y + 5*5), (811*5, 4*5, 147*5, 107*5))
            elif self.type == "win":
                screen.blit(self.image, (self.rect.x + 23*scale, self.rect.y + 2*scale), (189*scale, 35*scale, 57*scale, 10*scale))
            
        
        else:
            if self.type == "start":
                screen.blit(self.image, (self.rect.x + 18*scale, self.rect.y + 2*scale), (118*scale, 34*scale, 36*scale, 10*scale))
            elif self.type == "option":
                screen.blit(self.image, (self.rect.x + 10*scale, self.rect.y + 2*scale), (23*scale, 66*scale, 56*scale, 10*scale))
            elif self.type == "quit":
                screen.blit(self.image, (self.rect.x + 20*scale, self.rect.y + 2*scale), (35*scale, 98*scale, 32*scale, 10*scale))
            elif self.type == "menu":
                screen.blit(self.image, (self.rect.x + 18*scale, self.rect.y + 2*scale), (199*scale, 66*scale, 37*scale, 10*scale))
            elif self.type == "gacha":
                screen.blit(self.image, (self.rect.x + 13*scale, self.rect.y + 2*scale), (194*scale, 97*scale, 48*scale, 10*scale))
            elif self.type == "replay":
                screen.blit(self.image, (self.rect.x + 11*scale, self.rect.y + 2*scale), (113*scale, 97*scale, 53*scale, 10*scale))
            elif self.type == "game_over":
                screen.blit(self.image, (self.rect.x + 11*scale, self.rect.y + 2*scale), (101*scale, 65*scale, 78*scale, 10*scale))
            elif self.type == "pause":
                screen.blit(self.image, (self.rect.x + 7*scale, self.rect.y + 3*scale), (43*scale, 51*scale, 7*scale, 7*scale))
            elif self.type == "open":
                screen.blit(self.image2, (self.rect.x + 8*5, self.rect.y + 5*5), (17*5, 19*5, 93*5, 10*5))
            elif self.type == "oeuf":
                screen.blit(self.oeuf, (self.rect.x + 8*5, self.rect.y + 5*5), (55*5, 32*5, 46*5, 56*5))
            elif self.type == "win":
                screen.blit(self.image, (self.rect.x + 23*scale, self.rect.y + 2*scale), (189*scale, 35*scale, 57*scale, 10*scale))
        
class Egg(Entity):

    def __init__(self, x: int, y: int, type: str):
        super().__init__(False, x, y, 100*5, 100*5, "img/ui_eggs2-Sheet.png")
        self.type = type
        self.hover = False
        self.oeuf = pygame.transform.scale(pygame.image.load("img/ui_eggs2-Sheet.png").convert_alpha(), (1442*5, 112*5))
        self.background = pygame.Surface((self.rect.width,self.rect.height)).convert_alpha()
        self.w = 160
        self.h = 114
        self.scale = 5
        self.spriteSheet = pygame.transform.scale(pygame.image.load("img/ui_eggs2-Sheet.png").convert_alpha(), (self.w * 5 * self.scale, self.h * self.scale))
        self.frame = 0
        # Création de variables pour animation
        self.actualFrame = pygame.Rect(self.frame * self.w * self.scale, 0, self.w * self.scale, self.h * self.scale)
        self.timeNextFrame = 150
    
    def isPressed(self):
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            return self.rectOverlap(Entity(False, mouseX, mouseY))
    
    def update(self, dt):
        self.timeNextFrame -= dt
        print(self.timeNextFrame)
        if self.timeNextFrame < 0:
            self.timeNextFrame += 150
            if self.frame >= 9:
                self.frame = 0
            else:
                self.frame = (self.frame + 1) % 8
        self.actualFrame = pygame.Rect(self.frame * self.w * self.scale, 0, self.w * self.scale, self.h * self.scale)

    def draw(self, screen): 
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.rectOverlap(Entity(False, mouseX, mouseY)):
            if self.type == "oeuf":
                screen.blit(self.oeuf, (self.rect.x + 8*5, self.rect.y + 1*5), area = self.actualFrame)
        else:
            if self.type == "oeuf":
                screen.blit(self.oeuf, (self.rect.x + 60*5, self.rect.y + 40*5), (44*self.scale, 26*self.scale, 69*self.scale, 70*self.scale))