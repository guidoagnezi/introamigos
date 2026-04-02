import pygame
from settings import *
import time

class InputBox:
    def __init__(self, x, y, w, h, texto="", tamanho_fonte=28, tamanho_max_texto=10):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.ativo = False

        self.tamanho_max_texto = tamanho_max_texto

        self.tamanho_fonte = tamanho_fonte
        self.cor_inativa = (180, 180, 180)
        self.cor_ativa = (100, 150, 255)
        self.cor = self.cor_inativa

        self.backspace_held = False
        self.backspace_timer = 0
        self.backspace_delay = 0.4   
        self.backspace_interval = 0.05  
        self.backspace_started = False

        self.fonte = pygame.font.SysFont(None, self.tamanho_fonte)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.ativo = True
            else:
                self.ativo = False

            self.cor = self.cor_ativa if self.ativo else self.cor_inativa

        if event.type == pygame.KEYDOWN and self.ativo:
            if event.key == pygame.K_RETURN:
                print("Nome confirmado:", self.texto)

            elif event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
                self.backspace_held = True
                self.backspace_timer = time.time()
                self.backspace_started = False

            else:
                if len(self.texto) < self.tamanho_max_texto:
                    self.texto += event.unicode
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = False

        self.texto = self.texto.replace("^", "").replace("~", "").replace("´", "").replace("`", "")

    def update(self):

        if self.backspace_held and self.ativo:
            agora = time.time()

            if not self.backspace_started:
                if agora - self.backspace_timer > self.backspace_delay:
                    self.backspace_started = True
                    self.backspace_timer = agora
            else:
                if agora - self.backspace_timer > self.backspace_interval:
                    self.texto = self.texto[:-1]
                    self.backspace_timer = agora
                    
    def draw(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect, 2)

        superficie = self.fonte.render(self.texto, True, (0, 0, 0)).convert_alpha()
        tela.blit(superficie, (self.rect.x + 5, self.rect.y + 5))

        if self.ativo and int(time.time() * 2) % 2 == 0:
            cursor = self.fonte.render("|", True, (0,0,0)).convert_alpha()
            tela.blit(cursor, (self.rect.x + 5 + superficie.get_width(), self.rect.y + 5))