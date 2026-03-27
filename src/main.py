import pygame
from settings import *
from amigo import *
from cenario import *
from cenas import *
import tkinter as tk
from tkinter.filedialog import askopenfilename

 
class Game():

    def __init__(self):
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()
        pygame.init()

        self.cena_atual = CenaAcampamento(self)

    def setCena(self, cena):
        self.cena_atual = cena 
    def run(self):
        while True:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.cena_atual.handle_events(event)

            self.cena_atual.update()
            self.cena_atual.draw(self.janela)
            
            pygame.display.update()
            


if __name__ == "__main__":
    jogo = Game()
    jogo.run()