import pygame
from enum import Enum
import tkinter as tk
from tkinter.filedialog import askopenfilename

root = tk.Tk()
root.withdraw()

LARGURA = 1424
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
MESSAGE = "message"

mensagens = {
    "padrao": [

        "Eu vou para Pasárgada.",
        "Café com pão, café com pão, café com pão",
        "{assunto}. E nunca se esqueça disso.",
        "{assunto} {assunto} {assunto} sahur.",
        "Invista todo seu dinheiro em imóveis.",
        "IntroAmigos nem é tão bom assim.",
        "Clássico!",
        "Já booooora.",
        "Olá!",
        "Que téééééééédio.",
        "Você já ouviu falar em {assunto}?.",
        "Oie!",
        "Que fome. Quero comer {comida}.",
        "Nunca desperdice {comida}.",
        "{assunto} é show de bola.",
        "{assunto} é o futuro.",
        "{comida} é o meu prato favorito!",
        "Você é um amigo, amigo.",
        "{criador} é bacana.",
        "{criador}. Que nome familiar.",
        "Que lindo cenário.",
        "Bem, estou de mãos atadas.",
        "Quem disse isso?",
        "Sou especialista em {assunto}, filho.",
        "Tome!",
        "{comida}... {comida}... {comida}!!!",
        "{criador} é um caboclo sabido.",
        "Será que {criador} se interessa por {assunto}?",
        "Será que {criador} já comeu {comida}?",
        "Atrás de você!",
        "Vi, vivi e ven... Er... Como era mesmo?",
        "*Cof cof*",
        "Todos os direitos reservados.",
        "Se torne {criador}.",
        "IntroAmigos é o jogo mais difícil do mundo.",
        "Mas que saco...",
        "int main()... Ops! Linguagem errada.",
        "A HÁ! Eu não sei ler.",
        "public class... Opa, tá errado isso.",
        "Sou particularmente fã de {assunto}",
        "Você já jogou IntroBattle?",
        "Algo ameaçador vive no CT 13.",
        "Que calor.",
        "Que frio.",
        "{criador} é o meu fornecedor favorito de {comida}.",
        "Eu venci.",
        "Mas eu me recuso.",
        "Visite o CT 13.",
        "Visite o stand do IntroComp!",
        "Imagine.",
        "Cale-se, cale-se, cale-se.",
        "Para ser sincero, {assunto} é mais importante que oxigênio.",
        "Cuidado ao atravessar a Reta da Penha.",
        "O que você sabe sobre {assunto}?",
        "É {assunto} ou nada.",
        "Meu nome é {nome}, é um prazer te conhecer.",
        "Ser {personalidade} é tão ruim assim?",
        "{personalidade} é o meu tipo.",
        "Que pasa contigo?",
        "É o especialista paiiiiii",
        "Fala de computador automática.",
        "Tá começando a vazar.",
        "Me chamam de {nome} \"{comida}\" {assunto}",
        "Fala filhote.",
        "Fala galera.",
        "Olá, me chamo {nome}.",
        "{nome}, gostei desse nome.",
        "{nome} é?... Você pode repetir?",
        "*assovia e dá um pulo*",
        "Tenha respeito por {assunto}, amigo.",
        "*gira 2 vezes e pisca o olhos*",
        "*começa a se coçar inteiro*",
        "{amigo} é um caboclo bacana",
        "Será que {amigo} se interessa por {assunto}?",
        "Eu e {amigo} vamos andar aleatóriamente por aí.",
        "Quero dividir {comida} com {amigo}.",
        "Você viu o que {inimigo} fez?",
        "{inimigo} é um BABACA MALDITO.",
        "Espero que {amigo} nunca caia nas garras de {inimigo}.",
        "Bizarro. {inimigo} não sabe nada de {assunto}.",
        "{inimigo} é um pulga de bunda.",
        "Falando sério. Felbs Chelbs Lelbs.",
        "{amigo}nelson.",
        "Será que {amigo} já comeu {comida}?",
        "Certeza que {inimigo} nunca nem comeu {comida}.",

        ],
    "psicopata": [
        "Mal eles sabem...",
        "Muohohoharhar.",
        "Urgh...",
        "Estou rodeado de palhaços.",
        "Mataria por um pouco de {comida} agora",
        "*pensamentos maquiavélicos*",
        "{nome} é um deus!",
        "Saia de perto de mim.",
        "Eu sou a única pessoa normal por aqui.",
        "*assovia olhando pros lados*",
        "Entre em pânico e venda todos os seus bens.",
        "{inimigo} terá um destino pior que a morte."
    ],
    "resenhudo": [
        "Bom diiiiiiaaaaa.",
        "Professor, meu problema é outro.",
        "O que que há, velhinho?",
        "{comida} é pica pô, tá maluco?",
        "Saboooooorrrrrrrr {comida}.",
        "{amigo} é o taaaaaaaaal rapeize."
    ],
    "carente": [
        "Sou tãaaao tristinho...",
        "Você pode conversar comigo?",
        "Ei, psiu, eeeiii.",
        "Alou, tem alguém aí?",
        "Alguém pra falar de {assunto}, por favor?",
        "Ei, olha eu aqui!",
        "Olha o que eu sei fazer.",
        "Affs.....",
        "*bufa e olha pra você*"
    ],
    "diabolico": [
        "Nyehehehehe!!",
        "Estou tramando.",
        "Hihihihihi",
        "Psiu, ouve só...",
        "*pensamentos diabólicos*",
        "*esfrega as mãos e ri baixinho*",
    ],
    "cinico": [
        "Me dê qualquer tópico. Eu domino.",
        "Sou jovem, jogo bola e danço.",
        "Eles têm mais dinheiro que talento.",
        "Possuo habilidades incríveis que você nem imagina.",
        "Esse pessoal aí só anda e conversa...",
        "Eu não tenho {comida} aqui comigo, pede pra outro.",
        "Me fale um assunto. Dobre e passe pro próximo.",
        "Falo cerca de 67 idiomas."
    ],
    "covarde": [
        "Errrrrrm....",
        "Vou nessa.",
        "Errrr.... Pessoal, acho que isso não é uma boa ideia.",
        "V-v-você ouviu i-i-i-isso?",
        "AAAAAAAAHH!!! Ah, não é nada na verdade.",
        "Você viu aquilo?? *aponta para um atrás de você*",
        "Eu vou ficar por aqui mesmo...",
        "Que susto...",

    ],
    "malandro": [
        "Ei, você aí, me dá um real.",
        "Me empresta um dinheiro.",
        "Abre a boca e fecha os olhos.",
        "Olha ali!!! *rouba uma unha do seu pé*",
        "Olha ali!!! *rouba um fio do seu cabelo*",
        "Olha ali!!! *corre, dá meia volta e finge que nada aconteceu*",
        "Olha ali!!! *retira a maldição do seu corpo*",
        "Olha ali!!! *te gira 180 graus*"
    ],

    "ingenuo": [

        "Hã? Alguém disse alguma coisa?",
        "Uuuuhhhh...",
        "Aqui tem 100 reais, me devolve depois.",
        "Haha.... Isso é muito verdade."
    ],



}


# Temporizadores

WANDER_TIME = 120
TALK_COOLDOWN_PADRAO = 600

# Velocidade e Posicao

SPAWN_LIMIT = 50
MAX_VEL_X = 2
MAX_VEL_Y = 2

HUD_WIDTH = 256

# Imagens constantes
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

# Fontes
pygame.font.init()
fonte = pygame.font.SysFont(None, 24)
fonte2 = pygame.font.Font("fonte/guidofontenasal.ttf", 26)
fonte3 = pygame.font.Font("fonte/guidofontenasal.ttf", 30)
fonte4 = pygame.font.Font("fonte/guidofontenasal.ttf", 20)
fonte5 = pygame.font.SysFont(None, 48)
fonte6 = pygame.font.Font("fonte/guidofontenasal.ttf", 12)
fonte7 = pygame.font.SysFont(None, 30)
