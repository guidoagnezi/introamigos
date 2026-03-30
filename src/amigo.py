import pygame
import random
import math
from fogueira import *
from settings import *
import uuid
class Amigo():
    def __init__(self, img, nome, personalidade="PADRAO"):

        self.img = img
        self.rect = img.get_rect(center=((LARGURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT), (ALTURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT)))
        self.nome = nome
        self.personalidade = personalidade
        self.id = str(uuid.uuid4())
        self.target_vel_x = 0.0
        self.target_vel_y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0

        self.vel_mod = 1

        self.target_pos = None
        self.fogueira_alvo = None

        self.angulo = 0.0

        self.state = WANDERING

        self.wander_timer = WANDER_TIME

        self.energy = 1
        self.social_need = 0

        self.energy_consumption = random.uniform(0.00015, 0.00035) 
        self.social_need_gain = 0.0007
        
        self.step_timer = 0
        self.jump_height = 5
        self.vel_step = 0.2
        self.offset_y = 0
        
        self.talking_amigo = None
        self.talk_timer = 0
        self.last_talk = None
        self.talk_cooldown = 0
        self.talk_cd_max = TALK_COOLDOWN_PADRAO
        self.relacoes = {}

        self.alvo_social = None

        self.is_lider = False
        self.cap_lideranca = random.random()    

        self.img_desc = pygame.transform.scale_by(img, 0.9)
        self.txt_desc_nome = fonte5.render(f"{self.nome}", True, "black")
        self.txt_desc_pers = fonte6.render(self.personalidade, True, "black")

        self.init_personalidade(self.personalidade)

    def init_personalidade(self, personalidade):

        if "COVARDE" in personalidade:
            self.talk_cd_max = TALK_COOLDOWN_PADRAO * 3

        if "CARENTE" in personalidade:
            self.talk_cd_max = TALK_COOLDOWN_PADRAO * 0.5
            self.social_need_gain = 0.0014

        if "PRA FRENTE" in personalidade:
            self.vel_step = 0.25
            self.vel_mod = 1.5
            self.energy_consumption = random.uniform(0.0005, 0.0004)
        
        if "RESENHUDO" in personalidade:
            self.cap_lideranca = 1

    def setEstado(self, novo_estado):
        self.state = novo_estado
        if self.state == WANDERING:
            self.wander_timer = WANDER_TIME
            self.alvo_social = None

    def getEstado(self):
        return self.state
    
    def setTarget(self, x, y):
        self.target_vel_x = x
        self.target_vel_y = y
    
    def definir_lider(self, outro):

        if self.cap_lideranca > outro.cap_lideranca:
            return self, outro
        else:
            return outro, self
        
    def perceber_amigos(self, amigos):
        visiveis = []

        for outro in amigos:
            if outro == self:
                continue
            
            dx = outro.rect.x - self.rect.x
            dy = outro.rect.y - self.rect.y
            dist = (dx**2 + dy**2) ** 0.5
            dist = max(dist, 0.001)

            if dist < 200:
                visiveis.append((outro, dist))

        return sorted(visiveis, key=lambda x: x[1])
    
    def calcula_resultado(self, outro):

        chance = 0.5

        personalidade = self.personalidade.split()

        amigavel = ["RESENHUDO", "MALANDRO", "INGENUO"]
        antissocial = ["PSICOPATA", "DIABOLICO", "CINICO"]

        if any(p in personalidade for p in amigavel):
            chance += 0.2
        elif any(p in personalidade for p in antissocial):
            chance -= 0.2

        o_personalidade = self.personalidade.split()

        if any(p in o_personalidade for p in amigavel):
            chance += 0.3
        elif any(p in o_personalidade for p in antissocial):
            chance -= 0.2

        if outro in self.relacoes:
            chance += self.relacoes[outro] * 0.05
        print(chance)
        return "amizade" if random.random() < chance else "inimizade"

    def aplica_relacao(self, outro, resultado):

        if outro not in self.relacoes:
            self.relacoes[outro] = 0

        if resultado == "amizade":
            self.relacoes[outro] += 1
        else:
            self.relacoes[outro] -= 1
    
    def finaliza_interacao(self):

        self.target_amigo = None
        self.social_need -= 0.8
        self.alvo_social = None
        self.setEstado(WANDERING)

    def get_relacoes_filtradas(self, qtd=100):
        amigos = []
        inimigos = []

        for i, (outro, valor) in enumerate(self.relacoes.items()):
            if i == qtd:
                break

            if valor > 0:
                amigos.append((outro, valor))
            elif valor < 0:
                inimigos.append((outro, valor))

        return amigos, inimigos

    def update(self, amigos, fogueiras):
        
        self.energy -= self.energy_consumption
        self.energy = max(0, min(1, self.energy))
        
        self.social_need += self.social_need_gain
        self.social_need = max(0, min(1, self.social_need))

        if self.energy < 0.2 and self.state != RESTING:

            if fogueiras:
                self.fogueira_alvo = random.choice(fogueiras)
                self.target_pos = self.fogueira_alvo.get_ponto_aleatorio()

            self.setEstado(RESTING)

        if self.state == WANDERING:

            if self.wander_timer >= WANDER_TIME:
                self.target_vel_x = random.uniform(-MAX_VEL_X, MAX_VEL_X)
                self.target_vel_y = random.uniform(-MAX_VEL_Y, MAX_VEL_Y)
                self.wander_timer = 0
            else:
                self.wander_timer += 1
            
            if self.social_need > 0.6:
                if random.random() < 0.05:
                    self.setEstado(OBSERVING)

            suavizacao = 0.05
            self.vel_x += (self.target_vel_x - self.vel_x) * suavizacao
            self.vel_y += (self.target_vel_y - self.vel_y) * suavizacao

        if self.state == OBSERVING:

            # print(f"{self.nome} está observando")
            visiveis = self.perceber_amigos(amigos)

            if visiveis:
                self.alvo_social = visiveis[0][0]  
                self.setEstado(DECIDING)
            else:
                self.setEstado(WANDERING)

        if self.state == DECIDING and self.alvo_social:
            
            # print(f"{self.nome} está decidindo")
            relacao = self.relacoes.get(self.alvo_social, 0)

            if relacao < 0:
                self.setEstado(AVOIDING)
                print(f"{self.nome} decidiu evitar")

            elif relacao > 0:
                if random.random() < 0.3 and self.social_need > 0.8: 
                    lider, seguidor = self.definir_lider(self.alvo_social)

                    lider.is_lider = True
                    seguidor.is_lider = False

                    lider.alvo_social = seguidor
                    seguidor.alvo_social = lider

                    lider.setEstado(GROUPING)
                    seguidor.setEstado(GROUPING)

            else:
                if self.talk_cooldown == 0 and self.alvo_social.talk_cooldown == 0:
                    self.target_amigo = self.alvo_social
                    self.setEstado(FOLLOWING)
                else:
                    self.setEstado(WANDERING)
            
            

        if self.state == FOLLOWING and self.target_amigo:
            dx = self.target_amigo.rect.x - self.rect.x
            dy = self.target_amigo.rect.y - self.rect.y

            dist = (dx**2 + dy**2) ** 0.5
            dist = max(dist, 0.001)

            if dist > self.rect.width:
                self.vel_x = (dx / dist) * 2
                self.vel_y = (dy / dist) * 2
            else:
                self.setEstado(TALKING)

        if self.state == TALKING:
            self.vel_x *= 0.9
            self.vel_y *= 0.9

            self.talk_timer += 1

            if self.talk_timer > 120:  
                self.setEstado(INTERACTING)
                self.talk_timer = 0

        if self.state == INTERACTING and self.target_amigo:

            
            outro = self.target_amigo
            self.ultimo_amigo = outro
            
            resultado = self.calcula_resultado(outro)

            self.aplica_relacao(outro, resultado)
            outro.aplica_relacao(self, resultado)

            self.finaliza_interacao()
            outro.finaliza_interacao()
        
        if self.state == AVOIDING and self.alvo_social:

            # print(f"{self.nome} está evitando {self.alvo_social.nome}")

            dx = self.rect.x - self.alvo_social.rect.x
            dy = self.rect.y - self.alvo_social.rect.y

            dist = (dx**2 + dy**2) ** 0.5 + 0.01
            dist = max(dist, 0.001)
            if dist < 350:
                self.vel_x = (dx / dist) * 2
                self.vel_y = (dy / dist) * 2
            else:
                self.setEstado(WANDERING)
        
        if self.state == GROUPING and self.alvo_social:

            if self.is_lider:

                if random.random() < 0.02:
                    self.target_vel_x = random.uniform(-MAX_VEL_X, MAX_VEL_X)
                    self.target_vel_y = random.uniform(-MAX_VEL_Y, MAX_VEL_Y)

                suavizacao = 0.05
                self.vel_x += (self.target_vel_x - self.vel_x) * suavizacao
                self.vel_y += (self.target_vel_y - self.vel_y) * suavizacao

            else:

                dx = self.alvo_social.rect.x - self.rect.x
                dy = self.alvo_social.rect.y - self.rect.y

                dist = (dx**2 + dy**2) ** 0.5
                dist = max(dist, 0.001)

                offset_dist = 110

                target_x = self.alvo_social.rect.x - (dx / dist) * offset_dist
                target_y = self.alvo_social.rect.y - (dy / dist) * offset_dist

                dx2 = target_x - self.rect.x
                dy2 = target_y - self.rect.y

                dist2 = (dx2**2 + dy2**2) ** 0.5

                dist2 = max(dist2, 0.001)

                if dist2 < 60:
                    self.vel_x *= 0.9
                    self.vel_y *= 0.9
                else:
                    suavizacao = 0.05
                    self.vel_x += ((dx2 / dist2) * 2 - self.vel_x) * suavizacao
                    self.vel_y += ((dy2 / dist2) * 2 - self.vel_y) * suavizacao
                

            if random.random() < 0.001:
                print(f"{self.nome} decidiu sair do grupo")
                self.is_lider = False
                self.social_need = 0
                self.alvo_social = None
                self.setEstado(WANDERING)

        if self.state == RESTING:

            if self.target_pos:

                dx = self.target_pos[0] - self.rect.x
                dy = self.target_pos[1] - self.rect.y

                dist = (dx**2 + dy**2) ** 0.5
                dist = max(dist, 0.001)

                if dist > 10:
                    self.vel_x = (dx / dist) * 1.5
                    self.vel_y = (dy / dist) * 1.5
                else:
                    self.target_pos = None
                    self.vel_x *= 0.8
                    self.vel_y *= 0.8

            else:
                self.vel_x *= 0.9
                self.vel_y *= 0.9

                if self.fogueira_alvo:
                    self.energy += 0.004
                else:
                    self.energy += 0.002

            if self.energy > 0.8:
                self.fogueira_alvo = None
                self.setEstado(WANDERING)

        angulo_max = 15

        self.angulo = (self.vel_x / MAX_VEL_X) * angulo_max

        vel_modulo = abs(self.vel_x) + abs(self.vel_y)

        if vel_modulo > 0.1:
            self.step_timer += self.vel_step * vel_modulo
        elif self.state == TALKING:
            self.step_timer += self.vel_step * 1.5
        elif self.state == RESTING:
            self.step_timer += self.vel_step * 0.5

        self.offset_y = math.sin(self.step_timer) * self.jump_height

        self.rect.x += self.vel_x * self.vel_mod
        self.rect.y += self.vel_y * self.vel_mod

        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
    
    def draw(self, janela):

        img_rot = pygame.transform.rotate(self.img, -self.angulo)
        rect = img_rot.get_rect(topleft=(self.rect.x, self.rect.y + self.offset_y))
        janela.blit(img_rot, rect)
        
        # pygame.draw.rect(janela, (255, 0, 0), self.rect, 2)
        # janela.blit(fonte.render(self.state, True, "black"), (self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
        if self.state == FOLLOWING:
            rect_curioso = img_curioso.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_curioso, rect_curioso)
        
        if self.state == TALKING:
            rect_talking = img_talking.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_talking, rect_talking)
        
        if self.state == RESTING:
            rect_zzz = img_zzz.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_zzz, rect_zzz)

    def draw_bar(self, janela, x, y, valor, cor):

        largura = 160
        altura = 20

        pygame.draw.rect(janela, (50,50,50), (x, y, largura, altura))
        pygame.draw.rect(janela, cor, (x, y, largura * valor, altura))

    def draw_desc(self, janela):
        
        HUD_WIDTH = 256
        hud_direita_x = LARGURA - HUD_WIDTH

        if self.rect.right > hud_direita_x:
            hud_x = 0
        else:
            hud_x = hud_direita_x

        janela.blit(img_descricao, (hud_x, 0))

        rect = self.img_desc.get_rect(center=(hud_x + 85, 85))

        
        janela.blit(self.img_desc, rect)
        janela.blit(self.txt_desc_nome, (hud_x + 18, 180))
        janela.blit(self.txt_desc_pers, (hud_x + 18, 220))

        self.draw_bar(janela, hud_x + 18, 260, self.energy, "greenyellow")
        self.draw_bar(janela, hud_x + 18, 320, self.social_need, "dodgerblue3")
        amigos, inimigos = self.get_relacoes_filtradas()
        
        x_base = hud_x + 25
        y_base = 480

        for i, (amigo, valor) in enumerate(amigos):
            if i == 3:
                break
            x = x_base 
            y = y_base + i * 90
            janela.blit(pygame.transform.scale(amigo.img, (70,70)), (x, y))

        x_base_i = hud_x + 150

        for i, (amigo, valor) in enumerate(inimigos):
            if i == 3:
                break
            x = x_base_i
            y = y_base + i * 90
            janela.blit(pygame.transform.scale(amigo.img, (70,70)), (x, y))
