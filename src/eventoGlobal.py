import pygame

class EventoGlobal:
    def __init__(self, nome, duracao, efeito_inicio, efeito_update, efeito_fim):
        self.nome = nome
        self.duracao = duracao
        try:
            self.img = pygame.image.load(f"fundo/{nome}.png").convert_alpha()
        except:
            self.img = pygame.image.load("fundo/titulo_jogo.png").convert_alpha()
        self.timer = 0
        self.efeito_inicio = efeito_inicio
        self.efeito_update = efeito_update
        self.efeito_fim = efeito_fim
        self.ativo = False
        self.transparencia = 255

        self.pos_y = self.img.get_height()
        self.target_y = 0
        self.vel_y = 0
        self.animando = False

    def iniciar(self, amigos):
        
        self.transparencia = 255
        self.img.set_alpha(self.transparencia)

        self.ativo = True
        self.timer = 0
        self.pos_y = self.img.get_height()
        self.animando = True
        self.efeito_inicio(amigos)

    def update(self, amigos):
        if not self.ativo:
            return
    
        self.timer += 1
        self.efeito_update(amigos)

        # ANIMAÇÃO SUAVE (ease-out)
        if self.animando:
            suavizacao = 0.08
            self.vel_y += (self.target_y - self.pos_y) * suavizacao
            self.vel_y *= 0.4  # amortecimento

            self.pos_y += self.vel_y

            # trava quando chega perto
            if abs(self.target_y - self.pos_y) < 0.5:
                self.pos_y = self.target_y
                self.vel_y = 0
                self.animando = False
        if not self.animando:
            self.transparencia -= 1
            self.img.set_alpha(self.transparencia)

        if self.timer >= self.duracao:
            self.efeito_fim(amigos)
            self.ativo = False
    
    def draw(self, janela):

        janela.blit(self.img, (0, self.pos_y))