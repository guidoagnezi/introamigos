import pygame
import random
import math

class Fogueira:
    def __init__(self, x, y):
        self.img = pygame.image.load("fundo/fogueira.png")
        self.rect = self.img.get_rect(center=(x, y))
        self.raio_min = 120
        self.raio_max = 150

    def get_ponto_aleatorio(self):
        angulo = random.uniform(0, 2 * math.pi)

        raio = random.uniform(self.raio_min, self.raio_max)

        x = self.rect.centerx + math.cos(angulo) * raio
        y = self.rect.centery + math.sin(angulo) * raio

        return x, y

    def draw(self, janela):
        janela.blit(self.img, self.rect)
        # pygame.draw.circle(janela, "red", (self.rect.centerx, self.rect.centery), self.raio_min, 5)
        # pygame.draw.circle(janela, "red", (self.rect.centerx, self.rect.centery), self.raio_max, 5)
