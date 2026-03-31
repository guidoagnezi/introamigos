import pygame
from enum import Enum
import tkinter as tk
from tkinter.filedialog import askopenfilename

root = tk.Tk()
root.withdraw()

LARGURA = 1024
ALTURA = 768
FPS = 60
TITULO = "Intro Amigos"

# Constantes Amigos
# Estados


WANDERING = "wandering"
FOLLOWING = "following"
TALKING = "talking"
INTERACTING = "interacting"
OBSERVING = "observing"
DECIDING = "deciding"
AVOIDING = "avoiding"
GROUPING = "grouping"
RESTING = "resting"
GOSSIPING = "gossiping"
ARGUMENTING = "argumenting"
# Temporizadores

WANDER_TIME = 120
TALK_COOLDOWN_PADRAO = 600

# Velocidade e Posicao

SPAWN_LIMIT = 50
MAX_VEL_X = 2
MAX_VEL_Y = 2

HUD_WIDTH = 256

img_seta = pygame.image.load("amigo/seta.png")
img_positivo = pygame.image.load("amigo/positivo.png")
img_negativo = pygame.image.load("amigo/negativo.png")
img_maquiavelico = pygame.image.load("amigo/maquiavelico.png")
img_curioso = pygame.image.load("amigo/confuso.png")
img_talking = pygame.image.load("amigo/talking.png")
img_arguing = pygame.image.load("amigo/arguing.png")
img_zzz = pygame.image.load("amigo/zzz.png")
img_wandering = pygame.image.load("amigo/wandering_icon.png")
img_conversando = pygame.image.load("amigo/talking_icon.png")

img_carregar = pygame.image.load("fundo/carregar_frame.png")
img_descricao = pygame.image.load("fundo/desc_amigo.png")
pygame.font.init()
fonte = pygame.font.SysFont(None, 24)
fonte2 = pygame.font.Font("fonte/guidofontenasal.ttf", 26)
fonte3 = pygame.font.Font("fonte/guidofontenasal.ttf", 30)
fonte4 = pygame.font.Font("fonte/guidofontenasal.ttf", 20)

txt_amigos_desc = fonte4.render("AMIGOS", True, "black")
txt_inimigos_desc = fonte4.render("INIMIGOS", True, "black")

fonte5 = pygame.font.SysFont(None, 48)
fonte6 = pygame.font.Font("fonte/guidofontenasal.ttf", 12)