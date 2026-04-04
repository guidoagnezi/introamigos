import pygame

def clamp_rect(rect, largura_tela, altura_tela, margem=5):
    rect.x = max(margem, min(rect.x, largura_tela - rect.width - margem))
    rect.y = max(margem, min(rect.y, altura_tela - rect.height - margem))
    return rect