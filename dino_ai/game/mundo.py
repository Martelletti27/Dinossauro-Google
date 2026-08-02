from dino_ai.game.dino import Dino
from dino_ai.game.obstaculo import Obstaculo
from dino_ai.game.colisao import colisao

class Mundo:
    def __init__(self):
        self.dino = Dino()
        self.obstaculo = Obstaculo(
            x = 400,
            largura = 20,
            altura = 40,
            tipo = 0
        )
        self.velocidade = -3
    
    def passo(self):
        self.obstaculo.mover(self.velocidade)
        self.dino.atualizar()
        if colisao(self.dino, self.obstaculo) == True:
            self.dino.morrer()
 