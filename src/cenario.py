import pygame
from settings import *

class Cenario():

    def __init__(self, img, pos_x, pos_y):
        self.img = img
        self.rect = img.get_rect(center=(pos_x, pos_y))
        

    def draw(self, janela):
        janela.blit(self.img, self.rect)
    
    def update(self, amigos):
        
        pass