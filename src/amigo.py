import pygame
import random
import math
from settings import *

class Amigo():
    def __init__(self, img, nome, personalidade="PADRAO"):

        self.img = img
        self.rect = img.get_rect(center=((LARGURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT), (ALTURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT)))
        self.nome = nome

        self.personalidade = personalidade

        self.target_vel_x = 0.0
        self.target_vel_y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0

        self.angulo = 0.0

        self.state = WANDERING

        self.wander_timer = WANDER_TIME

        self.step_timer = 0
        self.jump_high = 5
        self.vel_step = 0.2
        self.offset_y = 0
        
        self.talking_amigo = None
        self.talk_timer = 0

        self.talk_cooldown = 0
        self.talk_cd_max = TALK_COOLDOWN
        self.relacoes = {}

    def setEstado(self, novo_estado):
        self.state = novo_estado
        if self.state == WANDERING:
            self.wander_timer = WANDER_TIME

    def getEstado(self):
        return self.state
    
    def setTarget(self, x, y):
        self.target_vel_x = x
        self.target_vel_y = y

    def comeca_conversa(self, outro):
        if outro.talk_cooldown == 0:
            outro.target_amigo = self
            outro.setEstado(FOLLOWING)
            outro.talk_cooldown = outro.talk_cd_max
            return True
        return False

    def draw_desc(self, janela):
        
        janela.blit(img_descricao, (0,0))
        max = max(self.relacoes, key=self.relacoes.get)
        if max:
            janela.blit(max.img, (200, 0))

    def update(self, amigos):
        
        if self.talk_cooldown > 0:
            self.talk_cooldown -= 1

        if self.state == WANDERING:

            if self.wander_timer >= WANDER_TIME:
                self.target_vel_x = random.uniform(-MAX_VEL_X, MAX_VEL_X)
                self.target_vel_y = random.uniform(-MAX_VEL_Y, MAX_VEL_Y)
                self.wander_timer = 0
            else:
                self.wander_timer += 1
            
            for outro in amigos:
                if outro == self or outro.state == FOLLOWING or outro.state == TALKING:
                    continue
                
                dx = outro.rect.x - self.rect.x
                dy = outro.rect.y - self.rect.y
                dist = (dx**2 + dy**2) ** 0.5

                if dist < 200 and self.talk_cooldown == 0:
                    if self.comeca_conversa(outro):
                        self.target_amigo = outro
                        self.setEstado(FOLLOWING)
                        self.talk_cooldown = self.talk_cd_max
                        break
                    continue
            
            suavizacao = 0.05
            self.vel_x += (self.target_vel_x - self.vel_x) * suavizacao
            self.vel_y += (self.target_vel_y - self.vel_y) * suavizacao

        if self.state == FOLLOWING and self.target_amigo:
            dx = self.target_amigo.rect.x - self.rect.x
            dy = self.target_amigo.rect.y - self.rect.y

            dist = (dx**2 + dy**2) ** 0.5

            if dist > self.rect.width:
                self.vel_x = (dx / dist) * 2
                self.vel_y = (dy / dist) * 2
            else:
                self.setEstado(TALKING)

        if self.state == TALKING:
            self.vel_x = 0
            self.vel_y = 0

            self.talk_timer += 1

            if self.talk_timer > 120:  # tempo conversando
                self.setEstado(INTERACTING)
                self.talk_timer = 0

        if self.state == INTERACTING and self.target_amigo:
    
            resultado = random.choice(["amizade", "inimizade"])

            if self.target_amigo not in self.relacoes:
                self.relacoes[self.target_amigo] = 0

            if resultado == "amizade":
                self.relacoes[self.target_amigo] += 1
            else:
                self.relacoes[self.target_amigo] -= 1

            self.target_amigo = None
            self.setEstado(WANDERING)
                
        angulo_max = 15

        self.angulo = (self.vel_x / MAX_VEL_X) * angulo_max

        vel_modulo = abs(self.vel_x) + abs(self.vel_y)

        if vel_modulo > 0.1:
            self.step_timer += self.vel_step * vel_modulo
        else:
            self.step_timer = 0

        self.offset_y = math.sin(self.step_timer) * self.jump_high

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
    
    def draw(self, janela):
        
        img_rot = pygame.transform.rotate(self.img, -self.angulo)
        rect = img_rot.get_rect(topleft=(self.rect.x, self.rect.y + self.offset_y))
        janela.blit(img_rot, rect)
        
        # pygame.draw.rect(janela, (255, 0, 0), self.rect, 2)
        if self.state == FOLLOWING:
            rect_curioso = img_curioso.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_curioso, rect_curioso)
        
        if self.state == TALKING:
            rect_talking = img_talking.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_talking, rect_talking)
