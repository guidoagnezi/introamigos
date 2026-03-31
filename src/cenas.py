import pygame
from settings import *
from cenario import *
from amigo import *
from slider import *
import tkinter as tk
from tkinter import filedialog
from inputBox import *
from botao import *
from fogueira import *
from arvore import *
from saveFile import *
class CenaAcampamento:
    def __init__(self, game):
        self.game = game

        self.mx, self.my = (0,0)
        self.already_following = False
        self.clique = False

        self.sprite_group_general = []
        self.sprite_group_amigo = []
        self.sprite_group_cenario = []
        self.fogueiras = []
        self.arvores = []

        self.carregar_assets()
        self.criar_cenarios()
        self.criar_amigos()
        self.criar_botoes()
        self.criar_fogueiras()
        self.criar_arvores()
    
    def criar_botoes(self):
        self.botao_confirmar = Botao(LARGURA/2 - 125, 700, self.img_botao_confirmar, "CRIAR AMIGO", self.cena_criacao)
        self.botao_save = Botao(5, 5, self.img_save, "", self.salvar_jogo)

    def carregar_assets(self):
        self.img = pygame.image.load("amigo/teste.png").convert_alpha()
        self.img2 = pygame.image.load("amigo/teste2.png").convert_alpha()
        self.img_fundo = pygame.image.load("fundo/fundo.png").convert_alpha()
        self.img_arb = pygame.image.load("fundo/arbusto.png").convert_alpha()
        self.img_botao_confirmar = pygame.image.load("fundo/confirmar_frame.png").convert_alpha()
        self.img_save = pygame.image.load("fundo/save_icon.png").convert_alpha()

    def criar_cenarios(self):
        arbusto = Cenario(self.img_arb, LARGURA/3, ALTURA/3)

        self.sprite_group_cenario.append(arbusto)
        self.sprite_group_general.append(arbusto)
    def criar_fogueiras(self):

        f = Fogueira(LARGURA/2, ALTURA/2)
        self.fogueiras.append(f)
        self.sprite_group_general.append(f)

    def criar_arvores(self):

        a = Arvore(pygame.image.load("fundo/arvore.png").convert_alpha(), 830, ALTURA - 600)
        self.arvores.append(a)
        self.sprite_group_general.append(a)

    def criar_amigos(self):
        # amigo = Amigo(self.img, "Guido")
        # amigo2 = Amigo(self.img2, "Xibo")

        # amigo3 = Amigo(pygame.image.load("amigo/lol.png").convert_alpha(), "Lude", "RESENHUDO INGENUO")
        # amigo4 = Amigo(pygame.image.load("amigo/jubilani.png").convert_alpha(), "Lude", "CARENTE BOM PRA NADA")
        # amigo5 = Amigo(pygame.image.load("amigo/peter.png").convert_alpha(), "Lude", "INGENUO PRA FRENTE")
        
        # self.sprite_group_amigo.append(amigo)
        # self.sprite_group_general.append(amigo)
        # self.sprite_group_amigo.append(amigo2)
        # self.sprite_group_general.append(amigo2)
        # self.sprite_group_amigo.append(amigo3)
        # self.sprite_group_general.append(amigo3)
        # self.sprite_group_amigo.append(amigo4)
        # self.sprite_group_general.append(amigo4)
        # self.sprite_group_amigo.append(amigo5)
        # self.sprite_group_general.append(amigo5)
        pass

    def adiciona_amigo(self, amigo):
        self.sprite_group_amigo.append(amigo)
        self.sprite_group_general.append(amigo)
        
    def cena_criacao(self):
        escolha = CenaCriadorAmigo(self.game, self)
        self.game.setCena(escolha)
    def salvar_jogo(self):
        s = self.game.save_file
        s.salvar_jogo(self.sprite_group_amigo)

    def recarregar(self, amigos):

        self.sprite_group_amigo.clear()
        self.sprite_group_general.clear()
        self.sprite_group_cenario.clear()
        self.fogueiras.clear()
        self.arvores.clear()

        self.carregar_assets()
        self.criar_cenarios()
        self.criar_botoes()
        self.criar_fogueiras()
        self.criar_arvores()

        self.sprite_group_amigo.extend(amigos)
        self.sprite_group_general.extend(amigos)

    def handle_events(self, event):
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mx, self.my = pygame.mouse.get_pos()
                self.clique = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # s = self.game.save_file
                    # s.salvar_jogo(self.sprite_group_amigo)
                    pass
            
                if event.key == pygame.K_l:
                    s = self.game.save_file
                    amigo_s = s.carregar_jogo()
                    self.recarregar(amigo_s)

            self.botao_confirmar.handle_event(event)
            self.botao_save.handle_event(event)
    def update(self):

            self.mx, self.my = pygame.mouse.get_pos()
            for amigo in self.sprite_group_amigo:
                amigo.update(self.sprite_group_amigo, self.fogueiras)
                if amigo.rect.collidepoint(self.mx, self.my) and self.clique:
                    pass

                
                    self.clique = False
                
                if amigo.state == FOLLOWING:
                    amigo.setTarget(self.mx, self.my)
                
                
            self.botao_confirmar.update()
            self.botao_save.update()
            for a in self.arvores:
                a.update(self.sprite_group_amigo)

    def draw(self, janela):
            
            self.sprite_group_general.sort(key= lambda obj: obj.rect.y + obj.rect.height)

            janela.fill("white")
            janela.blit(self.img_fundo, (0,0))
            
            for sprite in self.sprite_group_general:
                sprite.draw(janela)

            for amigo in self.sprite_group_amigo:
                if amigo.rect.collidepoint(self.mx, self.my):
                    amigo.draw_desc(janela)
            
            self.botao_confirmar.draw(janela)
            self.botao_save.draw(janela)
            pygame.display.update()

class CenaCriadorAmigo:
    def __init__(self, game, cena_acamp):
            self.game = game
            self.imagem_temp = None
            self.imagem_temp_quadro = None
            self.cena_acamp = cena_acamp

            self.personalidade = ""
            self.sprite_group_slider = []

            self.margem_esquerda = 15

            self.max_pontos = 25
            self.pontos_restantes = 0

            self.carregar_assets()
            self.criar_sliders()
            self.criar_botoes()
            self.criar_input_box()

    def carregar_assets(self):
        self.img_quadro_img_temp = pygame.image.load("fundo/frame_1.png").convert_alpha()
        self.img_quadro_img_temp = pygame.transform.scale_by(self.img_quadro_img_temp, 2).convert_alpha()
        self.rect_quadro = self.img_quadro_img_temp.get_rect(center=(LARGURA - 200, 200))

        self.img_titulo = pygame.image.load("fundo/titulo_criador.png").convert_alpha()
        self.rect_titulo = self.img_titulo.get_rect(topleft=(10,20))

        self.img_personalidade = pygame.image.load("fundo/titulo_personalidade.png").convert_alpha()
        self.rect_personalidade = self.img_titulo.get_rect(topleft=(self.margem_esquerda, 600))

        self.img_botao_confirmar = pygame.image.load("fundo/confirmar_frame.png").convert_alpha()
        self.img_botao_carregar = pygame.image.load("fundo/carregar_frame.png").convert_alpha()

        self.txt_nome = fonte2.render("NOME", True, "black").convert_alpha()
        self.rect_txt_nome = self.txt_nome.get_rect(topleft=(LARGURA - 340, 460))

    def criar_input_box(self):
        self.input_box = InputBox(LARGURA - 240, 460, 180, 40, tamanho_fonte=40)

    def criar_botoes(self):

        self.botao_confirmar = Botao(LARGURA - 340, 700, self.img_botao_confirmar, "CRIAR AMIGO", self.criar_amigo)

        self.botao_carregar_imagem = Botao(LARGURA - 340, 350, self.img_botao_carregar, "CARREGAR IMAGEM", self.selecionar_imagem, fonte=fonte4)
        
        self.botao_desenhar = Botao(LARGURA - 340, 400, self.img_botao_carregar, "DESENHAR AMIGO", self.abrir_canva, fonte=fonte4)

    def criar_sliders(self):
        self.sld_sim = Slider("SIMPATIA", self.margem_esquerda, 230, 500, 50, 10, 5)
        self.sld_vig = Slider("VIGARICE", self.margem_esquerda, 330, 500, 50, 10, 5)
        self.sld_cor = Slider("CORAGEM", self.margem_esquerda, 430, 500, 50, 10, 5)
        self.sld_pai = Slider("PAIXAO", self.margem_esquerda, 530, 500, 50, 10, 5)
        self.sprite_group_slider.append(self.sld_sim)
        self.sprite_group_slider.append(self.sld_vig)
        self.sprite_group_slider.append(self.sld_cor)
        self.sprite_group_slider.append(self.sld_pai)

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(
        title="Escolha uma imagem para o amigo",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
        )

        if caminho:
            try:
                self.imagem_temp = pygame.image.load(caminho).convert_alpha()
                self.imagem_temp_quadro = pygame.transform.scale(self.imagem_temp, (self.rect_quadro.
                width - 30, self.rect_quadro.height - 30)).convert_alpha()
                # self.imagem_temp = self.imagem_temp_quadro
            except pygame.error as e:
                print(f"Erro ao carregar: {e}")
    
    def criar_amigo(self):
        if self.imagem_temp:
            img = self.imagem_temp
            novo_amigo = Amigo(img, self.input_box.texto, self.personalidade)
            self.cena_acamp.adiciona_amigo(novo_amigo)
            self.game.setCena(self.cena_acamp)
    
    def abrir_canva(self):
        canva = CenaCanva(self.game, self)
        self.game.setCena(canva)

    def define_personalidade(self, atributos):

        atributos_norm = {k: v - 5 for k, v in atributos.items()}

        personalidades = {
            "MALANDRO":   {"simpatia": 0, "vigarice": 3, "paixao": 0, "coragem": 3},
            "RESENHUDO":  {"simpatia": 5, "vigarice": 0, "paixao": 0, "coragem": 1},
            "CARENTE":    {"simpatia": 3, "vigarice": 0, "paixao": 3, "coragem":-1},
            "PSICOPATA":  {"simpatia":-3, "vigarice": 2, "paixao":-2, "coragem": 0},
            "CINICO":     {"simpatia":-2, "vigarice": 3, "paixao":-1, "coragem": 0},
            "PRA FRENTE": {"simpatia": 0, "vigarice": 0, "paixao": 3, "coragem": 5},
            "DIABOLICO":  {"simpatia": 0, "vigarice": 5, "paixao": 0, "coragem": 0},
            "OBCECADO":   {"simpatia": 0, "vigarice": 0, "paixao": 5, "coragem": 0},
            "COVARDE":    {"simpatia": 0, "vigarice": 0, "paixao": 0, "coragem":-5},
            "INGENUO":    {"simpatia": 0, "vigarice":-5, "paixao": 0, "coragem":-5},
            "APATICO":    {"simpatia": 0, "vigarice": 0, "paixao":-5, "coragem": 0},

            "BOM PRA NADA": {
                "simpatia": "centro",
                "vigarice": "centro",
                "paixao": "centro",
                "coragem": "centro"
            }
        }

        scores = {}

        for nome, pesos in personalidades.items():
            score = 0

            for k in pesos:
                if pesos[k] == "centro":
                    score += -abs(atributos_norm[k]) 
                else:
                    score += pesos[k] * atributos_norm[k]

            if nome == "MALANDRO":
                if atributos_norm["vigarice"] > 2 and atributos_norm["coragem"] > 2:
                    score += 5

            if nome == "PSICOPATA":
                if all(v < -2 for v in atributos_norm.values()):
                    score += 8

            # quando o bichin é mediano
            if nome == "BOM PRA NADA":
                if all(-1 <= v <= 1 for v in atributos_norm.values()):
                    score += 6

            scores[nome] = score

        # print(scores, atributos_norm)

        ordenadas = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        top = [nome for nome, _ in ordenadas[:2]]

        top = list(set(top))

        prioridade_final = ["PRA FRENTE", "BOM PRA NADA"]

        top.sort(key=lambda nome: (nome in prioridade_final, nome))

        return " ".join(top)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        for slider in self.sprite_group_slider:
            slider.handle_event(event, self.sprite_group_slider, self.max_pontos)
        
        self.input_box.handle_event(event)
        self.botao_confirmar.handle_event(event)
        self.botao_carregar_imagem.handle_event(event)
        self.botao_desenhar.handle_event(event)

    def update(self):
        self.pontos_restantes = self.max_pontos - sum(s.valor for s in self.sprite_group_slider)
        
        if not self.imagem_temp or self.input_box.texto == "":
            self.botao_confirmar.setInatividade(True)
        else:
            self.botao_confirmar.setInatividade(False)

        self.botao_confirmar.update()
        self.botao_carregar_imagem.update()
        self.botao_desenhar.update()

        atributos = {
            "simpatia" : self.sld_sim.valor,
            "coragem" : self.sld_cor.valor,
            "vigarice" : self.sld_vig.valor,
            "paixao" : self.sld_pai.valor
        }
        # print(atributos)
        self.personalidade = self.define_personalidade(atributos)

    def draw(self, janela):
        janela.fill("white")
        
        txt_pt_rest = fonte2.render(f"PONTOS RESTANTES {self.pontos_restantes}", True, "black").convert_alpha()
        rect_txt_pt_rest = txt_pt_rest.get_rect(topleft=(self.margem_esquerda, 140))

        txt_personalidade_amigo = fonte2.render(self.personalidade, True, "black").convert_alpha()
        rect_txt_personalidade_amigo = txt_personalidade_amigo.get_rect(topleft=(self.margem_esquerda, 680))

        if self.imagem_temp:
            rect = self.imagem_temp_quadro.get_rect(center=self.rect_quadro.center)
            janela.blit(self.imagem_temp_quadro, rect)
        
        janela.blit(self.txt_nome, self.rect_txt_nome)

        janela.blit(self.img_quadro_img_temp, self.rect_quadro)
        janela.blit(self.img_titulo, self.rect_titulo)

        janela.blit(txt_pt_rest, rect_txt_pt_rest)
        janela.blit(self.img_personalidade, self.rect_personalidade)

        janela.blit(txt_personalidade_amigo, rect_txt_personalidade_amigo)
        for slider in self.sprite_group_slider:
            slider.draw(janela)
        
        self.botao_confirmar.draw(janela)
        self.botao_carregar_imagem.draw(janela)
        self.botao_desenhar.draw(janela)
        self.input_box.draw(janela)

class CenaCanva:
    def __init__(self, game, cena_criador):
        pygame.mouse.set_visible(False)
        self.game = game
        self.cena_criador = cena_criador

        self.canvas = pygame.Surface((500,500), pygame.SRCALPHA)

        self.rect_canvas = self.canvas.get_rect(center=(LARGURA/2, ALTURA/2))

        self.ferramenta = "pincel"

        self.desenhando = False
        self.cor_atual = (0, 0, 0)
        self.ultimo_ponto = None
        self.raio_pincel = 4

        self.historico = []
        self.max_historico = 10


        self.carregar_assets()
        self.criar_botoes()
        self.criar_borracha()

        

    def carregar_assets(self):
        self.fundo = pygame.image.load("fundo/fundo_canva.png").convert_alpha()
        self.fundo_rect = self.fundo.get_rect(center=(LARGURA/2, ALTURA/2))

        self.img_frame_confirmar = pygame.image.load("fundo/concluido_frame.png").convert_alpha()

        self.img_frame_pincel = pygame.image.load("fundo/frame_pincel.png").convert_alpha()
        self.img_frame_borracha = pygame.image.load("fundo/frame_borracha.png").convert_alpha()
        self.img_frame_bucket = pygame.image.load("fundo/frame_bucket.png").convert_alpha()
        self.img_frame_undo = pygame.image.load("fundo/frame_undo.png").convert_alpha()
        self.img_frame_pequeno = pygame.image.load("fundo/frame_pequeno.png").convert_alpha()
        self.img_frame_medio = pygame.image.load("fundo/frame_medio.png").convert_alpha()
        self.img_frame_grande = pygame.image.load("fundo/frame_grande.png").convert_alpha()
        self.img_frame_muito_grande = pygame.image.load("fundo/frame_muito_grande.png").convert_alpha()

        self.cursores = {
            "pincel": pygame.image.load("fundo/pincel.png").convert_alpha(),
            "borracha": pygame.image.load("fundo/borracha.png").convert_alpha(),
            "bucket": pygame.image.load("fundo/bucket.png").convert_alpha(),
        }

    def cria_superficie_paleta(self, cor):
        sur = pygame.Surface((33,33))
        sur.fill(cor)
        return sur

    def criar_botoes(self):
        
        self.botao_confirmar = Botao(LARGURA/2 - 200, ALTURA/2 + 260, self.img_frame_confirmar, "CONCLUIDO", self.concluir_cena, fonte=fonte4, cor_normal="white")

        self.botao_pincel = Botao(180, 150, self.img_frame_pincel, "", lambda: self.mudar_ferramenta("pincel"))
        self.botao_borracha = Botao(180, 230, self.img_frame_borracha, "", lambda: self.mudar_ferramenta("borracha"))
        self.botao_bucket = Botao(180, 310, self.img_frame_bucket, "", lambda: self.mudar_ferramenta("bucket"))

        self.botao_undo = Botao(180, 70, self.img_frame_undo, "", self.desfazer)

        primeiro = 400
        self.botao_pequeno = Botao(180, primeiro, self.img_frame_pequeno, "", lambda: self.mudar_tamanho(4))
        self.botao_medio =  Botao(180, primeiro + 80, self.img_frame_medio, "", lambda: self.mudar_tamanho(10))
        self.botao_grande =  Botao(180, primeiro + 160, self.img_frame_grande, "", lambda: self.mudar_tamanho(18))
        self.botao_muito_grande =  Botao(180, primeiro + 240, self.img_frame_muito_grande, "", lambda: self.mudar_tamanho(24))

        self.hud = [self.botao_borracha,
                    self.botao_pincel, 
                    self.botao_bucket,
                    self.botao_undo,

                    self.botao_confirmar, 

                    self.botao_pequeno, 
                    self.botao_medio, 
                    self.botao_grande, 
                    self.botao_muito_grande
                    ]
        
        # paleta
        
        cores = [
        "red",
        "darkred",
        "darkorange",
        "darkorange4",
        "yellow",
        "yellow3",
        "green1",
        "green4",
        "cyan",
        "cyan3",
        "blue",
        "blue4",
        "magenta1",
        "magenta4",
        "black",
        "gray58",
        "gray80",
        "azure",
        "darksalmon",
        "navajowhite",
        "saddlebrown",
        "coral4"

        ]

        
        for i, cor in enumerate(cores):
            x = 775 + (i % 2) * 40
            y = 150 + (i // 2) * 40

            botao = Botao(
                x, y,
                self.cria_superficie_paleta(cor),
                "",
                lambda c=cor: self.mudar_cor(c)
            )

            self.hud.append(botao)
        

    def criar_borracha(self):
        tamanho = self.raio_pincel * 2

        self.borracha_surface = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)

        pygame.draw.circle(
            self.borracha_surface,
            (0, 0, 0, 0), 
            (tamanho // 2, tamanho // 2),
            self.raio_pincel
        )
    
    def mudar_cor(self, cor):
        self.cor_atual = cor
    def cores_proximas(self, c1, c2, tol):
        return (
            abs(c1.r - c2.r) <= tol and
            abs(c1.g - c2.g) <= tol and
            abs(c1.b - c2.b) <= tol and
            abs(c1.a - c2.a) <= tol
        )
    
    def flood_fill(self, surface, x, y, nova_cor, tolerancia=0):
        largura, altura = surface.get_size()
        alvo = surface.get_at((x, y))

        if alvo == nova_cor:
            return

        stack = [(x, y)]
        visitados = set()

        while stack:
            px, py = stack.pop()

            if (px, py) in visitados:
                continue
            visitados.add((px, py))

            if px < 0 or px >= largura or py < 0 or py >= altura:
                continue

            cor_atual = surface.get_at((px, py))

            if not self.cores_proximas(cor_atual, alvo, tolerancia):
                continue

            surface.set_at((px, py), nova_cor)

            stack.append((px+1, py))
            stack.append((px-1, py))
            stack.append((px, py+1))
            stack.append((px, py-1))

    def mudar_tamanho(self, tamanho):
        self.raio_pincel = tamanho
        self.criar_borracha()
    def mudar_ferramenta(self, ferramenta):
        self.ferramenta = ferramenta

    def concluir_cena(self):
        self.cena_criador.imagem_temp = pygame.transform.scale(self.canvas, (150, 150))
        self.cena_criador.imagem_temp_quadro = pygame.transform.scale(self.cena_criador.imagem_temp, (self.cena_criador.rect_quadro.width - 30, self.cena_criador.rect_quadro.height - 30))
        self.game.setCena(self.cena_criador)
        pygame.mouse.set_visible(True)

    def salvar_estado(self):
        if len(self.historico) >= self.max_historico:
            self.historico.pop(0)

        self.historico.append(self.canvas.copy())
    def desfazer(self):
        if self.historico:
            self.canvas = self.historico.pop()
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_canvas.collidepoint(event.pos):

                self.salvar_estado()
                mx, my = event.pos
                x = mx - self.rect_canvas.x
                y = my - self.rect_canvas.y

                if self.ferramenta == "bucket":
                    self.flood_fill(self.canvas, x, y, self.cor_atual, tolerancia=10)
                else:
                    self.desenhando = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.desfazer()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.desenhando = False

        for b in self.hud: b.handle_event(event)

    def update(self):

        if self.desenhando:
            mx, my = pygame.mouse.get_pos()

            if self.rect_canvas.collidepoint((mx, my)):
                x = mx - self.rect_canvas.x
                y = my - self.rect_canvas.y

                if self.ultimo_ponto:

                    if self.ferramenta == "pincel":
                        dx = x - self.ultimo_ponto[0]
                        dy = y - self.ultimo_ponto[1]
                        dist = max(1, int((dx**2 + dy**2) ** 0.5))

                        for i in range(dist):
                            px = int(self.ultimo_ponto[0] + dx * i / dist)
                            py = int(self.ultimo_ponto[1] + dy * i / dist)

                            pygame.draw.circle(
                                self.canvas,
                                self.cor_atual,
                                (px, py),
                                self.raio_pincel
                            )

                    elif self.ferramenta == "borracha":

                        dx = x - self.ultimo_ponto[0]
                        dy = y - self.ultimo_ponto[1]
                        dist = max(1, int((dx**2 + dy**2) ** 0.5))

                        for i in range(dist):
                            px = int(self.ultimo_ponto[0] + dx * i / dist)
                            py = int(self.ultimo_ponto[1] + dy * i / dist)

                            self.canvas.blit(
                                self.borracha_surface,
                                (px - self.raio_pincel, py - self.raio_pincel),
                                special_flags=pygame.BLEND_RGBA_MULT
                            )

                self.ultimo_ponto = (x, y)
        else:
            self.ultimo_ponto = None

        for b in self.hud: b.update()

        # print(pygame.mouse.get_pos())

    def draw(self, janela):
        
        janela.fill("white")
        janela.blit(self.fundo, self.fundo_rect)
        janela.blit(self.canvas, self.rect_canvas)

        for b in self.hud: b.draw(janela)

        mx, my = pygame.mouse.get_pos()
        
        cor = self.cor_atual
        if self.cor_atual == "azure":
            cor = "black"
        pygame.draw.circle(
            janela,
            cor,
            (mx, my),
            self.raio_pincel,
            1,

        )

        cursor_img = self.cursores[self.ferramenta]
        
        rect = cursor_img.get_rect(bottomleft=(mx,my))
        janela.blit(cursor_img, rect)
        
class CenaTitulo:
    def __init__(self, game):
        self.slots = ["slot1", "slot2", "slot3"]
        self.game = game
        self.img = pygame.image.load("fundo/titulo_jogo.png").convert_alpha()
        self.rect = self.img.get_rect(center=(LARGURA/2, 200))
        self.sprite_group_botoes = []

        self.previews = {}
        self.carregar_assets()
        self.criar_botoes()
        self.criar_previews()
    
    def carregar_assets(self):

        self.img_apag = pygame.image.load("fundo/apagar.png").convert_alpha()

    def criar_botoes(self):
        x= LARGURA/2 - 150
        self.b_slot1 = Botao(x, ALTURA/2, img_carregar, "SLOT 1", lambda : self.carregar_save("slot1"), fonte4)
        self.b_slot2 = Botao(x, ALTURA/2 + 80, img_carregar, "SLOT 2", lambda : self.carregar_save("slot2"), fonte4)
        self.b_slot3 = Botao(x, ALTURA/2 + 160, img_carregar, "SLOT 3", lambda : self.carregar_save("slot3"), fonte4)
        
        self.b_apag1 = Botao(x + 290, ALTURA/2, self.img_apag, "", lambda : self.apagar_save("slot1"))
        self.b_apag2 = Botao(x + 290, ALTURA/2 + 80, self.img_apag, "", lambda : self.apagar_save("slot2"))
        self.b_apag3 = Botao(x + 290, ALTURA/2 + 160, self.img_apag, "", lambda : self.apagar_save("slot3"))

        self.sprite_group_botoes = [self.b_slot1, self.b_slot2, self.b_slot3,
                                    self.b_apag1, self.b_apag2, self.b_apag3]

    def criar_previews(self):
        for slot in self.slots:
            caminho = os.path.join("saves", slot, "save.json")
            # print(caminho)
            if os.path.exists(caminho):
                save = SaveFile(slot)

                try:
                    amigos = save.carregar_jogo()
                    self.previews[slot] = amigos
                except:
                    self.previews[slot] = []
            else:
                self.previews[slot] = []

    def apagar_save(self, slot):

        existe = os.path.exists(os.path.join("saves", slot, "save.json"))

        if existe:
            shutil.rmtree(f"saves/{slot}")
            self.criar_previews()

    def carregar_save(self, slot):

        existe = os.path.exists(os.path.join("saves", slot, "save.json"))
        
        save = SaveFile(slot)

        if existe:
            print("Carregando jogo")
            amigos = save.carregar_jogo()
        else:
            print("Criando Jogo")
            amigos = []
            save.salvar_jogo(amigos)

        self.game.save_file = save
        c = CenaAcampamento(self.game)
        c.recarregar(amigos)
        self.game.setCena(c)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for botao in self.sprite_group_botoes:
                botao.handle_event(event)

        return None
    
    def update(self):
        for b in self.sprite_group_botoes:
            b.update()

    
    def draw_preview_amigos(self, tela, amigos):
        if not amigos:
            # print("GUIDO")
            return

        tamanho = 80
        espacamento = 16

        x_base = 100
        y = 680
        for i, amigo in enumerate(amigos[:9]): 

            img = pygame.transform.scale(amigo.img, (tamanho, tamanho))

            x = x_base + i * (tamanho + espacamento)

            rect = img.get_rect(center=(x, y))

            tela.blit(img, rect)

    def draw(self, janela):

        janela.fill("white")
        janela.blit(self.img, self.rect)
        for b in self.sprite_group_botoes:
            b.draw(janela)
            if b.update():
                # print(self.previews)
                amigos = self.previews.get(b.texto.replace(" ", "").lower(), [])
                # print(amigos)
                # print(b.texto.replace(" ", "").lower())
                self.draw_preview_amigos(janela, amigos)
