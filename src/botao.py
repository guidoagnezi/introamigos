import pygame
from settings import *
class Botao:
    def __init__(self, x, y, img_frame, texto,callback, fonte=fonte2, cor_normal="black", cor_hover="green", cor_inativo="gray"):
        self.x = x
        self.y = y

        self.fonte = fonte
        self.texto : str = texto
        self.inativo = False

        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_inativo = cor_inativo

        self.cor = self.cor_normal

        self.img = img_frame
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.callback = callback

    def handle_event(self, event):
        if not self.inativo:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
    
    def update(self):
        mx, my = pygame.mouse.get_pos()

        if self.inativo:
            self.cor = self.cor_inativo

        elif self.rect.collidepoint((mx, my)):
            self.cor = self.cor_hover
            return True
        else:
            self.cor = self.cor_normal

        return False
    
    def setInatividade(self, atividade):
        self.inativo = atividade

    def draw(self, janela):

        janela.blit(self.img, self.rect)

        texto_surf = self.fonte.render(self.texto, True, self.cor)
        texto_rect = texto_surf.get_rect(center=self.rect.center)

        janela.blit(texto_surf, texto_rect)