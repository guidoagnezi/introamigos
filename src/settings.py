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
HUNGRY = "hungry"
EATING = "eating"
TALKING = "talking"
INTERACTING = "interacting"
PERSUING = "persuing"
STEALING = "stealing"

# Temporizadores

WANDER_TIME = 120
TALK_COOLDOWN = 600

# Velocidade e Posicao

SPAWN_LIMIT = 200
MAX_VEL_X = 2
MAX_VEL_Y = 2

img_seta = pygame.image.load("amigo/seta.png")
img_positivo = pygame.image.load("amigo/positivo.png")
img_negativo = pygame.image.load("amigo/negativo.png")
img_maquiavelico = pygame.image.load("amigo/maquiavelico.png")
img_curioso = pygame.image.load("amigo/confuso.png")
img_talking = pygame.image.load("amigo/talking.png")

img_descricao = pygame.image.load("fundo/desc_amigo.png")
pygame.font.init()
fonte = pygame.font.SysFont(None, 24)
fonte2 = pygame.font.Font("fonte/guidofontenasal.ttf", 26)
fonte3 = pygame.font.Font("fonte/guidofontenasal.ttf", 30)
fonte4 = pygame.font.Font("fonte/guidofontenasal.ttf", 20)