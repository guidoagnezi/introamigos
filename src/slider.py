import pygame
from settings import *
class Slider:
    def __init__(self, nome, x, y, largura, altura, n_barras, valor_inicial=0):
        self.nome = nome

        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

        self.n_barras = n_barras
        self.valor = valor_inicial

        self.arrastando = False
        
        self.espaco = 4

    def get_indice_mouse(self, mx):
        largura_total = self.largura
        barra_largura = (largura_total - (self.n_barras - 1) * self.espaco) / self.n_barras

        for i in range(self.n_barras):
            bx = self.x + i * (barra_largura + self.espaco)
            if bx <= mx <= bx + barra_largura:
                return i + 1

        return None

    def handle_event(self, event, sliders=None, limite_total=-1):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if self.x <= mx <= self.x + self.largura and self.y <= my <= self.y + self.altura:

                indice = self.get_indice_mouse(mx)

                if indice is not None:

                    soma_atual = sum(s.valor for s in sliders)

                    diff = indice - self.valor

                    if soma_atual + diff <= limite_total:
                        self.arrastando = True
                        self.valor = indice

        elif event.type == pygame.MOUSEBUTTONUP:
            self.arrastando = False

        elif event.type == pygame.MOUSEMOTION:
            if self.arrastando:
                mx, _ = pygame.mouse.get_pos()
                indice = self.get_indice_mouse(mx)

                if indice is not None:
                    soma_atual = sum(s.valor for s in sliders)
                    diff = indice - self.valor

                    if soma_atual + diff <= limite_total:
                        self.valor = indice

    def draw(self, tela):
        barra_largura = (self.largura - (self.n_barras - 1) * self.espaco) / self.n_barras

        desc = fonte2.render(f"{self.nome}", True, "black")
        rect = desc.get_rect(topleft=(self.x, self.y - self.altura + 5))

        value_txt = fonte3.render(f"{int(self.valor)}", True, "black")
        rect_value = value_txt.get_rect(topleft=(self.x + self.largura + 10, self.y + 5))

        tela.blit(desc, rect)
        tela.blit(value_txt, rect_value)

        for i in range(self.n_barras):
            bx = self.x + i * (barra_largura + self.espaco)

            if i < self.valor:
                cor = (100, 200, 100)
            else:
                cor = (200, 200, 200)

            pygame.draw.rect(
                tela,
                cor,
                (bx, self.y, barra_largura, self.altura),
                border_radius=0
            )