from dino_ai.game.dino import Dino
from dino_ai.game.obstaculo import Obstaculo
from dino_ai.game.colisao import colisao
from dino_ai.game.sensores import ler_sensores
from dino_ai.neural_network import criar_rede, copiar_para_entrada, calcular_saida, copiar_da_saida, copiar_vetor_para_camadas

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
        self.rede = criar_rede(1,6,6,3)
        if dna is not None:
            copiar_vetor_para_camadas(self.rede, dna)
    
    def passo(self):
        self.obstaculo.mover(self.velocidade)

        if self.obstaculo.x + self.obstaculo.largura < 0:
            self.obstaculo.x = 400
        
        self.dino.atualizar()

        self.sensores = ler_sensores(self.dino, self.obstaculo, self.velocidade)
        copiar_para_entrada(self.rede, self.sensores)
        calcular_saida(self.rede)
        saidas = copiar_da_saida(self.rede)

        if saidas[0] != 0:
            self.dino.pular()
        if saidas[1] != 0:
            pass #abaixar

        if colisao(self.dino, self.obstaculo) == True:
            self.dino.morrer()

