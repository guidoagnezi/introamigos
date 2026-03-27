import pygame
import tkinter as tk
from tkinter import filedialog
import sys


root = tk.Tk()
root.withdraw()

def selecionar_imagem():

    caminho = filedialog.askopenfilename(
        title="Escolha uma imagem para o jogo",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
    )
    return caminho

pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Carregador de Imagens")

imagem_surface = None
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                caminho = selecionar_imagem()
                if caminho:
                    try:
        
                        imagem_surface = pygame.image.load(caminho).convert_alpha()
                        imagem_surface = pygame.transform.scale(imagem_surface, (800, 600))
                    except pygame.error as e:
                        print(f"Erro ao carregar: {e}")

    tela.fill((30, 30, 30)) 

    if imagem_surface:
        pos = imagem_surface.get_rect(center=(400, 300))
        tela.blit(imagem_surface, pos)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
