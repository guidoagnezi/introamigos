import pygame
import random
import math

class Sombra:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
    
    def esta_na_sombra(self, pos):
        sombra = self.get_sombra_rect()

        area = sombra.inflate(80, 40)

        return area.collidepoint(pos)

    def get_sombra_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def get_ponto_sombra(self):
        sombra = self.get_sombra_rect().inflate(80, 40)

        x = random.uniform(sombra.left, sombra.right)
        y = random.uniform(sombra.top, sombra.bottom)

        return x, y

    def draw(self, janela):
        sombra_rect = self.get_sombra_rect()

        sombra_surf = pygame.Surface(
            (sombra_rect.width, sombra_rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            sombra_surf,
            (0, 0, 0, 80),
            (0, 0, sombra_rect.width, sombra_rect.height)
        )

        janela.blit(sombra_surf, sombra_rect)
        
class Arvore:
    def __init__(self, img, x, y):
        self.img = img

        self.x = x
        self.y = y

        self.rect = self.img.get_rect(center=(x, y))

        self.sombra_largura = self.rect.width * 1.2
        self.sombra_altura = 120

        self.sombra = Sombra(self.rect.centerx - self.sombra_largura/2, self.rect.bottom - self.sombra_altura / 2, self.rect.width * 1.2, 120)


        self.tilt_timer = 10000
        self.angulo = 0

        self.transparente = False

    def update(self, amigos):

        self.transparente = False

        for amigo in amigos:
            if (
                amigo.rect.centerx >= self.rect.left and
                amigo.rect.centerx <= self.rect.right and
                amigo.rect.top >= self.rect.top and
                amigo.rect.bottom <= self.rect.bottom
            ):
                self.transparente = True
                break

    def draw(self, janela):

        img_rot = pygame.transform.rotate(self.img, self.angulo)

        if self.transparente:
            img_rot.set_alpha(110)
        else:
            img_rot.set_alpha(255)

        
        janela.blit(img_rot, self.rect)
