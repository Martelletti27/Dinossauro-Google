# variaveis
from locale import delocalize


CHAO = 15
GRAVIDADE = 0.08
IMPULSO_PULO = 4
EM_PE = 0
ABAIXADO = 1
PULANDO = 2
MORTO = 3
VOANDO = 4

# Classe Dino
class Dino:
    def __init__(self):
        self.x = 100
        self.y = CHAO
        self.velocidade_y = 0
        self.estado = EM_PE
        self.fitness = 0
        self.cooldown = 0
        self.deslocamento = 0
    
    def pular(self):
        if self.estado == MORTO:
            return
        if self.estado == PULANDO:
            return
        if self.estado == VOANDO:
            return
        else:
            self.estado = PULANDO
            self.y = self.y + 1
            self.velocidade_y = self.velocidade_y + IMPULSO_PULO

    def atualizar(self):
        if self.estado == MORTO:
            return
        if self.y > CHAO:  ## no ar
            if self.estado != VOANDO:
                self.velocidade_y = self.velocidade_y - GRAVIDADE
            else:
                if self.velocidade_y <= 0:
                    self.velocidade_y = 0
                else:
                    self.velocidade_y = self.velocidade_y - GRAVIDADE
            self.y = self.y + self.velocidade_y
        else:
            self.velocidade_y = 0
            self.y = CHAO
            if self.estado == PULANDO:
                self.estado = EM_PE
        if self.estado == EM_PE or self.estado == ABAIXADO:
            self.fitness = self.fitness + 2
        else:
            self.fitness = self.fitness + 1

    def morrer(self):
        self.estado = MORTO

    def abaixar(self, ativo:bool):
        if self.estado == MORTO:
            return
        if self.estado == VOANDO:
            return
        if ativo:
            if self.estado == PULANDO:
                if self.velocidade_y > 0:
                    self.velocidade_y = 0
                self.y = self.y - 2
            else:
                self.estado = ABAIXADO
        else:
            if self.estado == ABAIXADO:
                self.estado = EM_PE

    def usar_aviao(self):
        if self.estado == MORTO or self.estado == VOANDO or self.cooldown >0:
            return
        self.estado = VOANDO
        self.y +=1
        if self.velocidade_y <= 0.5 and self.y < 25:
            self.velocidade_y += 4
        self.cooldown = 4000

    def atualizar_aviao(self, velocidade):
        passo_mundo = abs(velocidade)
        if self.estado == VOANDO:
            if self.deslocamento >= 820:
                self.deslocamento = 0
                self.estado = PULANDO
            else:
                self.deslocamento += passo_mundo
        self.cooldown -= passo_mundo