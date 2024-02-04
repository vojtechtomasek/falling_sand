import pygame
import random
import numpy as np

pygame.init()


WIDTH, HEIGHT = 800,800
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Falling sand")

WHITE = (255,255,255)

SAND_COLOR = (194, 178, 128)
grain_size = 8


class Grid:
    def __init__(self):
        self.grid = np.zeros((WIDTH*2,HEIGHT+grain_size))
        # List to store positions of sand particles
        self.position=[]
        self.hue_shift = 0  
    
    def addSand(self,pointX, pointY):
        if pointX >= 0 and pointX <= WIDTH and pointY >= 0 and pointY <= HEIGHT:
            if self.grid[pointX][pointY] == 0:
                # Set the grid at the clicked position to 1, representing sand
                self.grid[pointX][pointY] = 1
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
            list_points= list(points)
            self.position.remove(points)
            
            # Check if the sand is at the bottom of the window
            if points[1] >= HEIGHT - grain_size:
                self.position.append(points)
            
            # Check if the space below is empty, then move the sand down
            elif self.grid[points[0]][points[1] + grain_size] == 0:
                self.grid[points[0]][points[1]] = 0
                self.grid[points[0]][points[1]+grain_size] = 1
                list_points[1] += grain_size
                points= tuple(list_points)
                self.position.append(points)
                
            # Check for collisions and adjust sand accordingly
            elif self.grid[points[0]][points[1]+grain_size] == 1:
                if  (self.grid[points[0] + grain_size][points[1] + grain_size] == 1) and (self.grid[points[0]-grain_size][points[1]+grain_size] == 1):
                    self.position.append(points)
                    
                elif (self.grid[points[0] + grain_size][points[1]+grain_size] == 1) and (self.grid[points[0]-grain_size][points[1]+grain_size] == 0):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] - grain_size][points[1]+grain_size] = 1
                    list_points[0] -= grain_size
                    list_points[1] += grain_size
                    points= tuple(list_points)
                    self.position.append(points)
                    
                elif (self.grid[points[0] + grain_size][points[1] + grain_size]==0) and (self.grid[points[0] - grain_size][points[1] + grain_size] == 1):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] + grain_size][points[1] + grain_size] = 1
                    list_points[0] += grain_size
                    list_points[1] += grain_size
                    points= tuple(list_points)
                    self.position.append(points)
                    
                else:
                    self.grid[points[0]][points[1]] = 0
                    a = random.randint(0,1)
                    if a == 0:
                        a =- 1
                    self.grid[points[0] + a * grain_size][points[1] + grain_size] = 1
                    list_points[0] += a * grain_size
                    list_points[1] += grain_size
                    points= tuple(list_points)
                    self.position.append(points)
                    
                    
                    
    def draw(self, window):
        for points in self.position:
            
            # Apply the color change to SAND_COLOR
            color_changed_sand = self.change_sand_color(SAND_COLOR, self.hue_shift)
            pygame.draw.rect(window, color_changed_sand, (points[0], points[1], grain_size, grain_size), 0)
                    
    
    def change_sand_color(self, color, hue_shift):
        # Extract RGB components
        r, g, b = color

        # Shift the hue value
        hue_shifted = (self.hue_shift + hue_shift) % 360

        # Convert hue to RGB
        rgb_shifted = self.hsv_to_rgb(hue_shifted / 360, 1, 1)

        # Apply the shifted hue to the original color
        r *= rgb_shifted[0]
        g *= rgb_shifted[1]
        b *= rgb_shifted[2]

        return int(r), int(g), int(b)


    def hsv_to_rgb(self, h, s, v):
        # Convert HSV to RGB
        if s == 0.0:
            return v, v, v

        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        if i % 6 == 0:
            return v, t, p
        elif i % 6 == 1:
            return q, v, p
        elif i % 6 == 2:
            return p, v, t
        elif i % 6 == 3:
            return p, q, v
        elif i % 6 == 4:
            return t, p, v
        else:
            return v, p, q
    
    
def main():
    run= True
    clock= pygame.time.Clock()
    
    # Instance of the Grid class
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
                game.addSand(pos[0] - pos[0] % grain_size,pos[1] - pos[1] % grain_size)
        
        game.update_position()
        game.draw(WINDOW)
        
        game.hue_shift += 1
               
        pygame.display.update()
        
    pygame.quit()
    
    
if __name__ == "__main__":
    main()
            
        
