import pygame, math
from entity.enemy import *
from random import randint

class Level():
    
    def __init__(self, levelNumber):
        self.level = {}
        a = 'game/level/level' + str(levelNumber) + '.txt'
        docLevels = open(a, 'r')
        levels = docLevels.read()
        docLevels.close
        for row in levels.split('\n'):
            level = row.split(': ')
            self.level[level[0]] = level[1]
        ennemies = self.level['ennemies'].split(', ')
        self.level['ennemies'] = []
        for ennemy in ennemies:
            ennemyProps = ennemy.split('/')
            self.level['ennemies'].append({'time': int(ennemyProps[0]), 'type': int(ennemyProps[1])})
        obstacles = self.level['obstacles'].split(', ')
        self.level['obstacles'] = []
        for obstacle in obstacles:
            obstacleProps = obstacle.split('/')
            self.level['obstacles'].append({'time': int(obstacleProps[0]), 'type': int(obstacleProps[1])})
        self.level['difficulty'] = int(self.level['difficulty'])

        self.background = pygame.transform.scale(pygame.image.load(self.level['background']).convert(), (5012 * pygame.display.get_window_size()[1] / 1280, pygame.display.get_window_size()[1]))
        self.position = 0
        self.speed = 10
        
    def ennemiesSpawn(self, timer, game):
        for i in range(len(self.level['ennemies'])-1, -1, -1):
            if timer >= self.level['ennemies'][i]['time'] * 1000:
                for j in range(len(game.enemies)):
                    if game.enemies[j] == None:
                        match self.level['ennemies'][i]['type']:
                            case 1:
                                game.enemies[j] = SuicidePigeon(self.level['difficulty'], pygame.display.get_window_size()[0], randint(0, pygame.display.get_window_size()[1]))
                            case 2:
                                game.enemies[j] = StrafingDrone(self.level['difficulty'], pygame.display.get_window_size()[0], randint(0, pygame.display.get_window_size()[1]), game.projectiles)
                            case 3:
                                game.enemies[j] = DrunkPigeon(self.level['difficulty'])
                            case 4:
                                game.enemies[j] = Scientist(self.level['difficulty'], game.projectiles)
                            case 5:
                                game.enemies[j] = Boss(self.level['difficulty'], game.projectiles)
                            case _:
                                print("Not spawned\ncase: " + str(self.level['ennemies'][i]['type']))
                        break
                self.level['ennemies'].pop(i)

    def obstaclesSpawn(self, timer, game):
        for i in range(len(self.level['obstacles'])-1, -1, -1):
            if timer >= self.level['obstacles'][i]['time'] * 1000 + 5000:
                for j in range(len(game.obstacles)):
                    if game.obstacles[j] == None:
                        #game.obstacles[j] = Obstacle()
                        break
                self.level['obstacles'].pop(i)
    
    def draw(self, screen):
        i = 0
        while(i < 100):
            screen.blit(self.background, (self.background.get_width()*i + self.position, 0))
            i += 1

    def update(self):
        # FRAME FOR SCROLLING
        self.position -= self.speed
        # RESET THE SCROLL FRAME
        if abs(self.position) > self.background.get_width():
            self.position = 0
        