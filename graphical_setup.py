import pygame, sys
from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Yellow Submarine Control')

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (50, 255, 55)

### Creating window surface
window = pygame.display.set_mode((800, 600))

### Creating submarine
submarine = pygame.image.load('images/yellowsub.png') 
submarine = pygame.transform.scale(submarine, (int(submarine.get_width()*0.2) , int(submarine.get_height()*0.2 )))

### Final loop function
def final_loop():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)
