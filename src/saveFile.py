import pygame
import os
import json
import uuid
import shutil
from amigo import Amigo
class SaveFile:

    def __init__(self, nome):
        self.nome = nome
        self.caminho = os.path.join("saves", nome)

    def salvar_jogo(self, amigos):

        if os.path.exists(self.caminho):
            shutil.rmtree(self.caminho)

        os.makedirs(self.caminho)

        dados = {"amigos": []}

        for amigo in amigos:

            nome_img = f"{amigo.id}.png"
            caminho_img = os.path.join(self.caminho, nome_img)

            pygame.image.save(amigo.img, caminho_img)

            # 🔁 converte relacoes
            relacoes = {
                outro.id: valor
                for outro, valor in amigo.relacoes.items()
            }

            dados["amigos"].append({
                "id": amigo.id,
                "nome": amigo.nome,
                "x": amigo.rect.x,
                "y": amigo.rect.y,
                "state": amigo.state,
                "personalidade": amigo.personalidade,
                "energy": amigo.energy,
                "social_need": amigo.social_need,
                "relacoes": relacoes,
                "imagem": nome_img
            })

        with open(os.path.join(self.caminho, "save.json"), "w") as f:
            json.dump(dados, f, indent=4)
    
    def carregar_jogo(self):

        with open(os.path.join(self.caminho, "save.json"), "r") as f:
            dados = json.load(f)

        amigos = []
        id_map = {}

        # 🔹 PASSO 1 — criar amigos (sem relações ainda)
        for a in dados["amigos"]:
            caminho_img = os.path.join(self.caminho, a["imagem"])
            img = pygame.image.load(caminho_img).convert_alpha()

            amigo = Amigo(img, a["nome"], a["personalidade"])

            amigo.id = a["id"]
            amigo.rect.x = a["x"]
            amigo.rect.y = a["y"]
            amigo.state = "wandering"
            amigo.energy = a["energy"]
            amigo.social_need = a["social_need"]
            
            amigos.append(amigo)
            id_map[amigo.id] = amigo


        for amigo, data in zip(amigos, dados["amigos"]):
            amigo.relacoes = {
                id_map[outro_id]: valor
                for outro_id, valor in data["relacoes"].items()
                if outro_id in id_map
            }

        return amigos