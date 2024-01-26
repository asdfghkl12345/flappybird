import pygame,os
import constants as C
pygame.init()
IMAGES = {}
MUSIC = {}
for sound in os.listdir('assets/audio'):
    name,extension = os.path.splitext(sound)
    path = os.path.join('assets/audio',sound)
    MUSIC[name] = pygame.mixer.Sound(path)
for image in os.listdir('assets/sprites'):
    name,extension = os.path.splitext(image)
    path = os.path.join('assets/sprites',image)
    IMAGES[name] = pygame.image.load(path)