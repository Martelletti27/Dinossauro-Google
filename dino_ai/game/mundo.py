from dino_ai.game.dino import Dino, CHAO
from dino_ai.game.obstaculo import Obstaculo
from dino_ai.game.colisao import colisao
from dino_ai.game.sensores import ler_sensores
from dino_ai.neural_network import criar_rede, copiar_para_entrada, calcular_saida, copiar_da_saida, copiar_vetor_para_camadas
from dino_ai.config import QTD_CAMADAS_ESCONDIDAS, QTD_INPUT, QTD_HIDE, QTD_OUTPUT
import random

class Mundo:
    def __init__(self, dna=None):
        self.dino = Dino()
        self.obstaculo = Obstaculo(
            x = 400,
            largura = 20,
            altura = 40,
            tipo = 0
        )
        self.velocidade = -3
        self.rede = criar_rede(QTD_CAMADAS_ESCONDIDAS,QTD_INPUT,QTD_HIDE,QTD_OUTPUT)
        if dna is not None:
            copiar_vetor_para_camadas(self.rede, dna)
    
    def passo(self):
        self.obstaculo.mover(self.velocidade)

        if self.obstaculo.x + self.obstaculo.largura < 0:
            self.obstaculo.x = random.randint(350,550)

            aleatorio = random.randint(0,2)
            if aleatorio == 1:
                self.obstaculo.largura = 20
                self.obstaculo.altura = 40
                self.obstaculo.y = CHAO
            elif aleatorio == 2:
                self.obstaculo.largura = 30
                self.obstaculo.altura = 25
                self.obstaculo.y = CHAO + 30
            else:
                self.obstaculo.largura = 30
                self.obstaculo.altura = 70
                self.obstaculo.y = CHAO
        
            self.obstaculo.tipo = aleatorio

        self.dino.atualizar()

        if colisao(self.dino, self.obstaculo) == True:
            self.dino.morrer()

        self.sensores = ler_sensores(self.dino, self.obstaculo, self.velocidade)
        copiar_para_entrada(self.rede, self.sensores)
        calcular_saida(self.rede)
        saidas = copiar_da_saida(self.rede)

        self.dino.abaixar(saidas[1] != 0)

        if saidas[0] != 0:
            self.dino.pular()

        if saidas[2] != 0:
            self.dino.usar_aviao()

        if abs(self.velocidade) < 8:
            self.velocidade = self.velocidade - 0.0005
        
        self.dino.atualizar_aviao(self.velocidade)



