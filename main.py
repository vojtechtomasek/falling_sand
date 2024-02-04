import pygame
import math
import random
import numpy as np


pygame.init()

WIDTH, HEIGHT = 800,800
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Falling sand")

WHITE= (255,255,255)

SAND_COLOR=(194, 178, 128)
grain_size = 8

class Grid:
    def __init__(self):
        self.grid=np.zeros((WIDTH*2,HEIGHT+grain_size))
        self.position=[]
    
    def addSand(self,pointX, pointY):
        if pointX>=0 and pointX<=WIDTH and pointY>=0 and pointY<=HEIGHT:
            if self.grid[pointX][pointY]==0:
                self.grid[pointX][pointY]=1
                self.position.append((pointX,pointY))
                
                # Add more sand around the clicked position
                for i in range(-grain_size, grain_size+1, grain_size):
                    for j in range(-grain_size, grain_size+1, grain_size):
                        if i != 0 or j != 0:
                            new_x = pointX + i
                            new_y = pointY + j
                            if new_x >= 0 and new_x <= WIDTH and new_y >= 0 and new_y <= HEIGHT:
                                if self.grid[new_x][new_y] == 0:
                                    self.grid[new_x][new_y] = 1
                                    self.position.append((new_x, new_y))

    
    def update_position(self):
        for points in self.position:
            listpoints= list(points)
            self.position.remove(points)
            
            if points[1]>=HEIGHT-grain_size:
                self.position.append(points)
            
            elif self.grid[points[0]][points[1]+grain_size]==0:
                self.grid[points[0]][points[1]] = 0
                self.grid[points[0]][points[1]+grain_size] = 1
                listpoints[1]+=grain_size
                points= tuple(listpoints)
                self.position.append(points)
                
                
            elif self.grid[points[0]][points[1]+grain_size]==1:
                if  (self.grid[points[0]+grain_size][points[1]+grain_size]==1) and (self.grid[points[0]-grain_size][points[1]+grain_size]==1):
                    self.position.append(points)
                    
                elif (self.grid[points[0]+grain_size][points[1]+grain_size]==1) and (self.grid[points[0]-grain_size][points[1]+grain_size]==0):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0]-grain_size][points[1]+grain_size] = 1
                    listpoints[0]-=grain_size
                    listpoints[1]+=grain_size
                    points= tuple(listpoints)
                    self.position.append(points)
                    
                elif (self.grid[points[0]+grain_size][points[1]+grain_size]==0) and (self.grid[points[0]-grain_size][points[1]+grain_size]==1):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0]+grain_size][points[1]+grain_size] = 1
                    listpoints[0]+=grain_size
                    listpoints[1]+=grain_size
                    points= tuple(listpoints)
                    self.position.append(points)
                    
                else:
                    self.grid[points[0]][points[1]] = 0
                    a= random.randint(0,1)
                    if a==0:
                        a=-1
                    self.grid[points[0]+a*grain_size][points[1]+grain_size] = 1
                    listpoints[0]+=a*grain_size
                    listpoints[1]+=grain_size
                    points= tuple(listpoints)
                    self.position.append(points)
    
    def draw(self, window):
        for points in self.position:
            pygame.draw.rect(window, SAND_COLOR, (points[0],points[1],grain_size,grain_size), 0)       
                    

def main():
    run= True
    clock= pygame.time.Clock()
    
    game = Grid()
    
    while run:
        WINDOW.fill((0,0,0))
        pygame.display.set_caption("Falling Sand - FPS: {}".format(int(clock.get_fps())))
        clock.tick(100)
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
            
            elif pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                btn=pygame.mouse
                game.addSand(pos[0]-pos[0]%grain_size,pos[1]-pos[1]%grain_size)
        
        game.update_position()
        game.draw(WINDOW)
        
                
               
        pygame.display.update()
    pygame.quit()
    
    
if __name__ == "__main__":
    main()
            
        
