import pygame
import random
import math
from fogueira import *
from settings import *
import uuid
from utils import *

class Amigo():

    def __init__(self, img, nome, personalidade="PADRAO", comida_favoria="Biscoito", assunto_favorito="IntroComp", criador="Não creditado"):

        self.img = img
        self.rect = img.get_rect(center=((LARGURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT), (ALTURA/2) + random.uniform(-SPAWN_LIMIT, SPAWN_LIMIT)))
        self.nome = nome
        self.personalidade = personalidade
        self.comida = comida_favoria
        self.assunto = assunto_favorito
        self.criador = criador
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

        self.energy_consumption = random.uniform(0.00005, 0.00012) 
        self.social_need_gain = 0.0007
        
        self.step_timer = 0
        self.jump_height = 5
        self.vel_step = 0.2
        self.offset_y = 0
        
        self.talking_amigo = None
        self.talk_timer = 0
        self.last_talk = None
        self.relacoes = {}
        self.interaction_type = None
        self.opiniao = None
        self.alvo_social = None
        self.alvo_fofoca = None

        self.is_lider = False
        self.cap_lideranca = random.random()    

        self.img_desc = pygame.transform.scale_by(img, 0.9)
        self.txt_desc_nome = fonte5.render(f"{self.nome}", True, "black").convert_alpha()
        self.txt_desc_pers = fonte6.render(self.personalidade, True, "black").convert_alpha()
        self.txt_criador = fonte.render(f"Por: {self.criador}", True, "black").convert_alpha()
        
        self.acessorios = {
            "chapeu": None,
            "item": None
        }
        
        self.mensagem = None
        self.message_timer = 0
        self.frases = []
        self.frases.extend(mensagens["padrao"])

        self.init_personalidade(self.personalidade)

    def init_personalidade(self, personalidade):

        if "CARENTE" in personalidade:
            self.social_need_gain = 0.0014

        if "PRA FRENTE" in personalidade:
            self.vel_step = 0.25
            self.vel_mod = 1.5
            self.energy_consumption = random.uniform(0.0005, 0.0004)
        
        if "RESENHUDO" in personalidade:
            self.cap_lideranca = 1

        for (item, _) in mensagens.items():

            if item in self.personalidade.lower():
                self.frases.extend(mensagens[item])

    def setEstado(self, novo_estado):
        self.state = novo_estado
        if self.state == WANDERING:
            self.wander_timer = WANDER_TIME
            self.alvo_social = None
    
    def setAcessorio(self, tipo, img):
        self.acessorios[tipo] = img.convert_alpha()

    def removeAcessorios(self):
        for k in self.acessorios:
            self.acessorios[k] = None

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
        self.talk_timer = 0
        self.target_amigo = None
        self.social_need -= 0.8
        self.alvo_social = None
        print(self.relacoes)
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
    
    def gerar_mensagem(self, amigos):

        frase = random.choice(self.frases)

        proximos = self.perceber_amigos(amigos)
        nomes_proximos = [a.nome for a, _ in proximos]

        amigo_nome = random.choice(nomes_proximos) if nomes_proximos else "alguém"

        inimigos = [a.nome for a, v in self.relacoes.items() if v < 0]
        inimigo_nome = random.choice(inimigos) if inimigos else "fulano"


        return frase.format(
            comida=self.comida,
            assunto=self.assunto,
            criador=self.criador,
            nome=self.nome,
            personalidade=self.personalidade,
            amigo=amigo_nome,
            inimigo=inimigo_nome
        )
    
    def iniciar_mensagem(self, amigos):
        self.mensagem = self.gerar_mensagem(amigos)
        self.message_timer = 0
        self.setEstado(MESSAGE)

    def update(self, amigos, fogueiras):
        
        self.energy -= self.energy_consumption
        self.energy = max(0, min(1, self.energy))
        
        self.social_need += self.social_need_gain
        self.social_need = max(0, min(1, self.social_need))

        if self.state == WANDERING:

            if self.wander_timer >= WANDER_TIME:
                self.target_vel_x = random.uniform(-MAX_VEL_X, MAX_VEL_X)
                self.target_vel_y = random.uniform(-MAX_VEL_Y, MAX_VEL_Y)
                self.wander_timer = 0
            else:
                self.wander_timer += 1
            
            if self.energy < 0.2 and self.state != RESTING:

                if fogueiras:
                    self.fogueira_alvo = random.choice(fogueiras)
                    self.target_pos = self.fogueira_alvo.get_ponto_aleatorio()

                    self.setEstado(RESTING)

            elif random.random() < 0.001:
                self.iniciar_mensagem(amigos)

            elif self.social_need > 0.6:
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

            if relacao > 0:
                if random.random() < 0.05 and self.social_need > 0.8: 
                    lider, seguidor = self.definir_lider(self.alvo_social)

                    lider.is_lider = True
                    seguidor.is_lider = False

                    lider.alvo_social = seguidor
                    seguidor.alvo_social = lider

                    lider.setEstado(GROUPING)
                    seguidor.setEstado(GROUPING)

            elif relacao <= -2 and random.random() < 0.1:
                self.setEstado(AVOIDING)
                print(f"{self.nome} decidiu evitar")

            else:
                if self.social_need > 0.8:
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
                relacao = self.relacoes.get(self.target_amigo, 0)

                if relacao < 0 and random.random() < 0.5:
                    self.interaction_type = "argumento"
                    print(self.interaction_type)
                    self.setEstado(ARGUMENTING)

                elif random.random() < 0.5 and len(self.relacoes) > 1:
                    
                    terceiros = [a for a in self.relacoes.keys() if a != self.target_amigo]

                    if terceiros:
                        self.alvo_fofoca = random.choice(terceiros)
                        self.opiniao = self.relacoes.get(self.alvo_fofoca, 0)
                        self.target_amigo.relacoes[self.alvo_fofoca] = self.target_amigo.relacoes.get(self.alvo_fofoca, 0) + self.opiniao * 0.5
                    self.interaction_type = "fofoca"
                    self.setEstado(GOSSIPING)

                else:
                    self.interaction_type = "normal"
                    self.setEstado(INTERACTING)

                self.talk_timer = 0

        if self.state == ARGUMENTING and self.target_amigo:

            outro = self.target_amigo

            self.talk_timer += 1

            if self.talk_timer > 180:
                self.relacoes[outro] = self.relacoes.get(outro, 0) - 1.5
                outro.relacoes[self] = outro.relacoes.get(self, 0) - 1.5
                self.finaliza_interacao()
                outro.finaliza_interacao()

        if self.state == GOSSIPING and self.target_amigo:

            outro = self.target_amigo

            self.vel_x *= 0.9
            self.vel_y *= 0.9

            self.talk_timer += 1

            if self.talk_timer > 120:
                self.finaliza_interacao()
                outro.finaliza_interacao()

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

        if self.state == MESSAGE:

            self.vel_x *= 0.9
            self.vel_y *= 0.9

            self.message_timer += 1

            if self.message_timer > 180: 
                self.mensagem = None
                self.setEstado(WANDERING)

        # if self.rect.bottom > ALTURA - 100 and self.target_vel_y > 0:
        #     self.target_vel_y = abs(self.target_vel_y)
        
        # if self.rect.top < 100 and self.target_vel_y < 0:
        #     self.target_vel_y *= -1

        angulo_max = 15

        self.angulo = (self.vel_x / MAX_VEL_X) * angulo_max

        vel_modulo = abs(self.vel_x) + abs(self.vel_y)

        if vel_modulo > 0.1:
            self.step_timer += self.vel_step * vel_modulo
        elif self.state == TALKING or self.state == GOSSIPING or self.state == ARGUMENTING:
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
        if self.acessorios["chapeu"]:
            chapeu = self.acessorios["chapeu"]
            chapeu_rot = pygame.transform.rotate(chapeu, -self.angulo)
            rect_chapeu = chapeu_rot.get_rect(midbottom=(self.rect.centerx, self.rect.y + self.offset_y + 30))
            janela.blit(chapeu_rot, rect_chapeu)

        if self.acessorios["item"]:
            item = self.acessorios["item"]
            item_rot = pygame.transform.rotate(item, -self.angulo)
            rect_item = item_rot.get_rect(center=(self.rect.centerx + 60, self.rect.centery + self.offset_y))
            janela.blit(item_rot, rect_item)
        if self.state == MESSAGE and self.mensagem:
    
            padding = 10
            texto = fonte5.render(self.mensagem, True, "black")

            largura = texto.get_width() + padding * 2
            altura = texto.get_height() + padding * 2

            x = self.rect.centerx - largura // 2
            y = self.rect.y - 60 + self.offset_y

            balao_rect = pygame.Rect(x, y, largura, altura)

            balao_rect = clamp_rect(balao_rect, LARGURA, ALTURA, 40)

            pygame.draw.rect(janela, (255, 255, 255), balao_rect, border_radius=8)
            pygame.draw.rect(janela, (0, 0, 0), balao_rect, 2, border_radius=8)

            janela.blit(texto, (balao_rect.x + padding, balao_rect.y + padding))

            ponta_x = self.rect.centerx - 2
            ponta_y = balao_rect.bottom - 2
            
            pygame.draw.polygon(janela, (0, 0, 0), [
                (ponta_x - 8, ponta_y),
                (ponta_x + 8, ponta_y),
                (ponta_x, ponta_y + 13)
            ])
            pygame.draw.polygon(janela, (255, 255, 255), [
                (ponta_x - 5, ponta_y),
                (ponta_x + 5, ponta_y),
                (ponta_x, ponta_y + 10)
            ])

        if self.state == FOLLOWING:
            rect_curioso = img_curioso.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_curioso, rect_curioso)
        
        if self.state == TALKING:
            rect_talking = img_talking.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_talking, rect_talking)
        
        if self.state == ARGUMENTING:
            rect_arguing = img_arguing.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            janela.blit(img_arguing, rect_arguing)
        
        if self.state == GOSSIPING and self.target_amigo and self.alvo_fofoca:
            img_alvo = pygame.transform.scale(self.alvo_fofoca.img, (36, 34))
            rect_alvo = img_alvo.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y - 40 + self.offset_y))
            rect_humor = img_positivo.get_rect(center=(self.rect.x + self.rect.width / 2 + 40, self.rect.y - 40 + self.offset_y))

            janela.blit(img_alvo, rect_alvo)
            if self.opiniao > 0:
                janela.blit(img_positivo, rect_humor)
            
            else:
                janela.blit(img_negativo, rect_humor)
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

        janela.blit(self.txt_criador, (hud_x + 18, 250))
        self.draw_bar(janela, hud_x + 18, 315, self.energy, "greenyellow")
        self.draw_bar(janela, hud_x + 18, 350, self.social_need, "dodgerblue3")

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
        
        if self.state == TALKING or self.state == GOSSIPING:
            janela.blit(img_conversando, (hud_x + 190, 30))

        elif self.state == ARGUMENTING and self.target_amigo:
            janela.blit(img_negativo, (hud_x + 190, 30))

        elif self.state == GROUPING and self.alvo_social:
            janela.blit(pygame.transform.scale(self.alvo_social.img, (36, 34)), (hud_x+ 190, 30))
        
        elif self.state == RESTING:
            janela.blit(img_zzz, (hud_x + 190, 30))
        
        elif (self.state == ARGUMENTING or self.state == AVOIDING) and (not "PSICOPATA" in self.personalidade and not "DIABOLICO" in self.personalidade):
            janela.blit(img_negativo, (hud_x + 190, 30))

        elif (self.state == ARGUMENTING or self.state == AVOIDING) and ("PSICOPATA" in self.personalidade or "DIABOLICO" in self.personalidade):
            janela.blit(img_maquiavelico, (hud_x + 190, 30))
        else:
            janela.blit(img_wandering, (hud_x + 190, 30))