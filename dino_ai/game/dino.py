# variaveis
CHAO = 15
GRAVIDADE = 0.08
IMPULSO_PULO = 4
EM_PE = 0
ABAIXADO = 1
PULANDO = 2
MORTO = 3


# Classe Dino
class Dino:
    def __init__(self):
        self.x = 100
        self.y = CHAO
        self.velocidade_y = 0
        self.estado = EM_PE
        self.fitness = 0
    
    def pular(self):
        if self.estado == MORTO:
            return
        if self.estado == PULANDO:
            return
        else:
            self.estado = PULANDO
            self.y = self.y + 1
            self.velocidade_y = self.velocidade_y + IMPULSO_PULO

    def atualizar(self):
        if self.estado == MORTO:
            return
        if self.y > CHAO:  ## no ar
            self.velocidade_y = self.velocidade_y - GRAVIDADE
            self.y = self.y + self.velocidade_y
        else:
            self.velocidade_y = 0
            self.y = CHAO
            if self.estado == PULANDO:
                self.estado = EM_PE

    def morrer(self):
        self.estado = MORTO
